"""
backend/lambda_handler.py
HEPo — AWS Lambda Handler (API Gateway Proxy Integration)

Accepts a POST /detect request whose body is a JSON array of observation
objects (or {"observations": [...]}) and returns detected heat pockets.

Reuses backend/heat_pocket_detector.py without modification.
All validation rules (coordinate bounds, temperature range, time window,
cluster density, ΔT threshold) are enforced by the existing detector —
this handler does not weaken or bypass them.

Request body (either form accepted):
    [{"observationId": ..., "nodeId": ..., "timestamp": ...,
      "latitude": ..., "longitude": ..., "temperatureC": ..., ...}, ...]

    OR:

    {"observations": [...same array...]}

Response (200):
    {
        "pockets":   [...detected heat pocket objects...],
        "count":     <int>,
        "source":    "lambda",
        "inputCount": <int>
    }

Error responses:
    400  — malformed JSON or missing/wrong-typed observations field
    500  — unexpected internal error
"""

import json
import sys
import os

# Allow the handler to import from the same package directory whether invoked
# directly (e.g. sam local invoke) or as a Lambda function.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from heat_pocket_detector import detect_heat_pockets  # noqa: E402
from monte_carlo import generate_monte_carlo_observations  # noqa: E402


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------

def _response(status_code: int, body: dict) -> dict:
    """Build an API Gateway proxy-compatible response dict."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",    # permissive for local dev
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def _error(status_code: int, message: str) -> dict:
    return _response(status_code, {"error": message})


# ---------------------------------------------------------------------------
# Lambda entry-point
# ---------------------------------------------------------------------------

def handler(event: dict, context) -> dict:
    """
    Lambda handler — API Gateway Lambda proxy integration.

    Parameters
    ----------
    event : dict
        API Gateway proxy event. The JSON request body is in event["body"].
    context : LambdaContext
        AWS Lambda context object (unused; present for interface compatibility).

    Returns
    -------
    dict
        API Gateway proxy response with statusCode, headers, and body.
    """
    # ── CORS preflight ───────────────────────────────────────────────────────
    if event.get("httpMethod") == "OPTIONS":
        return _response(200, {"message": "OK"})

    # Generate fresh synthetic observations for the local demo.
    if (
        event.get("httpMethod") == "POST"
        and event.get("path", "").rstrip("/") == "/simulate"
    ):
        try:
            observations = generate_monte_carlo_observations()
            return _response(200, {
                "observations": observations,
                "count": len(observations),
                "source": "monte-carlo-simulation",
                "mode": "simulation",
            })
        except Exception as exc:
            print(f"[HEPo Lambda] Simulation error: {exc}", file=sys.stderr)
            return _error(500, "Internal server error during simulation.")

    # ── Parse request body ───────────────────────────────────────────────────
    raw_body = event.get("body") or ""
    if not raw_body:
        return _error(400, "Request body is required.")

    try:
        parsed = json.loads(raw_body)
    except (json.JSONDecodeError, ValueError) as exc:
        return _error(400, f"Invalid JSON in request body: {exc}")

    # Accept bare array OR {"observations": [...]}
    if isinstance(parsed, list):
        observations = parsed
    elif isinstance(parsed, dict):
        observations = parsed.get("observations")
        if observations is None:
            return _error(
                400,
                "Missing 'observations' key. Expected {\"observations\": [...]}"
                " or a bare JSON array."
            )
    else:
        return _error(
            400,
            "Request body must be a JSON array or an object with an 'observations' key."
        )

    if not isinstance(observations, list):
        return _error(400, "'observations' must be a JSON array.")

    # ── Run detection ────────────────────────────────────────────────────────
    try:
        pockets = detect_heat_pockets(observations)
    except Exception as exc:  # noqa: BLE001
        # Log to CloudWatch / SAM local stdout; do not expose internals to caller
        print(f"[HEPo Lambda] Detection error: {exc}", file=sys.stderr)
        return _error(500, "Internal server error during heat-pocket detection.")

    # ── Return results ───────────────────────────────────────────────────────
    return _response(200, {
        "pockets":    pockets,
        "count":      len(pockets),
        "inputCount": len(observations),
        "source":     "lambda",
    })

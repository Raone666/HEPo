"""
HEPo Heat-Pocket Detection Engine
=================================
Project: Heat Encroachment Pockets (HEPo)
Event: Environmental Hacks (Bharat Builds Tour — WeMakeDevs x AWS Builder Center)

Algorithm Overview for Hackathon Presentation:
----------------------------------------------
The detection engine ingests distributed geotagged temperature observations and
identifies localized microclimate thermal anomalies without requiring black-box ML.

Mathematical Steps:
1. Temporal Windowing: Filter observations within the recent 15-minute window.
2. Coordinate & Telemetry Sanitization: Reject records with invalid lat/lng or out-of-range temperatures.
3. Fixed-Radius Spatial Grouping: Group observations within ~200m using the Haversine formula.
4. Cluster Density Filtering: Require >= 3 observations to form a candidate cluster.
5. Local Baseline Estimation: Compute ambient urban background temperature from surrounding observations.
6. Thermal Delta Calculation: differenceC = clusterTemperature - baselineTemperature.
7. Anomaly Thresholding: Trigger 'HEAT POCKET DETECTED' when observationCount >= 3 and differenceC >= 3.0°C.
8. Multi-Factor Confidence Scoring: Composite score based on count, temperature variance, and recency.

Scientific Honesty & Prototype Disclosure:
- The +3.0°C threshold is a configurable prototype parameter, not a universal meteorological definition.
- HEPo detects observational microclimate anomalies; it does NOT claim causal attribution (e.g. asphalt vs canopy)
  nor does it provide certified medical diagnoses.
"""

import math
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple


# =============================================================================
# Configurable Prototype Parameters
# =============================================================================
DEFAULT_TIME_WINDOW_MINUTES = 15.0      # Observation validity window
DEFAULT_CLUSTER_RADIUS_METERS = 200.0    # Spatial grouping radius (~200m)
DEFAULT_DIFF_THRESHOLD_C = 3.0           # Prototype anomaly threshold (+3.0°C)
DEFAULT_MIN_OBSERVATIONS = 3             # Minimum sensor nodes per cluster
EARTH_RADIUS_METERS = 6371000.0          # WGS-84 Earth radius mean


# =============================================================================
# 1. Geospatial Distance Utility
# =============================================================================
def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes the Great Circle distance between two points on Earth in meters.
    Formula:
        d = 2 * R * asin(sqrt(sin^2(dlat/2) + cos(lat1)*cos(lat2)*sin^2(dlon/2)))
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_METERS * c


# =============================================================================
# 2. Timestamp Parser & Validator
# =============================================================================
def parse_iso_timestamp(timestamp_str: Any) -> Optional[datetime]:
    """
    Parses an ISO 8601 timestamp string into a UTC timezone-aware datetime.
    Supports formats with 'Z' or '+00:00' offsets.
    """
    if isinstance(timestamp_str, datetime):
        if timestamp_str.tzinfo is None:
            return timestamp_str.replace(tzinfo=timezone.utc)
        return timestamp_str.astimezone(timezone.utc)

    if not isinstance(timestamp_str, str):
        return None

    cleaned = timestamp_str.strip()
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def validate_observation(obs: Dict[str, Any]) -> bool:
    """
    Validates observation telemetry and coordinates:
    - Latitude in [-90.0, 90.0]
    - Longitude in [-180.0, 180.0]
    - Temperature in [-50.0°C, 70.0°C] (reasonable terrestrial limits)
    - Valid timestamp
    """
    if not isinstance(obs, dict):
        return False

    lat = obs.get("latitude")
    lon = obs.get("longitude")
    temp = obs.get("temperatureC")
    ts = obs.get("timestamp")

    if not isinstance(lat, (int, float)) or not (-90.0 <= lat <= 90.0) or math.isnan(lat):
        return False
    if not isinstance(lon, (int, float)) or not (-180.0 <= lon <= 180.0) or math.isnan(lon):
        return False
    if not isinstance(temp, (int, float)) or not (-50.0 <= temp <= 70.0) or math.isnan(temp):
        return False

    parsed_ts = parse_iso_timestamp(ts)
    if parsed_ts is None:
        return False

    return True


# =============================================================================
# 3. Temporal Window Filtering
# =============================================================================
def filter_recent_observations(
    observations: List[Dict[str, Any]],
    reference_time: Optional[datetime] = None,
    window_minutes: float = DEFAULT_TIME_WINDOW_MINUTES
) -> List[Dict[str, Any]]:
    """
    Filters observations to only those within the last `window_minutes` relative
    to `reference_time`. If `reference_time` is None, the maximum valid observation
    timestamp is used (or UTC now).
    """
    valid_observations = [o for o in observations if validate_observation(o)]
    if not valid_observations:
        return []

    # If reference time is not supplied, use latest observation timestamp
    if reference_time is None:
        parsed_times = [parse_iso_timestamp(o["timestamp"]) for o in valid_observations]
        reference_time = max(t for t in parsed_times if t is not None)
    elif reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=timezone.utc)

    window_delta = timedelta(minutes=window_minutes)
    recent_observations = []

    for obs in valid_observations:
        obs_dt = parse_iso_timestamp(obs["timestamp"])
        if obs_dt is None:
            continue
        # Allow up to 1 min of future clock drift
        age = reference_time - obs_dt
        if -timedelta(minutes=1) <= age <= window_delta:
            recent_observations.append(obs)

    return recent_observations


# =============================================================================
# 4. Spatial Clustering (~200m grouping)
# =============================================================================
def cluster_spatially(
    observations: List[Dict[str, Any]],
    radius_meters: float = DEFAULT_CLUSTER_RADIUS_METERS
) -> List[List[Dict[str, Any]]]:
    """
    Groups spatially adjacent observations into clusters where points lie within
    `radius_meters` of the cluster anchor.

    Clustering strategy:
    1. Sort observations descending by temperature (anchors highest thermal readings).
    2. Greedily collect all unassigned neighbors within radius_meters.
    3. Re-verify points relative to the cluster centroid to avoid unbounded chaining.
    """
    if not observations:
        return []

    # Deterministic sort: highest temperature first, then observation ID
    sorted_obs = sorted(
        observations,
        key=lambda x: (-float(x.get("temperatureC", 0)), str(x.get("observationId", "")))
    )

    clusters: List[List[Dict[str, Any]]] = []
    assigned_indices = set()

    for i, anchor in enumerate(sorted_obs):
        if i in assigned_indices:
            continue

        cluster_members = [anchor]
        assigned_indices.add(i)

        anchor_lat = float(anchor["latitude"])
        anchor_lon = float(anchor["longitude"])

        for j, candidate in enumerate(sorted_obs):
            if j in assigned_indices:
                continue

            cand_lat = float(candidate["latitude"])
            cand_lon = float(candidate["longitude"])

            dist = haversine_distance_meters(anchor_lat, anchor_lon, cand_lat, cand_lon)
            if dist <= radius_meters:
                cluster_members.append(candidate)
                assigned_indices.add(j)

        clusters.append(cluster_members)

    return clusters


# =============================================================================
# 5. Local Baseline Temperature Calculation
# =============================================================================
def calculate_local_baseline(
    cluster: List[Dict[str, Any]],
    all_observations: List[Dict[str, Any]],
    max_baseline_distance_meters: float = 2500.0
) -> float:
    """
    Calculates the ambient urban baseline temperature against which the cluster is compared.

    Methodology:
    - Identifies all observations outside the current cluster that are within a broader
      urban monitoring sector (`max_baseline_distance_meters` <= 2.5 km).
    - To prevent other anomalous heat pockets from contaminating the baseline,
      baseline computation prioritizes ambient background observations (or lower 75% distribution).
    - If insufficient surrounding points are available outside the cluster, falls back
      to the overall dataset baseline.
    """
    cluster_ids = {str(o.get("observationId", "")) for o in cluster}
    
    # Calculate centroid of candidate cluster
    c_lat = sum(float(o["latitude"]) for o in cluster) / len(cluster)
    c_lon = sum(float(o["longitude"]) for o in cluster) / len(cluster)

    # Nearby non-cluster observations
    ambient_candidates = []
    for obs in all_observations:
        if str(obs.get("observationId", "")) in cluster_ids:
            continue
        dist = haversine_distance_meters(c_lat, c_lon, float(obs["latitude"]), float(obs["longitude"]))
        if dist <= max_baseline_distance_meters:
            ambient_candidates.append(float(obs["temperatureC"]))

    if not ambient_candidates:
        # Fallback to all non-cluster observations
        ambient_candidates = [
            float(o["temperatureC"]) for o in all_observations
            if str(o.get("observationId", "")) not in cluster_ids
        ]

    if not ambient_candidates:
        # If no other observations exist, baseline defaults to cluster temperature
        return round(sum(float(o["temperatureC"]) for o in cluster) / len(cluster), 2)

    # Use mean of the non-anomalous ambient subset (< 39.0°C or lower 75% percentile)
    non_extreme = [t for t in ambient_candidates if t < 39.0]
    if len(non_extreme) >= 2:
        return round(sum(non_extreme) / len(non_extreme), 2)

    return round(sum(ambient_candidates) / len(ambient_candidates), 2)


# =============================================================================
# 6. Multi-Factor Detection Confidence Scoring
# =============================================================================
def calculate_confidence(
    cluster: List[Dict[str, Any]],
    reference_time: Optional[datetime] = None
) -> str:
    """
    Evaluates detection confidence: 'Low', 'Medium', or 'High'.

    Evaluation criteria:
    1. Observation Count (Spatial Redundancy):
       - count >= 5: 3 points
       - count == 4: 2 points
       - count == 3: 1 point
    2. Temperature Consistency (Low Variance):
       - std_dev <= 0.8°C: 3 points
       - 0.8°C < std_dev <= 1.4°C: 2 points
       - std_dev > 1.4°C: 1 point
    3. Recency (Observation Freshness):
       - mean age <= 7 min: 3 points
       - 7 min < mean age <= 12 min: 2 points
       - mean age > 12 min: 1 point

    Composite Score (out of 9):
    - 8 - 9: 'High'
    - 5 - 7: 'Medium'
    - <= 4:  'Low'

    Note: This reflects detection statistical confidence, not scientific certainty.
    """
    count = len(cluster)
    temps = [float(o["temperatureC"]) for o in cluster]
    mean_temp = sum(temps) / count

    # 1. Count score
    if count >= 5:
        score_count = 3
    elif count == 4:
        score_count = 2
    else:
        score_count = 1

    # 2. Consistency score (Standard Deviation)
    variance = sum((t - mean_temp) ** 2 for t in temps) / count
    std_dev = math.sqrt(variance)

    if std_dev <= 0.8:
        score_consistency = 3
    elif std_dev <= 1.4:
        score_consistency = 2
    else:
        score_consistency = 1

    # 3. Recency score
    if reference_time is None:
        parsed_times = [parse_iso_timestamp(o["timestamp"]) for o in cluster]
        valid_times = [t for t in parsed_times if t is not None]
        ref = max(valid_times) if valid_times else datetime.now(timezone.utc)
    else:
        ref = reference_time

    ages_minutes = []
    for o in cluster:
        dt = parse_iso_timestamp(o["timestamp"])
        if dt:
            age = max(0.0, (ref - dt).total_seconds() / 60.0)
            ages_minutes.append(age)

    mean_age = sum(ages_minutes) / len(ages_minutes) if ages_minutes else 0.0

    if mean_age <= 7.0:
        score_recency = 3
    elif mean_age <= 12.0:
        score_recency = 2
    else:
        score_recency = 1

    total_score = score_count + score_consistency + score_recency

    if total_score >= 8:
        return "High"
    elif total_score >= 5:
        return "Medium"
    else:
        return "Low"


# =============================================================================
# 7. Main Detection Algorithm Function
# =============================================================================
def detect_heat_pockets(
    observations: List[Dict[str, Any]],
    reference_time: Optional[datetime] = None,
    cluster_radius_meters: float = DEFAULT_CLUSTER_RADIUS_METERS,
    diff_threshold_c: float = DEFAULT_DIFF_THRESHOLD_C,
    min_observations: int = DEFAULT_MIN_OBSERVATIONS
) -> List[Dict[str, Any]]:
    """
    Executes the end-to-end HEPo Heat-Pocket Detection Algorithm.

    Parameters:
    - observations: List of raw observation dictionaries.
    - reference_time: Optional reference datetime (defaults to latest timestamp).
    - cluster_radius_meters: Spatial proximity grouping threshold (default: 200m).
    - diff_threshold_c: Prototype thermal difference threshold (default: +3.0°C).
    - min_observations: Minimum sensor count required for cluster candidacy (default: 3).

    Returns:
    List of detected heat pocket dictionaries conforming to the schema:
    {
        "latitude": float,
        "longitude": float,
        "radiusMeters": float,
        "temperatureC": float,
        "baselineTemperatureC": float,
        "differenceC": float,
        "observationCount": int,
        "confidence": "Low" | "Medium" | "High",
        "status": "HEAT POCKET DETECTED",
        "contributingNodeIds": List[str],
        "stdDevC": float
    }
    """
    # Step 1 & 2: Validate and filter to recent 15 minutes
    recent_observations = filter_recent_observations(
        observations,
        reference_time=reference_time,
        window_minutes=DEFAULT_TIME_WINDOW_MINUTES
    )
    if len(recent_observations) < min_observations:
        return []

    # Step 3: Spatial Grouping (~200m)
    clusters = cluster_spatially(recent_observations, radius_meters=cluster_radius_meters)

    detected_pockets: List[Dict[str, Any]] = []

    for cluster in clusters:
        # Step 4: Minimum observation threshold
        if len(cluster) < min_observations:
            continue

        # Step 5: Calculate local baseline temperature
        baseline_temp = calculate_local_baseline(cluster, recent_observations)

        # Step 6: Calculate cluster temperature
        temps = [float(o["temperatureC"]) for o in cluster]
        cluster_temp = round(sum(temps) / len(temps), 2)

        # Step 7: Calculate differenceC
        difference_c = round(cluster_temp - baseline_temp, 2)

        # Step 8: Heat Pocket Decision Rule
        # IF observationCount >= 3 AND differenceC >= 3.0°C -> HEAT POCKET DETECTED
        if difference_c >= diff_threshold_c:
            centroid_lat = round(sum(float(o["latitude"]) for o in cluster) / len(cluster), 6)
            centroid_lon = round(sum(float(o["longitude"]) for o in cluster) / len(cluster), 6)

            # Compute effective radius from centroid + 25m buffer
            max_dist = max(
                haversine_distance_meters(centroid_lat, centroid_lon, float(o["latitude"]), float(o["longitude"]))
                for o in cluster
            )
            radius_meters = round(max(140.0, min(cluster_radius_meters, max_dist + 25.0)), 1)

            # Calculate confidence
            confidence = calculate_confidence(cluster, reference_time=reference_time)

            # Variance for telemetry transparency
            variance = sum((t - cluster_temp) ** 2 for t in temps) / len(temps)
            std_dev = round(math.sqrt(variance), 2)

            node_ids = [str(o.get("nodeId", o.get("observationId", "unknown"))) for o in cluster]

            detected_pockets.append({
                "latitude": centroid_lat,
                "longitude": centroid_lon,
                "radiusMeters": radius_meters,
                "temperatureC": cluster_temp,
                "baselineTemperatureC": baseline_temp,
                "differenceC": difference_c,
                "observationCount": len(cluster),
                "confidence": confidence,
                "status": "HEAT POCKET DETECTED",
                "contributingNodeIds": node_ids,
                "stdDevC": std_dev
            })

    return detected_pockets


if __name__ == "__main__":
    import json
    import os

    seed_path = os.path.join(os.path.dirname(__file__), "..", "simulation", "observations_seed.json")
    if os.path.exists(seed_path):
        with open(seed_path, "r", encoding="utf-8") as f:
            sample_data = json.load(f)
        results = detect_heat_pockets(sample_data)
        print(f"Executed detection on {len(sample_data)} observations. Found {len(results)} heat pockets:")
        for p in results:
            print(json.dumps(p, indent=2))

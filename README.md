# HEPo 🌡️
### Heat Encroachment Pockets

<p align="center">
  <img src="https://img.shields.io/badge/Status-Experimental-yellow?style=flat-square" alt="Experimental prototype" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/AWS-SAM%20Local-FF9900?style=flat-square&logo=amazonaws&logoColor=white" alt="AWS SAM Local" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License" />
</p>

<p align="center">
  <b>A little map. A local temperature difference. A potential heat pocket.</b>
  <br />
  Exploring localized urban heat patterns through simulated geospatial observations.
</p>

<p align="center">
  <a href="https://github.com/Raone666/HEPo">Repository</a> ·
  <a href="#getting-started">Run locally</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#credits--open-source">Credits</a>
</p>

---

## `hepo --about`

```text
     _   _ _____ ____        _
    | | | | ____|  _ \   ___| |
    | |_| |  _| | |_) | / _ \ |
    |  _  | |___|  __/ |  __/ |
    |_| |_|_____|_|     \___|_|

    HEAT ENCROACHMENT POCKETS
    Pronounced: "hippo"

    PROJECT    :: Environmental Hacks
    EVENT      :: Bharat Builds Tour
    TRACK      :: Heat and Water
    INTERFACE  :: Progressive Web App
    COMPUTING  :: Python + AWS SAM Local
    DATA       :: SYNTHETIC / SIMULATION
    DEPLOYMENT :: LOCAL DEVELOPMENT
```

HEPo is an experimental Progressive Web App (PWA) exploring how geotagged temperature observations could help identify and visualize localized urban heat anomalies.

A city-wide temperature reading cannot describe every street, shaded walkway, or concrete-heavy block. HEPo explores a different question:

> Where might temperatures differ significantly between nearby locations?

**Important:** The current prototype uses synthetic observations. It does not collect verified live temperatures from physical sensors, and its displayed heat pockets are demonstrations of a detection workflow, not evidence of actual environmental conditions.

Built for **Environmental Hacks · Bharat Builds Tour**, organized by **WeMakeDevs × AWS Builder Center**.

## `01 / the problem`

Urban heat is not uniform. Nearby locations can experience different thermal conditions because of factors such as:

- Tree cover and shade.
- Concrete, asphalt, and other heat-retaining surfaces.
- Building density and street geometry.
- Traffic and human activity.
- Vegetation and local airflow.

Weather forecasts and regional measurements remain useful, but they may not represent every small-scale variation in an urban area.

Outdoor workers, delivery couriers, pedestrians, event organizers, and urban planners could benefit from better localized environmental information.

HEPo is a small prototype for exploring how such information might be organized and visualized.

## `02 / the approach`

The current workflow combines synthetic observations, spatial grouping, baseline comparison, and map visualization.

```text
       SYNTHETIC OBSERVATIONS
                 |
                 v
        VALIDATE THE INPUT
                 |
                 v
        GROUP NEARBY POINTS
                 |
                 v
       ESTIMATE LOCAL BASELINE
                 |
                 v
        COMPARE TEMPERATURES
                 |
                 v
       IDENTIFY POTENTIAL POCKETS
                 |
                 v
         DISPLAY ON THE MAP
```

The detection engine uses configurable rules to evaluate observations and return contextual information such as cluster temperature, baseline temperature, temperature difference, observation count, and a heuristic confidence classification.

These rules are experimental. Their scientific accuracy has not been established through field measurements.

## `03 / features`

### Interactive geospatial map

- Leaflet-based map interface.
- OpenStreetMap basemap.
- Geographically positioned demonstration observations.
- Visual exploration of detected heat pockets.
- Contextual information about the observations and detection results.

### Synthetic data generator

- Monte Carlo-style simulation of temperature observations.
- Demonstration dataset containing 26 observations across four zones.
- Temperature, humidity, timestamp, and geographic coordinates.
- Explicit simulation metadata.
- A **Refresh Simulation** control to request another dataset.

The simulated coordinates and temperatures must not be interpreted as verified real-world measurements.

### Heat-pocket detection

The current configured detection parameters are:

| Parameter | Value |
|---|---:|
| Observation time window | 15 minutes |
| Approximate clustering radius | 200 metres |
| Minimum observations per cluster | 3 |
| Minimum temperature anomaly | +3.0°C above baseline |

The detector uses spatial and temperature comparisons to identify potential anomalies. Its confidence labels are heuristic classifications, not statistically validated probabilities.

### Progressive Web App

- Responsive browser interface.
- Web app manifest.
- Service-worker support.
- Application-shell caching for supported offline use.
- Desktop and mobile browser access.

Local API requests and uncached external map tiles may require connectivity.

### Local serverless API

The repository includes an AWS SAM template and a Python Lambda handler exposing two routes:

| Route | Purpose |
|---|---|
| `POST /simulate` | Generate synthetic observations |
| `POST /detect` | Process submitted observations and return detection results |

The routes can be tested locally using AWS SAM CLI and Docker.

**Local SAM execution is not an AWS cloud deployment.** No public API, persistent cloud database, or production infrastructure is implied by this prototype.

## `04 / architecture`

```text
                         LOCAL MACHINE
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   Browser                                                │
│      │                                                   │
│      v                                                   │
│   PWA / Leaflet Map                                      │
│      │                                                   │
│      │ HTTP                                              │
│      v                                                   │
│   AWS SAM Local API                                      │
│      │                                                   │
│      ├──────── POST /simulate ────────┐                  │
│      │                                v                  │
│      │                         Monte Carlo              │
│      │                         Generator                 │
│      │                                │                  │
│      │                                v                  │
│      │                         Simulated Data            │
│      │                                                   │
│      └──────── POST /detect ──────────┐                  │
│                                       v                  │
│                               Heat-Pocket Detector       │
│                                       │                  │
│                                       v                  │
│                               Detection Results          │
│                                                          │
│   Docker provides the container environment for SAM.    │
└──────────────────────────────────────────────────────────┘
```

The frontend also contains client-side detection logic. Therefore, the results shown on the map should not automatically be described as output from the server-side `/detect` endpoint.

The current workflow is intended for local development and testing.

## `05 / technology`

| Technology | Role | Reference |
|---|---|---|
| Python | Simulation and detection logic | [Python](https://www.python.org/) |
| Python standard library | Backend functionality without additional detector dependencies | [Python documentation](https://docs.python.org/3/) |
| JavaScript | Browser-side application logic | [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript) |
| HTML and CSS | Interface and presentation | [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web) |
| Leaflet | Interactive maps | [Leaflet](https://leafletjs.com/) |
| OpenStreetMap | Map data and basemap | [OpenStreetMap](https://www.openstreetmap.org/) |
| PWA manifest and service worker | Installability and application-shell caching | [Web.dev](https://web.dev/learn/pwa/) |
| AWS SAM CLI | Serverless build and local API testing | [AWS SAM](https://github.com/aws/aws-sam-cli) |
| AWS Lambda interface | Handler execution model | [AWS Lambda](https://aws.amazon.com/lambda/) |
| Docker | Containerized local build and execution | [Docker](https://www.docker.com/) |
| Git | Version control | [Git](https://git-scm.com/) |
| GitHub | Source hosting and collaboration | [GitHub](https://github.com/) |

## `06 / getting started`

### Requirements

Install or configure:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- A modern web browser

The Lambda runtime is configured for Python 3.12. Using Docker for the SAM build avoids depending on the host's default Python version.

### 1. Clone the repository

```bat
git clone https://github.com/Raone666/HEPo.git
cd HEPo
```

If you already have the repository cloned, navigate to its directory instead.

### 2. Start Docker Desktop

Wait until the Docker engine is running, then check the installed tools:

```bat
git --version
python --version
docker --version
sam --version
```

### 3. Validate and build

Run these commands from the repository root:

```bat
sam validate --lint
sam build --use-container
```

The first command validates the SAM template. The second builds the application in a compatible container environment.

### 4. Start the local API

In the first Command Prompt window:

```bat
sam local start-api --host 127.0.0.1 --port 3000
```

Keep this window running.

### 5. Start the frontend

Open a second Command Prompt window in the repository root:

```bat
python -m http.server 8000 --directory frontend
```

Keep this window running too.

### 6. Open HEPo

Visit:

**http://127.0.0.1:8000**

Use **Refresh Simulation** to request a fresh synthetic dataset from the local API.

To stop either process, press `Ctrl+C` in its terminal.

Both addresses use `127.0.0.1`, which refers to your own computer. They are local development endpoints, not public services.

## `07 / API reference`

### `POST /simulate`

Generates a new synthetic observation dataset.

Example request:

```bat
curl.exe -i -X POST http://127.0.0.1:3000/simulate -H "Content-Type: application/json" -d "{}"
```

A successful response contains fields similar to:

```json
{
  "observations": [
    "... generated observation objects ..."
  ],
  "count": 26,
  "source": "monte-carlo-simulation",
  "mode": "simulation"
}
```

The observation objects above are abbreviated for documentation. The actual endpoint returns generated data.

### `POST /detect`

Accepts either a JSON array of observations or an object containing an `observations` array.

Example request body:

```json
{
  "observations": [
    {
      "observationId": "example-001",
      "nodeId": "example-node-001",
      "timestamp": "2026-10-11T10:00:00Z",
      "latitude": 28.7505,
      "longitude": 77.1168,
      "temperatureC": 35.2,
      "mode": "simulation"
    }
  ]
}
```

This example illustrates the request format. A single observation is not sufficient to satisfy the configured minimum cluster size.

Save a complete request body as `observations.json`, then run the following command from the directory containing that file:

```bat
curl.exe -i -X POST http://127.0.0.1:3000/detect -H "Content-Type: application/json" --data-binary "@observations.json"
```

The response includes the detection results and associated counts and metadata.

### HTTP status codes

| Status | Meaning |
|---|---|
| `200` | Request processed successfully |
| `400` | Missing, malformed, or invalid request data |
| `500` | Unexpected server-side error |

These endpoints are available only while the local SAM API is running.

## `08 / validation`

Validate the SAM template:

```bat
sam validate --lint
```

Check Python syntax:

```bat
python -m py_compile backend\lambda_handler.py backend\monte_carlo.py backend\heat_pocket_detector.py
```

Build the application:

```bat
sam build --use-container
```

Test the simulation route after starting the local API:

```bat
curl.exe -i -X POST http://127.0.0.1:3000/simulate -H "Content-Type: application/json" -d "{}"
```

Basic validation confirms that selected commands run successfully. It does not establish comprehensive test coverage, scientific accuracy, or production readiness.

## `09 / limitations`

HEPo is a prototype, with several important limitations:

- **Synthetic data:** Current demonstration observations are generated by simulation, not collected from physical sensors.
- **No verified live conditions:** The map does not establish current temperatures at the displayed coordinates.
- **Experimental detection:** Clustering rules and confidence classifications have not been scientifically validated.
- **No calibrated sensor network:** Future real-world inputs would require calibration, quality checks, and validation.
- **No assumed cloud deployment:** Local AWS SAM testing does not mean the application has been deployed to AWS.
- **Network dependencies:** Local API requests and uncached external map tiles may require connectivity.

HEPo is not a certified environmental monitoring platform or a substitute for official heat-risk guidance.

## `10 / roadmap`

Possible future improvements:

- Integrate validated environmental datasets or calibrated sensor readings.
- Evaluate detection performance against reference measurements.
- Improve spatial clustering and local baseline estimation.
- Add historical comparisons and trend visualization.
- Improve offline functionality and accessibility.
- Evaluate secure cloud deployment and persistent storage.
- Gather feedback from potential users.

These are future possibilities, not claims about existing functionality.

## `11 / credits & open source`

HEPo builds on work from open-source communities and tools. Their work deserves recognition alongside the development tools used to build this prototype.

### Open-source foundations

| Project | Contribution | Project reference |
|---|---|---|
| Python | Programming language and standard library | [Python](https://www.python.org/) |
| Leaflet | Interactive mapping library | [Leaflet repository](https://github.com/Leaflet/Leaflet) |
| OpenStreetMap | Community-maintained geographic data | [OpenStreetMap](https://www.openstreetmap.org/) |
| AWS SAM CLI | Open-source tooling for serverless applications and local testing | [AWS SAM CLI repository](https://github.com/aws/aws-sam-cli) |
| Git | Distributed version control | [Git project](https://git-scm.com/) |

OpenStreetMap data is provided under the Open Database License (ODbL). Map usage and attribution must follow the applicable OpenStreetMap requirements. Other projects retain their own licenses and attribution requirements.

The list above identifies major direct technologies. It is not a complete inventory of every transitive dependency. Consult the relevant project repositories and license files for the exact terms that apply.

### AI-assisted development tools

- **[Google Antigravity](https://antigravity.google/)** — Antigravity CLI assisted the development workflow.
- **[AWS Kiro](https://kiro.dev/)** — Kiro CLI assisted implementation and development tasks.

These tools supported development. Their mention does not imply that they are open-source projects or that their providers sponsor or endorse HEPo.

### Event acknowledgement

Built for **Environmental Hacks · Bharat Builds Tour**, organized by **WeMakeDevs × AWS Builder Center**.

### Design inspiration

The terminal-inspired presentation takes inspiration from [Andrew Grant (@Andrew6rant)](https://github.com/Andrew6rant). The visual approach is adapted for HEPo rather than copied from the original implementation.

Thank you to the maintainers, contributors, and communities who make these tools possible.

## `12 / repository map`

```text
HEPo/
├── backend/       # Simulation API and detection logic
├── frontend/      # Browser interface and PWA assets
├── simulation/    # Simulation-related project resources
├── tests/         # Test-related project resources
├── docs/          # Documentation
├── template.yaml  # AWS SAM application template
├── LICENSE        # Project license
├── .gitignore
└── README.md
```

This is a high-level directory map. Individual files and subdirectories may change as development continues.

## `13 / license`

HEPo is distributed under the MIT License. See [`LICENSE`](LICENSE) for the full license text.

The project license applies to HEPo's own code; third-party software, data, and services remain subject to their respective terms.

---

<p align="center">
  <b>HEPo</b>
  <br />
  Exploring the small differences that a city-wide average can hide.
  <br />
  <sub>One simulated observation at a time.</sub>
</p>

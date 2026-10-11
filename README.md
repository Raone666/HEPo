# HEPo 🌡️
### Heat Encroachment Pockets

**Pronounced:** *“hippo”*

[![Project](https://img.shields.io/badge/Project-Environmental%20Hacks-orange)](https://github.com/Raone666/HEPo)
[![Runtime](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![AWS SAM](https://img.shields.io/badge/AWS-SAM%20Local-FF9900)](https://docs.aws.amazon.com/serverless-application-model/)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow)](https://github.com/Raone666/HEPo)

**Built for:** Environmental Hacks · Bharat Builds Tour  
**Organized by:** WeMakeDevs × AWS Builder Center  
**Track:** Heat and Water · Localized Urban Heat Pockets

HEPo is a Progressive Web App (PWA) that explores how distributed, geotagged temperature observations can help identify and visualize localized urban heat anomalies.

Instead of treating an entire city as if it experiences the same temperature, HEPo focuses on differences between nearby locations and makes potential heat pockets easier to explore on an interactive map.

> **Important:** The current prototype uses synthetic simulation data, not readings from physical sensors. Its map results demonstrate the detection workflow and do not represent verified live environmental conditions.

---

## 🌍 The Problem

Urban heat is not distributed evenly.

Two locations only a few hundred metres apart can experience different thermal conditions because of:

- Limited shade and tree cover
- Roads, concrete, and other heat-retaining surfaces
- Building density and urban geometry
- Traffic and human activity
- Differences in local vegetation and airflow

Regional weather reports are useful, but they may not capture every small-scale variation within a city.

For outdoor workers, delivery couriers, pedestrians, and urban planners, understanding these local differences could support better-informed decisions.

**HEPo explores how localized temperature observations can make these patterns easier to identify and visualize.**

## 💡 The Solution

HEPo combines synthetic temperature observations, spatial clustering, local baseline comparison, and interactive geospatial visualization.

The intended workflow is:

1. Generate or receive geotagged temperature observations.
2. Validate observation fields and timestamps.
3. Group observations that are geographically close.
4. Compare cluster temperatures with a nearby baseline.
5. Identify potential heat anomalies using configurable rules.
6. Visualize the observations and detected pockets on a map.

The prototype provides contextual information such as temperature difference, observation count, and a heuristic confidence classification.

## 👥 Who Is HEPo For?

HEPo is designed with the following potential users in mind:

- Outdoor workers and delivery couriers
- Pedestrians and urban residents
- Event organizers
- Environmental teams
- Urban planners and researchers

**The question HEPo aims to explore:**

*Where might localized heat conditions differ significantly from nearby surroundings?*

HEPo is an experimental visualization tool, not a certified heat-safety service.

---

## ✨ Features

### 🗺️ Interactive Heat Map

- Leaflet-based interactive map
- OpenStreetMap basemap
- Geographically positioned temperature observations
- Heat-pocket visualization and contextual details
- Map controls for exploring detected areas

### 🧪 Synthetic Data Simulation

- Monte Carlo generator for simulated temperature observations
- 26 observations generated across four demonstration zones
- Temperature, humidity, timestamp, and geographic coordinates
- Explicit simulation metadata
- Refresh Simulation control for generating a new dataset

The example coordinates are demonstration locations, not verified measurements of real-world heat conditions.

### 🔎 Heat-Pocket Detection

The Python detection engine evaluates nearby observations and compares cluster temperatures with a local baseline.

The configured rules include:

| Parameter | Configured value |
|---|---|
| Observation time window | 15 minutes |
| Approximate clustering radius | 200 metres |
| Minimum observations per cluster | 3 |
| Minimum temperature anomaly | +3.0°C above baseline |

The engine also reports contextual information such as cluster temperature, baseline temperature, temperature difference, observation count, and confidence.

These are prototype detection rules. Their performance has not been established through scientific field validation.

### 📱 Progressive Web App

- Responsive browser interface
- Web app manifest
- Service-worker support
- Application-shell caching for supported offline use
- Desktop and mobile browser access

Some features, including requests to the local API and uncached map tiles, require network connectivity.

### ☁️ AWS SAM Local Integration

The repository includes an AWS SAM template defining a Python Lambda handler with two API routes:

- `POST /simulate` generates synthetic observations.
- `POST /detect` accepts observations and returns detection results.

The API can be tested locally using Docker and AWS SAM CLI. **This does not mean HEPo has been deployed to AWS.**

---

## 🏗️ Architecture

### Local development workflow

```text
                Docker Desktop
                      │
                      ▼
                AWS SAM Local
                      │
             ┌────────┴────────┐
             ▼                 ▼
       POST /simulate      POST /detect
             │                 │
             ▼                 ▼
       Monte Carlo        Python Heat-Pocket
        Generator            Detector
             │                 │
             ▼                 ▼
     Synthetic Readings   Detection Results
             │
             ▼
        Browser-based PWA
             │
             ▼
      Interactive Leaflet Map
```

The browser requests synthetic observations from the local simulation endpoint and updates the visualization. The detection endpoint separately supports server-side processing of submitted observations.

The frontend also includes client-side detection logic. The map's displayed results should therefore not automatically be interpreted as results returned by the `/detect` endpoint.

### Local versus cloud execution

AWS SAM CLI and Docker support local development and testing of the Lambda function.

The current documented workflow does not require a deployed public API. No cloud deployment, persistent cloud database, or production monitoring should be assumed unless those components are explicitly configured and deployed.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| Python | Simulation and heat-pocket detection |
| JavaScript | Frontend logic and visualization |
| HTML and CSS | User interface |
| Leaflet | Interactive geospatial mapping |
| OpenStreetMap | Basemap tiles |
| PWA manifest and service worker | Installability and application-shell caching |
| AWS SAM CLI | Serverless build and local API testing |
| AWS Lambda | Serverless handler interface |
| Docker | Container-based SAM build and local execution |
| Git and GitHub | Version control and source hosting |

---

## 🚀 Getting Started

### Prerequisites

Install or configure:

- [Git](https://git-scm.com/)
- [Python](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- A modern web browser

The Lambda function is configured for Python 3.12. Docker-based SAM builds can provide the compatible build environment without requiring Python 3.12 to be your default Windows installation.

### 1. Clone the repository

```bat
git clone https://github.com/Raone666/HEPo.git
cd HEPo
```

If you already have the repository, navigate to its directory instead.

### 2. Start Docker Desktop

Start Docker Desktop and wait until its engine is ready.

Verify the SAM installation:

```bat
sam --version
docker --version
```

### 3. Validate and build the SAM application

From the repository root:

```bat
sam validate --lint
sam build --use-container
```

The validation command checks the SAM template. The build command uses a containerized environment compatible with the configured Lambda runtime.

### 4. Start the local API

In the first Command Prompt window:

```bat
sam local start-api --host 127.0.0.1 --port 3000
```

Keep this terminal open while using the application.

### 5. Start the frontend

Open a second Command Prompt window:

```bat
python -m http.server 8000 --directory frontend
```

Keep this terminal open too.

### 6. Open HEPo

Visit:

**http://127.0.0.1:8000**

Use **Refresh Simulation** to request fresh synthetic observations from the local API.

To stop either process, press `Ctrl+C` in its terminal.

> These endpoints use `127.0.0.1`, which refers to your own machine. They are for local development, not public internet access.

---

## 🔌 API Reference

### `POST /simulate`

Generates a new synthetic observation dataset.

**Example request:**

```bat
curl.exe -X POST http://127.0.0.1:3000/simulate -H "Content-Type: application/json" -d "{}"
```

The successful response includes fields similar to:

```json
{
  "observations": [],
  "count": 26,
  "source": "monte-carlo-simulation",
  "mode": "simulation"
}
```

The empty array above is illustrative; the actual response contains generated observations.

### `POST /detect`

Accepts either a JSON array of observations or an object containing an `observations` array.

**Example request body:**

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

This illustrates the request shape; an individual observation may not be sufficient to form a detected heat pocket.

**Windows CMD example:**

Save your observation payload as `observations.json` in the current directory, then run:

```bat
curl.exe -X POST http://127.0.0.1:3000/detect -H "Content-Type: application/json" --data-binary "@observations.json"
```

The response includes the detected pockets, the number of pockets, the input observation count, and the response source.

### Expected status codes

| Status | Meaning |
|---|---|
| `200` | Request processed successfully |
| `400` | Missing, malformed, or invalid request data |
| `500` | Unexpected server-side error |

These endpoints are available only while the local SAM API is running.

---

## 🧪 Validation

The following commands check the SAM template and Python syntax:

```bat
sam validate --lint
python -m py_compile backend\lambda_handler.py backend\monte_carlo.py backend\heat_pocket_detector.py
```

Build the Lambda function using Docker:

```bat
sam build --use-container
```

Test the simulation endpoint after starting the local API:

```bat
curl.exe -i -X POST http://127.0.0.1:3000/simulate -H "Content-Type: application/json" -d "{}"
```

A successful response should contain the simulation mode and generated observations.

These commands provide basic validation. They do not, by themselves, establish comprehensive test coverage or scientific detection accuracy.

---

## ⚠️ Limitations

HEPo is a prototype, and its current limitations are important:

- **Synthetic observations:** No physical sensor readings are currently represented by the simulation.
- **No verified live conditions:** Example coordinates and temperatures are not a live environmental feed.
- **No deployed cloud service:** The documented AWS workflow is local SAM development and testing.
- **Heuristic detection:** Thresholds and confidence classifications require evaluation against ground-truth measurements.
- **Sensor calibration:** Future integration of phone-derived or physical sensor data would require careful calibration, quality control, and validation.
- **Network dependencies:** Uncached external map tiles and local API requests may require connectivity.

HEPo is not a certified environmental monitoring platform, medical tool, or substitute for official heat-risk guidance.

---

## 🧭 Future Work

Potential next steps include:

- Integrating validated environmental datasets or calibrated sensors
- Evaluating detection accuracy against reference measurements
- Improving baseline estimation and spatial clustering
- Adding historical heat-pattern comparisons
- Improving offline functionality and accessibility
- Evaluating secure cloud deployment and persistent storage
- Collecting feedback from potential users such as outdoor workers and urban planners

These items are planned possibilities, not claims about features already delivered.

---

## 🤖 Development Tools and Acknowledgements

HEPo was developed with assistance from AI-powered development tools:

- **[Google Antigravity](https://antigravity.google/)** — AI-assisted development workflow and coding support.
- **[AWS Kiro](https://kiro.dev/)** — AI-assisted development and implementation support.

These tools supported the development process. Project design decisions, integration, testing, and validation remain responsibilities of the project developer.

The project is built for the **Environmental Hacks — Bharat Builds Tour**, organized by **WeMakeDevs × AWS Builder Center**.

Thanks to the open-source communities behind Python, Leaflet, OpenStreetMap, and the other technologies used in this project.

---

## 📁 Repository Structure

```text
HEPo/
├── backend/
│   ├── heat_pocket_detector.py
│   ├── lambda_handler.py
│   └── monte_carlo.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── service-worker.js
│   └── manifest.webmanifest
├── docs/
│   └── architecture.md
├── template.yaml
├── .gitignore
└── README.md
```

This is a representative project structure. Verify file names against the repository before relying on this listing; additional files and tests may exist.

## 📄 License

Check the repository for a `LICENSE` file. If no license has been added, the project should not be described as having an open-source license until one is chosen and committed.

---

**HEPo — making localized urban heat patterns easier to explore, one simulated observation at a time.**

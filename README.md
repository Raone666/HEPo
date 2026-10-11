# HEPo 🌡️

### Heat Encroachment Pockets

*Pronounced “hippo”.*

[![Project](https://img.shields.io/badge/Project-Environmental%20Hacks-orange)](https://github.com/Raone666/HEPo)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![AWS SAM](https://img.shields.io/badge/AWS-SAM%20Local-FF9900)](https://github.com/aws/serverless-application-model)
[![Status](https://img.shields.io/badge/Status-Prototype-yellow)](https://github.com/Raone666/HEPo)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Built for:** Environmental Hacks · Bharat Builds Tour  
**Organized by:** WeMakeDevs × AWS Builder Center  
**Track:** Heat and Water · Localized Urban Heat Pockets

HEPo is a Progressive Web App (PWA) exploring how geotagged temperature observations can help identify and visualize localized urban heat anomalies.

Instead of treating a city as a single temperature reading, HEPo examines differences between nearby locations, compares spatial clusters against a local baseline, and displays potential heat pockets on an interactive map.

> [!IMPORTANT]
> **HEPo currently uses synthetic simulation data.** It does not measure live environmental conditions or receive readings from physical sensors. Its visualizations demonstrate a prototype workflow, not verified real-world heat conditions.

## Contents

- [Problem](#problem)
- [Approach](#approach)
- [Features](#features)
- [Architecture](#architecture)
- [Technology and acknowledgements](#technology-and-acknowledgements)
- [Getting started](#getting-started)
- [API reference](#api-reference)
- [Validation](#validation)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Problem

Urban heat varies across a city. Locations separated by only a few hundred metres can experience different thermal conditions because of factors such as:

- Tree cover and shade availability
- Roads, concrete, and other heat-retaining surfaces
- Building density and urban geometry
- Traffic and human activity
- Vegetation and local airflow

Regional weather reports provide useful context, but they may not capture every small-scale variation within an urban area.

For outdoor workers, delivery couriers, pedestrians, event organizers, and urban planners, understanding these local differences could support better-informed decisions.

HEPo explores the technical workflow behind identifying such differences from distributed observations.

## Approach

The prototype combines synthetic observations, spatial clustering, local baseline comparison, and geospatial visualization.

The intended processing pipeline is:

1. Generate or receive geotagged temperature observations.
2. Validate observation fields and timestamps.
3. Group geographically nearby observations.
4. Estimate a local baseline from surrounding observations.
5. Identify potential anomalies using configurable thresholds.
6. Return detection results and visualize the data on a map.

The prototype reports contextual information such as cluster temperature, baseline temperature, temperature difference, observation count, and a heuristic confidence classification.

The current implementation demonstrates this pipeline with generated data. Real-world detection accuracy has not been scientifically validated.

## Features

### 🗺️ Interactive map

- Leaflet-based geospatial visualization
- OpenStreetMap basemap
- Geographically positioned synthetic observations
- Heat-pocket visualization and contextual details
- Browser-based interface for exploring simulated results

### 🧪 Synthetic observation generator

- Monte Carlo simulation of temperature observations
- 26 observations across four demonstration zones
- Temperature, humidity, timestamps, and geographic coordinates
- Explicit simulation metadata
- Refresh Simulation control for requesting a new dataset

The generated locations and readings are illustrative. They should not be interpreted as measurements from actual streets or sensors.

### 🔎 Heat-pocket detection

The Python detection engine compares spatial clusters against a nearby baseline.

| Parameter | Configured value |
|---|---:|
| Observation time window | 15 minutes |
| Approximate clustering radius | 200 metres |
| Minimum observations per cluster | 3 |
| Minimum temperature anomaly | +3.0°C above baseline |

These values are prototype configuration choices, not scientifically established safety thresholds.

### 📱 Progressive Web App

- Responsive browser interface
- Web app manifest
- Service-worker support
- Application-shell caching for supported offline use
- Desktop and mobile browser access

Local API requests and uncached external map tiles may require network connectivity.

### ☁️ Local AWS serverless workflow

The repository includes an AWS SAM template and a Python Lambda handler exposing two routes:

- `POST /simulate` generates synthetic observations.
- `POST /detect` accepts observations and returns detection results.

AWS SAM CLI and Docker support local builds and testing. **The documented workflow does not imply that HEPo has been deployed to AWS.**

## Architecture

```text
                   Browser
                      |
                      v
                HEPo Frontend
                      |
             +--------+--------+
             |                 |
             v                 v
      POST /simulate     Client-side logic
             |                 |
             v                 v
       Monte Carlo       Map visualization
        Generator
             |
             v
     Synthetic observations


       Local AWS SAM API
             |
       +-----+-----+
       |           |
       v           v
   /simulate     /detect
       |           |
       v           v
   Generator    Python detector
                   |
                   v
            Detection results
```

The frontend requests synthetic observations from the local simulation endpoint and updates its visualization. The backend detection endpoint separately supports server-side processing of submitted observations.

The frontend also contains client-side detection logic. Results displayed by the map should not automatically be assumed to have come from the backend `/detect` endpoint.

### Local execution versus cloud deployment

The local development workflow uses AWS SAM CLI and Docker to build and run the serverless application on the developer's machine.

The current project does not claim to provide:

- A deployed public API
- A persistent cloud database
- Production monitoring
- Verified live environmental measurements

Those capabilities would require additional implementation, configuration, testing, and deployment.

## Technology and acknowledgements

HEPo builds on existing software, open standards, and developer tools. This section distinguishes the open-source projects used by the prototype from managed services and development assistants.

### Application and infrastructure

| Technology | Purpose |
|---|---|
| [Python](https://www.python.org/) | Simulation and detection logic |
| [Leaflet](https://leafletjs.com/) | Interactive maps |
| [OpenStreetMap](https://www.openstreetmap.org/) | Geographic map data |
| [AWS Serverless Application Model (SAM)](https://github.com/aws/serverless-application-model) | Serverless application definition and local development |
| [AWS Lambda](https://aws.amazon.com/lambda/) | Serverless execution interface targeted by the handler |
| [Docker](https://www.docker.com/) | Container tooling for local builds and execution |
| [Git](https://git-scm.com/) | Version control |
| [GitHub](https://github.com/) | Source hosting and collaboration |

Open-source projects and services are not interchangeable categories. AWS Lambda is a managed cloud service, while Docker Desktop is a product built using a broader ecosystem of technologies. Their inclusion here acknowledges their role without implying that every component is open source.

### AI-assisted development

The implementation workflow also used command-line AI development tools:

- [Google Antigravity](https://antigravity.google/) — AI-assisted development and coding workflow.
- [AWS Kiro](https://kiro.dev/) — AI-assisted development, code exploration, and implementation support.

These tools assisted development; they are not being presented as project sponsors or as substitutes for testing and verification. The project developer remains responsible for reviewing, integrating, and validating the resulting code.

### Open-source acknowledgements

Thanks to the maintainers and contributors of Python, Leaflet, OpenStreetMap, AWS SAM, and the wider open-source ecosystem that makes projects like HEPo possible.

Please refer to each project's official licensing and attribution requirements. OpenStreetMap data attribution is particularly important when publishing map-based applications.

## Getting started

### Prerequisites

Install or configure the following:

- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- A modern web browser

The Lambda function is configured for Python 3.12. A container-based SAM build can provide the compatible build environment without requiring Python 3.12 to be your default Windows installation.

The commands below use **PowerShell**.

### 1. Clone the repository

```powershell
git clone https://github.com/Raone666/HEPo.git
Set-Location HEPo
```

If you already have the repository, navigate to its existing directory instead:

```powershell
Set-Location "$HOME\Documents\GitHub\HEPo"
```

### 2. Check the development tools

Start Docker Desktop and wait for its engine to become ready.

```powershell
git --version
python --version
docker --version
sam --version
```

### 3. Validate and build

Run these commands from the repository root:

```powershell
sam validate --lint
sam build --use-container
```

The first command validates the SAM template. The second builds the application using a containerized environment compatible with the configured Lambda runtime.

### 4. Start the local API

In the first PowerShell terminal:

```powershell
sam local start-api --host 127.0.0.1 --port 3000
```

Leave this terminal running.

### 5. Start the frontend

Open a second PowerShell terminal and navigate to the repository root.

```powershell
Set-Location "$HOME\Documents\GitHub\HEPo"
python -m http.server 8000 --directory frontend
```

Leave this terminal running too.

### 6. Open HEPo

Visit:

<http://127.0.0.1:8000>

Use **Refresh Simulation** to request a new synthetic dataset from the local API.

To stop either server, press `Ctrl+C` in its terminal.

> Both services bind to `127.0.0.1`, making them available locally on your own machine. This setup is intended for development, not public internet access.

## API reference

The endpoints below are available while the local SAM API is running.

### `POST /simulate`

Generates a synthetic observation dataset.

**PowerShell example:**

```powershell
$body = '{}' 

Invoke-RestMethod `
    -Uri 'http://127.0.0.1:3000/simulate' `
    -Method Post `
    -ContentType 'application/json' `
    -Body $body
```

A successful response includes fields similar to:

```json
{
  "observations": [],
  "count": 26,
  "source": "monte-carlo-simulation",
  "mode": "simulation"
}
```

The empty `observations` array above is illustrative. The actual response contains generated observations.

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

This example illustrates the request structure. A single observation is not sufficient to satisfy the configured minimum cluster size.

Save your actual test payload as `observations.json` in the repository root, then run:

```powershell
Get-Content .\observations.json -Raw |
    ConvertFrom-Json |
    ConvertTo-Json -Depth 20 |
    Set-Content .\observations-normalized.json
```

Send the payload to the API:

```powershell
curl.exe -i `
    -X POST `
    'http://127.0.0.1:3000/detect' `
    -H 'Content-Type: application/json' `
    --data-binary '@observations.json'
```

The response includes detection results and associated counts and metadata.

### HTTP status codes

| Status | Meaning |
|---|---|
| `200` | Request processed successfully |
| `400` | Missing, malformed, or invalid request data |
| `500` | Unexpected server-side error |

Exact validation behavior depends on the submitted data and the handler's implementation.

## Validation

Run the following commands from the repository root.

### Validate the SAM template

```powershell
sam validate --lint
```

### Check Python syntax

```powershell
python -m py_compile `
    backend\lambda_handler.py `
    backend\monte_carlo.py `
    backend\heat_pocket_detector.py
```

### Build the application

```powershell
sam build --use-container
```

### Test the simulation endpoint

With the local API running in another terminal:

```powershell
curl.exe -i `
    -X POST `
    'http://127.0.0.1:3000/simulate' `
    -H 'Content-Type: application/json' `
    -d '{}'
```

Check that the response reports simulation mode and includes generated observations.

These checks establish basic template, syntax, build, and endpoint behavior. They do not establish comprehensive test coverage, real-world detection accuracy, or scientific validity.

## Limitations

HEPo is an experimental prototype. Its limitations include:

- **Synthetic data:** Current observations are generated by software rather than collected from physical sensors.
- **Unverified environmental conditions:** Demonstration coordinates and temperatures are not a live environmental feed.
- **Heuristic detection:** Clustering parameters and confidence classifications require validation against ground-truth measurements.
- **Sensor calibration:** Future integration of phone-derived or physical sensor data would require quality control and calibration.
- **No assumed cloud deployment:** The documented workflow is local. No deployed AWS service should be assumed.
- **Network dependencies:** Local API requests and uncached map tiles may require connectivity.
- **No certified heat-safety function:** HEPo is not a substitute for official heat alerts, environmental monitoring, or medical advice.

## Roadmap

Potential future work includes:

- Integrating validated environmental datasets or calibrated sensors
- Evaluating detection performance against reference measurements
- Improving baseline estimation and spatial clustering
- Comparing historical heat patterns
- Improving accessibility and offline support
- Evaluating secure cloud deployment and persistent storage
- Gathering feedback from outdoor workers and urban planners

These are possible extensions, not claims about features already implemented.

## Contributing

Bug reports, reproducible issues, documentation improvements, and carefully tested contributions are welcome.

When proposing changes:

1. Describe the problem and expected behavior.
2. Include steps to reproduce bugs where possible.
3. Validate changes before submitting them.
4. Preserve explicit simulation labeling unless real data sources have been implemented and verified.
5. Avoid committing secrets, generated build artifacts, or local environment files.

## License

HEPo is distributed under the MIT License. See [`LICENSE`](LICENSE) for the complete terms.

The license for HEPo does not replace the licenses, attribution obligations, or terms of service applicable to its dependencies and external data sources.

---

**HEPo — making localized urban heat patterns easier to explore, one simulated observation at a time.**

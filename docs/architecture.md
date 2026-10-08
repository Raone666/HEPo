# HEPo Architecture & System Design

**Project Name:** HEPo (Heat Encroachment Pockets, pronounced *"hippo"*)  
**Event:** Environmental Hacks — Bharat Builds Tour (WeMakeDevs × AWS Builder Center, October 8–11, 2026)  
**Track:** Heat and Water  
**Chosen Problem:** Localized Urban Heat Pockets  

---

## 1. Problem Statement & Core Value
> *"A city does not experience heat uniformly. Localized areas can become significantly hotter than their surroundings, while broad weather measurements may not reveal these small-scale differences."*

HEPo turns distributed temperature observations into a live map of localized urban heat pockets. It empowers outdoor workers, pedestrians, delivery workers, and municipal teams to detect microclimate thermal risks that broad regional forecasts miss.

---

## 2. End-to-End System Architecture

```
PWA Client (Frontend)
   │
   ├── [Offline App Shell + Service Worker]
   └── [Leaflet Geospatial Map + Thermal Layer]
         ▲
         │ (POST /observations, GET /observations, GET /heat-pockets)
         ▼
Amazon API Gateway (REST API)
         │
         ▼
AWS Lambda (Python Ingestion & Analytics Engine)
         │
         ├── CloudWatch (Operational Logging)
         ▼
Amazon DynamoDB (`HEPoObservations` Table)
```

---

## 3. Observation Schema (DynamoDB & PWA)

```json
{
  "observationId": "obs-00016",
  "nodeId": "sim-016",
  "timestamp": "2026-10-08T14:32:00Z",
  "latitude": 28.7551,
  "longitude": 77.1240,
  "temperatureC": 41.2,
  "humidityPercent": 33,
  "mode": "simulation",
  "siteDescription": "Shahbad Daulatpur Unshaded Transit Hub",
  "zoneTag": "pocket-1"
}
```

---

## 4. Heat Pocket Detection Algorithm

* **Time Window:** Recent observations (last 15 minutes).
* **Spatial Grouping:** Points within $\approx 200\text{ meters}$ calculated via the Haversine Great Circle distance formula.
* **Local Baseline Temperature:** Mean temperature of surrounding ambient urban baseline points.
* **Cluster Temperature:** Mean temperature of observations within the $\approx 200\text{ m}$ spatial cluster.
* **Thermal Difference:**
  $$\Delta T = T_{\text{cluster}} - T_{\text{baseline}}$$
* **Detection Criteria (Prototype Threshold):**
  $$\text{IF } \text{count} \ge 3 \text{ AND } \Delta T \ge 3.0^\circ\text{C} \implies \textbf{HEAT POCKET DETECTED}$$
* **Detection Confidence:**
  - `HIGH`: $\ge 5$ observations and standard deviation $\sigma \le 0.8^\circ\text{C}$.
  - `MEDIUM`: $\ge 4$ observations or standard deviation $\sigma \le 1.0^\circ\text{C}$.
  - `LOW`: Minimum threshold satisfied with higher variance.

---

## 5. Scientific Honesty & Prototype Disclosures
- **Simulation Mode:** All demonstration observations are clearly tagged with `mode: "simulation"`.
- **Scope:** HEPo detects observational thermal anomalies across microclimates. It does not replace certified meteorological observatories, claim causal attribution, or diagnose medical heat distress.

---

## 6. Implementation Status
- [x] **Phase 1: PWA Only** (Responsive mobile-first shell, Leaflet map, deterministic simulation, detection logic, offline service worker, manifest).
- [ ] **Phase 2: AWS Backend** (DynamoDB table `HEPoObservations`, Lambda function, API Gateway endpoints).
- [ ] **Phase 3: Integration & Demo** (Connecting PWA to live API Gateway, end-to-end testing, 3-minute video recording).

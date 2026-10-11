# HEPo — Heat Encroachment Pockets

> **Pronounced:** *"hippo"*

**Environmental Hacks — Bharat Builds Tour**  
**WeMakeDevs × AWS Builder Center**  
**Track:** Heat and Water • Localized Urban Heat Pockets

HEPo is a Progressive Web App (PWA) designed to detect and visualize localized urban heat pockets from distributed, geotagged temperature observations.

---

## 🌡️ The Problem

A city does not experience heat uniformly.

Two locations only a few hundred meters apart can experience noticeably different thermal conditions because of differences in shade, surface materials, building density, traffic, vegetation, and other local factors.

Broad weather measurements can describe regional conditions while missing these smaller-scale variations.

**HEPo focuses on the local picture.**

---

## 💡 The Solution

HEPo turns distributed temperature observations into a map of localized thermal anomalies.

The system:

1. Collects temperature observations with geographic coordinates and timestamps.
2. Groups nearby observations.
3. Calculates a local temperature baseline.
4. Identifies clusters that are significantly warmer than their surroundings.
5. Visualizes detected heat pockets on an interactive map.
6. Provides contextual information such as temperature difference, observation count, and confidence.

### Core idea

> **HEPo turns distributed temperature observations into a live map of localized urban heat pockets.**

---

## 👥 Who Is It For?

HEPo is designed to provide situational awareness for:

- Outdoor workers
- Delivery workers
- Pedestrians
- Urban residents
- Event organizers
- Environmental teams
- Urban planners
- Researchers

A simple user question HEPo aims to answer is:

> **"Is the area around me experiencing unusually high heat compared with nearby areas?"**

---

## 🚀 Current Status

### Phase 1 — PWA Prototype

The current version is a functional local prototype using deterministic simulated observations.

It demonstrates the complete observation-to-visualization workflow without requiring an active AWS account.

**Current mode: `SIMULATION MODE`**

The simulated observations are clearly labelled and are **not presented as real sensor measurements**.

---

## 📱 Features

### Progressive Web App

- Responsive mobile-first interface
- Installable PWA
- Service worker
- Offline application shell
- Mobile and desktop support

### Interactive Map

- Leaflet-based geospatial map
- OpenStreetMap basemap
- Temperature observations
- Thermal classification
- Detected heat-pocket visualization
- Interactive observation and heat-pocket details

### Heat-Pocket Detection

The current prototype uses a deterministic rule-based approach:

- Recent observations are considered.
- Nearby observations are grouped within approximately 200 meters.
- A local baseline is calculated.
- A cluster is considered a potential heat pocket when:
  - at least 3 observations are available
  - temperature difference is at least `+3.0°C`

The prototype also provides a confidence level:

- `HIGH`
- `MEDIUM`
- `LOW`

Confidence represents the consistency, density, and recency of observations. It does **not** represent scientific certainty.

---

## 🧪 Simulation Mode

The prototype currently uses deterministic simulated observations so that the demonstration produces a reproducible result.

The simulation includes:

- Normal observations
- Elevated observations
- Anomalous observations
- A deliberately generated heat-pocket cluster

This allows the detection pipeline to be tested consistently before connecting physical or external sensor data.

---

## 🏗️ Architecture

### Current Phase

```text
Simulated Observations
        │
        ▼
   PWA / Browser
        │
        ▼
Heat-Pocket Detection
        │
        ▼
 Interactive Map

# HEPo — Heat Encroachment Pockets

> **Pronounced:** *"hippo"*  
> **Event:** Environmental Hacks (Bharat Builds Tour — WeMakeDevs × AWS Builder Center)  
> **Track:** Heat and Water &bull; Localized Urban Heat Pockets  

HEPo is a Progressive Web App (PWA) that detects and visualizes localized urban heat pockets from distributed geotagged temperature observations.

---

## 🌟 The Problem & Solution

* **The Problem:** A city does not experience heat uniformly. Localized areas (unshaded transit junctions, dense asphalt, industrial container yards) can become significantly hotter than their surroundings (+3°C to +6°C excess), while broad weather measurements fail to reveal these small-scale differences.
* **The Solution:** HEPo turns distributed temperature observations into a live map of localized urban heat pockets, providing situational awareness for outdoor workers, delivery couriers, pedestrians, and urban planners.

---

## 🚀 Quick Start: Running the PWA Locally

No heavy node dependencies required. Start with Python's built-in static HTTP server:

```powershell
# From the repository root
python -m http.server 8000 --directory frontend
```

Then open your browser to:
[http://localhost:8000](http://localhost:8000)

### Testing Offline & PWA Capabilities
1. Open DevTools in Chrome/Edge (`F12`).
2. Go to the **Application** tab &rarr; **Service Workers** to verify `service-worker.js` is active.
3. Toggle **Offline** mode in DevTools Network tab and reload the page; the app shell and cached observations will load smoothly with an offline badge.
4. Click **Install App** in the header to install as a standalone PWA on desktop or mobile.

---

## 🧪 Automated Testing

Run the test suite to verify asset integrity, manifest conformance, schema adherence, and detection algorithm math:

```powershell
python -m unittest tests/test_phase1.py
```

To regenerate the deterministic simulation dataset:
```powershell
python simulation/generate_observations.py
```

---

## 📱 Phase 1 Deliverables (PWA Only)

* **Responsive Mobile-First PWA Shell**: High-contrast, accessible dark UI optimized for mobile touch targets and desktop inspectors.
* **Interactive Leaflet Geospatial Map**: Renders observation pins with direct temperature badges and pulse-animated heat pocket circles.
* **Deterministic Simulation Dataset**: 25 calibrated observations around Delhi Technological University (DTU) and surrounding microclimates.
* **Heat Pocket Detection Algorithm**:
  * Spatial grouping within ~200 meters.
  * Baseline comparison against ambient urban background.
  * Prototype threshold: $\ge 3$ observations and $\Delta T \ge +3.0^\circ\text{C}$.
  * Confidence rating (`HIGH`, `MEDIUM`, `LOW`).
* **Inspection Panels**: Detailed breakdown for selected observations and detected heat pocket zones.
* **PWA Manifest & Service Worker**: Standalone installability with offline app shell caching.
* **Scientific Honesty Disclosures**: Explicit simulation mode badges and microclimate anomaly disclaimers.

---

## 🏛️ System Architecture

See [`docs/architecture.md`](docs/architecture.md) for full architecture specifications, DynamoDB schema, and AWS integration roadmap.

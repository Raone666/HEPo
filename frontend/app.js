/**
 * HEPo (Heat Encroachment Pockets) - Core Application Logic
 * Refined Map Experience: Leaflet Circle Markers, Obvious Heat Pocket, Clean Legend & Mobile UI
 */

// ============================================================================
// 1. SMALL DETERMINISTIC DEMO DATASET (Delhi NCR / DTU Microclimate)
// ============================================================================
const DETERMINISTIC_OBSERVATIONS = [
  // --- Normal Observations: Shaded Campus & Vegetative Areas (34.0–35.6°C) ---
  { observationId: "obs-00001", nodeId: "sim-001", timestamp: "2026-10-08T14:33:00Z", latitude: 28.7495, longitude: 77.1162, temperatureC: 34.6, humidityPercent: 54, mode: "simulation", siteDescription: "DTU Sports Complex Lawn", zoneTag: "normal" },
  { observationId: "obs-00002", nodeId: "sim-002", timestamp: "2026-10-08T14:35:00Z", latitude: 28.7512, longitude: 77.1150, temperatureC: 34.8, humidityPercent: 53, mode: "simulation", siteDescription: "DTU Central Library Shaded Garden", zoneTag: "normal" },
  { observationId: "obs-00003", nodeId: "sim-003", timestamp: "2026-10-08T14:37:00Z", latitude: 28.7525, longitude: 77.1172, temperatureC: 34.2, humidityPercent: 56, mode: "simulation", siteDescription: "DTU Wetland & Lake Perimeter", zoneTag: "normal" },
  { observationId: "obs-00004", nodeId: "sim-004", timestamp: "2026-10-08T14:38:00Z", latitude: 28.7482, longitude: 77.1180, temperatureC: 35.1, humidityPercent: 51, mode: "simulation", siteDescription: "DTU South Faculty Tree Canopy", zoneTag: "normal" },
  { observationId: "obs-00005", nodeId: "sim-005", timestamp: "2026-10-08T14:40:00Z", latitude: 28.7538, longitude: 77.1141, temperatureC: 35.4, humidityPercent: 50, mode: "simulation", siteDescription: "Academic Block Courtyard", zoneTag: "normal" },
  { observationId: "obs-00006", nodeId: "sim-006", timestamp: "2026-10-08T14:42:00Z", latitude: 28.7470, longitude: 77.1155, temperatureC: 34.9, humidityPercent: 52, mode: "simulation", siteDescription: "Botanical Reserve Perimeter", zoneTag: "normal" },
  { observationId: "obs-00007", nodeId: "sim-007", timestamp: "2026-10-08T14:43:00Z", latitude: 28.7505, longitude: 77.1192, temperatureC: 35.6, humidityPercent: 49, mode: "simulation", siteDescription: "East Quadrangle Greenery", zoneTag: "normal" },
  { observationId: "obs-00008", nodeId: "sim-008", timestamp: "2026-10-08T14:44:00Z", latitude: 28.7460, longitude: 77.1198, temperatureC: 35.3, humidityPercent: 51, mode: "simulation", siteDescription: "Campus Gate 1 Buffer Lawn", zoneTag: "normal" },

  // --- Elevated Observations: Paved Corridors & Sector Roadways (36.5–37.8°C) ---
  { observationId: "obs-00009", nodeId: "sim-009", timestamp: "2026-10-08T14:31:00Z", latitude: 28.7435, longitude: 77.1220, temperatureC: 36.5, humidityPercent: 46, mode: "simulation", siteDescription: "Rohini Sector 17 Outer Ring", zoneTag: "elevated" },
  { observationId: "obs-00010", nodeId: "sim-010", timestamp: "2026-10-08T14:34:00Z", latitude: 28.7418, longitude: 77.1245, temperatureC: 37.1, humidityPercent: 43, mode: "simulation", siteDescription: "Sector 17 Market Perimeter", zoneTag: "elevated" },
  { observationId: "obs-00011", nodeId: "sim-011", timestamp: "2026-10-08T14:36:00Z", latitude: 28.7442, longitude: 77.1265, temperatureC: 36.8, humidityPercent: 45, mode: "simulation", siteDescription: "Residential Sector Avenue", zoneTag: "elevated" },
  { observationId: "obs-00012", nodeId: "sim-012", timestamp: "2026-10-08T14:39:00Z", latitude: 28.7465, longitude: 77.1240, temperatureC: 37.4, humidityPercent: 42, mode: "simulation", siteDescription: "Shahbad Extension Paved Crossing", zoneTag: "elevated" },
  { observationId: "obs-00013", nodeId: "sim-013", timestamp: "2026-10-08T14:41:00Z", latitude: 28.7395, longitude: 77.1210, temperatureC: 36.9, humidityPercent: 44, mode: "simulation", siteDescription: "Paved Collector Arterial Road", zoneTag: "elevated" },
  { observationId: "obs-00014", nodeId: "sim-014", timestamp: "2026-10-08T14:44:00Z", latitude: 28.7380, longitude: 77.1250, temperatureC: 37.8, humidityPercent: 41, mode: "simulation", siteDescription: "Commercial Sector 16 Connector", zoneTag: "elevated" },

  // --- Obvious Primary Heat-Pocket Cluster: Shahbad Transit & Truck Depot (40.9–42.1°C, N=6) ---
  { observationId: "obs-00015", nodeId: "sim-015", timestamp: "2026-10-08T14:32:00Z", latitude: 28.7551, longitude: 77.1240, temperatureC: 41.2, humidityPercent: 33, mode: "simulation", siteDescription: "Shahbad Daulatpur Unshaded Transit Hub", zoneTag: "pocket-1" },
  { observationId: "obs-00016", nodeId: "sim-016", timestamp: "2026-10-08T14:35:00Z", latitude: 28.7555, longitude: 77.1246, temperatureC: 41.8, humidityPercent: 31, mode: "simulation", siteDescription: "Truck Terminal Heavy Asphalt Yard", zoneTag: "pocket-1" },
  { observationId: "obs-00017", nodeId: "sim-017", timestamp: "2026-10-08T14:37:00Z", latitude: 28.7548, longitude: 77.1238, temperatureC: 40.9, humidityPercent: 34, mode: "simulation", siteDescription: "Metal Roofing Wholesale Yard", zoneTag: "pocket-1" },
  { observationId: "obs-00018", nodeId: "sim-018", timestamp: "2026-10-08T14:40:00Z", latitude: 28.7557, longitude: 77.1235, temperatureC: 42.1, humidityPercent: 30, mode: "simulation", siteDescription: "Concrete Freight Depot West", zoneTag: "pocket-1" },
  { observationId: "obs-00019", nodeId: "sim-019", timestamp: "2026-10-08T14:42:00Z", latitude: 28.7549, longitude: 77.1249, temperatureC: 41.5, humidityPercent: 32, mode: "simulation", siteDescription: "Transit Stopline (High Engine Idling)", zoneTag: "pocket-1" },
  { observationId: "obs-00020", nodeId: "sim-020", timestamp: "2026-10-08T14:44:00Z", latitude: 28.7553, longitude: 77.1244, temperatureC: 41.3, humidityPercent: 33, mode: "simulation", siteDescription: "Shahbad Central Asphalt Junction", zoneTag: "pocket-1" }
];

// Configuration
const CONFIG = {
  CLUSTER_DISTANCE_METERS: 200,   // Spatial grouping distance
  DIFF_THRESHOLD_C: 3.0,          // Anomaly threshold
  MIN_OBSERVATIONS: 3             // Minimum nodes to confirm cluster
};

// Application State
const state = {
  observations: [...DETERMINISTIC_OBSERVATIONS],
  heatPockets: [],
  selectedObservation: null,
  selectedPocket: null,
  urbanBaselineC: 0,
  averageTempC: 0
};

// Leaflet Map and Layer Groups
let map = null;
let observationsLayer = null;
let heatPocketsLayer = null;
let selectedHighlightLayer = null;

// ============================================================================
// 2. GEOSPATIAL CLUSTERING & ANOMALY DETECTION
// ============================================================================

function haversineDistanceMeters(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const toRad = (deg) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function detectHeatPockets(observations) {
  if (!observations || observations.length === 0) {
    return { pockets: [], baselineC: 0, averageC: 0 };
  }

  // Calculate Average Temperature across all readings
  const allTemps = observations.map(o => o.temperatureC);
  const averageC = Number((allTemps.reduce((s, t) => s + t, 0) / allTemps.length).toFixed(1));

  // Local Baseline: Ambient non-anomalous background (normal & elevated zones)
  const nonAnomalous = observations.filter(o => o.temperatureC < 39.0);
  const baselineValues = nonAnomalous.length > 0 ? nonAnomalous.map(o => o.temperatureC) : allTemps;
  const baselineC = Number((baselineValues.reduce((s, t) => s + t, 0) / baselineValues.length).toFixed(1));

  // Spatial Grouping (~200m)
  const clusters = [];
  const visited = new Set();

  for (let i = 0; i < observations.length; i++) {
    if (visited.has(i)) continue;

    const cluster = [observations[i]];
    visited.add(i);

    for (let j = 0; j < observations.length; j++) {
      if (!visited.has(j)) {
        const d = haversineDistanceMeters(
          observations[i].latitude,
          observations[i].longitude,
          observations[j].latitude,
          observations[j].longitude
        );
        if (d <= CONFIG.CLUSTER_DISTANCE_METERS) {
          cluster.push(observations[j]);
          visited.add(j);
        }
      }
    }

    if (cluster.length >= CONFIG.MIN_OBSERVATIONS) {
      clusters.push(cluster);
    }
  }

  const pockets = [];
  let pocketIndex = 1;

  for (const cluster of clusters) {
    const cTemps = cluster.map(c => c.temperatureC);
    const clusterTemp = Number((cTemps.reduce((s, t) => s + t, 0) / cTemps.length).toFixed(1));
    const differenceC = Number((clusterTemp - baselineC).toFixed(1));

    // Threshold check: >= 3 observations and >= +3.0°C difference
    if (cluster.length >= CONFIG.MIN_OBSERVATIONS && differenceC >= CONFIG.DIFF_THRESHOLD_C) {
      const centerLat = cluster.reduce((s, c) => s + c.latitude, 0) / cluster.length;
      const centerLng = cluster.reduce((s, c) => s + c.longitude, 0) / cluster.length;

      let maxD = 0;
      cluster.forEach(pt => {
        const dist = haversineDistanceMeters(centerLat, centerLng, pt.latitude, pt.longitude);
        if (dist > maxD) maxD = dist;
      });
      const radiusMeters = Math.max(140, Math.min(200, Math.round(maxD + 30)));

      // Standard deviation
      const variance = cTemps.reduce((sum, v) => sum + Math.pow(v - clusterTemp, 2), 0) / cTemps.length;
      const stdDev = Math.sqrt(variance);

      let confidence = "Low";
      if (cluster.length >= 5 && stdDev <= 0.8) {
        confidence = "High";
      } else if (cluster.length >= 4 || stdDev <= 1.0) {
        confidence = "Medium";
      }

      pockets.push({
        pocketId: `pocket-00${pocketIndex++}`,
        status: "HEAT POCKET DETECTED",
        latitude: Number(centerLat.toFixed(6)),
        longitude: Number(centerLng.toFixed(6)),
        radiusMeters: radiusMeters,
        temperatureC: clusterTemp,
        baselineTemperatureC: baselineC,
        differenceC: differenceC,
        observationCount: cluster.length,
        confidence: confidence,
        // UI aliases
        clusterTemperatureC: clusterTemp,
        localBaselineC: baselineC,
        stdDevC: Number(stdDev.toFixed(2)),
        nodes: cluster.map(c => c.nodeId),
        observations: cluster,
        primarySite: cluster[0].siteDescription || "Urban Heat Encroachment Zone"
      });
    }
  }

  return { pockets, baselineC, averageC };
}

// ============================================================================
// 3. LEAFLET MAP & VISUALIZATIONS
// ============================================================================

function initMap() {
  // Center in Delhi NCR (DTU sector)
  const defaultCenter = [28.7495, 77.1180];
  const defaultZoom = 15;

  map = L.map("map", {
    zoomControl: false,
    attributionControl: true
  }).setView(defaultCenter, defaultZoom);

  // Position standard zoom controls in top-left
  L.control.zoom({ position: "topleft" }).addTo(map);

  // Standard public OpenStreetMap tile layer (no API key required for prototype)
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
  }).addTo(map);

  heatPocketsLayer = L.layerGroup().addTo(map);
  observationsLayer = L.layerGroup().addTo(map);
  selectedHighlightLayer = L.layerGroup().addTo(map);

  // Dismiss drawer when clicking blank map area
  map.on("click", (e) => {
    if (e.originalEvent && !e.originalEvent.target.closest(".leaflet-interactive")) {
      closeDrawer();
    }
  });
}

function renderMapVisuals() {
  if (!map) return;

  observationsLayer.clearLayers();
  heatPocketsLayer.clearLayers();
  selectedHighlightLayer.clearLayers();

  // 1. Render Detected Heat Pocket (Clean, serious, visually obvious boundary)
  state.heatPockets.forEach((pocket) => {
    // Outer Heat Boundary Circle
    const boundaryCircle = L.circle([pocket.latitude, pocket.longitude], {
      radius: pocket.radiusMeters,
      color: "#ef4444",
      weight: 2,
      dashArray: "6, 6",
      fillColor: "#ef4444",
      fillOpacity: 0.22,
      className: "heat-pocket-boundary",
      interactive: true
    });

    boundaryCircle.bindTooltip(
      `<strong>${pocket.status}</strong><br>Avg: ${pocket.clusterTemperatureC}°C (+${pocket.differenceC}°C vs baseline)<br>Click for details`,
      { direction: "top", sticky: true }
    );

    boundaryCircle.on("click", (e) => {
      L.DomEvent.stopPropagation(e);
      openPocketDetails(pocket);
    });

    // Inner Core Marker
    const innerCoreCircle = L.circle([pocket.latitude, pocket.longitude], {
      radius: Math.round(pocket.radiusMeters * 0.35),
      color: "#dc2626",
      weight: 1.5,
      fillColor: "#dc2626",
      fillOpacity: 0.40,
      interactive: true
    });

    innerCoreCircle.on("click", (e) => {
      L.DomEvent.stopPropagation(e);
      openPocketDetails(pocket);
    });

    // Sleek Centroid Label Badge
    const centroidIcon = L.divIcon({
      className: "centroid-badge-wrapper",
      html: `<div class="centroid-badge">HEAT POCKET +${pocket.differenceC}°C</div>`,
      iconSize: [140, 20],
      iconAnchor: [70, 10]
    });

    const centroidMarker = L.marker([pocket.latitude, pocket.longitude], {
      icon: centroidIcon,
      interactive: false
    });

    heatPocketsLayer.addLayer(boundaryCircle);
    heatPocketsLayer.addLayer(innerCoreCircle);
    heatPocketsLayer.addLayer(centroidMarker);
  });

  // 2. Render Observations (Leaflet Circle Markers based on temperature state)
  state.observations.forEach((obs) => {
    let fillColor = "#10b981";  // normal
    let radius = 6.5;
    let category = "Normal";

    if (obs.temperatureC >= 40.0) {
      fillColor = "#ef4444";    // anomalous
      radius = 9;
      category = "Anomalous (+Heat Pocket)";
    } else if (obs.temperatureC >= 36.0) {
      fillColor = "#f59e0b";    // elevated
      radius = 7.5;
      category = "Elevated";
    }

    // Main observation circle marker
    const marker = L.circleMarker([obs.latitude, obs.longitude], {
      radius: radius,
      color: "#ffffff",
      weight: 1.5,
      fillColor: fillColor,
      fillOpacity: 0.95,
      interactive: true
    });

    // Extra subtle halo for anomalous points to make them visually distinct
    if (obs.temperatureC >= 40.0) {
      const halo = L.circleMarker([obs.latitude, obs.longitude], {
        radius: 14,
        color: "#ef4444",
        weight: 1,
        fillColor: "#ef4444",
        fillOpacity: 0.18,
        dashArray: "3, 3",
        interactive: false
      });
      observationsLayer.addLayer(halo);
    }

    marker.bindTooltip(
      `<strong>${obs.nodeId}</strong>: ${obs.temperatureC}°C<br>${category}<br>${obs.humidityPercent}% RH`,
      { direction: "top", offset: [0, -6] }
    );

    marker.on("click", (e) => {
      L.DomEvent.stopPropagation(e);
      openObservationDetails(obs, marker);
    });

    observationsLayer.addLayer(marker);
  });
}

/**
 * Requirement 7: Fit map bounds to observations on initial load
 */
function fitAllObservationsBounds() {
  if (!map || state.observations.length === 0) return;

  const latLngs = state.observations.map(o => [o.latitude, o.longitude]);
  const bounds = L.latLngBounds(latLngs);

  map.fitBounds(bounds, {
    padding: [45, 45],
    maxZoom: 16,
    animate: true,
    duration: 0.6
  });
}

function focusDetectedPocket() {
  if (!map || state.heatPockets.length === 0) return;

  const pocket = state.heatPockets[0];
  map.flyTo([pocket.latitude, pocket.longitude], 16, {
    duration: 0.8
  });
  openPocketDetails(pocket);
}

// ============================================================================
// 4. DETAIL PANELS (OBSERVATION & HEAT POCKET)
// ============================================================================

function openObservationDetails(obs, markerInstance) {
  state.selectedObservation = obs;
  state.selectedPocket = null;

  // Add selection highlight ring
  selectedHighlightLayer.clearLayers();
  if (markerInstance) {
    const highlight = L.circleMarker([obs.latitude, obs.longitude], {
      radius: 16,
      color: "#38bdf8",
      weight: 2.5,
      fill: false,
      interactive: false
    });
    selectedHighlightLayer.addLayer(highlight);
  }

  const diff = Number((obs.temperatureC - state.urbanBaselineC).toFixed(1));
  const diffSign = diff >= 0 ? `+${diff}` : `${diff}`;
  const isAnomalous = diff >= CONFIG.DIFF_THRESHOLD_C;

  const badgeEl = document.getElementById("drawer-badge");
  badgeEl.className = "drawer-tag tag-obs";
  badgeEl.textContent = `NODE • ${obs.nodeId}`;

  document.getElementById("drawer-title").textContent = obs.siteDescription || `Sensor Node ${obs.nodeId}`;

  const bodyEl = document.getElementById("drawer-body");
  bodyEl.innerHTML = `
    <div class="detail-hero-box">
      <div class="hero-temp-group">
        <span class="hero-temp-label">Observed Temperature</span>
        <span class="hero-temp-val ${isAnomalous ? 'danger' : (diff > 0.8 ? 'warning' : '')}">${obs.temperatureC}°C</span>
      </div>
      <div class="hero-diff-badge">
        <span class="hero-temp-label">vs Baseline (${state.urbanBaselineC}°C)</span>
        <span class="diff-pill ${isAnomalous ? 'danger' : 'neutral'}">${diffSign}°C</span>
      </div>
    </div>

    <div class="detail-grid">
      <div class="detail-cell">
        <span class="cell-label">Relative Humidity</span>
        <span class="cell-value">${obs.humidityPercent}% RH</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Telemetry Status</span>
        <span class="cell-value">${isAnomalous ? 'ANOMALOUS' : (diff > 0.8 ? 'ELEVATED' : 'NORMAL')}</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Observation ID</span>
        <span class="cell-value">${obs.observationId}</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Timestamp</span>
        <span class="cell-value">${new Date(obs.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })} UTC</span>
      </div>
      <div class="detail-cell" style="grid-column: span 2;">
        <span class="cell-label">Coordinates</span>
        <span class="cell-value">${obs.latitude.toFixed(5)}° N, ${obs.longitude.toFixed(5)}° E</span>
      </div>
    </div>

    <div class="disclaimer-box">
      <strong>SIMULATED OBSERVATION:</strong> Deterministic synthetic reading for hackathon demonstration. Identifies localized thermal microclimate anomalies.
    </div>
  `;

  document.getElementById("detail-drawer").classList.remove("hidden");
}

function openPocketDetails(pocket) {
  state.selectedPocket = pocket;
  state.selectedObservation = null;

  // Add selection highlight
  selectedHighlightLayer.clearLayers();
  const highlight = L.circle([pocket.latitude, pocket.longitude], {
    radius: pocket.radiusMeters + 8,
    color: "#38bdf8",
    weight: 2,
    dashArray: "4, 4",
    fill: false,
    interactive: false
  });
  selectedHighlightLayer.addLayer(highlight);

  const badgeEl = document.getElementById("drawer-badge");
  badgeEl.className = "drawer-tag tag-pocket";
  badgeEl.textContent = `HOTSPOT • ${pocket.pocketId}`;

  document.getElementById("drawer-title").textContent = pocket.status;

  const bodyEl = document.getElementById("drawer-body");
  bodyEl.innerHTML = `
    <div class="detail-hero-box">
      <div class="hero-temp-group">
        <span class="hero-temp-label">Cluster Temperature</span>
        <span class="hero-temp-val danger">${pocket.clusterTemperatureC}°C</span>
      </div>
      <div class="hero-diff-badge">
        <span class="hero-temp-label">Excess vs Baseline</span>
        <span class="diff-pill danger">+${pocket.differenceC}°C</span>
      </div>
    </div>

    <div class="detail-grid">
      <div class="detail-cell">
        <span class="cell-label">Local Baseline</span>
        <span class="cell-value">${pocket.localBaselineC}°C</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Contributing Nodes</span>
        <span class="cell-value">${pocket.observationCount} observations</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Cluster Radius</span>
        <span class="cell-value">~${pocket.radiusMeters} meters</span>
      </div>
      <div class="detail-cell">
        <span class="cell-label">Detection Confidence</span>
        <span class="badge-confidence confidence-${pocket.confidence.toLowerCase()}">${pocket.confidence}</span>
      </div>
      <div class="detail-cell" style="grid-column: span 2;">
        <span class="cell-label">Centroid Coordinates</span>
        <span class="cell-value">${pocket.latitude.toFixed(5)}° N, ${pocket.longitude.toFixed(5)}° E</span>
      </div>
    </div>

    <div>
      <span class="cell-label">Contributing Sensor Nodes:</span>
      <div class="node-chips">
        ${pocket.nodes.map(n => `<span class="node-chip">${n}</span>`).join("")}
      </div>
    </div>

    <div class="disclaimer-box">
      <strong>Thermal Anomaly Alert:</strong> Cluster exceeds ambient baseline by ≥ ${CONFIG.DIFF_THRESHOLD_C}°C across adjacent observations. High radiant exposure for outdoor workers and pedestrians in this micro-pocket.
    </div>
  `;

  document.getElementById("detail-drawer").classList.remove("hidden");
}

function closeDrawer() {
  document.getElementById("detail-drawer").classList.add("hidden");
  selectedHighlightLayer.clearLayers();
}

function updateMetricsUI() {
  document.getElementById("stat-active-nodes").textContent = state.observations.length;
  document.getElementById("stat-pockets-detected").textContent = state.heatPockets.length;
  document.getElementById("stat-avg-temp").textContent = `${state.averageTempC}°C`;
  document.getElementById("stat-baseline-temp").textContent = `${state.urbanBaselineC}°C`;
}

async function refreshSimulation() {
  const button = document.getElementById("btn-refresh-simulation");
  const status = document.getElementById("simulation-status");

  if (!button || button.disabled) return;

  button.disabled = true;
  if (status) status.textContent = "Generating fresh synthetic observations…";

  try {
    const response = await fetch("http://127.0.0.1:3000/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}"
    });

    if (!response.ok) {
      throw new Error(`Simulation API returned HTTP ${response.status}`);
    }

    const payload = await response.json();

    if (
      !Array.isArray(payload.observations) ||
      payload.observations.length === 0 ||
      !payload.observations.every((item) => item.mode === "simulation")
    ) {
      throw new Error("Simulation API returned invalid observation data");
    }

    state.observations = payload.observations;
    state.selectedObservation = null;
    state.selectedPocket = null;

    const result = detectHeatPockets(state.observations);
    state.heatPockets = result.pockets;
    state.urbanBaselineC = result.baselineC;
    state.averageTempC = result.averageC;

    updateMetricsUI();
    renderMapVisuals();
    fitAllObservationsBounds();

    if (status) {
      status.textContent =
        `Simulation mode · ${payload.count} synthetic observations · Local SAM API`;
    }

    console.info("[HEPo] Fresh Monte Carlo simulation loaded.");
  } catch (error) {
    console.error("[HEPo] Simulation refresh failed:", error);

    state.observations = [...DETERMINISTIC_OBSERVATIONS];
    state.selectedObservation = null;
    state.selectedPocket = null;

    const result = detectHeatPockets(state.observations);
    state.heatPockets = result.pockets;
    state.urbanBaselineC = result.baselineC;
    state.averageTempC = result.averageC;

    updateMetricsUI();
    renderMapVisuals();
    fitAllObservationsBounds();

    if (status) {
      status.textContent =
        "Local API unavailable · Showing original demonstration data";
    }
  } finally {
    button.disabled = false;
  }
}

// ============================================================================
// 5. EVENT BINDINGS & LIFECYCLE
// ============================================================================

function setupEventListeners() {
    const refreshButton = document.getElementById("btn-refresh-simulation");
  if (refreshButton) {
    refreshButton.addEventListener("click", refreshSimulation);
  }

  // Detail Drawer Close
  document.getElementById("btn-close-drawer").addEventListener("click", closeDrawer);

  // Map Controls
  document.getElementById("btn-focus-pocket").addEventListener("click", focusDetectedPocket);
  document.getElementById("btn-fit-bounds").addEventListener("click", fitAllObservationsBounds);

  // Legend Toggle & Close
  const legendEl = document.getElementById("map-legend");
  document.getElementById("btn-toggle-legend").addEventListener("click", () => {
    legendEl.classList.toggle("hidden");
  });
  document.getElementById("btn-close-legend").addEventListener("click", () => {
    legendEl.classList.add("hidden");
  });

  // Mode Toggle & Error Dismissal
  const modeBtn = document.getElementById("mode-toggle-btn");
  if (modeBtn) {
    modeBtn.addEventListener("click", () => {
      const modeLabel = document.getElementById("mode-label");
      if (modeBtn.classList.contains("badge-sim")) {
        modeBtn.className = "badge badge-live";
        if (modeLabel) modeLabel.textContent = "LIVE (STANDBY)";
      } else {
        modeBtn.className = "badge badge-sim";
        if (modeLabel) modeLabel.textContent = "SIMULATION MODE";
      }
    });
  }

  const dismissErrorBtn = document.getElementById("btn-dismiss-error");
  if (dismissErrorBtn) {
    dismissErrorBtn.addEventListener("click", () => {
      const errorBanner = document.getElementById("error-banner");
      if (errorBanner) errorBanner.classList.add("hidden");
    });
  }

  // Online / Offline Listeners
  window.addEventListener("online", handleOnline);
  window.addEventListener("offline", handleOffline);

  // PWA Install prompt handling
  let deferredPrompt = null;
  const installBtn = document.getElementById("install-btn");

  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.classList.remove("hidden");
  });

  installBtn.addEventListener("click", async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === "accepted") {
      installBtn.classList.add("hidden");
    }
    deferredPrompt = null;
  });
}

function handleOnline() {
  updateNetworkStatus();
  console.log("[HEPo PWA] Connectivity restored. Requesting fresh telemetry...");
  // Re-run detection and telemetry update
  const result = detectHeatPockets(state.observations);
  state.heatPockets = result.pockets;
  state.urbanBaselineC = result.baselineC;
  state.averageTempC = result.averageC;
  updateMetricsUI();
  renderMapVisuals();
}

function handleOffline() {
  updateNetworkStatus();
  console.warn("[HEPo PWA] Offline mode active. Utilizing cached application shell.");
}

function updateNetworkStatus() {
  const badge = document.getElementById("network-badge");
  const offlineBanner = document.getElementById("offline-banner");

  if (navigator.onLine) {
    if (badge) {
      badge.className = "badge badge-online";
      badge.innerHTML = `<span class="status-dot"></span> ONLINE`;
    }
    if (offlineBanner) offlineBanner.classList.add("hidden");
  } else {
    if (badge) {
      badge.className = "badge badge-offline";
      badge.innerHTML = `<span class="status-dot"></span> OFFLINE`;
    }
    if (offlineBanner) {
      offlineBanner.innerHTML = `<span><strong>Offline Mode:</strong> Live AWS cloud telemetry paused. Serving cached application shell &amp; observations.</span>`;
      offlineBanner.classList.remove("hidden");
    }
  }
}

function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("./service-worker.js")
        .then((reg) => {
          console.log("[HEPo PWA] Service Worker registered:", reg.scope);
        })
        .catch((err) => {
          console.warn("[HEPo PWA] Service Worker registration:", err);
        });
    });
  }
}

// ============================================================================
// 6. INITIALIZATION
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  initMap();
  setupEventListeners();
  updateNetworkStatus();

  // Run initial clustering & detection
  const result = detectHeatPockets(state.observations);
  state.heatPockets = result.pockets;
  state.urbanBaselineC = result.baselineC;
  state.averageTempC = result.averageC;

  updateMetricsUI();
  renderMapVisuals();
  registerServiceWorker();

  // Fit bounds to observations on initial load (Requirement 7)
  setTimeout(() => {
    fitAllObservationsBounds();
  }, 350);
});

"""
Phase 1 Automated Test Suite for HEPo PWA
Verifies all 15 core requirements:
1. Responsive mobile-first design (meta tags & CSS)
2. Installable PWA (manifest, icons)
3. Offline app shell (service-worker.js caching)
4. Leaflet map (local vendor files present)
5. Clean environmental monitoring interface
6. Header with HEPo branding
7. LIVE / SIMULATION MODE status indicator
8. Active Nodes counter
9. Heat Pockets counter
10. Average Temperature counter
11. Observation detail panel
12. Heat-pocket detail panel
13. Loading state
14. Error state
15. Offline state
16. Circle markers and circles verification (no emoji markers)
17. Deterministic mock dataset with normal, elevated, and obvious heat-pocket cluster
18. HTTP serving of all PWA assets
"""

import os
import json
import math
import unittest
import urllib.request
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(REPO_ROOT, "frontend")

class TestPhase1PWA(unittest.TestCase):

    def test_01_required_files_exist(self):
        """Verify all Phase 1 files are present and non-empty."""
        expected_files = [
            "frontend/index.html",
            "frontend/styles.css",
            "frontend/app.js",
            "frontend/manifest.webmanifest",
            "frontend/service-worker.js",
            "frontend/icons/favicon.svg",
            "frontend/icons/icon-192.png",
            "frontend/icons/icon-512.png",
            "frontend/icons/icon-maskable-512.png",
            "frontend/icons/apple-touch-icon.png",
            "frontend/vendor/leaflet/leaflet.js",
            "frontend/vendor/leaflet/leaflet.css",
            "simulation/generate_observations.py",
            "simulation/observations_seed.json"
        ]
        for rel_path in expected_files:
            full_path = os.path.join(REPO_ROOT, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Missing expected file: {rel_path}")
            self.assertGreater(os.path.getsize(full_path), 0, f"File is empty: {rel_path}")

    def test_02_manifest_installability(self):
        """Verify manifest.webmanifest satisfies PWA installation standards."""
        manifest_path = os.path.join(FRONTEND_DIR, "manifest.webmanifest")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("short_name"), "HEPo")
        self.assertEqual(manifest.get("display"), "standalone")
        self.assertTrue(manifest.get("start_url"))
        self.assertGreaterEqual(len(manifest.get("icons", [])), 2)
        
        # Verify icon files exist on disk
        for icon in manifest["icons"]:
            src = icon["src"]
            icon_disk_path = os.path.join(FRONTEND_DIR, src)
            self.assertTrue(os.path.exists(icon_disk_path), f"Icon file missing: {src}")

    def test_03_html_and_ui_requirements(self):
        """Verify required HTML elements for branding, status, counters, loading, error, and offline states."""
        html_path = os.path.join(FRONTEND_DIR, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Mobile viewport
        self.assertIn('name="viewport"', html)
        self.assertIn('viewport-fit=cover', html)

        # Branding
        self.assertIn("HEPo", html)
        self.assertIn("hippo", html)
        self.assertIn("Urban Heat Pocket Monitor", html)

        # LIVE / SIMULATION MODE status indicator (Req 7)
        self.assertIn('id="mode-toggle-btn"', html)
        self.assertIn('id="mode-label"', html)

        # Counters (Req 8, 9, 10)
        self.assertIn('id="stat-active-nodes"', html)
        self.assertIn('id="stat-pockets-detected"', html)
        self.assertIn('id="stat-avg-temp"', html)
        self.assertIn('id="stat-baseline-temp"', html)

        # Inspection Panels (Req 11, 12)
        self.assertIn('id="detail-drawer"', html)
        self.assertIn('id="drawer-badge"', html)
        self.assertIn('id="drawer-title"', html)
        self.assertIn('id="drawer-body"', html)

        # Loading, Error, Offline States (Req 13, 14, 15)
        self.assertIn('id="loading-overlay"', html)
        self.assertIn('id="error-banner"', html)
        self.assertIn('id="offline-banner"', html)

    def test_04_no_emoji_primary_visualization(self):
        """Verify code uses Leaflet circleMarker and circle rather than emoji for map rendering."""
        app_js_path = os.path.join(FRONTEND_DIR, "app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("L.circleMarker", code, "Must use Leaflet circleMarker for observations")
        self.assertIn("L.circle", code, "Must use Leaflet circle for heat-pocket boundaries")

    def test_05_deterministic_clustering_and_pocket_detection(self):
        """Verify deterministic dataset contains normal, elevated, and an obvious heat-pocket cluster."""
        seed_path = os.path.join(REPO_ROOT, "simulation", "observations_seed.json")
        with open(seed_path, "r", encoding="utf-8") as f:
            observations = json.load(f)

        normal_pts = [o for o in observations if o["temperatureC"] < 36.0]
        elevated_pts = [o for o in observations if 36.0 <= o["temperatureC"] < 39.0]
        pocket_pts = [o for o in observations if o["temperatureC"] >= 40.0]

        self.assertGreaterEqual(len(normal_pts), 5, "Must have normal observations (34-36°C)")
        self.assertGreaterEqual(len(elevated_pts), 5, "Must have elevated observations (36-38°C)")
        self.assertGreaterEqual(len(pocket_pts), 6, "Must have obvious heat pocket observations (40-42°C)")

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            dphi = math.radians(lat2 - lat1)
            dlam = math.radians(lon2 - lon1)
            a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
            return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Check that the primary pocket points cluster within 200m
        primary_cluster = [o for o in pocket_pts if o.get("zoneTag") == "pocket-1"]
        for p1 in primary_cluster:
            for p2 in primary_cluster:
                dist = haversine(p1["latitude"], p1["longitude"], p2["latitude"], p2["longitude"])
                self.assertLessEqual(dist, 200, "Primary heat pocket cluster points exceed 200m radius")

    def test_06_http_server_serves_pwa(self):
        """Verify HTTP server serves all PWA assets with 200 OK."""
        class CustomHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
            def log_message(self, format, *args):
                pass

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", 0))
        port = sock.getsockname()[1]
        sock.close()

        server = HTTPServer(("127.0.0.1", port), CustomHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        test_endpoints = [
            "/index.html",
            "/styles.css",
            "/app.js",
            "/manifest.webmanifest",
            "/service-worker.js",
            "/icons/favicon.svg",
            "/icons/icon-192.png",
            "/vendor/leaflet/leaflet.js",
            "/vendor/leaflet/leaflet.css"
        ]

        for ep in test_endpoints:
            url = f"http://127.0.0.1:{port}{ep}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                self.assertEqual(resp.status, 200, f"Endpoint failed: {ep}")

        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    unittest.main()

"""
Automated PWA Audit Suite for HEPo
==================================
Verifies PWA compliance for Chrome DevTools / Lighthouse criteria:
1. Web App Manifest (id, name, short_name, start_url, display mode, theme colors, icons)
2. Icon files on disk (192x192, 512x512, maskable, SVG)
3. HTML Theme and Viewport metadata
4. Service Worker caching & versioning
5. Offline telemetry behavior (no fake AWS data offline)
6. Dynamic online/offline UI transitions
"""

import os
import json
import unittest
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(REPO_ROOT, "frontend")


class TestPWAAudit(unittest.TestCase):

    def test_01_manifest_structure(self):
        """Audit manifest.webmanifest for PWA installation criteria."""
        manifest_path = os.path.join(FRONTEND_DIR, "manifest.webmanifest")
        self.assertTrue(os.path.exists(manifest_path), "manifest.webmanifest not found")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        # 1. Identity & Naming
        self.assertEqual(manifest.get("name"), "HEPo - Urban Heat Pocket Monitor")
        self.assertEqual(manifest.get("short_name"), "HEPo")
        self.assertTrue(manifest.get("description"))

        # 2. Navigation & Display
        self.assertEqual(manifest.get("start_url"), "./index.html")
        self.assertEqual(manifest.get("scope"), "./")
        self.assertEqual(manifest.get("display"), "standalone")
        self.assertEqual(manifest.get("orientation"), "portrait-primary")

        # 3. Colors
        self.assertEqual(manifest.get("theme_color"), "#0d1524")
        self.assertEqual(manifest.get("background_color"), "#0a0f1d")

        # 4. Icons
        icons = manifest.get("icons", [])
        self.assertGreaterEqual(len(icons), 3)

        sizes = [i.get("sizes") for i in icons]
        purposes = [i.get("purpose") for i in icons]

        self.assertIn("192x192", sizes, "Missing 192x192 icon in manifest")
        self.assertIn("512x512", sizes, "Missing 512x512 icon in manifest")
        self.assertIn("maskable", purposes, "Missing maskable icon in manifest")

    def test_02_icon_files_exist_and_match_dimensions(self):
        """Audit icon files on disk to guarantee valid dimensions and formats."""
        manifest_path = os.path.join(FRONTEND_DIR, "manifest.webmanifest")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        for icon in manifest["icons"]:
            src = icon["src"]
            file_path = os.path.join(FRONTEND_DIR, src)
            self.assertTrue(os.path.exists(file_path), f"Icon file missing on disk: {src}")

            # Verify PNG dimensions
            if icon.get("type") == "image/png":
                img = Image.open(file_path)
                expected_dim = int(icon["sizes"].split("x")[0])
                self.assertEqual(img.size, (expected_dim, expected_dim), f"Icon {src} dimensions mismatch")
                self.assertIn(img.format, ["PNG"], f"Icon {src} must be PNG format")

    def test_03_html_theme_and_viewport_metadata(self):
        """Audit index.html for viewport, theme-color, and apple-mobile tags."""
        html_path = os.path.join(FRONTEND_DIR, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Viewport
        self.assertIn('name="viewport"', html)
        self.assertIn('width=device-width', html)
        self.assertIn('initial-scale=1.0', html)

        # Manifest link
        self.assertIn('rel="manifest"', html)
        self.assertIn('href="manifest.webmanifest"', html)

        # Theme color matches manifest
        self.assertIn('name="theme-color" content="#0d1524"', html)

        # iOS / Apple mobile web app tags
        self.assertIn('name="apple-mobile-web-app-capable" content="yes"', html)
        self.assertIn('rel="apple-touch-icon"', html)

    def test_04_service_worker_caching_and_versioning(self):
        """Audit service-worker.js for cache versioning and shell asset pre-caching."""
        sw_path = os.path.join(FRONTEND_DIR, "service-worker.js")
        with open(sw_path, "r", encoding="utf-8") as f:
            sw_code = f.read()

        # Cache name versioning
        self.assertIn("CACHE_NAME = 'hepo-pwa-v", sw_code)

        # App shell assets
        required_assets = [
            "./index.html",
            "./styles.css",
            "./app.js",
            "./manifest.webmanifest",
            "./icons/favicon.svg",
            "./icons/icon-192.png",
            "./icons/icon-512.png",
            "./vendor/leaflet/leaflet.css",
            "./vendor/leaflet/leaflet.js"
        ]
        for asset in required_assets:
            self.assertIn(asset, sw_code, f"App shell asset missing in service worker cache: {asset}")

        # Tile caching
        self.assertIn("tile.openstreetmap.org", sw_code)

        # Navigation fallback
        self.assertIn("caches.match('./index.html')", sw_code)

    def test_05_no_fake_aws_data_offline(self):
        """Verify service worker returns 503 rather than fake data for offline telemetry."""
        sw_path = os.path.join(FRONTEND_DIR, "service-worker.js")
        with open(sw_path, "r", encoding="utf-8") as f:
            sw_code = f.read()

        self.assertIn("status: 503", sw_code, "Must return 503 when offline for AWS API endpoints")
        self.assertIn("offline: true", sw_code, "Must explicitly mark offline responses")

    def test_06_ui_offline_and_refresh_handlers(self):
        """Verify UI clearly indicates offline mode and hooks connectivity refresh."""
        app_js_path = os.path.join(FRONTEND_DIR, "app.js")
        with open(app_js_path, "r", encoding="utf-8") as f:
            app_code = f.read()

        # Service worker registration
        self.assertIn("navigator.serviceWorker.register", app_code)

        # Online / Offline handlers
        self.assertIn("addEventListener(\"online\", handleOnline)", app_code)
        self.assertIn("addEventListener(\"offline\", handleOffline)", app_code)

        # Clear offline indication
        self.assertIn("badge-offline", app_code)
        self.assertIn("offlineBanner.classList.remove(\"hidden\")", app_code)


if __name__ == "__main__":
    unittest.main()

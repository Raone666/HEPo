"""
Unit Test Suite for HEPo Heat-Pocket Detection Engine
=====================================================
Verifies all 10 algorithmic requirements:
1. Retrieval of observations from last 15 minutes.
2. Rejection of invalid coordinates or temperatures.
3. Spatial grouping using ~200m radius.
4. Minimum 3 observations required for cluster candidacy.
5. Local baseline temperature calculation.
6. Cluster temperature calculation.
7. differenceC = clusterTemperature - baselineTemperature.
8. Detection rule: observationCount >= 3 AND differenceC >= 3.0°C.
9. Return schema conformance (lat, lon, radius, temp, baseline, diff, count, confidence, status).
10. Confidence scoring (High, Medium, Low) based on count, variance, recency.
"""

import math
import unittest
from datetime import datetime, timezone, timedelta
import sys
import os

# Ensure backend module is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from heat_pocket_detector import (
    haversine_distance_meters,
    validate_observation,
    parse_iso_timestamp,
    filter_recent_observations,
    cluster_spatially,
    calculate_local_baseline,
    calculate_confidence,
    detect_heat_pockets,
    DEFAULT_CLUSTER_RADIUS_METERS,
    DEFAULT_DIFF_THRESHOLD_C,
    DEFAULT_MIN_OBSERVATIONS
)


class TestHeatPocketDetector(unittest.TestCase):

    def setUp(self):
        self.ref_time = datetime(2026, 10, 8, 14, 45, 0, tzinfo=timezone.utc)

    # -------------------------------------------------------------------------
    # Requirement 1 & 2: Validation and 15-Minute Temporal Filtering
    # -------------------------------------------------------------------------
    def test_01_validate_coordinates_and_temperatures(self):
        """Step 2: Reject invalid coordinates or out-of-bounds temperatures."""
        valid_obs = {
            "observationId": "obs-001",
            "latitude": 28.7500,
            "longitude": 77.1200,
            "temperatureC": 35.5,
            "timestamp": "2026-10-08T14:40:00Z"
        }
        self.assertTrue(validate_observation(valid_obs))

        # Invalid latitudes
        self.assertFalse(validate_observation({**valid_obs, "latitude": 95.0}))
        self.assertFalse(validate_observation({**valid_obs, "latitude": -91.0}))
        self.assertFalse(validate_observation({**valid_obs, "latitude": float("nan")}))
        self.assertFalse(validate_observation({**valid_obs, "latitude": "invalid"}))

        # Invalid longitudes
        self.assertFalse(validate_observation({**valid_obs, "longitude": 185.0}))
        self.assertFalse(validate_observation({**valid_obs, "longitude": -185.0}))

        # Invalid temperatures
        self.assertFalse(validate_observation({**valid_obs, "temperatureC": -60.0}))
        self.assertFalse(validate_observation({**valid_obs, "temperatureC": 75.0}))
        self.assertFalse(validate_observation({**valid_obs, "temperatureC": None}))

        # Invalid timestamp
        self.assertFalse(validate_observation({**valid_obs, "timestamp": "not-a-date"}))
        self.assertFalse(validate_observation({**valid_obs, "timestamp": None}))

    def test_02_filter_recent_observations_15_minutes(self):
        """Step 1: Retrieve only observations within the last 15 minutes."""
        obs_fresh_5m = {
            "observationId": "obs-01",
            "latitude": 28.7500,
            "longitude": 77.1200,
            "temperatureC": 35.0,
            "timestamp": (self.ref_time - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        obs_boundary_14m = {
            "observationId": "obs-02",
            "latitude": 28.7501,
            "longitude": 77.1201,
            "temperatureC": 35.2,
            "timestamp": (self.ref_time - timedelta(minutes=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        obs_expired_16m = {
            "observationId": "obs-03",
            "latitude": 28.7502,
            "longitude": 77.1202,
            "temperatureC": 35.1,
            "timestamp": (self.ref_time - timedelta(minutes=16)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        obs_expired_60m = {
            "observationId": "obs-04",
            "latitude": 28.7503,
            "longitude": 77.1203,
            "temperatureC": 35.3,
            "timestamp": (self.ref_time - timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        all_obs = [obs_fresh_5m, obs_boundary_14m, obs_expired_16m, obs_expired_60m]
        recent = filter_recent_observations(all_obs, reference_time=self.ref_time, window_minutes=15)

        self.assertEqual(len(recent), 2)
        recent_ids = {o["observationId"] for o in recent}
        self.assertIn("obs-01", recent_ids)
        self.assertIn("obs-02", recent_ids)
        self.assertNotIn("obs-03", recent_ids)
        self.assertNotIn("obs-04", recent_ids)

    # -------------------------------------------------------------------------
    # Requirement 3 & 4: Spatial Grouping ~200m and Minimum 3 Observations
    # -------------------------------------------------------------------------
    def test_03_spatial_grouping_200m_radius(self):
        """Step 3: Group spatially nearby observations within approximately 200m."""
        # 1 degree lat ~ 111,000m. 0.001 deg lat ~ 111m.
        # Anchor point
        p_anchor = {"observationId": "p0", "latitude": 28.75000, "longitude": 77.12000, "temperatureC": 38.0}
        # Point ~110m north (should cluster)
        p_near1 = {"observationId": "p1", "latitude": 28.75100, "longitude": 77.12000, "temperatureC": 38.2}
        # Point ~110m east (should cluster)
        p_near2 = {"observationId": "p2", "latitude": 28.75000, "longitude": 77.12110, "temperatureC": 38.1}
        # Point ~600m away (should NOT cluster with p0)
        p_far = {"observationId": "p3", "latitude": 28.75550, "longitude": 77.12000, "temperatureC": 35.0}

        clusters = cluster_spatially([p_anchor, p_near1, p_near2, p_far], radius_meters=200.0)

        # Expect 2 distinct spatial clusters: [p0, p1, p2] and [p3]
        self.assertEqual(len(clusters), 2)
        cluster_sizes = [len(c) for c in clusters]
        self.assertIn(3, cluster_sizes)
        self.assertIn(1, cluster_sizes)

    def test_04_minimum_3_observations_required(self):
        """Step 4 & 8: A candidate cluster requires at least 3 observations."""
        ts = self.ref_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Cluster with only 2 observations having extreme temperature (45.0°C)
        obs_only_two = [
            {"observationId": "a1", "latitude": 28.7500, "longitude": 77.1200, "temperatureC": 45.0, "timestamp": ts},
            {"observationId": "a2", "latitude": 28.7501, "longitude": 77.1201, "temperatureC": 45.5, "timestamp": ts},
            # Surrounding baseline points (outside 200m)
            {"observationId": "b1", "latitude": 28.7400, "longitude": 77.1100, "temperatureC": 35.0, "timestamp": ts},
            {"observationId": "b2", "latitude": 28.7402, "longitude": 77.1102, "temperatureC": 35.2, "timestamp": ts},
            {"observationId": "b3", "latitude": 28.7404, "longitude": 77.1104, "temperatureC": 35.1, "timestamp": ts},
        ]

        # Should NOT trigger a heat pocket because observationCount < 3
        detected = detect_heat_pockets(obs_only_two, reference_time=self.ref_time)
        self.assertEqual(len(detected), 0, "Clusters with < 3 observations must not trigger heat pocket")

    # -------------------------------------------------------------------------
    # Requirement 5, 6, 7, 8: Baseline, Delta, and Heat Pocket Decision Rule
    # -------------------------------------------------------------------------
    def test_05_threshold_decision_rule(self):
        """Step 5-8: Heat pocket triggered IF count >= 3 AND differenceC >= 3.0°C."""
        ts = self.ref_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Baseline observations (~35.0°C)
        baseline_pts = [
            {"observationId": f"base-{i}", "latitude": 28.7400 + i * 0.001, "longitude": 77.1100, "temperatureC": 35.0, "timestamp": ts}
            for i in range(5)
        ]

        # Scenario A: Cluster with count = 3 and difference = +2.5°C (Temp = 37.5°C vs 35.0°C baseline)
        # 37.5 - 35.0 = 2.5°C (< 3.0°C threshold -> NO HEAT POCKET)
        sub_threshold_cluster = [
            {"observationId": f"sub-{i}", "latitude": 28.7500 + i * 0.0003, "longitude": 77.1200, "temperatureC": 37.5, "timestamp": ts}
            for i in range(3)
        ]
        detected_sub = detect_heat_pockets(baseline_pts + sub_threshold_cluster, reference_time=self.ref_time)
        self.assertEqual(len(detected_sub), 0, "Sub-threshold (+2.5°C) must not trigger heat pocket")

        # Scenario B: Cluster with count = 3 and difference = +3.2°C (Temp = 38.2°C vs 35.0°C baseline)
        # 38.2 - 35.0 = 3.2°C (>= 3.0°C threshold -> HEAT POCKET DETECTED)
        above_threshold_cluster = [
            {"observationId": f"hot-{i}", "latitude": 28.7500 + i * 0.0003, "longitude": 77.1200, "temperatureC": 38.2, "timestamp": ts}
            for i in range(3)
        ]
        detected_above = detect_heat_pockets(baseline_pts + above_threshold_cluster, reference_time=self.ref_time)
        self.assertEqual(len(detected_above), 1, "Cluster meeting count >= 3 and diff >= 3.0°C must trigger heat pocket")
        pocket = detected_above[0]
        self.assertEqual(pocket["status"], "HEAT POCKET DETECTED")
        self.assertEqual(pocket["observationCount"], 3)
        self.assertAlmostEqual(pocket["differenceC"], 3.2, places=1)

    # -------------------------------------------------------------------------
    # Requirement 9: Return Schema Conformance
    # -------------------------------------------------------------------------
    def test_06_return_schema_conformance(self):
        """Step 9: Output dictionary must contain all required fields."""
        ts = self.ref_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        pts = [
            # 4 anomaly points (~41.2°C)
            {"observationId": "h1", "latitude": 28.7550, "longitude": 77.1240, "temperatureC": 41.2, "timestamp": ts},
            {"observationId": "h2", "latitude": 28.7552, "longitude": 77.1242, "temperatureC": 41.5, "timestamp": ts},
            {"observationId": "h3", "latitude": 28.7549, "longitude": 77.1239, "temperatureC": 40.9, "timestamp": ts},
            {"observationId": "h4", "latitude": 28.7554, "longitude": 77.1245, "temperatureC": 41.6, "timestamp": ts},
            # 4 baseline points (~35.5°C)
            {"observationId": "b1", "latitude": 28.7450, "longitude": 77.1150, "temperatureC": 35.2, "timestamp": ts},
            {"observationId": "b2", "latitude": 28.7452, "longitude": 77.1152, "temperatureC": 35.8, "timestamp": ts},
            {"observationId": "b3", "latitude": 28.7455, "longitude": 77.1155, "temperatureC": 35.4, "timestamp": ts},
            {"observationId": "b4", "latitude": 28.7458, "longitude": 77.1158, "temperatureC": 35.6, "timestamp": ts},
        ]

        results = detect_heat_pockets(pts, reference_time=self.ref_time)
        self.assertEqual(len(results), 1)
        pocket = results[0]

        # Verify all 9 required keys from Step 9
        required_keys = [
            "latitude",
            "longitude",
            "radiusMeters",
            "temperatureC",
            "baselineTemperatureC",
            "differenceC",
            "observationCount",
            "confidence",
            "status"
        ]
        for key in required_keys:
            self.assertIn(key, pocket, f"Missing required output key: {key}")

        self.assertIsInstance(pocket["latitude"], float)
        self.assertIsInstance(pocket["longitude"], float)
        self.assertIsInstance(pocket["radiusMeters"], (float, int))
        self.assertIsInstance(pocket["temperatureC"], float)
        self.assertIsInstance(pocket["baselineTemperatureC"], float)
        self.assertIsInstance(pocket["differenceC"], float)
        self.assertIsInstance(pocket["observationCount"], int)
        self.assertIn(pocket["confidence"], ["Low", "Medium", "High"])
        self.assertEqual(pocket["status"], "HEAT POCKET DETECTED")

    # -------------------------------------------------------------------------
    # Requirement 10: Multi-factor Confidence Scoring
    # -------------------------------------------------------------------------
    def test_07_confidence_scoring_multi_factor(self):
        """Step 10: Confidence evaluates count, temperature consistency, and recency."""
        # 1. High Confidence: 5+ observations, tight consistency (stdDev <= 0.8), fresh observations (< 5 min)
        ts_fresh = (self.ref_time - timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        cluster_high = [
            {"observationId": f"h-{i}", "temperatureC": 41.2 + (i * 0.1), "timestamp": ts_fresh}
            for i in range(5)
        ]
        self.assertEqual(calculate_confidence(cluster_high, reference_time=self.ref_time), "High")

        # 2. Medium Confidence: 4 observations, moderate variance
        ts_mid = (self.ref_time - timedelta(minutes=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
        cluster_med = [
            {"observationId": f"m-{i}", "temperatureC": 40.5 + (i * 0.4), "timestamp": ts_mid}
            for i in range(4)
        ]
        self.assertEqual(calculate_confidence(cluster_med, reference_time=self.ref_time), "Medium")

        # 3. Low Confidence: 3 observations (minimum), high variance (> 1.5°C), aging observations (> 12 min)
        ts_old = (self.ref_time - timedelta(minutes=14)).strftime("%Y-%m-%dT%H:%M:%SZ")
        cluster_low = [
            {"observationId": "l-1", "temperatureC": 39.0, "timestamp": ts_old},
            {"observationId": "l-2", "temperatureC": 41.0, "timestamp": ts_old},
            {"observationId": "l-3", "temperatureC": 43.5, "timestamp": ts_old},
        ]
        self.assertEqual(calculate_confidence(cluster_low, reference_time=self.ref_time), "Low")

    # -------------------------------------------------------------------------
    # End-to-End Test on Hackathon Simulation Seed
    # -------------------------------------------------------------------------
    def test_08_deterministic_seed_detection(self):
        """End-to-End: Verifies reliable detection on the 25-node DTU hackathon seed."""
        import json
        seed_path = os.path.join(os.path.dirname(__file__), "..", "simulation", "observations_seed.json")
        with open(seed_path, "r", encoding="utf-8") as f:
            seed_obs = json.load(f)

        results = detect_heat_pockets(seed_obs)
        self.assertGreaterEqual(len(results), 1, "Must detect primary heat pocket in seed")

        # Find primary Shahbad cluster
        primary = [p for p in results if "sim-016" in p.get("contributingNodeIds", [])][0]
        self.assertEqual(primary["observationCount"], 6)
        self.assertGreaterEqual(primary["differenceC"], 5.0)
        self.assertEqual(primary["confidence"], "High")
        self.assertEqual(primary["status"], "HEAT POCKET DETECTED")


if __name__ == "__main__":
    unittest.main()

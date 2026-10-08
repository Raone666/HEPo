"""
HEPo Simulation Data Generator
Deterministically generates urban temperature observation points across realistic zones:
- Normal zone: 34–36°C (e.g. green university campus / tree canopy)
- Elevated zone: 36–38°C (e.g. medium-density residential / paved corridors)
- Heat pocket: 40–42°C (e.g. intense unshaded transit hubs / industrial asphalt traps)

Centered around North Delhi / Delhi Technological University (DTU) area.
Guarantees reproducible detection for the hackathon 3-minute demo.
"""

import json
from datetime import datetime, timezone, timedelta

def generate_deterministic_observations():
    base_time = datetime(2026, 10, 8, 14, 45, 0, tzinfo=timezone.utc)
    
    # 1. Normal Zone (DTU Campus green area & water feature vicinity)
    # Target range: 34.0°C - 35.8°C
    normal_points = [
        {"lat": 28.7495, "lng": 77.1162, "temp": 34.6, "hum": 54, "offset": -12, "desc": "DTU Sports Complex Lawn"},
        {"lat": 28.7512, "lng": 77.1150, "temp": 34.8, "hum": 53, "offset": -10, "desc": "DTU Central Library Shaded Garden"},
        {"lat": 28.7525, "lng": 77.1172, "temp": 34.2, "hum": 56, "offset": -8,  "desc": "DTU Lake & Wetland Belt"},
        {"lat": 28.7482, "lng": 77.1180, "temp": 35.1, "hum": 51, "offset": -7,  "desc": "DTU South Faculty Canopy"},
        {"lat": 28.7538, "lng": 77.1141, "temp": 35.4, "hum": 50, "offset": -5,  "desc": "Academic Block IV Courtyard"},
        {"lat": 28.7470, "lng": 77.1155, "temp": 34.9, "hum": 52, "offset": -3,  "desc": "DTU Botanical Reserve Boundary"},
        {"lat": 28.7505, "lng": 77.1192, "temp": 35.6, "hum": 49, "offset": -2,  "desc": "East Hostel Quadrangle"},
        {"lat": 28.7460, "lng": 77.1198, "temp": 35.3, "hum": 51, "offset": -1,  "desc": "DTU Gate 1 Buffer Greenery"},
    ]

    # 2. Elevated Zone (Moderate residential density & arterial avenues)
    # Target range: 36.2°C - 37.9°C
    elevated_points = [
        {"lat": 28.7435, "lng": 77.1220, "temp": 36.5, "hum": 46, "offset": -14, "desc": "Rohini Sector 17 Outer Ring"},
        {"lat": 28.7418, "lng": 77.1245, "temp": 37.1, "hum": 43, "offset": -11, "desc": "Sector 17 Market Perimeter"},
        {"lat": 28.7442, "lng": 77.1265, "temp": 36.8, "hum": 45, "offset": -9,  "desc": "Residential Pocket C Avenue"},
        {"lat": 28.7465, "lng": 77.1240, "temp": 37.4, "hum": 42, "offset": -6,  "desc": "Shahbad Extension Crossing"},
        {"lat": 28.7395, "lng": 77.1210, "temp": 36.9, "hum": 44, "offset": -4,  "desc": "Paved Collector Road"},
        {"lat": 28.7420, "lng": 77.1180, "temp": 37.6, "hum": 41, "offset": -2,  "desc": "Commercial Plazas Roadway"},
        {"lat": 28.7380, "lng": 77.1250, "temp": 37.2, "hum": 43, "offset": -1,  "desc": "Sector 16 North Connector"},
    ]

    # 3. Heat Pocket 1 (Primary Anomaly - Shahbad Daulatpur Junction & Truck Stand)
    # Cluster center: lat 28.7552, lng 77.1242 (within ~130 meters)
    # Target range: 40.5°C - 42.2°C
    heat_pocket_1 = [
        {"lat": 28.7551, "lng": 77.1240, "temp": 41.2, "hum": 33, "offset": -13, "desc": "Shahbad Daulatpur Unshaded Transit Hub"},
        {"lat": 28.7555, "lng": 77.1246, "temp": 41.8, "hum": 31, "offset": -10, "desc": "Truck Terminal Asphalt Parking"},
        {"lat": 28.7548, "lng": 77.1238, "temp": 40.9, "hum": 34, "offset": -8,  "desc": "Metal Roofing Wholesale Yard"},
        {"lat": 28.7557, "lng": 77.1235, "temp": 42.1, "hum": 30, "offset": -5,  "desc": "Concrete Freight Yard West"},
        {"lat": 28.7549, "lng": 77.1249, "temp": 41.5, "hum": 32, "offset": -3,  "desc": "Intersection Stopline (High Traffic Idling)"},
        {"lat": 28.7553, "lng": 77.1244, "temp": 41.3, "hum": 33, "offset": -1,  "desc": "Central Asphalt Junction"},
    ]

    # 4. Heat Pocket 2 (Secondary Anomaly - Bawana Road Exposed Metal Depot Strip)
    # Cluster center: lat 28.7438, lng 77.1118 (within ~140 meters)
    # Target range: 40.1°C - 41.4°C
    heat_pocket_2 = [
        {"lat": 28.7436, "lng": 77.1115, "temp": 40.4, "hum": 36, "offset": -12, "desc": "Bawana Industrial Strip Scrap Depot"},
        {"lat": 28.7441, "lng": 77.1121, "temp": 41.1, "hum": 34, "offset": -9,  "desc": "Unshaded Paved Container Lot"},
        {"lat": 28.7439, "lng": 77.1112, "temp": 40.8, "hum": 35, "offset": -6,  "desc": "Industrial Gate Heavy Vehicle Siding"},
        {"lat": 28.7444, "lng": 77.1125, "temp": 40.3, "hum": 37, "offset": -2,  "desc": "Exposed Tar Mixing Yard"},
    ]

    observations = []
    counter = 1

    all_groups = [
        (normal_points, "normal"),
        (elevated_points, "elevated"),
        (heat_pocket_1, "pocket-1"),
        (heat_pocket_2, "pocket-2")
    ]

    for group, tag in all_groups:
        for item in group:
            obs_time = base_time + timedelta(minutes=item["offset"])
            obs = {
                "observationId": f"obs-{counter:05d}",
                "nodeId": f"sim-{counter:03d}",
                "timestamp": obs_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "latitude": round(item["lat"], 6),
                "longitude": round(item["lng"], 6),
                "temperatureC": round(item["temp"], 1),
                "humidityPercent": int(item["hum"]),
                "mode": "simulation",
                "siteDescription": item["desc"],
                "zoneTag": tag
            }
            observations.append(obs)
            counter += 1

    return observations

if __name__ == "__main__":
    obs = generate_deterministic_observations()
    print(f"Generated {len(obs)} deterministic observations:")
    temps = [o["temperatureC"] for o in obs]
    print(f"Temperature Range: {min(temps)}°C to {max(temps)}°C (Avg: {sum(temps)/len(temps):.2f}°C)")
    
    with open("simulation/observations_seed.json", "w", encoding="utf-8") as f:
        json.dump(obs, f, indent=2)
    print("Saved to simulation/observations_seed.json")

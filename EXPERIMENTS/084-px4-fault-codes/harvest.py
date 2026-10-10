#!/usr/bin/env python3
"""
E084 — Harvest PX4 fault code topics from discuss.px4.io
Stdlib Python 3.8 only, no external dependencies.
"""

import json
import time
import urllib.request
import urllib.error
import sys
import os
from pathlib import Path

BASE_URL = "https://discuss.px4.io"
RAW_DIR = Path("raw")
RAW_DIR.mkdir(exist_ok=True)

# Classification patterns (same as CLASSIFICATION_RULES.md)
FAULT_PATTERNS = [
    # (pattern_list, label)
    (["EKF2", "EKF.*fail", "EKF.*mismatch", "EKF.*error", "estimator.*fail", "estimator.*error", "EKF.*reset", "EKF.*diverg"], "EKF_FAILURE"),
    (["GPS.*fail", "GPS.*lost", "GPS.*glitch", "GPS.*no.fix", "GPS.*HDOP", "GNSS.*fail", "GNSS.*lost", "GPS.*jam", "GPS.*spoof", "GPS.*drift", "GPS.*accuracy"], "GPS_ISSUE"),
    (["IMU.*fail", "MAG.*fail", "compass.*fail", "BARO.*fail", "barometer.*fail", "accelerometer.*fail", "gyro.*fail", "rangefinder.*fail", "lidar.*fail", "optical.flow.*fail", "flow.*fail", "airspeed.*fail", "sensor.*fail", "sensor.*error"], "SENSOR_FAILURE"),
    (["motor.*fail", "servo.*fail", "actuator.*fail", "actuator.*saturat", "output.*fail", "ESC.*fail", "thrust.*fail", "propeller.*fail"], "ACTUATOR_FAILURE"),
    (["preflight.*fail", "prearm.*fail", "prearm.*check", "arming.*fail", "arming.*check", "preflight.*check", "can.not.arm", "cannot.arm", "arming.*denied"], "PREARM_FAILURE"),
    (["failsafe", "land.mode.*trigger", "RTL.*trigger", "return.to.launch.*trigger", "terminat", "emergency.*land", "failsafe.*trigger"], "FAILSAFE_TRIGGER"),
    (["link.*lost", "telemetry.*lost", "RC.*lost", "radio.*lost", "heartbeat.*lost", "MAVLink.*error", "MAVLink.*fail", "connection.*lost", "mavlink.*parse"], "LINK_LOSS"),
    (["battery.*low", "battery.*critical", "battery.*fail", "power.*fail", "power.*module.*fail", "voltage.*low", "cell.*low", "battery.*warning"], "BATTERY_ISSUE"),
    (["geofence.*breach", "geofence.*fail", "mission.*fail", "waypoint.*fail", "takeoff.*fail", "landing.*fail", "mission.*error"], "MISSION_FAILURE"),
    (["FMU.*assert", "FMU.*reset", "FMU.*overheat", "IO.*fail", "SD.*card.*error", "SD.*card.*fail", "log.*error", "log.*fail", "logging.*fail", "flash.*error", "boot.*fail"], "HARDWARE_FAILURE"),
    (["vibration", "vibe.*fail", "vibe.*high", "mechanical.*fail", "frame.*fail", "mount.*fail"], "VIBRATION_ISSUE"),
    (["parameter.*error", "config.*error", "param.*wrong", "parameter.*mismatch", "tuning.*fail", "PID.*fail", "tune.*fail"], "CONFIG_ISSUE"),
    (["error:", "fault:", "FAIL:", "CRITICAL:", "WARNING:"], "GENERIC_ERROR"),
]

AIRFRAME_PATTERNS = [
    (["multicopter", "quad", "quadcopter", "hexacopter", "octocopter", "coaxial"], "MULTICOPTER"),
    (["fixed.wing", "fixedwing", "plane", "airplane"], "FIXED_WING"),
    (["VTOL", "tiltrotor", "tailsitter", "quadplane"], "VTOL"),
    (["rover", "ground", "UGV"], "ROVER"),
    (["boat", "usv", "surface", "ship"], "BOAT"),
    (["sub", "rov", "uuv", "underwater"], "SUBMARINE"),
]

FC_PATTERNS = [
    (["Pixhawk"], "PIXHAWK"),
    (["Cube"], "CUBE"),
    (["Holybro"], "HOLYBRO"),
    (["CUAV"], "CUAV"),
    (["mRo"], "MRO"),
    (["Drotek"], "DROTEK"),
    (["STM32"], "STM32_GENERIC"),
    (["FMUv"], "FMU"),
]


def fetch_json(url, retries=3, delay=1.0):
    """Fetch JSON from URL with retries and polite delay."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "E084-PX4-Fault-Harvest/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(delay)  # Polite polling
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limited
                time.sleep(delay * (attempt + 1) * 2)
                continue
            print(f"HTTP error {e.code} for {url}", file=sys.stderr)
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
        if attempt < retries - 1:
            time.sleep(delay * (attempt + 1))
    return None


def classify_fault(title):
    """Classify fault type from title using patterns."""
    import re
    title_lower = title.lower()
    for patterns, label in FAULT_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                return label
    return None


def extract_airframe(text):
    """Extract airframe type from text."""
    import re
    text_lower = text.lower()
    for patterns, label in AIRFRAME_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return label
    return "UNKNOWN"


def extract_fc(text):
    """Extract flight controller hardware from text."""
    import re
    text_lower = text.lower()
    for patterns, label in FC_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return label
    return "UNKNOWN"


def harvest_latest_pages(max_pages=10):
    """Harvest topics from /latest.json pages."""
    all_topics = []
    for page in range(max_pages):
        url = f"{BASE_URL}/latest.json?no_definitions=true&page={page}"
        print(f"Fetching page {page}...")
        data = fetch_json(url)
        if not data:
            print(f"Failed to fetch page {page}, stopping.")
            break
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            print(f"No topics on page {page}, stopping.")
            break
        all_topics.extend(topics)
        # Save raw page
        with open(RAW_DIR / f"topics_page_{page}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Got {len(topics)} topics")
    return all_topics


def harvest_top_pages(max_pages=10, period="all"):
    """Harvest topics from /top.json pages for historical coverage."""
    all_topics = []
    for page in range(max_pages):
        url = f"{BASE_URL}/top.json?period={period}&page={page}"
        print(f"Fetching top/{period} page {page}...")
        data = fetch_json(url)
        if not data:
            print(f"Failed to fetch top page {page}, stopping.")
            break
        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            print(f"No topics on top page {page}, stopping.")
            break
        all_topics.extend(topics)
        with open(RAW_DIR / f"topics_top_{period}_page_{page}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Got {len(topics)} topics")
    return all_topics


def fetch_topic_details(topic_id):
    """Fetch full topic details including posts."""
    url = f"{BASE_URL}/t/{topic_id}.json"
    return fetch_json(url, delay=0.5)


def main():
    print("=== E084 PX4 Fault Code Harvest ===")
    
    # Harvest latest topics
    print("\n--- Harvesting latest topics ---")
    latest_topics = harvest_latest_pages(max_pages=15)
    
    # Harvest top topics (all time, yearly, monthly)
    print("\n--- Harvesting top topics (all time) ---")
    top_all = harvest_top_pages(max_pages=5, period="all")
    
    print("\n--- Harvesting top topics (yearly) ---")
    top_yearly = harvest_top_pages(max_pages=5, period="yearly")
    
    print("\n--- Harvesting top topics (monthly) ---")
    top_monthly = harvest_top_pages(max_pages=5, period="monthly")
    
    # Combine and deduplicate by topic ID
    all_topics = {}
    for t in latest_topics + top_all + top_yearly + top_monthly:
        tid = t["id"]
        if tid not in all_topics:
            all_topics[tid] = t
    
    print(f"\nTotal unique topics: {len(all_topics)}")
    
    # Filter for fault-indicator topics
    fault_topics = []
    for topic in all_topics.values():
        title = topic.get("title", "")
        fault_type = classify_fault(title)
        if fault_type:
            topic["fault_type"] = fault_type
            topic["airframe"] = extract_airframe(title)
            topic["fc_hardware"] = extract_fc(title)
            fault_topics.append(topic)
    
    print(f"Topics with fault indicators: {len(fault_topics)}")
    
    # Filter for view_count > 0 and reply_count > 0
    qualified_topics = [
        t for t in fault_topics
        if t.get("views", 0) > 0 and t.get("reply_count", 0) > 0
    ]
    print(f"Qualified topics (views>0, replies>0): {len(qualified_topics)}")
    
    # Save classified topics
    with open(RAW_DIR / "classified_topics.jsonl", "w") as f:
        for t in qualified_topics:
            f.write(json.dumps(t) + "\n")
    
    # Save summary
    summary = {
        "total_topics_harvested": len(all_topics),
        "fault_indicator_topics": len(fault_topics),
        "qualified_topics": len(qualified_topics),
        "fault_type_distribution": {},
        "airframe_distribution": {},
        "fc_hardware_distribution": {},
    }
    
    for t in qualified_topics:
        ft = t["fault_type"]
        af = t["airframe"]
        fc = t["fc_hardware"]
        summary["fault_type_distribution"][ft] = summary["fault_type_distribution"].get(ft, 0) + 1
        summary["airframe_distribution"][af] = summary["airframe_distribution"].get(af, 0) + 1
        summary["fc_hardware_distribution"][fc] = summary["fc_hardware_distribution"].get(fc, 0) + 1
    
    with open(RAW_DIR / "harvest_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n=== Fault type distribution ===")
    for ft, count in sorted(summary["fault_type_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {ft}: {count}")
    
    print("\n=== Airframe distribution ===")
    for af, count in sorted(summary["airframe_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {af}: {count}")
    
    print("\n=== FC Hardware distribution ===")
    for fc, count in sorted(summary["fc_hardware_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {fc}: {count}")
    
    print("\nHarvest complete. Qualified topics saved to raw/classified_topics.jsonl")


if __name__ == "__main__":
    main()
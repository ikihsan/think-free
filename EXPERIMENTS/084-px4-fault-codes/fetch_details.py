#!/usr/bin/env python3
"""
E084 — Fetch topic details for structured case assessment (G4)
Stdlib Python 3.8 only, no external dependencies.
"""

import json
import time
import urllib.request
import urllib.error
import sys
import random
from pathlib import Path

BASE_URL = "https://discuss.px4.io"
RAW_DIR = Path("raw")
CLASSIFIED_FILE = RAW_DIR / "classified_topics.jsonl"
DETAILS_DIR = RAW_DIR / "topic_details"
DETAILS_DIR.mkdir(exist_ok=True)

# Root cause specificity patterns (from CLASSIFICATION_RULES.md)
SPECIFIC_PATTERNS = [
    # Specific components
    r"replace\s+\w+", r"replaced\s+\w+",
    r"(GPS|IMU|magnetometer|barometer|ESC|motor|servo|wiring|connector|SD card|flight controller)\b",
    # Specific parameters
    r"EKF2_[A-Z_]+",
    r"GPS_[A-Z_]+",
    r"IMU_[A-Z_]+",
    r"MAG_[A-Z_]+",
    r"BAT_[A-Z_]+",
    r"[A-Z_]*_THR",
    r"[A-Z_]*_MAX",
    r"[A-Z_]*_MIN",
    # Specific actions with detail
    r"recalibrate\s+(magnetometer|compass|accelerometer|gyro|barometer|level)",
    r"check\s+(IMU|GPS|mag|compass|vibration|wiring)\s+(damping|mount|connection)",
    r"set\s+[A-Z_]+",
    r"update\s+firmware\s+to\s+v?\d+\.\d+",
    r"resolder",
    r"replace\s+(GPS module|IMU|magnetometer|barometer|ESC|motor|servo|FC|flight controller)",
]

GENERIC_PATTERNS = [
    r"check\s+wiring",
    r"recalibrate",
    r"update\s+firmware\b",
    r"check\s+connections",
    r"inspect\s+hardware",
    r"debug\s+further",
    r"contact\s+manufacturer",
    r"known\s+issue",
    r"check\s+logs\b",
]


def fetch_topic_details(topic_id):
    """Fetch full topic details including posts."""
    url = f"{BASE_URL}/t/{topic_id}.json"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "E084-PX4-Fault-Harvest/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(0.5)  # Polite polling
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            print(f"HTTP error {e.code} for topic {topic_id}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error fetching topic {topic_id}: {e}", file=sys.stderr)
            return None
    return None


def classify_root_cause(posts):
    """Classify root cause specificity from posts."""
    import re
    
    # Combine all post content
    all_text = " ".join(post.get("cooked", "") for post in posts).lower()
    
    # Check for specific patterns
    specific = False
    generic = False
    
    for pattern in SPECIFIC_PATTERNS:
        if re.search(pattern, all_text, re.IGNORECASE):
            specific = True
            break
    
    for pattern in GENERIC_PATTERNS:
        if re.search(pattern, all_text, re.IGNORECASE):
            generic = True
            break
    
    if specific and not generic:
        return "SPECIFIC"
    elif generic and not specific:
        return "GENERIC"
    elif specific and generic:
        return "MIXED"
    else:
        return "UNCLEAR"


def extract_airframe_from_posts(posts):
    """Extract airframe type from post content."""
    import re
    all_text = " ".join(post.get("cooked", "") for post in posts).lower()
    
    patterns = [
        (["multicopter", "quad", "quadcopter", "hexacopter", "octocopter", "coaxial"], "MULTICOPTER"),
        (["fixed.wing", "fixedwing", "plane", "airplane"], "FIXED_WING"),
        (["VTOL", "tiltrotor", "tailsitter", "quadplane"], "VTOL"),
        (["rover", "ground", "UGV"], "ROVER"),
        (["boat", "usv", "surface", "ship"], "BOAT"),
        (["sub", "rov", "uuv", "underwater"], "SUBMARINE"),
    ]
    
    for pattern_list, label in patterns:
        for pattern in pattern_list:
            if re.search(pattern, all_text, re.IGNORECASE):
                return label
    return "UNKNOWN"


def extract_fc_from_posts(posts):
    """Extract flight controller from post content."""
    import re
    all_text = " ".join(post.get("cooked", "") for post in posts).lower()
    
    patterns = [
        (["Pixhawk"], "PIXHAWK"),
        (["Cube"], "CUBE"),
        (["Holybro"], "HOLYBRO"),
        (["CUAV"], "CUAV"),
        (["mRo"], "MRO"),
        (["Drotek"], "DROTEK"),
        (["STM32"], "STM32_GENERIC"),
        (["FMUv"], "FMU"),
    ]
    
    for pattern_list, label in patterns:
        for pattern in pattern_list:
            if re.search(pattern, all_text, re.IGNORECASE):
                return label
    return "UNKNOWN"


def extract_px4_version(posts):
    """Extract PX4 version from posts."""
    import re
    all_text = " ".join(post.get("cooked", "") for post in posts)
    # PX4 version patterns: v1.14.3, 1.14.3, v1.15.0-beta, etc.
    matches = re.findall(r'(?:PX4|firmware|version)[\s:]*v?(\d+\.\d+\.\d+(?:-[a-z]+)?)', all_text, re.IGNORECASE)
    if matches:
        return matches[0]
    return None


def main():
    # Load classified topics
    topics = []
    with open(CLASSIFIED_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                topics.append(json.loads(line))
    
    print(f"Loaded {len(topics)} qualified topics")
    
    # Select random sample for G4 assessment (up to 50)
    sample_size = min(50, len(topics))
    random.seed(42)  # Reproducible
    sample = random.sample(topics, sample_size)
    
    print(f"Fetching details for {sample_size} random topics...")
    
    structured_cases = []
    root_cause_counts = {"SPECIFIC": 0, "GENERIC": 0, "MIXED": 0, "UNCLEAR": 0}
    
    for i, topic in enumerate(sample):
        tid = topic["id"]
        print(f"  [{i+1}/{sample_size}] Fetching topic {tid}...")
        
        details = fetch_topic_details(tid)
        if not details:
            print(f"    Failed to fetch")
            continue
        
        # Save raw details
        detail_file = DETAILS_DIR / f"topic_{tid}.json"
        with open(detail_file, "w") as f:
            json.dump(details, f, indent=2)
        
        # Check if it's a structured case
        posts = details.get("post_stream", {}).get("posts", [])
        if len(posts) < 2:  # Need at least OP + 1 reply
            print(f"    Not enough posts ({len(posts)})")
            continue
        
        # Classify root cause
        rc_class = classify_root_cause(posts)
        root_cause_counts[rc_class] += 1
        
        # Extract airframe/FC from posts if not in title
        airframe = topic["airframe"]
        fc = topic["fc_hardware"]
        if airframe == "UNKNOWN":
            airframe = extract_airframe_from_posts(posts)
        if fc == "UNKNOWN":
            fc = extract_fc_from_posts(posts)
        
        px4_version = extract_px4_version(posts)
        
        # Check if reply explicitly identifies root cause and repair
        has_root_cause = rc_class in ("SPECIFIC", "GENERIC", "MIXED")
        has_repair = any(
            re.search(r"(fix|repair|replace|recalibrate|set|update|parameter|config)", 
                     post.get("cooked", ""), re.IGNORECASE)
            for post in posts[1:]  # Skip OP
        )
        
        is_structured = has_root_cause and has_repair and (airframe != "UNKNOWN" or fc != "UNKNOWN")
        
        case_info = {
            "topic_id": tid,
            "title": topic["title"],
            "fault_type": topic["fault_type"],
            "airframe": airframe,
            "fc_hardware": fc,
            "px4_version": px4_version,
            "root_cause_class": rc_class,
            "has_repair": has_repair,
            "is_structured_case": is_structured,
            "reply_count": len(posts) - 1,
        }
        
        structured_cases.append(case_info)
        
        print(f"    Fault: {topic['fault_type']}, Airframe: {airframe}, FC: {fc}, RC: {rc_class}, Structured: {is_structured}")
    
    # Save structured cases
    with open(RAW_DIR / "structured_cases.jsonl", "w") as f:
        for case in structured_cases:
            f.write(json.dumps(case) + "\n")
    
    # Summary
    print(f"\n=== Structured Case Assessment ===")
    print(f"Sample size: {sample_size}")
    print(f"Structured cases found: {sum(1 for c in structured_cases if c['is_structured_case'])}")
    print(f"Root cause classification:")
    for cls, count in root_cause_counts.items():
        pct = count / sample_size * 100 if sample_size > 0 else 0
        print(f"  {cls}: {count} ({pct:.1f}%)")
    
    specific_pct = root_cause_counts["SPECIFIC"] / sample_size * 100 if sample_size > 0 else 0
    print(f"\nG4 Root cause specificity: {specific_pct:.1f}% SPECIFIC")
    print(f"  Gate threshold: >= 60%")
    print(f"  Status: {'PASS' if specific_pct >= 60 else 'FAIL' if sample_size > 0 else 'PENDING'}")
    
    # Also count airframe/FC combos in structured cases
    combo_counter = Counter()
    for c in structured_cases:
        if c["is_structured_case"]:
            combo_counter[(c["airframe"], c["fc_hardware"])] += 1
    
    print(f"\nAirframe/FC combos in structured cases:")
    for (af, fc), count in combo_counter.most_common():
        print(f"  {af} + {fc}: {count}")
    
    # Save summary
    summary = {
        "sample_size": sample_size,
        "structured_cases": sum(1 for c in structured_cases if c["is_structured_case"]),
        "root_cause_counts": root_cause_counts,
        "specific_pct": specific_pct,
        "g4_pass": specific_pct >= 60 if sample_size > 0 else None,
        "airframe_fc_combos": {f"{af}+{fc}": count for (af, fc), count in combo_counter.items()},
        "cases": structured_cases,
    }
    
    with open("g4_assessment.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\nG4 assessment saved to g4_assessment.json")


if __name__ == "__main__":
    import re
    from collections import Counter
    main()
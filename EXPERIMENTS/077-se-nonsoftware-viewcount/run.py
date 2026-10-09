#!/usr/bin/env python3
"""
E077 — Non-software Discourse view_count + unserved-open measurement.

Measures the view_count (arrival) instrument and unserved-open-like fraction
across a stratified sample of non-software Discourse forums. Pivoted from
Stack Exchange due to API rate limiting (Cloudflare error 1015).
"""

# origin-meta
# owner: EXPERIMENTS/PLAN.md
# status: active
# last-verified: 2026-10-09

import json
import os
import sys
import time
import urllib.request
from typing import Any, Dict, List, Optional

from measure import (
    harvest_forum_topics, measure_forum, aggregate_results,
    save_raw_data, classify_topics
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Pre-declared Discourse forums (stratified across non-software categories)
TARGET_FORUMS = [
    "community.anovaculinary.com",   # Cooking/Food
    "community.home-assistant.io",   # Home automation
    "discourse.ubuntu.com",          # General tech/Linux
    "meta.discourse.org",            # Meta (about Discourse)
    "forum.arduino.cc",              # Electronics/Hardware
    "community.openhab.org",         # Home automation
    "forum.mysensors.org",           # IoT/Sensors
    "community.linode.com",          # Cloud/Infrastructure
    "forums.raspberrypi.com",        # Hardware/Raspberry Pi
    "community.plotly.com",          # Data visualization
]

TOPICS_PER_FORUM = 50
SLEEP_BETWEEN_REQUESTS = 1.0  # seconds, polite polling


# ---------------------------------------------------------------------------
# Discourse API helpers
# ---------------------------------------------------------------------------

def fetch_latest_page(domain: str, page: int) -> Optional[Dict]:
    """Fetch a page of topics from a Discourse forum."""
    url = f"https://{domain}/latest.json?page={page}&per_page=30"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Think Free E077)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited on {domain} page {page}, waiting 30 seconds...")
            time.sleep(30)
            return fetch_latest_page(domain, page)
        print(f"    Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None


# Move harvest_forum_topics to measure.py and import it


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    """Main entry point."""
    print("=== E077 Non-software Discourse view_count + unserved-open Measurement ===")
    print(f"Target forums: {len(TARGET_FORUMS)}")
    print(f"Topics per forum: {TOPICS_PER_FORUM}")
    print("NOTE: Pivoted from Stack Exchange due to API rate limiting (Cloudflare 1015)")
    print()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    all_topics = []
    all_classified = []

    for domain in TARGET_FORUMS:
        try:
            # Harvest
            topics = harvest_forum_topics(domain)

            # Classify
            classified = classify_topics(topics)

            # Save raw data
            save_raw_data(domain, topics, classified, output_dir)

            # Measure
            result = measure_forum(topics, domain)
            all_results.append(result)

            all_topics.extend(topics)
            all_classified.extend(classified)

        except Exception as e:
            print(f"Error measuring {domain}: {e}")
            all_results.append({
                "domain": domain,
                "total": 0,
                "error": str(e),
            })

    # Aggregate results
    aggregate = aggregate_results(all_results)

    # Save aggregated results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump({
            "pivot_note": "Pivoted from Stack Exchange to Discourse due to Cloudflare 1015 rate limiting",
            "forums": all_results,
            "aggregate": aggregate,
        }, f, sort_keys=True, indent=2)

    print(f"\n=== Results saved to {output_path} ===")

    return 0 if aggregate["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
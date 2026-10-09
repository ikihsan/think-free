#!/usr/bin/env python3
"""
E077 — Non-software Discourse view_count + unserved-open measurement.

Measures the view_count (arrival) instrument and unserved-open-like fraction
across a stratified sample of non-software Discourse forums. Pivoted from
Stack Exchange due to API rate limiting (Cloudflare error 1015).
"""

import json
import os
import sys

from harvest import (
    TOPICS_PER_FORUM,
    harvest_forum_topics,
    save_raw_data,
)
from classify import classify_topics
from measure import measure_forum, aggregate_results, wilson_ci95


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


def main() -> int:
    """Main entry point for E077 Discourse measurement."""
    print("=== E077 Non-software Discourse view_count + unserved-open Measurement ===")
    print(f"Target forums: {len(TARGET_FORUMS)}")
    print(f"Topics per forum: {TOPICS_PER_FORUM}")
    print("NOTE: Pivoted from Stack Exchange due to Cloudflare 1015 rate limiting")
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
            result = measure_forum(classified, domain)
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
    agg = aggregate_results(all_results)

    # Save aggregated results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump({
            "pivot_note": "Pivoted from Stack Exchange to Discourse due to Cloudflare 1015 rate limiting",
            "forums": all_results,
            "aggregate": agg,
        }, f, sort_keys=True, indent=2)

    print(f"\n=== Results saved to {output_path} ===")

    return 0 if agg["all_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
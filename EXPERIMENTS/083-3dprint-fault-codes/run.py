#!/usr/bin/env python3
"""
E083 — 3D printer firmware/hardware fault codes on Discourse forums.
Fresh observation in a new domain to discover whether a concentrated,
structured problem population exists that could support a computational tool.
"""

import json
import os
import sys

from harvest import (
    TOPICS_PER_FORUM,
    harvest_forum_topics,
    harvest_topic_posts,
    save_raw_data,
)
from classify import classify_topics
from measure import measure_forum, aggregate_results, print_results


# ---------------------------------------------------------------------------
# Pre-declared Discourse forums (stratified across 3D printing communities)
# ---------------------------------------------------------------------------

TARGET_FORUMS = [
    "forum.creality.com",      # Creality printers (Ender, K1, CR, Halot series)
    "forum.lulzbot.com",       # LulzBot printers (TAZ, Mini)
    "community.home-assistant.io",  # Home Assistant (includes Klipper/Moonraker)
    "community.openhab.org",   # openHAB (includes 3D printing, Klipper)
    "forum.arduino.cc",        # Arduino (includes Marlin firmware, 3D printer controllers)
]

# Alternates (if any primary fails)
ALTERNATE_FORUMS = [
    "discourse.ubuntu.com",    # Ubuntu (includes Klipper, 3D printing)
    "meta.discourse.org",      # Discourse meta (negative control)
    "community.anovaculinary.com",  # Cooking (negative control, no 3D printing)
]


def main() -> int:
    """Main entry point for E083 3D printer fault code measurement."""
    print("=== E083 3D Printer Fault Codes on Discourse Forums ===")
    print(f"Target forums: {len(TARGET_FORUMS)}")
    print(f"Topics per forum: {TOPICS_PER_FORUM}")
    print("NOTE: Fresh observation in 3D printing hardware/firmware domain")
    print()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    all_topics = []
    all_classified = []
    all_posts = {}

    # Process primary forums
    for domain in TARGET_FORUMS:
        try:
            print(f"\n--- Harvesting {domain} ---")
            # Harvest topics
            topics = harvest_forum_topics(domain)
            print(f"  Harvested {len(topics)} topics")

            # Classify
            classified = classify_topics(topics)
            fault_count = sum(1 for t in classified if t.get("has_fault_indicator"))
            print(f"  Fault indicator topics: {fault_count}")

            # For preliminary analysis, we evaluate on title+metadata only
            # Full structured case analysis requires fetching posts (additional API calls)
            # Fetch posts for fault-indicator topics (up to 20 per forum to limit API calls)
            fault_topic_ids = [t["id"] for t in classified if t.get("has_fault_indicator")][:20]
            posts_by_topic = {}
            if fault_topic_ids:
                print(f"  Fetching posts for {len(fault_topic_ids)} fault topics...")
                posts_by_topic = harvest_topic_posts(domain, fault_topic_ids)

            # Save raw data
            save_raw_data(domain, topics, classified, posts_by_topic, output_dir)

            # Measure
            result = measure_forum(classified, domain)
            all_results.append(result)

            all_topics.extend(topics)
            all_classified.extend(classified)
            all_posts.update(posts_by_topic)

        except Exception as e:
            print(f"Error measuring {domain}: {e}")
            import traceback
            traceback.print_exc()
            all_results.append({
                "domain": domain,
                "total": 0,
                "fault_count": 0,
                "error": str(e),
            })

    # Try alternates if any primary failed
    successful_primaries = sum(1 for r in all_results if "error" not in r)
    if successful_primaries < len(TARGET_FORUMS):
        needed = len(TARGET_FORUMS) - successful_primaries
        print(f"\n--- Trying {needed} alternate forums ---")
        for domain in ALTERNATE_FORUMS[:needed]:
            try:
                print(f"\n--- Harvesting alternate {domain} ---")
                topics = harvest_forum_topics(domain)
                print(f"  Harvested {len(topics)} topics")

                classified = classify_topics(topics)
                fault_count = sum(1 for t in classified if t.get("has_fault_indicator"))
                print(f"  Fault indicator topics: {fault_count}")

                fault_topic_ids = [t["id"] for t in classified if t.get("has_fault_indicator")][:20]
                posts_by_topic = {}
                if fault_topic_ids:
                    print(f"  Fetching posts for {len(fault_topic_ids)} fault topics...")
                    posts_by_topic = harvest_topic_posts(domain, fault_topic_ids)

                save_raw_data(domain, topics, classified, posts_by_topic, output_dir)

                result = measure_forum(classified, domain)
                all_results.append(result)

                all_topics.extend(topics)
                all_classified.extend(classified)
                all_posts.update(posts_by_topic)

            except Exception as e:
                print(f"Error measuring alternate {domain}: {e}")
                all_results.append({
                    "domain": domain,
                    "total": 0,
                    "fault_count": 0,
                    "error": str(e),
                })

    # Aggregate results
    agg = aggregate_results(all_results)

    # Save aggregated results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump({
            "forums": all_results,
            "aggregate": agg,
        }, f, sort_keys=True, indent=2)

    print_results(all_results, agg)
    print(f"\n=== Results saved to {output_path} ===")

    # Also save combined classified data for cross-forum analysis
    combined_path = os.path.join(output_dir, "classified_all.jsonl")
    with open(combined_path, "w") as f:
        for t in all_classified:
            f.write(json.dumps(t) + "\n")
    print(f"Combined classified data saved to {combined_path}")

    return 0 if agg["all_evaluable_gates_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
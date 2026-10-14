#!/usr/bin/env python3
"""fetch_px4.py - Fetch topics from PX4 Discourse forum"""

import json
import os
import re
import sys
import urllib.request
import urllib.error

FORUM_BASE = "https://discuss.px4.io/c/{category}.json"
CATEGORIES = ["px4"]  # PX4 Discourse category slug
TOPICS_PER_CATEGORY = 150  # 150 total
MAX_PAGES = 5  # pagination limit
TOTAL_EXPECTED = 150


def fetch_category(category, page=1):
    """Fetch topics from a Discourse category."""
    url = FORUM_BASE.format(category=category)
    if page > 1:
        url += "?page={}".format(page)

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ThinkFree-Experiment/1.0",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8", "replace"))
            return data
    except Exception as e:
        print("Error fetching {}: {}".format(url, e))
        return None


def extract_topics(data, category):
    """Extract topic metadata from Discourse API response."""
    topics = []
    if not data or "topic_list" not in data:
        return topics

    for topic_data in data.get("topic_list", {}).get("topics", []):
        # Get view_count from the 'views' field, reply_count directly
        view_count = topic_data.get("views", 0)
        if view_count is None:
            view_count = 0
        reply_count = topic_data.get("reply_count", 0)
        if reply_count is None:
            reply_count = 0

        topic = {
            "id": topic_data.get("id"),
            "title": topic_data.get("title", ""),
            "view_count": int(view_count),
            "reply_count": int(reply_count),
            "category": category,
            "archetype": topic_data.get("archetype", ""),
            "tags": topic_data.get("tags", []),
        }
        topics.append(topic)

    return topics


def main():
    all_topics = []
    seen_ids = set()

    for category in CATEGORIES:
        page = 1
        fetched = 0
        while fetched < TOPICS_PER_CATEGORY and page <= MAX_PAGES:
            data = fetch_category(category, page)
            if not data:
                print("No data from {} page {}".format(category, page))
                break
            topics = extract_topics(data, category)
            for t in topics:
                # Skip if already fetched (by ID)
                if t["id"] in seen_ids:
                    continue
                seen_ids.add(t["id"])
                all_topics.append(t)
                fetched += 1
                if len(all_topics) >= TOTAL_EXPECTED:
                    break
            page += 1

    # Deduplicate by ID (just in case)
    unique_topics = []
    seen_ids2 = set()
    for t in all_topics:
        if t["id"] not in seen_ids2:
            seen_ids2.add(t["id"])
            unique_topics.append(t)

    # Sort by view_count descending for matched harvest
    unique_topics.sort(key=lambda t: t["view_count"], reverse=True)

    # Save results
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    results_path = os.path.join(output_dir, "results_raw.json")
    with open(results_path, "w") as f:
        json.dump({"topics": unique_topics, "total": len(unique_topics)}, f, indent=2)

    print("Fetched {} unique topics".format(len(unique_topics)))
    print("Saving to {}".format(results_path))

    # Print view_count summary
    if unique_topics:
        view_counts = [t["view_count"] for t in unique_topics]
        print("View count - min: {}, max: {}, median: {}".format(
            min(view_counts), max(view_counts), sorted(view_counts)[len(view_counts)//2]
        ))
        # Reply count summary
        reply_counts = [t["reply_count"] for t in unique_topics]
        print("Reply count - min: {}, max: {}, median: {}".format(
            min(reply_counts), max(reply_counts), sorted(reply_counts)[len(reply_counts)//2]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
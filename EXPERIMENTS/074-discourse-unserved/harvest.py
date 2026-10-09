#!/usr/bin/env python3
"""Harvest topics from non-technical Discourse instances for E074 measurement."""
import urllib.request
import json
import time
import os
import sys

INSTANCES = [
    ("community.anovaculinary.com", "cooking"),
    ("discuss.pixls.us", "photography"),
    ("community.glowforge.com", "crafts"),
    ("community.roonlabs.com", "audio"),
    ("keebtalk.com", "mechanical_keyboards"),
]

TOPICS_PER_INSTANCE = 150
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page(domain, page):
    url = f"https://{domain}/latest.json?page={page}&per_page=30"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def fetch_topic_body(domain, topic_id):
    url = f"https://{domain}/t/{topic_id}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
        posts = data.get("post_stream", {}).get("posts", [])
        if posts:
            return posts[0].get("cooked", "")[:2000]
        return ""

results = []
for domain, topic in INSTANCES:
    print(f"\n=== Harvesting {domain} ({topic}) ===")
    topics = []
    for page in range(6):  # 6 pages × 30 = 180 topics max
        try:
            data = fetch_page(domain, page)
            page_topics = data.get("topic_list", {}).get("topics", [])
            if not page_topics:
                break
            topics.extend(page_topics)
            print(f"  Page {page}: got {len(page_topics)} topics")
            time.sleep(0.3)
        except Exception as e:
            print(f"  Page {page} error: {e}")
            break

    # Take first N
    topics = topics[:TOPICS_PER_INSTANCE]
    print(f"  Total: {len(topics)} topics from {domain}")

    # Fetch body for first 50 topics (to keep runtime manageable)
    for i, t in enumerate(topics[:50]):
        try:
            body = fetch_topic_body(domain, t["id"])
            t["_body"] = body
            time.sleep(0.2)
        except Exception as e:
            t["_body"] = ""

    results.extend(topics)

# Save
output_path = os.path.join(OUTPUT_DIR, "discourse_topics.json")
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n=== Total: {len(results)} topics saved to {output_path} ===")

# Summary
by_instance = {}
for t in results:
    # Find which instance this came from
    for domain, topic in INSTANCES:
        if domain in t.get("_body", "") or True:  # we don't store domain per topic
            pass
# Actually let me just count
print(f"Topics with view_count > 0: {sum(1 for t in results if t.get('views', 0) > 0)}")
print(f"Topics with body: {sum(1 for t in results if t.get('_body', ''))}")

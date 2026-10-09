#!/usr/bin/env python3
"""Harvest topic list data from non-technical Discourse instances for E074."""
import urllib.request
import json
import time
import os

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

all_topics = []
for domain, topic in INSTANCES:
    print(f"\n=== {domain} ({topic}) ===")
    topics = []
    for page in range(6):
        try:
            data = fetch_page(domain, page)
            page_topics = data.get("topic_list", {}).get("topics", [])
            if not page_topics:
                break
            topics.extend(page_topics)
            print(f"  Page {page}: {len(page_topics)} topics")
            time.sleep(0.3)
        except Exception as e:
            print(f"  Page {page} error: {e}")
            break

    topics = topics[:TOPICS_PER_INSTANCE]
    for t in topics:
        t["_domain"] = domain
        t["_topic_category"] = topic
    all_topics.extend(topics)
    print(f"  Total: {len(topics)} topics")

output_path = os.path.join(OUTPUT_DIR, "discourse_topics.json")
with open(output_path, "w") as f:
    json.dump(all_topics, f, indent=2)

print(f"\n=== Total: {len(all_topics)} topics saved ===")
print(f"Topics with view_count > 0: {sum(1 for t in all_topics if t.get('views', 0) > 0)}")
print(f"Topics with reply_count >= 3: {sum(1 for t in all_topics if t.get('reply_count', 0) >= 3)}")
print(f"Topics with like_count > 0: {sum(1 for t in all_topics if t.get('like_count', 0) > 0)}")

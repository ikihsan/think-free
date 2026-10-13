#!/usr/bin/env python3
"""
E123 — Fetch Discourse Meta (meta.discourse.org) data for E119 matched-harvest measurement.

Fresh observation in a new domain per D083: the Discourse meta community itself.
"""

import json
import sys
import urllib.request
import time
from pathlib import Path

# Categories to fetch from meta.discourse.org
CATEGORIES = [
    ("support", 8),      # Support questions
    ("feature", 7),      # Feature requests
    ("bug", 9),          # Bug reports
    ("dev", 10),         # Development discussions
    ("marketplace", 11), # Marketplace
    ("hosting", 12),     # Hosting
    ("admins", 13),      # Admins
    ("mods", 14),        # Moderators
]

BASE_URL = "https://meta.discourse.org"

def fetch_category(category_slug, category_id, pages=10, per_page=30):
    """Fetch topics from a Discourse category."""
    all_topics = []
    for page in range(pages):
        url = f"{BASE_URL}/c/{category_slug}/{category_id}.json?page={page}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/E123"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
                topics = data.get("topic_list", {}).get("topics", [])
                if not topics:
                    break
                all_topics.extend(topics)
                print(f"  Page {page}: {len(topics)} topics")
        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break
        time.sleep(0.5)  # Rate limiting
    return all_topics


def main():
    print("=== E123 Fetching meta.discourse.org ===")
    all_topics = []
    
    for cat_slug, cat_id in CATEGORIES:
        print(f"\nFetching category: {cat_slug} (id={cat_id})")
        topics = fetch_category(cat_slug, cat_id, pages=5)
        for t in topics:
            t["source_category"] = cat_slug
        all_topics.extend(topics)
        if len(all_topics) >= 1000:
            break
    
    # Deduplicate by topic id
    seen = set()
    unique = []
    for t in all_topics:
        tid = t.get("id")
        if tid and tid not in seen:
            seen.add(tid)
            unique.append(t)
    
    # Filter for view_count > 0
    valid = [t for t in unique if t.get("views", 0) > 0]
    
    # Sort by views descending (matched harvest: same metric for both arms)
    valid.sort(key=lambda t: t.get("views", 0), reverse=True)
    
    print(f"\nTotal unique topics: {len(unique)}")
    print(f"Topics with views > 0: {len(valid)}")
    
    # Save as JSONL with combined_text for classification
    output_path = Path(__file__).parent / "data_meta.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for t in valid[:500]:  # Limit to 500 for experiment
            title = t.get("title", "")
            # Discourse API doesn't include body in list view; we'd need to fetch each topic
            # For now, use title + excerpt
            excerpt = t.get("excerpt", "")
            combined = f"{title} {excerpt}" if excerpt else title
            
            row = {
                "topic_id": t.get("id"),
                "title": title,
                "excerpt": excerpt[:200] if excerpt else "",
                "view_count": t.get("views", 0),
                "reply_count": t.get("reply_count", 0),
                "like_count": t.get("like_count", 0),
                "has_accepted_answer": t.get("has_accepted_answer", False),
                "tags": t.get("tags", []),
                "category": t.get("source_category", ""),
                "combined_text": combined,
            }
            f.write(json.dumps(row) + "\n")
    
    print(f"Saved {min(len(valid), 500)} topics to {output_path}")
    
    # Quick tag/category breakdown
    from collections import Counter
    cat_counts = Counter(t.get("source_category", "") for t in valid[:500])
    for cat, count in cat_counts.most_common():
        print(f"  Category {cat}: {count} items")


if __name__ == "__main__":
    main()
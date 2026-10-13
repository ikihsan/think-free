#!/usr/bin/env python3
"""
E125 — Fetch Jupyter Discourse (discourse.jupyter.org) data for matched-harvest measurement.

Fresh observation in a new domain per D083: Jupyter's Discourse forum (Q&A support style).
"""

import json
import sys
import urllib.request
import time
from pathlib import Path

# Categories to fetch from discourse.jupyter.org
CATEGORIES = [
    ("help", 6),              # Help/Support
    ("community", 7),         # Community
    ("development", 8),       # Development
    ("extensions", 9),        # Extensions
    ("hub", 10),              # JupyterHub
    ("lab", 11),              # JupyterLab
    ("notebook", 12),         # Notebook
]

BASE_URL = "https://discourse.jupyter.org"

def fetch_category(category_slug, category_id, pages=10, per_page=30):
    """Fetch topics from a Discourse category."""
    all_topics = []
    for page in range(pages):
        url = f"{BASE_URL}/c/{category_slug}/{category_id}.json?page={page}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "think-free/E125"})
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
    print("=== E125 Fetching discourse.jupyter.org ===")
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
    output_path = Path(__file__).parent / "data_jupyter.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for t in valid[:500]:  # Limit to 500 for experiment
            title = t.get("title", "")
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
    
    # Quick category breakdown
    from collections import Counter
    cat_counts = Counter(t.get("source_category", "") for t in valid[:500])
    for cat, count in cat_counts.most_common():
        print(f"  Category {cat}: {count} items")


if __name__ == "__main__":
    main()
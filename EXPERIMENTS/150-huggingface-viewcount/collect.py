#!/usr/bin/env python3
"""
Collect model data from Hugging Face Hub API.
Fetches models via multiple sort strategies for diverse coverage.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, List, Set, Optional

BASE_URL = "https://huggingface.co/api/models"
HEADERS = {"User-Agent": "think-free-experiment/1.0"}

# Sort strategies to get diverse coverage
SORT_STRATEGIES = [
    ("downloads", "downloads"),
    ("likes", "likes"),
    ("trendingScore", "trending"),
    ("createdAt", "recent"),
    ("lastModified", "modified"),
]

LIMIT_PER_SORT = 500
TOTAL_TARGET = 2000
REQUEST_DELAY = 0.1  # Be nice to the API


def fetch_models(sort: str, limit: int) -> List[Dict]:
    """Fetch models with given sort order."""
    url = f"{BASE_URL}?sort={sort}&direction=-1&limit={limit}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for sort={sort}: {e.read().decode()}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching sort={sort}: {e}", file=sys.stderr)
        return []


def fetch_random_sample(count: int) -> List[Dict]:
    """Fetch a random-ish sample by paginating through results."""
    models = []
    page = 0
    per_page = 100
    while len(models) < count:
        url = f"{BASE_URL}?limit={per_page}&page={page}"
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                batch = json.load(resp)
                if not batch:
                    break
                models.extend(batch)
                page += 1
                time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(f"Error fetching page {page}: {e}", file=sys.stderr)
            break
    return models[:count]


def main():
    print("Starting Hugging Face model collection...", file=sys.stderr)
    all_models: Dict[str, Dict] = {}  # deduplicate by modelId
    seen_ids: Set[str] = set()

    # Strategy 1: Top by different metrics
    for sort_key, sort_name in SORT_STRATEGIES:
        print(f"Fetching top {LIMIT_PER_SORT} by {sort_name}...", file=sys.stderr)
        batch = fetch_models(sort_key, LIMIT_PER_SORT)
        for m in batch:
            mid = m.get("modelId") or m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                all_models[mid] = m
        print(f"  Got {len(batch)}, total unique: {len(all_models)}", file=sys.stderr)
        time.sleep(REQUEST_DELAY)

    # Strategy 2: Random sample for tail coverage
    print(f"Fetching random sample...", file=sys.stderr)
    random_batch = fetch_random_sample(500)
    for m in random_batch:
        mid = m.get("modelId") or m.get("id")
        if mid and mid not in seen_ids:
            seen_ids.add(mid)
            all_models[mid] = m
    print(f"  Total unique after random: {len(all_models)}", file=sys.stderr)

    # Write raw data
    output_path = "EXPERIMENTS/150-huggingface-viewcount/RAW_DATA.jsonl"
    with open(output_path, "w") as f:
        for m in all_models.values():
            f.write(json.dumps(m) + "\n")
    print(f"Wrote {len(all_models)} models to {output_path}", file=sys.stderr)

    # Print summary stats
    likes = [m.get("likes", 0) for m in all_models.values()]
    downloads = [m.get("downloads", 0) for m in all_models.values()]
    trending = [m.get("trendingScore", 0) for m in all_models.values()]
    print(f"Likes: min={min(likes)}, max={max(likes)}, median={sorted(likes)[len(likes)//2]}", file=sys.stderr)
    print(f"Downloads: min={min(downloads)}, max={max(downloads)}, median={sorted(downloads)[len(downloads)//2]}", file=sys.stderr)
    print(f"Trending: min={min(trending)}, max={max(trending)}, median={sorted(trending)[len(trending)//2]}", file=sys.stderr)


if __name__ == "__main__":
    main()
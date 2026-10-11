#!/usr/bin/env python3
"""
E095: crates.io view-count principle test - Data Collection v2
Fetches random crates and classifies them by keywords/categories.
"""

import json
import time
import random
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Set, Optional

BASE_URL = "https://crates.io/api/v1"
USER_AGENT = "ThinkFree/1.0"
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Need-related keywords (from keyword search)
NEED_KEYWORDS = {
    "debugging", "debug", "error-handling", "error", "profiling", "profile",
    "logging", "log", "monitoring", "monitor", "tracing", "trace",
    "diagnostics", "diagnostic", "observability", "observe",
    "benchmarking", "benchmark", "testing", "test",
    "panic", "backtrace", "crash", "troubleshooting"
}

# Need-related categories (from category list)
NEED_CATEGORIES = {
    "development-tools::debugging",
    "development-tools::profiling",
    "development-tools::testing",
    "development-tools::benchmarking",
    "monitoring",
    "observability",
    "logging",
    "tracing",
}

TARGET_TOTAL = 300  # Fetch this many random crates, then classify
RAW_DIR = Path("EXPERIMENTS/095-crates-io-viewcount/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_json(url: str) -> Optional[Dict]:
    """Fetch JSON from URL with rate limiting and error handling."""
    time.sleep(RATE_LIMIT_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} for {url}: {e.reason}")
        if e.code == 429:
            print("Rate limited, waiting longer...")
            time.sleep(60)
            return fetch_json(url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None


def fetch_crate_details(name: str) -> Optional[Dict]:
    """Fetch detailed crate info including keywords and categories."""
    url = f"{BASE_URL}/crates/{name}"
    data = fetch_json(url)
    if data and "crate" in data:
        return data["crate"]
    return None


def is_need_related(crate: Dict) -> bool:
    """Check if crate is need-related based on keywords or categories."""
    keywords = set(crate.get("keywords", []))
    categories = set(crate.get("categories", []))
    
    # Check keywords
    if keywords & NEED_KEYWORDS:
        return True
    
    # Check categories
    if categories & NEED_CATEGORIES:
        return True
    
    return False


def main():
    print("=" * 60)
    print("E095: crates.io view-count data collection v2")
    print("=" * 60)
    
    # Step 1: Fetch random crates from first ~400 pages (max page that works)
    print("\n1. Fetching random crates from first 400 pages...")
    all_crates = []
    seen_names = set()
    
    # Pages 1-400 are valid (400*100 = 40,000 crates)
    pages = list(range(1, 401))
    random.shuffle(pages)
    
    for page in pages:
        if len(all_crates) >= TARGET_TOTAL:
            break
        url = f"{BASE_URL}/crates?per_page=100&page={page}"
        print(f"  Fetching page {page} (got {len(all_crates)}/{TARGET_TOTAL})...")
        data = fetch_json(url)
        if not data or "crates" not in data:
            continue
        for crate in data["crates"]:
            if crate["name"] not in seen_names:
                seen_names.add(crate["name"])
                all_crates.append(crate)
                if len(all_crates) >= TARGET_TOTAL:
                    break
    
    print(f"\nFetched {len(all_crates)} unique crates")
    
    # Step 2: Fetch detailed info for all crates
    print("\n2. Fetching detailed crate info (keywords, categories)...")
    detailed_crates = []
    
    for i, crate in enumerate(all_crates):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(all_crates)}")
        details = fetch_crate_details(crate["name"])
        if details:
            # Merge basic info with details
            merged = {**crate, **details}
            detailed_crates.append(merged)
        else:
            detailed_crates.append(crate)
    
    print(f"\nGot details for {len(detailed_crates)} crates")
    
    # Step 3: Classify
    print("\n3. Classifying crates...")
    need_related = []
    not_need_related = []
    
    for crate in detailed_crates:
        if is_need_related(crate):
            need_related.append(crate)
        else:
            not_need_related.append(crate)
    
    print(f"Need-related: {len(need_related)}")
    print(f"Not need-related: {len(not_need_related)}")
    
    # Show some examples of need-related crates
    print("\nExample need-related crates:")
    for c in need_related[:10]:
        kw = c.get("keywords", [])
        cat = c.get("categories", [])
        print(f"  {c['name']}: keywords={kw}, categories={cat}, downloads={c.get('downloads', 0)}, recent={c.get('recent_downloads', 0)}")
    
    # Save raw data
    output = {
        "collection_timestamp": time.time(),
        "need_keywords": list(NEED_KEYWORDS),
        "need_categories": list(NEED_CATEGORIES),
        "target_total": TARGET_TOTAL,
        "total_fetched": len(detailed_crates),
        "need_related_count": len(need_related),
        "not_need_related_count": len(not_need_related),
        "need_related": need_related,
        "not_need_related": not_need_related,
    }
    
    output_path = RAW_DIR / "crates_data_v2.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved raw data to {output_path}")
    print("Collection complete.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
E095: crates.io view-count principle test - Data Collection
Collects crate metadata from crates.io API for need-related and random crates.
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
RATE_LIMIT_DELAY = 1.0  # seconds between requests

NEED_KEYWORDS = [
    "debugging", "error-handling", "profiling", "logging",
    "monitoring", "tracing", "diagnostics", "observability",
    "benchmarking", "error", "panic", "backtrace"
]

TARGET_SAMPLE_SIZE = 200
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


def fetch_keyword_crates(keyword: str) -> List[Dict]:
    """Fetch all crates for a given keyword."""
    crates = []
    page = 1
    while True:
        url = f"{BASE_URL}/keywords/{keyword}/crates?per_page=100&page={page}"
        print(f"  Fetching {keyword} page {page}...")
        data = fetch_json(url)
        if not data or "crates" not in data:
            break
        page_crates = data["crates"]
        if not page_crates:
            break
        crates.extend(page_crates)
        if len(page_crates) < 100:
            break
        page += 1
    print(f"  {keyword}: {len(crates)} crates")
    return crates


def fetch_random_crates(target: int, exclude_names: Set[str]) -> List[Dict]:
    """Fetch random crates not in exclude_names."""
    crates = []
    # crates.io has ~350k crates, 100 per page = ~3500 pages
    # Sample random pages
    pages = list(range(1, 3500))
    random.shuffle(pages)
    
    for page in pages:
        if len(crates) >= target:
            break
        url = f"{BASE_URL}/crates?per_page=100&page={page}"
        print(f"  Fetching random page {page} (got {len(crates)}/{target})...")
        data = fetch_json(url)
        if not data or "crates" not in data:
            continue
        for crate in data["crates"]:
            if crate["name"] not in exclude_names:
                crates.append(crate)
                if len(crates) >= target:
                    break
    return crates


def fetch_crate_details(name: str) -> Optional[Dict]:
    """Fetch detailed crate info including keywords and categories."""
    url = f"{BASE_URL}/crates/{name}"
    data = fetch_json(url)
    if data and "crate" in data:
        return data["crate"]
    return None


def main():
    print("=" * 60)
    print("E095: crates.io view-count data collection")
    print("=" * 60)
    
    # Step 1: Fetch need-related crates
    print("\n1. Fetching need-related crates...")
    all_need_crates = []
    seen_names = set()
    
    for kw in NEED_KEYWORDS:
        crates = fetch_keyword_crates(kw)
        for c in crates:
            if c["name"] not in seen_names:
                seen_names.add(c["name"])
                c["matched_keywords"] = [kw]
                all_need_crates.append(c)
            else:
                # Add keyword to existing crate
                for existing in all_need_crates:
                    if existing["name"] == c["name"]:
                        existing["matched_keywords"].append(kw)
                        break
    
    print(f"\nTotal unique need-related crates: {len(all_need_crates)}")
    
    # Sample need-related crates
    if len(all_need_crates) > TARGET_SAMPLE_SIZE:
        need_sample = random.sample(all_need_crates, TARGET_SAMPLE_SIZE)
    else:
        need_sample = all_need_crates
    
    need_names = {c["name"] for c in need_sample}
    print(f"Need-related sample size: {len(need_sample)}")
    
    # Step 2: Fetch random crates
    print("\n2. Fetching random crates...")
    random_sample = fetch_random_crates(TARGET_SAMPLE_SIZE, need_names)
    random_names = {c["name"] for c in random_sample}
    print(f"Random sample size: {len(random_sample)}")
    
    # Step 3: Fetch detailed info for all sampled crates (to get keywords/categories)
    print("\n3. Fetching detailed crate info...")
    all_sampled = need_sample + random_sample
    detailed_crates = []
    
    for i, crate in enumerate(all_sampled):
        if i % 20 == 0:
            print(f"  Progress: {i}/{len(all_sampled)}")
        details = fetch_crate_details(crate["name"])
        if details:
            # Merge basic info with details
            merged = {**crate, **details}
            detailed_crates.append(merged)
        else:
            detailed_crates.append(crate)
    
    # Separate back into need-related and random
    need_detailed = [c for c in detailed_crates if c["name"] in need_names]
    random_detailed = [c for c in detailed_crates if c["name"] in random_names]
    
    print(f"\nNeed-related with details: {len(need_detailed)}")
    print(f"Random with details: {len(random_detailed)}")
    
    # Save raw data
    output = {
        "collection_timestamp": time.time(),
        "need_keywords": NEED_KEYWORDS,
        "target_sample_size": TARGET_SAMPLE_SIZE,
        "need_related": need_detailed,
        "random": random_detailed,
    }
    
    output_path = RAW_DIR / "crates_data.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved raw data to {output_path}")
    print("Collection complete.")


if __name__ == "__main__":
    main()
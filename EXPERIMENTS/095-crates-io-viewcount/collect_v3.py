#!/usr/bin/env python3
"""
E095: crates.io view-count principle test - Data Collection v3
Searches for need-related crates by keyword, fetches details, and compares with random sample.
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
RATE_LIMIT_DELAY = 0.3  # seconds between requests

NEED_KEYWORDS = [
    "logging", "monitoring", "observability", "tracing", "telemetry", "tracking",
    "debug", "debugging", "error", "profiling", "benchmark", "testing",
    "panic", "backtrace", "diagnostics", "troubleshooting"
]

TARGET_PER_KEYWORD = 30  # Target crates per keyword
TARGET_RANDOM = 200      # Random sample size for comparison
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


def search_keyword(keyword: str, limit: int) -> List[str]:
    """Search for crates by keyword, return list of crate names."""
    names = []
    url = f"{BASE_URL}/crates?q=keyword:{keyword}&per_page=100"
    while url and len(names) < limit:
        print(f"  Searching {keyword} (got {len(names)}/{limit})...")
        data = fetch_json(url)
        if not data or "crates" not in data:
            break
        for crate in data["crates"]:
            names.append(crate["name"])
            if len(names) >= limit:
                break
        # Get next page URL
        url = data.get("meta", {}).get("next_page")
        if url:
            url = f"{BASE_URL}/crates{url}"
    return names[:limit]


def fetch_crate_details(name: str) -> Optional[Dict]:
    """Fetch detailed crate info including keywords and categories."""
    url = f"{BASE_URL}/crates/{name}"
    data = fetch_json(url)
    if data and "crate" in data:
        return data["crate"]
    return None


def fetch_random_crates(target: int, exclude_names: Set[str]) -> List[Dict]:
    """Fetch random crates not in exclude_names."""
    crates = []
    # Valid pages are 1-400 (approx 40k crates)
    pages = list(range(1, 401))
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


def main():
    print("=" * 60)
    print("E095: crates.io view-count data collection v3")
    print("=" * 60)
    
    # Step 1: Search for need-related crates by keyword
    print("\n1. Searching for need-related crates by keyword...")
    all_need_names = set()
    keyword_results = {}
    
    for kw in NEED_KEYWORDS:
        names = search_keyword(kw, TARGET_PER_KEYWORD)
        keyword_results[kw] = names
        all_need_names.update(names)
        print(f"  {kw}: {len(names)} crates")
    
    print(f"\nTotal unique need-related crate names: {len(all_need_names)}")
    
    # Step 2: Fetch details for need-related crates
    print("\n2. Fetching details for need-related crates...")
    need_crates = []
    for i, name in enumerate(all_need_names):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(all_need_names)}")
        details = fetch_crate_details(name)
        if details:
            need_crates.append(details)
        else:
            # Fallback: create minimal record
            need_crates.append({"name": name, "downloads": 0, "recent_downloads": 0, "keywords": [], "categories": []})
    
    print(f"Got details for {len(need_crates)} need-related crates")
    
    # Step 3: Fetch random crates for comparison
    print("\n3. Fetching random crates for comparison...")
    random_basic = fetch_random_crates(TARGET_RANDOM, all_need_names)
    random_names = {c["name"] for c in random_basic}
    
    print("\n4. Fetching details for random crates...")
    random_crates = []
    for i, crate in enumerate(random_basic):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(random_basic)}")
        details = fetch_crate_details(crate["name"])
        if details:
            random_crates.append(details)
        else:
            random_crates.append(crate)
    
    print(f"Got details for {len(random_crates)} random crates")
    
    # Step 4: Verify classification
    print("\n5. Verifying classification...")
    need_verified = []
    random_verified = []
    
    for crate in need_crates:
        # Double-check it actually has need-related keywords
        keywords = set(crate.get("keywords", []))
        categories = set(crate.get("categories", []))
        if any(kw in keywords for kw in NEED_KEYWORDS) or "development-tools::debugging" in categories:
            need_verified.append(crate)
        else:
            # Misclassified - move to random
            random_verified.append(crate)
    
    for crate in random_crates:
        keywords = set(crate.get("keywords", []))
        categories = set(crate.get("categories", []))
        if any(kw in keywords for kw in NEED_KEYWORDS) or "development-tools::debugging" in categories:
            # Actually need-related
            need_verified.append(crate)
        else:
            random_verified.append(crate)
    
    print(f"Verified need-related: {len(need_verified)}")
    print(f"Verified random: {len(random_verified)}")
    
    # Show examples
    print("\nExample need-related crates:")
    for c in need_verified[:10]:
        kw = c.get("keywords", [])
        cat = c.get("categories", [])
        print(f"  {c['name']}: keywords={kw}, categories={cat}, downloads={c.get('downloads', 0)}, recent={c.get('recent_downloads', 0)}")
    
    print("\nExample random crates:")
    for c in random_verified[:10]:
        kw = c.get("keywords", [])
        cat = c.get("categories", [])
        print(f"  {c['name']}: keywords={kw}, categories={cat}, downloads={c.get('downloads', 0)}, recent={c.get('recent_downloads', 0)}")
    
    # Save raw data
    output = {
        "collection_timestamp": time.time(),
        "need_keywords": NEED_KEYWORDS,
        "target_per_keyword": TARGET_PER_KEYWORD,
        "target_random": TARGET_RANDOM,
        "keyword_results": keyword_results,
        "need_related": need_verified,
        "random": random_verified,
    }
    
    output_path = RAW_DIR / "crates_data_v3.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved raw data to {output_path}")
    print("Collection complete.")


if __name__ == "__main__":
    main()
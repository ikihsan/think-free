#!/usr/bin/env python3
"""
E220: Fetch USAspending NAICS and recipient data for 3 enterable IT PSC codes.

Current window: FY2023. Prior window: FY2018-2022 (5 years).
Writes raw/ with NAICS breakdown and per-(PSC, NAICS) recipient data.
"""

import json
import os
import hashlib
import time
import requests
from pathlib import Path

BASE_URL = "https://api.usaspending.gov/api/v2/search/spending_by_category/"

CODES = ["DA01", "DA10", "7A21"]
WINDOWS = {
    "current": [{"start_date": "2023-01-01", "end_date": "2023-12-31"}],
    "prior": [{"start_date": "2018-01-01", "end_date": "2022-12-31"}],
}

EXP_DIR = Path(__file__).parent
RAW_DIR = EXP_DIR / "raw"
RAW_DIR.mkdir(exist_ok=True)

CACHE_FILE = RAW_DIR / "fetch_cache.json"
RATE_LIMIT_DELAY = 65  # seconds between requests (60 req/hour limit)


def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_atomic(path: Path, content: str):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content)
    tmp.replace(path)


def fetch_with_cache(url, payload, cache_key, cache):
    """Fetch from API or cache, with rate limiting and integrity."""
    if cache_key in cache:
        cached = cache[cache_key]
        path = RAW_DIR / cached["file"]
        if path.exists():
            with open(path, "rb") as f:
                if sha256_bytes(f.read()) == cached["sha256"]:
                    print(f"  [CACHE] {cache_key}")
                    with open(path) as f:
                        return json.load(f)
    
    print(f"  [FETCH] {cache_key} ...", flush=True)
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    
    # Write raw response
    fname = f"{cache_key}.json"
    fpath = RAW_DIR / fname
    content = json.dumps(data)
    write_atomic(fpath, content)
    
    # Write meta with SHA-256
    meta = {
        "cache_key": cache_key,
        "file": fname,
        "sha256": sha256_bytes(content.encode()),
        "url": url,
        "payload": payload,
    }
    meta_path = RAW_DIR / f"{cache_key}.meta.json"
    write_atomic(meta_path, json.dumps(meta, indent=2))
    
    # Update cache
    cache[cache_key] = {"file": fname, "sha256": meta["sha256"]}
    save_cache(cache)
    
    # Rate limit
    time.sleep(RATE_LIMIT_DELAY)
    return data


def fetch_naics(code, window, cache):
    """Fetch NAICS breakdown for a PSC code in a window."""
    url = f"{BASE_URL}naics/"
    payload = {
        "filters": {"psc_codes": [code], "time_period": window},
        "category": "naics",
        "limit": 100,
    }
    cache_key = f"naics_{code}_{window[0]['start_date'][:4]}"
    return fetch_with_cache(url, payload, cache_key, cache)


def fetch_recipients(code, naics, window, cache):
    """Fetch recipients for a (PSC, NAICS) combination in a window."""
    url = f"{BASE_URL}recipient/"
    payload = {
        "filters": {"psc_codes": [code], "naics_codes": [naics], "time_period": window},
        "category": "recipient",
        "limit": 100,
    }
    cache_key = f"recipients_{code}_{naics}_{window[0]['start_date'][:4]}"
    return fetch_with_cache(url, payload, cache_key, cache)


def fetch_all_naics_pages(code, window, cache):
    """Fetch all pages of NAICS breakdown for a PSC code."""
    url = f"{BASE_URL}naics/"
    payload = {
        "filters": {"psc_codes": [code], "time_period": window},
        "category": "naics",
        "limit": 100,
    }
    cache_key = f"naics_{code}_{window[0]['start_date'][:4]}"
    
    # Check cache first
    if cache_key in cache:
        cached = cache[cache_key]
        path = RAW_DIR / cached["file"]
        if path.exists():
            with open(path, "rb") as f:
                if sha256_bytes(f.read()) == cached["sha256"]:
                    print(f"  [CACHE] {cache_key}")
                    with open(path) as f:
                        return json.load(f)
    
    print(f"  [FETCH] {cache_key} ...", flush=True)
    all_results = []
    page = 1
    while True:
        p_payload = {**payload, "page": page}
        resp = requests.post(url, json=p_payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        page_meta = data.get("page_metadata", {})
        if not page_meta.get("hasNext", False):
            break
        page += 1
        time.sleep(RATE_LIMIT_DELAY)
    
    # Combine into single response format
    combined = {
        "category": "naics",
        "spending_level": "transactions",
        "limit": 100,
        "page_metadata": {"page": 1, "next": None, "previous": None, "hasNext": False, "hasPrevious": False},
        "results": all_results,
    }
    
    fname = f"{cache_key}.json"
    fpath = RAW_DIR / fname
    content = json.dumps(combined)
    write_atomic(fpath, content)
    
    meta = {
        "cache_key": cache_key,
        "file": fname,
        "sha256": sha256_bytes(content.encode()),
        "url": url,
        "payload": payload,
        "pages_fetched": page,
    }
    meta_path = RAW_DIR / f"{cache_key}.meta.json"
    write_atomic(meta_path, json.dumps(meta, indent=2))
    
    cache[cache_key] = {"file": fname, "sha256": meta["sha256"]}
    save_cache(cache)
    return combined


def fetch_all_recipient_pages(code, naics, window, cache):
    """Fetch all pages of recipients for a (PSC, NAICS) combination."""
    url = f"{BASE_URL}recipient/"
    payload = {
        "filters": {"psc_codes": [code], "naics_codes": [naics], "time_period": window},
        "category": "recipient",
        "limit": 100,
    }
    cache_key = f"recipients_{code}_{naics}_{window[0]['start_date'][:4]}"
    
    # Check cache first
    if cache_key in cache:
        cached = cache[cache_key]
        path = RAW_DIR / cached["file"]
        if path.exists():
            with open(path, "rb") as f:
                if sha256_bytes(f.read()) == cached["sha256"]:
                    print(f"  [CACHE] {cache_key}")
                    with open(path) as f:
                        return json.load(f)
    
    print(f"  [FETCH] {cache_key} ...", flush=True)
    all_results = []
    page = 1
    while True:
        p_payload = {**payload, "page": page}
        resp = requests.post(url, json=p_payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        page_meta = data.get("page_metadata", {})
        if not page_meta.get("hasNext", False):
            break
        page += 1
        time.sleep(RATE_LIMIT_DELAY)
    
    combined = {
        "category": "recipient",
        "spending_level": "transactions",
        "limit": 100,
        "page_metadata": {"page": 1, "next": None, "previous": None, "hasNext": False, "hasPrevious": False},
        "results": all_results,
    }
    
    fname = f"{cache_key}.json"
    fpath = RAW_DIR / fname
    content = json.dumps(combined)
    write_atomic(fpath, content)
    
    meta = {
        "cache_key": cache_key,
        "file": fname,
        "sha256": sha256_bytes(content.encode()),
        "url": url,
        "payload": payload,
        "pages_fetched": page,
    }
    meta_path = RAW_DIR / f"{cache_key}.meta.json"
    write_atomic(meta_path, json.dumps(meta, indent=2))
    
    cache[cache_key] = {"file": fname, "sha256": meta["sha256"]}
    save_cache(cache)
    return combined


def main():
    print("=" * 72)
    print("E220 FETCH — IT PSC Sub-Segment Entrant Advisor")
    print("=" * 72)
    
    cache = load_cache()
    
    # Step 1: Fetch NAICS breakdown for all 3 codes, both windows
    print("\n--- Step 1: NAICS Breakdown ---")
    naics_data = {}
    for code in CODES:
        for window_name, window in WINDOWS.items():
            data = fetch_all_naics_pages(code, window, cache)
            naics_data[(code, window_name)] = data
            results = data.get("results", [])
            print(f"    {code} {window_name}: {len(results)} NAICS codes")
    
    # Step 2: Select top NAICS codes by obligation for recipient fetch
    # Prioritize: top 5 by obligation per code per window, but deduplicate
    print("\n--- Step 2: Select Top NAICS for Recipient Fetch ---")
    target_naics = {}  # code -> set of naics codes
    
    for code in CODES:
        target_naics[code] = set()
        for window_name in ["current", "prior"]:
            data = naics_data[(code, window_name)]
            results = data.get("results", [])
            # Sort by amount descending
            sorted_results = sorted(results, key=lambda x: x.get("amount", 0), reverse=True)
            for r in sorted_results[:8]:  # Top 8 per window
                naics = r.get("code")
                if naics:
                    target_naics[code].add(naics)
        print(f"    {code}: {len(target_naics[code])} target NAICS codes: {sorted(target_naics[code])}")
    
    # Step 3: Fetch recipients for each (code, naics, window)
    print("\n--- Step 3: Recipient Data per (PSC, NAICS) ---")
    for code in CODES:
        for naics in sorted(target_naics[code]):
            for window_name, window in WINDOWS.items():
                data = fetch_all_recipient_pages(code, naics, window, cache)
                results = data.get("results", [])
                print(f"    {code} NAICS {naics} {window_name}: {len(results)} recipients")
    
    # Summary
    print("\n" + "=" * 72)
    print("FETCH COMPLETE")
    print("=" * 72)
    
    # Count files
    json_files = list(RAW_DIR.glob("*.json"))
    meta_files = list(RAW_DIR.glob("*.meta.json"))
    print(f"Raw JSON files: {len([f for f in json_files if not f.name.endswith('.meta.json')])}")
    print(f"Meta files: {len(meta_files)}")
    print(f"Cache entries: {len(cache)}")
    
    return 0


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
E222: fetch the outcome window (FY2024-2025) recipient lists for the 23
population sub-segments declared in PROTOCOL.md.

The only network step of E222. Resumable: each response is written to raw/
with SHA-256 + request meta; valid cached responses are skipped on re-run.
Rate limited to <= 1 request / 65 s (USAspending unauthenticated limit).
"""

import hashlib
import json
import time
import urllib.request
from pathlib import Path

EXP_DIR = Path(__file__).parent
RAW_DIR = EXP_DIR / "raw"
RAW_DIR.mkdir(exist_ok=True)
POP_FILE = EXP_DIR / "results" / "preflight_population.json"

BASE_URL = "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/"
OUTCOME_WINDOW = [{"start_date": "2024-01-01", "end_date": "2025-12-31"}]
RATE_LIMIT_DELAY = 65
USER_AGENT = "think-free-research/0.1 (+e222-forward-outcome)"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def cache_valid(cache_key):
    fpath = RAW_DIR / f"{cache_key}.json"
    meta_path = RAW_DIR / f"{cache_key}.meta.json"
    if not (fpath.exists() and meta_path.exists()):
        return None
    with open(meta_path) as f:
        meta = json.load(f)
    with open(fpath, "rb") as f:
        if sha256_bytes(f.read()) == meta.get("sha256"):
            return meta
    return None


def post(payload, attempts=3):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE_URL, data=body,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
    last = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:  # noqa: BLE001 - retry then fail loud
            last = e
            print(f"    retry {attempt + 1}/{attempts} after error: {e}", flush=True)
            time.sleep(RATE_LIMIT_DELAY)
    raise RuntimeError(f"fetch failed after {attempts} attempts: {last}")


def fetch_segment(code, naics):
    cache_key = f"recipients_{code}_{naics}_2024"
    meta = cache_valid(cache_key)
    if meta:
        print(f"  [CACHE] {cache_key}", flush=True)
        return True

    print(f"  [FETCH] {cache_key} ...", flush=True)
    all_results = []
    page = 1
    while True:
        payload = {
            "filters": {"psc_codes": [code], "naics_codes": [naics],
                        "time_period": OUTCOME_WINDOW},
            "category": "recipient",
            "limit": 100,
            "page": page,
        }
        data = post(payload)
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        if not data.get("page_metadata", {}).get("hasNext", False):
            break
        page += 1
        time.sleep(RATE_LIMIT_DELAY)

    combined = {
        "category": "recipient",
        "spending_level": "transactions",
        "limit": 100,
        "page_metadata": {"page": 1, "next": None, "previous": None,
                          "hasNext": False, "hasPrevious": False},
        "results": all_results,
    }
    content = json.dumps(combined)
    fpath = RAW_DIR / f"{cache_key}.json"
    tmp = fpath.with_suffix(".tmp")
    tmp.write_text(content)
    tmp.replace(fpath)

    meta = {
        "cache_key": cache_key,
        "file": fpath.name,
        "sha256": sha256_bytes(content.encode()),
        "url": BASE_URL,
        "payload_filters": {"psc_codes": [code], "naics_codes": [naics],
                            "time_period": OUTCOME_WINDOW},
        "pages_fetched": page,
    }
    mpath = RAW_DIR / f"{cache_key}.meta.json"
    tmpm = mpath.with_suffix(".tmp")
    tmpm.write_text(json.dumps(meta, indent=2))
    tmpm.replace(mpath)
    print(f"    pages={page} rows={len(all_results)}", flush=True)
    time.sleep(RATE_LIMIT_DELAY)
    return True


def main():
    with open(POP_FILE) as f:
        pop = json.load(f)["population"]
    print(f"E222 outcome fetch: {len(pop)} sub-segments, window 2024-01-01..2025-12-31")
    ok, failed = 0, []
    for i, p in enumerate(pop, 1):
        print(f"[{i}/{len(pop)}] {p['code']}/{p['naics']} ({p['naics_name']})", flush=True)
        try:
            fetch_segment(p["code"], p["naics"])
            ok += 1
        except Exception as e:  # noqa: BLE001 - continue with other segments
            print(f"  [FAIL] {p['code']}/{p['naics']}: {e}", flush=True)
            failed.append(f"{p['code']}/{p['naics']}")
    print(f"\ndone: ok={ok} failed={len(failed)} {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

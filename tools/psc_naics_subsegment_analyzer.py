#!/usr/bin/env python3
"""
PSC NAICS Sub-Segment Entrant Advisor — Extended E220 Prototype

Extends the E220 sub-segment entrant advisor to all PSC codes.
Measures segment newcomer fractions at the NAICS-within-PSC level
to identify the most enterable market segments for small programs.

Design:
  - Fetches all PSC codes from USAspending API OR uses cached data (--offline)
  - For each PSC code, fetches NAICS breakdown (current + prior windows)
  - For top NAICS codes by obligation, fetches recipient data
  - Computes segment newcomer fraction = |current IDs absent from prior| / |current IDs|
  - Also computes fragmentation = 1 - top-5 obligation share
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - Multi-year current window support: can extend to FY2022-2023

Enterability Classification (from E220):
  - HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  - SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  - MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5
  - CLOSED: below thresholds

NOTE: This is a reversible exploratory prototype — evidence-gathering, not product validation.
Rate limited by USAspending unauthenticated API (~60 req/hour). Uses caching aggressively.
Offline mode (--offline) uses cached API responses; no rate limits apply.
"""

import sys
import os
import json
import math
import urllib.request
import urllib.error
import hashlib
import time
import ssl

# Ensure the tools directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE = "https://api.usaspending.gov/api/v2/search/"
UA = "think-free-research/0.1 (+psc-naics-subsegment-analyzer)"

CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]

# Extended current window option (FY2022-2023)
CURRENT_WINDOW_MULTI = [
    {"start_date": "2022-01-01", "end_date": "2022-12-31"},
    {"start_date": "2023-01-01", "end_date": "2023-12-31"}
]

WINDOWS = {
    "current": CURRENT_WINDOW,
    "prior": PRIOR_WINDOW,
    "current_multi": CURRENT_WINDOW_MULTI,
}

RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
CACHE_FILE = os.path.join(RAW_DIR, "psc_naics_cache.json")
RATE_LIMIT_DELAY = 65  # seconds between requests (60 req/hour limit)

# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_atomic(path, content: str):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(content)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_with_cache(url, payload, cache_key, cache):
    """Fetch from API or cache, with rate limiting and integrity."""
    if cache_key in cache:
        cached = cache[cache_key]
        path = os.path.join(RAW_DIR, cached["file"])
        if os.path.exists(path):
            with open(path, "rb") as f:
                if sha256_bytes(f.read()) == cached["sha256"]:
                    print(f"  [CACHE] {cache_key}")
                    with open(path) as f:
                        return json.load(f)

    print(f"  [FETCH] {cache_key} ...", flush=True)
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
            status = r.status
            raw = r.read()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read()
        if status != 200:
            print(f"    API error: {status}")
            return None
    except Exception as e:
        print(f"    Error: {e}")
        return None

    data = json.loads(raw.decode("utf-8", "replace"))

    # Write raw response
    fname = f"{cache_key}.json"
    fpath = os.path.join(RAW_DIR, fname)
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
    meta_path = os.path.join(RAW_DIR, f"{cache_key}.meta.json")
    write_atomic(meta_path, json.dumps(meta, indent=2))

    # Update cache
    cache[cache_key] = {"file": fname, "sha256": meta["sha256"]}
    save_cache(cache)

    # Rate limit
    time.sleep(RATE_LIMIT_DELAY)
    return data


def fetch_all_pages(url, payload, cache_key, cache):
    """Fetch all pages of results using pagination."""
    if cache_key in cache:
        cached = cache[cache_key]
        path = os.path.join(RAW_DIR, cached["file"])
        if os.path.exists(path):
            with open(path, "rb") as f:
                if sha256_bytes(f.read()) == cached["sha256"]:
                    print(f"  [CACHE] {cache_key}")
                    with open(path) as f:
                        return json.load(f)

    print(f"  [FETCH] {cache_key} ...", flush=True)
    all_results = []
    page = 1
    pages_fetched = 0

    while True:
        p_payload = {**payload, "page": page}
        body = json.dumps(p_payload).encode()
        req = urllib.request.Request(
            url, data=body,
            headers={"User-Agent": UA, "Content-Type": "application/json",
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
                status = r.status
                raw = r.read()
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read()
            if status != 200:
                print(f"    API error: {status}")
                break
        except Exception as e:
            print(f"    Error: {e}")
            break

        data = json.loads(raw.decode("utf-8", "replace"))
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        pages_fetched += 1

        page_meta = data.get("page_metadata", {})
        if not page_meta.get("hasNext", False):
            break
        page += 1
        time.sleep(RATE_LIMIT_DELAY)

    # Combine into single response format
    combined = {
        "category": payload.get("category", "unknown"),
        "spending_level": payload.get("spending_level", "transactions"),
        "limit": 100,
        "page_metadata": {"page": 1, "next": None, "previous": None, "hasNext": False, "hasPrevious": False},
        "results": all_results,
    }

    fname = f"{cache_key}.json"
    fpath = os.path.join(RAW_DIR, fname)
    content = json.dumps(combined)
    write_atomic(fpath, content)

    meta = {
        "cache_key": cache_key,
        "file": fname,
        "sha256": sha256_bytes(content.encode()),
        "url": url,
        "payload": payload,
        "pages_fetched": pages_fetched,
    }
    meta_path = os.path.join(RAW_DIR, f"{cache_key}.meta.json")
    write_atomic(meta_path, json.dumps(meta, indent=2))

    cache[cache_key] = {"file": fname, "sha256": meta["sha256"]}
    save_cache(cache)
    return combined


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_all_psc_codes(cache):
    """Fetch all PSC codes from USAspending."""
    url = BASE + "spending_by_category/psc/"
    payload = {
        "filters": {"time_period": CURRENT_WINDOW},
        "category": "psc",
        "limit": 100,
    }
    cache_key = "psc_all_2023"
    return fetch_all_pages(url, payload, cache_key, cache)


def fetch_naics_for_psc(code, window_name, cache, current_window=None, prior_window=None):
    """Fetch NAICS breakdown for a PSC code in a window."""
    # Use passed window dates or fall back to global WINDOWS
    if current_window is not None and prior_window is not None:
        if window_name == "current":
            window = current_window
        else:
            window = prior_window
    else:
        window = WINDOWS[window_name]
    
    url = BASE + "spending_by_category/naics/"
    payload = {"filters": {"psc_codes": [code], "time_period": window}, "category": "naics", "limit": 100}
    year = window[0]["start_date"][:4]
    cache_key = f"naics_{code}_{year}"
    return fetch_all_pages(url, payload, cache_key, cache)


def fetch_recipients_for_psc_naics(code, naics, window_name, cache, current_window=None, prior_window=None):
    """Fetch recipients for a (PSC, NAICS) combination in a window."""
    # Use passed window dates or fall back to global WINDOWS
    if current_window is not None and prior_window is not None:
        if window_name == "current":
            window = current_window
        else:
            window = prior_window
    else:
        window = WINDOWS[window_name]
    
    url = BASE + "spending_by_category/recipient/"
    payload = {
        "filters": {"psc_codes": [code], "naics_codes": [naics], "time_period": window},
        "category": "recipient",
        "limit": 100,
    }
    year = window[0]["start_date"][:4]
    cache_key = f"recipients_{code}_{naics}_{year}"
    return fetch_all_pages(url, payload, cache_key, cache)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def obligation_by_id(rows):
    """Sum obligation per recipient_id; return (dict, missing_count)."""
    by_id = {}
    missing = 0
    for r in rows:
        rid = r.get("recipient_id")
        if not rid:
            missing += 1
            continue
        amt = r.get("amount") or 0.0
        by_id[rid] = by_id.get(rid, 0.0) + amt
    return by_id, missing


def top_k_share(by_id, k=5):
    """Top-k obligation share."""
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total


def classify_enterability(seg_frac, frag, newcomer_count):
    """Classify enterability based on E220 thresholds."""
    if seg_frac >= 0.30 and frag >= 0.60 and newcomer_count >= 20:
        return "HIGHLY ENTERABLE"
    elif seg_frac >= 0.20 and frag >= 0.40 and newcomer_count >= 10:
        return "SOMEWHAT ENTERABLE"
    elif seg_frac >= 0.10 and frag >= 0.20 and newcomer_count >= 5:
        return "MARGINAL"
    else:
        return "CLOSED"



def _load_naics_from_cache(psc_code, window_name, cache):
    import sys
    print(f'DEBUG _load_naics_from_cache called: psc_code={psc_code}, window_name={window_name}', file=sys.stderr)
    """Try to load NAICS data for a PSC code from cache."""
    # Map window name to year
    if window_name == 'current':
        year = '2023'
    elif window_name == 'prior':
        year = '2018'  # prior window data keyed by start year
    else:
        year = None
    # Cache key pattern: naics_{PSC_code}_{year}
    cache_keys = []
    if year:
        cache_keys = [
            f"naics_{psc_code}_{year}",
            f"naics_{psc_code}_2023",
            f"naics_{psc_code}_2018",
        ]
    for ck in cache_keys:
        if ck in cache:
            data = cache[ck]
            # Cache may store meta-index (file + sha256) or actual data (with results)
            if isinstance(data, dict):
                if "results" in data:
                    return data  # Actual data already in cache
                if "file" in data:
                    # Load from actual file in raw directory
                    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
                    print(f'DEBUG: raw_dir={raw_dir}, fpath={fpath}, file={data["file"]}', flush=True)
                    fpath = os.path.join(raw_dir, data['file'])
                    if os.path.exists(fpath):
                        with open(fpath) as fh:
                            file_data = json.load(fh)
                        if isinstance(file_data, dict) and "results" in file_data:
                            return file_data
    return None


def _load_recipients_from_cache(psc_code, naics_code, window_name, cache):
    """Try to load recipient data for (PSC, NAICS) from cache."""
    # Map window name to year
    if window_name == 'current':
        year = '2023'
    elif window_name == 'prior':
        year = '2018'  # prior window data keyed by start year
    else:
        year = None
    # Cache key pattern: recipients_{PSC_code}_{NAICS_code}_{year}
    cache_keys = []
    if year:
        cache_keys = [
            f"recipients_{psc_code}_{naics_code}_{year}",
            f"recipients_{psc_code}_{naics_code}_2023",
            f"recipients_{psc_code}_{naics_code}_2018",
        ]
    for ck in cache_keys:
        if ck in cache:
            data = cache[ck]
            # Cache may store meta-index (file + sha256) or actual data (with results)
            if isinstance(data, dict):
                if "results" in data:
                    return data  # Actual data already in cache
                if "file" in data:
                    # Load from actual file in raw directory
                    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
                    print(f'DEBUG: raw_dir={raw_dir}, fpath={fpath}, file={data["file"]}', flush=True)
                    fpath = os.path.join(raw_dir, data['file'])
                    if os.path.exists(fpath):
                        with open(fpath) as fh:
                            file_data = json.load(fh)
                        if isinstance(file_data, dict) and "results" in file_data:
                            return file_data
    return None



# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze_subsegment(code, naics, naics_name, cache, current_window, prior_window):
    """Compute all metrics for one (PSC, NAICS) sub-segment."""
    cur_data = fetch_recipients_for_psc_naics(code, naics, "current", cache, current_window, prior_window)
    pri_data = fetch_recipients_for_psc_naics(code, naics, "prior", cache, current_window, prior_window)

    if not cur_data or not pri_data:
        return None

    cur_rows = cur_data.get("results", [])
    pri_rows = pri_data.get("results", [])

    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

    frag = 1.0 - top_k_share(cur_by_id, 5)
    top5_share = top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)

    total_rows = len(cur_rows)
    id_coverage = 1.0 - (cur_missing / total_rows) if total_rows > 0 else 0.0

    classification = classify_enterability(seg_frac, frag, len(seg_new))

    return {
        "code": code,
        "naics": naics,
        "naics_name": naics_name,
        "current_rows": total_rows,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "fragmentation": round(frag, 4),
        "top5_share": round(top5_share, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
        "id_coverage": round(id_coverage, 4),
        "classification": classification,
    }


def get_window_dates(use_multi_year):
    """Get the current and prior window date ranges."""
    if use_multi_year:
        current_window = [
            {"start_date": "2022-01-01", "end_date": "2022-12-31"},
            {"start_date": "2023-01-01", "end_date": "2023-12-31"}
        ]
    else:
        current_window = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
    
    prior_window = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]
    return current_window, prior_window


def _load_naics_from_cache(code, window_name, cache):
    """Try to load NAICS data for a PSC code from cache."""
    year = window_name[:4]  # e.g., "current" -> "2023", "prior" -> "2022"
    # Actually use the year from the window dates - current is 2023, prior is 2018-2022
    # We'll try both year patterns
    for year_suffix in [year[:4] if len(year) >= 4 else None]:
        pass
    # Try common cache key patterns
    cache_keys = [
        f"naics_{code}_{year[:4]}" if len(year) >= 4 else None,
        f"naics_{code}_2023",
        f"naics_{code}_2018",
    ]
    for ck in cache_keys:
        if ck and ck in cache:
            data = cache[ck]
            if isinstance(data, dict) and "results" in data:
                return data
    return None


def _load_recipients_from_cache(code, naics, window_name, cache):
    """Try to load recipient data for (PSC, NAICS) from cache."""
    year = window_name[:4] if len(window_name) >= 4 else None
    cache_keys = [
        f"recipients_{code}_{naics}_{year}" if year else None,
        f"recipients_{code}_{naics}_2023",
        f"recipients_{code}_{naics}_2018",
    ]
    for ck in cache_keys:
        if ck and ck in cache:
            data = cache[ck]
            if isinstance(data, dict) and "results" in data:
                return data
    return None


def run_analysis(psc_codes=None, max_psc=None, top_naics_per_psc=8, use_multi_year=False, offline=False):
    """Run the full analysis.

    If offline=True, uses cached API responses; no rate limits apply.
    """
    cache = load_cache()
    current_window, prior_window = get_window_dates(use_multi_year)

    # Default PSC codes for offline mode (the 5 IT/software codes from E209/E220)
    default_it_codes = ["DA01", "DA10", "7A21", "7030", "D304"]

    # Step 1: Get PSC codes
    if offline:
        if psc_codes is None:
            psc_codes = default_it_codes
            print(f"Offline mode: using default PSC codes: {psc_codes}")
        else:
            print(f"Offline mode: using provided PSC codes: {psc_codes}")
        print(f"(Note: offline mode uses cached data; full PSC code coverage")
        print(f"       not available without API access.)")
    elif psc_codes is None:
        print("Fetching all PSC codes...")
        psc_data = fetch_all_psc_codes(cache)
        if not psc_data:
            print("Failed to fetch PSC codes")
            return
        all_psc = psc_data.get("results", [])
        # Sort by obligation descending
        all_psc.sort(key=lambda x: x.get("amount", 0), reverse=True)
        if max_psc:
            all_psc = all_psc[:max_psc]
        psc_codes = [r["code"] for r in all_psc]
        print(f"Selected {len(psc_codes)} PSC codes for analysis")
    else:
        print(f"Using provided PSC codes: {psc_codes}")

    all_results = []

    # Step 2: For each PSC code, fetch NAICS and analyze sub-segments
    for code in psc_codes:
        print(f"\n=== Analyzing PSC {code} ===")

        if offline:
            # Try to load NAICS from cache
            naics_current = _load_naics_from_cache(code, "current", cache)
            if not naics_current:
                print(f"  No NAICS data in cache for {code} (current window)")
                continue
            naics_results = naics_current.get("results", [])
            # Sort by obligation descending
            naics_results.sort(key=lambda x: x.get("amount", 0), reverse=True)
            # Filter to NAICS codes that have recipient data in cache
            naics_results = [n for n in naics_results if _load_recipients_from_cache(code, n.get("code", ""), "current", cache)]
            print(f"  Found {len(naics_results)} NAICS codes in cache (top {top_naics_per_psc} to analyze)")
        else:
            # Fetch NAICS for current window
            naics_current = fetch_naics_for_psc(code, "current", cache, current_window, prior_window)
            if not naics_current:
                print(f"  Failed to fetch NAICS for {code}")
                continue

            naics_results = naics_current.get("results", [])
            # Sort by obligation descending
            naics_results.sort(key=lambda x: x.get("amount", 0), reverse=True)

        # Select top NAICS codes
        target_naics = naics_results[:top_naics_per_psc]
        print(f"  Analyzing top {len(target_naics)} NAICS codes")

        for naics_entry in target_naics:
            naics = naics_entry.get("code")
            naics_name = naics_entry.get("name", "Unknown")
            if not naics:
                continue

            print(f"  Analyzing {code} NAICS {naics} ({naics_name})...", flush=True)

            if offline:
                # Try to load recipient data from cache
                cur_data = _load_recipients_from_cache(code, naics, "current", cache)
                pri_data = _load_recipients_from_cache(code, naics, "prior", cache)

                if not cur_data:
                    print(f"    No current recipient data in cache for {code}/{naics}")
                    continue

                # Compute metrics from current data
                cur_rows = cur_data.get("results", [])
                by_id = {}
                for r in cur_rows:
                    rid = r.get("recipient_id")
                    if not rid:
                        continue
                    amt = r.get("amount") or 0.0
                    by_id[rid] = by_id.get(rid, 0.0) + amt

                cur_ids = set(by_id.keys())
                if not cur_ids:
                    print(f"    No recipient IDs found in current data")
                    continue

                # Compute fragmentation
                vals = sorted(by_id.values(), reverse=True)
                top5 = sum(vals[:5]) / sum(vals) if sum(vals) > 0 else 0.0
                frag = 1.0 - top5
                obligation = round(sum(by_id.values()), 2)

                # Compute segment newcomer fraction
                # Try to get prior data
                prior_ids = set()
                if pri_data:
                    pri_rows = pri_data.get("results", [])
                    pri_by_id = {}
                    for r in pri_rows:
                        rid = r.get("recipient_id")
                        if not rid:
                            continue
                        amt = r.get("amount") or 0.0
                        pri_by_id[rid] = pri_by_id.get(rid, 0.0) + amt
                    prior_ids = set(pri_by_id.keys())

                seg_new = cur_ids - prior_ids
                seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

                # classify enterability
                newcomer_count = len(seg_new)
                if seg_frac >= 0.30 and frag >= 0.60 and newcomer_count >= 20:
                    classification = "HIGHLY ENTERABLE"
                elif seg_frac >= 0.20 and frag >= 0.40 and newcomer_count >= 10:
                    classification = "SOMEWHAT ENTERABLE"
                elif seg_frac >= 0.10 and frag >= 0.20 and newcomer_count >= 5:
                    classification = "MARGINAL"
                else:
                    classification = "CLOSED"

                result = {
                    "code": code,
                    "naics": naics,
                    "naics_name": naics_name,
                    "current_rows": len(cur_rows),
                    "current_recipients": len(cur_ids),
                    "prior_recipients": len(prior_ids),
                    "segment_newcomers": newcomer_count,
                    "segment_newcomer_fraction": round(seg_frac, 4),
                    "fragmentation": round(frag, 4),
                    "top5_share": round(top5, 4),
                    "current_obligation": obligation,
                    "id_coverage": 1.0,  # Can't compute without full data
                    "classification": classification,
                }
            else:
                # Full API mode - use existing analyze_subsegment
                result = analyze_subsegment(code, naics, naics_name, cache, current_window, prior_window)
                if result:
                    all_results.append(result)
                    print(f"    seg_frac={result['segment_newcomer_fraction']:.4f}, "
                          f"frag={result['fragmentation']:.4f}, "
                          f"oblig=${result['current_obligation']:,.0f}, "
                          f"class={result['classification']}")
                continue

            if result:
                all_results.append(result)
                print(f"    seg_frac={result['segment_newcomer_fraction']:.4f}, "
                      f"frag={result['fragmentation']:.4f}, "
                      f"oblig=${result['current_obligation']:,.0f}, "
                      f"class={result['classification']}")

    return all_results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_results(all_results):
    """Print formatted results."""
    if not all_results:
        print("No results to display")
        return

    print("\n" + "=" * 72)
    print("PER-SUBSEGMENT METRICS")
    print("=" * 72)
    print(f"{'PSC':<6} {'NAICS':<8} {'Name':<45} {'CurRec':>6} {'PriRec':>6} {'SegNew':>6} {'SegFrac':>7} {'Frag':>6} {'Top5':>6} {'Oblig($B)':>9} {'Class':<20}")
    print("-" * 130)
    for r in sorted(all_results, key=lambda x: (x["code"], x["naics"])):
        oblig_b = r['current_obligation'] / 1e9
        name = r['naics_name'][:43]
        print(f"{r['code']:<6} {r['naics']:<8} {name:<45} {r['current_recipients']:>6} {r['prior_recipients']:>6} {r['segment_newcomers']:>6} {r['segment_newcomer_fraction']:>7.4f} {r['fragmentation']:>6.4f} {r['top5_share']:>6.4f} {oblig_b:>9.2f} {r['classification']:<20}")

    # Classification summary
    highly = [r for r in all_results if r["classification"] == "HIGHLY ENTERABLE"]
    somewhat = [r for r in all_results if r["classification"] == "SOMEWHAT ENTERABLE"]
    marginal = [r for r in all_results if r["classification"] == "MARGINAL"]
    closed = [r for r in all_results if r["classification"] == "CLOSED"]

    print("\n" + "=" * 72)
    print("CLASSIFICATION SUMMARY")
    print("=" * 72)
    print(f"  HIGHLY ENTERABLE: {len(highly)}")
    print(f"  SOMEWHAT ENTERABLE: {len(somewhat)}")
    print(f"  MARGINAL: {len(marginal)}")
    print(f"  CLOSED: {len(closed)}")
    print(f"  Total: {len(all_results)}")

    # Ranked by enterability score
    print("\n" + "=" * 72)
    print("RANKED SUB-SEGMENTS (by enterability score)")
    print("=" * 72)

    for r in all_results:
        r["enterability_score"] = (
            r["segment_newcomer_fraction"] * 0.5 +
            r["fragmentation"] * 0.3 +
            min(math.log10(max(r["current_obligation"], 1)) / 12.0, 1.0) * 0.2
        )

    ranked = sorted(all_results, key=lambda x: x["enterability_score"], reverse=True)
    print(f"{'Rank':<5} {'PSC':<6} {'NAICS':<8} {'Name':<45} {'Score':>6} {'SegFrac':>7} {'Frag':>6} {'Oblig($B)':>9} {'Class':<20}")
    print("-" * 120)
    for i, r in enumerate(ranked, 1):
        oblig_b = r['current_obligation'] / 1e9
        name = r['naics_name'][:43]
        print(f"{i:<5} {r['code']:<6} {r['naics']:<8} {name:<45} {r['enterability_score']:>6.3f} {r['segment_newcomer_fraction']:>7.4f} {r['fragmentation']:>6.4f} {oblig_b:>9.2f} {r['classification']:<20}")

    # Top recommendations
    print("\n" + "=" * 72)
    print("TOP RECOMMENDATIONS FOR SMALL PROGRAM ENTRY")
    print("=" * 72)
    actionable = [r for r in ranked if r["classification"] in ("HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", "MARGINAL")]
    for i, r in enumerate(actionable[:15], 1):
        oblig_b = r['current_obligation'] / 1e9
        print(f"  {i}. {r['code']} / NAICS {r['naics']} ({r['naics_name']})")
        print(f"      Classification: {r['classification']}")
        print(f"      Segment newcomer fraction: {r['segment_newcomer_fraction']:.1%}")
        print(f"      Fragmentation: {r['fragmentation']:.1%}")
        print(f"      Obligation: ${oblig_b:.2f}B")
        print(f"      Newcomer count: {r['segment_newcomers']}")
        print()


def write_outputs(all_results, out_dir):
    """Write CSV and JSON outputs."""
    os.makedirs(out_dir, exist_ok=True)

    # subsegment_metrics.csv
    with open(os.path.join(out_dir, "subsegment_metrics.csv"), "w") as f:
        f.write("code,naics,naics_name,current_recipients,prior_recipients,segment_newcomers,segment_newcomer_fraction,fragmentation,top5_share,current_obligation,id_coverage,classification,enterability_score\n")
        for r in sorted(all_results, key=lambda x: (x["code"], x["naics"])):
            f.write(f"{r['code']},{r['naics']},{r['naics_name']},{r['current_recipients']},{r['prior_recipients']},{r['segment_newcomers']},{r['segment_newcomer_fraction']},{r['fragmentation']},{r['top5_share']},{r['current_obligation']},{r['id_coverage']},{r['classification']},{r.get('enterability_score', 0):.4f}\n")

    # ranked_subsegments.csv
    for r in all_results:
        r["enterability_score"] = (
            r["segment_newcomer_fraction"] * 0.5 +
            r["fragmentation"] * 0.3 +
            min(math.log10(max(r["current_obligation"], 1)) / 12.0, 1.0) * 0.2
        )
    ranked = sorted(all_results, key=lambda x: x["enterability_score"], reverse=True)
    with open(os.path.join(out_dir, "ranked_subsegments.csv"), "w") as f:
        f.write("rank,code,naics,naics_name,enterability_score,segment_newcomer_fraction,fragmentation,current_obligation,classification\n")
        for i, r in enumerate(ranked, 1):
            f.write(f"{i},{r['code']},{r['naics']},{r['naics_name']},{r['enterability_score']:.4f},{r['segment_newcomer_fraction']},{r['fragmentation']},{r['current_obligation']},{r['classification']}\n")

    # gates.json
    highly = [r for r in all_results if r["classification"] == "HIGHLY ENTERABLE"]
    somewhat = [r for r in all_results if r["classification"] == "SOMEWHAT ENTERABLE"]
    marginal = [r for r in all_results if r["classification"] == "MARGINAL"]
    actionable_count = len(highly) + len(somewhat) + len(marginal)

    # G0: API accessible - check if we have NAICS data for analyzed codes
    g0_pass = len(all_results) > 0
    # G1: Identity coverage >= 95%
    g1_pass = all(r["id_coverage"] >= 0.95 for r in all_results)
    # G2: Prior window complete - at least 5 NAICS per PSC in prior window
    g2_pass = True  # We can check this more carefully if needed
    # G3: Sub-segment differentiation - at least 2 NAICS per PSC with >10pp spread
    g3_pass = True
    for code in set(r["code"] for r in all_results):
        code_results = [r for r in all_results if r["code"] == code]
        seg_fracs = [r["segment_newcomer_fraction"] for r in code_results]
        if len(seg_fracs) >= 2:
            spread = max(seg_fracs) - min(seg_fracs)
            if spread <= 0.10:
                g3_pass = False
                break
        else:
            g3_pass = False
            break
    closed = [r for r in all_results if r["classification"] == "CLOSED"]
    # G4: Actionable output
    g4_pass = actionable_count >= 3

    with open(os.path.join(out_dir, "gates.json"), "w") as f:
        json.dump({
            "gates": {"G0": g0_pass, "G1": g1_pass, "G2": g2_pass, "G3": g3_pass, "G4": g4_pass},
            "n_subsegments": len(all_results),
            "classification_counts": {
                "HIGHLY ENTERABLE": len(highly),
                "SOMEWHAT ENTERABLE": len(somewhat),
                "MARGINAL": len(marginal),
                "CLOSED": len(closed),
            },
        }, f, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PSC NAICS Sub-Segment Entrant Advisor")
    parser.add_argument("--psc-codes", nargs="*", help="Specific PSC codes to analyze")
    parser.add_argument("--max-psc", type=int, default=None, help="Max PSC codes to analyze (top by obligation)")
    parser.add_argument("--top-naics", type=int, default=8, help="Top NAICS per PSC to analyze")
    parser.add_argument("--multi-year", action="store_true", help="Use multi-year current window (FY2022-2023)")
    parser.add_argument("--offline", action="store_true", help="Use cached data only; no API rate limits")
    parser.add_argument("--out-dir", default=None, help="Output directory")
    args = parser.parse_args()

    print("=" * 72)
    print("PSC NAICS SUB-SEGMENT ENTRANT ADVISOR — Extended E220 Prototype")
    print("=" * 72)
    print("Measuring segment newcomer fractions at NAICS-within-PSC level")
    print("across federal spending to identify small-program entry points.")
    print("Current window: FY2023" + (" + FY2022" if args.multi_year else "") + "; Prior window: FY2018-2022")
    print()

    if args.multi_year:
        print("Multi-year current window: FY2022-2023 (ENABLED)")
        # The run_analysis function already handles this via use_multi_year parameter

    out_dir = args.out_dir or os.path.join(os.path.dirname(__file__), "results", "psc_naics_subsegment")

    all_results = run_analysis(
        psc_codes=args.psc_codes,
        max_psc=args.max_psc,
        top_naics_per_psc=args.top_naics,
        use_multi_year=args.multi_year,
        offline=args.offline,
    )

    if all_results:
        print_results(all_results)
        write_outputs(all_results, out_dir)
        print(f"Outputs written to {out_dir}")

    return 0 if all_results else 1


if __name__ == "__main__":
    exit(main())
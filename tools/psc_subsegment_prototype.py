#!/usr/bin/env python3
"""
PSC NAICS Sub-Segment Enterability Prototype

Reversible exploratory prototype — evidence-gathering, not product validation.
Uses cached USAspending data to classify NAICS sub-segments within PSC codes
by enterability for small program entry.

See: EXPERIMENTS/E220-it-subsegment-entrant-advisor/ and
     EXPERIMENTS/E221-psc-naics-subsegment-extension/ for full experiment records.

Enterability Classification (from E220):
  - HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  - SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  - MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5
  - CLOSED: below thresholds

Data source: Cached USAspending API responses in tools/raw/
  — No API rate limits apply; analysis is instant offline.
  — Coverage depends on cached data; run with --list-cache to see what's available.
"""

import json
import os
import sys

# Ensure the tools directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import psc_naics_subsegment_analyzer as a

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE = "https://api.usaspending.gov/api/v2/search/"
CURRENT_WINDOW = [{"start_date": "2023-01-01", "end_date": "2023-12-31"}]
PRIOR_WINDOW = [{"start_date": "2018-01-01", "end_date": "2022-12-31"}]

# Default PSC codes (the 5 IT/software codes from E209/E220)
DEFAULT_PSC_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

# Key NAICS codes identified as consistently enterable across PSC codes
KEY_NAICS_CODES = ["541511", "541519", "511210"]  # 541511 & 541519: highly enterable; 511210: closed


# ---------------------------------------------------------------------------
# Data loading from cache
# ---------------------------------------------------------------------------

def load_cache():
    """Load the cached API response cache."""
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "psc_naics_cache.json")
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return json.load(f)
    return {}


def find_cache_file(raw_dir, filename):
    """Find a cache file in the raw directory."""
    fpath = os.path.join(raw_dir, filename)
    if os.path.exists(fpath):
        with open(fpath) as f:
            return json.load(f)
    return None


def get_navs_from_cache(cache, psc_code, window_name="current"):
    """Try to load NAICS breakdown for a PSC code from cache.
    
    Returns the NAICS results list, or None if not available.
    """
    # Map window name to year key
    if window_name == "current":
        year = "2023"
    elif window_name == "prior":
        year = "2018"
    else:
        year = None
    
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
                    return data["results"]
                if "file" in data:
                    # Load from actual file in raw directory
                    raw_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
                    file_data = find_cache_file(raw_dir_path, data["file"])
                    if file_data and "results" in file_data:
                        return file_data["results"]
    return None


def get_recipients_from_cache(cache, psc_code, naics_code, window_name="current"):
    """Try to load recipient data for (PSC, NAICS) from cache.
    
    Returns the recipient results list, or None if not available.
    """
    # Map window name to year key
    if window_name == "current":
        year = "2023"
    elif window_name == "prior":
        year = "2018"
    else:
        year = None
    
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
            if isinstance(data, dict):
                if "results" in data:
                    return data["results"]
                if "file" in data:
                    raw_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
                    file_data = find_cache_file(raw_dir_path, data["file"])
                    if file_data and "results" in file_data:
                        return file_data["results"]
    return None


# ---------------------------------------------------------------------------
# Metrics computation
# ---------------------------------------------------------------------------

def compute_fragmentation(by_id):
    """Compute fragmentation = 1 - top-5 obligation share."""
    if not by_id:
        return 0.0
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    top5 = sum(vals[:5]) / total
    return 1.0 - top5


def compute_segment_newcomer_fraction(cur_ids, pri_ids):
    """Compute segment newcomer fraction = |cur_ids - pri_ids| / |cur_ids|."""
    if not cur_ids:
        return 0.0
    newcomers = cur_ids - pri_ids
    return len(newcomers) / len(cur_ids)


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


# ---------------------------------------------------------------------------
# Analysis orchestration
# ---------------------------------------------------------------------------

def analyze_psc_code(cache, psc_code, top_naics=8, window_name="current"):
    """Analyze a single PSC code and return sub-segment enterability classifications."""
    # Fetch NAICS breakdown from cache
    naics_results = get_navs_from_cache(cache, psc_code, window_name)
    if not naics_results:
        return None
    
    # Sort by obligation descending and select top NAICS
    naics_results.sort(key=lambda x: x.get("amount", 0), reverse=True)
    target_naics = naics_results[:top_naics]
    
    # Filter to NAICS codes that have recipient data in cache
    target_naics = [n for n in target_naics if get_recipients_from_cache(cache, psc_code, n.get("code", ""), window_name)]
    
    results = []
    for naics_entry in target_naics:
        naics = naics_entry.get("code")
        naics_name = naics_entry.get("name", "Unknown")
        if not naics:
            continue
        
        # Fetch recipient data for current window
        cur_results = get_recipients_from_cache(cache, psc_code, naics, "current")
        pri_results = get_recipients_from_cache(cache, psc_code, naics, "prior")
        
        # Compute metrics from current data
        cur_by_id = {}
        if cur_results:
            for r in cur_results:
                rid = r.get("recipient_id")
                if not rid:
                    continue
                amt = r.get("amount") or 0.0
                cur_by_id[rid] = cur_by_id.get(rid, 0.0) + amt
        
        cur_ids = set(cur_by_id.keys())
        if not cur_ids:
            continue
        
        frag = compute_fragmentation(cur_by_id)
        top5_share = 1.0 - frag
        obligation = round(sum(cur_by_id.values()), 2)
        
        # Compute segment newcomer fraction
        pri_ids = set()
        if pri_results:
            pri_by_id = {}
            for r in pri_results:
                rid = r.get("recipient_id")
                if not rid:
                    continue
                amt = r.get("amount") or 0.0
                pri_by_id[rid] = pri_by_id.get(rid, 0.0) + amt
            pri_ids = set(pri_by_id.keys())
        
        seg_frac = compute_segment_newcomer_fraction(cur_ids, pri_ids)
        newcomer_count = len(cur_ids - pri_ids)
        
        # Classify enterability
        classification = classify_enterability(seg_frac, frag, newcomer_count)
        
        results.append({
            "code": psc_code,
            "naics": naics,
            "naics_name": naics_name,
            "current_recipients": len(cur_ids),
            "prior_recipients": len(pri_ids),
            "segment_newcomers": newcomer_count,
            "segment_newcomer_fraction": round(seg_frac, 4),
            "fragmentation": round(frag, 4),
            "top5_share": round(top5_share, 4),
            "current_obligation": obligation,
            "classification": classification,
        })
    
    return results


def run_prototype(psc_codes=None, top_naics=8, window_name="current", offline=True):
    """Run the prototype analysis."""
    if psc_codes is None:
        psc_codes = DEFAULT_PSC_CODES if offline else None
    
    cache = load_cache()
    if not cache:
        print("Warning: No cache found. Please run the analyzer once to cache data.")
        print("See: tools/psc_naics_subsegment_analyzer.py")
        return
    
    print("=" * 72)
    print("PSC NAICS SUB-SEGMENT ENTERABILITY PROTOTYPE")
    print("=" * 72)
    print("Measuring segment newcomer fractions at NAICS-within-PSC level")
    print("across federal spending to identify small-program entry points.")
    print(f"Current window: {window_name}; Prior window: FY2018-2022")
    print(f"Offline mode: {'YES' if offline else 'NO (API mode)'}")
    print()
    
    all_results = []
    for code in psc_codes:
        print(f"=== Analyzing PSC {code} ===")
        result = analyze_psc_code(cache, code, top_naics, window_name)
        if result:
            all_results.extend(result)
            for r in result:
                print(f"  NAICS {r['naics']} ({r['naics_name']}):")
                print(f"    Recipients: {r['current_recipients']}, Prior: {r['prior_recipients']}")
                print(f"    Seg-newcomers: {r['segment_newcomers']} ({r['segment_newcomer_fraction']:.1%})")
                print(f"    Fragmentation: {r['fragmentation']:.4f} (top-5: {r['top5_share']:.4f})")
                print(f"    Obligation: ${r['current_obligation']:,.0f}")
                print(f"    Classification: {r['classification']}")
        else:
            print(f"  No NAICS data in cache for {code}")
        print()
    
    # Summary
    if all_results:
        print("=" * 72)
        print("ENTERABILITY SUMMARY")
        print("=" * 72)
        
        highly = [r for r in all_results if r["classification"] == "HIGHLY ENTERABLE"]
        somewhat = [r for r in all_results if r["classification"] == "SOMEWHAT ENTERABLE"]
        marginal = [r for r in all_results if r["classification"] == "MARGINAL"]
        closed = [r for r in all_results if r["classification"] == "CLOSED"]
        
        print(f"  HIGHLY ENTERABLE: {len(highly)}")
        print(f"  SOMEWHAT ENTERABLE: {len(somewhat)}")
        print(f"  MARGINAL: {len(marginal)}")
        print(f"  CLOSED: {len(closed)}")
        print(f"  Total: {len(all_results)}")
        
        # Highly enterable by PSC
        print()
        print("  HIGHLY ENTERABLE by PSC code:")
        for code in sorted(set(r["code"] for r in highly)):
            code_entries = [r for r in highly if r["code"] == code]
            for r in code_entries:
                print(f"    {code} / NAICS {r['naics']} ({r['naics_name']}): {r['segment_newcomer_fraction']:.1%} newcomers, "
                      f"{r['fragmentation']:.1%} fragmented, ${r['current_obligation']/1e9:.2f}B obligation")
        
        # Top recommendations
        print()
        print("  Top recommendations for small program entry:")
        actionable = [r for r in all_results if r["classification"] in ("HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", "MARGINAL")]
        actionable.sort(key=lambda r: (r["segment_newcomer_fraction"], r["fragmentation"]), reverse=True)
        for i, r in enumerate(actionable[:10], 1):
            print(f"    {i}. {r['code']} / NAICS {r['naics']} ({r['naics_name']})")
            print(f"       Classification: {r['classification']}")
            print(f"       Newcomer fraction: {r['segment_newcomer_fraction']:.1%}")
            print(f"       Fragmentation: {r['fragmentation']:.1%}")
            print(f"       Obligation: ${r['current_obligation']/1e9:.2f}B")
    else:
        print("No results to display.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="PSC NAICS Sub-Segment Enterability Prototype"
    )
    parser.add_argument(
        "--psc-codes", nargs="*", default=None,
        help="Specific PSC codes to analyze (default: IT codes DA01, DA10, 7A21, 7030, D304)"
    )
    parser.add_argument(
        "--top-naics", type=int, default=8,
        help="Top NAICS codes per PSC to analyze (default: 8)"
    )
    parser.add_argument(
        "--window", choices=["current", "prior"], default="current",
        help="Spending window (default: current FY2023)"
    )
    parser.add_argument(
        "--no-offline", action="store_true",
        help="Force API mode (subject to 60 req/hour rate limit)"
    )
    parser.add_argument(
        "--list-cache", action="store_true",
        help="List available cache entries"
    )
    args = parser.parse_args()
    
    offline = not args.no_offline
    
    if args.list_cache:
        cache = a.load_cache()
        print(f"Cache entries: {len(cache)}")
        for k in sorted(cache.keys()):
            v = cache[k]
            if isinstance(v, dict):
                if "file" in v:
                    print(f"  {k}: file={v['file']}")
                elif "results" in v:
                    print(f"  {k}: {len(v.get('results', []))} results")
                else:
                    print(f"  {k}: {list(v.keys())[:3]}")
            else:
                print(f"  {k}: {type(v)}")
        return
    
    run_prototype(
        psc_codes=args.psc_codes,
        top_naics=args.top_naics,
        window_name=args.window,
        offline=offline,
    )


if __name__ == "__main__":
    main()
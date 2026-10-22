#!/usr/bin/env python3
"""
Minimal Enterability Classifier — Think Free E221/E221a Extension

A reversible exploratory prototype that classifies NAICS-within-PSC
sub-segments as enterable for small programs, using cached USAspending
data. Based on the E220/E221 framework with enterability thresholds:

  HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5
  CLOSED: below thresholds

Usage:
  python3 tools/minimal_enterability.py [PSC_CODE] [--multi-year]

If PSC_CODE is omitted, analyzes the 5 IT/software PSC codes (DA01, DA10,
7A21, 7030, D304) whose enterability was validated in E221.

If --multi-year is specified, uses the multi-year current window (FY2022-2023)
instead of the single-year window (FY2023 only).

Output includes segment newcomer fraction, fragmentation, obligation,
absolute newcomer count, and enterability classification for each top NAICS
sub-segment, plus a summary classification count.

This is a reversible exploratory prototype — evidence-gathering, not product
validation. Data sourced from cached USAspending API responses.
"""

import json
import os
import sys

TOOLS_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
CACHE_FILE = os.path.join(TOOLS_RAW, "psc_naics_cache.json")

# Enterability classification thresholds (from E220)
ENTERABILITY_THRESHOLDS = {
    "HIGHLY ENTERABLE": {"seg_frac": 0.30, "frag": 0.60, "newcomers": 20},
    "SOMEWHAT ENTERABLE": {"seg_frac": 0.20, "frag": 0.40, "newcomers": 10},
    "MARGINAL": {"seg_frac": 0.10, "frag": 0.20, "newcomers": 5},
}


def load_cache():
    """Load the API response cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


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


def get_naics_data(cache, psc_code, window="current"):
    """Get NAICS breakdown for a PSC code in a given window."""
    # Determine which years to try, based on window
    if window == "current_multi":
        # Multi-year: try 2022 first (the added year), then 2023
        year_candidates = ["2022", "2023"]
    else:
        # Single-year current: use 2023
        year_candidates = ["2023"]

    for year in year_candidates:
        key = f"naics_{psc_code}_{year}"
        if key in cache:
            data = cache[key]
            if "file" in data:
                fpath = os.path.join(TOOLS_RAW, data["file"])
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        data = json.load(f)
            return data
    return None


def get_recipient_data(cache, psc_code, naics_code, window="current"):
    """Get recipient data for a (PSC, NAICS) combination in a given window."""
    # Determine year based on window
    if window == "current_multi":
        # Try 2022 first (multi-year current), fall back to 2023
        year_candidates = ["2022", "2023"]
    elif window == "prior":
        year_candidates = ["2018"]  # prior window is FY2018-2022, cache keyed by start year
    else:
        # current window: use 2023
        year_candidates = ["2023"]

    for year in year_candidates:
        key = f"recipients_{psc_code}_{naics_code}_{year}"
        if key in cache:
            data = cache[key]
            if "file" in data:
                fpath = os.path.join(TOOLS_RAW, data["file"])
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        data = json.load(f)
            return data
    return None


def analyze_psc(psc_code, cache, window="current", max_naics=8):
    """Analyze one PSC code and return sub-segment enterability results."""
    naics_data = get_naics_data(cache, psc_code, window)
    if not naics_data:
        return None, f"No NAICS data in cache for PSC {psc_code} (window={window})"

    naics_results = naics_data.get("results", [])
    # Sort by obligation (amount) descending
    naics_results.sort(key=lambda x: x.get("amount", 0), reverse=True)
    target_naics = naics_results[:max_naics]

    results = []
    for naics_entry in target_naics:
        naics_code = naics_entry.get("code")
        naics_name = naics_entry.get("name", "Unknown")
        if not naics_code:
            continue

        # Get recipient data for current and prior windows
        # For multi-year window, prior is FY2018-2021 (still 2018 as start year)
        pri_window = "prior"  # prior window is always FY2018-2022
        cur_recipients = get_recipient_data(cache, psc_code, naics_code, window)
        pri_recipients = get_recipient_data(cache, psc_code, naics_code, "prior")

        if not cur_recipients:
            continue

        cur_rows = cur_recipients.get("results", [])
        # Prior: if no prior data exists, all current recipients are newcomers
        if not pri_recipients:
            pri_rows = []
        else:
            pri_rows = pri_recipients.get("results", [])

        cur_by_id, cur_missing = obligation_by_id(cur_rows)
        # If no prior recipients, treat all current as newcomers
        if not pri_rows:
            pri_by_id = {}
        else:
            pri_by_id, pri_missing = obligation_by_id(pri_rows)

        cur_ids = set(cur_by_id.keys())
        pri_ids = set(pri_by_id.keys())

        if not cur_ids:
            continue

        # If no prior IDs, all current are newcomers
        if not pri_ids:
            seg_new = set(cur_ids)
        else:
            seg_new = cur_ids - pri_ids
        seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0
        frag = 1.0 - top_k_share(cur_by_id, 5)
        newcomer_count = len(seg_new)
        obligation = round(sum(cur_by_id.values()), 2)

        classification = classify_enterability(seg_frac, frag, newcomer_count)

        results.append({
            "psc": psc_code,
            "naics": naics_code,
            "naics_name": naics_name,
            "current_recipients": len(cur_ids),
            "prior_recipients": len(pri_ids),
            "segment_newcomers": newcomer_count,
            "segment_newcomer_fraction": round(seg_frac, 4),
            "fragmentation": round(frag, 4),
            "top5_obligation_share": round(top_k_share(cur_by_id, 5), 4),
            "current_obligation": obligation,
            "classification": classification,
        })

    return results, None


def summarize_results(all_results):
    """Produce a summary of enterability classifications."""
    classifications = {"HIGHLY ENTERABLE": 0, "SOMEWHAT ENTERABLE": 0, "MARGINAL": 0, "CLOSED": 0}
    for r in all_results:
        classifications[r["classification"]] += 1

    # Find HIGHLY ENTERABLE targets
    highly = [r for r in all_results if r["classification"] == "HIGHLY ENTERABLE"]
    highly.sort(key=lambda x: x["segment_newcomer_fraction"], reverse=True)

    return {
        "total": len(all_results),
        "classifications": classifications,
        "highly_enterable": highly,
        "highly_count": len(highly),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Minimal Enterability Classifier")
    parser.add_argument("psc_code", nargs="?", help="PSC code to analyze (e.g., DA01)")
    parser.add_argument("--multi-year", action="store_true",
                        help="Use multi-year current window (FY2022-2023) instead of single-year (FY2023)")
    parser.add_argument("--top-naics", type=int, default=8,
                        help="Top NAICS codes per PSC to analyze (default: 8)")
    parser.add_argument("--out-dir", default=None,
                        help="Output directory for results")
    args = parser.parse_args()

    psc_argument = args.psc_code
    use_multi_year = args.multi_year
    window = "current_multi" if use_multi_year else "current"

    tools_raw = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    cache = load_cache()

    print("=" * 72)
    print("MINIMAL ENTERABILITY CLASSIFIER")
    print("Think Free — Extended E220/E221 Prototype")
    print("=" * 72)
    print(f"Window: {'FY2022-2023 multi-year' if use_multi_year else 'FY2023 single-year'}")
    print()

    # Determine which PSC codes to analyze
    if psc_argument:
        psc_codes = [psc_argument.upper()]
        # Validate the PSC code has data
        test_data = get_naics_data(cache, psc_argument.upper(), window)
        if not test_data:
            print(f"\nERROR: No NAICS data in cache for PSC {psc_argument.upper()} (window={window})")
            print(f"Available codes with cached data include: {', '.join(sorted([k.split('_')[1] for k in cache.keys() if 'naics_' in k]))}")
            sys.exit(1)
    else:
        # Default: 5 IT/software PSC codes validated in E221
        # These are the codes that have cached NAICS data
        psc_codes = ["DA01", "DA10", "7A21", "7030", "D304"]
        # Filter to codes that have data in the cache for this window
        psc_codes = [c for c in psc_codes if get_naics_data(cache, c, window)]
        if not psc_codes:
            print("\nERROR: No cached data available for any default PSC code (window={window})")
            sys.exit(1)
        print(f"\nAnalyzing default PSC codes (5 IT/software codes from E221 validation, window={window})")

    all_results = []
    for psc in psc_codes:
        print(f"\n=== Analyzing PSC {psc} ===")
        results, error = analyze_psc(psc, cache, window, args.top_naics)
        if error:
            print(f"  {error}")
            continue
        if not results:
            print(f"  No sub-segments analyzed for PSC {psc}")
            continue

        for r in results:
            all_results.append(r)
            print(f"  {r['naics']} ({r['naics_name']}): "
                  f"seg_frac={r['segment_newcomer_fraction']:.4f}, "
                  f"frag={r['fragmentation']:.4f}, "
                  f"oblig=${r['current_obligation']:,.0f}, "
                  f"class={r['classification']}")

    # Print summary
    summary = summarize_results(all_results)
    print("\n" + "=" * 72)
    print("SUMMARY BY CLASSIFICATION")
    print("=" * 72)
    for cls in ["HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", "MARGINAL", "CLOSED"]:
        count = summary["classifications"][cls]
        print(f"  {cls}: {count}")

    print(f"\n  Total sub-segments analyzed: {summary['total']}")
    print(f"  HIGHLY ENTERABLE: {summary['highly_count']}")

    if summary["highly_enterable"]:
        print("\n  TOP HIGHLY ENTERABLE TARGETS:")
        for r in summary["highly_enterable"][:5]:
            print(f"    {r['psc']} / {r['naics']} ({r['naics_name']}): "
                  f"seg_frac={r['segment_newcomer_fraction']:.4f}, "
                  f"frag={r['fragmentation']:.4f}, "
                  f"oblig=${r['current_obligation']:,.0f}, "
                  f"newcomers={r['segment_newcomers']}")

    # Save results to file
    output_path = os.path.join(tools_raw, "minimal_enterability_output.json")
    with open(output_path, "w") as f:
        json.dump({
            "results": all_results,
            "summary": summary,
            "psc_codes_analyzed": psc_codes,
            "window": window,
        }, f, indent=2)
    print(f"\nResults saved to {output_path}")

    print("\n" + "=" * 72)
    print("NOTICE: This is a reversible exploratory prototype — evidence-gathering,")
    print("not product validation. Data sourced from cached USAspending API responses.")
    print("=" * 72)


if __name__ == "__main__":
    main()
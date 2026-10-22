#!/usr/bin/env python3
"""
Minimal Enterability Classifier — Think Free E221/E221 Extension

A reversible exploratory prototype that classifies NAICS-within-PSC
sub-segments as enterable for small programs, using cached USAspending
data. Based on the E220/E221 framework with enterability thresholds:

  HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5
  CLOSED: below thresholds

Usage:
  python3 tools/minimal_enterability.py [PSC_CODE]

If PSC_CODE is omitted, analyzes the 5 IT/software PSC codes (DA01, DA10,
7A21, 7030, D304) whose enterability was validated in E221.

Output includes segment newcomer fraction, fragmentation, obligation,
absolute newcomer count, and enterability classification for each top NAICS
sub-segment, plus a summary classification count.
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
    year_map = {"current": "2023", "prior": "2018", "current_multi": "2022"}
    year = year_map.get(window, "2023")
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
    year_map = {"current": "2023", "prior": "2018"}
    year = year_map.get(window, "2023")
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


def analyze_psc(psc_code, cache, max_naics=8):
    """Analyze one PSC code and return sub-segment enterability results."""
    naics_data = get_naics_data(cache, psc_code, "current")
    if not naics_data:
        return None, f"No NAICS data in cache for PSC {psc_code}"

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
        cur_recipients = get_recipient_data(cache, psc_code, naics_code, "current")
        pri_recipients = get_recipient_data(cache, psc_code, naics_code, "prior")

        if not cur_recipients:
            continue

        cur_rows = cur_recipients.get("results", [])
        pri_rows = pri_recipients.get("results", []) if pri_recipients else []

        cur_by_id, cur_missing = obligation_by_id(cur_rows)
        pri_by_id, pri_missing = obligation_by_id(pri_rows) if pri_rows else ({}, 0)

        cur_ids = set(cur_by_id.keys())
        pri_ids = set(pri_by_id.keys())

        if not cur_ids:
            continue

        seg_new = cur_ids - pri_ids
        seg_frac = len(seg_new) / len(cur_ids)
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
    psc_argument = None
    if len(sys.argv) > 1:
        psc_argument = sys.argv[1].upper()

    cache = load_cache()
    print("=" * 72)
    print("MINIMAL ENTERABILITY CLASSIFIER")
    print("Think Free — Extended E220/E221 Prototype")
    print("=" * 72)

    # Determine which PSC codes to analyze
    if psc_argument:
        psc_codes = [psc_argument]
        # Validate the PSC code has data
        test_data = get_naics_data(cache, psc_argument, "current")
        if not test_data:
            print(f"\nERROR: No NAICS data in cache for PSC {psc_argument}")
            print("Available codes with cached data include: DA01, DA10, 7A21, R425")
            sys.exit(1)
    else:
        # Default: 5 IT/software PSC codes validated in E221
        psc_codes = ["DA01", "DA10", "7A21", "7030", "D304"]
        print(f"\nAnalyzing default PSC codes (5 IT/software codes from E221 validation)")
        print(f"(Uses cached data; no API calls or rate limits)")
        # Quick check: verify at least DA01 has data
        test_data = get_naics_data(cache, "DA01", "current")
        if not test_data:
            print("ERROR: No cached data available")
            sys.exit(1)

    all_results = []
    for psc in psc_codes:
        print(f"\n=== Analyzing PSC {psc} ===")
        results, error = analyze_psc(psc, cache)
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
    output_path = os.path.join(TOOLS_RAW, "minimal_enterability_output.json")
    with open(output_path, "w") as f:
        json.dump({
            "results": all_results,
            "summary": summary,
            "psc_codes_analyzed": psc_codes,
        }, f, indent=2)
    print(f"\nResults saved to {output_path}")

    print("\n" + "=" * 72)
    print("NOTICE: This is a reversible exploratory prototype — evidence-gathering,")
    print("not product validation. Data sourced from cached USAspending API responses.")
    print("=" * 72)


if __name__ == "__main__":
    main()
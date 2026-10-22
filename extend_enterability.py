#!/usr/bin/env python3
"""
Extend enterability analysis beyond the 5 IT PSC codes using cached data.
Uses the same thresholds as E220/E221:
  - HIGHLY ENTERABLE: seg_frac >= 0.30, frag >= 0.60, newcomers >= 20
  - SOMEWHAT ENTERABLE: seg_frac >= 0.20, frag >= 0.40, newcomers >= 10
  - MARGINAL: seg_frac >= 0.10, frag >= 0.20, newcomers >= 5
  - CLOSED: below thresholds
"""

import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, "/home/ubuntu/think-free/tools")
from psc_naics_subsegment_analyzer import classify_enterability, obligation_by_id, top_k_share

TOOLS_RAW = "/home/ubuntu/think-free/tools/raw"
RESULTS_DIR = "/home/ubuntu/think-free/EXPERIMENTS"

def load_json(path):
    with open(path) as f:
        return json.load(f)

def find_cache_keys(cache, prefix):
    """Find all cache keys starting with prefix."""
    return [k for k in cache if k.startswith(prefix)]

def compute_subsegment_metrics(code, naics, naics_name, cur_recipients, pri_recipients):
    """Compute metrics for one (PSC, NAICS) sub-segment, mirroring the analyzer."""
    # Combine current recipient data
    cur_by_id, cur_missing = obligation_by_id(cur_recipients.get("results", []))
    pri_by_id, pri_missing = obligation_by_id(pri_recipients.get("results", []))

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    if not cur_ids:
        return None

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids)

    frag = 1.0 - top_k_share(cur_by_id, 5)
    top5_share = top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)

    classification = classify_enterability(seg_frac, frag, len(seg_new))

    return {
        "code": code,
        "naics": naics,
        "naics_name": naics_name,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "fragmentation": round(frag, 4),
        "top5_share": round(top5_share, 4),
        "current_obligation": obligation,
        "classification": classification,
    }


def main():
    cache = load_json(os.path.join(TOOLS_RAW, "psc_naics_cache.json"))

    # PSC codes to analyze - focus on non-IT codes from E196's G4 list
    # These are PSC codes that have cached NAICS and recipient data from prior experiments
    psc_codes_to_analyze = {
        "R425": "Support-Professional: Engineering/Technical",
        "2840": "Gas turbines and jet engines",
        "1680": "Misc. aircraft accessories and components",
        "S206": "Housekeeping — guard",
        "S216": "Housekeeping — facilities operations support",
        "4220": "Marine lifesaving and diving equipment",
        "Q999": "Medical — other",
        "2320": "Trucks and truck tractors, wheeled",
        "8905": "Meat, poultry and fish",
        "Z2AA": "Repair or alteration of office buildings",
        "U099": "Education/training — other",
    }

    all_results = []

    print("=" * 80)
    print("EXTENDED ENTERABILITY ANALYSIS: PSC codes beyond IT/software")
    print("=" * 80)

    for code, code_name in psc_codes_to_analyze.items():
        print(f"\n--- Analyzing PSC {code} ({code_name}) ---")

        # Try to find NAICS data for this PSC code
        naics_keys = find_cache_keys(cache, f"naics_{code}_")
        if not naics_keys:
            print(f"  No NAICS data in cache for PSC {code}")
            continue

        # Sort NAICS by obligation (descending) - use the first NAICS entry's amount
        # Each naics key like "naics_DA01_2023" maps to data with "results" containing NAICS entries
        # But the cache structure varies; let's look at what's available

        # For each NAICS code entry, try to find recipient data
        for naics_key in naics_keys:
            naics_data = cache[naics_key]
            # Check if this NAICS data has results
            if "results" not in naics_data:
                continue

            naics_results = naics_data["results"]
            # Sort by obligation (amount) descending
            naics_results.sort(key=lambda x: x.get("amount", 0), reverse=True)

            # Take top NAICS codes (limit to avoid too many)
            for naics_entry in naics_results[:5]:
                naics_code = naics_entry.get("code")
                naics_name = naics_entry.get("name", "Unknown")
                if not naics_code:
                    continue

                # Try to find recipient data for (PSC, NAICS) combination
                rec_key_patterns = [
                    f"recipients_{code}_{naics_code}_2023",
                    f"recipients_{code}_{naics_code}_2018",
                    f"recipients_{code}_{naics_code}_2022",
                ]

                cur_recipients = None
                pri_recipients = None

                for rk in rec_key_patterns:
                    if rk in cache:
                        recipient_data = cache[rk]
                        if "results" in recipient_data:
                            if "2023" in rk or "2022" in rk:
                                cur_recipients = recipient_data
                            if "2018" in rk:
                                pri_recipients = recipient_data
                            break  # Use first match

                if not cur_recipients:
                    # Try loading from file path
                    if "file" in recipient_data:
                        raw_file = os.path.join(TOOLS_RAW, recipient_data["file"])
                        if os.path.exists(raw_file):
                            with open(raw_file) as f:
                                recipient_data = json.load(f)
                            if "results" in recipient_data:
                                if "2023" in rk or "2022" in rk:
                                    cur_recipients = recipient_data
                                if "2018" in rk:
                                    pri_recipients = recipient_data

                if not cur_recipients or not pri_recipients:
                    continue

                # Compute metrics
                result = compute_subsegment_metrics(code, naics_code, naics_name, 
                                                    cur_recipients, pri_recipients)
                if result:
                    all_results.append(result)
                    print(f"  {code} / {naics_code} ({naics_name}): "
                          f"seg_frac={result['segment_newcomer_fraction']:.4f}, "
                          f"frag={result['fragmentation']:.4f}, "
                          f"oblig=${result['current_obligation']:,.0f}, "
                          f"class={result['classification']}")

    # Summarize results
    if not all_results:
        print("\nNo results computed. Insufficient cached data.")
        return

    # Print summary by classification
    classifications = defaultdict(list)
    for r in all_results:
        classifications[r["classification"]].append(r)

    print("\n" + "=" * 80)
    print("SUMMARY BY CLASSIFICATION")
    print("=" * 80)
    for cls in ["HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", "MARGINAL", "CLOSED"]:
        if cls in classifications:
            entries = classifications[cls]
            print(f"\n{cls} ({len(entries)} sub-segments):")
            # Sort by enterability score (descending) - use segment_newcomer_fraction as proxy
            entries.sort(key=lambda x: x["segment_newcomer_fraction"], reverse=True)
            for e in entries[:5]:  # Top 5 per classification
                print(f"  {e['code']} / {e['naics']} ({e['naics_name']}): "
                      f"seg_frac={e['segment_newcomer_fraction']:.4f}, "
                      f"frag={e['fragmentation']:.4f}, "
                      f"oblig=${e['current_obligation']:,.0f}")

    # Overall summary
    print(f"\n{'=' * 80}")
    print(f"TOTAL: {len(all_results)} sub-segments analyzed")
    print(f"  HIGHLY ENTERABLE: {len(classifications.get('HIGHLY ENTERABLE', []))}")
    print(f"  SOMEWHAT ENTERABLE: {len(classifications.get('SOMEWHAT ENTERABLE', []))}")
    print(f"  MARGINAL: {len(classifications.get('MARGINAL', []))}")
    print(f"  CLOSED: {len(classifications.get('CLOSED', []))}")

    # Save results
    output_path = os.path.join(RESULTS_DIR, "extend_enterability-results.json")
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Also save summary
    summary_path = os.path.join(RESULTS_DIR, "extend_enterability-summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"Extended enterability analysis beyond 5 IT PSC codes\n")
        f.write(f"Total sub-segments analyzed: {len(all_results)}\n")
        for cls in ["HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE", "MARGINAL", "CLOSED"]:
            count = len(classifications.get(cls, []))
            f.write(f"  {cls}: {count}\n")
        f.write("\nKey finding: ")
        # Determine key finding
        highly = len(classifications.get("HIGHLY ENTERABLE", []))
        if highly > 0:
            f.write(f"Found {highly} HIGHLY ENTERABLE sub-segments beyond IT codes. ")
            # List some examples
            highly_entries = classifications.get("HIGHLY ENTERABLE", [])[:3]
            for e in highly_entries:
                f.write(f"{e['code']}/{e['naics']}, ")
        else:
            f.write("No HIGHLY ENTERABLE sub-segments found beyond IT codes. ")
    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    main()
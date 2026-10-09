#!/usr/bin/env python3
"""
E077 — Non-software Discourse view_count + unserved-open measurement.

Measures the view_count (arrival) instrument and unserved-open-like fraction
across a stratified sample of non-software Discourse forums. Pivoted from
Stack Exchange due to API rate limiting (Cloudflare error 1015).
"""
import json
import math
import os
import sys

from harvest_classify import (
    TARGET_FORUMS,
    TOPICS_PER_FORUM,
    SLEEP_BETWEEN_REQUESTS,
    fetch_latest_page,
    classify_topics,
    harvest_forum_topics,
    wilson_ci95,
    measure_forum,
    save_raw_data,
)


def main() -> int:
    """Main entry point for E077 Discourse measurement."""
    print("=== E077 Non-software Discourse view_count + unserved-open Measurement ===")
    print(f"Target forums: {len(TARGET_FORUMS)}")
    print(f"Topics per forum: {TOPICS_PER_FORUM}")
    print("NOTE: Pivoted from Stack Exchange due to Cloudflare 1015 rate limiting")
    print()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    all_topics = []
    all_classified = []

    for domain in TARGET_FORUMS:
        try:
            # Harvest
            topics = harvest_forum_topics(domain)

            # Classify
            classified = classify_topics(topics)

            # Save raw data
            save_raw_data(domain, topics, classified, output_dir)

            # Measure
            result = measure_forum(domain)
            all_results.append(result)

            all_topics.extend(topics)
            all_classified.extend(classified)

        except Exception as e:
            print(f"Error measuring {domain}: {e}")
            all_results.append({
                "domain": domain,
                "total": 0,
                "error": str(e),
            })

    # Aggregate results
    total_all = sum(r["total"] for r in all_results if "error" not in r)
    view_positive_all = sum(r["view_positive"] for r in all_results if "error" not in r)
    need_topics_all = sum(r["need_topics"] for r in all_results if "error" not in r)
    unserved_all = sum(r["unserved_open_like"] for r in all_results if "error" not in r)

    ci_low, ci_high = wilson_ci95(unserved_all, total_all)

    print(f"\n=== AGGREGATE RESULTS ===")
    print(f"Total topics: {total_all}")
    if total_all > 0:
        print(f"view_count > 0: {view_positive_all} ({view_positive_all/total_all*100:.1f}%)")
        print(f"Need topics: {need_topics_all} ({need_topics_all/total_all*100:.1f}%)")
        print(f"Unserved-open-like: {unserved_all} ({unserved_all/total_all*100:.2f}%)")
        print(f"Wilson CI95: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]")
    else:
        print("No data collected")

    # Gate assessments
    print(f"\n=== GATE ASSESSMENTS ===")

    # G1: view_count validation
    vc_rate = view_positive_all / total_all if total_all > 0 else 0
    g1_pass = vc_rate >= 0.95
    print(f"G1 (view_count >= 95%): {'PASS' if g1_pass else 'FAIL'} — {vc_rate*100:.1f}%")

    # G2: need prevalence
    need_rate = need_topics_all / total_all if total_all > 0 else 0
    g2_pass = need_rate >= 0.05
    print(f"G2 (need prevalence >= 5%): {'PASS' if g2_pass else 'FAIL'} — {need_rate*100:.1f}%")

    # G3: unserved fraction measurable
    unserved_rate = unserved_all / total_all if total_all > 0 else 0
    g3_pass = unserved_rate < 0.50 and ci_high < 0.60
    print(f"G3 (unserved < 50%, CI95 upper < 60%): {'PASS' if g3_pass else 'FAIL'} — {unserved_rate*100:.1f}%, CI95=[{ci_low*100:.1f}%, {ci_high*100:.1f}%]")

    # G4: cross-forum variance
    forums_with_unserved = sum(1 for r in all_results if "error" not in r and r["unserved_open_like"] > 0)
    g4_pass = forums_with_unserved >= 3
    print(f"G4 (>= 3 forums with unserved > 0): {'PASS' if g4_pass else 'FAIL'} — {forums_with_unserved} forums")

    all_gates_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\nALL GATES: {'PASS' if all_gates_pass else 'FAIL'}")

    # Save aggregated results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(output_path, "w") as f:
        json.dump({
            "pivot_note": "Pivoted from Stack Exchange to Discourse due to Cloudflare 1015 rate limiting",
            "forums": all_results,
            "aggregate": {
                "total": total_all,
                "view_positive": view_positive_all,
                "need_topics": need_topics_all,
                "unserved_open_like": unserved_all,
                "unserved_fraction": unserved_rate,
                "wilson_ci95": [ci_low, ci_high],
                "gates": {
                    "G1_view_count": {"pass": g1_pass, "value": vc_rate},
                    "G2_need_prevalence": {"pass": g2_pass, "value": need_rate},
                    "G3_unserved_fraction": {"pass": g3_pass, "value": unserved_rate, "ci95": [ci_low, ci_high]},
                    "G4_cross_forum_variance": {"pass": g4_pass, "forums_with_unserved": forums_with_unserved},
                },
                "all_gates_pass": all_gates_pass,
            }
        }, f, sort_keys=True, indent=2)

    print(f"\n=== Results saved to {output_path} ===")

    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    sys.exit(main())
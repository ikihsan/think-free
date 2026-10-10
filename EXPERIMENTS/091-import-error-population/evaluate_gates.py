#!/usr/bin/env python3
"""
E091 — Evaluate kill gates for import-error population experiment.
"""

import json
from pathlib import Path

HERE = Path(__file__).parent


def main():
    results_path = HERE / "results.json"
    if not results_path.exists():
        print("results.json not found. Run classify.py first.")
        return 1

    with open(results_path) as f:
        results = json.load(f)

    total = results.get("total_sampled", 0)
    module_no_dist = results.get("module_no_dist_count", 0)
    rate = results.get("module_no_dist_rate", 0.0)
    categories = results.get("categories", {})

    # Venue breakdown
    classified_path = HERE / "classified.jsonl"
    venue_counts = {}
    venue_module_no_dist = {}
    if classified_path.exists():
        with open(classified_path) as f:
            for line in f:
                item = json.loads(line)
                venue = item.get("venue", "unknown")
                venue_counts[venue] = venue_counts.get(venue, 0) + 1
                if item.get("category") == "names_module_no_dist":
                    venue_module_no_dist[venue] = venue_module_no_dist.get(venue, 0) + 1

    # Gate G1: rate >= 1%
    g1_pass = rate >= 0.01

    # Gate G2: total sample >= 200
    g2_pass = total >= 200

    # Gate G3: each venue >= 50 (or all available if fewer)
    venues = set(venue_counts.keys())
    g3_pass = all(venue_counts.get(v, 0) >= 50 for v in venues) if venues else False

    # Update results
    results.update({
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "venue_counts": venue_counts,
        "venue_module_no_dist": venue_module_no_dist,
    })

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    # Print verdict
    print(f"\n=== Gate Evaluation ===")
    print(f"G1 (rate >= 1%): {'PASS' if g1_pass else 'FAIL'} — rate = {rate:.2%}")
    print(f"G2 (sample >= 200): {'PASS' if g2_pass else 'FAIL'} — total = {total}")
    print(f"G3 (venue diversity >= 50 each): {'PASS' if g3_pass else 'FAIL'}")
    for v in sorted(venues):
        vc = venue_counts.get(v, 0)
        vmd = venue_module_no_dist.get(v, 0)
        print(f"  {v}: {vc} total, {vmd} module-no-dist")

    all_pass = g1_pass and g2_pass and g3_pass
    print(f"\nOverall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
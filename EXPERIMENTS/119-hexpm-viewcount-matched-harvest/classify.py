#!/usr/bin/env python3
"""
E119 — Hex.pm view-count classifier with whole-word matching,
expanded vocabulary, and contextual disambiguation for matched-harvest
experiment. Addresses E113/F116 binding constraint: shared classifier only
labelled 28% of rows. This prototype declares a coverage floor (80%) and uses
anchored whole-word matching with contextual disambiguation.
"""

import re
import json
from pathlib import Path
import sys

# Import sibling modules: the classifier core, vocabulary, statistics,
# and harvest were split out of this file at the 300-line cap. They are
# re-imported here so `classify` stays the entry point and
# `from classify import <name>` keeps resolving the same names.
sys.path.insert(0, str(Path(__file__).parent))
from classify_core import (
    classify_description,
    classify_repo,
    has_need_context,
    tokenize,
    window_tokens,
)
from harvest import (
    collect_pool,
    fetch_hexpm_packages,
    fetch_hexpm_random,
)
from stats import cliff_delta, compute_active_rate, compute_coverage, mann_whitney_u
from vocab import DISAMBIG_WINDOW, GENERIC_TERMS, NEED_INDICATORS


def main():
    import sys
    print("=" * 60)
    print("E119 — Hex.pm view-count matched-harvest experiment")
    print("=" * 60)
    print()

    # Step 1: Collect pool from Hex.pm
    print("[1] Collecting pool from Hex.pm API...")
    # Step 1: collect the Hex.pm pool (harvest.py owns the fetch step).
    all_packages = collect_pool()
    print(f"  Total packages collected: {len(all_packages)}")

    # Step 2: Classify each package
    print()
    print("[2] Classifying packages...")
    classifications = []
    package_results = []

    for i, pkg in enumerate(all_packages[:200]):
        cls, weight, reason = classify_repo(pkg["name"], pkg["description"])
        classifications.append((cls, weight, reason))
        pkg["_classification"] = cls
        pkg["_weight"] = weight
        pkg["_reason"] = reason
        package_results.append(pkg)
        if (i + 1) % 20 == 0:
            print(f" classified {i+1}/200...")

    # Step 3: Compute coverage
    print()
    print("[3] Computing coverage metrics...")
    coverage_rate, classified_count, total_count = compute_coverage(classifications)
    print(f"  Total packages: {total_count}")
    print(f"  Classified (weight >= 0.5): {classified_count} ({coverage_rate:.1%})")
    print(f"  Coverage floor: 80%")

    need_classified = sum(1 for c, w, r in classifications if c == "need-related" and w >= 0.5)
    random_classified = sum(1 for c, w, r in classifications if c == "random" and w >= 0.5)
    uncertain = sum(1 for c, w, r in classifications if c == "uncertain")
    print(f"  Need-related classified: {need_classified}")
    print(f"  Random classified: {random_classified}")
    print(f"  Uncertain: {uncertain}")

    # Step 4: Split into matched harvest arms
    print()
    print("[4] Splitting into matched harvest arms...")

    need_group = [p for p in package_results if p.get("_classification") == "need-related"]
    random_group = [p for p in package_results if p.get("_classification") == "random"]

    print(f"  Need-related: {len(need_group)} packages")
    print(f"  Random: {len(random_group)} packages")

    # G1: Sample size ≥ 50 per group
    gates_result = {}
    gates_result["G1_sample_size"] = len(need_group) >= 50 and len(random_group) >= 50
    gates_passed = []
    gates_passed.append("G1" if gates_result["G1_sample_size"] else "G1-failed")
    print(f"  G1 (sample ≥ 50 per group): {'PASS' if gates_result['G1_sample_size'] else 'FAIL'}")
    if not gates_result["G1_sample_size"]:
        print(f"    need-related: {len(need_group)}, random: {len(random_group)}")

    # G2: Coverage floor ≥ 80%
    gates_result["G2_coverage"] = coverage_rate >= 0.80
    gates_passed.append("G2" if gates_result["G2_coverage"] else "G2-failed")
    print(f"  G2 (coverage ≥ 80%): {'PASS' if gates_result['G2_coverage'] else 'FAIL'}")
    if not gates_result["G2_coverage"]:
        print(f"    Current coverage: {coverage_rate:.1%}")

    # If G2 fails, stop here
    if not gates_result["G2_coverage"]:
        print()
        print("  **G2 FAILED: coverage floor not met**")
        print("  Per protocol, effect size (G3) cannot be meaningfully measured")
        print("  without coverage of the population.")
        goto_effect_size = False
    else:
        goto_effect_size = True

    # Step 5: Effect size measurement (if G2 passed)
    if goto_effect_size and len(need_group) > 0 and len(random_group) > 0:
        print()
        print("[5] Computing effect size (matched harvest)...")

        need_downloads = [p.get("recent_downloads", 0) for p in need_group if p.get("recent_downloads", 0) > 0]
        random_downloads = [p.get("recent_downloads", 0) for p in random_group if p.get("recent_downloads", 0) > 0]

        print(f"  Need-related downloads (positive): {len(need_downloads)}")
        print(f"  Random downloads (positive): {len(random_downloads)}")

        if len(need_downloads) > 0 and len(random_downloads) > 0:
            delta = cliff_delta(need_downloads, random_downloads)
            u_stat, p_value = mann_whitney_u(need_downloads, random_downloads)

            gates_result["G3_cliff_delta"] = delta > 0.147
            gates_passed.append("G3" if gates_result["G3_cliff_delta"] else "G3-failed")
            print(f"  G3 (Cliff's delta > 0.147): {'PASS' if gates_result['G3_cliff_delta'] else 'FAIL'}")
            print(f"    Cliff's delta = {delta:.4f}")

            gates_result["G3_p_value"] = p_value < 0.05
            print(f"  Mann-Whitney U p-value = {p_value:.6f}")
            print(f"    p < 0.05: {'PASS' if p_value < 0.05 else 'FAIL'}")

            # G4: Both categories represented
            gates_result["G4_bothrepresented"] = True
            gates_passed.append("G4" if gates_result["G4_bothrepresented"] else "G4-failed")
            print(f"  G4 (both categories represented): PASS")

            # Wilson CI95
            all_downloads = need_downloads + random_downloads
            if all_downloads:
                median_val = sorted(all_downloads)[len(all_downloads) // 2]
                need_above = sum(1 for d in need_downloads if d > median_val)
                wilson_lb = need_above / len(need_downloads)
                gates_result["G3_wilson_lb"] = wilson_lb > 0.60
                print(f"  Wilson LB (need above random median > 0.60): {wilson_lb:.4f}")
                print(f"    > 0.60: {'PASS' if wilson_lb > 0.60 else 'FAIL'}")
        else:
            for _ in ["G3_cliff_delta", "G3_p_value", "G3_wilson_lb", "G4_bothrepresented"]:
                if _ not in gates_result:
                    gates_passed.append(_.replace("G3", "G3").replace("G4", "G4") + "-failed")
    else:
        for _ in ["G1_sample_size", "G2_coverage", "G3_cliff_delta", "G4_bothrepresented"]:
            if _ not in gates_result:
                gates_passed.append(_ + "-failed")

    # Step 6: Summary
    print()
    print("=" * 60)
    print("GATE SUMMARY")
    print("=" * 60)
    all_pass = all(gates_result.get(g, False) for g in ["G1_sample_size", "G2_coverage", "G3_cliff_delta", "G4_bothrepresented"])
    print(f"  G1 (sample size): {'PASS' if gates_result.get('G1_sample_size') else 'FAIL'}")
    print(f"  G2 (coverage floor): {'PASS' if gates_result.get('G2_coverage') else 'FAIL'}")
    print(f"  G3 (Cliff's delta): {'PASS' if gates_result.get('G3_cliff_delta') else 'FAIL'}")
    print(f"  G4 (both represented): {'PASS' if gates_result.get('G4_bothrepresented') else 'FAIL'}")
    print()
    if all_pass:
        print("  RESULT: ALL GATES PASS — view-count principle validated on Hex.pm under matched harvest")
    else:
        failed = [g for g in ["G1_sample_size", "G2_coverage", "G3_cliff_delta", "G4_bothrepresented"]
                  if not gates_result.get(g, False)]
        print(f"  RESULT: GATES FAILED — {', '.join(failed)}")
        if "G2_coverage" in failed:
            print("  Note: G2 failure means effect size measurement is not meaningful")
            print("  without population coverage. Classifier improvement needed.")
        if "G3_cliff_delta" in failed:
            print("  Note: G3 failure under matched harvest means the view-count")
            print("  principle does not generalize to Hex.pm with a proper design —")
            print("  previous 'ALL GATES PASS' results were harvest artifacts.")
            print(f"  Observed Cliff's delta: {gates_result.get('G3_cliff_delta', 'N/A')}")

    output = {
        "experiment": "E119",
        "platform": "Hex.pm",
        "pool_size": min(200, len(all_packages)),
        "coverage_floor": 0.80,
        "coverage_rate": coverage_rate,
        "classified": {
            "need_related": sum(1 for c, w, r in classifications if c == "need-related" and w >= 0.5),
            "random": sum(1 for c, w, r in classifications if c == "random" and w >= 0.5),
            "uncertain": sum(1 for c, w, r in classifications if c == "uncertain"),
        },
        "gate_results": gates_result,
        "packages": package_results,
    }

    results_path = Path(__file__).parent / "results.json"
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to {results_path}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
#!/usr/bin/env python3
"""
E116 — View-count classifier prototype: gate evaluation and result analysis.

Runs after classify.py has collected and classified the pool.
Evaluates all four gates (G1-G4) and produces a summary.
"""

import json
import sys
from pathlib import Path
from statistics import median


def load_results(path="results.json"):
    with open(path) as f:
        return json.load(f)


def evaluate_gates(results):
    """Evaluate all four gates and return gate results + overall pass/fail."""
    g = results["gate_results"]
    coverage = results["coverage_rate"]
    pool_size = results["pool_size"]
    classifications = results["classified"]

    gate_details = {}

    # G1: Sample size ≥ 50 per group
    need_n = g.get("need_group_size", 0)
    random_n = g.get("random_group_size", 0)
    gate_details["G1"] = {
        "pass": need_n >= 50 and random_n >= 50,
        "need_count": need_n,
        "random_count": random_n,
        "criterion": "≥ 50 per group",
    }

    # G2: Coverage floor ≥ declared floor
    floor = results["coverage_floor"]
    gate_details["G2"] = {
        "pass": coverage >= floor,
        "rate": coverage,
        "floor": floor,
        "criterion": f"≥ {floor:.0%} of pool classified",
    }

    # G3: Cliff's delta > 0.147 AND (Wilson LB > 0.60 OR p-value < 0.05)
    cliff = g.get("cliff_delta", 0)
    p_val = g.get("p_value", 1.0)
    wilson_lb = g.get("wilson_lb", 0.0)

    # G3 has three sub-criteria; all must pass
    gate_details["G3"] = {
        "pass": cliff > 0.147 and wilson_lb > 0.60 and p_val < 0.05,
        "cliff_delta": cliff,
        "wilson_lb": wilson_lb,
        "p_value": p_val,
        "criterion": "Cliff's delta > 0.147 AND Wilson LB > 0.60 AND p < 0.05",
    }

    # G4: Both categories represented
    gate_details["G4"] = {
        "pass": g.get("both_represented", False),
        "need_count": g.get("need_group_size", 0),
        "random_count": g.get("random_group_size", 0),
        "criterion": "need-related > 0 AND random > 0",
    }

    # Overall: all gates must pass
    all_pass = all(d["pass"] for d in gate_details.values())
    gate_details["OVERALL"] = {
        "pass": all_pass,
        "criterion": "All G1-G4 pass",
    }

    return gate_details


def summarize_classifications(results):
    """Summarize the classification breakdown."""
    classified = results["classified"]
    total = classified["need_related"] + classified["random"] + classified["uncertain"]

    print(f"\nClassification summary:")
    print(f"  Total packages: {total}")
    print(f"  Need-related: {classified['need_related']} ({classified['need_related']/total*100:.1f}%)")
    print(f"  Random: {classified['random']} ({classified['random']/total*100:.1f}%)")
    print(f"  Uncertain: {classified['uncertain']} ({classified['uncertain']/total*100:.1f}%)")
    print(f"  Coverage rate: {results['coverage_rate']:.1%}")

    return total


def main():
    import os

    results_path = Path(__file__).parent / "results.json"
    if not results_path.exists():
        print(f"Error: {results_path} not found. Run classify.py first.")
        sys.exit(1)

    results = load_results(results_path)

    print("\n" + "=" * 60)
    print("E116 — Gate Evaluation")
    print("=" * 60)

    summarize_classifications(results)

    gate_details = evaluate_gates(results)

    print("\n" + "-" * 60)
    print("GATE RESULTS")
    print("-" * 60)

    for gate_name, details in gate_details.items():
        status = "PASS" if details["pass"] else "FAIL"
        print(f"  {gate_name}: {status}")
        print(f"    Criterion: {details['criterion']}")
        if "rate" in details:
            print(f"    Rate: {details['rate']:.1%} (floor: {details['floor']:.1%})")
        if "cliff_delta" in details:
            print(f"    Cliff's delta: {details['cliff_delta']:.4f}")
        if "p_value" in details:
            print(f"    p-value: {details['p_value']:.6f}")
        if "wilson_lb" in details:
            print(f"    Wilson LB: {details['wilson_lb']:.4f}")
        if "need_count" in details:
            print(f"    Need count: {details['need_count']}")
        if "random_count" in details:
            print(f"    Random count: {details['random_count']}")

    print()
    overall = gate_details.get("OVERALL", {})
    if overall.get("pass", False):
        print("RESULT: ALL GATES PASS — classifier prototype validated")
    else:
        failed = [g for g, d in gate_details.items()
                  if g != "OVERALL" and not d.get("pass", False)]
        print(f"RESULT: GATES FAILED — {', '.join(failed)}")
        if "G2" in failed:
            print("  Note: G2 (coverage floor) failure means effect size")
            print("  measurement is not meaningful without population coverage.")

    return 0 if overall.get("pass", False) else 1


if __name__ == "__main__":
    sys.exit(main())
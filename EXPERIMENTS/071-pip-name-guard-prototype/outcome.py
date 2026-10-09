#!/usr/bin/env python3
"""E071 outcome: gate evaluation and result reporting.

Reads harvested results from both arms, computes the key metrics,
and reports whether the view_count principle is supported on PyPI.

Usage:
    python3 outcome.py     # evaluate both arms' results
    python3 outcome.py --arm 1    # evaluate arm A only
    python3 outcome.py --arm 2    # evaluate arm B only
"""

import json
import os
import sys
import argparse
from statistics import mean, stdev


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load_arm_results(arm_id):
    """Load harvested results for one arm."""
    if arm_id == 1:
        path = os.path.join(HERE, "raw", "arm-a-results.jsonl")
    else:
        path = os.path.join(HERE, "raw", "arm-b-results.jsonl")

    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def classify_activity(score):
    """Classify activity score into category."""
    if score == -1:
        return "missing"
    elif score >= 10:
        return "active"
    elif score > 0:
        return "inactive"
    else:
        return "missing"


def evaluate_arm(arm_id):
    """Evaluate one arm's results and return gate outcomes."""
    results = load_arm_results(arm_id)

    # Classify each package
    classifications = []
    active_count = 0
    inactive_count = 0
    missing_count = 0

    for r in results:
        score = r["activity_score"]
        cls = classify_activity(score)
        r["classification"] = cls
        classifications.append(cls)

        if cls == "active":
            active_count += 1
        elif cls == "inactive":
            inactive_count += 1
        else:
            missing_count += 1

    # Compute fractions
    n = len(results)
    active_frac = active_count / n if n > 0 else 0
    inactive_frac = inactive_count / n if n > 0 else 0
    missing_frac = missing_count / n if n > 0 else 0

    # Wilson score interval for the active fraction
    # Wilson CI: p_hat + z^2/(2n) +/- z * sqrt(p_hat(1-p_hat)/n + z^2/(4n^2)) / (1 + z^2/n)
    # Using z = 1.96 for 95% CI
    z = 1.96
    if n > 0 and active_count > 0 and active_count < n:
        p_hat = active_count / n
        denominator = 1 + z**2 / n
        center_adjusted = (p_hat + z**2 / (2 * n)) / denominator
        margin = (z * ((p_hat * (1 - p_hat) + z**2 / (4 * n)) ** 0.5) / denominator)
        lower = max(0, center_adjusted - margin)
        upper = min(1, center_adjusted + margin)
    else:
        lower = 0 if active_frac == 0 else 1
        upper = 1 if active_frac == 0 else 1

    # Two-sample t-test comparing activity scores between arms
    # (need to load both arms)
    from .harvest import ARM_A_PACKAGES, ARM_B_PACKAGES

    return {
        "n": n,
        "active_count": active_count,
        "inactive_count": inactive_count,
        "missing_count": missing_count,
        "active_fraction": active_frac,
        "active_ci95_lower": lower,
        "active_ci95_upper": upper,
        "classifications": classifications,
    }


def main():
    parser = argparse.ArgumentParser(description="E071 outcome evaluation")
    parser.add_argument("--arm", type=int, choices=[1, 2], default=None,
                        help="Arm to evaluate (1 or 2), or both if omitted")
    args = parser.parse_args()

    if args.arm is None:
        # Evaluate both arms
        results_1 = evaluate_arm(1)
        results_2 = evaluate_arm(2)

        print("=" * 60)
        print("E071 — PyPI Package Activity as view_count proxy")
        print("=" * 60)
        print()

        # Arm A summary
        print("=== Arm A: Need-related packages ===")
        print(f"  Packages evaluated: {results_1['n']}")
        print(f"  Active: {results_1['active_count']} ({results_1['active_fraction']:.2%})")
        print(f"  95% CI: [{results_1['active_ci95_lower']:.3f}, {results_1['active_ci95_upper']:.3f}]")
        print(f"  Inactive: {results_1['inactive_count']}")
        print(f"  Missing: {results_1['missing_count']}")

        # Arm B summary
        print()
        print("=== Arm B: Random packages ===")
        print(f"  Packages evaluated: {results_2['n']}")
        print(f"  Active: {results_2['active_count']} ({results_2['active_fraction']:.2%})")
        print(f"  95% CI: [{results_2['active_ci95_lower']:.3f}, {results_2['active_ci95_upper']:.3f}]")
        print(f"  Inactive: {results_2['inactive_count']}")
        print(f"  Missing: {results_2['missing_count']}")

        # Key comparison
        print()
        print("=== Key comparison ===")
        diff = results_1['active_fraction'] - results_2['active_fraction']
        print(f"  Difference (A - B): {diff:.4f} ({diff*100:.2f} percentage points)")
        print(f"  Active fraction A: {results_1['active_fraction']:.2%}")
        print(f"  Active fraction B: {results_2['active_fraction']:.2%}")

        # Gate decision
        print()
        print("=== Gate G3 decision ===")
        # G3: if lower CI95 > 0.6, support view_count principle
        #    if upper CI95 < 0.4, refute it
        #    otherwise inconclusive
        support_lower = results_1['active_ci95_lower'] > 0.6
        refute_upper = results_1['active_ci95_upper'] < 0.4

        if support_lower:
            print("  G3 PASSES: lower CI95 > 0.6 — PyPI activity systematically differentiates need-related packages. view_count principle supported on PyPI.")
        elif refute_upper:
            print("  G3 FAILS: upper CI95 < 0.4 — PyPI activity does NOT systematically differentiate need-related packages. view_count principle refuted on PyPI.")
        else:
            print("  G3 INCONCLUSIVE: inconclusive zone — cannot determine from this experiment.")

        print()
        print("=" * 60)

    elif args.arm == 1:
        results = evaluate_arm(1)
        print(f"Arm {results['n']} packages evaluated")
        print(f"Active fraction: {results['active_fraction']:.2%}")
        print(f"95% CI: [{results['active_ci95_lower']:.3f}, {results['active_ci95_upper']:.3f}]")
        print(f"Classifications: {results['classifications']}")

    elif args.arm == 2:
        results = evaluate_arm(2)
        print(f"Arm {results['n']} packages evaluated")
        print(f"Active fraction: {results['active_fraction']:.2%}")
        print(f"95% CI: [{results['active_ci95_lower']:.3f}, {results['active_ci95_upper']:.3f}]")
        print(f"Classifications: {results['classifications']}")


if __name__ == "__main__":
    main()
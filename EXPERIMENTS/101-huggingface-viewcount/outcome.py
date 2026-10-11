#!/usr/bin/env python3
"""Evaluate gates for E101 Hugging Face Hub view-count experiment."""

import json
import math
import os
import sys
from typing import List, Tuple

ACTIVE_THRESHOLD = 100  # downloads_lastMonth > 100
G1_MIN_MODELS = 30
G3_WILSON_LOWER_BOUND = 0.60
G2_ALPHA = 0.05


def wilson_lower_bound(successes: int, trials: int, confidence: float = 0.95) -> float:
    """Wilson score interval lower bound."""
    if trials == 0:
        return 0.0
    z = 1.96  # 95% confidence
    p = successes / trials
    denominator = 1 + z**2 / trials
    centre = p + z**2 / (2 * trials)
    adjustment = z * math.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2))
    return (centre - adjustment) / denominator


def welch_t_test(p1: float, n1: int, p2: float, n2: int) -> Tuple[float, float]:
    """Welch's t-test for two proportions with Agresti-Caffo adjustment for boundaries.
    
    Returns (t_stat, p_value).
    """
    import math
    if n1 == 0 or n2 == 0:
        return 0.0, 1.0
    
    # Agresti-Caffo adjustment: add 1 success and 1 failure to each group
    # This prevents zero standard errors at boundaries (p=0 or p=1)
    adj_n1 = n1 + 2
    adj_n2 = n2 + 2
    adj_p1 = (p1 * n1 + 1) / adj_n1
    adj_p2 = (p2 * n2 + 1) / adj_n2
    
    # Standard error for difference in proportions
    se1 = math.sqrt(adj_p1 * (1 - adj_p1) / adj_n1)
    se2 = math.sqrt(adj_p2 * (1 - adj_p2) / adj_n2)
    se = math.sqrt(se1**2 + se2**2)
    
    if se == 0:
        return 0.0, 1.0
    
    t_stat = (adj_p1 - adj_p2) / se
    
    # Degrees of freedom (Welch-Satterthwaite)
    df = (se1**2 + se2**2)**2 / (se1**4 / (adj_n1 - 1) + se2**4 / (adj_n2 - 1))
    
    # Two-tailed p-value approximation using normal distribution
    # (for large df, t approaches normal)
    p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))
    
    return t_stat, p_value


def load_models(path: str) -> List[dict]:
    models = []
    if not os.path.exists(path):
        return models
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                models.append(json.loads(line))
    return models


def evaluate_gates(arm1: List[dict], arm2: List[dict]) -> dict:
    """Evaluate all predeclared gates."""
    
    # G1: Retrieval
    n1, n2 = len(arm1), len(arm2)
    g1_pass = n1 >= G1_MIN_MODELS and n2 >= G1_MIN_MODELS
    
    # Activity classification
    active1 = sum(1 for m in arm1 if m.get("downloads", 0) > ACTIVE_THRESHOLD)
    active2 = sum(1 for m in arm2 if m.get("downloads", 0) > ACTIVE_THRESHOLD)
    
    rate1 = active1 / n1 if n1 > 0 else 0.0
    rate2 = active2 / n2 if n2 > 0 else 0.0
    
    # G2: Activity difference (Welch's t-test)
    t_stat, p_value = welch_t_test(rate1, n1, rate2, n2)
    g2_pass = p_value < G2_ALPHA and rate1 > rate2
    
    # G3: Need-related activity floor (Wilson lower bound)
    wilson_lb = wilson_lower_bound(active1, n1)
    g3_pass = wilson_lb > G3_WILSON_LOWER_BOUND
    
    return {
        "g1_retrieval": {
            "pass": g1_pass,
            "need_related_count": n1,
            "random_count": n2,
            "min_required": G1_MIN_MODELS,
        },
        "g2_activity_difference": {
            "pass": g2_pass,
            "need_related_active_rate": rate1,
            "random_active_rate": rate2,
            "need_related_active": active1,
            "need_related_total": n1,
            "random_active": active2,
            "random_total": n2,
            "t_statistic": t_stat,
            "p_value": p_value,
            "alpha": G2_ALPHA,
        },
        "g3_need_related_floor": {
            "pass": g3_pass,
            "wilson_lower_bound": wilson_lb,
            "threshold": G3_WILSON_LOWER_BOUND,
            "active": active1,
            "total": n1,
        },
        "summary": {
            "active_threshold": ACTIVE_THRESHOLD,
            "overall_pass": g1_pass and g2_pass and g3_pass,
        }
    }


def main():
    arm1 = load_models("raw/need-related.jsonl")
    arm2 = load_models("raw/random.jsonl")
    
    if not arm1 and not arm2:
        print("No data found. Run harvest.py first.", file=sys.stderr)
        sys.exit(1)
    
    results = evaluate_gates(arm1, arm2)
    
    # Print results
    print("=" * 60)
    print("E101 Hugging Face Hub View-Count Experiment Results")
    print("=" * 60)
    
    g1 = results["g1_retrieval"]
    print(f"\nG1 Retrieval: {'PASS' if g1['pass'] else 'FAIL'}")
    print(f"  Need-related models: {g1['need_related_count']}")
    print(f"  Random models: {g1['random_count']}")
    print(f"  Minimum required per arm: {g1['min_required']}")
    
    g2 = results["g2_activity_difference"]
    print(f"\nG2 Activity Difference: {'PASS' if g2['pass'] else 'FAIL'}")
    print(f"  Need-related active rate: {g2['need_related_active_rate']:.3f} ({g2['need_related_active']}/{g2['need_related_total']})")
    print(f"  Random active rate: {g2['random_active_rate']:.3f} ({g2['random_active']}/{g2['random_total']})")
    print(f"  t-statistic: {g2['t_statistic']:.3f}")
    print(f"  p-value: {g2['p_value']:.6f} (alpha={g2['alpha']})")
    
    g3 = results["g3_need_related_floor"]
    print(f"\nG3 Need-Related Activity Floor: {'PASS' if g3['pass'] else 'FAIL'}")
    print(f"  Wilson CI95 lower bound: {g3['wilson_lower_bound']:.4f}")
    print(f"  Threshold: {g3['threshold']}")
    print(f"  Active: {g3['active']}/{g3['total']}")
    
    print(f"\nOverall: {'ALL GATES PASS' if results['summary']['overall_pass'] else 'GATES FAILED'}")
    
    # Write results
    os.makedirs("results", exist_ok=True)
    with open("results/results.json", "w") as f:
        json.dump({
            "experiment": "E101 Hugging Face Hub view-count principle",
            "protocol": "PROTOCOL.md",
            "gates": results,
            "arms": {
                "need_related": {"count": len(arm1)},
                "random": {"count": len(arm2)},
            }
        }, f, indent=2)
    
    print(f"\nResults written to results/results.json")


if __name__ == "__main__":
    main()
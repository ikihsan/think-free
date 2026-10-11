#!/usr/bin/env python3
"""
E111 — Analyze classified Docker Hub data and evaluate gates.
"""

import json
import math
from pathlib import Path
from statistics import median

try:
    from scipy.stats import mannwhitneyu
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available, using manual Mann-Whitney U implementation")


def mann_whitney_u_manual(x, y):
    """Manual Mann-Whitney U test implementation (two-sided)."""
    # Combine and rank
    combined = [(v, 0) for v in x] + [(v, 1) for v in y]
    combined.sort(key=lambda p: p[0])

    # Assign ranks (average for ties)
    ranks = {}
    i = 0
    n = len(combined)
    while i < n:
        j = i
        while j < n and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    # Sum ranks for group 0 (x)
    r1 = sum(ranks[i] for i in range(n) if combined[i][1] == 0)
    n1 = len(x)
    n2 = len(y)

    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    # Normal approximation for p-value (large sample)
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sigma == 0:
        return u, 1.0
    z = (u - mu) / sigma
    # Two-tailed p-value
    import math
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u, p


def cliffs_delta(x, y):
    """Compute Cliff's delta effect size."""
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return 0.0
    greater = sum(1 for a in x for b in y if a > b)
    less = sum(1 for a in x for b in y if a < b)
    return (greater - less) / (n1 * n2)


def wilson_ci_lower(k, n, z=1.96):
    """Wilson score interval lower bound for proportion."""
    if n == 0:
        return 0.0
    p = k / n
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjustment = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    lower = (centre - adjustment) / denominator
    return max(0.0, lower)


def evaluate_gates(need_pulls, random_pulls):
    """Evaluate all four gates."""
    results = {}

    # G1: Sample size
    total_need = len(need_pulls)
    total_random = len(random_pulls)
    total = total_need + total_random
    g1_pass = total >= 200 and total_need >= 100 and total_random >= 100
    results["g1"] = {
        "pass": g1_pass,
        "total": total,
        "need_count": total_need,
        "random_count": total_random,
        "threshold": ">= 200 total, >= 100 per group",
    }

    # G2: Mann-Whitney U test + Cliff's delta
    if SCIPY_AVAILABLE:
        stat, p_value = mannwhitneyu(need_pulls, random_pulls, alternative="two-sided")
    else:
        stat, p_value = mann_whitney_u_manual(need_pulls, random_pulls)

    cd = cliffs_delta(need_pulls, random_pulls)
    g2_pass = p_value < 0.05 and cd > 0.147
    results["g2"] = {
        "pass": g2_pass,
        "p_value": p_value,
        "cliffs_delta": cd,
        "threshold": "p < 0.05, Cliff's delta > 0.147",
        "need_median": median(need_pulls) if need_pulls else 0,
        "random_median": median(random_pulls) if random_pulls else 0,
    }

    # G3: Wilson CI95 lower bound for proportion of need-related above random median
    if random_pulls:
        random_med = median(random_pulls)
        need_above = sum(1 for p in need_pulls if p > random_med)
        total_need = len(need_pulls)
        wilson_lb = wilson_ci_lower(need_above, total_need)
        g3_pass = wilson_lb > 0.60
    else:
        random_med = 0
        need_above = 0
        total_need = len(need_pulls)
        wilson_lb = 0.0
        g3_pass = False

    results["g3"] = {
        "pass": g3_pass,
        "wilson_lb": wilson_lb,
        "need_above_median": need_above,
        "total_need": total_need,
        "random_median": random_med,
        "threshold": "Wilson CI95 LB > 0.60",
    }

    # G4: Both categories represented
    g4_pass = total_need > 0 and total_random > 0
    results["g4"] = {
        "pass": g4_pass,
        "need_count": total_need,
        "random_count": total_random,
        "threshold": "need-related > 0 AND random > 0",
    }

    results["all_pass"] = all(r["pass"] for r in results.values())
    return results


def main():
    input_path = Path(__file__).parent / "classified_data.json"
    with open(input_path) as f:
        data = json.load(f)

    analysis_repos = data["analysis_set"]

    # Extract pull counts
    need_pulls = []
    random_pulls = []

    for repo in analysis_repos:
        pulls = repo.get("pull_count", 0)
        if repo in data["classified"]["need-related"]:
            need_pulls.append(pulls)
        elif repo in data["classified"]["random"]:
            random_pulls.append(pulls)

    print("E111 — Gate Evaluation")
    print("=" * 50)
    print(f"Need-related count: {len(need_pulls)}")
    print(f"Random count: {len(random_pulls)}")

    if need_pulls:
        print(f"Need pulls: median={median(need_pulls)}, mean={sum(need_pulls)/len(need_pulls):.0f}")
    if random_pulls:
        print(f"Random pulls: median={median(random_pulls)}, mean={sum(random_pulls)/len(random_pulls):.0f}")

    # Evaluate gates
    gate_results = evaluate_gates(need_pulls, random_pulls)

    print("\nGate Results:")
    for gate, result in gate_results.items():
        if gate == "all_pass":
            continue
        status = "PASS" if result["pass"] else "FAIL"
        print(f"  {gate.upper()}: {status}")
        for k, v in result.items():
            if k != "pass":
                print(f"    {k}: {v}")

    print(f"\nALL GATES PASS: {gate_results['all_pass']}")

    # Full results
    output = {
        "experiment": "E111",
        "platform": "Docker Hub",
        "metric": "pull_count",
        "classified_counts": data["counts"],
        "analysis_counts": {
            "need-related": len(need_pulls),
            "random": len(random_pulls),
        },
        "pull_counts": {
            "need-related": {
                "median": median(need_pulls) if need_pulls else 0,
                "mean": sum(need_pulls) / len(need_pulls) if need_pulls else 0,
                "values": need_pulls,
            },
            "random": {
                "median": median(random_pulls) if random_pulls else 0,
                "mean": sum(random_pulls) / len(random_pulls) if random_pulls else 0,
                "values": random_pulls,
            },
        },
        "gates": gate_results,
        "verdict": "ALL GATES PASS — Principle supported on Docker Hub" if gate_results["all_pass"] else "GATES FAILED — Principle not supported on Docker Hub",
    }

    out_path = Path(__file__).parent / "results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    main()
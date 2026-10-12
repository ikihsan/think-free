#!/usr/bin/env python3
"""E110 — Analyze RubyGems data and evaluate gates."""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple


def load_data() -> List[Dict]:
    """Load collected package data."""
    with open("raw/collected.json") as f:
        data = json.load(f)
    return data["packages"]


def is_active(pkg: Dict) -> bool:
    """Check if package has version_downloads > 0."""
    return pkg.get("downloads_version", 0) > 0


def mann_whitney_u(need_vals: List[int], random_vals: List[int]) -> Tuple[float, float, float]:
    """Mann-Whitney U test. Returns (U, p_value, cliff_delta)."""
    # Combine and rank
    combined = [(v, "need") for v in need_vals] + [(v, "random") for v in random_vals]
    combined.sort(key=lambda x: x[0])

    # Assign ranks (average for ties)
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    # Sum ranks for need group
    n1 = len(need_vals)
    n2 = len(random_vals)
    r1 = sum(ranks[i] for i in range(n1))

    # U statistic
    u1 = r1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    # Normal approximation for p-value
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if std_u == 0:
        return u, 1.0, 0.0
    z = (u - mean_u) / std_u

    # Two-tailed p-value
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))

    # Cliff's delta
    # delta = (num_need_greater - num_random_greater) / (n1 * n2)
    greater = sum(1 for nv in need_vals for rv in random_vals if nv > rv)
    less = sum(1 for nv in need_vals for rv in random_vals if nv < rv)
    cliff_delta = (greater - less) / (n1 * n2) if n1 * n2 > 0 else 0.0

    return u, p, cliff_delta


def wilson_ci95_lower(x: int, n: int) -> float:
    """Wilson CI95 lower bound for proportion x/n."""
    if n == 0:
        return 0.0
    z = 1.96
    phat = x / n
    denominator = 1 + z**2 / n
    centre = phat + z**2 / (2 * n)
    margin = z * math.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    return max(0, (centre - margin) / denominator)


def evaluate_gates(packages: List[Dict]) -> Dict:
    """Evaluate G1-G4 gates."""
    # Classify
    need_pkgs = [p for p in packages if p["classification"] == "need-related"]
    random_pkgs = [p for p in packages if p["classification"] == "random"]

    # Active counts
    need_active = sum(1 for p in need_pkgs if is_active(p))
    random_active = sum(1 for p in random_pkgs if is_active(p))

    need_total = len(need_pkgs)
    random_total = len(random_pkgs)
    classified_total = need_total + random_total

    need_rate = need_active / need_total if need_total > 0 else 0
    random_rate = random_active / random_total if random_total > 0 else 0

    # G1: classified sample size >= 100
    g1_pass = classified_total >= 100

    # G2: Mann-Whitney U test p < 0.05, Cliff's delta > 0.147
    need_downloads = [p["downloads_version"] for p in need_pkgs]
    random_downloads = [p["downloads_version"] for p in random_pkgs]
    u_stat, p_val, cliff_delta = mann_whitney_u(need_downloads, random_downloads)
    g2_pass = (p_val < 0.05) and (cliff_delta > 0.147)

    # G3: Wilson CI95 lower bound for proportion of need-related above random median > 0.60
    if random_downloads:
        random_median = sorted(random_downloads)[len(random_downloads) // 2]
    else:
        random_median = 0
    need_above_median = sum(1 for v in need_downloads if v > random_median)
    wilson_lb = wilson_ci95_lower(need_above_median, need_total)
    g3_pass = wilson_lb > 0.60

    # G4: both categories represented
    g4_pass = need_total > 0 and random_total > 0

    return {
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "all_pass": g1_pass and g2_pass and g3_pass and g4_pass,
        "statistics": {
            "classified_total": classified_total,
            "need_total": need_total,
            "random_total": random_total,
            "need_active": need_active,
            "random_active": random_active,
            "need_rate": need_rate,
            "random_rate": random_rate,
            "u_statistic": u_stat,
            "p_value": p_val,
            "cliff_delta": cliff_delta,
            "random_median": random_median,
            "need_above_median": need_above_median,
            "wilson_lb": wilson_lb,
        }
    }


def main():
    print("=== E110 RubyGems View-Count Gate Evaluation ===\n")

    packages = load_data()
    print(f"Loaded {len(packages)} packages")

    results = evaluate_gates(packages)

    stats = results["statistics"]
    print(f"\n--- Classification ---")
    print(f"  Need-related: {stats['need_total']}")
    print(f"  Random: {stats['random_total']}")
    print(f"  Total classified: {stats['classified_total']}")

    print(f"\n--- Activity (version_downloads > 0) ---")
    print(f"  Need-related active: {stats['need_active']}/{stats['need_total']} = {stats['need_rate']:.1%}")
    print(f"  Random active: {stats['random_active']}/{stats['random_total']} = {stats['random_rate']:.1%}")

    print(f"\n--- Gates ---")
    print(f"  G1 (sample >= 100): {'PASS' if results['g1_pass'] else 'FAIL'} ({stats['classified_total']})")
    print(f"  G2 (MWU p<0.05, delta>0.147): {'PASS' if results['g2_pass'] else 'FAIL'} (p={stats['p_value']:.6f}, delta={stats['cliff_delta']:.4f})")
    print(f"  G3 (Wilson LB > 0.60): {'PASS' if results['g3_pass'] else 'FAIL'} (LB={stats['wilson_lb']:.4f}, need_above_median={stats['need_above_median']}/{stats['need_total']}, random_median={stats['random_median']})")
    print(f"  G4 (both categories): {'PASS' if results['g4_pass'] else 'FAIL'}")

    print(f"\n--- Overall: {'ALL GATES PASS' if results['all_pass'] else 'SOME GATES FAILED'} ---")

    # Save results
    output = {
        "experiment": "E110",
        "platform": "RubyGems",
        "gates": results,
        "conclusion": "view-count principle supported on RubyGems" if results["all_pass"] else "view-count principle not supported on RubyGems",
    }

    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nResults saved to results.json")


if __name__ == "__main__":
    main()
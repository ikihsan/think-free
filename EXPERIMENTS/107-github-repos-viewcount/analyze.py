#!/usr/bin/env python3
"""E107 — Analyze GitHub repositories for view-count principle gates"""
import json
import os
import math
from typing import List, Dict, Tuple

def wilson_ci_lower(p: float, n: int, z: float = 1.96) -> float:
    """Wilson score interval lower bound at 95% confidence."""
    if n == 0:
        return 0.0
    denominator = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    adjustment = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (centre - adjustment) / denominator


def mann_whitney_u(group1: List[float], group2: List[float]) -> Tuple[float, float]:
    """Mann-Whitney U test. Returns (U statistic, p-value approximation)."""
    # Combine and rank
    combined = [(v, 0) for v in group1] + [(v, 1) for v in group2]
    combined.sort(key=lambda x: x[0])
    
    # Assign ranks (handling ties)
    ranks = []
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        # Average rank for ties
        avg_rank = (i + 1 + j) / 2
        for k in range(i, j):
            ranks.append((combined[k][1], avg_rank))
        i = j
    
    # Sum ranks for group 0
    n1 = len(group1)
    n2 = len(group2)
    rank_sum_1 = sum(r for g, r in ranks if g == 0)
    
    # U statistic
    u1 = rank_sum_1 - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation for p-value (valid for n1,n2 > 20)
    mean_u = n1 * n2 / 2
    std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    
    if std_u == 0:
        return u, 1.0
    
    z = (u - mean_u) / std_u
    # Two-tailed p-value
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    
    return u, p


def cliffs_delta(group1: List[float], group2: List[float]) -> float:
    """Cliff's delta effect size."""
    n1, n2 = len(group1), len(group2)
    if n1 == 0 or n2 == 0:
        return 0.0
    
    greater = 0
    less = 0
    for x in group1:
        for y in group2:
            if x > y:
                greater += 1
            elif x < y:
                less += 1
    
    return (greater - less) / (n1 * n2)


def main():
    # Load raw data
    raw_path = "EXPERIMENTS/107-github-repos-viewcount/raw_data.json"
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found. Run harvest.py first.")
        return 1
    
    with open(raw_path) as f:
        all_repos = json.load(f)
    
    print("=== E107 — Gate Evaluation ===")
    print(f"Total repositories loaded: {len(all_repos)}")
    
    # Filter to classified repositories
    need_related = [r for r in all_repos if r["classification"] == "need-related"]
    random_repos = [r for r in all_repos if r["classification"] == "random"]
    ambiguous = [r for r in all_repos if r["classification"] == "ambiguous"]
    
    print(f"Need-related: {len(need_related)}")
    print(f"Random: {len(random_repos)}")
    print(f"Ambiguous: {len(ambiguous)}")
    
    if len(need_related) == 0 or len(random_repos) == 0:
        print("ERROR: One or both groups empty!")
        return 1
    
    # Activity metrics
    def is_active(repo: Dict) -> bool:
        stars = repo.get("stargazers_count", 0)
        # Check if pushed in last 365 days
        pushed_at = repo.get("pushed_at", "")
        recent = False
        if pushed_at:
            try:
                from datetime import datetime, timezone
                pushed = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                recent = (now - pushed).days <= 365
            except:
                pass
        return stars > 0 and recent
    
    # Star counts
    need_stars = [r.get("stargazers_count", 0) for r in need_related]
    random_stars = [r.get("stargazers_count", 0) for r in random_repos]
    
    # Active status
    need_active = sum(1 for r in need_related if is_active(r))
    random_active = sum(1 for r in random_repos if is_active(r))
    
    need_active_rate = need_active / len(need_related)
    random_active_rate = random_active / len(random_repos)
    
    print(f"\nActivity rates (stars>0 & pushed≤365d):")
    print(f"  Need-related: {need_active}/{len(need_related)} = {need_active_rate:.3f}")
    print(f"  Random: {random_active}/{len(random_repos)} = {random_active_rate:.3f}")
    
    # Gate G1: Sample size
    total_classified = len(need_related) + len(random_repos)
    g1_pass = total_classified >= 100 and len(need_related) >= 50 and len(random_repos) >= 50
    print(f"\nG1 - Classified sample size ≥ 100 (50 per group): {'PASS' if g1_pass else 'FAIL'}")
    print(f"  Total classified: {total_classified} (need: {len(need_related)}, random: {len(random_repos)})")
    
    # Gate G2: Mann-Whitney U test on star counts
    u_stat, p_value = mann_whitney_u(need_stars, random_stars)
    delta = cliffs_delta(need_stars, random_stars)
    g2_pass = p_value < 0.05 and delta > 0.147
    print(f"\nG2 - Mann-Whitney U test (p<0.05, Cliff's δ>0.147): {'PASS' if g2_pass else 'FAIL'}")
    print(f"  U statistic: {u_stat:.1f}")
    print(f"  p-value: {p_value:.6f}")
    print(f"  Cliff's delta: {delta:.4f}")
    print(f"  Need median stars: {sorted(need_stars)[len(need_stars)//2]}")
    print(f"  Random median stars: {sorted(random_stars)[len(random_stars)//2]}")
    
    # Gate G3: Wilson CI95 lower bound for proportion above random median
    random_median = sorted(random_stars)[len(random_stars)//2]
    need_above_median = sum(1 for s in need_stars if s > random_median)
    prop_above = need_above_median / len(need_stars)
    wilson_lb = wilson_ci_lower(prop_above, len(need_stars))
    g3_pass = wilson_lb > 0.60
    print(f"\nG3 - Wilson CI95 LB for proportion above random median > 0.60: {'PASS' if g3_pass else 'FAIL'}")
    print(f"  Random median: {random_median}")
    print(f"  Need above median: {need_above_median}/{len(need_stars)} = {prop_above:.3f}")
    print(f"  Wilson CI95 lower bound: {wilson_lb:.4f}")
    
    # Gate G4: Both categories represented
    g4_pass = len(need_related) > 0 and len(random_repos) > 0
    print(f"\nG4 - Both categories represented: {'PASS' if g4_pass else 'FAIL'}")
    print(f"  Need-related: {len(need_related)}, Random: {len(random_repos)}")
    
    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    verdict = "ALL GATES PASS — Principle supported on GitHub repositories" if all_pass else "SOME GATES FAILED — Principle not supported"
    print(f"\n=== Overall: {verdict} ===")
    
    # Detailed results for each repo
    results = {
        "experiment": "E107",
        "platform": "GitHub code repositories",
        "metric": "stargazers_count",
        "total_harvested": len(all_repos),
        "classified": {
            "need-related": len(need_related),
            "random": len(random_repos),
            "ambiguous": len(ambiguous),
        },
        "active_rates": {
            "need-related": need_active_rate,
            "random": random_active_rate,
        },
        "star_counts": {
            "need-related": {
                "median": sorted(need_stars)[len(need_stars)//2],
                "mean": sum(need_stars) / len(need_stars),
                "values": need_stars,
            },
            "random": {
                "median": sorted(random_stars)[len(random_stars)//2],
                "mean": sum(random_stars) / len(random_stars),
                "values": random_stars,
            },
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g2_p_value": p_value,
        "g2_cliffs_delta": delta,
        "g3_pass": g3_pass,
        "g3_prop_above_median": prop_above,
        "g3_wilson_lb": wilson_lb,
        "g4_pass": g4_pass,
        "all_pass": all_pass,
        "verdict": verdict,
        "conclusion": "Principle supported on GitHub repositories" if all_pass else "Principle does not generalize to GitHub repositories",
    }
    
    # Save results
    os.makedirs("EXPERIMENTS/107-github-repos-viewcount", exist_ok=True)
    with open("EXPERIMENTS/107-github-repos-viewcount/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to EXPERIMENTS/107-github-repos-viewcount/results.json")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
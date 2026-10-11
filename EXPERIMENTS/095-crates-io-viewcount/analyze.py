#!/usr/bin/env python3
"""
E095: crates.io view-count principle test - Analysis (stdlib only)
Analyzes collected data to test the view-count principle.
"""

import json
import math
from pathlib import Path
from typing import List, Dict, Tuple

RAW_DIR = Path("EXPERIMENTS/095-crates-io-viewcount/raw")
OUTPUT_DIR = Path("EXPERIMENTS/095-crates-io-viewcount")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> Tuple[List[Dict], List[Dict]]:
    """Load need-related and random crates from raw data."""
    with open(RAW_DIR / "crates_data_v3.json") as f:
        data = json.load(f)
    return data["need_related"], data["random"]


def is_active(crate: Dict) -> bool:
    """Check if crate is 'active' (recent_downloads > 0)."""
    return crate.get("recent_downloads", 0) > 0


def normal_cdf(x: float) -> float:
    """Standard normal CDF approximation."""
    # Abramowitz and Stegun approximation
    t = 1.0 / (1.0 + 0.2316419 * abs(x))
    d = 0.3989423 * math.exp(-x * x / 2.0)
    prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    return 1.0 - prob if x >= 0 else prob


def proportion_test(need_active: int, need_total: int, rand_active: int, rand_total: int) -> Dict:
    """Two-sample proportion z-test."""
    p1 = need_active / need_total
    p2 = rand_active / rand_total
    p_pool = (need_active + rand_active) / (need_total + rand_total)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/need_total + 1/rand_total))
    z = (p1 - p2) / se if se > 0 else 0
    p_value = 2 * normal_cdf(-abs(z))
    
    # Wilson CI for need-related proportion
    z_alpha = 1.96  # 95% CI
    denom = 1 + z_alpha**2 / need_total
    center = (p1 + z_alpha**2 / (2 * need_total)) / denom
    margin = (z_alpha / denom) * math.sqrt(p1 * (1 - p1) / need_total + z_alpha**2 / (4 * need_total**2))
    ci_low = center - margin
    ci_high = center + margin
    
    return {
        "need_active_rate": p1,
        "random_active_rate": p2,
        "difference": p1 - p2,
        "z_score": z,
        "p_value": p_value,
        "wilson_ci_need": [ci_low, ci_high],
        "wilson_ci_lower_bound": ci_low,
    }


def mannwhitney_test(need_values: List[float], rand_values: List[float]) -> Dict:
    """Mann-Whitney U test for continuous downloads (log scale)."""
    # Filter out zeros for log comparison
    need_nonzero = [v for v in need_values if v > 0]
    rand_nonzero = [v for v in rand_values if v > 0]
    
    if len(need_nonzero) < 3 or len(rand_nonzero) < 3:
        return {"error": "Insufficient non-zero values"}
    
    # Test on log values
    need_log = [math.log(v) for v in need_nonzero]
    rand_log = [math.log(v) for v in rand_nonzero]
    
    # Combine and rank
    combined = [(v, 0) for v in need_log] + [(v, 1) for v in rand_log]
    combined.sort(key=lambda x: x[0])
    
    # Assign ranks (handle ties)
    ranks = {}
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        # Average rank for ties
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    
    # Sum of ranks for need group
    need_rank_sum = sum(ranks[k] for k, (_, g) in enumerate(combined) if g == 0)
    
    n1 = len(need_log)
    n2 = len(rand_log)
    
    # U statistic
    u1 = need_rank_sum - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation for p-value
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (u - mu) / sigma if sigma > 0 else 0
    p_value = 2 * normal_cdf(-abs(z))
    
    # Rank-biserial correlation (effect size)
    r = 1 - (2 * u) / (n1 * n2)
    
    return {
        "need_nonzero_count": n1,
        "random_nonzero_count": n2,
        "need_log_mean": sum(need_log) / n1 if n1 else 0,
        "random_log_mean": sum(rand_log) / n2 if n2 else 0,
        "u_statistic": u,
        "p_value": p_value,
        "rank_biserial_r": r,
    }


def evaluate_gates(need_crates: List[Dict], random_crates: List[Dict], prop_result: Dict, mw_result: Dict) -> Dict:
    """Evaluate the four gates."""
    
    # G1: Sample size
    g1_pass = len(need_crates) >= 100 and len(random_crates) >= 100
    
    # G2: Significance (p < 0.05 for either test)
    g2_pass = False
    if "p_value" in prop_result:
        g2_pass = g2_pass or prop_result["p_value"] < 0.05
    if "p_value" in mw_result and "error" not in mw_result:
        g2_pass = g2_pass or mw_result["p_value"] < 0.05
    
    # G3: Effect size
    g3_pass = False
    if "wilson_ci_lower_bound" in prop_result:
        g3_pass = g3_pass or prop_result["wilson_ci_lower_bound"] > 0.60
    if "rank_biserial_r" in mw_result and "error" not in mw_result:
        g3_pass = g3_pass or abs(mw_result["rank_biserial_r"]) > 0.3
    
    # G4: Arrival field rate (download metadata available)
    need_with_downloads = sum(1 for c in need_crates if "downloads" in c and "recent_downloads" in c)
    rand_with_downloads = sum(1 for c in random_crates if "downloads" in c and "recent_downloads" in c)
    g4_need_rate = need_with_downloads / len(need_crates) if need_crates else 0
    g4_rand_rate = rand_with_downloads / len(random_crates) if random_crates else 0
    g4_pass = g4_need_rate >= 0.95 and g4_rand_rate >= 0.95
    
    return {
        "G1_sample_size": {"pass": g1_pass, "need_n": len(need_crates), "random_n": len(random_crates), "threshold": ">= 100 each"},
        "G2_significance": {"pass": g2_pass, "prop_p": prop_result.get("p_value"), "mw_p": mw_result.get("p_value"), "threshold": "p < 0.05"},
        "G3_effect_size": {"pass": g3_pass, "wilson_lb": prop_result.get("wilson_ci_lower_bound"), "rank_biserial": mw_result.get("rank_biserial_r"), "threshold": "Wilson LB > 0.60 or |r| > 0.3"},
        "G4_arrival_field": {"pass": g4_pass, "need_rate": g4_need_rate, "random_rate": g4_rand_rate, "threshold": ">= 95%"},
    }


def median(lst: List[float]) -> float:
    """Compute median."""
    if not lst:
        return 0
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    if n % 2 == 0:
        return (sorted_lst[n//2 - 1] + sorted_lst[n//2]) / 2
    return sorted_lst[n//2]


def main():
    print("=" * 60)
    print("E095: crates.io view-count principle test - Analysis")
    print("=" * 60)
    
    need_crates, random_crates = load_data()
    
    print(f"\nNeed-related crates: {len(need_crates)}")
    print(f"Random crates: {len(random_crates)}")
    
    # Activity analysis
    need_active = sum(1 for c in need_crates if is_active(c))
    random_active = sum(1 for c in random_crates if is_active(c))
    
    print(f"\nActivity (recent_downloads > 0):")
    print(f"  Need-related: {need_active}/{len(need_crates)} = {need_active/len(need_crates):.4f}")
    print(f"  Random: {random_active}/{len(random_crates)} = {random_active/len(random_crates):.4f}")
    
    # Proportion test
    prop_result = proportion_test(need_active, len(need_crates), random_active, len(random_crates))
    print(f"\nProportion test:")
    print(f"  Need active rate: {prop_result['need_active_rate']:.4f}")
    print(f"  Random active rate: {prop_result['random_active_rate']:.4f}")
    print(f"  Difference: {prop_result['difference']:.4f}")
    print(f"  z-score: {prop_result['z_score']:.4f}")
    print(f"  p-value: {prop_result['p_value']:.6f}")
    print(f"  Wilson CI95 for need: [{prop_result['wilson_ci_need'][0]:.4f}, {prop_result['wilson_ci_need'][1]:.4f}]")
    print(f"  Wilson CI95 lower bound: {prop_result['wilson_ci_lower_bound']:.4f}")
    
    # Continuous download analysis
    need_downloads = [c.get("downloads", 0) for c in need_crates]
    random_downloads = [c.get("downloads", 0) for c in random_crates]
    need_recent = [c.get("recent_downloads", 0) for c in need_crates]
    random_recent = [c.get("recent_downloads", 0) for c in random_crates]
    
    print(f"\nTotal downloads (all):")
    print(f"  Need median: {median(need_downloads)}")
    print(f"  Random median: {median(random_downloads)}")
    
    print(f"\nRecent downloads (all):")
    print(f"  Need median: {median(need_recent)}")
    print(f"  Random median: {median(random_recent)}")
    
    # Mann-Whitney on total downloads
    mw_total = mannwhitney_test(need_downloads, random_downloads)
    print(f"\nMann-Whitney U test (total downloads, log scale):")
    if "error" not in mw_total:
        print(f"  Need non-zero: {mw_total['need_nonzero_count']}")
        print(f"  Random non-zero: {mw_total['random_nonzero_count']}")
        print(f"  Need log mean: {mw_total['need_log_mean']:.2f}")
        print(f"  Random log mean: {mw_total['random_log_mean']:.2f}")
        print(f"  U statistic: {mw_total['u_statistic']:.0f}")
        print(f"  p-value: {mw_total['p_value']:.6f}")
        print(f"  Rank-biserial r: {mw_total['rank_biserial_r']:.4f}")
    else:
        print(f"  {mw_total['error']}")
    
    # Mann-Whitney on recent downloads
    mw_recent = mannwhitney_test(need_recent, random_recent)
    print(f"\nMann-Whitney U test (recent downloads, log scale):")
    if "error" not in mw_recent:
        print(f"  Need non-zero: {mw_recent['need_nonzero_count']}")
        print(f"  Random non-zero: {mw_recent['random_nonzero_count']}")
        print(f"  Need log mean: {mw_recent['need_log_mean']:.2f}")
        print(f"  Random log mean: {mw_recent['random_log_mean']:.2f}")
        print(f"  U statistic: {mw_recent['u_statistic']:.0f}")
        print(f"  p-value: {mw_recent['p_value']:.6f}")
        print(f"  Rank-biserial r: {mw_recent['rank_biserial_r']:.4f}")
    else:
        print(f"  {mw_recent['error']}")
    
    # Evaluate gates
    gates = evaluate_gates(need_crates, random_crates, prop_result, mw_recent)
    print(f"\n{'='*60}")
    print("GATE EVALUATION")
    print(f"{'='*60}")
    for gate_name, gate_result in gates.items():
        status = "PASS" if gate_result["pass"] else "FAIL"
        print(f"\n{gate_name}: {status}")
        for k, v in gate_result.items():
            if k != "pass":
                print(f"  {k}: {v}")
    
    all_pass = all(g["pass"] for g in gates.values())
    print(f"\n{'='*60}")
    print(f"OVERALL: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'}")
    print(f"{'='*60}")
    
    # Save results
    results = {
        "need_count": len(need_crates),
        "random_count": len(random_crates),
        "need_active": need_active,
        "random_active": random_active,
        "proportion_test": prop_result,
        "mannwhitney_total": mw_total,
        "mannwhitney_recent": mw_recent,
        "gates": gates,
        "all_gates_pass": all_pass,
    }
    
    with open(OUTPUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to {OUTPUT_DIR / 'results.json'}")


if __name__ == "__main__":
    main()
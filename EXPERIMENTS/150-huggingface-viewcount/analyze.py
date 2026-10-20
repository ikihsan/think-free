#!/usr/bin/env python3
"""
Statistical analysis of need-related vs general models on Hugging Face.
Computes Cliff's delta, Mann-Whitney U, and other effect size measures.
"""
import json
import sys
import math
from typing import List, Tuple

def cliffs_delta(group1: List[float], group2: List[float]) -> float:
    """
    Compute Cliff's delta effect size using sorting for O(n log n) performance.
    Delta = (number of pairs where g1 > g2 - number where g1 < g2) / (n1 * n2)
    Range: -1 to 1. Positive means group1 tends to be larger.
    """
    if not group1 or not group2:
        return 0.0
    
    # Sort both groups
    g1_sorted = sorted(group1)
    g2_sorted = sorted(group2)
    n1, n2 = len(g1_sorted), len(g2_sorted)
    
    # Count pairs where g1 > g2 using two-pointer technique
    greater = 0
    j = 0
    for x in g1_sorted:
        while j < n2 and g2_sorted[j] < x:
            j += 1
        greater += j
    
    # Count pairs where g1 < g2
    less = 0
    j = 0
    for y in g2_sorted:
        while j < n1 and g1_sorted[j] < y:
            j += 1
        less += j
    
    return (greater - less) / (n1 * n2)


def mann_whitney_u(group1: List[float], group2: List[float]) -> Tuple[float, float]:
    """
    Compute Mann-Whitney U statistic and p-value (normal approximation).
    Returns (U, p_value).
    """
    if not group1 or not group2:
        return 0.0, 1.0
    
    n1, n2 = len(group1), len(group2)
    
    # Combine and rank
    combined = [(x, 0) for x in group1] + [(y, 1) for y in group2]
    combined.sort(key=lambda x: x[0])
    
    # Handle ties
    ranks = [0] * (n1 + n2)
    i = 0
    while i < n1 + n2:
        j = i
        while j < n1 + n2 and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j
    
    # Sum ranks for group1
    r1 = sum(ranks[k] for k, (_, g) in enumerate(combined) if g == 0)
    
    # U statistic
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    
    # Normal approximation for p-value
    mu = n1 * n2 / 2.0
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12.0)
    
    # Tie correction
    tie_correction = 0.0
    i = 0
    while i < n1 + n2:
        j = i
        while j < n1 + n2 and combined[j][0] == combined[i][0]:
            j += 1
        t = j - i
        if t > 1:
            tie_correction += t * (t - 1) * (t + 1)
        i = j
    
    if tie_correction > 0:
        sigma = math.sqrt(n1 * n2 / 12.0 * ((n1 + n2 + 1) - tie_correction / (n1 + n2) / (n1 + n2 - 1)))
    
    if sigma == 0:
        return u, 1.0
    
    z = (u - mu) / sigma
    # Two-tailed p-value
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    
    return u, p


def bootstrap_ci(data1: List[float], data2: List[float], n_bootstrap: int = 200) -> Tuple[float, float]:
    """Bootstrap confidence interval for Cliff's delta."""
    import random
    deltas = []
    combined1 = data1[:]
    combined2 = data2[:]
    for _ in range(n_bootstrap):
        sample1 = [random.choice(combined1) for _ in combined1]
        sample2 = [random.choice(combined2) for _ in combined2]
        deltas.append(cliffs_delta(sample1, sample2))
    deltas.sort()
    lower = deltas[int(0.025 * n_bootstrap)]
    upper = deltas[int(0.975 * n_bootstrap)]
    return lower, upper


def shuffle_test(data1: List[float], data2: List[float], n_shuffles: int = 200) -> float:
    """Permutation test: fraction of shuffles with delta >= observed."""
    import random
    observed = cliffs_delta(data1, data2)
    combined = data1 + data2
    n1 = len(data1)
    count = 0
    for _ in range(n_shuffles):
        random.shuffle(combined)
        shuffled1 = combined[:n1]
        shuffled2 = combined[n1:]
        if cliffs_delta(shuffled1, shuffled2) >= observed:
            count += 1
    return count / n_shuffles


def analyze_metric(need_values: List[float], gen_values: List[float], metric_name: str) -> dict:
    """Analyze a single metric."""
    if not need_values or not gen_values:
        return {"metric": metric_name, "error": "Empty group"}
    
    delta = cliffs_delta(need_values, gen_values)
    u, p = mann_whitney_u(need_values, gen_values)
    ci_lower, ci_upper = bootstrap_ci(need_values, gen_values)
    shuffle_p = shuffle_test(need_values, gen_values)
    
    # Medians
    need_median = sorted(need_values)[len(need_values)//2]
    gen_median = sorted(gen_values)[len(gen_values)//2]
    
    # Means
    need_mean = sum(need_values) / len(need_values)
    gen_mean = sum(gen_values) / len(gen_values)
    
    return {
        "metric": metric_name,
        "need_n": len(need_values),
        "general_n": len(gen_values),
        "need_median": need_median,
        "general_median": gen_median,
        "need_mean": need_mean,
        "general_mean": gen_mean,
        "cliffs_delta": delta,
        "mann_whitney_u": u,
        "p_value": p,
        "ci_95_lower": ci_lower,
        "ci_95_upper": ci_upper,
        "shuffle_p": shuffle_p,
    }


def main():
    input_path = "EXPERIMENTS/150-huggingface-viewcount/CLASSIFIED.jsonl"
    
    need_related = []
    general = []
    
    with open(input_path) as f:
        for line in f:
            model = json.loads(line)
            if model.get("_classification") == "need-related":
                need_related.append(model)
            elif model.get("_classification") == "general":
                general.append(model)
    
    print(f"Need-related: {len(need_related)}")
    print(f"General: {len(general)}")
    
    # Extract metrics
    metrics = ["likes", "downloads", "trendingScore"]
    results = {}
    
    for metric in metrics:
        need_vals = [m.get(metric, 0) for m in need_related]
        gen_vals = [m.get(metric, 0) for m in general]
        result = analyze_metric(need_vals, gen_vals, metric)
        results[metric] = result
        
        print(f"\n=== {metric} ===")
        print(f"  Need-related: n={result['need_n']}, median={result['need_median']:.1f}, mean={result['need_mean']:.1f}")
        print(f"  General:      n={result['general_n']}, median={result['general_median']:.1f}, mean={result['general_mean']:.1f}")
        print(f"  Cliff's delta: {result['cliffs_delta']:.4f} (95% CI: [{result['ci_95_lower']:.4f}, {result['ci_95_upper']:.4f}])")
        print(f"  Mann-Whitney U: {result['mann_whitney_u']:.1f}, p={result['p_value']:.6f}")
        print(f"  Shuffle p: {result['shuffle_p']:.4f}")
    
    # Decision based on kill gate
    print("\n=== DECISION ===")
    all_small = all(r['cliffs_delta'] < 0.147 for r in results.values())
    any_medium = any(r['cliffs_delta'] >= 0.33 for r in results.values())
    any_large = any(r['cliffs_delta'] >= 0.474 for r in results.values())
    all_negative = all(r['cliffs_delta'] < -0.147 for r in results.values())
    
    if all_negative:
        decision = "FAIL (direction kill gate: general outperforms need-related)"
    elif all_small:
        decision = "FAIL (primary kill gate: all metrics show negligible effect)"
    elif any_large:
        decision = "PASS (large effect on at least one metric)"
    elif any_medium:
        decision = "PASS (medium effect on at least one metric)"
    else:
        decision = "WEAK (small effect only)"
    
    print(f"Decision: {decision}")
    
    # Write results
    output = {
        "results": results,
        "decision": decision,
        "need_related_count": len(need_related),
        "general_count": len(general),
        "excluded_count": 1900 - len(need_related) - len(general),
    }
    
    with open("EXPERIMENTS/150-huggingface-viewcount/RESULT.json", "w") as f:
        json.dump(output, f, indent=2)
    
    # Write human-readable result
    with open("EXPERIMENTS/150-huggingface-viewcount/RESULT.md", "w") as f:
        f.write("# Experiment 150: Hugging Face Hub View-Count Principle Test\n\n")
        f.write(f"**Decision: {decision}**\n\n")
        f.write(f"Need-related models: {len(need_related)}\n")
        f.write(f"General models: {len(general)}\n")
        f.write(f"Excluded: {1900 - len(need_related) - len(general)}\n\n")
        
        for metric in metrics:
            r = results[metric]
            f.write(f"## {metric}\n\n")
            f.write(f"- Need-related: n={r['need_n']}, median={r['need_median']:.1f}, mean={r['need_mean']:.1f}\n")
            f.write(f"- General: n={r['general_n']}, median={r['general_median']:.1f}, mean={r['general_mean']:.1f}\n")
            f.write(f"- Cliff's delta: **{r['cliffs_delta']:.4f}** (95% CI: [{r['ci_95_lower']:.4f}, {r['ci_95_upper']:.4f}])\n")
            f.write(f"- Mann-Whitney U: {r['mann_whitney_u']:.1f}, p={r['p_value']:.6f}\n")
            f.write(f"- Shuffle test p: {r['shuffle_p']:.4f}\n\n")
        
        f.write("## Interpretation\n\n")
        if "PASS" in decision:
            f.write("Need-related models show systematically higher activity metrics than general foundation models. ")
            f.write("The view-count principle extends to Hugging Face Hub for models.\n")
        elif "WEAK" in decision:
            f.write("Need-related models show a small but detectable activity advantage. ")
            f.write("The effect is present but may not be practically significant.\n")
        else:
            f.write("No meaningful activity advantage detected for need-related models. ")
            f.write("The view-count principle does not extend to Hugging Face Hub models under this classification.\n")


if __name__ == "__main__":
    main()
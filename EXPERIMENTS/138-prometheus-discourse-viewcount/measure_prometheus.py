#!/usr/bin/env python3
"""
Measure gates for Prometheus Discourse experiment with matched harvest design.
"""

import json
import sys
import math
from scipy import stats
import numpy as np


def wilson_ci(count, total, z=1.96):
    """Wilson score interval for binomial proportion."""
    if total == 0:
        return (0.0, 1.0)
    p = count / total
    denominator = 1 + z**2 / total
    centre = (p + z**2 / (2 * total)) / denominator
    half = (z * math.sqrt(p * (1 - p) / total + z**2 / (4 * total**2))) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))


def cliffs_delta(x, y):
    """Cliff's delta effect size."""
    if not x or not y:
        return 0.0
    # Vectorized comparison
    x_arr = np.array(x)
    y_arr = np.array(y)
    greater = np.sum(x_arr[:, None] > y_arr[None, :])
    less = np.sum(x_arr[:, None] < y_arr[None, :])
    total = len(x) * len(y)
    return (greater - less) / total


def mannwhitney_u(x, y):
    """Mann-Whitney U test."""
    if not x or not y:
        return 0.0, 1.0
    u_stat, p_value = stats.mannwhitneyu(x, y, alternative="two-sided")
    return u_stat, p_value


def load_classified(jsonl_path):
    topics = []
    with open(jsonl_path, "r") as f:
        for line in f:
            topics.append(json.loads(line))
    return topics


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 measure_prometheus.py <classified.jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]
    topics = load_classified(input_path)

    print(f"Loaded {len(topics)} topics")

    # G1: View count coverage
    vc_positive = sum(1 for t in topics if t.get("view_count", 0) > 0)
    g1_rate = vc_positive / len(topics) if topics else 0
    g1_pass = g1_rate >= 0.95

    print(f"\nG1: View count > 0: {vc_positive}/{len(topics)} = {g1_rate*100:.1f}% {'PASS' if g1_pass else 'FAIL'}")

    # Split by classification
    need_topics = [t for t in topics if t.get("classification") == "need"]
    random_topics = [t for t in topics if t.get("classification") == "random"]
    excluded_topics = [t for t in topics if t.get("classification") == "excluded"]

    classified_count = len(need_topics) + len(random_topics)
    coverage = classified_count / len(topics) if topics else 0
    need_fraction = len(need_topics) / classified_count if classified_count > 0 else 0

    g2_cov_pass = coverage >= 0.60
    g2_need_pass = need_fraction >= 0.05
    g2_pass = g2_cov_pass and g2_need_pass

    print(f"\nG2: Classifier coverage: {classified_count}/{len(topics)} = {coverage*100:.1f}% {'PASS' if g2_cov_pass else 'FAIL'} (floor: 60%)")
    print(f"    Need fraction: {len(need_topics)}/{classified_count} = {need_fraction*100:.1f}% {'PASS' if g2_need_pass else 'FAIL'} (floor: 5%)")
    print(f"    Excluded: {len(excluded_topics)}")

    # G4: Sample size
    g4_pass = classified_count >= 30
    print(f"\nG4: Classified total: {classified_count} {'PASS' if g4_pass else 'FAIL'} (floor: 30)")

    # G3: Unserved fraction (zero replies)
    need_with_replies = sum(1 for t in need_topics if t.get("reply_count", 0) > 0)
    need_zero_replies = len(need_topics) - need_with_replies
    unserved_rate = need_zero_replies / len(need_topics) if need_topics else 0
    ci_low, ci_high = wilson_ci(need_zero_replies, len(need_topics))
    g3_pass = ci_high < 0.60

    print(f"\nG3: Unserved fraction (zero replies): {need_zero_replies}/{len(need_topics)} = {unserved_rate*100:.1f}%")
    print(f"    Wilson CI95: [{ci_low*100:.1f}%, {ci_high*100:.1f}%] {'PASS' if g3_pass else 'FAIL'} (upper < 60%)")

    # Matched harvest: Cliff's delta on view_count
    print("\n--- Matched Harvest Analysis ---")
    need_views = [t.get("view_count", 0) for t in need_topics]
    random_views = [t.get("view_count", 0) for t in random_topics]

    if need_views and random_views:
        # Pooled matched harvest: sort all classified by view_count, split at median
        all_classified = need_topics + random_topics
        all_classified.sort(key=lambda t: t.get("view_count", 0), reverse=True)
        mid = len(all_classified) // 2
        high_engagement = all_classified[:mid]
        low_engagement = all_classified[mid:]

        high_need = sum(1 for t in high_engagement if t.get("classification") == "need")
        high_random = sum(1 for t in high_engagement if t.get("classification") == "random")
        low_need = sum(1 for t in low_engagement if t.get("classification") == "need")
        low_random = sum(1 for t in low_engagement if t.get("classification") == "random")

        high_need_frac = high_need / (high_need + high_random) if (high_need + high_random) > 0 else 0
        low_need_frac = low_need / (low_need + low_random) if (low_need + low_random) > 0 else 0

        print(f"High engagement half (top {mid}): need={high_need}, random={high_random}, need_frac={high_need_frac*100:.1f}%")
        print(f"Low engagement half (bottom {len(all_classified)-mid}): need={low_need}, random={low_random}, need_frac={low_need_frac*100:.1f}%")

        # Cliff's delta on view_count distributions
        delta = cliffs_delta(need_views, random_views)
        u_stat, p_value = mannwhitney_u(need_views, random_views)

        print(f"\nCliff's delta (need vs random view_count): {delta:.4f}")
        print(f"Mann-Whitney U: U={u_stat:.0f}, p={p_value:.6f}")

        # Active rate
        active_need = sum(1 for t in need_topics if t.get("reply_count", 0) > 0)
        active_rate = active_need / len(need_topics) if need_topics else 0
        print(f"\nActive rate (≥1 reply): {active_need}/{len(need_topics)} = {active_rate*100:.1f}%")

    # Overall result
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass

    result = {
        "experiment": "E138",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_topics": len(topics),
        "classified": classified_count,
        "need_related": len(need_topics),
        "random": len(random_topics),
        "excluded": len(excluded_topics),
        "coverage": coverage,
        "need_fraction": need_fraction,
        "g1": {"rate": g1_rate, "pass": g1_pass},
        "g2": {"coverage": coverage, "need_fraction": need_fraction, "pass": g2_pass},
        "g3": {"unserved_rate": unserved_rate, "ci_low": ci_low, "ci_high": ci_high, "pass": g3_pass},
        "g4": {"classified": classified_count, "pass": g4_pass},
        "matched_harvest": {
            "cliffs_delta": delta if need_views and random_views else None,
            "mannwhitney_p": p_value if need_views and random_views else None,
        },
        "overall": "PASS" if all_pass else "FAIL",
    }

    # Save results
    output_path = input_path.replace("_classified.jsonl", "_results.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n=== OVERALL: {result['overall']} ===")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    import time
    main()
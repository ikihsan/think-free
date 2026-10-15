"""E117: Gate evaluation for view-count classifier prototype v3.

Evaluates all four gates (G1-G4) per the protocol:
- G1: Classified sample size >= 100 total (50 per group minimum)
- G2: Coverage floor >= 80% of representative pool classified
- G3: Effect size — Cliff's delta > 0.147 and Mann-Whitney p < 0.05
- G4: Both categories represented (need-related > 0 AND random > 0)

Uses only Python standard library. No external dependencies.
"""

import math
from typing import Dict, Any, Tuple, Optional


def cliff_delta(x: list, y: list) -> float:
    """Compute Cliff's delta effect size between two independent samples."""
    n_x = len(x)
    n_y = len(y)
    if n_x == 0 or n_y == 0:
        return 0.0
    count = 0
    for xi in x:
        for yi in y:
            if xi > yi:
                count += 1
            elif xi < yi:
                count -= 1
    total_pairs = n_x * n_y
    if total_pairs == 0:
        return 0.0
    delta = (2.0 * count) / total_pairs - 1.0
    return delta


def mann_whitney_u(x: list, y: list) -> Tuple[float, float]:
    """Mann-Whitney U test using standard library only."""
    n_x = len(x)
    n_y = len(y)
    if n_x == 0 or n_y == 0:
        return 0.0, 1.0
    combined = [(val, 0) for val in x] + [(val, 1) for val in y]
    combined.sort(key=lambda t: t[0])
    ranks = [0.0] * (n_x + n_y)
    i = 0
    while i < len(combined):
        val = combined[i][0]
        j = i
        while j < len(combined) and combined[j][0] == val:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[combined[k][1]] = avg_rank
        i = j
    rx = sum(ranks[:n_x])
    ux = rx - n_x * (n_x + 1) / 2.0
    if n_x >= 10 and n_y >= 10:
        mean_u = n_x * n_y / 2.0
        tie_counts = {}
        for val, _ in combined:
            tie_counts[val] = tie_counts.get(val, 0) + 1
        tie_correction = 0.0
        for t in tie_counts.values():
            if t > 1:
                tie_correction += t * (t - 1.0)
        n_total = n_x + n_y
        var_u = (n_x * n_y * (n_total + 1.0) - tie_correction) / 12.0
        if var_u <= 0:
            return ux, 1.0
        z = (ux - mean_u) / var_u ** 0.5
        p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
        p = min(1.0, max(0.0, p))
        return ux, p
    else:
        total_pairs = n_x * n_y
        if total_pairs <= 1000:
            from itertools import combinations
            n_total = n_x + n_y
            extreme_count = 0
            total_permutations = 0
            for combo in combinations(range(n_total), n_x):
                total_permutations += 1
                chosen_ranks = sorted([c + 1 for c in combo])
                rx_enum = sum(chosen_ranks)
                ux_enum = rx_enum - n_x * (n_x + 1) / 2.0
                mean_u = total_pairs / 2.0
                if abs(ux_enum - mean_u) >= abs(ux - mean_u):
                    extreme_count += 1
            if total_permutations > 0:
                p = extreme_count / total_permutations * 2.0
            else:
                p = 1.0
        else:
            p = 1.0
        return ux, p


def run_gates(results: Dict[str, Any]) -> Dict[str, Any]:
    """Run all four gates on the experiment results."""
    classified = results.get("classified", {})
    # Read coverage_rate from top-level or fall back to classified
    coverage_rate = results.get("coverage_rate", classified.get("coverage_rate", 0))
    need_related = classified.get("need_related", 0)
    random_n = classified.get("random", 0)
    pool_size_actual = classified.get("pool_size_actual", 0)

    # G1: Classified sample size >= 100 total (50 per group minimum)
    g1_total = need_related + random_n
    g1_pass = g1_total >= 100
    g1_details = {
        "total_classified": g1_total,
        "threshold": 100,
        "pass": g1_pass,
        "need_50_plus": need_related >= 50,
        "random_50_plus": random_n >= 50,
    } if not g1_pass else {"total_classified": g1_total, "threshold": 100, "pass": True}

    # G2: Coverage floor >= 80% of representative pool classified
    g2_pass = coverage_rate >= 0.8
    g2_details = {
        "coverage_rate": coverage_rate,
        "threshold": 0.8,
        "pass": g2_pass,
    } if not g2_pass else {"coverage_rate": coverage_rate, "threshold": 0.8, "pass": True}

    # G3: Effect size — Cliff's delta > 0.147 and Mann-Whitney p < 0.05
    need_downloads = [p["downloads"] for p in results.get("need_related", [])]
    random_downloads = [p["downloads"] for p in results.get("random", [])]
    g3_pass = False
    g3_details = {}
    if len(need_downloads) > 0 and len(random_downloads) > 0:
        delta = cliff_delta(need_downloads, random_downloads)
        u_stat, p_value = mann_whitney_u(need_downloads, random_downloads)
        g3_pass = (p_value < 0.05) and (abs(delta) > 0.147)
        g3_details = {
            "p_value": float(p_value),
            "cliff_delta": float(delta),
            "threshold_p": 0.05,
            "threshold_delta": 0.147,
            "need_n": len(need_downloads),
            "random_n": len(random_downloads),
            "pass": g3_pass,
        }
    else:
        g3_details = {
            "p_value": None,
            "cliff_delta": None,
            "threshold_p": 0.05,
            "threshold_delta": 0.147,
            "need_n": len(need_downloads),
            "random_n": len(random_downloads),
            "pass": False,
            "reason": "Insufficient sample for effect size measurement",
        }

    # G4: Both categories represented (need-related > 0 AND random > 0)
    g4_pass = need_related > 0 and random_n > 0
    g4_details = {
        "need_related_count": need_related,
        "random_count": random_n,
        "pass": g4_pass,
    } if not g4_pass else {"need_related_count": need_related, "random_count": random_n, "pass": True}

    all_pass = g1_pass and g2_pass and g3_pass and g4_pass

    gate_results = {
        "G1_sample_size": {"pass": g1_pass, **g1_details},
        "G2_coverage_floor": {"pass": g2_pass, **g2_details},
        "G3_effect_size": {"pass": g3_pass, **g3_details},
        "G4_both_categories": {"pass": g4_pass, **g4_details},
        "all_pass": all_pass,
    }
    return gate_results

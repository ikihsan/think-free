#!/usr/bin/env python3
"""
E083 — Measurement and gate evaluation for 3D printer fault codes.
"""

import json
import math
from typing import Any, Dict, List


def wilson_ci95(successes: int, trials: int) -> tuple:
    """Wilson score interval for binomial proportion, 95% CI."""
    if trials == 0:
        return (0.0, 0.0)
    p = successes / trials
    z = 1.96
    denominator = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denominator
    half = z * math.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))


def measure_forum(classified: List[Dict], domain: str) -> Dict:
    """Measure gates for a single forum's classified topics."""
    total = len(classified)
    with_fault = [t for t in classified if t.get("has_fault_indicator")]
    fault_count = len(with_fault)

    # G1: Population (structured cases) - requires reply analysis, not evaluable from title only
    # G2: Fault concentration
    fault_dist = {}
    for t in with_fault:
        ft = t.get("fault_type", "OTHER")
        fault_dist[ft] = fault_dist.get(ft, 0) + 1

    top10_faults = sorted(fault_dist.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_count = sum(c for _, c in top10_faults)
    concentration = top10_count / fault_count if fault_count > 0 else 0.0

    # G3: Printer model coverage for top 10 fault types
    # Store actual model sets for cross-forum aggregation
    models_per_fault = {}
    for ft, _ in top10_faults:
        models = set()
        for t in with_fault:
            if t.get("fault_type") == ft:
                model = t.get("printer_model", "Unknown")
                if model != "Unknown":
                    models.add(model)
        models_per_fault[ft] = models  # Store set, not count

    total_models_top10 = sum(len(m) for m in models_per_fault.values())
    avg_models_per_fault = total_models_top10 / len(top10_faults) if top10_faults else 0

    # view_count validation
    vc_positive = sum(1 for t in classified if t.get("views", 0) > 0)
    vc_rate = vc_positive / total if total > 0 else 0.0

    # Need prevalence (fault indicator rate)
    need_rate = fault_count / total if total > 0 else 0.0

    return {
        "domain": domain,
        "total": total,
        "fault_count": fault_count,
        "fault_distribution": fault_dist,
        "top10_faults": top10_faults,
        "concentration_top10": concentration,
        "models_per_fault": {ft: list(models) for ft, models in models_per_fault.items()},  # Serialize sets as lists
        "avg_models_per_fault": avg_models_per_fault,
        "vc_positive": vc_positive,
        "vc_rate": vc_rate,
        "need_rate": need_rate,
    }


def aggregate_results(results: List[Dict]) -> Dict:
    """Aggregate results across forums and evaluate gates."""
    total = sum(r.get("total", 0) for r in results)
    total_fault = sum(r.get("fault_count", 0) for r in results)

    # Aggregate fault distribution
    agg_fault_dist = {}
    for r in results:
        for ft, count in r.get("fault_distribution", {}).items():
            agg_fault_dist[ft] = agg_fault_dist.get(ft, 0) + count

    top10_faults = sorted(agg_fault_dist.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_count = sum(c for _, c in top10_faults)
    concentration = top10_count / total_fault if total_fault > 0 else 0.0

    # Aggregate model coverage - union of model sets across forums
    models_per_fault_agg = {}
    for ft, _ in top10_faults:
        models = set()
        for r in results:
            # models_per_fault stores lists (serialized from sets)
            model_list = r.get("models_per_fault", {}).get(ft, [])
            models.update(model_list)
        models_per_fault_agg[ft] = len(models)

    total_models_top10 = sum(models_per_fault_agg.values())
    avg_models = total_models_top10 / len(top10_faults) if top10_faults else 0

    # view_count aggregate
    total_vc = sum(r.get("vc_positive", 0) for r in results)
    vc_rate = total_vc / total if total > 0 else 0.0

    # Need prevalence aggregate
    need_rate = total_fault / total if total > 0 else 0.0

    # Gate evaluations
    g1_population = "PENDING"  # Requires reply analysis
    g2_concentration = "PASS" if concentration >= 0.30 else "FAIL"
    g3_coverage = "PASS" if avg_models >= 10 else "FAIL"  # ≥ 10 distinct printer models in top 10 fault types
    g4_specificity = "PENDING"  # Requires manual review of replies
    g5_incumbent = "PENDING"    # Requires manual tool survey

    # G1: ≥ 100 structured cases (not evaluable from title only)
    # G2: Top 10 fault types cover ≥ 30% of cases
    # G3: ≥ 10 distinct printer models in top 10 fault types
    # G4: ≥ 60% name specific replaceable part (requires replies)
    # G5: No free tool covers ≥ 50% of top 10 (manual survey)

    all_gates_pass = (
        g2_concentration == "PASS" and
        g3_coverage == "PASS"
    )  # Only evaluable gates for now

    return {
        "total_topics": total,
        "total_fault_topics": total_fault,
        "fault_distribution": agg_fault_dist,
        "top10_faults": top10_faults,
        "concentration_top10": concentration,
        "models_per_fault_agg": models_per_fault_agg,
        "avg_models_per_fault_top10": avg_models,
        "vc_rate": vc_rate,
        "need_rate": need_rate,
        "gates": {
            "G1_population": g1_population,
            "G2_concentration": g2_concentration,
            "G3_coverage": g3_coverage,
            "G4_specificity": g4_specificity,
            "G5_incumbent_gap": g5_incumbent,
        },
        "all_evaluable_gates_pass": all_gates_pass,
    }


def print_results(results: List[Dict], agg: Dict):
    """Print formatted results."""
    print("\n=== Per-Forum Results ===")
    for r in results:
        print(f"\n{r['domain']}:")
        print(f"  Total: {r['total']}, Fault topics: {r['fault_count']}")
        print(f"  view_count > 0: {r['vc_positive']}/{r['total']} ({r['vc_rate']:.1%})")
        print(f"  Fault rate: {r['need_rate']:.1%}")
        print(f"  Top 10 concentration: {r['concentration_top10']:.1%}")
        print(f"  Avg models per top fault: {r['avg_models_per_fault']:.1f}")
        if r['top10_faults']:
            print(f"  Top faults: {', '.join(f'{ft}({c})' for ft, c in r['top10_faults'][:5])}")

    print("\n=== Aggregate Results ===")
    print(f"Total topics: {agg['total_topics']}")
    print(f"Total fault topics: {agg['total_fault_topics']}")
    print(f"view_count rate: {agg['vc_rate']:.1%}")
    print(f"Fault rate: {agg['need_rate']:.1%}")
    print(f"Top 10 concentration: {agg['concentration_top10']:.1%}")
    print(f"Avg models per top fault: {agg['avg_models_per_fault_top10']:.1f}")
    if 'models_per_fault_agg' in agg:
        print(f"Models per top fault: {agg['models_per_fault_agg']}")

    print("\nGate Evaluations:")
    for gate, status in agg['gates'].items():
        print(f"  {gate}: {status}")

    print(f"\nAll evaluable gates pass: {agg['all_evaluable_gates_pass']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 measure.py <classified.jsonl> [domain]")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        classified = [json.loads(line) for line in f]

    domain = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    result = measure_forum(classified, domain)
    agg = aggregate_results([result])
    print_results([result], agg)
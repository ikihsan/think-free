#!/usr/bin/env python3
"""E086 outcome: report view-count arrival metrics.

Reports the distribution of search result counts (arrival counts) across
need statements, without any classify_served classification or discrimination
test. This is a fresh observation of the view-count principle's core metric.

Usage:
    python3 outcome.py     # report arrival count distributions
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Corpus paths
TREATMENT_RESULTS = os.path.join(HERE, "raw", "treatment-results.jsonl")
CONTROL_RESULTS = os.path.join(HERE, "raw", "control-results.jsonl")


def load_results(path):
    """Load results from a JSONL file."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results


def evaluate_gates():
    """Evaluate arrival count distributions and print verdicts."""
    treatment = load_results(TREATMENT_RESULTS)
    control = load_results(CONTROL_RESULTS)
    
    print(f"Treatment results: {len(treatment)} statements")
    print(f"Control results: {len(control)} statements\n")
    
    # G1 retrieval: >= 30 need statements harvested, each yielding web search results
    t_g1 = "PASS" if len(treatment) >= 30 else "FAIL"
    c_g1 = "PASS" if len(control) >= 30 else "FAIL"
    print(f"G1 retrieval:")
    print(f"  Treatment: {t_g1} ({len(treatment)} >= 30)")
    print(f"  Control: {c_g1} ({len(control)} >= 30)")
    
    if t_g1 == "FAIL" or c_g1 == "FAIL":
        print(f"\nG1 FAIL — stopping gate evaluation.")
        return
    
    # Compute arrival count distributions
    # For each statement, we have num_results from the harvest
    t_num_results = [r['num_results'] for r in treatment]
    c_num_results = [r['num_results'] for r in control]
    
    # Distribution of num_results buckets
    def bucket(n):
        """Categorize num_results into buckets."""
        if n <= 0:
            return '0'
        elif n == 1:
            return '1'
        elif n == 2:
            return '2'
        elif n == 3:
            return '3'
        elif n <= 5:
            return '4-5'
        elif n <= 10:
            return '6-10'
        else:
            return '11+'
    
    t_buckets = [bucket(n) for n in t_num_results]
    c_buckets = [bucket(n) for n in c_num_results]
    
    # Count frequencies
    from collections import Counter
    t_bucket_counts = Counter(t_buckets)
    c_bucket_counts = Counter(c_buckets)
    
    # G3 measurement: fraction of need statements yielding >=k search results
    print(f"\n--- G3: Arrival count distribution ---")
    
    # Fractions yielding at least k results
    for k in [1, 2, 3, 5, 10]:
        t_at_least_k = sum(1 for n in t_num_results if n >= k) / len(t_num_results) if t_num_results else 0
        c_at_least_k = sum(1 for n in c_num_results if n >= k) / len(c_num_results) if c_num_results else 0
        print(f"  Yielding ≥{k} search result:")
        print(f"    Treatment: {t_at_least_k:.3f} ({sum(1 for n in t_num_results if n >= k)}/{len(t_num_results)})")
        print(f"    Control: {c_at_least_k:.3f} ({sum(1 for n in c_num_results if n >= k)}/{len(c_num_results)})")
    
    # Bucket distribution summary
    print(f"\n  Treatment bucket distribution: {dict(t_bucket_counts)}")
    print(f"  Control bucket distribution: {dict(c_bucket_counts)}")
    
    # Simple statistical comparison
    t_mean = sum(t_num_results) / len(t_num_results) if t_num_results else 0
    c_mean = sum(c_num_results) / len(c_num_results) if c_num_results else 0
    t_median = sorted(t_num_results)[len(t_num_results)//2] if t_num_results else 0
    c_median = sorted(c_num_results)[len(c_num_results)//2] if c_num_results else 0
    
    print(f"\n  Treatment: mean={t_mean:.1f}, median={t_median}")
    print(f"  Control: mean={c_mean:.1f}, median={c_median}")
    print(f"  Ratio treatment/control mean: {t_mean/c_mean:.2f} if c_mean > 0 else 'N/A'")
    
    # G4 not applicable — no classifier-dependent answerability test
    print(f"\n--- G4: Not applicable (no classifier-dependent answerability test) ---")
    print(f"  This experiment does not use a classifier, so G4 as defined in E083")
    print(f"  (17 of 20 top-arrival need statements classified as served or partial_served)")
    print(f"  does not apply.")
    
    # Summary
    print(f"\n=== ARRIVAL METRICS SUMMARY ===")
    print(f"G1 retrieval: {'PASS' if (t_g1 == 'PASS' and c_g1 == 'PASS') else 'FAIL'}")
    print(f"G2: Not applicable — no classifier discrimination test")
    print(f"G3: Arrival count distribution reported above (fractions yielding ≥1, ≥2, ≥3, ≥5, ≥10 results)")
    print(f"G4: Not applicable — no classifier-dependent answerability test")
    print(f"\nTreatment arm: {len(t_num_results)} statements, arrival counts range from{min(t_num_results)} to {max(t_num_results)}")
    print(f"Control arm: {len(c_num_results)} statements, arrival counts range from{min(c_num_results)} to {max(c_num_results)}")
    print(f"\nKey observation: The view-count principle's arrival metric (search result count)")
    print(f"varies across statements. The distribution shape and comparison between treatment")
    print(f"and control arms provides the primary evidence for this experiment's finding.")


if __name__ == "__main__":
    evaluate_gates()
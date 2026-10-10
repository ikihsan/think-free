#!/usr/bin/env python3
"""E092 outcome: evaluate gates for the view-count arrival count prototype.

Computes G1 (retrieval) and G3 (measurement) verdicts based on the harvested
search results. G2 and G4 are declared N/A — this experiment does not use
a classifier discrimination test.

The key metric reported is arrival_count (num_search_results per query),
without any classify_served classification.

Usage:
    python3 outcome.py     # evaluate all gates
"""
import json
import os
import sys

TREATMENT_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "raw", "treatment-results.jsonl")
CONTROL_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "raw", "control-results.jsonl")


def load_results(path):
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results


def evaluate_gates():
    treatment = load_results(TREATMENT_RESULTS)
    control = load_results(CONTROL_RESULTS)

    print(f"Treatment results: {len(treatment)} statements")
    print(f"Control results: {len(control)} statements\n")

    # G1 retrieval
    t_g1 = "PASS" if len(treatment) >= 30 else "FAIL"
    c_g1 = "PASS" if len(control) >= 30 else "FAIL"
    print(f"G1 retrieval:")
    print(f"  Treatment: {t_g1} ({len(treatment)} >= 30)")
    print(f"  Control: {c_g1} ({len(control)} >= 30)")

    # G3 measurement: arrival count distribution
    t_arrival_counts = [r['num_results'] for r in treatment]
    c_arrival_counts = [r['num_results'] for r in control]

    t_mean = sum(t_arrival_counts) / len(t_arrival_counts) if t_arrival_counts else 0
    t_median = sorted(t_arrival_counts)[len(t_arrival_counts) // 2] if t_arrival_counts else 0
    t_min = min(t_arrival_counts) if t_arrival_counts else 0
    t_max = max(t_arrival_counts) if t_arrival_counts else 0

    c_mean = sum(c_arrival_counts) / len(c_arrival_counts) if c_arrival_counts else 0
    c_median = sorted(c_arrival_counts)[len(c_arrival_counts) // 2] if c_arrival_counts else 0
    c_min = min(c_arrival_counts) if c_arrival_counts else 0
    c_max = max(c_arrival_counts) if c_arrival_counts else 0

    # Distribution buckets
    t_buckets = {}
    c_buckets = {}
    for count in t_arrival_counts:
        t_buckets[count] = t_buckets.get(count, 0) + 1
    for count in c_arrival_counts:
        c_buckets[count] = c_buckets.get(count, 0) + 1

    print(f"G3 measurement:")
    print(f"  Treatment: n={len(t_arrival_counts)}, mean={t_mean:.2f}, median={t_median}, min={t_min}, max={t_max}")
    print(f"  Treatment distribution: {t_buckets}")
    print(f"  Control: n={len(c_arrival_counts)}, mean={c_mean:.2f}, median={c_median}, min={c_min}, max={c_max}")
    print(f"  Control distribution: {c_buckets}")
    print(f"  G3: REPORTING GATE — arrival count distribution reported above (no pass/fail)")

    print(f"\nG1 retrieval: {'PASS' if t_g1 == 'PASS' and c_g1 == 'PASS' else 'FAIL'}")
    print(f"G2 control validity: N/A — this experiment does not use a classifier discrimination test")
    print(f"G4 answerability: N/A — no classifier-dependent answerability test")

    g1_pass = t_g1 == "PASS" and c_g1 == "PASS"
    overall = "ALL GATES PASSED" if g1_pass else "SOME GATES FAILED"
    print(f"\nOverall: {overall}")


if __name__ == "__main__":
    evaluate_gates()

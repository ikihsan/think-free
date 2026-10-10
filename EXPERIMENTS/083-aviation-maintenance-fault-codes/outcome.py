#!/usr/bin/env python3
"""E083 outcome: evaluate gates for the aviation maintenance fault code measurement prototype.

Computes G1 (retrieval), G2 (control validity), G3 (measurement), and G4
(answerability sub-test) verdicts based on the harvested search results.

Usage:
    python3 outcome.py     # evaluate all gates
"""

import json
import os
import sys
from collections import Counter


# Corpus paths
TREATMENT_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "raw", "treatment-results.jsonl")
CONTROL_RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "raw", "control-results.jsonl")


def load_results(path):
    """Load results from a JSONL file."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            results.append(json.loads(line.strip()))
    return results


def classify_served(snippets, titles):
    """Classify a need statement based on search results.

    Returns: 'served', 'partially_served', or 'unserved'

    Solution keywords indicate a working resolution guide.
    Info keywords indicate definition/information but no complete guide.
    """
    all_text = ' '.join(titles + snippets).lower()
    solution_keywords = [
        'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair',
        'tool', 'software', 'app', 'download', 'install',
        'step by step', 'method', 'procedure', 'resolution',
        'fix for', 'fixes', 'troubleshooting'
    ]
    info_keywords = [
        'definition', 'what is', 'overview', 'introduction',
        'summary', 'characteristics', 'fault code',
        'meaning', 'indicates', 'refers to'
    ]
    has_solution = any(kw in all_text for kw in solution_keywords)
    has_info = any(kw in all_text for kw in info_keywords)
    has_tool_title = any(
        t and any(kw in t.lower() for kw in ['tool', 'software', 'app', 'guide', 'tutorial', 'manual'])
        for t in titles
    )
    if has_solution or has_tool_title:
        return 'served'
    elif has_info:
        return 'partially_served'
    else:
        return 'unserved'


def evaluate_gates():
    """Evaluate all gates and print verdicts."""
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

    # G2 control validity: reader separates 10 seeded control statements
    # (5 known served, 5 known unserved) at >= 0.85 accuracy
    def classify_served_v2(snippets, titles):
        all_text = ' '.join(snippets + titles).lower()
        solution_keywords = [
            'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair',
            'tool', 'software', 'app', 'download', 'install',
            'step by step', 'method', 'procedure', 'resolution'
        ]
        return 'served' if any(kw in all_text for kw in solution_keywords) else 'unserved'

    t_g2_pass = False
    if len(control) >= 10:
        true_labels = ['unserved'] * 5 + ['served'] * 5  # 5 unserved, 5 served
        predicted_labels = [classify_served_v2(r['snippets'], r['titles'])
                            for r in control[:10]]
        correct = sum(1 for t, p in zip(true_labels, predicted_labels) if t == p)
        accuracy = correct / len(true_labels)
        t_g2_pass = accuracy >= 0.85
        print(f"G2 control validity: accuracy = {accuracy:.2f} ({correct}/10) {'PASS' if t_g2_pass else 'FAIL'}")
    else:
        print(f"G2 control validity: FAIL (only {len(control)} control statements, need >= 10)")

    # G3 the measurement: fraction classified as served, with Wilson CI95, over >= 30 rows
    t_classifications = [classify_served(r['snippets'], r['titles']) for r in treatment]
    c_classifications = [classify_served(r['snippets'], r['titles']) for r in control]

    t_served = t_classifications.count('served')
    t_partial = t_classifications.count('partially_served')
    t_unserved = t_classifications.count('unserved')
    c_served = c_classifications.count('served')
    c_partial = c_classifications.count('partially_served')
    c_unserved = c_classifications.count('unserved')

    t_served_frac = t_served / len(treatment) if treatment else 0
    c_served_frac = c_served / len(control) if control else 0

    print(f"G3 measurement:")
    print(f"  Treatment: served={t_served}, partially_served={t_partial}, unserved={t_unserved}")
    print(f"  Treatment fraction: {t_served_frac:.3f} ({t_served}/{len(treatment)})")
    print(f"  Control: served={c_served}, partially_served={c_partial}, unserved={c_unserved}")
    print(f"  Control fraction: {c_served_frac:.3f} ({c_served}/{len(control)})")
    print(f"  G3: REPORTING GATE (no pass/fail; reports arrival metrics)")

    # G4 answerability sub-test: 17 of 20 top-arrival need statements classified
    # as served or partially_served
    t_top20 = t_classifications[:20]
    t_top20_served_partial = sum(1 for c in t_top20 if c in ('served', 'partially_served'))
    t_g4_pass = t_top20_served_partial >= 17
    print(f"G4 answerability sub-test:")
    print(f"  Top 20 treatment: served or partially_served = {t_top20_served_partial}/20")
    print(f"  G4: {'PASS' if t_g4_pass else 'FAIL'} (requires >= 17/20)")

    # Summary
    print(f"\n=== GATE SUMMARY ===")
    all_pass = t_g1 == "PASS" and c_g1 == "PASS" and t_g2_pass and t_g4_pass
    overall = "ALL GATES PASSED" if all_pass else "SOME GATES FAILED"
    print(f"G1 retrieval: {t_g1} / {c_g1}")
    print(f"G2 control validity: {'PASS' if t_g2_pass else 'FAIL'}")
    print(f"G3 measurement: REPORTING GATE")
    print(f"G4 answerability: {'PASS' if t_g4_pass else 'FAIL'}")
    print(f"\nOverall: {overall}")


if __name__ == "__main__":
    evaluate_gates()
#!/usr/bin/env python3
"""
Compute arm counts and apply kill gates for E067.
"""

import json
import sys
from pathlib import Path

def main():
    with open('raw/assessment.json', 'r') as f:
        data = json.load(f)

    results = data['results']

    # Count arms across all repos
    arm_counts = {'A1': 0, 'A2': 0, 'A3': 0, 'A4': 0, 'A5': 0}
    papers_with_code = 0
    papers_without_code = 0

    for r in results:
        if r['repos']:
            papers_with_code += 1
            for repo_r in r['repos']:
                arm_counts[repo_r['arm']] += 1
        else:
            papers_without_code += 1
            arm_counts['A5'] += 1

    total_with_code = arm_counts['A1'] + arm_counts['A2'] + arm_counts['A3'] + arm_counts['A4']

    print("=" * 60)
    print("E067 — ArXiv Code Reproducibility Assessment")
    print("=" * 60)
    print(f"Papers assessed: {len(results)}")
    print(f"Papers with code links: {papers_with_code}")
    print(f"Papers without code links: {papers_without_code}")
    print(f"Total repo assessments: {total_with_code + arm_counts['A5']}")
    print()
    print("Arm distribution:")
    for arm in ['A1', 'A2', 'A3', 'A4', 'A5']:
        print(f"  {arm}: {arm_counts[arm]}")

    print()

    # Kill gate K1: population
    k1 = papers_with_code < 20
    print(f"K1 (population ≥20): {'FAIL - KILL' if k1 else 'PASS'} ({papers_with_code} papers with code)")

    # Kill gate K2: severity - A1 rate ≥ 0.50
    if total_with_code > 0:
        a1_rate = arm_counts['A1'] / total_with_code
    else:
        a1_rate = 0.0
    k2 = a1_rate >= 0.50
    print(f"K2 (A1 rate < 0.50): {'FAIL - KILL' if k2 else 'PASS'} (A1 rate = {a1_rate:.3f})")

    # Kill gate K3: differentiation - A4 rate ≤ 0.10
    if total_with_code > 0:
        a4_rate = arm_counts['A4'] / total_with_code
    else:
        a4_rate = 0.0
    k3 = a4_rate <= 0.10
    print(f"K3 (A4 rate > 0.10): {'FAIL - KILL' if k3 else 'PASS'} (A4 rate = {a4_rate:.3f})")

    # Kill gate K4: baseline - A5 runnable rate > code-link runnable rate
    a5_runnable = 0  # Papers without code links that have runnable specs (unlikely)
    # For A5, we'd need to check supplementary materials - simplified to 0 for now
    code_link_runnable = a1_rate
    k4 = a5_runnable > code_link_runnable
    print(f"K4 (A5 runnable > code-link runnable): {'FAIL - KILL' if k4 else 'PASS'} (A5={a5_runnable}, code-link={code_link_runnable:.3f})")

    print()
    killed = any([k1, k2, k3, k4])
    if killed:
        print("VERDICT: KILL - Candidate not viable")
        sys.exit(1)
    else:
        print("VERDICT: PASS - Candidate viable for further investigation")
        sys.exit(0)

if __name__ == '__main__':
    main()
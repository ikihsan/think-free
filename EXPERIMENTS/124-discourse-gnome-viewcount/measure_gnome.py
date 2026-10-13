#!/usr/bin/env python3
"""
E124 — Measure view-count principle on discourse.gnome.org using matched-harvest design.
Uses IMPROVED Discourse classifier (classifier_gnome) with blog/announcement exclusion patterns.
"""

import json
import sys
import math
import re
from collections import Counter
from pathlib import Path

# Import improved GNOME classifier
from classifier_gnome import (
    DISCOURSE_NEED_PATTERNS,
    DISCOURSE_EXCLUDED_PATTERNS,
    compute_gnome_coverage,
    classify_gnome_item
)


def measure_gnome_framework(data_path, coverage_floor=0.60):
    rows = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: rows.append(json.loads(line))
            except json.JSONDecodeError: continue
    total = len(rows)
    if total == 0: return {'error': 'no rows loaded', 'g1_pass': False}

    vc_positive = sum(1 for r in rows if r.get('view_count', 0) > 0)
    vc_rate = vc_positive / total if total > 0 else 0
    g1_pass = vc_rate >= 0.95

    assessments = []
    if g1_pass:
        assessments.append(f"G1: {vc_rate*100:.1f}% >= 95% — MET")
    else:
        assessments.append(f"G1: {vc_rate*100:.1f}% < 95% — NOT MET")

    if not g1_pass:
        return {k: v for k, v in {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'g1_pass': False, 'g2_pass': False, 'g3_pass': False, 'g4_pass': False,
            'assessments': assessments, 'halt_reason': 'G1 failed',
            'coverage_floor': coverage_floor, 'need_total': 0,
            'unserved_count': 0, 'served_count': 0, 'ci95': [0, 0], 'conclusion': ''}.items()}

    # Classify all items using improved GNOME classifier
    assessment = compute_gnome_coverage(rows)
    classified_total = assessment['classified']
    coverage = assessment['coverage']
    need_total = assessment['need_related']
    unclassified = assessment['unclassified']

    # G2: coverage floor first
    cov_met = coverage >= coverage_floor
    need_frac = need_total / classified_total if classified_total > 0 else 0
    need_frac_met = need_total / total >= 0.05 if total > 0 else False
    g2_pass = cov_met and need_frac_met

    assessments += [f"G2 cov: {coverage*100:.1f}% >= {coverage_floor*100:.0f}% — MET"
        if cov_met else f"G2 cov: {coverage*100:.1f}% < {coverage_floor*100:.0f}% — NOT MET"]

    if not g2_pass:
        return {k: v for k, v in {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'coverage': coverage, 'classified_total': classified_total,
            'need_related': need_total, 'random': classified_total - need_total,
            'unclassified': unclassified, 'g1_pass': True, 'g2_pass': False, 'g3_pass': False,
            'g4_pass': False, 'assessments': assessments,
            'halt_reason': 'G2 failed', 'coverage_floor': coverage_floor,
            'need_total': need_total, 'unserved_count': 0, 'served_count': 0,
            'ci95': [0, 0], 'conclusion': ''}.items()}

    # G4: sample size
    if classified_total < 30:
        return {k: v for k, v in {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'coverage': coverage, 'classified_total': classified_total,
            'need_related': need_total, 'random': classified_total - need_total,
            'unclassified': unclassified, 'g1_pass': True, 'g2_pass': True, 'g3_pass': False,
            'g4_pass': False, 'assessments': assessments,
            'halt_reason': f'G4 failed: classified_total {classified_total} < 30',
            'coverage_floor': coverage_floor, 'need_total': need_total,
            'unserved_count': 0, 'served_count': 0, 'ci95': [0, 0], 'conclusion': ''}.items()}

    # G3: unserved fraction
    need_items = []
    for r in rows:
        combined = r.get('combined_text', '').lower()
        # Classify using improved GNOME classifier
        classification = classify_gnome_item(combined)
        
        if classification != 'need-related':
            continue
        
        # Discourse unserved logic: no replies AND no accepted answer
        reply_count = r.get('reply_count', 0)
        has_accepted = r.get('has_accepted_answer', False)
        unserved = (reply_count == 0) and (not has_accepted)
        need_items.append({'row': r, 'unserved': unserved})

    n_actual = len(need_items)
    u_count = sum(1 for i in need_items if i['unserved'])
    s_count = n_actual - u_count
    frac = u_count / n_actual if n_actual > 0 else 0
    z = 1.96; n = n_actual; p = frac
    denom = 1 + z**2 / n; centre = (p + z**2/(2*n)) / denom
    half = (z / denom) * math.sqrt(p*(1-p)/n + z**2/(4*n**2))
    ci_low, ci_high = centre - half, centre + half
    g3_pass = ci_high < 0.60

    concl = ('ALL GATES PASS — view-count principle supported on this Discourse domain with matched harvest and coverage floor'
        if g3_pass else 'G3 FAIL — unserved fraction not below threshold; line closed for this domain')

    return {'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
        'coverage': coverage, 'classified_total': classified_total,
        'need_related': need_total, 'random': classified_total - need_total,
        'unclassified': unclassified, 'g1_pass': True, 'g2_pass': True, 'g3_pass': g3_pass, 'g4_pass': classified_total >= 30,
        'unserved_fraction': frac, 'unserved_count': u_count, 'served_count': s_count,
        'need_total': n_actual, 'coverage_floor': coverage_floor, 'ci95': [ci_low, ci_high],
        'assessments': assessments, 'halt_reason': None, 'conclusion': concl}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 measure_gnome.py <path-to-jsonl> [coverage_floor]")
        sys.exit(1)
    data_path = sys.argv[1]
    cov_floor = float(sys.argv[2]) if len(sys.argv) > 2 else 0.60
    if not Path(data_path).exists():
        print(f"Error: file not found: {data_path}"); sys.exit(1)
    result = measure_gnome_framework(data_path, cov_floor)
    if 'error' in result:
        print(f"Error: {result['error']}"); sys.exit(1)
    print(f"\nG1: {'PASS' if result['g1_pass'] else 'FAIL'}")
    print(f"G2: {'PASS' if result['g2_pass'] else 'FAIL'}")
    print(f"G3: {'PASS' if result['g3_pass'] else 'FAIL'}")
    print(f"G4: {'PASS' if result['g4_pass'] else 'FAIL'}")
    print(f"Concl: {result['conclusion']}")
    
    # Save results
    output_path = Path(data_path).parent / "results.json"
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to {output_path}")
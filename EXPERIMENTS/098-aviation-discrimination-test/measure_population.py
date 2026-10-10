#!/usr/bin/env python3
"""E098 — Population measurement for aviation fault codes using validated instrument."""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from discrimination_test import classify_topic, has_specific_fault_code


def wilson_ci(k: int, n: int, z: float = 1.959963985) -> tuple:
    """Wilson 95% CI for proportion."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def main():
    # Load the harvested topics
    input_path = os.path.join(HERE, "..", "096-aviation-view-count", "treatment-needs.jsonl")
    
    rows = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    
    print(f"Total harvested topics: {len(rows)}")
    
    # Filter for fault-related topics
    fault_keywords = ['fault', 'error', 'code', 'malfunction', 'failure', 'troubleshoot', 
                      'diagnostic', 'alert', 'warning', 'ecam', 'eicas', 'mcdp', 'mfd', 
                      'fault code', 'error code', 'fault message']
    
    fault_rows = []
    for r in rows:
        title = r['title'].lower()
        if any(kw in title for kw in fault_keywords):
            fault_rows.append(r)
    
    print(f"Fault-related topics: {len(fault_rows)}")
    
    # Classify each fault-related topic
    served = 0
    partially_served = 0
    unserved = 0
    
    details = []
    
    for r in fault_rows:
        classification = classify_topic(r)
        details.append({
            'id': r['id'],
            'title': r['title'],
            'view_count': r['view_count'],
            'answer_count': r['answer_count'],
            'accepted': r.get('accepted_answer_id') is not None,
            'fault_code_specific': has_specific_fault_code(r['title']),
            'classification': classification
        })
        
        if classification == 'served':
            served += 1
        elif classification == 'partially_served':
            partially_served += 1
        else:
            unserved += 1
    
    total = len(fault_rows)
    
    print(f"\n=== POPULATION MEASUREMENT RESULTS ===")
    print(f"Total fault-related topics: {total}")
    print(f"  Served: {served} ({served/total*100:.1f}%)")
    print(f"  Partially Served: {partially_served} ({partially_served/total*100:.1f}%)")
    print(f"  Unserved: {unserved} ({unserved/total*100:.1f}%)")
    
    # Wilson CIs
    s_p, s_lo, s_hi = wilson_ci(served, total)
    p_p, p_lo, p_hi = wilson_ci(partially_served, total)
    u_p, u_lo, u_hi = wilson_ci(unserved, total)
    
    print(f"\nWilson 95% CIs:")
    print(f"  Served: [{s_lo:.3f}, {s_hi:.3f}]")
    print(f"  Partially Served: [{p_lo:.3f}, {p_hi:.3f}]")
    print(f"  Unserved: [{u_lo:.3f}, {u_hi:.3f}]")
    
    # Top 20 by view_count for answerability sub-test
    top20 = sorted(fault_rows, key=lambda x: x['view_count'], reverse=True)[:20]
    top20_served_or_partial = sum(1 for r in top20 if classify_topic(r) in ['served', 'partially_served'])
    print(f"\nAnswerability sub-test (top 20 by view_count):")
    print(f"  Served or partially served: {top20_served_or_partial}/20 = {top20_served_or_partial/20*100:.1f}%")
    print(f"  Gate G4 (≥17/20): {'PASS' if top20_served_or_partial >= 17 else 'FAIL'}")
    
    # Save detailed results
    results = {
        'experiment': 'E098',
        'population_measurement': {
            'total_fault_topics': total,
            'served': served,
            'partially_served': partially_served,
            'unserved': unserved,
            'served_fraction': served/total,
            'partially_served_fraction': partially_served/total,
            'unserved_fraction': unserved/total,
            'served_ci95': [s_lo, s_hi],
            'partially_served_ci95': [p_lo, p_hi],
            'unserved_ci95': [u_lo, u_hi],
            'g4_answerability': {
                'top20_served_or_partial': top20_served_or_partial,
                'pass': top20_served_or_partial >= 17
            }
        },
        'details': details
    }
    
    results_path = os.path.join(HERE, 'population_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=1)
    
    print(f"\nDetailed results saved to {results_path}")
    
    return results


if __name__ == "__main__":
    main()
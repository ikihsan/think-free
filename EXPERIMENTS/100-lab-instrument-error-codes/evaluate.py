#!/usr/bin/env python3
"""
Evaluate gate results for E100 experiment.
"""

import json

from constants import (
    Classification,
    LABEL_SERVED,
    LABEL_UNSERVED_OPEN_LIKE,
    LABEL_NOT_A_NEED,
    SEED_CONTROLS,
    wilson_ci_lower,
    wilson_ci_upper,
)


def evaluate_gates(classifications):
    """Evaluate all gates."""
    # Filter vc_positive (need statements with concrete fault code need)
    vc_positive = [c for c in classifications if c.label in (LABEL_SERVED, LABEL_UNSERVED_OPEN_LIKE)]
    unserved = [c for c in vc_positive if c.label == LABEL_UNSERVED_OPEN_LIKE]
    served = [c for c in vc_positive if c.label == LABEL_SERVED]
    not_need = [c for c in classifications if c.label == LABEL_NOT_A_NEED]
    
    # G1: Need prevalence
    g1_pass = len(vc_positive) >= 15
    g1_detail = f"{len(vc_positive)} vc_positive items (threshold 15)"
    
    # G2: Control validity - check seeded controls
    # Seed items are item_000 through item_003
    ctrl_correct = 0
    ctrl_total = 0
    seed_mapping = {'item_000': 's1', 'item_001': 's2', 'item_002': 'u1', 'item_003': 'u2'}
    for c in classifications:
        if c.item_id in seed_mapping:
            ctrl_total += 1
            expected = SEED_CONTROLS[seed_mapping[c.item_id]]['label']
            if c.label == expected:
                ctrl_correct += 1
    
    g2_accuracy = ctrl_correct / ctrl_total if ctrl_total > 0 else 0
    g2_pass = g2_accuracy >= 0.85
    g2_detail = f"Control accuracy: {ctrl_correct}/{ctrl_total} = {g2_accuracy:.2f} (threshold 0.85)"
    
    # G3: Unserved fraction with Wilson CI95
    if len(vc_positive) >= 15:
        unserved_frac = len(unserved) / len(vc_positive)
        ci_lower = wilson_ci_lower(unserved_frac, len(vc_positive))
        ci_upper = wilson_ci_upper(unserved_frac, len(vc_positive))
        g3_pass = ci_upper < 0.60  # Upper bound < 60%
        g3_detail = f"Unserved fraction: {unserved_frac:.3f} ({len(unserved)}/{len(vc_positive)}), Wilson CI95: [{ci_lower:.3f}, {ci_upper:.3f}], upper < 0.60: {g3_pass}"
    else:
        unserved_frac = 0
        ci_lower = 0
        ci_upper = 1
        g3_pass = False
        g3_detail = f"Insufficient vc_positive items ({len(vc_positive)} < 15)"
    
    # G4: view_count validation
    view_positive = sum(1 for c in classifications if c.view_count > 0)
    total_with_views = len(classifications)
    view_positive_rate = view_positive / total_with_views if total_with_views > 0 else 0
    g4_pass = view_positive_rate >= 0.95
    g4_detail = f"View positive rate: {view_positive_rate:.3f} ({view_positive}/{total_with_views})"
    
    return {
        'G1_need_prevalence': {'pass': g1_pass, 'detail': g1_detail, 'value': len(vc_positive)},
        'G2_control_validity': {'pass': g2_pass, 'detail': g2_detail, 'value': g2_accuracy},
        'G3_unserved_fraction': {'pass': g3_pass, 'detail': g3_detail, 'value': unserved_frac, 'ci': [ci_lower, ci_upper]},
        'G4_view_count_validation': {'pass': g4_pass, 'detail': g4_detail, 'value': view_positive_rate},
        'counts': {
            'total': len(classifications),
            'vc_positive': len(vc_positive),
            'served': len(served),
            'unserved_open_like': len(unserved),
            'not_a_need': len(not_need),
            'view_positive': view_positive,
        }
    }


def print_results(results):
    """Print gate results."""
    print("\n=== GATE RESULTS ===")
    for gate_name, gate_result in results.items():
        if gate_name == 'counts':
            continue
        status = "PASS" if gate_result['pass'] else "FAIL"
        print(f"  {gate_name}: {status}")
        print(f"    {gate_result['detail']}")
    
    print(f"\n=== COUNTS ===")
    for k, v in results['counts'].items():
        print(f"  {k}: {v}")
    
    # Overall verdict
    all_pass = all(results[g]['pass'] for g in results if g != 'counts')
    print(f"\n=== OVERALL: {'ALL GATES PASS' if all_pass else 'SOME GATES FAIL'} ===")
    return all_pass


def save_results(classifications, results):
    """Save results to JSON."""
    output = {
        'classifications': [
            {
                'item_id': c.item_id,
                'label': c.label,
                'rationale': c.rationale,
                'title': c.title,
                'view_count': c.view_count,
                'fault_codes': c.fault_codes,
                'instrument_types': c.instrument_types,
            }
            for c in classifications
        ],
        'gates': results,
    }
    
    with open('results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to results.json")


if __name__ == '__main__':
    # For testing
    print("This module provides evaluation functions. Run classify.py for full experiment.")
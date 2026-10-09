#!/usr/bin/env python3
"""
E076 — view_count + unserved-open measurement framework.

A reusable instrument for measuring arrivals (view_count) and unserved fractions
across different domains/corpora. Designed as a lightweight prototype/probe
that helps researchers apply the mission's core measurement framework without
building a product.

See RESEARCH/F.md C1-C6 for the pre-release check lens; this prototype
answers the important uncertainty of whether the framework is practically
applicable beyond the mission's own experiments.

NOT PRODUCT VALIDATION. Evidence-gathering prototype.
"""

import json
import sys
import os
from collections import Counter
import math


def load_jsonl(path):
    """Load a JSONL file, one JSON object per line."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip malformed lines rather than failing entirely
                continue
    return rows


def classify_by_outcome_class(outcome_class):
    """Classify based on pre-classified outcome_class field ('served' or 'unserved')."""
    if outcome_class == 'served':
        return 'served'
    elif outcome_class == 'unserved':
        return 'unserved'
    return None  # unknown, fall back to company_response classification


def classify_by_company_response(company_response):
    """Classify based on company_response text field."""
    served_responses = {
        'Closed with monetary relief',
        'Closed with non-monetary relief',
        'Closed with explanation',
    }
    return 'served' if company_response in served_responses else 'unserved'


def smart_classify(row, outcome_field='outcome_class', company_response_field='company_response'):
    """Smart classification: try outcome_class first, fall back to company_response."""
    outcome = row.get(outcome_field, '')
    classified = classify_by_outcome_class(outcome)
    if classified is not None:
        return classified
    # Fall back to company_response classification
    return classify_by_company_response(row.get(company_response_field, ''))


def measure_framework(data_path, view_count_field='view_count', outcome_field='outcome_class'):
    """
    Measure the view_count + unserved-open framework on a corpus.
    
    Returns a dict with:
    - total_rows: number of rows loaded
    - vc_positive: rows where view_count > 0 (independent arrivals observed)
    - vc_zero: rows where view_count == 0 or missing
    - vc_positive_rate: vc_positive / total_rows
    - served: rows classified as served
    - unserved: rows classified as unserved
    - unserved_rate: unserved / total_rows with Wilson CI95
    - unserved_by_reason: Counter of company_response values for unserved rows
    - per_product: breakdown by product field if present
    """
    rows = load_jsonl(data_path)
    total = len(rows)
    
    if total == 0:
        return {'error': 'no rows loaded'}
    
    # G1: view_count validation
    vc_positive = sum(1 for r in rows if r.get(view_count_field, 0) > 0)
    vc_zero = total - vc_positive
    vc_rate = vc_positive / total
    
    # G3: unserved-open fraction using smart classification
    served = sum(1 for r in rows if smart_classify(r, outcome_field, company_response_field) == 'served')
    unserved = total - served
    p = unserved / total
    z = 1.96
    n = total
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2*n)) / denom
    half = (z / denom) * math.sqrt(p*(1-p)/n + z**2/(4*n**2))
    ci_low = centre - half
    ci_high = centre + half
    
    # Break down unserved by response using smart classification
    unserved_by_reason = Counter()
    for r in rows:
        if smart_classify(r, outcome_field, company_response_field) == 'unserved':
            resp = r.get(company_response_field, 'unknown')
            unserved_by_reason[resp] += 1
    
    # Per-product breakdown (if product field exists)
    per_product = {}
    has_product = any('product' in r for r in rows[:10])  # check sample
    if has_product:
        prod_counts = Counter(r.get('product', 'unknown') for r in rows)
        for prod, count in prod_counts.most_common():
            prod_served = sum(1 for r in rows if r.get('product') == prod and r.get(outcome_field, '') in {
                'Closed with monetary relief',
                'Closed with non-monetary relief',
                'Closed with explanation',
            })
            per_product[prod] = {
                'total': count,
                'served': prod_served,
                'unserved': count - prod_served,
                'rate': (count - prod_served) / count if count > 0 else 0,
            }
    
    result = {
        'total_rows': total,
        'vc_positive': vc_positive,
        'vc_zero': vc_zero,
        'vc_positive_rate': vc_rate,
        'served': served,
        'unserved': unserved,
        'unserved_rate': p,
        'unserved_ci95': [ci_low, ci_high],
        'unserved_by_reason': dict(unserved_by_reason),
    }
    
    if per_product:
        result['per_product'] = per_product
    
    # Assessment text
    assessments = []
    if vc_rate >= 0.95:
        assessments.append(f"G1 view_count: {vc_rate*100:.1f}% positive >= 95% threshold — MET")
    else:
        assessments.append(f"G1 view_count: {vc_rate*100:.1f}% positive < 95% threshold — NOT MET")
    
    unserved_pct = p * 100
    if unserved_pct <= 1.0:
        assessments.append(f"G3 unserved fraction: {unserved_pct:.1f}% — very low, consistent with administrative delays pattern")
    elif unserved_pct <= 5.0:
        assessments.append(f"G3 unserved fraction: {unserved_pct:.1f}% — low, likely administrative")
    else:
        assessments.append(f"G3 unserved fraction: {unserved_pct:.1f}% — higher than observed domains, warrants investigation")
    
    result['assessments'] = assessments
    
    return result


def interactive_cli():
    """CLI entry point for running the framework on a data file."""
    if len(sys.argv) < 2:
        print("Usage: python3 view_count_framework.py <path-to-jsonl>")
        print("  Expected fields: view_count, outcome_class (or company_response), optional: product")
        sys.exit(1)
    
    data_path = sys.argv[1]
    
    if not os.path.exists(data_path):
        print(f"Error: file not found: {data_path}")
        sys.exit(1)
    
    result = measure_framework(data_path)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    print(f"\n=== view_count + unserved-open Framework Report ===")
    print(f"Data file: {data_path}")
    print(f"\nG1 — view_count validation:")
    print(f"  Total rows: {result['total_rows']}")
    print(f"  view_count > 0: {result['vc_positive']} ({result['vc_positive_rate']*100:.1f}%)")
    print(f"  view_count == 0 or missing: {result['vc_zero']}")
    for a in result['assessments'][:1]:
        print(f"  -> {a}")
    
    print(f"\nG3 — unserved-open fraction:")
    print(f"  Served: {result['served']} ({result['served']/result['total_rows']*100:.1f}%)")
    print(f"  Unserved: {result['unserved']} ({result['unserved_rate']*100:.1f}%)")
    print(f"  Wilson CI95: [{result['unserved_ci95'][0]*100:.1f}%, {result['unserved_ci95'][1]*100:.1f}%]")
    for a in result['assessments'][1:]:
        print(f"  -> {a}")
    
    print(f"\nUnserved breakdown by reason:")
    for reason, count in sorted(result['unserved_by_reason'].items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count} ({count/result['total_rows']*100:.1f}%)")
    
    if 'per_product' in result:
        print(f"\nPer-product breakdown:")
        for prod, info in sorted(result['per_product'].items(), key=lambda x: -x[1]['total']):
            print(f"  {prod}: {info['total']} total, {info['unserved']} unserved ({info['rate']*100:.1f}%)")
    
    print(f"\n---")
    print(f"Assessments:")
    for a in result['assessments']:
        print(f"  {a}")


if __name__ == '__main__':
    interactive_cli()
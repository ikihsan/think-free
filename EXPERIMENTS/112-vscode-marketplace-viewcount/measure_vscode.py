#!/usr/bin/env python3
"""
E112 — Gated view-count measurement for VS Code Marketplace.
Adapted from E119 measure_framework.py with matched harvest design.
"""

import json

_CACHE = {}


def _load(filename, key):
    """A moved-out data list, read once and cached.

    The list was inline here as a Python literal and pushed the file over
    the 300-line cap in `docs/policy/doc-standards.md`; it is data, so it
    now lives in a `.json` sibling, which the cap exempts.
    """
    if not _CACHE:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              filename), encoding="utf-8") as handle:
            _CACHE.update(json.load(handle))
    return _CACHE[key]


import sys
import os
import math
from pathlib import Path
from viewcount_stats import (cliffs_delta, mann_whitney_u, wilson_ci)

# Need-related keywords (declared before measurement, from PROTOCOL.md)
NEED_KEYWORDS = _load('vscode_keywords.json', 'NEED_KEYWORDS')

EXCLUDED_KEYWORDS = _load('vscode_keywords.json', 'EXCLUDED_KEYWORDS')

def classify_extension(text: str) -> str:
    """Classify extension text as 'need-related', 'random', or 'unclassified'."""
    text_lower = text.lower()
    
    # Check excluded keywords first (hard exclusion)
    for kw in EXCLUDED_KEYWORDS:
        if kw.lower() in text_lower:
            return 'random'
    
    # Check need-related keywords
    for kw in NEED_KEYWORDS:
        if kw.lower() in text_lower:
            return 'need-related'
    
    return 'unclassified'

def compute_coverage(extensions: list) -> dict:
    """Compute coverage statistics."""
    total = len(extensions)
    if total == 0:
        return {'total': 0, 'classified': 0, 'unclassified': 0, 'coverage': 0.0, 'need_related': 0, 'random': 0}
    
    need_related = 0
    random_count = 0
    unclassified = 0
    
    for ext in extensions:
        text = f"{ext.get('display_name', '')} {ext.get('description', '')} {' '.join(ext.get('tags', []))}"
        classification = classify_extension(text)
        
        if classification == 'need-related':
            need_related += 1
        elif classification == 'random':
            random_count += 1
        else:
            unclassified += 1
    
    classified = need_related + random_count
    coverage = classified / total if total > 0 else 0.0
    
    return {
        'total': total,
        'classified': classified,
        'unclassified': unclassified,
        'coverage': coverage,
        'need_related': need_related,
        'random': random_count,
    }




def measure_vscode(data_path: str, coverage_floor: float = 0.60) -> dict:
    """Run gated measurement on VS Code Marketplace data."""
    extensions = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                extensions.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    total = len(extensions)
    if total == 0:
        return {'error': 'no rows loaded', 'g1_pass': False}
    
    # G1: arrival metric coverage (install_count > 0)
    vc_positive = sum(1 for e in extensions if e.get('install_count', 0) > 0)
    vc_rate = vc_positive / total if total > 0 else 0
    g1_pass = vc_rate >= 0.95
    
    assessments = []
    if g1_pass:
        assessments.append(f"G1: {vc_rate*100:.1f}% >= 95% — MET")
    else:
        assessments.append(f"G1: {vc_rate*100:.1f}% < 95% — NOT MET")
    
    if not g1_pass:
        return {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'g1_pass': False, 'g2_pass': False, 'g3_pass': False, 'g4_pass': False,
            'assessments': assessments, 'halt_reason': 'G1 failed',
            'coverage_floor': coverage_floor, 'need_total': 0,
            'cliffs_delta': 0, 'p_value': 1.0, 'conclusion': ''
        }
    
    # Classify all items
    assessment = compute_coverage(extensions)
    classified_total = assessment['classified']
    coverage = assessment['coverage']
    need_total = assessment['need_related']
    random_total = assessment['random']
    unclassified = assessment['unclassified']
    
    # G2: coverage floor
    cov_met = coverage >= coverage_floor
    need_frac_met = need_total / total >= 0.05 if total > 0 else False
    g2_pass = cov_met and need_frac_met
    
    assessments.append(f"G2 cov: {coverage*100:.1f}% >= {coverage_floor*100:.0f}% — {'MET' if cov_met else 'NOT MET'}")
    assessments.append(f"G2 need_frac: {need_total}/{total} = {need_total/total*100:.1f}% >= 5% — {'MET' if need_frac_met else 'NOT MET'}")
    
    if not g2_pass:
        return {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'coverage': coverage, 'classified_total': classified_total,
            'need_related': need_total, 'random': random_total, 'unclassified': unclassified,
            'g1_pass': True, 'g2_pass': False, 'g3_pass': False, 'g4_pass': False,
            'assessments': assessments, 'halt_reason': 'G2 failed',
            'coverage_floor': coverage_floor, 'need_total': need_total,
            'cliffs_delta': 0, 'p_value': 1.0, 'conclusion': ''
        }
    
    # G4: sample size
    if classified_total < 30:
        return {
            'total_rows': total, 'vc_positive': vc_positive, 'vc_rate': vc_rate,
            'coverage': coverage, 'classified_total': classified_total,
            'need_related': need_total, 'random': random_total, 'unclassified': unclassified,
            'g1_pass': True, 'g2_pass': True, 'g3_pass': False, 'g4_pass': False,
            'assessments': assessments, 'halt_reason': f'G4 failed: classified_total {classified_total} < 30',
            'coverage_floor': coverage_floor, 'need_total': need_total,
            'cliffs_delta': 0, 'p_value': 1.0, 'conclusion': ''
        }
    
    # Matched harvest design: split from same pool, sort by install_count descending
    # Classify each extension
    classified_extensions = []
    for ext in extensions:
        text = f"{ext.get('display_name', '')} {ext.get('description', '')} {' '.join(ext.get('tags', []))}"
        classification = classify_extension(text)
        if classification in ('need-related', 'random'):
            classified_extensions.append({
                'ext': ext,
                'classification': classification,
                'install_count': ext.get('install_count', 0)
            })
    
    # Sort by install_count descending
    classified_extensions.sort(key=lambda x: x['install_count'], reverse=True)
    
    # Split into need and random arms
    need_arm = [e for e in classified_extensions if e['classification'] == 'need-related']
    random_arm = [e for e in classified_extensions if e['classification'] == 'random']
    
    need_installs = [e['install_count'] for e in need_arm]
    random_installs = [e['install_count'] for e in random_arm]
    
    # Compute Cliff's delta and Mann-Whitney U
    delta = cliffs_delta(need_installs, random_installs)
    u_stat, p_value = mann_whitney_u(need_installs, random_installs)
    
    # G3: separation (Cliff's delta > 0.2 AND p < 0.05)
    g3_pass = delta > 0.2 and p_value < 0.05
    
    assessments.append(f"G3: Cliff's delta = {delta:.4f} (> 0.2? {'YES' if delta > 0.2 else 'NO'}), p = {p_value:.6f} (< 0.05? {'YES' if p_value < 0.05 else 'NO'}) — {'PASS' if g3_pass else 'FAIL'}")
    
    # G4: need-related active rate (>= 50% have > 100 installs)
    need_active = sum(1 for x in need_installs if x > 100)
    need_active_rate = need_active / len(need_installs) if need_installs else 0
    g4_pass = need_active_rate >= 0.5
    
    assessments.append(f"G4: Need-related active rate = {need_active_rate*100:.1f}% (>{100} installs) — {'MET' if g4_pass else 'NOT MET'}")
    
    # Summary stats
    need_median = sorted(need_installs)[len(need_installs)//2] if need_installs else 0
    random_median = sorted(random_installs)[len(random_installs)//2] if random_installs else 0
    
    concl = ('ALL GATES PASS — view-count principle supported on VS Code Marketplace with matched harvest'
        if g3_pass and g4_pass else 'G3/G4 FAIL — principle does not generalize to this domain')
    
    return {
        'total_rows': total,
        'vc_positive': vc_positive,
        'vc_rate': vc_rate,
        'coverage': coverage,
        'classified_total': classified_total,
        'need_related': need_total,
        'random': random_total,
        'unclassified': unclassified,
        'g1_pass': True,
        'g2_pass': True,
        'g3_pass': g3_pass,
        'g4_pass': g4_pass,
        'need_arm_size': len(need_arm),
        'random_arm_size': len(random_arm),
        'need_median_installs': need_median,
        'random_median_installs': random_median,
        'need_active_rate': need_active_rate,
        'cliffs_delta': delta,
        'p_value': p_value,
        'coverage_floor': coverage_floor,
        'assessments': assessments,
        'halt_reason': None,
        'conclusion': concl
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 measure_vscode.py <path-to-jsonl> [coverage_floor]")
        sys.exit(1)
    data_path = sys.argv[1]
    cov_floor = float(sys.argv[2]) if len(sys.argv) > 2 else 0.60
    if not os.path.exists(data_path):
        print(f"Error: file not found: {data_path}")
        sys.exit(1)
    result = measure_vscode(data_path, cov_floor)
    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    print(f"\n=== GATE RESULTS ===")
    for a in result['assessments']:
        print(a)
    print(f"\n=== SUMMARY ===")
    print(f"Total extensions: {result['total_rows']}")
    print(f"Install count coverage: {result['vc_rate']*100:.1f}%")
    print(f"Classifier coverage: {result['coverage']*100:.1f}%")
    print(f"Classified: {result['classified_total']} (need: {result['need_related']}, random: {result['random']})")
    print(f"Unclassified: {result['unclassified']}")
    print(f"Need arm size: {result['need_arm_size']}")
    print(f"Random arm size: {result['random_arm_size']}")
    print(f"Need median installs: {result['need_median_installs']}")
    print(f"Random median installs: {result['random_median_installs']}")
    print(f"Cliff's delta: {result['cliffs_delta']:.4f}")
    print(f"Mann-Whitney p-value: {result['p_value']:.6f}")
    print(f"Need active rate (>100): {result['need_active_rate']*100:.1f}%")
    print(f"\nConclusion: {result['conclusion']}")
    
    # Save results
    with open('results.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("\nSaved results.json")

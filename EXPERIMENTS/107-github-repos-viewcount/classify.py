#!/usr/bin/env python3
"""
E107 — Classification patterns and helpers for GitHub repos view-count experiment.
"""

import re
from math import sqrt

# Classification patterns (same as PROTOCOL.md)
need_patterns = [
    r'\bhow (do|can|to|should|would|is|are)\b',
    r'\bwhat (is|are|should|would|could|causes?|makes?)\b',
    r'\bwhy (is|are|do|does|did|can|won|not)\b',
    r'\bhelp\b',
    r'\bissue|problem|error|broken|failure|not working\b',
    r'\brecommend|suggestion|advice\b',
    r'\bwhich (one|should|is best|to buy|to use|get)\b',
    r'\bwhere (can|to|is|are)\b',
    r'\bany (idea|suggestion|tip|advice|recommendation)\b',
    r'\bcan (someone|anybody|anyone)\b',
    r'\bstuck|confused|lost\b',
    r'\btrying to\b',
    r'\bwondering\b',
    r'\bshould I\b',
]

non_need_patterns = [
    r'\bIC\b',
    r'\bshow.*(off|me)\b',
    r'\bmy (new|first|latest) (setup|build|project|purchase)\b',
    r'\blook at (this|my)\b',
    r'\bjust (got|bought|picked up|received)\b',
    r'\bwhat.*(you|getting|ordering|buying)\b',
    r'\bwelcome to\b',
    r'\bthank(s| you)\b',
    r'\bimage(s)?\s*(only|thread)\b',
    r'\bpicture(s)?\s*(only|thread|uno)\b',
    r'\bintroductions?\b',
    r'\bfeature request\b',
    r'\bbenchmark\b',
    r'\bannounc\b',
    r'\brelease\b',
]

def is_need(title):
    """Check if title matches need patterns and doesn't match non-need patterns."""
    # Check non-need patterns first
    for pattern in non_need_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return False
    # Check need patterns
    for pattern in need_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return True
    return False

def wilson_upper_bound(p, n, z=1.96):
    """Wilson CI95 upper bound."""
    if n == 0:
        return 1.0
    phat = p
    denominator = 1 + z*z/n
    centre = phat + z*z/(2*n)
    margin = z * sqrt(phat*(1-phat)/n + z*z/(4*n*n))
    upper = (centre + margin) / denominator
    return min(upper, 1.0)

def check_gates(classified, total_issues, repo_fractions):
    """Check all gates and return pass/fail with details."""
    results = {}
    
    # G1: arrival metric >= 95% across ALL issues
    arrival_positive = classified['arrival_positive']
    g1_pass = arrival_positive / total_issues >= 0.95 if total_issues > 0 else False
    results['g1'] = {
        'pass': g1_pass,
        'value': f"{arrival_positive}/{total_issues} = {arrival_positive/total_issues*100:.1f}%",
        'detail': 'arrival metric available' if g1_pass else 'arrival metric not available'
    }
    
    # G2: need prevalence >= 5%
    total_need = classified['need']
    g2_pass = total_need / total_issues >= 0.05 if total_issues > 0 else False
    results['g2'] = {
        'pass': g2_pass,
        'value': f"{total_need}/{total_issues} = {total_need/total_issues*100:.1f}%",
        'detail': 'need prevalence measurable' if g2_pass else 'need prevalence too low'
    }
    
    # G3: unserved-open-like fraction < 50% with Wilson CI95 upper < 60%
    unserved_count = classified['unserved_count']
    served_count = classified['served_count']
    total_need_check = unserved_count + served_count
    if total_need_check > 0:
        p = unserved_count / total_need_check
        upper = wilson_upper_bound(p, total_need_check)
        g3_pass = p < 0.5 and upper < 0.6
    else:
        p = 0
        upper = 1.0
        g3_pass = False
    unserved_pct = unserved_count / total_need_check * 100 if total_need_check > 0 else 0
    results['g3'] = {
        'pass': g3_pass,
        'value': f"{unserved_count}/{total_need_check} = {unserved_pct:.1f}%",
        'detail': f'Unserved fraction={p*100:.1f}%, Wilson upper={upper*100:.1f}%'
    }
    
    # G4: at least 3 repos with unserved > 0
    repos_with_unserved = sum(1 for f in repo_fractions.values() if f > 0)
    results['g4'] = {
        'pass': repos_with_unserved >= 3,
        'value': f"{repos_with_unserved} repos with unserved > 0",
        'detail': f'Repos: {repo_fractions}'
    }
    
    return results
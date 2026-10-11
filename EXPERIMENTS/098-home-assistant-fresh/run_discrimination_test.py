#!/usr/bin/env python3
"""
Discrimination test for fault_need_classifier_v3 on Home Assistant error codes domain.
Tests the instrument against probes with labels known by construction.
"""

import json
import urllib.request
import urllib.parse
import time
import re
from typing import Dict, List, Tuple
from math import sqrt

# Probes with labels known by construction (from PROTOCOL.md)
PROBES = [
    # Known-served (5)
    {"query": "Home Assistant error integration not found", "domain": "HA", "expected": "served", "type": "known-served"},
    {"query": "ESPHome error code 0x80", "domain": "ESPHome", "expected": "served", "type": "known-served"},
    {"query": "Zigbee2MQTT error 0x15", "domain": "Zigbee", "expected": "served", "type": "known-served"},
    {"query": "Automation trigger failed template", "domain": "HA", "expected": "served", "type": "known-served"},
    {"query": "Supervisor error unhealthy DNS", "domain": "HA", "expected": "served", "type": "known-served"},
    # Known-unserved (5)
    {"query": "QuantumFlux error 0xDEADBEEF", "domain": "Synthetic", "expected": "unserved", "type": "known-unserved"},
    {"query": "HyperDrive fault 99999", "domain": "Synthetic", "expected": "unserved", "type": "known-unserved"},
    {"query": "NeuralLink error XYZ-123", "domain": "Synthetic", "expected": "unserved", "type": "known-unserved"},
    {"query": "WarpCore breach code 1701", "domain": "Synthetic", "expected": "unserved", "type": "known-unserved"},
    {"query": "Vintage 2015 Home Assistant error 999", "domain": "Real/obsolete", "expected": "unserved", "type": "known-unserved"},
]

# Solution keywords (from E090 instrument)
SOLUTION_KEYWORDS = [
    'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair', 
    'troubleshoot', 'step by step', 'method', 'procedure',
    'resolve', 'workaround', 'patch', 'update', 'upgrade',
    'configuration', 'config', 'setting', 'option', 'parameter'
]

# Error code patterns
ERROR_CODE_PATTERNS = [
    r'error\s+code\s+\d+',
    r'error\s+code\s+[A-Z0-9_]+',
    r'error\s+[A-Z]{3,}',
    r'fault\s+code\s+\d+',
    r'fault\s+code\s+[A-Z0-9_]+',
    r'\bError\s+Code\s+\d+\b',
    r'\bError\s+[A-Z]{3,}\b',
    r'error\s+\d+',
    r'exit\s+code\s+-?\d+',
    r'0x[0-9a-fA-F]+',
    r'\b(INVALID|UNSUPPORTED|TIMEOUT|FAILED|UNKNOWN|NOT_FOUND)\b',
]

def has_error_code(text: str) -> bool:
    """Check if text contains error code patterns."""
    text_lower = text.lower()
    for pattern in ERROR_CODE_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False

def has_solution_keyword(text: str) -> bool:
    """Check if text contains solution-oriented keywords."""
    text_lower = text.lower()
    for kw in SOLUTION_KEYWORDS:
        if kw in text_lower:
            return True
    return False

def search_discourse(query: str) -> Dict:
    """Search Home Assistant Discourse for query and return first page results."""
    url = f"https://community.home-assistant.io/search.json?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree/1.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  Search error for '{query}': {e}")
        return {}

def classify_probe(query: str, search_results: Dict) -> str:
    """
    Apply fault_need_classifier_v3 logic to probe.
    Served if error_code_present AND has_solution_keyword in results.
    """
    # Check if query itself has error code
    error_code_present = has_error_code(query)
    
    # Check search results for solution keywords
    has_solution = False
    posts = search_results.get('posts', [])
    for post in posts:
        blurb = post.get('blurb', '')
        if has_solution_keyword(blurb):
            has_solution = True
            break
        # Also check topic title
        topic_title = post.get('fancy_title', '')
        if has_solution_keyword(topic_title):
            has_solution = True
            break
    
    # Also check topics array
    topics = search_results.get('topics', [])
    for topic in topics:
        title = topic.get('title', '')
        if has_solution_keyword(title):
            has_solution = True
            break
    
    # Simplified classifier (E092 style): served if error_code_present AND has_solution_keyword
    if error_code_present and has_solution:
        return "served"
    elif error_code_present and not has_solution:
        return "unserved"
    else:
        return "unserved"

def wilson_ci(p: float, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denominator
    half = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))

def newcombe_ci(p1: float, n1: int, p2: float, n2: int) -> Tuple[float, float]:
    """Newcombe hybrid score interval for difference of proportions."""
    ci1 = wilson_ci(p1, n1)
    ci2 = wilson_ci(p2, n2)
    diff = p1 - p2
    lower = diff - sqrt((p1 - ci1[0])**2 + (ci2[1] - p2)**2)
    upper = diff + sqrt((ci1[1] - p1)**2 + (p2 - ci2[0])**2)
    return (lower, upper)

def main():
    print("Running discrimination test on Home Assistant error codes domain...")
    print("=" * 60)
    
    results = []
    for probe in PROBES:
        print(f"\nProbe: '{probe['query']}' (expected: {probe['expected']})")
        search_results = search_discourse(probe['query'])
        classification = classify_probe(probe['query'], search_results)
        
        result = {
            'query': probe['query'],
            'domain': probe['domain'],
            'expected': probe['expected'],
            'type': probe['type'],
            'classified': classification,
            'correct': classification == probe['expected'],
            'search_results_count': len(search_results.get('posts', [])) + len(search_results.get('topics', []))
        }
        results.append(result)
        print(f"  Classified: {classification} {'✓' if result['correct'] else '✗'}")
        print(f"  Search results: {result['search_results_count']}")
        time.sleep(0.5)  # Polite polling
    
    # Compute metrics
    known_served = [r for r in results if r['type'] == 'known-served']
    known_unserved = [r for r in results if r['type'] == 'known-unserved']
    
    tp = sum(1 for r in known_served if r['classified'] == 'served')
    fn = sum(1 for r in known_served if r['classified'] == 'unserved')
    fp = sum(1 for r in known_unserved if r['classified'] == 'served')
    tn = sum(1 for r in known_unserved if r['classified'] == 'unserved')
    
    tpr = tp / len(known_served) if known_served else 0
    fnr = fn / len(known_served) if known_served else 0
    fpr = fp / len(known_unserved) if known_unserved else 0
    tnr = tn / len(known_unserved) if known_unserved else 0
    
    # Wilson CIs
    tpr_ci = wilson_ci(tpr, len(known_served))
    fpr_ci = wilson_ci(fpr, len(known_unserved))
    diff_ci = newcombe_ci(tpr, len(known_served), fpr, len(known_unserved))
    
    print("\n" + "=" * 60)
    print("DISCRIMINATION TEST RESULTS")
    print("=" * 60)
    print(f"Known-served (n={len(known_served)}): TP={tp}, FN={fn}, TPR={tpr:.3f} (CI95: {tpr_ci[0]:.3f}-{tpr_ci[1]:.3f})")
    print(f"Known-unserved (n={len(known_unserved)}): FP={fp}, TN={tn}, FPR={fpr:.3f} (CI95: {fpr_ci[0]:.3f}-{fpr_ci[1]:.3f})")
    print(f"Difference (TPR-FPR) = {tpr - fpr:.3f} (Newcombe CI95: {diff_ci[0]:.3f}-{diff_ci[1]:.3f})")
    
    # Gate evaluation
    print("\nGATE EVALUATION:")
    g1_pass = fpr < 0.10
    g2_pass = tpr > 0.70
    g3_pass = fnr < 0.30
    
    print(f"G1 (FPR < 0.10): {fpr:.3f} {'PASS' if g1_pass else 'FAIL'}")
    print(f"G2 (TPR > 0.70): {tpr:.3f} {'PASS' if g2_pass else 'FAIL'}")
    print(f"G3 (FNR < 0.30): {fnr:.3f} {'PASS' if g3_pass else 'FAIL'}")
    
    overall_pass = g1_pass and (g2_pass or g3_pass)
    print(f"\nOVERALL: {'PASS' if overall_pass else 'FAIL'}")
    
    # Save results
    output = {
        'probes': results,
        'metrics': {
            'known_served_n': len(known_served),
            'known_unserved_n': len(known_unserved),
            'tp': tp, 'fn': fn, 'fp': fp, 'tn': tn,
            'tpr': tpr, 'fnr': fnr, 'fpr': fpr, 'tnr': tnr,
            'tpr_ci95': tpr_ci,
            'fpr_ci95': fpr_ci,
            'diff_ci95': diff_ci,
        },
        'gates': {
            'G1_fpr': {'value': fpr, 'threshold': 0.10, 'pass': g1_pass},
            'G2_tpr': {'value': tpr, 'threshold': 0.70, 'pass': g2_pass},
            'G3_fnr': {'value': fnr, 'threshold': 0.30, 'pass': g3_pass},
            'overall_pass': overall_pass,
        }
    }
    
    with open('raw/discrimination_test_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to raw/discrimination_test_results.json")

if __name__ == '__main__':
    main()
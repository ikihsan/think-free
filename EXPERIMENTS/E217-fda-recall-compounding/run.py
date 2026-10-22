#!/usr/bin/env python3
"""
E217: FDA Drug Recall Patterns — Compounding Pharmacy vs Commercial Manufacturer Risk Profile

Fetches FDA drug enforcement reports and tests whether compounding pharmacies
have higher Class I recall proportions than commercial manufacturers.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import time
import hashlib
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

BASE = "https://api.fda.gov/drug/enforcement.json"
UA = "think-free-research/0.1 (+E217-fda-recall-compounding)"

# Compounding pharmacy indicators
COMPOUNDING_KEYWORDS = [
    "pharmacy", "compounding", "apothecary", "wellness pharmacy",
    "compounding pharmacy", "pharmacy services", "rx pharmacy"
]

def is_compounding(firm_name):
    """Classify firm as compounding pharmacy based on name."""
    if not firm_name:
        return False
    name_lower = firm_name.lower()
    return any(kw in name_lower for kw in COMPOUNDING_KEYWORDS)

def fetch_page(limit=1000, skip=0):
    """Fetch one page of recall data."""
    url = f"{BASE}?limit={limit}&skip={skip}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            time.sleep(2)
            return fetch_page(limit, skip)
        raise
    except Exception:
        raise

def fetch_all_recalls(max_pages=20):
    """Fetch recall data up to max_pages pages."""
    all_results = []
    skip = 0
    limit = 1000
    
    for page in range(max_pages):
        print(f"Fetching page {page+1} (skip={skip})...", flush=True)
        data = fetch_page(limit, skip)
        results = data.get("results", [])
        if not results:
            break
        all_results.extend(results)
        meta = data.get("meta", {}).get("results", {})
        total = meta.get("total", 0)
        print(f"  Got {len(results)} recalls, total available: {total}")
        skip += limit
        if skip >= total:
            break
        time.sleep(0.5)  # Be polite
    return all_results

def classify_recalls(recalls):
    """Classify recalls and build contingency table."""
    compounding_class1 = 0
    compounding_other = 0
    commercial_class1 = 0
    commercial_other = 0
    classified = 0
    unclassified = 0
    
    for r in recalls:
        classification = r.get("classification")
        firm = r.get("recalling_firm")
        if not classification or not firm:
            unclassified += 1
            continue
        
        is_comp = is_compounding(firm)
        is_class1 = (classification == "Class I")
        
        if is_comp:
            if is_class1:
                compounding_class1 += 1
            else:
                compounding_other += 1
        else:
            if is_class1:
                commercial_class1 += 1
            else:
                commercial_other += 1
        classified += 1
    
    return {
        "compounding_class1": compounding_class1,
        "compounding_other": compounding_other,
        "commercial_class1": commercial_class1,
        "commercial_other": commercial_other,
        "classified": classified,
        "unclassified": unclassified,
    }

def fisher_exact(a, b, c, d):
    """Fisher's exact test (one-sided: odds ratio > 1).
    Table:
        a  b  (compounding: class1, other)
        c  d  (commercial: class1, other)
    Returns (p_value, odds_ratio, ci_lower, ci_upper)
    """
    import math
    
    # Odds ratio
    if b == 0 or c == 0:
        odds_ratio = float('inf')
    else:
        odds_ratio = (a * d) / (b * c)
    
    # Compute p-value using hypergeometric distribution
    # One-sided: probability of observing this or more extreme (higher odds ratio)
    n1 = a + b
    n2 = c + d
    m1 = a + c
    m2 = b + d
    n = n1 + n2
    
    # Log factorials for numerical stability
    def log_fact(x):
        if x <= 1:
            return 0.0
        return sum(math.log(i) for i in range(2, int(x) + 1))
    
    # Probability of observed table
    def log_prob(a_val):
        return (log_fact(n1) + log_fact(n2) + log_fact(m1) + log_fact(m2) -
                log_fact(a_val) - log_fact(n1 - a_val) -
                log_fact(m1 - a_val) - log_fact(n2 - m1 + a_val) -
                log_fact(n))
    
    log_p_obs = log_prob(a)
    
    # Sum probabilities of all tables with odds ratio >= observed
    p_value = 0.0
    max_a = min(n1, m1)
    for a_val in range(0, max_a + 1):
        b_val = n1 - a_val
        c_val = m1 - a_val
        d_val = n2 - c_val
        if b_val < 0 or c_val < 0 or d_val < 0:
            continue
        if a_val == 0 or b_val == 0 or c_val == 0 or d_val == 0:
            or_val = float('inf')
        else:
            or_val = (a_val * d_val) / (b_val * c_val)
        if or_val >= odds_ratio - 1e-10:
            p_value += math.exp(log_prob(a_val))
    
    # Woolf CI for odds ratio
    if a > 0 and b > 0 and c > 0 and d > 0:
        log_or = math.log(odds_ratio)
        se = math.sqrt(1/a + 1/b + 1/c + 1/d)
        ci_lower = math.exp(log_or - 1.96 * se)
        ci_upper = math.exp(log_or + 1.96 * se)
    else:
        ci_lower = 0.0
        ci_upper = float('inf')
    
    return p_value, odds_ratio, ci_lower, ci_upper

def main():
    print("=" * 72)
    print("E217: FDA Drug Recall Patterns — Compounding vs Commercial")
    print("=" * 72)
    print()
    
    # Create raw directory
    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    # Fetch recalls
    print("Fetching FDA drug enforcement reports...")
    recalls = fetch_all_recalls(max_pages=20)
    print(f"Total fetched: {len(recalls)}")
    
    # Save raw data
    raw_path = os.path.join(raw_dir, "recalls.jsonl")
    with open(raw_path, "w") as f:
        for r in recalls:
            f.write(json.dumps(r) + "\n")
    print(f"Raw data saved to {raw_path}")
    
    # Classify
    print("\nClassifying recalls...")
    counts = classify_recalls(recalls)
    
    a = counts["compounding_class1"]
    b = counts["compounding_other"]
    c = counts["commercial_class1"]
    d = counts["commercial_other"]
    classified = counts["classified"]
    unclassified = counts["unclassified"]
    
    print(f"\nContingency table:")
    print(f"                    | Class I  | Not Class I | Total")
    print(f"  Compounding       |    {a:3d}   |    {b:3d}     |  {a+b:3d}")
    print(f"  Commercial        |    {c:3d}   |    {d:3d}     |  {c+d:3d}")
    print(f"  Total             |   {a+c:3d}   |   {b+d:3d}     |  {classified:3d}")
    print(f"\n  Unclassified (missing data): {unclassified}")
    
    # Coverage
    coverage = classified / (classified + unclassified) if (classified + unclassified) > 0 else 0
    print(f"\nClassification coverage: {coverage:.4f} ({classified}/{classified+unclassified})")
    
    # Kill gate G1: sample size
    n_comp = a + b
    n_comm = c + d
    g1_pass = n_comp >= 50 and n_comm >= 50
    print(f"\nG1 (sample size ≥50 per group): {'PASS' if g1_pass else 'FAIL'}")
    print(f"  Compounding: {n_comp}, Commercial: {n_comm}")
    
    # Kill gate G4: coverage
    g4_pass = coverage >= 0.95
    print(f"G4 (coverage ≥95%): {'PASS' if g4_pass else 'FAIL'}")
    
    if n_comp == 0 or n_comm == 0:
        print("\nInsufficient data for statistical test.")
        return
    
    # Fisher's exact test
    print("\nRunning Fisher's exact test (one-sided)...")
    p_value, odds_ratio, ci_lower, ci_upper = fisher_exact(a, b, c, d)
    
    print(f"  Odds ratio: {odds_ratio:.4f}")
    print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"  p-value (one-sided): {p_value:.6f}")
    
    # Kill gate G2: statistical significance
    g2_pass = p_value < 0.05
    print(f"\nG2 (p < 0.05): {'PASS' if g2_pass else 'FAIL'}")
    
    # Kill gate G3: effect magnitude
    g3_pass = odds_ratio > 2.0
    print(f"G3 (odds ratio > 2.0): {'PASS' if g3_pass else 'FAIL'}")
    
    # Overall verdict
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n{'='*72}")
    print(f"OVERALL VERDICT: {'ALL GATES PASS' if all_pass else 'KILL GATE FIRED'}")
    print(f"{'='*72}")
    
    # Save results
    results = {
        "counts": {
            "compounding_class1": a,
            "compounding_other": b,
            "commercial_class1": c,
            "commercial_other": d,
            "total_classified": classified,
            "total_unclassified": unclassified,
        },
        "coverage": coverage,
        "odds_ratio": odds_ratio,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": p_value,
        "gates": {
            "G1_sample_size": g1_pass,
            "G2_significance": g2_pass,
            "G3_effect_magnitude": g3_pass,
            "G4_coverage": g4_pass,
        },
        "verdict": "PASS" if all_pass else "FAIL",
    }
    
    results_path = os.path.join(raw_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print(f"\nResults saved to {results_path}")
    
    return all_pass

if __name__ == "__main__":
    main()
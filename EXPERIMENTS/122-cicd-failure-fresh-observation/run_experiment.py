#!/usr/bin/env python3
"""
E122 — CI/CD pipeline failure classification experiment runner.

Implements the full experiment per PROTOCOL.md:
1. Generate synthetic fixtures
2. Run classifier on fixtures (KG1: ≥80% accuracy)
3. If KG1 passes, fetch real failed runs from GitHub Actions API
4. Classify real runs (KG2: ≥5 categories, KG3: ≤30% unknown, KG4: ≥20% prevalence + remediation)
5. Report results with all gates
"""

import json
import sys
import os
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# Add experiment directory to path
sys.path.insert(0, str(Path(__file__).parent))

from classifier import classify_log, FailureCategory, evaluate_on_fixtures
from synthetic_fixtures import get_fixtures
from gh_actions_fetch import (fetch_github_actions_failures)


def run_kg1_synthetic() -> Dict[str, Any]:
    """Run KG1: Classifier accuracy on synthetic fixtures."""
    print("=" * 60)
    print("KG1: Synthetic fixture classification accuracy")
    print("=" * 60)
    
    fixtures = get_fixtures()
    results = evaluate_on_fixtures(fixtures)
    
    accuracy = results['accuracy']
    print(f"Overall accuracy: {accuracy:.2%} ({results['correct']}/{results['total']})")
    print("\nPer-category accuracy:")
    for cat, acc in results['per_category_accuracy'].items():
        if acc is not None:
            count = results['per_category_counts'][cat]['total']
            print(f"  {cat}: {acc:.2%} ({results['per_category_counts'][cat]['correct']}/{count})")
        else:
            print(f"  {cat}: N/A (0 fixtures)")
    
    kg1_pass = accuracy >= 0.80
    print(f"\nKG1 (≥80% accuracy): {'PASS' if kg1_pass else 'FAIL'}")
    
    return {
        'gate': 'KG1',
        'pass': kg1_pass,
        'accuracy': accuracy,
        'details': results,
    }




def run_real_classification(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run classifier on real failed runs and evaluate gates KG2-KG4."""
    print("=" * 60)
    print("Classifying real failed runs...")
    print("=" * 60)
    
    classifications = []
    categories_found = set()
    unknown_count = 0
    
    for run in runs:
        result = classify_log(run['log_text'])
        classifications.append({
            'repo': run['repo'],
            'run_id': run['run_id'],
            'workflow': run['workflow_name'],
            'job': run['job_name'],
            'category': result.category.value,
            'confidence': result.confidence,
            'patterns': result.matched_patterns,
            'url': run['html_url'],
        })
        
        categories_found.add(result.category)
        if result.category == FailureCategory.UNKNOWN:
            unknown_count += 1
    
    total = len(classifications)
    unknown_pct = unknown_count / total if total > 0 else 1.0
    
    # Category distribution
    cat_counts = {}
    for c in classifications:
        cat_counts[c['category']] = cat_counts.get(c['category'], 0) + 1
    
    print(f"Total classified: {total}")
    print(f"Unknown: {unknown_count} ({unknown_pct:.1%})")
    print(f"Distinct categories found: {len(categories_found)}")
    print("\nCategory distribution:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        print(f"  {cat}: {count} ({pct:.1f}%)")
    
    # KG2: ≥5 distinct failure categories
    kg2_pass = len(categories_found) >= 5
    print(f"\nKG2 (≥5 categories): {'PASS' if kg2_pass else 'FAIL'} ({len(categories_found)} found)")
    
    # KG3: ≤30% unknown
    kg3_pass = unknown_pct <= 0.30
    print(f"KG3 (≤30% unknown): {'PASS' if kg3_pass else 'FAIL'} ({unknown_pct:.1%})")
    
    # KG4: At least one category has ≥20% prevalence AND known remediation
    # Remediation-known categories: test_failure, dependency_error, compile_error, environment_error, timeout, permission_error
    remediation_known = {
        FailureCategory.TEST_FAILURE, FailureCategory.DEPENDENCY_ERROR,
        FailureCategory.COMPILE_ERROR, FailureCategory.ENVIRONMENT_ERROR,
        FailureCategory.TIMEOUT, FailureCategory.PERMISSION_ERROR,
    }
    
    kg4_pass = False
    kg4_category = None
    for cat in remediation_known:
        count = cat_counts.get(cat.value, 0)
        pct = count / total if total > 0 else 0
        if pct >= 0.20:
            kg4_pass = True
            kg4_category = cat.value
            break
    
    print(f"KG4 (≥20% prevalence + remediation): {'PASS' if kg4_pass else 'FAIL'}")
    if kg4_pass:
        print(f"  Category: {kg4_category} ({cat_counts[kg4_category]}/{total} = {cat_counts[kg4_category]/total:.1%})")
    
    return {
        'classifications': classifications,
        'total': total,
        'categories_found': len(categories_found),
        'unknown_count': unknown_count,
        'unknown_pct': unknown_pct,
        'category_counts': cat_counts,
        'kg2': {'pass': kg2_pass, 'categories_found': len(categories_found)},
        'kg3': {'pass': kg3_pass, 'unknown_pct': unknown_pct},
        'kg4': {'pass': kg4_pass, 'category': kg4_category, 'prevalence': cat_counts.get(kg4_category, 0) / total if kg4_category and total > 0 else 0},
    }


def save_results(kg1_result: Dict, real_result: Dict = None) -> str:
    """Save experiment results to JSON."""
    output = {
        'experiment': 'E122',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'kg1': kg1_result,
    }
    
    if real_result:
        output['real_data'] = real_result
        all_pass = kg1_result['pass'] and real_result['kg2']['pass'] and real_result['kg3']['pass'] and real_result['kg4']['pass']
        output['overall'] = 'ALL_GATES_PASS' if all_pass else 'SOME_GATES_FAIL'
    else:
        output['overall'] = 'KG1_FAIL_NO_REAL_DATA'
    
    output_path = Path(__file__).parent / 'results.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {output_path}")
    return str(output_path)


def main():
    print("E122 — CI/CD Pipeline Failure Classification Experiment")
    print("=" * 60)
    
    # Step 1: KG1 on synthetic fixtures
    kg1_result = run_kg1_synthetic()
    
    if not kg1_result['pass']:
        print("\n" + "=" * 60)
        print("KG1 FAILED — Experiment stops here. Domain closed for candidate generation.")
        print("=" * 60)
        save_results(kg1_result)
        return 1
    
    print("\nKG1 PASSED — Proceeding to real data collection...")
    
    # Step 2: Fetch real failed runs
    runs = fetch_github_actions_failures(limit=100)
    
    if not runs:
        print("\nNo real runs fetched. Cannot evaluate KG2-KG4.")
        save_results(kg1_result)
        return 1
    
    # Step 3: Classify real runs and evaluate KG2-KG4
    real_result = run_real_classification(runs)
    
    # Step 4: Save and report
    save_results(kg1_result, real_result)
    
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE")
    print("=" * 60)
    
    all_pass = kg1_result['pass'] and real_result['kg2']['pass'] and real_result['kg3']['pass'] and real_result['kg4']['pass']
    if all_pass:
        print("VERDICT: ALL GATES PASS — Domain supports further investigation toward a candidate.")
        return 0
    else:
        print("VERDICT: SOME GATES FAIL — Domain closed for candidate generation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
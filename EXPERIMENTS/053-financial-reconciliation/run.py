#!/usr/bin/env python3
"""Main experiment runner for financial reconciliation."""

import argparse
import json
import time
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate import generate_scenario
from match import match_with_config, DEFAULT_CONFIG
from evaluate import evaluate_all, check_kill_gate


def run_scenario(scenario: str, seed: int, config: dict = None) -> dict:
    """Run a single scenario and return results."""
    print(f"\n=== Running {scenario} scenario (seed={seed}) ===")
    
    # Generate data
    bank_txns, ledger_txns, true_matches = generate_scenario(scenario, seed)
    print(f"Generated: {len(bank_txns)} bank, {len(ledger_txns)} ledger, {len(true_matches)} true matches")
    
    # Convert to dicts
    bank_dicts = [txn.to_dict() for txn in bank_txns]
    ledger_dicts = [txn.to_dict() for txn in ledger_txns]
    
    # Collect all IDs
    all_bank_ids = {txn.id for txn in bank_txns}
    all_ledger_ids = {txn.id for txn in ledger_txns}
    
    # Run matching
    start_time = time.perf_counter()
    result = match_with_config(bank_dicts, ledger_dicts, config)
    elapsed = time.perf_counter() - start_time
    
    print(f"Matching completed in {elapsed:.4f}s")
    print(f"Found {len(result['matches'])} 1:1 matches, {len(result['splits'])} splits")
    
    # Evaluate
    metrics = evaluate_all(result, true_matches, all_bank_ids, all_ledger_ids)
    
    # Check kill gate
    gate_passed, failures = check_kill_gate(metrics, scenario)
    
    print(f"\nResults for {scenario}:")
    o2o = metrics['one_to_one']
    print(f"  1:1 Precision: {o2o['precision']:.4f}")
    print(f"  1:1 Recall:    {o2o['recall']:.4f}")
    print(f"  1:1 F1:        {o2o['f1']:.4f}")
    print(f"  1:1 FPR:       {o2o['false_positive_rate']:.4f}")
    print(f"  1:1 TP/FP/FN:  {o2o['tp']}/{o2o['fp']}/{o2o['fn']}")
    
    if metrics['splits']['true_positives'] + metrics['splits']['false_positives'] + metrics['splits']['false_negatives'] > 0:
        print(f"  Splits Precision: {metrics['splits']['precision']:.4f}")
        print(f"  Splits Recall:    {metrics['splits']['recall']:.4f}")
        print(f"  Splits F1:        {metrics['splits']['f1']:.4f}")
        print(f"  Splits TP/FP/FN:  {metrics['splits']['true_positives']}/{metrics['splits']['false_positives']}/{metrics['splits']['false_negatives']}")
    
    print(f"  Kill gate: {'PASSED' if gate_passed else 'FAILED'}")
    for f in failures:
        print(f"    - {f}")
    
    return {
        'scenario': scenario,
        'seed': seed,
        'config': config or DEFAULT_CONFIG,
        'counts': {
            'bank_transactions': len(bank_txns),
            'ledger_transactions': len(ledger_txns),
            'true_matches': len(true_matches),
            'predicted_matches': len(result['matches']),
            'predicted_splits': len(result['splits']),
        },
        'timing': {
            'matching_seconds': elapsed,
        },
        'metrics': metrics,
        'kill_gate': {
            'passed': gate_passed,
            'failures': failures,
        },
        'matches_detail': result['matches'][:20],  # First 20 for inspection
        'splits_detail': result['splits'],
    }


def main():
    parser = argparse.ArgumentParser(description="Financial reconciliation falsification experiment")
    parser.add_argument('--scenario', choices=['clean', 'realistic', 'adversarial', 'all'],
                        default='all', help='Scenario to run')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', type=str, default='results.json', help='Output file')
    parser.add_argument('--config', type=str, help='JSON config file for matching parameters')
    
    args = parser.parse_args()
    
    # Load custom config if provided
    config = None
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    
    scenarios = ['clean', 'realistic', 'adversarial'] if args.scenario == 'all' else [args.scenario]
    
    all_results = {
        'experiment': '053-financial-reconciliation',
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'scenarios': []
    }
    
    overall_pass = True
    for scenario in scenarios:
        result = run_scenario(scenario, args.seed, config)
        all_results['scenarios'].append(result)
        if not result['kill_gate']['passed']:
            overall_pass = False
    
    all_results['overall_kill_gate_passed'] = overall_pass
    
    # Save results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"OVERALL: {'PASS' if overall_pass else 'FAIL'}")
    print(f"Results saved to {output_path}")
    print(f"{'='*50}")
    
    # Exit code for CI
    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
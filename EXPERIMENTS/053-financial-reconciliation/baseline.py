#!/usr/bin/env python3
"""Baseline comparison for financial reconciliation."""

from generate import generate_scenario
from match import match_with_config, DEFAULT_CONFIG
from evaluate import evaluate_all, check_kill_gate


def naive_exact_match(bank_txns: list, ledger_txns: list) -> dict:
    """Naive baseline: exact match on amount and date only."""
    matches = []
    matched_bank = set()
    matched_ledger = set()
    
    for b in bank_txns:
        if b['id'] in matched_bank:
            continue
        for l in ledger_txns:
            if l['id'] in matched_ledger:
                continue
            if abs(b['amount'] - l['amount']) < 0.01 and b['date'] == l['date']:
                matches.append({'bank_id': b['id'], 'ledger_id': l['id'], 'score': 100})
                matched_bank.add(b['id'])
                matched_ledger.add(l['id'])
                break
    
    return {'matches': matches, 'splits': [], 'config_used': {}}


def run_comparison(scenario: str, seed: int) -> dict:
    """Run both algorithms and compare."""
    bank_txns, ledger_txns, true_matches = generate_scenario(scenario, seed)
    bank_dicts = [txn.to_dict() for txn in bank_txns]
    ledger_dicts = [txn.to_dict() for txn in ledger_txns]
    all_bank_ids = {txn.id for txn in bank_txns}
    all_ledger_ids = {txn.id for txn in ledger_txns}
    
    # Our algorithm
    our_result = match_with_config(bank_dicts, ledger_dicts, DEFAULT_CONFIG)
    our_metrics = evaluate_all(our_result, true_matches, all_bank_ids, all_ledger_ids)
    
    # Naive baseline
    naive_result = naive_exact_match(bank_dicts, ledger_dicts)
    naive_metrics = evaluate_all(naive_result, true_matches, all_bank_ids, all_ledger_ids)
    
    return {
        'scenario': scenario,
        'seed': seed,
        'our': {
            'precision': our_metrics['one_to_one']['precision'],
            'recall': our_metrics['one_to_one']['recall'],
            'f1': our_metrics['one_to_one']['f1'],
            'matches': len(our_result['matches']),
            'splits': len(our_result['splits']),
        },
        'naive': {
            'precision': naive_metrics['one_to_one']['precision'],
            'recall': naive_metrics['one_to_one']['recall'],
            'f1': naive_metrics['one_to_one']['f1'],
            'matches': len(naive_result['matches']),
        }
    }


if __name__ == "__main__":
    for scenario in ['clean', 'realistic', 'adversarial']:
        print(f"\n=== {scenario.upper()} ===")
        for seed in [42, 123, 456]:
            cmp = run_comparison(scenario, seed)
            print(f"  Seed {seed}:")
            print(f"    Our:     P={cmp['our']['precision']:.3f} R={cmp['our']['recall']:.3f} F1={cmp['our']['f1']:.3f} (matches={cmp['our']['matches']}, splits={cmp['our']['splits']})")
            print(f"    Naive:   P={cmp['naive']['precision']:.3f} R={cmp['naive']['recall']:.3f} F1={cmp['naive']['f1']:.3f} (matches={cmp['naive']['matches']})")
            if cmp['our']['f1'] > cmp['naive']['f1']:
                print(f"    → Our algorithm wins by {cmp['our']['f1'] - cmp['naive']['f1']:.3f} F1")
            else:
                print(f"    → Naive wins or ties")
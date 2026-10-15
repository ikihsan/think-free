#!/usr/bin/env python3
"""
Run E065's detector on OFX transactions and evaluate against labels.
"""

import json
import random
import sys
from datetime import date
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))

from detect import detect_recurring_expenses, evaluate_detection
from normalize import normalize_merchant

TRANSACTIONS_FILE = Path(__file__).parent / "transactions.jsonl"
LABELS_FILE = Path(__file__).parent / "labels.jsonl"
GATES_FILE = Path(__file__).parent / "gates.json"

def load_transactions() -> List[Dict[str, Any]]:
    """Load and normalize transactions."""
    transactions = []
    with open(TRANSACTIONS_FILE) as f:
        for line in f:
            txn = json.loads(line)
            # Parse date
            txn['date'] = date.fromisoformat(txn['date'])
            # Normalize merchant using E065's normalizer
            txn['merchant'] = normalize_merchant(txn['merchant'])
            transactions.append(txn)
    return transactions

def load_labels() -> Dict[str, str]:
    """Load ground truth labels."""
    labels = {}
    with open(LABELS_FILE) as f:
        for line in f:
            entry = json.loads(line)
            labels[entry['merchant']] = entry['label']
    return labels

def get_positive_merchants(labels: Dict[str, str]) -> List[str]:
    """Get list of positive merchants (normalized)."""
    # We need to normalize the label keys too to match
    positive = []
    for merchant, label in labels.items():
        if label == "positive":
            norm_merchant = normalize_merchant(merchant)
            positive.append(norm_merchant)
    return positive

def run_naive_baseline(transactions: List[Dict[str, Any]], positive_merchants: List[str]) -> Dict[str, Any]:
    """Run naive baseline: same merchant ≥3 times."""
    expenses = [t for t in transactions if t["amount"] < 0]
    by_merchant = {}
    for t in expenses:
        m = t["merchant"]
        by_merchant[m] = by_merchant.get(m, 0) + 1
    
    detected_merchants = set(m for m, count in by_merchant.items() if count >= 3)
    true_merchants = set(positive_merchants)
    
    tp = len(detected_merchants & true_merchants)
    fp = len(detected_merchants - true_merchants)
    fn = len(true_merchants - detected_merchants)
    
    all_merchants = set(t["merchant"] for t in expenses)
    non_recurring = all_merchants - true_merchants
    tn = len(non_recurring - detected_merchants)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fpr, 4),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "detected": sorted(list(detected_merchants)),
        "expected": sorted(list(true_merchants)),
    }

def permutation_control(transactions: List[Dict[str, Any]], positive_merchants: List[str]) -> float:
    """Permutation control: shuffle dates within each merchant, run detector, count detections."""
    # Group by merchant
    by_merchant = {}
    for t in transactions:
        m = t["merchant"]
        by_merchant.setdefault(m, []).append(t)
    
    # Shuffle dates within each merchant group
    shuffled_transactions = []
    for merchant, txns in by_merchant.items():
        dates = [t["date"] for t in txns]
        random.shuffle(dates)
        for txn, new_date in zip(txns, dates):
            shuffled_txn = txn.copy()
            shuffled_txn["date"] = new_date
            shuffled_transactions.append(shuffled_txn)
    
    # Run detector on shuffled data
    detected = detect_recurring_expenses(shuffled_transactions)
    shuffled_detected = set(d["merchant"] for d in detected)
    
    # Run on original
    detected_orig = detect_recurring_expenses(transactions)
    orig_detected = set(d["merchant"] for d in detected_orig)
    
    if len(orig_detected) == 0:
        return 0.0
    
    return len(shuffled_detected) / len(orig_detected)

def main():
    print("Loading transactions...")
    transactions = load_transactions()
    print(f"Loaded {len(transactions)} transactions")
    
    print("Loading labels...")
    labels = load_labels()
    positive_merchants = get_positive_merchants(labels)
    print(f"Positive merchants (normalized): {positive_merchants}")
    
    # Show normalized merchants
    print("\nNormalized merchants:")
    merchants_seen = set()
    for t in transactions:
        if t['merchant'] not in merchants_seen:
            merchants_seen.add(t['merchant'])
            print(f"  {t['merchant']}")
    
    print("\nRunning detector...")
    detected = detect_recurring_expenses(transactions)
    print(f"Detected {len(detected)} recurring expenses:")
    for d in detected:
        print(f"  {d['merchant']} | {d['interval']} | score={d['score']} | cv={d['amount_cv']} | count={d['transaction_count']}")
    
    # Evaluate
    eval_result = evaluate_detection(detected, positive_merchants, transactions)
    print(f"\nDetector results:")
    print(f"  Precision: {eval_result['precision']:.4f}")
    print(f"  Recall: {eval_result['recall']:.4f}")
    print(f"  F1: {eval_result['f1']:.4f}")
    print(f"  FPR: {eval_result['fpr']:.4f}")
    print(f"  TP: {eval_result['tp']}, FP: {eval_result['fp']}, FN: {eval_result['fn']}, TN: {eval_result['tn']}")
    print(f"  Missed: {eval_result['missed']}")
    print(f"  False positives: {eval_result['false_positives']}")
    
    print("\nRunning naive baseline...")
    baseline = run_naive_baseline(transactions, positive_merchants)
    print(f"Baseline results:")
    print(f"  Precision: {baseline['precision']:.4f}")
    print(f"  Recall: {baseline['recall']:.4f}")
    print(f"  F1: {baseline['f1']:.4f}")
    print(f"  FPR: {baseline['fpr']:.4f}")
    print(f"  Detected: {baseline['detected']}")
    
    print("\nRunning permutation control...")
    perm_ratio = permutation_control(transactions, positive_merchants)
    print(f"Permutation ratio (shuffled/original detections): {perm_ratio:.4f}")
    
    # Gate evaluation
    gates = {
        "G1_recall": {"threshold": 0.90, "actual": eval_result['recall'], "passed": eval_result['recall'] >= 0.90},
        "G2_precision": {"threshold": 0.70, "actual": eval_result['precision'], "passed": eval_result['precision'] >= 0.70},
        "G3_f1_margin": {"threshold": 0.05, "actual": eval_result['f1'] - baseline['f1'], "passed": (eval_result['f1'] - baseline['f1']) >= 0.05},
        "G4_permutation": {"threshold": 0.10, "actual": perm_ratio, "passed": perm_ratio <= 0.10},
    }
    
    print("\n=== GATE EVALUATION ===")
    all_passed = True
    for name, gate in gates.items():
        status = "✅ PASS" if gate["passed"] else "❌ FAIL"
        print(f"  {name}: {gate['actual']:.4f} (threshold: {gate['threshold']}) {status}")
        if not gate["passed"]:
            all_passed = False
    
    print(f"\nOverall: {'✅ ALL GATES PASSED' if all_passed else '❌ SOME GATES FAILED'}")
    
    # Save results
    results = {
        "detector": eval_result,
        "baseline": baseline,
        "permutation_ratio": perm_ratio,
        "gates": gates,
        "all_gates_passed": all_passed,
    }
    
    with open(GATES_FILE, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to {GATES_FILE}")
    
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
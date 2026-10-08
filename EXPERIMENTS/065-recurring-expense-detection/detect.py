#!/usr/bin/env python3
"""
Recurring expense detection algorithm.
Deterministic, stdlib-only detection of recurring expenses from normalized transactions.
"""

from collections import defaultdict
from datetime import timedelta
from typing import Dict, List, Any

from scoring import (
    TARGET_INTERVALS,
    detect_interval_pattern,
    amount_consistency,
    compute_recurring_score,
)


# Utility keywords for variable-amount merchants (utilities)
VARIABLE_MERCHANT_KEYWORDS = [
    "ELECTRIC", "GAS", "WATER", "POWER", "ENERGY", "UTILITY",
    "EDISON", "PGE", "SCE", "SDGE", "CONED", "NATIONAL GRID",
    "DUKE ENERGY", "SOUTHERN COMPANY", "DOMINION", "EXELON",
    "NEXTERA", "XCEL", "ENTERGY", "FIRSTENERGY", "PPL",
    "CMS ENERGY", "CENTERPOINT", "AMEREN", "AES", "VISTRA",
    "NRG", "CALPINE", "DYNEGY", "TENASKA", "LS POWER",
]


def is_variable_merchant(merchant: str) -> bool:
    """Check if merchant is a known variable-amount utility."""
    return any(kw in merchant for kw in VARIABLE_MERCHANT_KEYWORDS)


def detect_recurring_expenses(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Main detection function.
    Input: list of normalized transactions with keys: date, amount, merchant
    Output: list of detected recurring expenses with details
    """
    # Filter to expenses only (negative amounts)
    expenses = [t for t in transactions if t["amount"] < 0]

    # Group by normalized merchant
    by_merchant = defaultdict(list)
    for txn in expenses:
        by_merchant[txn["merchant"]].append(txn)

    results = []

    for merchant, txns in by_merchant.items():
        if len(txns) < 3:
            continue  # Need at least 3 occurrences

        # Sort by date
        txns.sort(key=lambda x: x["date"])

        # Compute gaps between consecutive transactions
        gaps = []
        for i in range(1, len(txns)):
            gap = (txns[i]["date"] - txns[i-1]["date"]).days
            gaps.append(gap)

        # Detect interval pattern
        interval_name, interval_regularity, expected_interval = detect_interval_pattern(gaps)

        if interval_name is None or interval_regularity < 0.45:
            continue  # No clear pattern

        # Check amount consistency
        amounts = [t["amount"] for t in txns]
        cv, mad, median_amount = amount_consistency(amounts)

        variable = is_variable_merchant(merchant)

        # Reject if amount variance too high
        if not variable and cv > 0.15:
            continue  # Amount too variable for a subscription
        if variable and cv > 0.40:
            continue  # Even utilities have some consistency

        # Compute overall score
        score = compute_recurring_score(len(txns), interval_regularity, cv, interval_name, variable)

        if score < 0.5:
            continue

        # Next expected date
        last_date = txns[-1]["date"]
        next_expected = last_date + timedelta(days=int(expected_interval))

        # Amount range
        abs_amounts = [abs(a) for a in amounts]
        amount_min = min(abs_amounts)
        amount_max = max(abs_amounts)

        results.append({
            "merchant": merchant,
            "interval": interval_name,
            "interval_days": expected_interval,
            "transaction_count": len(txns),
            "interval_regularity": round(interval_regularity, 3),
            "amount_cv": round(cv, 4) if cv != float('inf') else None,
            "amount_mad": round(mad, 2),
            "median_amount": round(median_amount, 2),
            "amount_range": (round(amount_min, 2), round(amount_max, 2)),
            "score": round(score, 3),
            "first_date": txns[0]["date"].isoformat(),
            "last_date": last_date.isoformat(),
            "next_expected_date": next_expected.isoformat(),
            "is_variable": variable,
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def evaluate_detection(
    detected: List[Dict[str, Any]],
    ground_truth_merchants: List[str],
    all_transactions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluate detection against ground truth.
    Returns precision, recall, F1, FPR.
    """
    detected_merchants = set(d["merchant"] for d in detected)
    true_merchants = set(ground_truth_merchants)

    tp = len(detected_merchants & true_merchants)
    fp = len(detected_merchants - true_merchants)
    fn = len(true_merchants - detected_merchants)

    # For FPR, need true negatives: non-recurring merchants correctly not detected
    all_merchants = set(t["merchant"] for t in all_transactions if t["amount"] < 0)
    non_recurring_merchants = all_merchants - true_merchants
    tn = len(non_recurring_merchants - detected_merchants)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fpr, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "detected": sorted(list(detected_merchants)),
        "expected": sorted(list(true_merchants)),
        "missed": sorted(list(true_merchants - detected_merchants)),
        "false_positives": sorted(list(detected_merchants - true_merchants)),
    }


if __name__ == "__main__":
    # Test with synthetic corpus
    from normalize import load_corpus
    from pathlib import Path

    manifest_path = Path("/home/ubuntu/think-free/EXPERIMENTS/065-recurring-expense-detection/corpus/synthetic/manifest.json")
    corpus = load_corpus(manifest_path)

    all_results = []
    for fname, data in corpus.items():
        txns = data["transactions"]
        ground_truth = data["metadata"]["recurring_merchants"]

        detected = detect_recurring_expenses(txns)
        eval_result = evaluate_detection(detected, ground_truth, txns)

        all_results.append({
            "file": fname,
            "eval": eval_result,
            "detections": detected,
        })

    # Aggregate
    total_tp = sum(r["eval"]["tp"] for r in all_results)
    total_fp = sum(r["eval"]["fp"] for r in all_results)
    total_fn = sum(r["eval"]["fn"] for r in all_results)
    total_tn = sum(r["eval"]["tn"] for r in all_results)

    print(f"Overall: TP={total_tp}, FP={total_fp}, FN={total_fn}, TN={total_tn}")
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr = total_fp / (total_fp + total_tn) if (total_fp + total_tn) > 0 else 0

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1: {f1:.4f}")
    print(f"FPR: {fpr:.4f}")

    # Show failures
    print("\n--- Failures ---")
    for r in all_results:
        if r["eval"]["fn"] > 0 or r["eval"]["fp"] > 0:
            print(f"\n{r['file']}:")
            print(f"  Missed: {r['eval']['missed']}")
            print(f"  False positives: {r['eval']['false_positives']}")
            for d in r["detections"]:
                print(f"  Detected: {d['merchant']} | {d['interval']} | score={d['score']} | cv={d['amount_cv']}")
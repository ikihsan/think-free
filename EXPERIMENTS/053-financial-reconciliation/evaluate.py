#!/usr/bin/env python3
"""Evaluation metrics for financial reconciliation experiment."""

from typing import List, Tuple, Dict, Set
from dataclasses import dataclass


@dataclass
class Metrics:
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int  # not really applicable but included for completeness


def evaluate_matches(predicted_matches: List[Tuple[str, str]], 
                     true_matches: List[Tuple[str, str]],
                     all_bank_ids: Set[str],
                     all_ledger_ids: Set[str]) -> Metrics:
    """
    Evaluate 1:1 matches.
    
    predicted_matches: list of (bank_id, ledger_id)
    true_matches: list of (bank_id, ledger_id) - ground truth
    """
    pred_set = set(predicted_matches)
    true_set = set(true_matches)
    
    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    
    # For false positive rate, we need true negatives
    # Total possible pairs = len(all_bank_ids) * len(all_ledger_ids)
    # But this is huge. Instead, compute FPR as FP / (FP + TN) where TN = total possible negative pairs correctly identified
    # More practically: FPR = FP / (total predicted negatives) but we don't predict negatives explicitly
    # Use: FPR = FP / (FP + number of true non-matches)
    # Number of true non-matches = total possible pairs - true matches
    total_pairs = len(all_bank_ids) * len(all_ledger_ids)
    tn = total_pairs - len(true_set) - fp  # pairs that are not matches and not predicted as matches
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    
    return Metrics(
        precision=precision,
        recall=recall,
        f1=f1,
        false_positive_rate=fpr,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=tn
    )


def evaluate_splits(predicted_splits: List[Tuple[str, List[str]]],
                    true_splits: List[Tuple[str, List[str]]]) -> Dict:
    """
    Evaluate split matches (1:many).
    predicted_splits: list of (primary_id, [secondary_ids])
    true_splits: list of (primary_id, [secondary_ids])
    """
    # Convert to sets of frozensets for comparison
    pred_split_sets = set()
    for primary, secondaries in predicted_splits:
        pred_split_sets.add(frozenset([primary] + secondaries))
    
    true_split_sets = set()
    for primary, secondaries in true_splits:
        true_split_sets.add(frozenset([primary] + secondaries))
    
    tp = len(pred_split_sets & true_split_sets)
    fp = len(pred_split_sets - true_split_sets)
    fn = len(true_split_sets - pred_split_sets)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }


def evaluate_all(result: dict, true_matches: List, all_bank_ids: Set[str], all_ledger_ids: Set[str]) -> dict:
    """Evaluate both 1:1 matches and splits."""
    # Extract 1:1 matches from result
    pred_matches = [(m['bank_id'], m['ledger_id']) for m in result['matches']]
    
    # Extract true 1:1 matches (filter out splits)
    true_1to1 = [m for m in true_matches if isinstance(m[1], str)]
    true_splits = [m for m in true_matches if isinstance(m[1], list)]
    
    # Extract predicted splits
    pred_splits = [(s['primary_id'], s['secondary_ids']) for s in result['splits']]
    
    # Evaluate 1:1
    metrics_1to1 = evaluate_matches(pred_matches, true_1to1, all_bank_ids, all_ledger_ids)
    
    # Evaluate splits
    metrics_splits = evaluate_splits(pred_splits, true_splits)
    
    # Combined metrics (weighted by count)
    total_true = len(true_1to1) + len(true_splits)
    total_pred = len(pred_matches) + len(pred_splits)
    
    return {
        'one_to_one': {
            'precision': metrics_1to1.precision,
            'recall': metrics_1to1.recall,
            'f1': metrics_1to1.f1,
            'false_positive_rate': metrics_1to1.false_positive_rate,
            'tp': metrics_1to1.true_positives,
            'fp': metrics_1to1.false_positives,
            'fn': metrics_1to1.false_negatives,
        },
        'splits': metrics_splits,
        'combined': {
            'total_true_matches': total_true,
            'total_predicted': total_pred,
        }
    }


def check_kill_gate(metrics: dict, scenario: str) -> Tuple[bool, List[str]]:
    """Check if kill gate is passed for a scenario."""
    failures = []
    o2o = metrics['one_to_one']
    
    if scenario == "clean":
        if o2o['precision'] < 0.90:
            failures.append(f"Clean precision {o2o['precision']:.3f} < 0.90")
        if o2o['recall'] < 0.85:
            failures.append(f"Clean recall {o2o['recall']:.3f} < 0.85")
        if o2o['false_positive_rate'] > 0.05:
            failures.append(f"Clean FPR {o2o['false_positive_rate']:.3f} > 0.05")
    elif scenario == "realistic":
        if o2o['precision'] < 0.70:
            failures.append(f"Realistic precision {o2o['precision']:.3f} < 0.70")
        if o2o['recall'] < 0.65:
            failures.append(f"Realistic recall {o2o['recall']:.3f} < 0.65")
        if o2o['false_positive_rate'] > 0.10:
            failures.append(f"Realistic FPR {o2o['false_positive_rate']:.3f} > 0.10")
    elif scenario == "adversarial":
        if o2o['precision'] < 0.50:
            failures.append(f"Adversarial precision {o2o['precision']:.3f} < 0.50")
        if o2o['recall'] < 0.45:
            failures.append(f"Adversarial recall {o2o['recall']:.3f} < 0.45")
        if o2o['false_positive_rate'] > 0.15:
            failures.append(f"Adversarial FPR {o2o['false_positive_rate']:.3f} > 0.15")
    
    return len(failures) == 0, failures


if __name__ == "__main__":
    # Test with dummy data
    pred = [("B0001", "L0001"), ("B0002", "L0002"), ("B0003", "L0003")]
    true = [("B0001", "L0001"), ("B0002", "L0002"), ("B0004", "L0004")]
    bank_ids = {"B0001", "B0002", "B0003", "B0004"}
    ledger_ids = {"L0001", "L0002", "L0003", "L0004"}
    
    m = evaluate_matches(pred, true, bank_ids, ledger_ids)
    print(f"Precision: {m.precision:.3f}, Recall: {m.recall:.3f}, F1: {m.f1:.3f}, FPR: {m.false_positive_rate:.3f}")
    print(f"TP: {m.true_positives}, FP: {m.false_positives}, FN: {m.false_negatives}")
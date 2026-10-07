#!/usr/bin/env python3
"""
Evaluate claim contradiction extractor against ground truth.
Stdlib only.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


def load_jsonl(filepath: str) -> List[Dict]:
    """Load JSONL file."""
    data = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def normalize_contradiction(contra: Dict) -> Tuple[str, str, str]:
    """Create a normalized key for a contradiction."""
    subject = contra.get("subject", "").lower().strip()
    obj = contra.get("object", "").lower().strip()
    ctype = contra.get("contradiction_type", "").lower().strip()
    return (subject, obj, ctype)


def evaluate(predictions: List[Dict], ground_truth: List[Dict]) -> Dict:
    """Evaluate predictions against ground truth."""
    
    # Build ground truth set
    gt_set = set()
    gt_by_pair = defaultdict(list)
    for gt in ground_truth:
        if gt.get("contradiction", False):
            key = (gt["variable_pair"][0].lower(), gt["variable_pair"][1].lower(), gt["contradiction_type"].lower())
            gt_set.add(key)
            gt_by_pair[(gt["variable_pair"][0].lower(), gt["variable_pair"][1].lower())].append(gt)
    
    # Build prediction set
    pred_set = set()
    pred_by_pair = defaultdict(list)
    for pred in predictions:
        key = (pred["subject"].lower(), pred["object"].lower(), pred["contradiction_type"].lower())
        pred_set.add(key)
        pred_by_pair[(pred["subject"].lower(), pred["object"].lower())].append(pred)
    
    # Calculate metrics
    true_positives = len(gt_set & pred_set)
    false_positives = len(pred_set - gt_set)
    false_negatives = len(gt_set - pred_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Per-pair analysis
    pair_results = {}
    for pair_key in set(list(gt_by_pair.keys()) + list(pred_by_pair.keys())):
        gt_contras = set(gt["contradiction_type"].lower() for gt in gt_by_pair.get(pair_key, []))
        pred_contras = set(pred["contradiction_type"].lower() for pred in pred_by_pair.get(pair_key, []))
        
        tp = len(gt_contras & pred_contras)
        fp = len(pred_contras - gt_contras)
        fn = len(gt_contras - pred_contras)
        
        pair_results[f"{pair_key[0]}|{pair_key[1]}"] = {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "gt_types": list(gt_contras),
            "pred_types": list(pred_contras)
        }
    
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "total_ground_truth": len(gt_set),
        "total_predictions": len(pred_set),
        "pair_results": pair_results
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate contradiction extractor")
    parser.add_argument("--predictions", required=True, help="Predictions JSONL file")
    parser.add_argument("--ground-truth", required=True, help="Ground truth JSONL file")
    parser.add_argument("--output", required=True, help="Output JSON file with results")
    args = parser.parse_args()
    
    predictions = load_jsonl(args.predictions)
    ground_truth = load_jsonl(args.ground_truth)
    
    results = evaluate(predictions, ground_truth)
    
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"True Positives: {results['true_positives']}")
    print(f"False Positives: {results['false_positives']}")
    print(f"False Negatives: {results['false_negatives']}")
    print(f"Precision: {results['precision']:.3f}")
    print(f"Recall: {results['recall']:.3f}")
    print(f"F1: {results['f1']:.3f}")
    print(f"Total Ground Truth Contradictions: {results['total_ground_truth']}")
    print(f"Total Predictions: {results['total_predictions']}")
    
    # Check kill gates
    print("\n--- KILL GATE CHECK ---")
    recall_gate = results['recall'] >= 0.60
    precision_gate = results['precision'] >= 0.80
    print(f"Recall ≥ 60%: {'PASS' if recall_gate else 'FAIL'} ({results['recall']:.1%})")
    print(f"Precision ≥ 80%: {'PASS' if precision_gate else 'FAIL'} ({results['precision']:.1%})")
    print(f"Overall: {'PASS' if (recall_gate and precision_gate) else 'FAIL'}")


if __name__ == "__main__":
    main()
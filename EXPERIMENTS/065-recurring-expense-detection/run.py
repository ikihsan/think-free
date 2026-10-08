#!/usr/bin/env python3
"""
Main experiment runner for recurring expense detection.
"""

import argparse
import json
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from normalize import load_corpus, parse_csv_file
from detect import detect_recurring_expenses, evaluate_detection


def run_detection(corpus_dir: Path, gate_mode: bool = False) -> dict:
    """Run detection on all files in corpus."""
    manifest_path = corpus_dir / "manifest.json"
    if not manifest_path.exists():
        # Try to find manifest in parent
        manifest_path = corpus_dir.parent / "manifest.json"
    
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_path}")
    
    corpus = load_corpus(manifest_path)
    
    all_results = []
    total_tp = total_fp = total_fn = total_tn = 0
    
    for fname, data in corpus.items():
        txns = data["transactions"]
        ground_truth = data["metadata"].get("recurring_merchants", [])
        
        detected = detect_recurring_expenses(txns)
        eval_result = evaluate_detection(detected, ground_truth, txns)
        
        all_results.append({
            "file": fname,
            "format": data["format"],
            "eval": eval_result,
            "detections": detected,
            "metadata": data["metadata"],
        })
        
        total_tp += eval_result["tp"]
        total_fp += eval_result["fp"]
        total_fn += eval_result["fn"]
        total_tn += eval_result["tn"]
    
    # Overall metrics
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = total_fp / (total_fp + total_tn) if (total_fp + total_tn) > 0 else 0.0
    
    overall = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fpr, 4),
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
        "tn": total_tn,
        "num_files": len(corpus),
    }
    
    # Gate evaluation
    gate_passed = True
    gate_results = {}
    
    if gate_mode:
        gate_results = {
            "precision": {"threshold": 0.85, "actual": precision, "passed": precision >= 0.85},
            "recall": {"threshold": 0.80, "actual": recall, "passed": recall >= 0.80},
            "fpr": {"threshold": 0.05, "actual": fpr, "passed": fpr <= 0.05},
        }
        gate_passed = all(g["passed"] for g in gate_results.values())
    
    return {
        "overall": overall,
        "gate_results": gate_results,
        "gate_passed": gate_passed,
        "per_file": all_results,
    }


def run_naive_baseline(corpus_dir: Path) -> dict:
    """Run naive baseline: same merchant ≥3 times."""
    manifest_path = corpus_dir / "manifest.json"
    if not manifest_path.exists():
        manifest_path = corpus_dir.parent / "manifest.json"
    
    corpus = load_corpus(manifest_path)
    
    total_tp = total_fp = total_fn = total_tn = 0
    
    for fname, data in corpus.items():
        txns = data["transactions"]
        ground_truth = set(data["metadata"].get("recurring_merchants", []))
        
        # Naive: any merchant with ≥3 expense transactions
        expenses = [t for t in txns if t["amount"] < 0]
        by_merchant = {}
        for t in expenses:
            m = t["merchant"]
            by_merchant[m] = by_merchant.get(m, 0) + 1
        
        detected_merchants = set(m for m, count in by_merchant.items() if count >= 3)
        
        tp = len(detected_merchants & ground_truth)
        fp = len(detected_merchants - ground_truth)
        fn = len(ground_truth - detected_merchants)
        
        all_merchants = set(t["merchant"] for t in expenses)
        non_recurring = all_merchants - ground_truth
        tn = len(non_recurring - detected_merchants)
        
        total_tp += tp
        total_fp += fp
        total_fn += fn
        total_tn += tn
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    fpr = total_fp / (total_fp + total_tn) if (total_fp + total_tn) > 0 else 0.0
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "fpr": round(fpr, 4),
        "tp": total_tp,
        "fp": total_fp,
        "fn": total_fn,
        "tn": total_tn,
    }


def main():
    parser = argparse.ArgumentParser(description="Recurring expense detection experiment")
    parser.add_argument("--corpus", type=Path, default=Path("corpus/synthetic"), help="Corpus directory")
    parser.add_argument("--gate", action="store_true", help="Run gate evaluation")
    parser.add_argument("--baseline", action="store_true", help="Run baseline comparison")
    parser.add_argument("--output", type=Path, help="Output JSON file")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    
    print(f"Loading corpus from {args.corpus}...")
    results = run_detection(args.corpus, gate_mode=args.gate)
    
    print(f"\n=== Overall Results ===")
    print(f"Files: {results['overall']['num_files']}")
    print(f"Precision: {results['overall']['precision']:.4f}")
    print(f"Recall: {results['overall']['recall']:.4f}")
    print(f"F1: {results['overall']['f1']:.4f}")
    print(f"FPR: {results['overall']['fpr']:.4f}")
    print(f"TP: {results['overall']['tp']}, FP: {results['overall']['fp']}, FN: {results['overall']['fn']}, TN: {results['overall']['tn']}")
    
    if args.gate:
        print(f"\n=== Gate Evaluation ===")
        for name, g in results["gate_results"].items():
            status = "✅ PASS" if g["passed"] else "❌ FAIL"
            print(f"  {name}: {g['actual']:.4f} (threshold: {g['threshold']}) {status}")
        print(f"\nOverall gate: {'✅ PASSED' if results['gate_passed'] else '❌ FAILED'}")
    
    if args.baseline:
        print(f"\n=== Naive Baseline Comparison ===")
        baseline = run_naive_baseline(args.corpus)
        print(f"Baseline Precision: {baseline['precision']:.4f}")
        print(f"Baseline Recall: {baseline['recall']:.4f}")
        print(f"Baseline F1: {baseline['f1']:.4f}")
        print(f"Baseline FPR: {baseline['fpr']:.4f}")
        
        our_f1 = results['overall']['f1']
        baseline_f1 = baseline['f1']
        improvement = our_f1 - baseline_f1
        print(f"\nOur F1: {our_f1:.4f}")
        print(f"Baseline F1: {baseline_f1:.4f}")
        print(f"Improvement: {improvement:+.4f}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")
    
    if args.gate and not results['gate_passed']:
        sys.exit(1)


if __name__ == "__main__":
    main()
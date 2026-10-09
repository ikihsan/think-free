#!/usr/bin/env python3
"""
E080 Food Recall Purchase Matching - Falsification Experiment Runner
Runs the matching experiment and evaluates predeclared kill gates.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from fixtures import generate_fixtures, write_fixtures
from matcher import run_matching, evaluate_results, MatchResult

KILL_GATES = {
    "G1_precision": 0.80,      # ≥80% precision
    "G2_recall": 0.60,         # ≥60% recall
    "G3_format_coverage": 2,   # ≥2 of 3 formats pass G1+G2
    "G4_negative_control": 0.0, # 0% false positives on clean negatives (specificity = 1.0)
}

def load_fixtures(fixture_dir: Path) -> Dict[str, Any]:
    """Load generated fixtures."""
    recalls = json.loads((fixture_dir / "recalls.json").read_text())
    purchases = {}
    for fmt in ["receipt", "loyalty_csv", "manual_entry"]:
        purchases[fmt] = json.loads((fixture_dir / f"purchases_{fmt}.json").read_text())
    ground_truth = json.loads((fixture_dir / "ground_truth.json").read_text())
    return {
        "recalls": recalls,
        "purchases": purchases,
        "ground_truth": ground_truth,
    }

def run_experiment(fixture_dir: Path = None) -> Dict[str, Any]:
    """Run the full experiment and return results."""
    
    if fixture_dir and fixture_dir.exists():
        fixtures = load_fixtures(fixture_dir)
    else:
        fixtures = generate_fixtures()
    
    recalls = fixtures["recalls"]
    all_results = {}
    all_metrics = {}
    
    for fmt in ["receipt", "loyalty_csv", "manual_entry"]:
        purchases = fixtures["purchases"][fmt]
        results = run_matching(purchases, recalls)
        gt = {p["purchase_id"]: p["ground_truth_recall"] for p in purchases}
        metrics = evaluate_results(results, gt)
        
        all_results[fmt] = [
            {
                "purchase_id": r.purchase_id,
                "predicted_recall": r.recall_id,
                "match_type": r.match_type,
                "confidence": r.confidence,
                "true_recall": gt[r.purchase_id],
                "correct": (r.recall_id == gt[r.purchase_id]) if (r.recall_id or gt[r.purchase_id]) else True,
            }
            for r in results
        ]
        all_metrics[fmt] = metrics
    
    # Evaluate kill gates
    gate_results = {}
    
    # G1: Precision ≥ 80% on each format
    gate_results["G1_precision"] = {
        fmt: metrics["precision"] >= KILL_GATES["G1_precision"]
        for fmt, metrics in all_metrics.items()
    }
    
    # G2: Recall ≥ 60% on each format
    gate_results["G2_recall"] = {
        fmt: metrics["recall"] >= KILL_GATES["G2_recall"]
        for fmt, metrics in all_metrics.items()
    }
    
    # G3: At least 2 formats pass both G1 and G2
    formats_passing_both = sum(
        1 for fmt in ["receipt", "loyalty_csv", "manual_entry"]
        if gate_results["G1_precision"][fmt] and gate_results["G2_recall"][fmt]
    )
    gate_results["G3_format_coverage"] = formats_passing_both >= KILL_GATES["G3_format_coverage"]
    
    # G4: Specificity = 1.0 (0% false positives on clean negatives) on each format
    gate_results["G4_negative_control"] = {
        fmt: metrics["specificity"] >= 1.0 - 1e-9  # Allow floating point
        for fmt, metrics in all_metrics.items()
    }
    
    # Overall verdict
    all_gates_pass = (
        all(gate_results["G1_precision"].values()) and
        all(gate_results["G2_recall"].values()) and
        gate_results["G3_format_coverage"] and
        all(gate_results["G4_negative_control"].values())
    )
    
    return {
        "metrics": all_metrics,
        "gate_results": gate_results,
        "kill_gates": KILL_GATES,
        "verdict": "PASS" if all_gates_pass else "FAIL",
        "formats_passing_both": formats_passing_both,
    }

def print_results(results: Dict[str, Any]):
    """Print formatted results."""
    print("=" * 60)
    print("E080 FOOD RECALL MATCHING - FALSIFICATION EXPERIMENT")
    print("=" * 60)
    
    print("\nPER-FORMAT METRICS:")
    print("-" * 60)
    for fmt in ["receipt", "loyalty_csv", "manual_entry"]:
        m = results["metrics"][fmt]
        print(f"\n  {fmt}:")
        print(f"    TP={m['true_positives']:2d}  FP={m['false_positives']:2d}  FN={m['false_negatives']:2d}  TN={m['true_negatives']:2d}")
        print(f"    Precision: {m['precision']:.3f}  (gate: ≥{KILL_GATES['G1_precision']:.0%})")
        print(f"    Recall:    {m['recall']:.3f}  (gate: ≥{KILL_GATES['G2_recall']:.0%})")
        print(f"    Specificity: {m['specificity']:.3f}  (gate: 1.000)")
        print(f"    F1:        {m['f1']:.3f}")
    
    print("\nKILL GATE RESULTS:")
    print("-" * 60)
    for gate, result in results["gate_results"].items():
        if isinstance(result, dict):
            for fmt, passed in result.items():
                status = "PASS" if passed else "FAIL"
                print(f"  {gate} [{fmt}]: {status}")
        else:
            status = "PASS" if result else "FAIL"
            print(f"  {gate}: {status}")
    
    print("\n" + "=" * 60)
    print(f"OVERALL VERDICT: {results['verdict']}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="E080 Food Recall Matching Falsification Experiment")
    parser.add_argument("--gate", action="store_true", help="Run with gate evaluation (default)")
    parser.add_argument("--fixtures", type=str, help="Path to fixture directory")
    parser.add_argument("--generate-fixtures", type=str, help="Generate fixtures to directory")
    parser.add_argument("--output", type=str, help="Output results JSON path")
    args = parser.parse_args()
    
    if args.generate_fixtures:
        write_fixtures(args.generate_fixtures)
        return 0
    
    fixture_dir = Path(args.fixtures) if args.fixtures else None
    results = run_experiment(fixture_dir)
    
    print_results(results)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to {args.output}")
    
    # Exit code: 0 for PASS, 1 for FAIL
    return 0 if results["verdict"] == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
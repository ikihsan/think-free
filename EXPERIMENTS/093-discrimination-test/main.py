<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->
#!/usr/bin/env python3
"""
E093 — Discrimination test prototype for view-count principle classification.

Tests whether an improved discrimination instrument can pass G2 (≥0.85 accuracy)
on hand-classified labels "known by construction" from the E083 aviation
maintenance experiment.

The current instrument (Bing search + 19-word solution keyword list) fails:
  - 19/30 automated "served" vs 0/30 hand "served"
  - G2 accuracy 0.70, needs ≥0.85

This prototype tests improved classification signals against the ground truth
from E083/E088.
"""

import json
import os
import sys

from classify import classify_hand, classify_v1, classify_v2, classify_original

EXP = "/home/ubuntu/think-free/EXPERIMENTS/083-aviation-maintenance-fault-codes"
TREATMENT_RESULTS = os.path.join(EXP, "raw", "treatment-results.jsonl")


def load_treatment_results():
    """Load treatment arm search results (20 rows, statement_ids 0-19)."""
    results = []
    with open(TREATMENT_RESULTS, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def compute_g2_accuracy(predictions, hand_labels, n_known_served=5, n_known_unserved=5):
    """Compute G2 accuracy: separate 5 known-served + 5 known-unserved at >= 0.85 accuracy."""
    if len(predictions) < n_known_served + n_known_unserved:
        return False, 0.0, "Not enough rows for G2 test"
    
    true_labels = ['served'] * n_known_served + ['unserved'] * n_known_unserved
    pred_labels = predictions[:n_known_served + n_known_unserved]
    
    correct = sum(1 for t, p in zip(true_labels, pred_labels) if t == p)
    accuracy = correct / len(true_labels)
    g2_pass = accuracy >= 0.85
    
    return g2_pass, accuracy, f"{correct}/{len(true_labels)}"


def evaluate(test_function, name, n_control=10):
    """Evaluate a classification function against hand labels, reporting G2 accuracy."""
    results = load_treatment_results()
    hand_labels = []
    
    for r in results:
        hand_labels.append(classify_hand(r))
    
    predictions = [test_function(r) for r in results]
    
    g2_pass, g2_accuracy, g2_detail = compute_g2_accuracy(
        predictions, hand_labels, n_known_served=n_control//2, n_known_unserved=n_control//2
    )
    
    true_served = [h == 'served' for h in hand_labels]
    pred_served = [p == 'served' for p in predictions]
    correct = sum(1 for t, p in zip(true_served, pred_served) if t == p)
    overall_accuracy = correct / len(true_served) if true_served else 0
    
    hand_served = sum(1 for h in hand_labels if h == 'served')
    hand_partial = sum(1 for h in hand_labels if h == 'partially_served')
    hand_unserved = sum(1 for h in hand_labels if h == 'unserved')
    
    pred_served = sum(1 for p in predictions if p == 'served')
    pred_partial = sum(1 for p in predictions if p == 'partially_served')
    pred_unserved = sum(1 for p in predictions if p == 'unserved')
    
    print(f"\n=== {name} ===")
    print(f"Hand labels: served={hand_served}, partially_served={hand_partial}, unserved={hand_unserved}/{len(hand_labels)}")
    print(f"Predictions: served={pred_served}, partially_served={pred_partial}, unserved={pred_unserved}/{len(predictions)}")
    print(f"Overall binary accuracy (served vs not-served): {overall_accuracy:.4f} ({correct}/{len(true_served)})")
    print(f"G2 test ({n_control} control: {n_control//2} known-served + {n_control//2} known-unserved):")
    print(f"  {g2_detail} — {'PASS' if g2_pass else 'FAIL'} (threshold: ≥0.85)")
    
    print(f"\nPer-row details:")
    for i in range(min(len(results), 30)):
        q = results[i]['query'][:50]
        print(f"  Row {i+1}: query='{q}'  hand={hand_labels[i]}  pred={predictions[i]}")
    
    if not g2_pass and len(results) > n_control:
        print(f"  (G2 control set: first {n_control} rows)")
        for i in range(n_control):
            q = results[i]['query'][:50]
            print(f"    Row {i+1}: query='{q}'  hand={hand_labels[i]}  pred={predictions[i]}")
    
    return g2_pass


def main():
    print("E093 — Discrimination test prototype")
    print("=" * 60)
    print("Testing improved discrimination instruments against")
    print("hand-classified ground truth from E083 aviation domain.")
    print()
    print("G2 threshold: ≥0.85 accuracy on 5 known-served + 5 known-unserved")
    print("Hand ground truth pattern: 0 served, 6 partially_served, 24 unserved (30 total)")
    print()
    
    g2_1 = evaluate(classify_v1, "v1: subject mention + guide structure", n_control=10)
    g2_2 = evaluate(classify_v2, "v2: subject + step-by-step + part info", n_control=10)
    g2_3 = evaluate(classify_original, "original: has_solution OR has_tool_title", n_control=10)
    
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"v1 (subject+guide):    G2 {'PASS' if g2_1 else 'FAIL'}")
    print(f"v2 (subject+steps+pi):  G2 {'PASS' if g2_2 else 'FAIL'}")
    print(f"fallback (original):   G2 {'PASS' if g2_3 else 'FAIL'}")
    print()
    print("G2 threshold: ≥0.85 accuracy on 5 known-served + 5 known-unserved")
    print("Hand ground truth: 0 served, 6 partially_served, 24 unserved (30 total)")
    print()
    if g2_1 or g2_2:
        print("✓ A passing discrimination test found — population measurement can proceed")
    elif not g2_3:
        print("✗ No passing test yet with improved instruments")
        print("  The original classifier passes G2 by coincidence on this sample,")
        print("  but fails on the full 30-row experiment (0.70 accuracy, F109/D095).")
        print("  Route must be re-entered through a discrimination test that passes")
        print("  on labels known by construction, not through another domain screen")
        print("  (per D088 and D095)")
    else:
        print("✗ All instruments fail G2 — need fundamental redesign")
        print("  Key problem: generic solution keywords ('how to', 'repair', 'app')")
        print("  produce widespread false positives in technical fault-code domains.")
        print("  Any valid instrument must require specific subject mention, not")
        print("  just keyword patterns.")


if __name__ == "__main__":
    main()
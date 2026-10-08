#!/usr/bin/env python3
"""E066 runner: E065's detector, unmodified, on real Berka transactions.

Gates predeclared in PROTOCOL.md:
  G1 micro-recall >= 0.50 over positive groups
  G2 micro-precision >= 0.60 (SLUZBY groups scored neither way)
  G3 detector micro-F1 - naive micro-F1 >= 0.05 (naive: group has >= 3 debits)
  G4 permutation control: detected groups on date-shuffled data <= 10% of real
"""

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "065-recurring-expense-detection"))
sys.path.insert(0, str(HERE))

import detect as det  # noqa: E402  E065's detector, unmodified
import berka  # noqa: E402

GATES = {"G1_recall": 0.50, "G2_precision": 0.60, "G3_f1_margin": 0.05,
         "G4_permuted_ratio": 0.10}


def evaluate(detected_merchants, positive, excluded, negative, count_excluded_positive=False):
    """Micro counts for one account. Excluded merchants are removed from
    detected before scoring unless count_excluded_positive, in which case they
    are treated as additional positives (sensitivity row)."""
    det_set = set(detected_merchants)
    if count_excluded_positive:
        positive = positive | excluded
    else:
        det_set = det_set - excluded
    tp = len(det_set & positive)
    fp = len(det_set & negative)
    fn = len(positive - det_set)
    tn = len(negative - det_set)
    return tp, fp, fn, tn


def pool(rows):
    tp = sum(r[0] for r in rows)
    fp = sum(r[1] for r in rows)
    fn = sum(r[2] for r in rows)
    tn = sum(r[3] for r in rows)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(f1, 4), "fpr": round(fpr, 4)}


def permute_dates(txns, rng):
    """Shuffle dates across one account's transactions (marginals preserved)."""
    dates = [t["date"] for t in txns]
    rng.shuffle(dates)
    return [{"date": d, "amount": t["amount"], "merchant": t["merchant"]}
            for d, t in zip(dates, txns)]


def main():
    accounts = berka.load_accounts(HERE / "raw" / "trans.csv")
    r_sample, c_sample, positives_by_account = berka.sample_accounts(accounts)
    sample = r_sample + c_sample

    det_rows, naive_rows, sens_rows = [], [], []
    detected_total = 0
    fp_merchants = defaultdict(int)
    for aid in sample:
        txns = accounts[aid]
        positive, excluded, negative = berka.label_groups(txns)
        detected = det.detect_recurring_expenses(txns)
        det_merchants = {d["merchant"] for d in detected}
        detected_total += len(det_merchants)
        det_rows.append(evaluate(det_merchants, positive, excluded, negative))
        sens_rows.append(evaluate(det_merchants, positive, excluded, negative,
                                  count_excluded_positive=True))
        counts = defaultdict(int)
        for t in txns:
            if t["amount"] < 0:
                counts[t["merchant"]] += 1
        naive_merchants = {m for m, c in counts.items() if c >= 3}
        naive_rows.append(evaluate(naive_merchants, positive, excluded, negative))
        for m in det_merchants & negative:
            fp_merchants[m] += 1

    pooled = pool(det_rows)
    naive = pool(naive_rows)
    sensitivity = pool(sens_rows)

    # G4: permutation control, seed 42
    rng = random.Random(42)
    permuted_total = 0
    for aid in sample:
        permuted_total += len(det.detect_recurring_expenses(permute_dates(accounts[aid], rng)))
    permuted_ratio = permuted_total / detected_total if detected_total else 0.0

    gates = {
        "G1_recall": {"threshold": GATES["G1_recall"], "actual": pooled["recall"],
                      "pass": pooled["recall"] >= GATES["G1_recall"]},
        "G2_precision": {"threshold": GATES["G2_precision"], "actual": pooled["precision"],
                         "pass": pooled["precision"] >= GATES["G2_precision"]},
        "G3_f1_margin": {"threshold": GATES["G3_f1_margin"],
                         "actual": round(pooled["f1"] - naive["f1"], 4),
                         "pass": pooled["f1"] - naive["f1"] >= GATES["G3_f1_margin"]},
        "G4_permuted_ratio": {"threshold": GATES["G4_permuted_ratio"],
                              "actual": round(permuted_ratio, 4),
                              "pass": permuted_ratio <= GATES["G4_permuted_ratio"]},
    }

    results = {
        "experiment": "066-berka-real-validation",
        "sample": {"positive_bearing_accounts": len(r_sample),
                   "control_accounts": len(c_sample),
                   "all_positive_bearing": len(positives_by_account),
                   "total_accounts": len(accounts)},
        "detector": pooled,
        "naive_baseline": naive,
        "sensitivity_sluzby_positive": sensitivity,
        "detected_groups_total": detected_total,
        "permuted_detected_groups": permuted_total,
        "top_false_positive_merchants": dict(sorted(
            fp_merchants.items(), key=lambda kv: -kv[1])[:20]),
        "gates": gates,
        "all_gates_passed": all(g["pass"] for g in gates.values()),
    }
    out = HERE / "results.json"
    out.write_text(json.dumps(results, indent=2))
    print(json.dumps({"detector": pooled, "naive": naive,
                      "gates": {k: v["pass"] for k, v in gates.items()},
                      "all_gates_passed": results["all_gates_passed"]}, indent=2))


if __name__ == "__main__":
    main()

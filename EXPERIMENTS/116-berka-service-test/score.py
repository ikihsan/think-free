#!/usr/bin/env python3
"""E116 scorer: assistant vs detector vs naive baseline, one key.

Group-level, pooled (micro) across accounts -- E066's evaluation,
unchanged. Reads only the committed key and the committed
answers; nothing about the outcome is hard-coded here.

Matching semantics (declared in PROTOCOL.md):
- A positive group is found (TP) iff its counterparty identity
  (bank + account) appears in that account's answers.
- An answer is an FP iff its counterparty identity matches no
  positive group of that account.
- The detector and the naive baseline predict whole merchant
  keys; a predicted key is a TP iff it is a positive group key.

Standard library only. Python 3.8.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "066-berka-real-validation"))
sys.path.insert(0, os.path.join(HERE, "..", "065-recurring-expense-detection"))

import berka  # noqa: E402

GATES = {
    "G0_R_recall": 0.50,
    "G0_C_precision": 0.80,
    "K1_assistant_recall": 0.95,
    "K2_f1_margin_over_detector": 0.05,
}


def load_key(path):
    key = {}
    with open(path) as fh:
        for line in fh:
            if line.strip():
                rec = json.loads(line)
                # build_sample.py stores Berka's integer account_id, but
                # the extracts and answers use the "R%03d"/"C%03d" form.
                # Normalize so answers match key rows.
                aid = "%s%03d" % (rec["arm"], rec["account_id"])
                key[aid] = rec
    return key


def _berka_id(aid):
    """Map a "R001"/"C009" scorer id back to Berka's integer account id."""
    return int(aid[1:])


def load_answers(path):
    answers = {}
    with open(path) as fh:
        for line in fh:
            if line.strip():
                rec = json.loads(line)
                answers[rec["account_id"]] = rec["counterparties"]
    return answers


def _identity(merchant_key):
    """bank + account identity of a merchant key."""
    parts = merchant_key.split("|", 2)
    return (parts[1], parts[2]) if len(parts) == 3 else None


def score_assistant(key, answers):
    """Micro TP/FP/FN for the assistant's counterparty answers.

    The unit is the positive GROUP (E066's unit): a group is
    found when its counterparty identity is named, so two
    positive groups at one counterparty are both found by one
    answer. An answer is an FP when its identity matches no
    positive group of that account.
    """
    tp = fp = fn = 0
    per_arm = {}
    for aid, rec in key.items():
        positives = set(rec["positive_merchants"])
        pos_identities = set(_identity(m) for m in positives)
        named = set()
        for cp in answers.get(aid, []):
            bank, account = cp.split(" / ", 1)
            named.add((bank, account))
        # TP: positive groups whose identity was named.
        arm_tp = sum(1 for m in positives if _identity(m) in named)
        arm_fp = len(named - pos_identities)
        arm_fn = len(pos_identities - named)
        tp += arm_tp
        fp += arm_fp
        fn += arm_fn
        arm = rec["arm"]
        a = per_arm.setdefault(arm, {"tp": 0, "fp": 0, "fn": 0})
        a["tp"] += arm_tp
        a["fp"] += arm_fp
        a["fn"] += arm_fn
    return _metrics(tp, fp, fn), per_arm


def account_groups(aid):
    """The account's debit merchant groups: {merchant_key: count}."""
    raw = os.path.join(HERE, "..", "066-berka-real-validation", "raw", "trans.csv")
    if not hasattr(account_groups, "_cache"):
        account_groups._cache = berka.load_accounts(raw)
    groups = {}
    for t in account_groups._cache[aid]:
        if t["amount"] < 0:
            groups[t["merchant"]] = groups.get(t["merchant"], 0) + 1
    return groups


def _metrics(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def score_predictions(key, predicted):
    """Score a reader that predicts whole merchant keys.

    `predicted`: {account_id: [merchant_key, ...]} -- the detector's
    detections or the naive baseline's groups.
    """
    tp = fp = fn = 0
    per_arm = {}
    for aid, rec in key.items():
        positives = set(rec["positive_merchants"])
        preds = set(predicted.get(aid, []))
        arm_tp = len(preds & positives)
        arm_fp = len(preds - positives)
        arm_fn = len(positives - preds)
        tp += arm_tp
        fp += arm_fp
        fn += arm_fn
        arm = rec["arm"]
        a = per_arm.setdefault(arm, {"tp": 0, "fp": 0, "fn": 0})
        a["tp"] += arm_tp
        a["fp"] += arm_fp
        a["fn"] += arm_fn
    return _metrics(tp, fp, fn), per_arm


def detector_predictions(key):
    """E066's detector, imported unmodified, on the same accounts."""
    import detect

    accounts = account_groups  # lazy cache holder
    if not hasattr(detector_predictions, "_loaded"):
        raw = os.path.join(HERE, "..", "066-berka-real-validation", "raw", "trans.csv")
        detector_predictions._accounts = berka.load_accounts(raw)
        detector_predictions._loaded = True
    predicted = {}
    for aid in key:
        results = detect.detect_recurring_expenses(detector_predictions._accounts[_berka_id(aid)])
        predicted[aid] = [d["merchant"] for d in results]
    return predicted


def naive_predictions(key):
    """Any counterparty group with >= 3 debits."""
    if not hasattr(naive_predictions, "_accounts"):
        raw = os.path.join(HERE, "..", "066-berka-real-validation", "raw", "trans.csv")
        naive_predictions._accounts = berka.load_accounts(raw)
    predicted = {}
    for aid in key:
        groups = {}
        for t in naive_predictions._accounts[_berka_id(aid)]:
            if t["amount"] < 0:
                groups[t["merchant"]] = groups.get(t["merchant"], 0) + 1
        predicted[aid] = [m for m, n in groups.items() if n >= 3]
    return predicted


def run(key_path, answers_path):
    key = load_key(key_path)
    answers = load_answers(answers_path)
    assistant, assistant_arm = score_assistant(key, answers)
    detector, detector_arm = score_predictions(key, detector_predictions(key))
    naive, naive_arm = score_predictions(key, naive_predictions(key))

    r = assistant_arm.get("R", {"tp": 0, "fp": 0, "fn": 0})
    c = assistant_arm.get("C", {"tp": 0, "fp": 0, "fn": 0})
    r_recall = r["tp"] / (r["tp"] + r["fn"]) if (r["tp"] + r["fn"]) else 0.0
    c_precision = c["tp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else 1.0

    gates = {
        "G0_R_recall": (r_recall, GATES["G0_R_recall"], r_recall >= GATES["G0_R_recall"]),
        "G0_C_precision": (c_precision, GATES["G0_C_precision"], c_precision >= GATES["G0_C_precision"]),
        "K1_assistant_recall": (assistant["recall"], GATES["K1_assistant_recall"], assistant["recall"] >= GATES["K1_assistant_recall"]),
        "K2_f1_margin_over_detector": (
            assistant["f1"] - detector["f1"],
            GATES["K2_f1_margin_over_detector"],
            assistant["f1"] - detector["f1"] >= GATES["K2_f1_margin_over_detector"],
        ),
    }
    served = all(g[2] for g in gates.values())
    return {
        "n_accounts": len(key),
        "assistant": assistant,
        "detector": detector,
        "naive": naive,
        "assistant_arm": assistant_arm,
        "detector_arm": detector_arm,
        "naive_arm": naive_arm,
        "gates": {name: {"actual": round(g[0], 4), "threshold": g[1], "pass": g[2]} for name, g in gates.items()},
        "served": served,
    }


if __name__ == "__main__":
    key_path = os.path.join(HERE, "key.jsonl")
    answers_path = os.path.join(HERE, "answers.jsonl")
    result = run(key_path, answers_path)
    with open(os.path.join(HERE, "result.json"), "w") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps(result["gates"], indent=1))
    print("SERVED" if result["served"] else "NOT SERVED")
    print("assistant  P %.4f  R %.4f  F1 %.4f" % (result["assistant"]["precision"], result["assistant"]["recall"], result["assistant"]["f1"]))
    print("detector   P %.4f  R %.4f  F1 %.4f" % (result["detector"]["precision"], result["detector"]["recall"], result["detector"]["f1"]))
    print("naive      P %.4f  R %.4f  F1 %.4f" % (result["naive"]["precision"], result["naive"]["recall"], result["naive"]["f1"]))

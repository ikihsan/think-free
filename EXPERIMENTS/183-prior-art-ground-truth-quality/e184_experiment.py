#!/usr/bin/env python3
"""
E184: Do vote margin, corroboration count, and residualised prescriptive
divergence add predictive power beyond standard text + metadata features
for identifying the top-voted answer on Stack Overflow?

Design (answer-level prediction):
  - Fetch N questions with >=2 answers from Stack Exchange API
  - For each question, create one row per answer
  - Label: 1 if this answer is the top-voted answer, 0 otherwise
  - Baseline features: TF-IDF(question) dot TF-IDF(answer), answer score rank,
    answer length, code blocks, question score, answer count
  - Treatment: baseline + three question-level signals
      (vote margin, corroboration count, residualised prescriptive divergence)
  - Compare: 5-fold cross-validated AUC
  - Kill gate: if treatment_auc - baseline_auc < 0.02, signals don't add enough

Split at the 300-line cap (2026-10-18): this file is the driver; the
Stack Exchange and text code is in e184_lib.py and the model in
e184_model.py. The raw capture is written to raw/results.json beside this
script, not to the process working directory.
"""

import json
import os
import time

import numpy as np

from e184_lib import compute_tfidf, fetch_answers, fetch_questions
from e184_model import build_answer_features, compute_three_signals, cross_validate

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("E184: Testing three signals for answer quality prediction")
    print("=" * 60)

    # 1. Fetch questions
    print("\n[1] Fetching questions from Stack Exchange API...")
    questions = fetch_questions(n=200)
    print(f"    Fetched {len(questions)} questions")

    # 2. Fetch answers and build dataset
    print("\n[2] Fetching answers and building dataset...")
    baseline_data = []
    treatment_data = []
    labels = []

    for i, q in enumerate(questions):
        qid = q["question_id"]
        answers = fetch_answers(qid)
        if len(answers) < 2:
            continue

        answers.sort(key=lambda a: a.get("score", 0), reverse=True)

        # Compute TF-IDF for question and all answers
        q_text = q.get("title", "") + " " + q.get("body", "")
        a_texts = [a.get("body", "") for a in answers]
        all_texts = [q_text] + a_texts
        tfidf_vecs = compute_tfidf(all_texts)
        q_tfidf = tfidf_vecs[0]
        a_tfidfs = tfidf_vecs[1:]

        # Compute three signals
        signals = compute_three_signals(q, answers, q_tfidf, a_tfidfs)

        # Build features for each answer
        for rank, (ans, a_tfidf) in enumerate(zip(answers, a_tfidfs)):
            is_top = (rank == 0)
            feats = build_answer_features(q, ans, is_top, rank, len(answers), q_tfidf, a_tfidf)
            baseline_data.append(feats)
            treatment_data.append(feats + [
                signals["vote_margin"],
                signals["corroboration_count"],
                signals["residual_div"],
            ])
            labels.append(1 if is_top else 0)

        if (i + 1) % 20 == 0:
            print(f"    Processed {i + 1}/{len(questions)} questions")

        time.sleep(0.3)

    X_baseline = np.array(baseline_data)
    X_treatment = np.array(treatment_data)
    y = np.array(labels)

    print(f"\n    Dataset: {len(y)} answer rows from {len(questions)} questions")
    print(f"    Baseline features: {X_baseline.shape[1]}")
    print(f"    Treatment features: {X_treatment.shape[1]}")
    print(f"    Positive class (top answer): {sum(y)}/{len(y)} = {sum(y)/len(y):.4f}")

    # 3. Cross-validation
    print("\n[3] Running 5-fold cross-validation...")
    baseline_aucs = cross_validate(X_baseline, y, n_folds=5)
    treatment_aucs = cross_validate(X_treatment, y, n_folds=5)

    baseline_mean = np.mean(baseline_aucs)
    treatment_mean = np.mean(treatment_aucs)
    delta = treatment_mean - baseline_mean

    print(f"\n    Baseline AUC: {baseline_mean:.4f} {chr(0x00B1)} {np.std(baseline_aucs):.4f}")
    print(f"    Treatment AUC: {treatment_mean:.4f} {chr(0x00B1)} {np.std(treatment_aucs):.4f}")
    print(f"    Delta: {delta:.4f}")

    # 4. Kill gate
    print("\n[4] Kill gate: delta >= 0.02?")
    if delta >= 0.02:
        print(f"    PASSED: signals add {delta:.4f} AUC")
        verdict = "PASS"
    else:
        print(f"    FAILED: signals add only {delta:.4f} AUC")
        verdict = "FAIL"

    # 5. Save results beside this script, not in the caller's cwd
    results = {
        "experiment": "E184",
        "question": "Do vote margin, corroboration count, and residualised prescriptive divergence add predictive power beyond standard text + metadata features for identifying the top-voted answer?",
        "n_answer_rows": len(y),
        "n_questions": len(questions),
        "n_baseline_features": int(X_baseline.shape[1]),
        "n_treatment_features": int(X_treatment.shape[1]),
        "positive_class_rate": float(sum(y) / len(y)),
        "baseline_auc": float(baseline_mean),
        "baseline_auc_std": float(np.std(baseline_aucs)),
        "treatment_auc": float(treatment_mean),
        "treatment_auc_std": float(np.std(treatment_aucs)),
        "delta": float(delta),
        "kill_gate": "delta >= 0.02",
        "verdict": verdict,
    }

    out_path = os.path.join(OUT_DIR, "raw", "e184-results.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n    Results saved to {out_path}")
    print(f"    Verdict: {verdict}")


if __name__ == "__main__":
    main()

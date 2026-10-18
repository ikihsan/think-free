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
  - Compare: 5-fold cross-validated AUC (question-grouped would be better
    but simple random CV is a first screen)
  - Kill gate: if treatment_auc - baseline_auc < 0.02, signals don't add enough
"""

import json
import math
import re
import time
import urllib.request
import urllib.parse
import gzip
import io
from collections import Counter

import numpy as np

# ---------- Stack Exchange API ----------

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "stackoverflow"


def api_get(path, params=None, max_retries=3):
    """Make a GET request to the Stack Exchange API with retry."""
    if params is None:
        params = {}
    params["site"] = SITE
    params["filter"] = "withbody"
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
            resp = urllib.request.urlopen(req, timeout=15)
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
            return json.loads(data)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                raise


def fetch_questions(n=200, pagesize=100):
    """Fetch n high-vote questions with answers."""
    questions = []
    page = 1
    while len(questions) < n:
        params = {
            "pagesize": min(pagesize, n - len(questions)),
            "page": page,
            "order": "desc",
            "sort": "votes",
            "filter": "withbody",
        }
        data = api_get("questions", params)
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            if item.get("answer_count", 0) >= 2:
                questions.append(item)
        page += 1
        if not data.get("has_more"):
            break
        time.sleep(0.5)
    return questions[:n]


def fetch_answers(question_id):
    """Fetch all answers for a question."""
    params = {
        "pagesize": 100,
        "order": "desc",
        "sort": "votes",
        "filter": "withbody",
    }
    data = api_get(f"questions/{question_id}/answers", params)
    return data.get("items", [])


# ---------- Text processing ----------

def tokenize(text):
    """Simple tokenizer: lowercase, extract word tokens."""
    if not text:
        return []
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"```.*?```", " CODE ", text, flags=re.DOTALL)
    return re.findall(r"[a-z]+", text.lower())


def compute_tfidf(documents):
    """Compute TF-IDF vectors for a list of documents."""
    tokenized = [tokenize(doc) for doc in documents]
    df = Counter()
    for tokens in tokenized:
        for token in set(tokens):
            df[token] += 1
    n_docs = len(documents)
    vectors = []
    for tokens in tokenized:
        tf = Counter(tokens)
        vec = {}
        for token, count in tf.items():
            if df[token] > 1:
                tf_val = 1 + math.log(count)
                idf_val = math.log(n_docs / df[token])
                vec[token] = tf_val * idf_val
        norm = math.sqrt(sum(v ** 2 for v in vec.values()))
        if norm > 0:
            vec = {k: v / norm for k, v in vec.items()}
        vectors.append(vec)
    return vectors


def cosine_similarity(vec1, vec2):
    """Cosine similarity between two sparse vectors."""
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    return sum(vec1[k] * vec2[k] for k in common)


# ---------- Feature engineering ----------

def compute_three_signals(question, answers, q_tfidf, a_tfidfs):
    """
    Compute the three signals at the question level.

    1. Vote margin: (top - second) / (top + second + 1), normalised
    2. Corroboration count: number of answers sharing > 30% Jaccard with top answer
    3. Residualised prescriptive divergence: mean(1 - cos(a, residual(a)))
       where residual(a) = a - proj_q(a)
    """
    if len(answers) < 2:
        return {"vote_margin": 0.0, "corroboration_count": 0.0, "residual_div": 0.0}

    sorted_answers = sorted(answers, key=lambda a: a.get("score", 0), reverse=True)
    top = sorted_answers[0]
    second = sorted_answers[1]

    # 1. Vote margin
    top_votes = top.get("score", 0)
    second_votes = second.get("score", 0)
    vote_margin = (top_votes - second_votes) / (top_votes + second_votes + 1)

    # 2. Corroboration count
    top_tokens = set(tokenize(top.get("body", "")))
    corroboration = 0
    for ans in sorted_answers[1:]:
        ans_tokens = set(tokenize(ans.get("body", "")))
        if top_tokens and ans_tokens:
            jaccard = len(top_tokens & ans_tokens) / len(top_tokens | ans_tokens)
            if jaccard > 0.3:
                corroboration += 1

    # 3. Residualised prescriptive divergence
    divergences = []
    for a_vec in a_tfidfs:
        common = set(a_vec.keys()) & set(q_tfidf.keys())
        dot = sum(a_vec[k] * q_tfidf[k] for k in common)
        residual = {}
        for k, v in a_vec.items():
            residual[k] = v - dot * q_tfidf.get(k, 0.0)
        norm = math.sqrt(sum(v ** 2 for v in residual.values()))
        if norm > 0:
            residual = {k: v / norm for k, v in residual.items()}
        sim = cosine_similarity(a_vec, residual)
        divergences.append(1.0 - sim)

    residual_div = float(np.mean(divergences)) if divergences else 0.0

    return {
        "vote_margin": vote_margin,
        "corroboration_count": float(corroboration),
        "residual_div": residual_div,
    }


def build_answer_features(question, answer, is_top, answer_rank, total_answers, q_tfidf, a_tfidf):
    """Build feature vector for a question-answer pair."""
    q_text = question.get("title", "") + " " + question.get("body", "")
    a_text = answer.get("body", "")
    q_tokens = tokenize(q_text)
    a_tokens = tokenize(a_text)

    # Text similarity features
    f_qa_cosine = cosine_similarity(q_tfidf, a_tfidf)
    f_q_len = len(q_tokens)
    f_a_len = len(a_tokens)
    f_q_code = q_text.count("```") + q_text.count("<code>")
    f_a_code = a_text.count("```") + a_text.count("<code>")
    f_q_marks = q_text.count("?")

    # Metadata features
    f_answer_score = answer.get("score", 0)
    f_answer_rank = answer_rank
    f_is_top = 1.0 if is_top else 0.0  # NOT used as feature, only as label
    f_question_score = question.get("score", 0)
    f_answer_count = question.get("answer_count", 0)

    features = [
        f_qa_cosine,
        f_q_len,
        f_a_len,
        f_q_code,
        f_a_code,
        f_q_marks,
        f_answer_score,
        f_answer_rank,
        f_question_score,
        f_answer_count,
    ]
    return features


# ---------- Logistic regression ----------

class SimpleLogisticRegression:
    """Simple logistic regression with L2 regularization, using numpy."""

    def __init__(self, lr=0.1, n_iters=1000, l2=0.01):
        self.lr = lr
        self.n_iters = n_iters
        self.l2 = l2
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        for _ in range(self.n_iters):
            z = X @ self.weights + self.bias
            y_pred = 1 / (1 + np.exp(-z))
            dw = (X.T @ (y_pred - y)) / n_samples + self.l2 * self.weights
            db = np.mean(y_pred - y)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        z = X @ self.weights + self.bias
        return 1 / (1 + np.exp(-z))


# ---------- Evaluation ----------

def compute_auc(y_true, y_scores):
    """Compute AUC using the Mann-Whitney U statistic."""
    pos = [s for s, y in zip(y_scores, y_true) if y == 1]
    neg = [s for s, y in zip(y_scores, y_true) if y == 0]
    if not pos or not neg:
        return 0.5
    n_pos = len(pos)
    n_neg = len(neg)
    u = 0
    for p in pos:
        for n in neg:
            if p > n:
                u += 1
            elif p == n:
                u += 0.5
    return u / (n_pos * n_neg)


def cross_validate(X, y, n_folds=5):
    """K-fold cross-validation."""
    n = len(X)
    fold_size = n // n_folds
    aucs = []
    indices = list(range(n))
    for fold in range(n_folds):
        test_start = fold * fold_size
        test_end = test_start + fold_size if fold < n_folds - 1 else n
        test_idx = indices[test_start:test_end]
        train_idx = indices[:test_start] + indices[test_end:]
        X_train = X[train_idx]
        y_train = y[train_idx]
        X_test = X[test_idx]
        y_test = y[test_idx]
        mean = X_train.mean(axis=0)
        std = X_train.std(axis=0) + 1e-8
        X_train = (X_train - mean) / std
        X_test = (X_test - mean) / std
        model = SimpleLogisticRegression(lr=0.1, n_iters=500, l2=0.01)
        model.fit(X_train, y_train)
        y_scores = model.predict_proba(X_test)
        auc = compute_auc(y_test, y_scores)
        aucs.append(auc)
    return aucs


# ---------- Main ----------

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
        top_answer = answers[0]

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

    # 5. Save results
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

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n    Results saved to results.json")
    print(f"    Verdict: {verdict}")


if __name__ == "__main__":
    main()

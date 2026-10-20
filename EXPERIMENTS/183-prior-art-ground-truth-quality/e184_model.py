"""E184 support — feature engineering, logistic regression, evaluation.

Split from e184_experiment.py at the 300-line cap (2026-10-18). Imports
`tokenize` and `cosine_similarity` from e184_lib. No behaviour changed.
"""

import math

import numpy as np

from e184_lib import cosine_similarity, tokenize


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

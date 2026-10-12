#!/usr/bin/env python3
"""Regression tests for the E116 scorer.

The scorer's job is to be a ruler: it must compute the
declared metrics from (key, answers) and nothing else.
These tests feed it synthetic keys and answers whose
outcome is known by construction, including the case
where the assistant is wrong, so a scorer that cannot
fail cannot ship.

Run: python3 test_score.py
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import score  # noqa: E402


def make_key():
    """Two accounts with known groups.

    R100: two positive groups (POJISTNE, SIPO), one
    negative group (NA), one excluded (SLUZBY).
    C200: no positive groups, one negative, one excluded.
    """
    return {
        "R100": {
            "account_id": "R100",
            "arm": "R",
            "positive_merchants": ["POJISTNE|AB|111", "SIPO|CD|222"],
            "excluded_merchants": ["SLUZBY|EF|333"],
            "negative_group_count": 1,
        },
        "C200": {
            "account_id": "C200",
            "arm": "C",
            "positive_merchants": [],
            "excluded_merchants": ["SLUZBY|EF|333"],
            "negative_group_count": 1,
        },
    }


class TestAssistantScoring(unittest.TestCase):
    def test_perfect_answer_scores_one(self):
        answers = {
            "R100": ["AB / 111", "CD / 222"],
            "C200": [],
        }
        m, arms = score.score_assistant(make_key(), answers)
        self.assertEqual((m["tp"], m["fp"], m["fn"]), (2, 0, 0))
        self.assertEqual(m["precision"], 1.0)
        self.assertEqual(m["recall"], 1.0)
        self.assertEqual(m["f1"], 1.0)

    def test_empty_answer_has_zero_recall(self):
        answers = {"R100": [], "C200": []}
        m, _ = score.score_assistant(make_key(), answers)
        self.assertEqual(m["tp"], 0)
        self.assertEqual(m["fn"], 2)
        self.assertEqual(m["recall"], 0.0)

    def test_hallucinated_counterparty_is_an_fp(self):
        answers = {
            "R100": ["AB / 111", "ZZ / 999"],
            "C200": ["QQ / 888"],
        }
        m, arms = score.score_assistant(make_key(), answers)
        self.assertEqual(m["tp"], 1)
        self.assertEqual(m["fp"], 2)
        self.assertEqual(m["fn"], 1)
        # The C arm's precision is what G0 reads: one answer,
        # no positive group, so 0.0.
        self.assertEqual(arms["C"]["fp"], 1)

    def test_identity_matching_is_on_bank_and_account(self):
        # The assistant copies the counterparty verbatim; the
        # key's merchant carries the k_symbol prefix. The two
        # must match on the bank + account tail only.
        answers = {"R100": ["AB / 111"], "C200": []}
        m, _ = score.score_assistant(make_key(), answers)
        self.assertEqual(m["tp"], 1)

    def test_same_identity_two_positive_groups_both_found(self):
        # Two standing-order groups at one counterparty (e.g.
        # insurance and household at the same bank account):
        # one correct answer names both.
        key = {
            "R100": {
                "account_id": "R100",
                "arm": "R",
                "positive_merchants": ["POJISTNE|AB|111", "SIPO|AB|111"],
                "excluded_merchants": [],
                "negative_group_count": 0,
            }
        }
        answers = {"R100": ["AB / 111"]}
        m, _ = score.score_assistant(key, answers)
        self.assertEqual((m["tp"], m["fn"]), (2, 0))


class TestPredictionScoring(unittest.TestCase):
    def test_detector_style_key_matching(self):
        predicted = {
            "R100": ["POJISTNE|AB|111", "NA|GH|444"],
            "C200": [],
        }
        m, _ = score.score_predictions(make_key(), predicted)
        self.assertEqual(m["tp"], 1)
        self.assertEqual(m["fp"], 1)
        self.assertEqual(m["fn"], 1)

    def test_naive_baseline_recall_is_complete(self):
        # The naive rule predicts every group with >= 3 debits;
        # every positive group qualifies by definition, so its
        # recall is 1.0 -- which is why it is the baseline.
        predicted = {
            "R100": ["POJISTNE|AB|111", "SIPO|CD|222", "NA|GH|444"],
            "C200": ["NA|GH|444"],
        }
        m, _ = score.score_predictions(make_key(), predicted)
        self.assertEqual(m["recall"], 1.0)
        self.assertGreater(m["fp"], 0)


class TestGateLogic(unittest.TestCase):
    def _gate_run(self, assistant_recall):
        # Build a key with 100 positive groups and an answer
        # set that recovers exactly `assistant_recall` of them.
        positives = ["POJISTNE|AB|%03d" % i for i in range(100)]
        key = {
            "R001": {
                "account_id": "R001",
                "arm": "R",
                "positive_merchants": positives,
                "excluded_merchants": [],
                "negative_group_count": 0,
            }
        }
        n_found = int(round(assistant_recall * 100))
        answers = {"R001": ["AB / %03d" % i for i in range(n_found)]}
        m, _ = score.score_assistant(key, answers)
        return m

    def test_recall_above_the_k1_threshold_passes(self):
        m = self._gate_run(0.96)
        self.assertGreaterEqual(m["recall"], score.GATES["K1_assistant_recall"])

    def test_recall_below_the_k1_threshold_fails(self):
        m = self._gate_run(0.90)
        self.assertLess(m["recall"], score.GATES["K1_assistant_recall"])

    def test_g0_c_precision_fires_on_hallucination(self):
        key = {
            "C001": {
                "account_id": "C001",
                "arm": "C",
                "positive_merchants": [],
                "excluded_merchants": [],
                "negative_group_count": 5,
            }
        }
        answers = {"C001": ["AB / 1", "CD / 2", "EF / 3", "GH / 4"]}
        m, arms = score.score_assistant(key, answers)
        c = arms["C"]
        precision = c["tp"] / (c["tp"] + c["fp"])
        self.assertEqual(precision, 0.0)
        self.assertLess(precision, score.GATES["G0_C_precision"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Regression tests for the E115 scorer.

Two properties matter and both are about the instrument rather than the
result:

1. The key in `score.py` must agree with the table in `M2-CASES.md`.  A
   scorer whose key can drift from the committed reference is a scorer that
   can be made to pass by editing one of them.
2. The scorer must FIRE.  Feeding it the plain-headcount reading must produce
   a lower score than feeding it the recorded answers, on the counting-rule
   subset in particular.  A scorer that returns 14/14 for every input
   measures nothing, and this record has been wrong that way repeatedly.

Run: python3 tests_here.py
"""

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import score  # noqa: E402


class TestKeyIntegrity(unittest.TestCase):
    def test_key_matches_committed_markdown(self):
        self.assertEqual(
            score.key_from_markdown(),
            score.KEY,
            "M2-CASES.md table and score.py KEY have diverged",
        )

    def test_key_has_the_declared_composition(self):
        # M2-CASES.md declares 14 cases, 6 YES and 8 NO, before any answer.
        self.assertEqual(len(score.KEY), 14)
        yes = sum(1 for v in score.KEY.values() if v == "YES")
        self.assertEqual(yes, 6, "declared composition was 6 YES / 8 NO")
        self.assertEqual(len(score.KEY) - yes, 8)

    def test_every_naive_wrong_case_is_keyed(self):
        for cid in score.NAIVE_WRONG:
            self.assertIn(cid, score.KEY)


class TestScorerFires(unittest.TestCase):
    """The null control must score materially below the recorded arms."""

    def _score_file(self, name):
        rows = []
        path = os.path.join(HERE, name)
        with open(path) as fh:
            for line in fh:
                if line.strip():
                    rows.append(json.loads(line))
        agree = 0
        div = div_agree = 0
        for rec in rows:
            cid = rec["case_id"]
            got = score.normalize(rec["assistant_answer"])
            ok = got == score.KEY[cid]
            agree += 1 if ok else 0
            if cid in score.NAIVE_WRONG:
                div += 1
                div_agree += 1 if ok else 0
        return agree, len(rows), div_agree, div

    def test_null_control_scores_zero_on_counting_rule_subset(self):
        agree, n, div_agree, div = self._score_file("answers-null-naive.jsonl")
        self.assertEqual(n, len(score.KEY))
        self.assertEqual(
            div_agree, 0, "the null arm got a counting-rule case right, so the key "
            "may be satisfiable by the naive reading"
        )
        self.assertEqual(div, 6)
        self.assertLess(agree, n, "null control scored a perfect 14/14")

    def test_both_treatment_arms_beat_the_control(self):
        control = self._score_file("answers-null-naive.jsonl")[0]
        for name in ("answers.jsonl", "answers-m2b.jsonl"):
            agree, n, _, _ = self._score_file(name)
            self.assertEqual(n, len(score.KEY), name)
            self.assertGreater(agree, control, "%s does not beat the control" % name)

    def test_normalize_reads_the_answers_actually_written(self):
        # The keys are not all YES/NO; a normalizer that only handled the
        # boolean cells would score P4 and P7b as unparseable and silently
        # drop them.
        self.assertEqual(score.normalize("48"), "48")
        self.assertEqual(score.normalize("SAME (one worksite, 180 employees)"), "SAME")
        self.assertEqual(score.normalize("**yes**"), "YES")
        self.assertIsNone(score.normalize("I am not sure"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
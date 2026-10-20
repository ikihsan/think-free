#!/usr/bin/env python3
"""test_squad.py — the checks the E141 numbers depend on.

Standard library only, no network. Exits 0 when every check holds and 1
otherwise. Three of these are the reason the numbers can be read at all:
the corpus identity, the recomputability of both declared exclusions from the
arm file alone (D124), and the instrument's ability to recover correct pairs
that are NOT copies of the arms that built it.

Run:  python3 test_squad.py
"""
import hashlib
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))
import valueset  # noqa: E402

EXPECTED_SHA256 = "80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8"
DIGIT = re.compile(r"\d")
VALUE_SPAN = re.compile(r"^[\s$€£]*\d|^(January|February|March|April|May|June|July|"
                         r"August|September|October|November|December)\b", re.I)


def rows():
    return [json.loads(line) for line in
            open(os.path.join(HERE, "arms.jsonl"), encoding="utf-8")]


class Corpus(unittest.TestCase):
    def test_identity(self):
        path = os.path.join(HERE, "raw", "dev-v2.0.json")
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for block in iter(lambda: fh.read(1 << 20), b""):
                h.update(block)
        self.assertEqual(h.hexdigest(), EXPECTED_SHA256)

    def test_arm_membership_matches_the_corpus_label(self):
        """A row is A exactly when the corpus did not mark it impossible."""
        raw = json.load(open(os.path.join(HERE, "raw", "dev-v2.0.json"),
                             encoding="utf-8"))
        truth = {}
        for art in raw["data"]:
            for para in art["paragraphs"]:
                for qa in para["qas"]:
                    truth[qa["id"]] = bool(qa.get("is_impossible"))
        for row in rows():
            self.assertEqual(row["arm"] == "B", truth[row["id"]], row["id"])

    def test_answer_present_exactly_on_the_answerable_arm(self):
        for row in rows():
            self.assertEqual(bool(row["answer"]), row["arm"] == "A", row["id"])

    def test_ids_unique_and_contexts_intact(self):
        seen = set()
        for row in rows():
            self.assertNotIn(row["id"], seen)
            seen.add(row["id"])
            digest = hashlib.sha256(row["context"].encode("utf-8")).hexdigest()
            self.assertEqual(digest, row["context_sha256"], row["id"])


class ExclusionsAreCheckableFromTheArmFile(unittest.TestCase):
    """D124: the exclusion behind K1's denominator must be recomputable here."""

    def test_has_digit_is_recomputable(self):
        for row in rows():
            self.assertEqual(row["has_digit"], bool(DIGIT.search(row["question"])),
                             row["id"])

    def test_answer_is_value_is_recomputable(self):
        for row in rows():
            self.assertEqual(row["answer_is_value"],
                             bool(VALUE_SPAN.match(row["answer"])), row["id"])


class InstrumentControls(unittest.TestCase):
    """`extra` non-empty must mean an absent value; empty must not always mean so.

    The positives are rewordings of the SAME value in the SAME document, not
    copies of the arms that built the canonicalizer. Several of them are the
    shapes a person actually writes and this corpus is full of. Whether the
    instrument recovers each one is a measurement, not an assertion, so a
    failure here is reported by name rather than worked around.
    """

    DOC = ("The plant opened in 1994 at a cost of $12,500,000, employed 340 people, "
           "and produced 1,250 units a day until March 3, 2011.")

    POSITIVE = [
        ("thousands separator dropped", "It opened in 1994 and cost 12500000 dollars."),
        ("currency word instead of the sign", "It cost 12.5 million dollars."),
        ("date order swapped", "The plant shut on 3 March 2011."),
        ("date with an ordinal suffix", "The plant shut on March 3rd, 2011."),
        ("comma grouping in a plain number", "It employed 1,250 people."),
        ("a bare year restated", "1994 is the year it opened."),
    ]
    NEGATIVE = [
        ("a year the document does not carry", "It opened in 1995."),
        ("a count the document does not carry", "It employed 341 people."),
        ("a money value off by a factor of ten", "It cost $1,250,000."),
    ]

    @unittest.expectedFailure
    def test_positive_rewordings_are_not_condemned(self):
        """AMENDMENT-2: two of the six fail, and the mechanism is the value's kind.

        `canonical()` keys a value by (kind, number), so `$12,500,000` and
        `12500000 dollars` are different keys for one number. E140's corpus
        wrote dollar amounts with a symbol, so its 0 false positives in 929
        values could not have found this. The expected-failure marker is
        load-bearing: a fix to `valueset.py` turns this into an unexpected
        success, which is the signal that the claim below is now falsified and
        the marker should come off.
        """
        bad = []
        for name, sub in self.POSITIVE:
            ref = valueset.canonical(self.DOC)
            got = valueset.canonical(sub)
            extra = [k for k in got if k not in ref]
            if extra:
                bad.append("%s: %s" % (name, extra))
        self.assertEqual(bad, [], "the instrument condemned a correct reworded value: "
                                  + "; ".join(bad))

    def test_absent_values_are_found(self):
        for name, sub in self.NEGATIVE:
            ref = valueset.canonical(self.DOC)
            got = valueset.canonical(sub)
            self.assertTrue([k for k in got if k not in ref],
                            "the instrument missed " + name)

    def test_a_multiset_difference_is_caught_in_the_scored_direction(self):
        ref = valueset.canonical(self.DOC)
        got = valueset.canonical("It employed 340 people and produced 1,000 units a day.")
        self.assertTrue([k for k in got if k not in ref])


class ScoreArithmetic(unittest.TestCase):
    def test_verdicts_partition_the_corpus(self):
        path = os.path.join(HERE, "verdicts.jsonl")
        if not os.path.exists(path):
            self.skipTest("score.py has not run")
        got = [json.loads(line) for line in open(path, encoding="utf-8")]
        self.assertEqual(len(got), len(rows()))
        n = sum(1 for _ in got)
        parts = sum(1 for r in got if r["verdict"] in ("condemn", "clear", "defer"))
        self.assertEqual(parts, n)
        gates = json.load(open(os.path.join(HERE, "gates.json"), encoding="utf-8"))
        tri = gates["triage"]
        self.assertEqual(tri["condemn"]["k"] + tri["clear"]["k"] + tri["defer"]["k"], n)

    def test_declared_thresholds_are_the_ones_evaluated(self):
        path = os.path.join(HERE, "gates.json")
        if not os.path.exists(path):
            self.skipTest("score.py has not run")
        gates = json.load(open(path, encoding="utf-8"))
        want = {
            "K1_detection_B_digit": 0.95,
            "K2_false_positive_A": 0.98,
            "K3_coverage_A": 0.30,
            "K5_coverage_A_value_answer": 0.30,
        }
        for key, floor in want.items():
            observed = gates[key]["rate"]
            expected = observed >= floor
            self.assertEqual(gates[key]["passed"], expected,
                             "%s: passed flag disagrees with its own rate" % key)
        cov = gates["K4_coverage_digit_arms"]
        self.assertEqual(len(cov["A_digit"]["ci95"]), 2)
        self.assertEqual(len(cov["B_digit"]["ci95"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""E028's gates, falsified against the bytes that would break them.

Every test here is asserted against the committed capture, not against a
fixture that agrees with the code. A test built from the same object as the
assertion proves nothing, which is the defect class F013 and defect 22 name.

The file was split at the 300-line cap into this and `test_capture_integrity.py`;
the split is by invariant, not by size alone. This file holds the *gates* — the
verdict, the controls, agreement, and the reader separation. The sibling holds
the *capture* — the fetched documentation, the refusals recorded beside it, and
the protocol's existence.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def read_jsonl(name):
    with open(os.path.join(RAW, name)) as fh:
        return [json.loads(l) for l in fh if l.strip()]


class TestWilsonAndKappa(unittest.TestCase):
    def test_wilson_on_the_recorded_floor(self):
        sys.path.insert(0, HERE)
        from fitstats import wilson
        self.assertEqual([round(x, 3) for x in wilson(0, 24)],
                         [0.0, 0.138])
        self.assertEqual([round(x, 3) for x in wilson(15, 39)],
                         [0.249, 0.541])
        self.assertEqual([round(x, 3) for x in wilson(14, 38)],
                         [0.234, 0.527])

    def test_wilson_refuses_an_unmeasured_population(self):
        sys.path.insert(0, HERE)
        from fitstats import wilson
        self.assertEqual(wilson(0, 0), [None, None])

    def test_kappa_of_identical_label_vectors_is_not_reported_as_a_pass(self):
        sys.path.insert(0, HERE)
        from fitstats import agreement_note, cohen_kappa
        cats = ("serves", "partial", "does_not_serve", "unreadable",
                "no_distinguishing_attribute")
        same = ["serves", "does_not_serve", "partial"]
        self.assertEqual(cohen_kappa(same, list(same), cats), 1.0)
        self.assertIsNotNone(agreement_note(1.0))
        self.assertIn("warning", agreement_note(1.0))

    def test_kappa_is_undefined_on_degenerate_marginals(self):
        sys.path.insert(0, HERE)
        from fitstats import cohen_kappa
        self.assertIsNone(cohen_kappa(["yes"] * 19, ["yes"] * 19,
                                      ("yes", "inferred", "none")))

    def test_kappa_reproduces_the_0_9226_e023_quotes_for_two_readers(self):
        """Checked against a figure written by a different session, on a
        different population, from committed labels rather than from a vector
        invented here. E023 reported κ = 0.9226 over 38 shared rows between
        its reader and E022's."""
        sys.path.insert(0, HERE)
        from fitstats import cohen_kappa
        here = os.path.dirname(HERE)
        e23 = os.path.join(here, "023-served-baseline", "raw", "labels.tsv")
        e22 = os.path.join(here, "022-need-outcomes", "raw", "labels.tsv")
        mine = {}
        with open(e23) as fh:
            header = fh.readline().rstrip("\n").split("\t")
            ix = header.index("comment_id")
            il = header.index("label")
            ia = header.index("arm")
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if len(p) > max(ix, il, ia) and p[ia] == "need":
                    mine[p[ix]] = p[il]
        theirs = {}
        with open(e22) as fh:
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 2:
                    theirs[p[0]] = p[1]
        shared = [i for i in mine if i in theirs]
        a = [mine[i] for i in shared]
        b = [theirs[i] for i in shared]
        self.assertGreaterEqual(len(shared), 30)
        cats = sorted(set(a) | set(b))
        self.assertEqual(round(cohen_kappa(a, b, cats), 4), 0.9226)


class TestLexicalIndexIsCalibratedNotBare(unittest.TestCase):
    def test_lexical_difference_is_reported_with_its_base_rate(self):
        with open(os.path.join(HERE, "results.json")) as fh:
            res = json.load(fh)
        lex = res["lexical_index"]
        for key in ("own_mean_coverage", "mismatched_mean_coverage",
                    "difference", "n_own", "n_mismatched", "informative"):
            self.assertIn(key, lex)
        self.assertEqual(lex["n_own"], lex["n_mismatched"])
        self.assertFalse(lex["informative"])

    def test_lexical_index_feeds_no_gate(self):
        with open(os.path.join(HERE, "results.json")) as fh:
            res = json.load(fh)
        blob = json.dumps(res["gates"])
        self.assertNotIn("coverage", blob)


class TestTheVerdictFollowsTheDeclaredGate(unittest.TestCase):
    """The gate table is read, not recomputed, so a moved threshold shows up."""

    def setUp(self):
        with open(os.path.join(HERE, "results.json")) as fh:
            self.res = json.load(fh)

    def test_verdict_is_not_evaluated_and_names_the_failing_control(self):
        self.assertEqual(self.res["verdict"], "not_evaluated")
        self.assertIn("A4", self.res["verdict_reason"])
        self.assertIn("C2", self.res["verdict_reason"])

    def test_the_reason_names_the_labels_that_failed_the_control(self):
        self.assertIn("partial", self.res["verdict_reason"])

    def test_the_failing_control_is_the_declared_positive_one(self):
        self.assertFalse(self.res["gates"]["a1_instrument"][
            "c2_positive_control_H03"])
        self.assertEqual(self.res["controls"]["c2_positive_H03"],
                         {"r1": "partial", "r2": "partial"})

    def test_the_mismatched_control_passed_at_zero(self):
        for reader in ("r1", "r2"):
            c1 = self.res["controls"]["c1_mismatched"][reader]
            self.assertEqual(c1["called_serving"], 0)
            self.assertEqual(c1["rate_called_serving"], 0.0)

    def test_a4_fired_for_the_control_not_for_a_missing_population(self):
        a4 = self.res["gates"]["a4_not_evaluated"]
        self.assertTrue(a4["fires"])
        self.assertFalse(a4["under_ten"])
        self.assertGreaterEqual(a4["fit_population"], 10)

    def test_neither_a3_nor_b1_fired(self):
        self.assertFalse(self.res["gates"][
            "a3_kill_does_not_serve_lower_bound_0_20"]["fires"])
        self.assertFalse(self.res["gates"]["b1_serves_lower_bound_0_60"][
            "fires"])

    def test_agreement_is_below_the_declared_floor(self):
        a2 = self.res["gates"]["a2_agreement"]
        self.assertLess(a2["kappa"], 0.6)
        self.assertFalse(a2["passes"])

    def test_the_excluded_rows_are_named_with_a_reason(self):
        pop = self.res["population"]
        self.assertEqual(
            pop["excluded_no_distinguishing_attribute"], ["H05", "H30"])
        self.assertEqual(pop["excluded_unreadable"], [])
        self.assertEqual(pop["fit_population"],
                         pop["fit_rows_naming_at_least_one_artifact"]
                         - len(pop["excluded_no_distinguishing_attribute"]))

    def test_the_unmeasured_arm_is_declared_not_implied(self):
        pop = self.res["population"]
        self.assertEqual(pop["declared_total"], 29)
        self.assertFalse(pop["arm2_executed"])
        self.assertEqual(pop["arm2_sealed_rows"], 10)


class TestTheRubricCannotBeSatisfiedBySilence(unittest.TestCase):
    """`does_not_serve` must be reachable; `unreadable` must not swallow it."""

    def test_every_row_in_the_fit_table_has_both_readers_and_evidence(self):
        with open(os.path.join(HERE, "results.json")) as fh:
            res = json.load(fh)
        for entry in res["fit_table"]:
            for reader in ("r1", "r2"):
                self.assertIn("label_" + reader, entry)
                self.assertIn("note_" + reader, entry)
            self.assertIsInstance(entry["agree"], bool)

    def test_every_reader_label_is_one_of_the_declared_categories(self):
        declared = {"serves", "partial", "does_not_serve", "unreadable",
                    "no_distinguishing_attribute"}
        seen = set()
        for reader in ("r1", "r2"):
            for batch in (1, 2):
                for rec in read_jsonl("step_b_%s_batch%d.jsonl"
                                      % (reader, batch)):
                    self.assertIn(rec["label"], declared)
                    self.assertTrue(rec["note"])
                    seen.add(rec["label"])
        self.assertTrue({"serves", "partial", "does_not_serve"} <= seen,
                        "the scheme never separated anything: %s" % seen)

    def test_evidence_quotes_come_from_the_file_they_name(self):
        docs = {}
        for rec in read_jsonl("fetch_log.jsonl"):
            if rec["has_text"] and os.path.isfile(rec["path"]):
                with open(rec["path"]) as fh:
                    docs[rec["path"]] = fh.read()
        checked = 0
        for reader in ("r1", "r2"):
            for batch in (1, 2):
                for rec in read_jsonl("step_b_%s_batch%d.jsonl"
                                      % (reader, batch)):
                    for quote in rec.get("evidence") or []:
                        if " :: " not in quote:
                            continue
                        path, text = quote.split(" :: ", 1)
                        if path not in docs:
                            continue
                        self.assertIn(text.strip()[:80], docs[path],
                                      "%s %s: quote not in the named file"
                                      % (reader, rec["row"]))
                        checked += 1
        self.assertGreater(checked, 0, "no evidence quote was verified")


class TestProtocolWasDeclaredBeforeTheData(unittest.TestCase):
    def test_both_amendments_and_the_rubric_exist(self):
        for name in ("PROTOCOL.md", "PROTOCOL-AMENDMENT-1.md",
                     "PROTOCOL-AMENDMENT-2.md", "RUBRIC.md"):
            self.assertTrue(os.path.exists(os.path.join(HERE, name)), name)

    def test_the_declared_population_matches_what_was_measured(self):
        with open(os.path.join(HERE, "PROTOCOL.md")) as fh:
            protocol = fh.read()
        self.assertIn("**29 prior-art deaths", protocol)
        with open(os.path.join(HERE, "results.json")) as fh:
            res = json.load(fh)
        self.assertEqual(res["population"]["declared_total"], 29)

    def test_the_base_rate_control_exists_even_though_it_finds_nothing(self):
        """F043's lesson: a rate read without a control means nothing. The
        control is here and it is reported, not omitted because it was 0.065."""
        with open(os.path.join(HERE, "results.json")) as fh:
            res = json.load(fh)
        self.assertIsNotNone(res["lexical_index"]["mismatched_mean_coverage"])


if __name__ == "__main__":
    unittest.main()
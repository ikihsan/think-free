#!/usr/bin/env python3
"""Falsification cases for 016's two gates.

`docs/policy/gate-falsification.md` asks for a gate to be falsified against the
defect's own bytes before it is trusted, in both directions. Both directions here
are fixed by the declared hypothesis rather than chosen after the fact: H1
predicts the young arm is *mostly documents*, so a gate that quietly lowers its
share threshold, or that treats a class with no decided rows as passing, is the
gate that matters. H2 has three declared answers and one of them is "inconclusive",
so the case that matters most is the one at the boundary — **three hits must not
be rounded up to four.**

The last class of test is the one 015's `INSTRUMENT_CORRECTION` teaches: a gate
computed on the hand review rather than on the mechanical classification it was
declared on would report a number no declared rule produced.

Run: python3 -m unittest discover -s tests -p 'test_artifact_tally.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "016-incumbent-artifact-type"))

import classification  # noqa: E402
import servingjoin     # noqa: E402
import tally           # noqa: E402


def row(repo, klass, arm="young", decided=True, served=False, stars=100):
    return {"repo": repo, "arm": arm, "group": arm, "need": "n", "stars": stars,
            "class": klass, "class_reason": None, "hits": [], "releases": None,
            "root_size": None, "measured_by_015": True,
            "served": (served if decided else None), "best_rate": 0,
            "best_cumulative": 0, "undecided": not decided}


def mech(class_):
    return {"class": class_, "install_line": class_ == "tutorial",
            "foreign_link": class_ == "tutorial", "shell_blocks": 3}


def read(arm="young", stars=100, repeated=True, class_="teaches_only"):
    return {"repo": "r%d" % stars, "arm": arm, "stars": stars,
            "repeated": repeated, "procedure": "do the thing", "class": class_,
            "judgement_note": "note"}


class H1Test(unittest.TestCase):
    def test_document_majority_with_a_gap_survives(self):
        rows = [row("d%d" % i, "document", served=True) for i in range(7)]
        rows += [row("x%d" % i, "executable", served=False) for i in range(3)]
        out = tally.h1(rows)
        self.assertEqual(out["verdict"], "survives")
        self.assertFalse(out["conditions"][0]["dead"])
        self.assertFalse(out["conditions"][1]["dead"])

    def test_document_majority_with_no_gap_is_dead(self):
        """Both classes unserved means documents do not serve *worse* than tools,
        which is the second half of H1. The declared gate is `dead = A or B`, so
        one firing condition is enough and the verdict is dead, not a split."""
        rows = [row("d%d" % i, "document", served=False) for i in range(7)]
        rows += [row("x%d" % i, "executable", served=False) for i in range(3)]
        out = tally.h1(rows)
        self.assertEqual(out["verdict"], "dead")
        self.assertTrue(out["conditions"][1]["dead"])

    def test_exactly_half_is_dead(self):
        """The gate is `<= 50%` dead, so a tie does not survive. Stated as a test
        because a tie is exactly where a gate gets quietly nudged."""
        rows = [row("d%d" % i, "document") for i in range(5)]
        rows += [row("x%d" % i, "executable") for i in range(5)]
        out = tally.h1(rows)
        self.assertTrue(out["conditions"][0]["dead"])
        self.assertEqual(out["verdict"], "dead")

    def test_unreadable_rows_leave_the_denominator(self):
        rows = [row("d%d" % i, "document") for i in range(2)]
        rows += [row("u%d" % i, "unreadable", decided=False) for i in range(8)]
        out = tally.h1(rows)
        self.assertEqual(out["readable"], 2)
        self.assertEqual(out["documents"], 2)

    def test_rate_parity_kills_a_document_majority(self):
        rows = [row("d%d" % i, "document", served=True, decided=True)
                for i in range(6)]
        rows += [row("x%d" % i, "executable", served=True, decided=True)
                 for i in range(3)]
        out = tally.h1(rows)
        names = [c["name"] for c in out["conditions"]]
        self.assertIn("rate_parity", names)
        parity = [c for c in out["conditions"] if c["name"] == "rate_parity"][0]
        self.assertTrue(parity["dead"], msg=parity)
        self.assertEqual(out["verdict"], "dead")

    def test_rate_parity_beyond_the_band_does_not_kill(self):
        rows = [row("d%d" % i, "document", served=True) for i in range(6)]
        rows += [row("x%d" % i, "executable", served=False) for i in range(3)]
        out = tally.h1(rows)
        parity = [c for c in out["conditions"] if c["name"] == "rate_parity"][0]
        self.assertFalse(parity["dead"], msg=parity)
        self.assertEqual(out["verdict"], "survives")

    def test_one_class_with_no_decided_row_is_reported_not_assumed(self):
        """A condition that cannot be computed is not counted as fired, and the
        gate is decided on the share alone. Asserting `False` rather than `None`
        is deliberate: `None` would be read downstream as "unknown and therefore
        blocking", which is not what the declaration says."""
        rows = [row("d%d" % i, "document", decided=False) for i in range(6)]
        rows += [row("x%d" % i, "executable", served=True) for i in range(3)]
        out = tally.h1(rows)
        parity = [c for c in out["conditions"] if c["name"] == "rate_parity"][0]
        self.assertFalse(parity["dead"])
        self.assertIsNone(parity["value"])
        self.assertIn("cannot be compared", parity["detail"])
        self.assertEqual(out["verdict"], "survives")

    def test_an_undecidable_parity_still_kills_an_exact_tie(self):
        rows = [row("d%d" % i, "document", decided=False) for i in range(5)]
        rows += [row("x%d" % i, "executable", decided=False) for i in range(5)]
        out = tally.h1(rows)
        self.assertEqual(out["verdict"], "dead")
        self.assertTrue(out["conditions"][0]["dead"])

    def test_no_readable_row_is_inconclusive_not_survives(self):
        out = tally.h1([row("u%d" % i, "unreadable", decided=False) for i in range(4)])
        self.assertEqual(out["verdict"], "inconclusive")

    def test_unreadable_repos_are_named(self):
        rows = [row("d0", "document")] + [row("u0", "unreadable", decided=False)]
        self.assertEqual(tally.h1(rows)["unreadable_repos"], ["u0"])


class H2Test(unittest.TestCase):
    def build(self, hits, misses=0, arm="young"):
        reads = {"rows": {}}
        mech_by_repo = {}
        for i in range(hits):
            name = "hit%d" % i
            reads["rows"][name] = read(arm=arm, stars=1000 + i)
            mech_by_repo[name] = mech("teaches_only")
        for i in range(misses):
            name = "miss%d" % i
            reads["rows"][name] = read(arm=arm, stars=100 + i, class_="tutorial")
            mech_by_repo[name] = mech("tutorial")
        return tally.h2(reads, mech_by_repo)

    def test_four_hits_survive(self):
        self.assertEqual(self.build(4, 6)["verdict"], "survives")

    def test_two_hits_are_dead(self):
        self.assertEqual(self.build(2, 8)["verdict"], "dead")

    def test_three_hits_are_inconclusive_and_do_not_round_up(self):
        out = self.build(3, 7)
        self.assertEqual(out["hits"], 3)
        self.assertEqual(out["verdict"], "inconclusive")
        self.assertNotEqual(out["verdict"], "survives")

    def test_a_row_is_a_hit_only_when_both_conditions_hold(self):
        reads = {"rows": {
            "repeated_but_tutorial": read(class_="tutorial"),
            "teaches_only_but_not_repeated": read(repeated=False, class_="teaches_only"),
            "both": read(class_="teaches_only"),
        }}
        mech_by_repo = {"repeated_but_tutorial": mech("tutorial"),
                        "teaches_only_but_not_repeated": mech("teaches_only"),
                        "both": mech("teaches_only")}
        out = tally.h2(reads, mech_by_repo)
        self.assertEqual(out["hits"], 1)
        self.assertEqual(out["hit_repos"], ["both"])

    def test_a_row_missing_from_the_readme_cannot_score(self):
        reads = {"rows": {"a": read(class_="teaches_only")}}
        out = tally.h2(reads, {})
        self.assertEqual(out["hits"], 0)

    def test_a_readme_that_no_one_fetched_is_not_a_verdict(self):
        """The first run of this gate returned `dead` for H2 with zero rows read,
        because 0 hits is `<= 2`. A gate must not answer about a population nobody
        looked at, and the fix is the gate's, not the report's."""
        out = tally.h2({"rows": {}}, {})
        self.assertEqual(out["verdict"], "not_evaluated")
        self.assertEqual(out["n"], 0)

    def test_a_population_quarter_of_the_declared_size_is_flagged(self):
        out = self.build(4)
        self.assertEqual(out["n"], 4)
        self.assertTrue(out["population_short"])
        self.assertEqual(out["population_declared_n"], 10)

    def test_a_full_population_is_not_flagged_short(self):
        self.assertFalse(self.build(4, 6)["population_short"])

    def test_control_reading_is_reported_separately_and_can_kill_the_generative_reading(self):
        reads = {"rows": {}}
        mech_by_repo = {}
        for i in range(4):
            name = "p%d" % i
            reads["rows"][name] = read(arm="placebo", stars=10 + i)
            mech_by_repo[name] = mech("teaches_only")
        for i in range(4):
            name = "q%d" % i
            reads["rows"][name] = read(arm="placebo", stars=20 + i, class_="tutorial")
            mech_by_repo[name] = mech("tutorial")
        out = tally.h2(reads, mech_by_repo)
        self.assertEqual(out["n"], 0)
        self.assertEqual(out["control"]["n"], 8)
        self.assertEqual(out["control"]["generative_reading"], "dead")

    def test_a_control_that_behaves_differently_leaves_the_reading_live(self):
        reads = {"rows": {}}
        mech_by_repo = {}
        for i in range(2):
            name = "p%d" % i
            reads["rows"][name] = read(arm="placebo", stars=10 + i)
            mech_by_repo[name] = mech("teaches_only")
        for i in range(6):
            name = "q%d" % i
            reads["rows"][name] = read(arm="placebo", stars=20 + i, class_="tutorial")
            mech_by_repo[name] = mech("tutorial")
        out = tally.h2(reads, mech_by_repo)
        self.assertEqual(out["control"]["generative_reading"], "live")

    def test_a_declared_population_that_differs_from_the_read_is_reported(self):
        reads = {"rows": {"a": read()}, "declared_population": "young documents",
                 "population_mismatch": "read 4, declared 10"}
        out = tally.h2(reads, {"a": mech("teaches_only")})
        self.assertEqual(out["population_mismatch"], "read 4, declared 10")


class GateUsesTheMechanicalClassTest(unittest.TestCase):
    def test_tally_does_not_consult_the_review_for_the_gate(self):
        """The gate is declared on the mechanical classification. `reviewed.json`
        exists to make the mechanical rule's error rate visible, and if it ever
        started feeding H1 the declared gate would no longer be the declared gate."""
        import inspect
        source = inspect.getsource(tally.h1)
        self.assertNotIn("reviewed", source)
        self.assertNotIn("reviewed_class", source)

    def test_build_reports_the_audit_beside_the_gate(self):
        result = tally.build()
        self.assertIn("audit", result)
        self.assertIn("classification", result)
        self.assertEqual(result["h2"]["key"], tally.H2_KEY)
        self.assertIn("hits", result["h2"])
        self.assertIn("control", result["h2"])

    def test_an_unreviewed_row_is_never_counted_as_agreement(self):
        rows = [row("a", "document"), row("b", "executable", arm="young")]
        out = tally.audit(rows, {"rows": {"a": {"reviewed_class": "document"}}})
        self.assertEqual(out["young"]["agree"], 1)
        self.assertEqual(out["young"]["unreviewed"], 1)
        self.assertEqual(out["young"]["disagree"], 0)

    def test_a_disagreement_is_counted_as_a_disagreement(self):
        rows = [row("a", "document")]
        out = tally.audit(rows, {"rows": {"a": {"reviewed_class": "executable",
                                               "reason": "why"}}})
        self.assertEqual(out["young"]["disagree"], 1)
        self.assertEqual(out["young"]["rows"][0]["reason"], "why")

    def test_boundary_rows_are_counted_separately(self):
        rows = [row("a", "document")]
        out = tally.audit(rows, {"rows": {"a": {"reviewed_class": "document",
                                               "boundary": True}}})
        self.assertEqual(out["young"]["boundary"], 1)
        self.assertEqual(out["young"]["agree"], 1)

    def test_population_completeness_is_reported(self):
        result = tally.build()
        self.assertIn("complete", result["population"])
        self.assertIn("by_arm", result["population"])


class CrossTabulationTest(unittest.TestCase):
    def test_cross_counts_only_the_requested_arm(self):
        rows = [row("d0", "document", arm="young"),
                row("x0", "executable", arm="mature", decided=False)]
        only = servingjoin.cross(rows, "young")
        self.assertEqual(only["document"]["n"], 1)
        self.assertEqual(only["executable"]["n"], 0)

    def test_cross_never_counts_an_undecided_row_as_served(self):
        rows = [row("d0", "document", decided=False, served=True),
                row("d1", "document", decided=True, served=True)]
        out = servingjoin.cross(rows, "young")["document"]
        self.assertEqual(out["decided"], 1)
        self.assertEqual(out["served"], 1)
        self.assertEqual(out["served_share"], 1.0)

    def test_cross_reports_a_null_share_rather_than_zero_for_an_undecided_class(self):
        rows = [row("d0", "document", decided=False)]
        out = servingjoin.cross(rows, "young")["document"]
        self.assertIsNone(out["served_share"])


class ReadShapeTest(unittest.TestCase):
    def test_a_missing_reads_json_is_a_failure_not_a_pass(self):
        ok, problems = __import__("readfields").check_reads()
        self.assertFalse(ok or not problems)   # either it is absent, or it is named

    def test_every_known_answer_case_still_classifies_as_declared(self):
        for label, cached, expected in classification.KNOWN_ANSWER:
            self.assertEqual(classification.classify(cached)["class"], expected,
                             msg=label)


class FetchCacheTest(unittest.TestCase):
    """The cache is the one place a budget limit can become a permanent claim.

    The core budget is 60 an hour and this experiment needs two requests per row
    over 61 rows, so a run runs out mid-population and every later row answers 403.
    If that answer is cached as a reading, "I could not ask today" becomes "this
    repository could not be read" and no later run re-asks -- which is exactly the
    dead-branch defect F032 records, where zero measured installs was not zero
    users. These cases hold the difference.
    """
    def setUp(self):
        import rootlisting
        self.rl = rootlisting

    def test_a_refused_half_is_not_complete(self):
        self.assertFalse(self.rl._complete({"contents": self.rl.REFUSED,
                                            "releases": 0}))
        self.assertFalse(self.rl._complete({"contents": [],
                                            "releases": self.rl.REFUSED}))

    def test_a_missing_half_is_not_complete(self):
        self.assertFalse(self.rl._complete({"contents": []}))
        self.assertFalse(self.rl._complete({}))

    def test_both_halves_answered_is_complete(self):
        self.assertTrue(self.rl._complete({"contents": [], "releases": 0}))

    def test_an_empty_repository_is_a_complete_answer(self):
        """404 on the contents API means no commits, which is a reading about the
        repository rather than a failure to read it. It must not be re-asked
        forever, and it must not become `executable`."""
        self.assertTrue(self.rl._complete({"contents": self.rl.EMPTY,
                                           "releases": 0}))

    def test_status_ignores_a_half_cached_row(self):
        rows = [{"repo": "a"}, {"repo": "b"}]
        self.assertEqual(self.rl.status(rows), (0, 2))


if __name__ == "__main__":
    unittest.main()
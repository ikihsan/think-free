#!/usr/bin/env python3
"""Falsification cases for the 014 instrument and its gate.

Written and run before the measurement touched a single incumbent, for the reason
`docs/policy/gate-falsification.md` gives: a gate written after seeing the data
is a rationalisation. Two of these cases exist because the hypothesis under test
predicts **low** numbers, so every failure mode that flatters it has to be
falsified positively rather than reasoned about.

The case F032 records is the one that matters most: the first census credited
npm downloads to a repository whose package belonged to somebody else, and the
miscount under-reported the incumbent of a mature niche. Counting a download for
the wrong project would do the same here, so the attribution check is asserted in
both directions and a rejected figure is still recorded.

Run: python3 -m unittest discover -s tests -p 'test_serving_stats.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "015-incumbent-serving"))

import attribution  # noqa: E402
import serving  # noqa: E402
import verdict as stats  # noqa: E402


def row(repo="owner/name", rate=None, cumulative=None, refused=None,
        unverified=None, cum_channel="ghreleases"):
    return {"repo": repo, "stars": 100,
            "rate": [{"channel": "npm:name", "value": v} for v in (rate or [])],
            "cumulative": [{"channel": cum_channel, "value": v, "assets": 3,
                            "releases": 3} for v in (cumulative or [])],
            "refused": refused or [], "unverified": unverified or []}


class AttributionTest(unittest.TestCase):
    """A name is not an identity. F032's exact case must be refused."""

    def test_repository_urls_are_parsed_in_the_shapes_metadata_emits(self):
        cases = [
            ("git+https://github.com/vitejs/vite.git", ("vitejs", "vite")),
            ("https://github.com/vitejs/vite", ("vitejs", "vite")),
            ("git@github.com:vitejs/vite.git", ("vitejs", "vite")),
            ("https://github.com/vitejs/vite/tree/main/pkg", None),
            ("https://gitlab.com/vitejs/vite", None),
            ("", None),
            (None, None),
        ]
        for url, expected in cases:
            got = attribution.declared_repo((url or "").strip())
            self.assertEqual(got, expected, url)

    def test_a_package_belonging_to_another_owner_is_not_this_project(self):
        self.assertFalse(serving.owned_by(("mrdrozdov", "please"),
                                           "thought-machine/please"))
        self.assertTrue(serving.owned_by(("thought-machine", "please"),
                                         "thought-machine/please"))
        self.assertFalse(serving.owned_by(None, "vitejs/vite"))

    def test_case_does_not_decide_attribution(self):
        self.assertTrue(serving.owned_by(("ViteJS", "Vite"), "vitejs/vite"))

    def test_a_rejected_attribution_is_recorded_rather_than_dropped(self):
        """An unverified figure must be visible to the reader, not silently gone."""
        r = row(repo="thought-machine/please", unverified=["npm:please"])
        self.assertIn("npm:please", r["unverified"])
        self.assertEqual(stats.classify(r), (0, 0, True))


class FloorsTest(unittest.TestCase):
    """The floors are declared; the gate must read them and not round them."""

    def test_below_the_rate_floor_is_not_served(self):
        self.assertFalse(stats.served(row(rate=[999])))
        self.assertTrue(stats.served(row(rate=[1000])))

    def test_release_floor_is_ten_thousand(self):
        self.assertFalse(stats.served(row(cumulative=[9999])))
        self.assertTrue(stats.served(row(cumulative=[10000])))

    def test_docker_floor_is_a_hundred_thousand(self):
        """Docker pulls are cumulative over the image's whole life, so a lower
        floor would count an old abandoned image as a served need."""
        self.assertFalse(stats.served(row(cumulative=[99999],
                                           cum_channel="dockerpulls")))
        self.assertTrue(stats.served(row(cumulative=[100000],
                                          cum_channel="dockerpulls")))

    def test_a_docker_pull_count_does_not_borrow_the_release_floor(self):
        """The two cumulative channels are floored independently, so a figure
        cannot pass by being read through the wrong channel."""
        self.assertFalse(stats.served(row(cumulative=[50000],
                                           cum_channel="dockerpulls")))

    def test_the_two_classes_are_reported_separately(self):
        """A cumulative hit is not a rate hit, and the tally says which."""
        r = row(rate=[500], cumulative=[20000])
        t = stats.tally([r])
        self.assertEqual(t["served"], 1)
        self.assertEqual(t["served_by_rate_channel"], 0)
        self.assertEqual(t["served_by_release_assets"], 1)

    def test_a_row_no_channel_could_read_is_undecided_not_zero(self):
        """Nothing read is not the same finding as nothing there."""
        rate, cumulative, undecided = stats.classify(row())
        self.assertTrue(undecided)
        self.assertEqual((rate, cumulative), (0, 0))
        self.assertEqual(stats.tally([row()])["decided"], 0)

    def test_a_zero_registry_figure_is_read_and_is_a_finding(self):
        """A registry that recognises a package and reports 0 downloads has
        answered the question. That is decided-and-unserved."""
        r = {"repo": "o/zero", "rate": [{"channel": "npm:x", "value": 0}],
             "cumulative": [], "refused": [], "unverified": []}
        rate, cumulative, undecided = stats.classify(r)
        self.assertFalse(undecided)
        self.assertEqual((rate, cumulative), (0, 0))
        self.assertFalse(stats.served(r))

    def test_publishing_nothing_is_not_a_figure_about_use(self):
        """The defect this experiment's first run contained.

        A repository with no release assets has told us about its *distribution*,
        not its use. Counting it as a decided zero put 13 of 30 incumbents into
        the denominator with no evidence in them and printed 40% served; leaving
        them out gives 12 of 17, or 71%. A project that ships nothing must not
        masquerade as a project nobody uses.
        """
        r = {"repo": "o/silent", "rate": [],
             "cumulative": [{"channel": "ghreleases", "value": 0, "assets": 0,
                             "releases": 0}],
             "refused": [], "unverified": []}
        self.assertTrue(stats.classify(r)[2])
        self.assertEqual(stats.tally([r])["decided"], 0)
        self.assertEqual(stats.tally([r])["undecided"], 1)

    def test_the_correction_moves_the_share_upward(self):
        """Stated so a later reader can see which way the correction moved it.

        Three projects that publish nothing and four that are read below the floor:
        the corrected tally drops the three, and the served share of what remains
        is 0 either way -- so the assertion is on the denominators, which is where
        the first run's error actually lived.
        """
        silent = [{"repo": "o/s%d" % i, "stars": 1, "rate": [],
                   "cumulative": [{"channel": "ghreleases", "value": 0, "assets": 0,
                                   "releases": 0}], "refused": [], "unverified": []}
                  for i in range(3)]
        quiet = [row(repo="o/u%d" % i, rate=[300]) for i in range(4)]
        t = stats.tally(silent + quiet)
        self.assertEqual((t["decided"], t["undecided"]), (4, 3))
        self.assertEqual(t["served"], 0)

    def test_a_refused_everywhere_row_is_undecided_in_both_arms(self):
        """A refusal is not an absence, and neither arm may count it as one."""
        r = {"repo": "o/refused", "rate": [], "cumulative": [],
             "refused": ["npm:x", "pypi:x", "ghreleases"], "unverified": []}
        self.assertTrue(stats.classify(r)[2])
        self.assertEqual(stats.tally([r])["undecided"], 1)


class GateTest(unittest.TestCase):
    """Both directions of the declared gate, and both inconclusive branches."""

    def many(self, served_n, total=10):
        """Decided rows: an unserved project *is* read, its figure is just low.

        A row no channel could read is a different case and is built explicitly
        where it is tested, because conflating "read as zero" with "not read" is
        the mistake the `undecided` branch exists to prevent.
        """
        rows = [row(repo="o/s%d" % i, rate=[5000]) for i in range(served_n)]
        rows += [row(repo="o/l%d" % i, rate=[500]) for i in range(total - served_n)]
        return rows

    def test_gate_says_survives_below_the_declared_half(self):
        verdict, _, _, _ = stats.gate(self.many(4), [])
        self.assertEqual(verdict, "survives")

    def test_gate_says_dead_at_or_above_the_declared_half(self):
        verdict, _, _, _ = stats.gate(self.many(5), [])
        self.assertEqual(verdict, "dead")

    def test_gate_is_inconclusive_when_a_placebo_is_served(self):
        """The instrument's own falsification arm outranks the population."""
        placebo = [row(repo="p/unused", rate=[99999])]
        verdict, reason, _, _ = stats.gate(self.many(9), placebo)
        self.assertEqual(verdict, "inconclusive")
        self.assertIn("p/unused", reason)

    def test_gate_is_inconclusive_above_the_declared_undecided_share(self):
        rows = self.many(9, total=10)
        verdict, reason, _, _ = stats.gate(rows, [])
        self.assertEqual(verdict, "dead")
        undecided_heavy = [row(repo="o/x%d" % i, rate=[], cumulative=[]) for i in range(3)]
        undecided_heavy += [row(repo="o/s%d" % i, rate=[5000]) for i in range(7)]
        verdict, reason, _, _ = stats.gate(undecided_heavy, [])
        self.assertEqual(verdict, "inconclusive")
        self.assertIn("undecided", reason)

    def test_gate_says_inconclusive_when_nothing_was_read(self):
        verdict, reason, _, _ = stats.gate([row(repo="o/a")], [])
        self.assertEqual(verdict, "inconclusive")
        self.assertIn("no incumbent", reason)

    def test_an_empty_sample_is_not_a_result(self):
        verdict, _, _, _ = stats.gate([], [])
        self.assertEqual(verdict, "inconclusive")

    def test_an_unreadable_placebo_arm_is_not_a_pass(self):
        """The declared placebo was five unreadable zero-star repositories.

        A false positive was impossible there, so the floors were never
        challenged. Reporting that arm as clean would claim a test that did not
        run -- the same dead-branch defect F032 records, in the opposite
        direction.
        """
        placebo = {"readable_controls": 0, "false_positives": [],
                   "verdict": "no control was readable, so the arm proves nothing"}
        verdict, reason, _, _ = stats.gate(self.many(9), [], placebo)
        self.assertEqual(verdict, "inconclusive")
        self.assertIn("never challenged", reason)

    def test_a_floor_that_fires_on_a_known_unused_control_is_reported(self):
        placebo = {"readable_controls": 5, "false_positives": ["p/fake"],
                   "verdict": "a floor fired on 1 of 5 readable controls"}
        verdict, reason, _, _ = stats.gate(self.many(9), [], placebo)
        self.assertEqual(verdict, "inconclusive")
        self.assertIn("p/fake", reason)

    def test_an_exercised_clean_arm_leaves_the_population_to_decide(self):
        placebo = {"readable_controls": 6, "false_positives": [],
                   "verdict": "a floor fired on 0 of 6 readable controls"}
        self.assertEqual(stats.gate(self.many(9), [], placebo)[0], "dead")
        self.assertEqual(stats.gate(self.many(2), [], placebo)[0], "survives")


if __name__ == "__main__":
    unittest.main()
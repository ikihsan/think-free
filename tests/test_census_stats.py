#!/usr/bin/env python3
"""Falsification cases for the T-0059 census instrument.

These cases were written and run before the census touched the network. They
exist because the first gate was specified on Spearman correlation, and the
synthetic case `test_spearman_cannot_resolve_the_sparse_regime` shows that
statistic cannot tell the only two situations apart that matter here. The gate
was changed on the strength of this test rather than after seeing a result, and
these tests keep that decision honest.

Run: python3 -m unittest discover -s tests -p 'test_census_stats.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "012-prior-art-predicts-adoption"))

import census  # noqa: E402
import stats  # noqa: E402
import usage  # noqa: E402


class OwnershipTest(unittest.TestCase):
    """A name match is not an identity, and treating it as one is fatal here.

    The first census credited 39,000,000 downloads/month to `PostHog/posthog`
    from a search for "agent session log", and 47 to `thought-machine/please`
    — the 2,616-star incumbent of the mature reproducible-build niche — because
    the npm package `please` belongs to `mrdrozdov/please`. Under-counting a
    niche's leader is precisely what manufactures the hypothesis's result, so
    the verifier must reject that case and not merely the case where a package
    declares no repository at all.
    """

    def test_repository_urls_are_parsed_in_the_shapes_registries_emit(self):
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
            m = usage.REPO_IN_URL.search((url or "").strip())
            got = (m.group(1).lower(), m.group(2).lower()) if m else None
            self.assertEqual(got, expected, url)

    def test_ownership_requires_an_exact_owner_and_name(self):
        self.assertTrue(usage.owned_by(("vitejs", "vite"), "vitejs/vite"))
        self.assertFalse(usage.owned_by(("mrdrozdov", "please"),
                                        "thought-machine/please"))
        self.assertFalse(usage.owned_by(None, "vitejs/vite"))

    def test_case_does_not_decide_ownership(self):
        self.assertTrue(usage.owned_by(("ViteJS", "Vite"), "vitejs/vite"))


class InstrumentTest(unittest.TestCase):
    """Two defects this file's self-check caught before any result existed.

    Both pushed measurements towards zero, which is the direction that flatters
    the hypothesis under test. A census with that bias built in does not report
    a wrong number; it reports the number it was built to produce.
    """

    def test_npm_two_response_shapes_are_both_read(self):
        """The bulk endpoint keys by package; the single one answers flat."""
        flat = {"downloads": 779837152, "start": "2026-09-04",
                "package": "vite"}
        keyed = {"vite": {"downloads": 779837152}}
        for shape in (flat, keyed):
            inner = shape.get("vite")
            inner = inner if isinstance(inner, dict) else shape
            self.assertEqual(inner.get("downloads"), 779837152)

    def test_a_throttle_is_not_recorded_as_zero_usage(self):
        """shields.io returns HTTP 200 with a rate-limit body.

        Reading it as a figure gives zero downloads for an installed package,
        so `parse_human` must refuse the text outright. Returning 0 instead of
        None here would be the bug, because 0 is a legitimate measurement for a
        published package nobody installs.
        """
        self.assertIsNone(usage.parse_human("rate limited by upstream service"))
        self.assertEqual(usage.parse_human("795M/month"), 795000000)

    def test_the_three_outcomes_stay_distinct(self):
        """REFUSED, None (absent) and 0 (measured as zero) are three facts."""
        self.assertIsNotNone(usage.REFUSED)
        self.assertNotEqual(usage.REFUSED, 0)
        self.assertIsNone(usage.parse_human("no data"))
        absent = usage.npm_bulk(["definitely-not-a-real-package-xyzzy"])
        self.assertIn(absent["definitely-not-a-real-package-xyzzy"], (None, 0))

    def test_refusals_are_counted_separately_from_zero_usage(self):
        rows = [{"names": ["a"], "usage_30d": 0, "usage_refused": ["pypi"]},
                {"names": ["b"], "usage_30d": 0, "usage_refused": []}]
        self.assertEqual(usage.refusals(rows), 1)


def niche(used_at, n=25, used_value=5000):
    """A leaderboard of n projects with exactly one used project, at index
    `used_at` (0 = leaderboard's first)."""
    stars = list(range(n, 0, -1))
    used = [0] * n
    used[used_at] = used_value
    return stars, used


class SpearmanTest(unittest.TestCase):

    def test_perfect_and_reversed(self):
        s = [100, 90, 80, 70, 60, 50, 40, 30]
        u = [900, 800, 700, 600, 500, 400, 300, 200]
        self.assertAlmostEqual(stats.spearman(s, u), 1.0, places=6)
        self.assertAlmostEqual(stats.spearman(s, list(reversed(u))), -1.0,
                               places=6)

    def test_spearman_cannot_resolve_the_sparse_regime(self):
        """The reason the primary statistic is not Spearman.

        One used project at the top and one at rank 3 of 25 are the situations
        the gate must separate. Spearman gives 0.340 against 0.283 - it does not
        separate them - while the star rank of the most-used project gives 1
        against 3. If this test ever fails, Spearman would again be a usable
        primary statistic and the gate's justification would need rewriting.
        """
        s1, u1 = niche(0)
        s3, u3 = niche(2)
        self.assertLess(abs(stats.spearman(s3, u3) - stats.spearman(s1, u1)),
                        0.2)
        self.assertEqual(stats.star_rank_of_most_used(s1, u1), 1)
        self.assertEqual(stats.star_rank_of_most_used(s3, u3), 3)

    def test_entirely_tied_side_is_undefined_not_zero(self):
        """An unanswerable question must read as None, never as 0.0.

        Zero would be indistinguishable from a real negative answer, which is
        exactly how this repository's own machine-fact gates were green on one
        VM and red on another for opposite reasons (F018).
        """
        s = [5, 4, 3, 2]
        self.assertIsNone(stats.spearman(s, [0, 0, 0, 0]))
        self.assertIsNone(stats.star_rank_of_most_used(s, [0, 0, 0, 0]))
        self.assertIsNone(stats.star_rank_of_most_used([7, 7, 7], [0, 5, 0]))


class OverlapTest(unittest.TestCase):

    def test_chance_overlap_is_capped_at_one(self):
        """At k=5 over n=25 every top-5 shares its one used member.

        Uncapped, chance reads 3.125 and the observed 1.0 looks like a failure.
        Capped at 1.0 the case correctly reports that the overlap carries no
        information.
        """
        s, u = niche(2)
        hit, frac, chance = stats.top_k_overlap(s, u)
        self.assertEqual(hit, 5)
        self.assertEqual(frac, 1.0)
        self.assertEqual(chance, 1.0)

    def test_overlap_can_still_carry_information(self):
        """With everything used, the overlap must separate a matching
        leaderboard from an inverted one, and the chance figure must not
        swallow the difference."""
        s = list(range(10, 0, -1))
        matching = list(range(100, 0, -10))
        self.assertEqual(stats.top_k_overlap(s, matching)[1], 1.0)
        self.assertEqual(stats.top_k_overlap(s, matching)[2], 1.0)
        hit, frac, _ = stats.top_k_overlap(s, list(reversed(matching)))
        self.assertEqual(frac, 0.0)
        self.assertEqual(hit, 0)


class ThresholdTest(unittest.TestCase):

    def test_fractions_are_reported_at_several_thresholds(self):
        u = [0, 1, 999, 1000, 5000, 200000]
        self.assertEqual(stats.used_fraction(u, 1), 0.833)
        self.assertEqual(stats.used_fraction(u, 1000), 0.5)
        self.assertEqual(stats.used_fraction(u, 100000), 0.167)

    def test_empty_is_none(self):
        self.assertIsNone(stats.used_fraction([]))


class GateTest(unittest.TestCase):
    """The gate on synthetic niches, in both directions."""

    @staticmethod
    def niche(key, age, used_at, n=25, max_usage=5000):
        stars, used = niche(used_at, n, max_usage)
        return {"key": key, "age": age, "n": n, "max_usage": max_usage,
                "star_rank_of_most_used": stats.star_rank_of_most_used(stars, used),
                "used_fraction_over_0": stats.used_fraction(used, 1),
                "spearman_stars_vs_usage": stats.spearman(stars, used)}

    def test_gate_says_h_survives_on_the_expected_data(self):
        rows = [self.niche("a", "young", 7), self.niche("b", "young", 12),
                self.niche("c", "young", 20), self.niche("d", "mature", 9),
                self.niche("e", "mature", 15)]
        verdict, detail = census.gate(rows)
        self.assertTrue(verdict.startswith("H SURVIVES"), verdict)
        self.assertEqual(sorted(detail["most_used_not_leader"]),
                         ["a", "b", "c", "d", "e"])

    def test_gate_says_h_dead_on_the_opposite_data(self):
        rows = [self.niche("a", "young", 0, max_usage=900000),
                self.niche("b", "young", 0, max_usage=400000),
                self.niche("c", "mature", 0, max_usage=200000),
                self.niche("d", "mature", 3, max_usage=70000),
                self.niche("e", "mature", 5, max_usage=40000)]
        verdict, detail = census.gate(rows)
        self.assertTrue(verdict.startswith("H DEAD"), verdict)
        self.assertEqual(sorted(detail["most_used_is_leader"]), ["a", "b", "c"])

    def test_gate_refuses_to_round_up_a_split_result(self):
        """Two each way is not a pass in either direction. This is the case the
        mission's own declared gates have twice failed to handle (F010, a gate
        that could not fail; F024, a restated number the obvious rule missed)."""
        rows = [self.niche("a", "young", 0, max_usage=900000),
                self.niche("b", "young", 0, max_usage=400000),
                self.niche("c", "young", 9), self.niche("d", "mature", 14)]
        verdict, _ = census.gate(rows)
        self.assertTrue(verdict.startswith("INCONCLUSIVE"), verdict)

    def test_a_leader_that_is_used_barely_does_not_count_as_evidence(self):
        """#1 on the leaderboard with 4 downloads a month is not a dominant
        incumbent, so it must not satisfy the dead-H branch."""
        rows = [self.niche("a", "young", 0, max_usage=4),
                self.niche("b", "young", 0, max_usage=9),
                self.niche("c", "young", 0, max_usage=0),
                self.niche("d", "mature", 11), self.niche("e", "mature", 4)]
        verdict, detail = census.gate(rows)
        self.assertNotIn("a", detail["most_used_is_leader"])
        self.assertFalse(verdict.startswith("H DEAD"), verdict)


if __name__ == "__main__":
    unittest.main()
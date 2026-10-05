#!/usr/bin/env python3
"""Falsification cases for 017's cross-tabulation and its fetch cache.

Split from `test_artifact_tally.py` at the 300-line cap, by subject rather than by
size: the gate's arithmetic is one question and the population plumbing under it
is another.

`CrossTabulationTest` holds the property the whole comparison rests on - an
undecided row never becomes a served row - because 015's own first run got that
wrong in the opposite direction and named the correction.

`FetchCacheTest` holds the one place a budget limit can become a permanent claim.
The core budget is 60 an hour and this experiment needs two requests per row, so a
run runs out mid-population and every later row answers 403. If that answer is
cached as a reading, "I could not ask today" becomes "this repository could not
be read" and no later run re-asks - which is the dead-branch defect F032 records,
where zero measured installs was not zero users. This experiment hit it twice and
both rows classified as `unreadable`, which looks like a finding.

Run: python3 -m unittest discover -s tests -p 'test_artifact_population.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "017-incumbent-artifact-type"))

import servingjoin  # noqa: E402


def row(repo, klass, arm="young", decided=True, served=False, stars=100):
    return {"repo": repo, "arm": arm, "group": arm, "need": "n", "stars": stars,
            "class": klass, "class_reason": None, "hits": [], "releases": None,
            "root_size": None, "measured_by_015": True,
            "served": (served if decided else None), "best_rate": 0,
            "best_cumulative": 0, "undecided": not decided}


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

    def test_an_unreadable_row_is_never_counted_as_a_document(self):
        """The whole reason `unreadable` is its own class: a row this instrument
        cannot open must not land in the class whose claim is that the repository
        is prose."""
        rows = [row("u0", "unreadable", decided=False),
                row("d0", "document", decided=True, served=False)]
        out = servingjoin.cross(rows, "young")
        self.assertEqual(out["unreadable"]["n"], 1)
        self.assertEqual(out["document"]["n"], 1)
        self.assertEqual(out["unreadable"]["served"], 0)


class FetchCacheTest(unittest.TestCase):
    """The one place a budget limit can become a permanent claim.

    The core budget is 60 an hour and this experiment needs two requests per row,
    so a run runs out mid-population and every later row answers 403. If that
    answer is cached as a reading, "I could not ask today" becomes "this
    repository could not be read" and no later run re-asks -- which is the
    dead-branch defect F032 records, where zero measured installs was not zero
    users. This experiment hit it twice on its first fetch, and both rows
    classified as `unreadable`, which is indistinguishable from a finding.
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
        self.assertEqual(self.rl.status([{"repo": "a"}, {"repo": "b"}]), (0, 2))

    def test_the_committed_cache_holds_no_refusal(self):
        """The real cache, not a fixture: this is the property that was violated."""
        cache = self.rl.load_cache()
        self.assertTrue(cache, msg="no cache committed")
        for name, entry in cache.items():
            self.assertNotEqual(entry.get("contents"), self.rl.REFUSED, msg=name)
            self.assertNotEqual(entry.get("releases"), self.rl.REFUSED, msg=name)

    def test_one_vocabulary_for_a_refusal(self):
        """The fetcher declared `"refused"` and the classifier compared against
        `"refused:upstream"`, so a refused listing matched no branch and reached
        the `unexpected_shape` fallback -- the right class for the wrong reason,
        and one edit away from the wrong count."""
        import classification
        self.assertEqual(self.rl.REFUSED, classification.REFUSED)
        out = classification.classify({"contents": self.rl.REFUSED,
                                       "releases": self.rl.REFUSED})
        self.assertEqual(out["class"], "unreadable")
        self.assertEqual(out["reason"], "refused")

    def test_a_refused_row_is_never_a_shape_fallback(self):
        """A row that fell through to `unexpected_shape` is a row the reason
        cannot explain, so the reason names the refusal."""
        import classification
        out = classification.classify({"contents": self.rl.REFUSED,
                                       "releases": 0})
        self.assertEqual(out["reason"], "refused")
        self.assertNotEqual(out["reason"], "unexpected_shape")

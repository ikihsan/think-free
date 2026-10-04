#!/usr/bin/env python3
"""Falsification cases for 015's relevance filter, name guesses and self-check.

Split out of `test_serving_stats.py` at the 300-line cap, by invariant: that file
holds the cases about **whether a figure counts**, and this one holds the cases
about **which project a figure is about to be attached to**. The second question
is the one F032 shows is fatal when it is answered by a name match.

Run: python3 -m unittest discover -s tests -p 'test_serving_selection.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "015-incumbent-serving"))

import attribution  # noqa: E402
import selfcheck  # noqa: E402
import serving  # noqa: E402
import verdict as stats  # noqa: E402


class GuessTest(unittest.TestCase):
    """Names are guessed mechanically, so a wrong guess can only lower a figure."""

    def test_a_common_suffix_yields_a_second_guess(self):
        self.assertEqual(serving.guesses("acme/ripgrep-cli"), ["ripgrep-cli", "ripgrep"])

    def test_a_short_name_is_not_stripped_to_nothing(self):
        self.assertEqual(serving.guesses("acme/js"), ["js"])

    def test_guesses_are_unique_and_never_empty(self):
        out = serving.guesses("acme/tool")
        self.assertEqual(out, sorted(set(out), key=out.index))
        self.assertTrue(out)


class OnTopicTest(unittest.TestCase):
    """The relevance filter is mechanical, so it can be asserted rather than trusted.

    It exists because the population itself carries F030's defect: the query
    `flashcards anki` returns `donnemartin/system-design-primer`. A filter tuned
    by hand could be tuned in whichever direction flatters the answer.
    """

    def test_stopwords_and_short_tokens_are_not_content_terms(self):
        terms = stats.content_terms("a tool for the web")
        self.assertNotIn("the", terms)
        self.assertNotIn("for", terms)
        self.assertNotIn("tool", terms)
        self.assertEqual(terms, {"web"})

    def test_a_real_content_term_survives(self):
        self.assertIn("flashcard", stats.content_terms("flashcard spaced repetition"))
        self.assertIn("uptime", stats.content_terms("uptime monitor"))

    def test_an_off_topic_repository_is_excluded(self):
        """The case that motivated the arm: 373k stars, nothing to do with anki."""
        row = {"repo": "donnemartin/system-design-primer", "stars": 373170,
               "desc": "Everything you need to know about system design",
               "phrasings": ["flashcards anki"]}
        self.assertFalse(stats.is_ontopic(row))

    def test_a_matching_description_keeps_the_repository(self):
        row = {"repo": "ankitects/anki", "stars": 31752, "desc": "flashcards",
               "phrasings": ["flashcard spaced repetition"]}
        self.assertTrue(stats.is_ontopic(row))

    def test_the_filter_selects_a_subset_never_a_superset(self):
        rows = [{"repo": "a/anki", "desc": "flashcards", "phrasings": ["flashcards anki"]},
                {"repo": "b/unrelated", "desc": "systems", "phrasings": ["flashcards anki"]}]
        self.assertEqual([r["repo"] for r in stats.ontopic(rows)], ["a/anki"])

    def test_a_row_with_no_phrasing_is_excluded_rather_than_assumed_on_topic(self):
        """A repository nothing phrased cannot be judged relevant to a need."""
        self.assertFalse(stats.is_ontopic({"repo": "a/b", "desc": "anki", "phrasings": []}))


class SelfcheckShapeTest(unittest.TestCase):
    """The self-check must contain cases in both directions, or it proves nothing."""

    def test_the_self_check_asserts_known_used_tools(self):
        self.assertGreaterEqual(len(selfcheck.SELFCHECK), 5)
        for label, fn, floor in selfcheck.SELFCHECK:
            self.assertGreater(floor, 0, label)
            self.assertTrue(callable(fn), label)

    def test_the_release_channel_is_covered_by_a_selfcheck_case(self):
        """The channel added to close F032's dead branch must itself be falsified."""
        labels = " ".join(l for l, _, _ in selfcheck.SELFCHECK)
        self.assertIn("release", labels)

    def test_the_bottleneck_incumbent_is_not_the_only_release_case(self):
        """`thought-machine/please` was invisible to every registry channel.

        If the release channel only ever saw it, the branch would be closed by one
        anecdote. `cli/cli` is in the self-check instead, and `please` is read in
        `results.json` as data.
        """
        labels = " ".join(l for l, _, _ in selfcheck.SELFCHECK)
        self.assertNotIn("please", labels)

    def test_the_self_check_counts_its_negative_case(self):
        """The refusal case is the one that catches F032, so it is inside the count.

        `selfcheck` prints and returns `failed`; the assertion is that the one
        negative case is *added to the same counter* rather than reported apart,
        because a negative case reported separately is a case that can be dropped.
        """
        import inspect
        src = inspect.getsource(selfcheck.run)
        self.assertIn("failed += 1", src)
        self.assertIn("len(SELFCHECK) + 1", src)


class TransportTest(unittest.TestCase):
    """The three outcomes must stay apart, because the hypothesis predicts zero.

    A refusal folded into a zero reads as "nobody uses this tool", which is the
    finding this experiment is looking for. That is F032's third instrument defect
    -- shields.io answering HTTP 200 for a throttle -- in the same shape.
    """

    def test_a_missing_resource_is_an_absence_not_a_refusal(self):
        self.assertIsNone(attribution.jget("https://registry.npmjs.org/%s/latest" % _NO_SUCH_PKG))
        self.assertNotEqual(attribution.jget("https://registry.npmjs.org/%s/latest" % _NO_SUCH_PKG),
                            attribution.REFUSED)

    def test_a_body_that_is_not_json_is_a_refusal_not_a_zero(self):
        self.assertEqual(attribution.jget("https://example.invalid/not-json"), attribution.REFUSED)

    def test_owned_by_normalises_both_sides(self):
        self.assertTrue(attribution.owned_by(("BurntSushi", "ripgrep"),
                                              "burntsushi/ripgrep"))


_NO_SUCH_PKG = "origin-serving-no-such-package-4f2a9c"


if __name__ == "__main__":
    unittest.main()

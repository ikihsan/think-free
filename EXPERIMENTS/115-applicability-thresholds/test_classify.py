#!/usr/bin/env python3
"""Regression tests for the E115 classifier.

`classify.py`'s docstring promises these: the two artifact shapes
M1.md reports are *deliberately left in place*, because the precision
figure (11 of 15 flagged spans hand-read as real) is a statement
about this extractor. These tests pin both shapes so that number
stays reproducible if the regexes ever change.

What is pinned:

1. **Comma-grouped numbers.** `\\b` matches between the comma and
   the `0` of "1,000", so the extractor reports "000 or more
   employees". This is F116's unanchored-substring class, in the
   exact place the E113 protocol said to guard against it.
2. **Adjacent nouns.** "salaries less than employees at the GS-11,
   step 1" is a comparison between two salaries, not a headcount,
   and the threshold vocabulary matches it anyway.

A repaired extractor would fail these tests, and that is the point:
changing them means M1.md's 11-of-15 has to be re-measured.

Run: python3 test_classify.py
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import classify  # noqa: E402


def _spans(xml_text):
    lab, detail = classify.label(xml_text.encode("utf-8"))
    return lab, [r["span"] for r in detail["threshold_spans"]]


class TestPinnedDefectShapes(unittest.TestCase):
    """The two artifacts M1.md reports, pinned where they occur."""

    def test_comma_grouped_number_matches_inside_the_group(self):
        # The real text is "which has 1,000 or more employees"
        # (the shape of sections 1614.702, 4262.7, 4262.8).
        lab, spans = _spans("<P>which has 1,000 or more employees</P>")
        self.assertEqual(lab, "need")
        self.assertEqual(spans, ["000 or more employees"])

    def test_salary_comparison_matches_threshold_vocabulary(self):
        # The real text is "salaries less than employees at the
        # GS-11, step 1" (section 1614.203): a comparison between
        # two salaries, not a headcount.
        lab, spans = _spans(
            "<P>salaries less than employees at the GS-11, step 1</P>"
        )
        self.assertEqual(lab, "need")
        self.assertEqual(spans, ["less than employees"])


class TestRealThresholdsStillLabel(unittest.TestCase):
    """The shapes the extractor exists to find."""

    def test_plain_headcount_threshold(self):
        lab, spans = _spans(
            "<P>employs 50 or more employees for each working day</P>"
        )
        self.assertEqual(lab, "need")
        self.assertEqual(spans, ["50 or more employees"])

    def test_divergent_rule_is_flagged(self):
        # FMLA shape (the actual text of section 825.104(a)): a
        # window over a period is not a headcount at a moment, so
        # the row must come out 'matched', not 'need'.
        lab, detail = classify.label(
            b"<P>employs 50 or more employees for each working day "
            b"during each of 20 or more calendar workweeks in the "
            b"current or preceding calendar year</P>"
        )
        self.assertEqual(lab, "matched")
        self.assertEqual(detail["n_divergent_spans"], 1)
        self.assertTrue(detail["threshold_spans"][0]["divergent"])

    def test_no_threshold_is_unlabelled(self):
        lab, detail = classify.label(b"<P>This section defines terms.</P>")
        self.assertEqual(lab, "unlabelled")
        self.assertEqual(detail["threshold_spans"], [])


class TestPartSplitting(unittest.TestCase):
    """`label_part` must keep a section's body with its own heading."""

    PART = (
        b'<DIV6><HEAD>Subpart A</HEAD>'
        b'<DIV8 TYPE="SECTION"><HEAD>&#167; 1.1 Scope and purpose</HEAD>'
        b'<P>Applies to employers with 20 or more employees.</P></DIV8>'
        b'<DIV8 TYPE="SECTION"><HEAD>&#167; 1.2 Penalties</HEAD>'
        b'<P>Nothing numeric here.</P></DIV8></DIV6>'
    )

    def test_sections_are_split_with_headings_and_citations(self):
        rows = classify.label_part(self.PART)
        self.assertEqual(len(rows), 2)
        self.assertIn("Scope and purpose", rows[0]["heading"])
        self.assertTrue(rows[0]["heading_is_scope"])
        self.assertEqual(rows[0]["label_outcome"], "need")
        self.assertEqual(rows[1]["label_outcome"], "unlabelled")
        self.assertFalse(rows[1]["heading_is_scope"])

    def test_definitions_is_a_scope_heading(self):
        # The SCOPE_HEADING vocabulary includes "definitions":
        # a threshold in a definitions section is still in a
        # scope-shaped section.
        self.assertTrue(
            classify.SCOPE_HEADING.search("§ 1.3 Definitions")
        )

    def test_first_piece_is_not_reported_as_a_section(self):
        # pieces[0] is the part header before the first DIV8; the
        # first attempt (splitting on HEAD) shredded it into rows.
        rows = classify.label_part(self.PART)
        self.assertNotIn("Subpart A", [r["heading"] for r in rows])


if __name__ == "__main__":
    unittest.main(verbosity=2)

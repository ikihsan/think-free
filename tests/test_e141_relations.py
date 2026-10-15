#!/usr/bin/env python3
"""E141: falsification tests for the rational reader and the two relations.

The empirical controls in `recover.py` are the real evidence; these exist so a
reader can check the instrument's edges without re-fetching 11 MB of HELM. Each
test names what would make it fail.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "EXPERIMENTS", "141-scorer-false-negatives"))

from relations import eq_t1, eq_t2, float_value, norm_eq, rational_value  # noqa: E402


class RationalReaderTest(unittest.TestCase):
    """Fails if the grammar admits anything it cannot prove, or refuses a
    fraction it can."""

    def test_exact_fractions(self) -> None:
        for text, want in (("1/2", "1/2"), ("0.5", "1/2"), ("50", "50"),
                           ("-7/4", "-7/4"), ("(2)/(3)", "2/3"),
                           ("2**3", "8"), ("2**-1", "1/2")):
            v = rational_value(text)
            self.assertIsNotNone(v, text)
            self.assertEqual(str(v), want, text)

    def test_thousands_separator_but_not_tuples(self) -> None:
        self.assertEqual(str(rational_value("6,840")), "6840")
        # `3,4` is ambiguous between a number and a pair; refusing is the
        # sound choice and a wrong guess here would be a false positive.
        self.assertIsNone(rational_value("(3,4)"))

    def test_outside_the_grammar_is_refused_not_assumed(self) -> None:
        for text in ("x+1", "sqrt(2)", "pi", "\\infty", "5(3)", "inf",
                     "1/0", "2**0.5", "", "1+", "abc"):
            self.assertIsNone(rational_value(text), text)

    def test_no_name_or_call_can_be_smuggled_in(self) -> None:
        # The reader is not `eval`. Anything with a letter in it is out.
        for text in ("__import__('os')", "1;2", "open('x')", "2 if 1 else 3"):
            self.assertIsNone(rational_value(text), text)


class RelationTest(unittest.TestCase):
    """Fails if the harness's own operator or the wider relation drifts."""

    def test_norm_eq_reproduces_the_harness_rule(self) -> None:
        self.assertTrue(norm_eq(r"\frac{1}{2}", r"\dfrac{1}{2}"))
        self.assertTrue(norm_eq(r"\frac14", r"\frac{1}{4}"))
        # The harness's normalizer does NOT strip a thousands separator. That is
        # not an oversight in this file: it is one of the four P1 rows E141
        # recovered, and asserting otherwise here would hide the finding.
        self.assertFalse(norm_eq("6,840", "6840"))
        # The two rows E136 documented as the harness's own false negatives.
        self.assertFalse(norm_eq(r"\frac{3}{2}", "1.5"))
        self.assertFalse(norm_eq(r"\frac{7}{12}", r"\frac{35}{60}"))

    def test_eq_t1_is_a_strict_superset_of_norm_eq(self) -> None:
        pairs = [(r"\frac{1}{2}", r"\dfrac{1}{2}"), ("1/2", "0.5"),
                 (r"\frac{3}{2}", "1.5"), ("6840", "6,840"),
                 (r"\frac{4}{11}", r"\frac{44}{121}"), ("5", "6"),
                 ("x", "x"), ("0.333", r"\frac{1}{3}")]
        for a, b in pairs:
            wide, _ = eq_t1(a, b)
            self.assertTrue(wide or not norm_eq(a, b), (a, b))

    def test_eq_t1_refuses_different_values_that_look_close(self) -> None:
        for a, b in ((r"\frac{1}{5}", r"\frac{4}{5}"), ("1/2", "0.51"),
                     (r"\frac{1}{3}", "0.334"), ("(2,1)", "(2,2)"),
                     (r"x^9+6859", r"x^9+361"), ("-16", "-2")):
            ok, _ = eq_t1(a, b)
            self.assertFalse(ok, (a, b))

    def test_t2_is_only_a_tolerance_tier(self) -> None:
        # T2's declared tolerance is 1e-9 relative, which is far below any
        # rounding a model would print: 0.333 against 1/3 is rejected, as it was
        # on all 2,874 rows. T2 therefore fires only on differences no reader
        # would call a difference, and reported zero recoveries, as declared.
        self.assertFalse(eq_t1(r"\frac{1}{3}", "0.333")[0])
        self.assertFalse(eq_t2(r"\frac{1}{3}", "0.333"))
        self.assertTrue(eq_t2("0.5000000001", "0.5"))
        self.assertFalse(eq_t2(r"\frac{1}{2}", "0.5"))
        self.assertEqual(float_value("6,840"), 6840.0)
        self.assertIsNone(float_value("sqrt(2)"))


if __name__ == "__main__":
    unittest.main()
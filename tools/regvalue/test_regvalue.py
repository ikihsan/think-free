#!/usr/bin/env python3
"""Tests for regvalue tool."""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regvalue import (
    normalize, extract, canonical, numeric_multiset,
    compare_canonical, compare_numeric, _money, _date, _code
)


class TestNormalize(unittest.TestCase):
    def test_html_tags_removed(self):
        self.assertEqual(normalize("<p>Hello</p>"), "Hello")
    
    def test_entities_decoded(self):
        # html.unescape decodes & to &, etc.
        self.assertEqual(normalize("&"), "&")
    
    def test_whitespace_collapsed(self):
        self.assertEqual(normalize("a\n\nb  c"), "a b c")


class TestExtract(unittest.TestCase):
    def test_money_extraction(self):
        text = "The penalty is \$12,500,000 per violation."
        vals = extract(text)
        self.assertIn(("money", "$12,500,000"), vals)
    
    def test_date_extraction(self):
        text = "Effective January 15, 2024."
        vals = extract(text)
        self.assertIn(("date", "January 15, 2024"), vals)
    
    def test_code_extraction(self):
        text = "See 10 CFR 52.63(a)."
        vals = extract(text)
        self.assertIn(("code", "10 CFR 52.63(a)"), vals)
    
    def test_no_nested_double_count(self):
        # "49 CFR 1002.3(a)" should count once, not as 49, 1002.3, etc.
        text = "49 CFR 1002.3(a)"
        vals = extract(text)
        # Should only have one code match
        codes = [v for v in vals if v[0] == "code"]
        self.assertEqual(len(codes), 1)


class TestCanonical(unittest.TestCase):
    def test_money_canonical(self):
        text = "The penalty is \$12,500,000."
        canon = canonical(text)
        self.assertIn(("money", 12500000.0), canon)
    
    def test_date_canonical(self):
        text = "Effective January 15, 2024."
        canon = canonical(text)
        self.assertIn(("date", (2024, 1, 15)), canon)
    
    def test_money_scale(self):
        text = "The cost is \$5 million."
        canon = canonical(text)
        self.assertIn(("money", 5000000.0), canon)
    
    def test_code_canonical(self):
        text = "See 10 CFR 52.63(a)."
        canon = canonical(text)
        # Code canonicalization removes spaces and dots but keeps parentheses
        self.assertIn(("code", "10cfr5263(a)"), canon)


class TestNumericMultiset(unittest.TestCase):
    def test_matches_across_kinds(self):
        ref = "The penalty is \$12,500,000."
        sub = "The penalty is 12500000 dollars."
        # Canonical mode distinguishes money vs num
        self.assertNotEqual(canonical(ref), canonical(sub))
        # Numeric mode matches
        self.assertEqual(numeric_multiset(ref), numeric_multiset(sub))
    
    def test_sorted(self):
        text = "Values: 100, 50, 200"
        nums = numeric_multiset(text)
        self.assertEqual(nums, [50.0, 100.0, 200.0])


class TestCompareCanonical(unittest.TestCase):
    def test_match(self):
        ref = "Penalty \$100 effective Jan 1, 2024."
        sub = "Penalty \$100 effective Jan 1, 2024."
        result = compare_canonical(ref, sub)
        self.assertEqual(result["verdict"], "match")
    
    def test_mismatch_missing(self):
        ref = "Penalty \$100 and \$200."
        sub = "Penalty \$100."
        result = compare_canonical(ref, sub)
        self.assertEqual(result["verdict"], "mismatch")
        self.assertEqual(len(result["missing"]), 1)
    
    def test_mismatch_extra(self):
        ref = "Penalty \$100."
        sub = "Penalty \$100 and \$200."
        result = compare_canonical(ref, sub)
        self.assertEqual(result["verdict"], "mismatch")
        self.assertEqual(len(result["extra"]), 1)


class TestCompareNumeric(unittest.TestCase):
    def test_match(self):
        ref = "Penalty \$100."
        sub = "Penalty 100 dollars."
        result = compare_numeric(ref, sub)
        self.assertEqual(result["verdict"], "match")
    
    def test_mismatch(self):
        ref = "Penalty \$100."
        sub = "Penalty \$200."
        result = compare_numeric(ref, sub)
        self.assertEqual(result["verdict"], "mismatch")


class TestMoneyParsing(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(_money("\$12,500,000"), 12500000.0)
    
    def test_million(self):
        self.assertEqual(_money("\$5 million"), 5000000.0)
    
    def test_billion(self):
        self.assertEqual(_money("\$2 billion"), 2000000000.0)
    
    def test_thousand(self):
        self.assertEqual(_money("\$10 thousand"), 10000.0)


class TestDateParsing(unittest.TestCase):
    def test_month_name(self):
        self.assertEqual(_date("January 15, 2024"), (2024, 1, 15))
    
    def test_abbreviated(self):
        self.assertEqual(_date("Jan 15, 2024"), (2024, 1, 15))
    
    def test_day_first(self):
        self.assertEqual(_date("15 January 2024"), (2024, 1, 15))
    
    def test_slash_us_format(self):
        # Assumes US format MM/DD/YYYY
        self.assertEqual(_date("1/15/2024"), (2024, 1, 15))
        self.assertEqual(_date("12/31/2024"), (2024, 12, 31))


class TestCodeCanonical(unittest.TestCase):
    def test_cfr(self):
        self.assertEqual(_code("10 CFR 52.63(a)"), "10cfr5263(a)")
    
    def test_usc(self):
        self.assertEqual(_code("42 U.S.C. 1395"), "42usc1395")
    
    def test_fr(self):
        self.assertEqual(_code("91 FR 52593"), "91fr52593")


if __name__ == "__main__":
    unittest.main()
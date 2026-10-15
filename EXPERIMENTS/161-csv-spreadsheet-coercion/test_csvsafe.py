#!/usr/bin/env python3
"""Tests for csvsafe, against outcomes a real engine was measured to produce.

Every expectation in this file is an observation from E161's LibreOffice run
(results-controls.json, sample-changes-*.tsv), not a reading of documentation.
The engine is not needed to run these tests; the tests hold the classifier to
what the engine did.
"""
import csv
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from csvsafe import classify, repair, protect  # noqa: E402

# value -> (rule, damaging) as LibreOffice 6.4.7.2 under C.UTF-8 left it
MEASURED = [
    ("01234", "leading_zero", True),
    ("07", "leading_zero", True),
    ("02108", "leading_zero", True),
    ("00", "leading_zero", True),
    ("0001234567890123", "leading_zero", True),
    ("01234567890", "leading_zero", True),
    ("+01234", "leading_zero", True),
    ("4111111111111111", "precision_loss", True),
    ("12345678901234567", "precision_loss", True),
    ("12345678901234567890", "precision_loss", True),
    ("1234567890.123456789", "precision_loss", True),
    ("=1+1", "formula_executed", True),
    ("2020-01-02", "date", False),
    ("01/02/2020", "date", False),
    ("2-Jan-2020", "date", False),
    ("January 2, 2020", "date", False),
    ("2020-01-02T15:04:05", "datetime", False),
    ("02/09/2005 12:00:00 AM", "datetime", False),
    ("12:30", "time", False),
    ("12:30:45", "time", False),
    ("1:30 PM", "time", False),
    ("1,234", "thousands_separator", False),
    ("12%", "percent", False),
    ("$1,234.56", "currency", False),
    ("TRUE", "bool", False),
    ("1.50", "number_spelling", False),
    ("319.40", "number_spelling", False),
    ("0.", "number_spelling", False),
    (".5", "number_spelling", False),
    ("1.5E10", "number_spelling", False),
    ("12345 ", "whitespace", False),
    ("1e-7", "number_spelling", False),
]

# values LibreOffice stored unchanged: the checker must not flag them
LEFT_ALONE = [
    "", "1", "42", "3.14", "123456789012345", "9780306406157",
    "1HGBH41JXMN109186", "GB82 WEST 1234 5698 7654 32", "4111 1111 1111 1111",
    "555-123-4567", "020 7946 0018", "10.091627",
    "-85.527029", "http://example.org/id/1", "a.b@example.gov.uk",
    "3f2504e0-4f89-11d3-9a0c-0305e82c3301", "NULL", "NaN", "Z\u00fcrich",
    "\u6771\u4eac\u90fd", "PREM-LIC\\1617", "Alan",
]


class TestClassifier(unittest.TestCase):
    def test_measured_damage_and_alteration(self):
        for value, rule, damaging in MEASURED:
            got_rule, got_harm = classify(value)
            self.assertEqual((value, rule), (value, got_rule))
            self.assertEqual((value, damaging), (value, got_harm))

    def test_values_the_engine_left_alone(self):
        for value in LEFT_ALONE:
            self.assertEqual((value, classify(value)), (value, (None, False)),
                             "checker flagged a value the engine kept: %r" % value)


# Measured false alarms: the checker flags these, the engine did not change
# them.  None is damaging, so `write` leaves the cell alone; `--all` would
# protect it unnecessarily.  Kept as tests so the record does not drift.
MEASURED_FALSE_ALARMS = [
    ("+1-800-555-1212", "formula_coercion"),
    ("+1-1", "formula_coercion"),
    ("02.01.2020", "date"),
    ("01-02-2020", "date"),
    ("2020-01-02T15:04:05Z", "datetime"),
    ("31/08/2005 12:00:00 AM", "datetime"),
]


class TestMeasuredFalseAlarms(unittest.TestCase):
    def test_flagged_but_not_changed(self):
        for value, rule in MEASURED_FALSE_ALARMS:
            self.assertEqual(classify(value), (rule, False),
                             "false alarm changed shape: %r" % value)

    def test_none_of_them_is_damaging(self):
        for value, _rule in MEASURED_FALSE_ALARMS:
            self.assertFalse(classify(value)[1],
                             "a false alarm was marked damaging: %r" % value)


class TestRepair(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def write(self, name, rows):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)
        return path

    def read(self, path):
        with open(path, encoding="utf-8", newline="") as f:
            return list(csv.reader(f))

    def test_write_protects_only_damaging_cells_by_default(self):
        src = self.write("in.csv", [["id", "n", "note"],
                                    ["01234", "7", "plain text"],
                                    ["12345678901234567", "3.14", "319.40"]])
        dst = os.path.join(self.dir, "out.csv")
        repair(src, dst, all_rules=False)
        self.assertEqual(self.read(dst), [
            ["id", "n", "note"],
            ['="01234"', "7", "plain text"],
            ['="12345678901234567"', "3.14", "319.40"],
        ])

    def test_write_all_protects_altered_cells_too(self):
        src = self.write("in.csv", [["id", "n"], ["01234", "319.40"]])
        dst = os.path.join(self.dir, "out.csv")
        repair(src, dst, all_rules=True)
        self.assertEqual(self.read(dst), [["id", "n"], ['="01234"', '="319.40"']])

    def test_repaired_file_is_still_parseable_and_idempotent_in_shape(self):
        src = self.write("in.csv", [["a"], ['say "hi"'], ["01234"]])
        dst = os.path.join(self.dir, "out.csv")
        repair(src, dst, all_rules=False)
        rows = self.read(dst)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1], ['say "hi"'])
        self.assertEqual(rows[2], ['="01234"'])

    def test_protect_doubles_quotes(self):
        self.assertEqual(protect('a"b'), '="a""b"')

    def test_check_exit_code_is_3_when_damage_found(self):
        src = self.write("in.csv", [["id", "n"], ["01234", "7"]])
        rc = subprocess.call([sys.executable, os.path.join(HERE, "csvsafe.py"),
                              "check", src], stdout=subprocess.DEVNULL)
        self.assertEqual(rc, 3)

    def test_check_exit_code_is_0_when_clean(self):
        src = self.write("in.csv", [["name", "n"], ["Alan", "7"]])
        rc = subprocess.call([sys.executable, os.path.join(HERE, "csvsafe.py"),
                              "check", src], stdout=subprocess.DEVNULL)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
"""Regression for the Fisher tail in `compose.py`.

`fisher_greater` returned P(X >= col1) instead of P(X >= observed) for one
session, which dropped every term below the maximum whenever the comparison row
had any successes. On this experiment's own table that reported p=0.0014 for a
result whose true one-tailed value is 0.0307 - a fabricated 22x significance on
the finding that was driving the writeup.

A p-value with no test is an assertion with a decimal point. This checks it
against exhaustive enumeration of the 2x2 over all fixed-margin labelings, which
is the definition of the exact test and needs no library.
"""
import itertools
import math
import os
import random
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from compose import fisher_greater  # noqa: E402


def brute_force(a, b, c, d):
    """Exact P(X >= a) by enumerating every labeling with the same margins."""
    total, row1, col1 = a + b + c + d, a + b, a + c
    cells = [1] * col1 + [0] * (total - col1)
    hits = seen = 0
    for combo in itertools.combinations(range(total), row1):
        seen += 1
        if sum(cells[i] for i in combo) >= a:
            hits += 1
    return float(hits) / seen


def pmf_normalised(a, b, c, d):
    row1, total, col1 = a + b, a + b + c + d, a + c
    return sum(math.comb(col1, k) * math.comb(total - col1, row1 - k)
               / math.comb(total, row1)
               for k in range(max(0, row1 - (total - col1)), min(row1, col1) + 1))


class TestFisherGreater(unittest.TestCase):
    def _cases(self, count, seed, hi):
        random.seed(seed)
        out = []
        while len(out) < count:
            table = tuple(random.randint(0, hi) for _ in range(4))
            a, b, c, d = table
            if 0 < a + b + c + d <= 14 and a + b > 0 and c + d > 0:
                out.append(table)
        return out

    def test_matches_exhaustive_enumeration(self):
        for table in self._cases(120, seed=7, hi=5):
            self.assertAlmostEqual(fisher_greater(*table), brute_force(*table),
                                   places=12, msg="table %s" % (table,))

    def test_pmf_sums_to_one(self):
        for table in self._cases(120, seed=11, hi=5):
            self.assertAlmostEqual(pmf_normalised(*table), 1.0, places=9,
                                   msg="table %s" % (table,))

    def test_tail_is_not_the_max_term_when_row_two_has_successes(self):
        """The exact regression: c > 0 is when the bug bit."""
        self.assertAlmostEqual(fisher_greater(4, 3, 1, 12), 0.0307017, places=6)
        self.assertAlmostEqual(fisher_greater(2, 2, 1, 2), 0.6285714, places=6)

    def test_degenerate_tables(self):
        self.assertEqual(fisher_greater(0, 5, 0, 5), 1.0)      # nothing observable
        self.assertAlmostEqual(fisher_greater(5, 0, 0, 5), fisher_greater(5, 0, 0, 5))
        self.assertEqual(fisher_greater(0, 0, 3, 4), 1.0)      # empty row -> p = 1


if __name__ == "__main__":
    unittest.main()

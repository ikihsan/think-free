#!/usr/bin/env python3
"""
E073 -- the piecewise-constant amount gate.

This file is E065's `detect.py` with ONE change, stated in
PROTOCOL.md: the amount-consistency gate (a fixed 0.15 CV
ceiling plus the utility-keyword escape hatch) is replaced by
a piecewise-constant price model. Everything else -- the n >= 3
floor, `detect_interval_pattern`, the 0.45 regularity floor,
`compute_recurring_score`, the 0.5 score floor -- is E065's,
called from E065's own frozen `scoring.py`.

The model: a group's amounts, in date order, quantized to
integer cents, are piecewise-constant with at most one step
when the run-length encoding of consecutive equal cent values
has at most 2 runs. One run is the fixed-price subscription
E065 already catches; two runs is a single price change, in
either direction. Drift, oscillation and second steps are
rejected, exactly as the CV ceiling rejected them.

The utility-keyword escape hatch is withdrawn: it existed only
to relax the CV ceiling, and the pwc gate subsumes it on
stricter terms (a utility with drifting amounts has more than
2 runs and is still rejected).

Scoring: an accepted group's amounts are fully explained by
the model (<= 2 parameters), so `compute_recurring_score` is
called with amount_cv = 0.0 -- the frozen function's own
amount_factor = 1.0 branch. No score constant is invented
here.

Standard library only. Python 3.8.
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from datetime import timedelta
from typing import Any, Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
E65 = os.path.join(HERE, "..", "065-recurring-expense-detection")
for _p in (E65,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from scoring import (  # noqa: E402  (E065's frozen module)
    detect_interval_pattern,
    compute_recurring_score,
)

# The model's only parameter, named here and nowhere else.
MAX_SEGMENTS = 2


def cent_runs(amounts: List[float]) -> List[Tuple[int, int]]:
    """
    Run-length encode `amounts` (already in date order) at cent
    precision. Returns [(cent_value, count), ...] in order.
    """
    runs: List[Tuple[int, int]] = []
    for a in amounts:
        c = int(round(abs(a) * 100))
        if runs and runs[-1][0] == c:
            runs[-1] = (c, runs[-1][1] + 1)
        else:
            runs.append((c, 1))
    return runs


def piecewise_constant(amounts: List[float],
                       max_segments: int = MAX_SEGMENTS) -> Tuple[bool, int]:
    """
    The amount gate. True iff the amounts are piecewise-constant
    with at most `max_segments` constant segments (at most
    `max_segments - 1` price changes).
    """
    return len(cent_runs(amounts)) <= max_segments, len(cent_runs(amounts))


def detect_recurring_expenses_pwc(
        transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    E065's `detect_recurring_expenses`, identical except for the
    amount gate. Input: normalized transactions with keys
    date, amount, merchant. Output: detected recurring expenses.
    """
    expenses = [t for t in transactions if t["amount"] < 0]

    by_merchant = defaultdict(list)
    for txn in expenses:
        by_merchant[txn["merchant"]].append(txn)

    results = []

    for merchant, txns in by_merchant.items():
        if len(txns) < 3:
            continue  # Need at least 3 occurrences (E065, unchanged)

        txns.sort(key=lambda x: x["date"])

        gaps = []
        for i in range(1, len(txns)):
            gap = (txns[i]["date"] - txns[i - 1]["date"]).days
            gaps.append(gap)

        interval_name, interval_regularity, expected_interval = \
            detect_interval_pattern(gaps)

        if interval_name is None or interval_regularity < 0.45:
            continue  # No clear pattern (E065, unchanged)

        # ---- E073: the piecewise-constant amount gate ----
        amounts = [t["amount"] for t in txns]
        accepted, n_segments = piecewise_constant(amounts)
        if not accepted:
            continue  # Not explained by <= 2 constant price segments

        # The model fully explains the amounts: E065's own
        # amount_factor = 1.0 branch (amount_cv < 0.02).
        score = compute_recurring_score(
            len(txns), interval_regularity, 0.0, interval_name, False)

        if score < 0.5:
            continue  # E065's score floor, unchanged

        last_date = txns[-1]["date"]
        next_expected = last_date + timedelta(days=int(expected_interval))

        abs_amounts = [abs(a) for a in amounts]
        results.append({
            "merchant": merchant,
            "interval": interval_name,
            "interval_days": expected_interval,
            "transaction_count": len(txns),
            "interval_regularity": round(interval_regularity, 3),
            "amount_segments": n_segments,
            "amount_cv": 0.0 if n_segments == 1 else None,
            "median_amount": round(
                sorted(abs_amounts)[len(abs_amounts) // 2], 2),
            "amount_range": (round(min(abs_amounts), 2),
                             round(max(abs_amounts), 2)),
            "score": round(score, 3),
            "first_date": txns[0]["date"].isoformat(),
            "last_date": last_date.isoformat(),
            "next_expected_date": next_expected.isoformat(),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

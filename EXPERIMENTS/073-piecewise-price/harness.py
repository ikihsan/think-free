#!/usr/bin/env python3
"""
E073 harness -- shared helpers for eval_arms.py.

Split out of eval_arms.py on 2026-10-09 at its 300-line cap. The rule is
unchanged: a split moves material to the file whose invariant it belongs in,
never shortens prose. This file holds the corpus loader, the arm runners,
and the census helpers; eval_arms.py holds main().

Standard library only. Python 3.8.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
E72 = os.path.join(HERE, "..", "072-merchant-noise-raw")
E65 = os.path.join(HERE, "..", "065-recurring-expense-detection")
for _p in (E72, E65, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from corpus import load_account                      # noqa: E402  (E072)
from arm_sign import convention, make_expenses       # noqa: E402  (E072)
from probe_undergroup import brand                  # noqa: E402  (E072)
import normalize                                    # noqa: E402  (E065's, as in E072)
import actual_find_schedules as actual              # noqa: E402  (E072's port)
import detect                                       # noqa: E402  (E065's frozen)
import detect_pwc                                   # noqa: E402  (this experiment)


def load_all():
    # E072's load_all(), byte-for-byte in behaviour: no mixed-side filter.
    # (An earlier version of this file filtered them, which broke G0.)
    corpus = json.load(open(os.path.join(E72, "raw/CORPUS.json")))
    accounts = []
    for e in corpus["accounts"]:
        acc = load_account(e)
        if not acc["rows"]:
            continue
        conv = convention(acc["rows"])
        accounts.append({
            "id": e["id"], "repo": e.get("repo"), "rows": acc["rows"],
            "conv": conv, "expenses": make_expenses(acc["rows"], conv["side"]),
        })
    return accounts


def group_key(row, arm):
    if arm in ("e065_raw", "e073_pwc_raw", "actual_raw"):
        return row["merchant"]
    return normalize.normalize_merchant(row["merchant"])


def run_e065(rows, arm):
    txns = [dict(r, merchant=group_key(r, arm)) for r in rows]
    return [d["merchant"] for d in detect.detect_recurring_expenses(txns)]


def run_pwc(rows, arm):
    txns = [dict(r, merchant=group_key(r, arm)) for r in rows]
    return [d["merchant"] for d in detect_pwc.detect_recurring_expenses_pwc(txns)]


def run_actual(rows, arm, today):
    txns = [{"date": r["date"], "amount": r["amount"], "payee": group_key(r, arm),
             "account": "acct"} for r in rows]
    return [s["payee"] for s in actual.find_schedules(txns, today=today)]


def run_naive(rows, arm):
    counts = defaultdict(int)
    for r in rows:
        if r["amount"] < 0:
            counts[group_key(r, arm)] += 1
    return [m for m, n in counts.items() if n >= 3]


def amount_runs(amounts):
    """Run-length encode amounts at cent precision, in date order."""
    runs = []
    for a in amounts:
        c = int(round(abs(a) * 100))
        if runs and runs[-1][0] == c:
            runs[-1] = (c, runs[-1][1] + 1)
        else:
            runs.append((c, 1))
    return runs


def describe_group(acc, merchant):
    """The pwc arm's own view of one (account, merchant-string) group.

    The detector sees `amount < 0` rows only (E065's expense side),
    so the census must too: a negative-side account's rows carry
    positive credits (payments, refunds) that the detector never
    sees, and a merchant string can appear on both sides.
    """
    txns = sorted([r for r in acc["expenses"] if r["merchant"] == merchant
                   and r["amount"] < 0],
                  key=lambda x: x["date"])
    amounts = [t["amount"] for t in txns]
    gaps = [(txns[i]["date"] - txns[i - 1]["date"]).days
            for i in range(1, len(txns))]
    interval_name, regularity, expected = detect.detect_interval_pattern(gaps)
    runs = amount_runs(amounts)
    return {
        "merchant": merchant,
        "n": len(txns),
        "interval": interval_name,
        "interval_regularity": round(regularity, 3) if regularity is not None else None,
        "segments": len(runs),
        "amount_runs": [[r[0] / 100.0, r[1]] for r in runs],
        "amount_range": (round(min(abs(a) for a in amounts), 2),
                         round(max(abs(a) for a in amounts), 2)),
        "first_date": txns[0]["date"].isoformat(),
        "last_date": txns[-1]["date"].isoformat(),
    }

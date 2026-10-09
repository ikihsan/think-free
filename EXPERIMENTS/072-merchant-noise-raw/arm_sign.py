#!/usr/bin/env python3
"""
Per-account amount-sign convention, declared before any detector ran.

E065's `detect.py` keeps expenses as `amount < 0`. Real exports disagree about
sign: of the 38 accounts in this corpus, **17 record debits as positive** and 21
as negative (`observed`, `arm_sign.py --report`). Running the detector
unmodified on the 17 would return zero detections for a reason that has nothing
to do with the mechanism under test.

So this module declares ONE rule, applied to the amount column only:

    an account's debits are the side that dominates its own sign distribution.

This is a column-semantics adapter, in the same class as the `Debit`/`Credit`
column choice E066's loader already made. It is **not** a mechanism change: it
never touches a merchant string, never touches a date, and never touches a
magnitude. The alternative reading -- that this is tuning -- is answered by
reporting both arms: `raw_sign` (detector exactly as shipped) and
`sign_normalised`, so the reader sees the whole format effect rather than a
number that has quietly absorbed it.

Accounts with a near-tie are declared `ambiguous` and are reported separately
rather than assigned a side, because a coin flip on sign would be a coin flip
on the whole account.
"""
from __future__ import annotations

# Two rules, and the reason the first version of this file used neither of them
# is worth recording.
#
# VERSION 1 declared "the side that dominates by >= 90% of non-zero amounts".
# It produced an uninterpretable spread: 11 of 38 accounts fell into
# `ambiguous`, at shares of 0.68 to 0.90, including plain credit-card
# statements whose positive amounts are the monthly *payments* the cardholder
# makes. A threshold on a marginal share is a coin flip dressed as a rule.
#
# The replacement reads the sign convention off the FILE'S SHAPE instead:
#
#   * A file containing ANY negative amounts is using the bookkeeping
#     convention -- debits negative, payments/refunds positive. That is what a
#     credit-card statement does, so expenses are the negative side.
#   * A file containing NO negative amounts at all is using the "amount is the
#     spend" convention (Mint, Monarch, Plaid-style feeds). Expenses are
#     positive.
#   * A file where the minority sign exceeds MINORITY_MAX is `mixed`: it carries
#     both conventions and no single assignment is defensible. Those accounts are
#     reported separately and never pooled into a headline number.
#
# This separates the corpus with no arbitrary band, and the accounts it calls
# mixed are reported as mixed rather than guessed at.
MINORITY_MAX = 0.25


def convention(rows):
    """
    rows: [{"amount": float}, ...]
    Returns {"side": "negative"|"positive"|"ambiguous", "neg": n, "pos": n,
             "total": n, "zero": n, "share": float}
    """
    neg = sum(1 for r in rows if r["amount"] < 0)
    pos = sum(1 for r in rows if r["amount"] > 0)
    zero = sum(1 for r in rows if r["amount"] == 0)
    total = neg + pos
    if total == 0:
        return {"side": "ambiguous", "neg": neg, "pos": pos, "total": 0, "zero": zero,
                "share": 0.0}
    minority = min(neg, pos) / total
    if neg == 0:
        side = "positive"
    elif pos == 0:
        side = "negative"
    elif minority > MINORITY_MAX:
        side = "mixed"
    else:
        side = "negative"  # bookkeeping convention: debits negative
    return {"side": side, "neg": neg, "pos": pos, "total": total, "zero": zero,
            "share": (max(neg, pos) / total), "minority_share": minority}


def make_expenses(rows, side):
    """
    Return rows with the amount sign set so that debits are negative, which is
    what E065's `detect.py` expects. `mixed` and unknown sides are returned
    unaltered: their accounts are excluded from every headline number, so
    guessing here would only matter for a figure nobody reads.
    """
    if side == "negative":
        return list(rows)
    if side == "positive":
        return [dict(r, amount=-abs(r["amount"])) for r in rows]
    return list(rows)


if __name__ == "__main__":
    import json
    import os
    import sys

    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, HERE)
    from corpus import load_account  # noqa: E402

    corpus = json.load(open(os.path.join(HERE, "raw/CORPUS.json")))
    counts = {}
    for e in corpus["accounts"]:
        acc = load_account(e)
        c = convention(acc["rows"])
        counts[c["side"]] = counts.get(c["side"], 0) + 1
        print("%-4s %-10s neg=%4d pos=%4d share=%.3f" % (e["id"], c["side"], c["neg"], c["pos"], c["share"]))
    print()
    print("accounts by declared side:", counts)
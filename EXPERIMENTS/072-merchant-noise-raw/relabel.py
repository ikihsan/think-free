#!/usr/bin/env python3
"""
Build the hand-verified watchlist, and freeze it.

The protocol requires labels that come from reading raw rows, not from any
detector's output. This script therefore does two things in this order:

  1. PRINT the candidate families -- (account, brand, n rows, first date, last
     date, interval statistics, median amount, sample raw strings) -- for a
     human to read.
  2. `--freeze` writes `watchlist.json` from a hand-written table that names
     each kept family and WHY.

No detector runs in this file. `eval_watchlist.py` and `eval_arms.py` read the
frozen watchlist; neither can write it.

Why a watchlist rather than hand-labelling all ~36,000 rows: the question E066
left open is whether a REAL recurring payment survives the merchant axis. That
is a question about positives. Negatives are supplied by the corpus itself --
every transaction that is not in the watchlist -- so precision is measured
against the account's real non-recurring traffic, which is the harder and more
useful negative population anyway.
"""
from __future__ import annotations

import json
import os
import re
import statistics
import sys
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from corpus import load_account      # noqa: E402
from arm_sign import convention, make_expenses   # noqa: E402
from probe_undergroup import brand    # noqa: E402

# Candidate generation: brands a person plausibly pays a recurring subscription
# or bill for. Chosen from the vocabulary of the corpus's own descriptors, by
# reading them (probe_undergroup.py section 2 prints them), not from an external
# list of "subscription companies" -- a list would import its own bias.
CANDIDATE_BRANDS = [
    "NETFLIX", "SPOTIFY", "HULU", "ADOBE", "APPLE", "GOOGLE", "DISNEY",
    "CHATGPT", "YOUTUBE", "PARAMOUNT", "PEACOCK", "SPECTRUM", "COMCAST",
    "VERIZON", "PROGRESSIVE", "STATE", "BRIGHTWHEEL", "VODAFONE", "TELEKOM",
    "WINDSTREAM", "SPOTIFY", "FITNESS", "GYM", "USMOBILE", "CHEWY", "PRIME",
    "SHOPIFY", "AMAZON", "WEBFLOW", "SQUARESPACE", "GODADDY", "DROPBOX",
    "PLANET", "EQUINOX", "LAFITNESS", "24HOUR", "MEMBER", "SUB", "PREMIUM",
]


def intervals(dates):
    ds = sorted(set(dates))
    gaps = [(ds[i] - ds[i - 1]).days for i in range(1, len(ds))]
    return gaps


def describe(account_id, brand_token, rows):
    dates = [r["date"] for r in rows]
    amounts = [abs(r["amount"]) for r in rows]
    gaps = intervals(dates)
    med_gap = statistics.median(gaps) if gaps else None
    cv = (statistics.pstdev(amounts) / statistics.mean(amounts)) if len(amounts) > 1 and statistics.mean(amounts) else None
    return {
        "account": account_id, "brand": brand_token, "n": len(rows),
        "first": str(min(dates)), "last": str(max(dates)),
        "span_days": (max(dates) - min(dates)).days,
        "median_gap": med_gap, "gap_values": sorted(gaps)[:14],
        "median_amount": round(statistics.median(amounts), 2) if amounts else None,
        "amount_cv": round(cv, 4) if cv is not None else None,
        "sample_raw": sorted({r["merchant"] for r in rows})[:6],
    }


def candidates(min_rows=4):
    corpus = json.load(open(os.path.join(HERE, "raw/CORPUS.json")))
    fams = defaultdict(list)
    for e in corpus["accounts"]:
        acc = load_account(e)
        side = convention(acc["rows"])["side"]
        for r in make_expenses(acc["rows"], side):
            b = brand(r["merchant"])
            if b in CANDIDATE_BRANDS:
                fams[(e["id"], b)].append(r)
    return [describe(a, b, rows) for (a, b), rows in sorted(fams.items()) if len(rows) >= min_rows]


def main():
    if "--freeze" in sys.argv:
        src = os.path.join(HERE, "watchlist_decisions.json")
        frozen = json.load(open(os.path.join(HERE, "watchlist.json"))) if os.path.exists(
            os.path.join(HERE, "watchlist.json")) else None
        if frozen:
            print("watchlist.json already exists; refusing to overwrite a frozen label set.")
            print("Delete it deliberately if you mean to relabel.")
            return 1
        json.dump(json.load(open(src)), open(os.path.join(HERE, "watchlist.json"), "w"), indent=1)
        print("frozen %d entries" % len(json.load(open(os.path.join(HERE, "watchlist.json")))["families"]))
        return 0

    cands = candidates()
    print("%d candidate families (>= 4 rows, expense side, brand in the declared list)\n" % len(cands))
    for c in cands:
        print("%-4s %-14s n=%3d %s..%s span=%4dd gap=%s amt=%s cv=%s"
              % (c["account"], c["brand"][:14], c["n"], c["first"], c["last"],
                 c["span_days"], c["median_gap"], c["median_amount"], c["amount_cv"]))
        for s in c["sample_raw"][:4]:
            print("        %s" % s[:88])
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
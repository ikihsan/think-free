#!/usr/bin/env python3
"""
Print, for hand reading, exactly what the arms got wrong in both directions.

Two lists, because the two error directions have different causes and the
experiment is about separating them:

  MISSED   watchlist families no arm found. Each is printed with every raw
           descriptor string that carries it and the normalized names they
           collapsed to, so the reader can see whether the loss happened in
           GROUPING (one merchant split into many names) or in SCORING (one
           group the interval+amount core rejected).

  SAMPLED  a stratified sample of the groups the arms reported that are NOT in
           the watchlist. These are `false positives` only if they are not
           recurring. The watchlist is small by construction -- it exists to
           answer a question about POSITIVES -- so most of these are almost
           certainly real recurring payments the watchlist never claimed, and
           reporting them as false positives would understate precision by an
           unknown and large amount. They are read and labelled by hand, and
           the hand labels are what precision is computed from.
"""
import json, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "065-recurring-expense-detection"))
from corpus import load_account            # noqa: E402
from arm_sign import convention, make_expenses  # noqa: E402
from probe_undergroup import brand         # noqa: E402
import normalize                            # noqa: E402
import detect                               # noqa: E402

SAMPLE_PER_STRATUM = 6


def families(accounts):
    out = defaultdict(list)
    for acc in accounts:
        for r in acc["expenses"]:
            out[(acc["id"], brand(r["merchant"]))].append(r)
    return out


def main():
    corpus = json.load(open(os.path.join(HERE, "raw/CORPUS.json")))
    watch = json.load(open(os.path.join(HERE, "watchlist.json")))
    wl = {(f["account"], f["brand"]): f for f in watch["families"]}

    accounts = []
    for e in corpus["accounts"]:
        acc = load_account(e)
        if not acc["rows"]:
            continue
        accounts.append({"id": e["id"], "expenses": make_expenses(acc["rows"],
                                                                 convention(acc["rows"])["side"])})
    fam = families(accounts)

    detected = {}
    for acc in accounts:
        txns = [dict(r, merchant=normalize.normalize_merchant(r["merchant"]))
                for r in acc["expenses"]]
        detected[acc["id"]] = {d["merchant"]: d for d in detect.detect_recurring_expenses(txns)}

    print("=" * 78)
    print("MISSED -- watchlist families E065 (normalized arm) did not report")
    print("=" * 78)
    for key, f in sorted(wl.items()):
        rows = fam.get(key, [])
        brands = {brand(m) for m in (normalize.normalize_merchant(r["merchant"]) for r in rows)}  # noqa: E501
        if brands & set(detected.get(key[0], {})):
            continue
        dates = sorted(r["date"] for r in rows)
        gaps = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
        raws = sorted({r["merchant"] for r in rows})
        norms = sorted({normalize.normalize_merchant(r["merchant"]) for r in rows})
        print()
        print("%-4s %-14s rows=%d span=%dd median_gap=%s" %
              (key[0], key[1], len(rows), (dates[-1] - dates[0]).days if dates else 0,
               statistics.median(gaps) if gaps else None))
        print("     distinct raw strings: %d -> distinct normalized names: %d"
              % (len(raws), len(norms)))
        for s in raws[:5]:
            print("       raw  %s" % s[:86])
        for s in norms[:5]:
            print("       norm %s" % s[:86])

    print()
    print("=" * 78)
    print("SAMPLED for hand reading -- groups E065 reported that the watchlist does not claim")
    print("=" * 78)
    buckets = defaultdict(list)
    for acc in accounts:
        for m, d in sorted(detected[acc["id"]].items()):
            if (acc["id"], brand(m)) in wl:
                continue
            buckets[d["interval"]].append((acc["id"], m, d))
    for interval in sorted(buckets):
        rows = buckets[interval]
        step = max(1, len(rows) // SAMPLE_PER_STRATUM)
        print()
        print("--- stratum: interval=%s  (%d groups; sampling %d)" %
              (interval, len(rows), min(len(rows), len(rows[::step][:SAMPLE_PER_STRATUM]))))
        for acc_id, m, d in rows[::step][:SAMPLE_PER_STRATUM]:
            print("  %-4s %-34s n=%2d cv=%s amt=%s  %s..%s" %
                  (acc_id, m[:34], d["transaction_count"], d["amount_cv"],
                   d["amount_range"], d["first_date"], d["last_date"]))


if __name__ == "__main__":
    main()
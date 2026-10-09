#!/usr/bin/env python3
"""
E072 -- run the three arms, score them, fire the gates.

Arms (predeclared in PROTOCOL.md):

  A  `e065_raw`        E065 detect.py, unmodified, on RAW descriptor strings
  B  `actual_raw`      Actual Budget findSchedules(), ported, on RAW strings
  C  `e065_normalized` E065 detect.py on E065's normalize_merchant() output
  D  `actual_shared`   Actual on the SAME normalized names as arm C
  E  `naive`           E065's own naive baseline: a merchant seen >= 3 times

Arms C and D share a merchant axis, so C-vs-D isolates the interval+amount
ENGINE. Arms A and B both see dirty strings, so A-vs-B asks who copes better
with what a bank actually sends -- and because Actual's production matcher runs
on a payee its importer has already cleaned, B is a LOWER BOUND on the
incumbent, never a fair fight. Arm C/D remove that handicap by substituting
E065's normalizer for Actual's import rules, which is a different handicap and
is labelled as one.

Labels come from `watchlist.json`, frozen by `relabel.py --freeze` before this
file ran, and this file cannot write it.

Every number below is a count over accounts, with the account as the sampling
unit and reported pooled AND per-account, because one person's spending can
carry a pooled rate and the gate G5 exists to catch exactly that.
"""
from __future__ import annotations

import json
import os
import random
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "065-recurring-expense-detection"))

from corpus import load_account                      # noqa: E402
from arm_sign import convention, make_expenses       # noqa: E402
from probe_undergroup import brand                   # noqa: E402
import normalize                                      # noqa: E402
import actual_find_schedules as actual               # noqa: E402

HERE_E = os.path.join(HERE, "..", "065-recurring-expense-detection")
sys.path.insert(0, HERE_E)
import detect                                          # noqa: E402

MIN_ROWS_FOR_POSITIVE = 3


def load_all():
    corpus = json.load(open(os.path.join(HERE, "raw/CORPUS.json")))
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
    if arm in ("e065_raw", "actual_raw"):
        return row["merchant"]
    return normalize.normalize_merchant(row["merchant"])


def run_e065(rows, arm):
    txns = [dict(r, merchant=group_key(r, arm)) for r in rows]
    return [d["merchant"] for d in detect.detect_recurring_expenses(txns)]


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


# ---------------------------------------------------------------------------
# Label mapping. A watchlist entry is a (account, brand) family. A detection is
# scored by which family its merchant string falls in, decided by BRAND, so a
# detector is judged on whether it FOUND the subscription, not on whether it
# produced the same string the hand-labeller wrote.
# ---------------------------------------------------------------------------

def brand_of(name):
    return brand(name)


def score(account_rows, watchlist_accounts, detected_keys):
    """
    detected_keys: set of brand tokens the arm reported for this account.
    positives: brands the watchlist labels as recurring in this account.
    """
    pos = watchlist_accounts
    tp = sorted(pos & detected_keys)
    fn = sorted(pos - detected_keys)
    fp = sorted(detected_keys - pos)
    return tp, fp, fn


def main():
    accounts = load_all()
    watch = json.load(open(os.path.join(HERE, "watchlist.json")))
    wl_by_account = defaultdict(set)
    for f in watch["families"]:
        wl_by_account[f["account"]].add(f["brand"])

    results = {"corpus": {"accounts": len(accounts),
                          "transactions": sum(len(a["rows"]) for a in accounts)},
               "watchlist": {"families": len(watch["families"]),
                             "distinct_merchants": len({f["merchant"] for f in watch["families"]}),
                             "excluded_families": len(watch["excluded_families"])},
               "arms": {}}

    arms = ["e065_raw", "actual_raw", "e065_normalized", "actual_shared", "naive"]
    per_account = {a: {} for a in arms}

    for acc in accounts:
        rows = acc["expenses"]
        today = max(r["date"] for r in rows)
        for arm in arms:
            if arm == "e065_raw":
                keys = {brand_of(k) for k in run_e065(rows, arm)}
            elif arm == "e065_normalized":
                keys = {brand_of(k) for k in run_e065(rows, arm)}
            elif arm == "actual_raw":
                keys = {brand_of(k) for k in run_actual(rows, arm, today)}
            elif arm == "actual_shared":
                keys = {brand_of(k) for k in run_actual(rows, arm, today)}
            else:
                keys = {brand_of(k) for k in run_naive(rows, arm)}
            tp, fp, fn = score(rows, wl_by_account.get(acc["id"], set()), keys)
            per_account[arm][acc["id"]] = {
                "detected_brands": len(keys), "tp": len(tp), "fp": len(fp), "fn": len(fn),
                "positives_available": len(wl_by_account.get(acc["id"], set())),
                "missed": fn[:10],
                "side": acc["conv"]["side"],
            }

    for arm in arms:
        tp = sum(v["tp"] for v in per_account[arm].values())
        fp = sum(v["fp"] for v in per_account[arm].values())
        fn = sum(v["fn"] for v in per_account[arm].values())
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * p * r / (p + r) if p + r else 0.0
        results["arms"][arm] = {
            "precision": round(p, 4), "recall": round(r, 4), "f1": round(f1, 4),
            "tp": tp, "fp": fp, "fn": fn,
            "detected_groups": sum(v["detected_brands"] for v in per_account[arm].values()),
            "accounts_with_positives": sum(1 for v in per_account[arm].values()
                                           if v["positives_available"] > 0),
        }

    results["per_account"] = per_account

    # ---- G3 permutation control, on the primary arm ----------------------
    rng = random.Random(20261009)
    for arm in ("e065_raw", "actual_raw"):
        base = results["arms"][arm]["tp"]
        survived = 0
        trials = 0
        for acc in accounts:
            pos = wl_by_account.get(acc["id"], set())
            if not pos:
                continue
            for _ in range(3):
                rows = [dict(r, date=r["date"]) for r in acc["expenses"]]
                dates = [r["date"] for r in rows]
                rng.shuffle(dates)
                for r, d in zip(rows, dates):
                    r["date"] = d
                if arm == "e065_raw":
                    keys = {brand_of(k) for k in run_e065(rows, arm)}
                else:
                    keys = {brand_of(k) for k in run_actual(rows, arm, max(r["date"] for r in rows))}
                survived += len(pos & keys)
                trials += len(pos)
        results["permutation_control"] = results.get("permutation_control", {})
        results["permutation_control"][arm] = {
            "baseline_tp": base, "trials_positives": trials, "survived": survived,
            "rate": round(survived / trials, 4) if trials else None,
        }

    # ---- G5 leave-one-out: drop the largest account ----------------------
    biggest = max(accounts, key=lambda a: len(a["rows"]))["id"]
    g5 = {}
    for arm in arms:
        tp = fp = fn = 0
        for k, v in per_account[arm].items():
            if k == biggest:
                continue
            tp += v["tp"]; fp += v["fp"]; fn += v["fn"]
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        g5[arm] = {"precision": round(p, 4), "recall": round(r, 4),
                   "f1": round(2 * p * r / (p + r) if p + r else 0.0, 4),
                   "tp": tp, "fp": fp, "fn": fn}
    results["leave_one_out"] = {"dropped": biggest, "arms": g5}

    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=1)

    # ---- report ----------------------------------------------------------
    print("corpus: %d accounts, %d transactions" % (results["corpus"]["accounts"],
                                                    results["corpus"]["transactions"]))
    print("watchlist: %d families, %d distinct merchants, %d families excluded as unresolved"
          % (results["watchlist"]["families"], results["watchlist"]["distinct_merchants"],
             results["watchlist"]["excluded_families"]))
    print()
    print("%-18s %8s %8s %8s %6s %6s %6s %8s" % ("arm", "prec", "rec", "F1", "TP", "FP", "FN", "groups"))
    for arm in arms:
        a = results["arms"][arm]
        print("%-18s %8.4f %8.4f %8.4f %6d %6d %6d %8d"
              % (arm, a["precision"], a["recall"], a["f1"], a["tp"], a["fp"], a["fn"],
                 a["detected_groups"]))
    print()
    for arm, v in results["permutation_control"].items():
        print("permutation control %-16s baseline TP=%d, %d/%d survive date-shuffling = %.4f"
              % (arm, v["baseline_tp"], v["survived"], v["trials_positives"], v["rate"]))
    print()
    print("leave-one-out (dropping %s, the largest account):" % biggest)
    for arm in arms:
        print("   %-18s F1 %.4f  (full: %.4f)" % (arm, g5[arm]["f1"], results["arms"][arm]["f1"]))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
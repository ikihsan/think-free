#!/usr/bin/env python3
"""
E073 -- run the pwc arms against E072's frozen corpus, score them,
and emit the census the hand-read gate P1b needs.

Arms (predeclared in PROTOCOL.md):

  `e065_raw`        frozen E065 detect.py, raw strings. G0 fidelity
                    arm: must reproduce E072's row exactly.
  `e073_pwc_raw`    the piecewise-constant gate on the SAME raw
                    strings -- the primary arm. The only difference
                    from `e065_raw` is the amount gate.
  `e073_pwc_norm`   the pwc gate on E065's normalized names -- the
                    axis E072 used to isolate the engine.
  `actual_raw`      the incumbent, re-run on the same rows.
  `naive`           E065's naive baseline (>= 3 debits to a merchant).

The corpus loader, the sign convention, the brand token, E065's
normalizer, the Actual port and E065's frozen detector are E072's
and E065's bytes, imported, never copied. Labels come from E072's
frozen `watchlist.json`, which this file cannot write.

Shared helpers (load_all, group_key, run_*, amount_runs,
describe_group) live in `harness.py`, split out at the 300-line cap.

Standard library only. Python 3.8.
"""
from __future__ import annotations

import json
import os
import random
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
E72 = os.path.join(HERE, "..", "072-merchant-noise-raw")
E65 = os.path.join(HERE, "..", "065-recurring-expense-detection")
for _p in (E72, E65, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from probe_undergroup import brand                  # noqa: E402  (E072)
import detect_pwc                                   # noqa: E402  (this experiment)
from harness import (                               # noqa: E402  (this experiment)
    load_all, run_e065, run_pwc, run_actual, run_naive, describe_group,
)


def main():
    accounts = load_all()
    watch = json.load(open(os.path.join(E72, "watchlist.json")))
    wl_by_account = defaultdict(set)
    for f in watch["families"]:
        wl_by_account[f["account"]].add(f["brand"])

    results = {"corpus": {"accounts": len(accounts),
                          "transactions": sum(len(a["rows"]) for a in accounts)},
               "watchlist": {"families": len(watch["families"]),
                             "distinct_merchants": len({f["merchant"] for f in watch["families"]}),
                             "excluded_families": len(watch["excluded_families"])},
               "arms": {}}

    arms = ["e065_raw", "e073_pwc_raw", "e073_pwc_norm", "actual_raw", "naive"]
    per_account = {a: {} for a in arms}

    # ---- per-account string-level detection, for the census ----------
    added_groups = []     # pwc accepts, e065 rejects (raw axis)
    dropped_groups = []   # e065 accepts, pwc rejects (raw axis)
    pwc_accepted = {"segments_1": 0, "segments_2": 0, "total": 0}

    for acc in accounts:
        rows = acc["expenses"]
        today = max(r["date"] for r in rows)
        strings = {}
        for arm in arms:
            if arm == "e065_raw":
                det = run_e065(rows, arm)
            elif arm == "e073_pwc_raw":
                det = run_pwc(rows, arm)
            elif arm == "e073_pwc_norm":
                det = run_pwc(rows, arm)
            elif arm == "actual_raw":
                det = run_actual(rows, arm, today)
            else:
                det = run_naive(rows, arm)
            strings[arm] = det
            keys = {brand(k) for k in det}
            pos = wl_by_account.get(acc["id"], set())
            tp, fp, fn = sorted(pos & keys), sorted(keys - pos), sorted(pos - keys)
            per_account[arm][acc["id"]] = {
                "detected_brands": len(keys), "tp": len(tp), "fp": len(fp),
                "fn": len(fn), "positives_available": len(pos),
                "missed": fn[:10], "side": acc["conv"]["side"],
            }

        # ---- census on the raw axis ------------------------------------
        e065_set = set(strings["e065_raw"])
        pwc_set = set(strings["e073_pwc_raw"])
        pos = wl_by_account.get(acc["id"], set())
        for m in sorted(pwc_set):
            g = describe_group(acc, m)
            pwc_accepted["total"] += 1
            key = "segments_%d" % g["segments"]
            pwc_accepted[key] = pwc_accepted.get(key, 0) + 1
            if m not in e065_set:
                added_groups.append(dict(
                    g, account=acc["id"],
                    watchlist_hit=brand(m) in pos,
                    watchlist_brand=brand(m) if brand(m) in pos else None))
        for m in sorted(e065_set - pwc_set):
            g = describe_group(acc, m)
            dropped_groups.append(dict(
                g, account=acc["id"],
                watchlist_hit=brand(m) in pos,
                watchlist_brand=brand(m) if brand(m) in pos else None))

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

    # ---- G3 permutation control, E072's procedure --------------------
    rng = random.Random(20261009)
    results["permutation_control"] = {}
    for arm in ("e065_raw", "e073_pwc_raw"):
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
                    keys = {brand(k) for k in run_e065(rows, arm)}
                else:
                    keys = {brand(k) for k in run_pwc(rows, arm)}
                survived += len(pos & keys)
                trials += len(pos)
        results["permutation_control"][arm] = {
            "baseline_tp": base, "trials_positives": trials, "survived": survived,
            "rate": round(survived / trials, 4) if trials else None,
        }

    # ---- G5 leave-one-out: drop the largest account ------------------
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

    # ---- census summaries --------------------------------------------
    results["census"] = {
        "pwc_accepted_groups": pwc_accepted,
        "single_segment_share": round(
            pwc_accepted.get("segments_1", 0) / pwc_accepted["total"], 4)
        if pwc_accepted["total"] else None,
        "added_groups": len(added_groups),
        "added_watchlist_hits": sum(1 for g in added_groups if g["watchlist_hit"]),
        "dropped_groups": len(dropped_groups),
        "dropped_watchlist_hits": sum(1 for g in dropped_groups if g["watchlist_hit"]),
    }

    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    json.dump(added_groups, open(os.path.join(HERE, "added_groups.json"), "w"), indent=1)
    json.dump(dropped_groups, open(os.path.join(HERE, "dropped_groups.json"), "w"), indent=1)

    # ---- report ------------------------------------------------------
    print("corpus: %d accounts, %d transactions"
          % (results["corpus"]["accounts"], results["corpus"]["transactions"]))
    print("watchlist: %d families, %d distinct merchants"
          % (results["watchlist"]["families"], results["watchlist"]["distinct_merchants"]))
    print()
    print("%-18s %8s %8s %8s %6s %6s %6s %8s"
          % ("arm", "prec", "rec", "F1", "TP", "FP", "FN", "groups"))
    for arm in arms:
        a = results["arms"][arm]
        print("%-18s %8.4f %8.4f %8.4f %6d %6d %6d %8d"
              % (arm, a["precision"], a["recall"], a["f1"], a["tp"], a["fp"],
                 a["fn"], a["detected_groups"]))
    print()
    for arm, v in results["permutation_control"].items():
        print("permutation control %-16s baseline TP=%d, %d/%d survive = %.4f"
              % (arm, v["baseline_tp"], v["survived"], v["trials_positives"], v["rate"]))
    print()
    print("leave-one-out (dropping %s, the largest account):" % biggest)
    for arm in arms:
        print("   %-18s P %.4f  R %.4f  F1 %.4f"
              % (arm, g5[arm]["precision"], g5[arm]["recall"], g5[arm]["f1"]))
    print()
    c = results["census"]
    print("pwc accepted %d groups: %d one-segment, %d two-segment "
          "(single-segment share %.4f)"
          % (c["pwc_accepted_groups"]["total"],
             c["pwc_accepted_groups"].get("segments_1", 0),
             c["pwc_accepted_groups"].get("segments_2", 0),
             c["single_segment_share"]))
    print("added groups (pwc accepts, e065 rejects): %d, of which watchlist hits: %d"
          % (c["added_groups"], c["added_watchlist_hits"]))
    print("dropped groups (e065 accepts, pwc rejects): %d, of which watchlist hits: %d"
          % (c["dropped_groups"], c["dropped_watchlist_hits"]))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

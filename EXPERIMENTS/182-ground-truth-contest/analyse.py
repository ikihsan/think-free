#!/usr/bin/env python3
"""E182 stage 2: compute the four ground-truth states and evaluate every gate.

Reads only files this experiment or E177 committed. Never reads an assistant
answer; joins E177's arm label and verdict afterwards, at the join step.

Usage: python3 analyse.py
"""
import hashlib
import json
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fisher_exact_2x2(a, b, c, d):
    """Two-sided Fisher exact for [[a,b],[c,d]]. Returns (p, oddsratio|None)."""
    n = a + b + c + d
    if n == 0:
        return (None, None)
    r1, r2, c1 = a + b, c + d, a + c

    def logc(x, y):
        return (math.lgamma(r1 + 1) - math.lgamma(x + 1) - math.lgamma(y + 1)
                + math.lgamma(c1 + 1) - math.lgamma(a + 1) - math.lgamma(b + 1)
                + math.lgamma(c + 1) + math.lgamma(d + 1))

    def row_total(x):
        return math.lgamma(x + 1) + math.lgamma(n - x + 1)

    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    obs = logc(a, b)
    tot = 0.0
    for x in range(lo, hi + 1):
        lp = obs - row_total(x) + row_total(a)
        tot += math.exp(lp)
    p = min(1.0, tot)
    orr = None
    if b * c:
        orr = (a * d) / float(b * c)
    return (p, orr)


def classify(n_answers, top, runner_up):
    """The four mutually exclusive, exhaustive states, per PROTOCOL.md section 2."""
    if n_answers <= 0:
        return "no_answers"
    if n_answers == 1:
        return "uncorroborated"
    if runner_up is None or runner_up <= 0:
        return "unopposed"
    if runner_up >= 0.5 * top:
        return "contested"
    return "decisive"


def main():
    rows = {r["qid"]: r for r in json.load(open(os.path.join(
        E177, "rows.json")))["rows"]}
    labels = {l["qid"]: l for l in json.load(open(os.path.join(
        E177, "labels.json")))["labels"]}
    verdicts = {}
    with open(os.path.join(E177, "score", "verdicts.jsonl")) as fh:
        for line in fh:
            line = line.strip()
            if line:
                v = json.loads(line)
                verdicts[v["pid"]] = v

    scores = json.load(open(os.path.join(HERE, "scores.json")))
    qids = sorted(int(k) for k in scores["rows"])

    table, g4_fail = [], []
    for q in qids:
        src = rows[q]
        got = scores["rows"][str(q)]
        by_score = sorted(got, key=lambda a: (-(a["score"] or 0),
                                              a["answer_id"] or 0))
        top = (by_score[0]["score"] if by_score else None)
        runner = (by_score[1]["score"] if len(by_score) > 1 else None)
        state = classify(len(by_score), top, runner)

        # G4: does the fresh fetch reproduce E177's committed shape?
        count_ok = (len(by_score) == src["answer_count"])
        score_ok = (top == src["key_score"])
        if not (count_ok and score_ok):
            g4_fail.append({"qid": q, "was_count": src["answer_count"],
                            "now_count": len(by_score),
                            "was_key_score": src["key_score"],
                            "now_top_score": top,
                            "count_ok": count_ok, "score_ok": score_ok})

        pid = "g-%d" % q
        arm = labels[q]["arm"]
        reached = verdicts[pid]["same_resolution"] == "YES"
        table.append({
            "qid": q, "arm": arm, "reached": reached,
            "n_answers": len(by_score), "top": top, "runner_up": runner,
            "state": state,
            "ratio": (round(runner / float(top), 4)
                      if (top and top > 0 and runner and runner > 0) else None),
            "accepted_ids": [a["answer_id"] for a in by_score
                             if a["is_accepted"]],
            "was_key_score": src["key_score"],
            "was_answer_count": src["answer_count"],
        })

    n = len(table)
    complete = sum(1 for r in table if r["n_answers"] > 0)

    def share(state, rows_):
        k = sum(1 for r in rows_ if r["state"] == state)
        m = len(rows_)
        lo, hi = wilson(k, m)
        return {"k": k, "n": m, "rate": (k / float(m) if m else None),
                "ci95": [lo, hi]}

    def cell(arm, reached):
        return [r for r in table if r["arm"] == arm and r["reached"] == reached]

    evid_miss, evid_hit = cell("EVID", False), cell("EVID", True)
    self_hit, self_miss = cell("SELF", True), cell("SELF", False)

    g1 = complete >= 55
    g4 = len(g4_fail) <= 3                      # >= 57 of 60 reproduce

    # G2 -- the decisive gate
    g2rows = []
    if evid_miss and evid_hit:
        a = sum(1 for r in evid_miss if r["state"] == "contested")
        b = sum(1 for r in evid_miss if r["state"] != "contested")
        c = sum(1 for r in evid_hit if r["state"] == "contested")
        d = sum(1 for r in evid_hit if r["state"] != "contested")
        p, orr = fisher_exact_2x2(a, b, c, d)
        diff = (a / float(len(evid_miss))) - (c / float(len(evid_hit)))
        g2rows = {"table": [[a, b], [c, d]], "fisher_p": p, "odds_ratio": orr,
                  "diff": round(diff, 4),
                  "fires": bool(p is not None and p < 0.05 and diff >= 0.20)}
    else:
        g2rows = {"table": None, "fisher_p": None, "diff": None,
                  "fires": False, "note": "no EVID pair to compare"}

    # G3 -- prevalence
    g3 = share("contested", table)
    g3_fires = g3["rate"] is not None and g3["rate"] >= 0.25

    # K1 -- the disagreement-framing kill
    k1 = share("uncorroborated", table)
    k1_fires = k1["rate"] is not None and k1["rate"] >= 0.50

    out = {
        "population": {"n": n, "complete_score_vectors": complete,
                       "population_sha256": scores["population_sha256"],
                       "quota_before": scores.get("quota_before"),
                       "quota_after": scores.get("quota_after")},
        "gates": {
            "G1_population_measured": {"fires_pass": g1,
                                       "need": 55, "got": complete},
            "G4_population_stable": {"fires_pass": g4, "reproduced": n - len(g4_fail),
                                     "need": 57, "got": n - len(g4_fail),
                                     "disagreements": g4_fail},
            "G2_differential": g2rows,
            "G3_prevalence": {"fires_pass": g3_fires, **g3, "bar": 0.25},
            "K1_kill_disagreement": {"fires": k1_fires, **k1, "bar": 0.50},
        },
        "states_overall": {s: share(s, table)
                           for s in ["contested", "decisive", "unopposed",
                                     "uncorroborated"]},
        "cells": {
            "EVID_missed": {"n": len(evid_miss), "contested": share("contested", evid_miss)},
            "EVID_hit": {"n": len(evid_hit), "contested": share("contested", evid_hit)},
            "SELF_hit": {"n": len(self_hit), "contested": share("contested", self_hit)},
            "SELF_missed": {"n": len(self_miss), "contested": share("contested", self_miss)},
        },
        "rows": table,
    }
    with open(os.path.join(HERE, "states.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")

    # ---- report ----
    print("population %d rows, %d complete score vectors" % (n, complete))
    print("G4 population stable: %s (%d of %d reproduced)"
          % ("PASS" if g4 else "FAIL", n - len(g4_fail), n))
    for r in g4_fail:
        print("   drift qid %d: answers %s->%s, key score %s->%s"
              % (r["qid"], r["was_count"], r["now_count"],
                 r["was_key_score"], r["now_top_score"]))
    print("G1 population measured: %s (%d >= 55)" % ("PASS" if g1 else "FAIL", complete))
    print()
    print("state            overall            EVID miss       EVID hit"
          "        SELF hit       SELF miss")
    for s in ["contested", "decisive", "unopposed", "uncorroborated"]:
        cells = [table, evid_miss, evid_hit, self_hit, self_miss]
        line = "%-15s" % s
        for c in cells:
            k = sum(1 for r in c if r["state"] == s)
            line += " %2d/%-2d=%5.3f  " % (k, len(c),
                                            (k / float(len(c)) if c else 0.0))
        print(line)
    print()
    print("G3 prevalence contested >= 0.25: %s (%d/%d = %.4f, Wilson [%.4f, %.4f])"
          % ("PASS" if g3_fires else "FAIL", g3["k"], g3["n"], g3["rate"],
             g3["ci95"][0], g3["ci95"][1]))
    print("K1 uncorroborated >= 0.50 -> kill: %s (%d/%d = %.4f)"
          % ("KILLED" if k1_fires else "not fired", k1["k"], k1["n"], k1["rate"]))
    print()
    if g2rows.get("fisher_p") is not None:
        print("G2 differential: EVID missed %d/%d contested vs EVID hit %d/%d"
              % (g2rows["table"][0][0], len(evid_miss),
                 g2rows["table"][1][0], len(evid_hit)))
        print("   diff %+0.4f, Fisher p %.6g, odds ratio %s -> %s"
              % (g2rows["diff"], g2rows["fisher_p"],
                 ("%.4f" % g2rows["odds_ratio"]) if g2rows["odds_ratio"] else "n/a",
                 "FIRES" if g2rows["fires"] else "does not fire"))
    print()
    print("rows digest %s"
          % hashlib.sha256(json.dumps(
              [(r["qid"], r["state"]) for r in table]).encode()).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
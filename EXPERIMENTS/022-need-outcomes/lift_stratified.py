#!/usr/bin/env python3
"""E022: the depth-stratified lift.

This is the arm the verdict rests on. `lift.py` compared 1401 need comments
against 13409 non-trigger siblings pooled and got 0.81x, but **that comparison is
confounded**: the control was built by reading each story's top-level kid list,
so it contains only depth-0 comments, while 471 of the 1401 need comments sit at
depth 1 or 2. Depth changes the reply rate on its own -- 0.672 at depth 0 against
0.544 at depth 1 in the 12-story pilot -- so the pooled number is partly a
measurement of where a comment sits in a thread.

This module stratifies. For each depth stratum it reports the need rate, the
control rate, the ratio, and the row counts, and it reports a Mantel-Haenszel
summary of the common odds ratio so the strata can be pooled without letting the
biggest stratum decide the answer.

**Two strata carry the arm and thirteen carry the need arm alone.** The control
was collected at depths 0 and 1 only, so the MH summary is computed over the two
strata where both arms exist. That is a real ceiling and not a formality: 434 of
the 1401 need comments sit at depth 2 or below with no depth-matched control at
all, so the deep tail of the population is *unmeasured* rather than measured at
zero. The first version of this file reported "471 of 1401 at depth 1 or 2",
which was true of a capture in which 434 rows were still `null` -- the deep tail
was missing and therefore invisible. `need_depth_walk.py` was repaired (F042) and
the population is now complete; the control arm has not been extended to match,
and the odds ratio below is unchanged by the repair because the two strata it
uses were never affected.

Unresolved depths stay in their own stratum. Dropping them would quietly
reweight the population toward shallow comments, which is the stratum with the
highest reply rate.
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
CONTROL = os.path.join(HERE, "raw", "control_depth.jsonl")
NEED_DEPTH = os.path.join(HERE, "raw", "need_depth.jsonl")


def ci(k, n, z=1.96):
    """Wilson interval. The normal approximation misbehaves at small cell counts."""
    if not n:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def mantel_haenszel(strata):
    """Common odds ratio across strata: sum(R) / sum(S), MH estimator.

    Returns (or_, lo, hi). A stratum with a zero cell contributes to the variance
    correction only, which is the standard continuity adjustment.
    """
    num = den = 0.0
    p_sum = q_sum = r_sum = s_sum = 0.0
    for a, b, c, d in strata:      # a=need&answered b=need&not c=ctrl&ans d=ctrl&not
        n = a + b + c + d
        if n == 0:
            continue
        r = a * d / float(n)
        s = b * c / float(n)
        num += r
        den += s
        p_sum += (a + d) * b * c / (n * n) if n > 1 else 0.0
        q_sum += (a * d - b * c) / float(n)
        r_sum += a * d / float(n)
        s_sum += b * c / float(n)
    if den == 0 or num == 0:
        return (None, None, None)
    or_ = num / den
    # Robins-Breslow-Greenland variance.
    P, Q = p_sum, q_sum
    R, S = r_sum, s_sum
    if R + S == 0:
        return (or_, None, None)
    var = ((P - 0.5 * Q) / R) ** 2 + ((P + 0.5 * Q) / S) ** 2
    se = math.sqrt(var) if var > 0 else None
    if not se:
        return (or_, None, None)
    return (or_, math.exp(math.log(or_) - 1.96 * se), math.exp(math.log(or_) + 1.96 * se))


A2_KILL = 1.0     # the declared floor, from PROTOCOL.md, before the first fetch


def decide(or_):
    """Gate A2, read from the odds ratio alone.

    PROTOCOL.md declared this before any outcome was observed: if the
    within-thread lift is not greater than 1.0 the trigger vocabulary carries no
    information about being answered, and the experiment reports `not
    informative`. That is a real possible result and not a failure of the run,
    which is why the decision is a function with one argument rather than a
    branch inside the printing code.
    """
    if or_ is None:
        return {"verdict": "not_evaluable", "odds_ratio": None,
                "declared_floor": A2_KILL,
                "reason": "no stratum carries both arms"}
    return {"verdict": "fires" if or_ <= A2_KILL else "survives",
            "odds_ratio": round(or_, 4),
            "declared_floor": A2_KILL,
            "meaning": ("need comments are not more likely to be answered than "
                        "non-need comments at the same depth, so a trigger "
                        "phrase does not mark a comment the thread answers")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    outcome = {str(json.loads(l)["comment_id"]): json.loads(l)
               for l in open(OUTCOMES)}
    ndepth = {str(json.loads(l)["comment_id"]): json.loads(l)
              for l in open(NEED_DEPTH)}
    ctrl = [json.loads(l) for l in open(CONTROL)]

    need_by_depth = defaultdict(list)
    for cid, rec in ndepth.items():
        if rec.get("answered") is None:
            continue
        d = rec.get("depth")
        need_by_depth["unresolved" if d is None else d].append(cid)

    ctrl_by_depth = defaultdict(list)
    for rec in ctrl:
        if rec.get("answered") is None:
            continue
        ctrl_by_depth[rec.get("depth")].append(rec)

    strata = []
    rows = []
    for d in sorted(set(need_by_depth) | set(ctrl_by_depth),
                    key=lambda x: (x == "unresolved", x if x != "unresolved" else 0)):
        nids = need_by_depth.get(d, [])
        crecs = ctrl_by_depth.get(d, [])
        nk = sum(1 for c in nids if outcome[c]["answered"])
        ck = sum(1 for c in crecs if c["answered"])
        pn = len(nids)
        qn = len(crecs)
        nr = nk / float(pn) if pn else None
        cr = ck / float(qn) if qn else None
        ratio = (nr / cr) if (nr is not None and cr) else None
        rows.append({
            "depth": "unresolved" if d == "unresolved" else d,
            "need_answered": nk, "need_n": pn, "need_rate": nr,
            "need_ci95": ci(nk, pn),
            "control_answered": ck, "control_n": qn, "control_rate": cr,
            "control_ci95": ci(ck, qn),
            "lift": ratio,
        })
        if pn and qn:
            strata.append((nk, pn - nk, ck, qn - ck))

    or_, lo, hi = mantel_haenszel(strata)
    gate = decide(or_)
    deep_unmatched = sum(r["need_n"] for r in rows
                         if r["depth"] not in (0, 1, "unresolved"))

    out = {
        "schema": "origin.need-outcome-lift-stratified/1",
        "strata": rows,
        "mantel_haenszel_or": or_,
        "mantel_haenszel_ci95": [lo, hi],
        "strata_counted": len(strata),
        "gate_a2": gate,
        "need_rows_without_a_depth_matched_control": deep_unmatched,
        "ceiling": ("The control arm holds depths 0 and 1 only, so %d need "
                    "comments at depth 2 or below have no matched control. The "
                    "odds ratio is computed over the %d strata where both arms "
                    "exist and says nothing about the deep tail."
                    % (deep_unmatched, len(strata))),
        "note": ("Depth stratified because the pooled control was top-level only. "
                 "'unresolved' holds need comments whose ancestor chain could not "
                 "be read; they are not folded into depth 0. After F042's repair "
                 "that stratum is empty."),
    }

    if args.json:
        print(json.dumps(out, indent=1, sort_keys=True))
        return 0

    print("%-10s %-16s %-16s %8s" % ("depth", "need", "control", "lift"))
    for r in rows:
        n = ("%d/%d=%.3f" % (r["need_answered"], r["need_n"], r["need_rate"])) \
            if r["need_n"] else "-"
        c = ("%d/%d=%.3f" % (r["control_answered"], r["control_n"], r["control_rate"])) \
            if r["control_n"] else "-"
        print("%-10s %-16s %-16s %8s"
              % (r["depth"], n, c, ("%.3fx" % r["lift"]) if r["lift"] else "-"))
    print()
    if or_ is None:
        print("MH odds ratio      not computable")
    else:
        print("MH common odds ratio %.3f  CI95 [%.3f, %.3f]  over %d strata"
              % (or_, lo, hi, len(strata)))
        print("  (>1 means need comments are more likely to be answered)")
    print()
    print("gate A2 (declared floor %.1f)  %s" % (A2_KILL, gate["verdict"]))
    print("  %s" % gate.get("meaning", gate.get("reason", "")))
    if deep_unmatched:
        print("ceiling: %d need comments at depth >=2 have no depth-matched "
              "control, so the deep tail is unmeasured" % deep_unmatched)
    return 0


if __name__ == "__main__":
    sys.exit(main())

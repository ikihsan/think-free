#!/usr/bin/env python3
"""E022: the within-thread lift, and the gate A2 verdict.

Gate A2 was declared in PROTOCOL.md before the first fetch: if the reply rate of
comments carrying a need trigger is not **greater** than the reply rate of
non-trigger comments in the same threads, the trigger vocabulary carries no
information about being answered and the arm reports `not informative`.

The comparison is *paired within thread* because the obvious rival explanation is
thread busyness, and a thread that gets no replies would depress both arms
alike. So this reports three things, in increasing strength:

  1. the pooled rates and their ratio,
  2. the same comparison restricted to threads that contain BOTH kinds, which is
     the only place the two arms are comparable at all,
  3. a per-thread sign test: threads where needs were answered and controls were
     not, against the reverse.
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
CONTROL = os.path.join(HERE, "raw", "control.jsonl")


def wilson(k, n, z=1.96):
    """Wilson interval. Normal approximation is wrong at these counts per cell."""
    if not n:
        return (0.0, 0.0)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    need = [json.loads(l) for l in open(OUTCOMES)]
    ctrl = [json.loads(l) for l in open(CONTROL)]

    need_ok = [r for r in need if r["answered"] is not None]
    ctrl_ok = [r for r in ctrl if r["answered"] is not None]
    need_unreadable = len(need) - len(need_ok)
    ctrl_unreadable = len(ctrl) - len(ctrl_ok)

    nk = sum(1 for r in need_ok if r["answered"])
    ck = sum(1 for r in ctrl_ok if r["answered"])
    pooled_lift = (nk / float(len(need_ok))) / (ck / float(len(ctrl_ok)))

    # Paired: only threads holding both kinds are comparable.
    need_by_story = defaultdict(list)
    ctrl_by_story = defaultdict(list)
    for r in need_ok:
        need_by_story[r["story_id"]].append(r)
    for r in ctrl_ok:
        ctrl_by_story[r["story_id"]].append(r)
    both = sorted(set(need_by_story) & set(ctrl_by_story))

    pk = sum(1 for s in both for r in need_by_story[s] if r["answered"])
    pn = sum(len(need_by_story[s]) for s in both)
    qk = sum(1 for s in both for r in ctrl_by_story[s] if r["answered"])
    qn = sum(len(ctrl_by_story[s]) for s in both)
    paired_lift = (pk / float(pn)) / (qk / float(qn)) if pn and qk else None

    # Sign test over threads holding both kinds and a mixed outcome.
    a = b = 0
    for s in both:
        na = sum(1 for r in need_by_story[s] if r["answered"])
        ca = sum(1 for r in ctrl_by_story[s] if r["answered"])
        if na > ca:
            a += 1
        elif ca > na:
            b += 1
    n_ab = a + b
    # Two-sided exact binomial p under H0: p=0.5.
    if n_ab:
        k = min(a, b)
        # Exact integer arithmetic, then a shifted division. `2 ** n` overflows
        # a float past n=1024 and this arm runs over ~1200 threads, so both
        # operands are scaled by a common power of two before conversion. The
        # ratio is unchanged and the shift keeps them inside float range.
        num = sum(math.comb(n_ab, i) for i in range(0, k + 1))
        den = 2 ** n_ab
        if num == 0:
            p_two = 0.0
        else:
            shift = max(0, den.bit_length() - 900)
            ratio = float(num >> shift) / float(den >> shift)
            p_two = min(1.0, 2.0 * ratio)
    else:
        p_two = None

    lift = paired_lift if paired_lift is not None else pooled_lift
    gate_a2 = "met" if (lift is not None and lift > 1.0) else "NOT met"
    verdict = ("informative" if gate_a2 == "met"
               else "not informative")

    out = {
        "schema": "origin.need-outcome-lift/1",
        "population": {
            "need_comments": len(need),
            "need_readable": len(need_ok),
            "need_unreadable": need_unreadable,
            "control_comments": len(ctrl),
            "control_readable": len(ctrl_ok),
            "control_unreadable": ctrl_unreadable,
            "stories_in_need_arm": len(need_by_story),
            "stories_with_both_arms": len(both),
        },
        "pooled": {
            "need_answered": nk,
            "need_rate": nk / float(len(need_ok)) if need_ok else None,
            "need_ci95": wilson(nk, len(need_ok)),
            "control_answered": ck,
            "control_rate": ck / float(len(ctrl_ok)) if ctrl_ok else None,
            "control_ci95": wilson(ck, len(ctrl_ok)),
            "lift": pooled_lift,
        },
        "paired_within_thread": {
            "need_answered": pk, "need_n": pn,
            "control_answered": qk, "control_n": qn,
            "need_rate": pk / float(pn) if pn else None,
            "control_rate": qk / float(qn) if qn else None,
            "lift": paired_lift,
        },
        "sign_test": {
            "threads_needs_higher": a,
            "threads_controls_higher": b,
            "threads_tied": len(both) - n_ab,
            "p_two_sided": p_two,
        },
        "gate_a2": gate_a2,
        "verdict": verdict,
    }

    if args.json:
        print(json.dumps(out, indent=1, sort_keys=True))
        return 0

    p = out["population"]
    print("population")
    print("  need comments      %d readable, %d unreadable"
          % (p["need_readable"], p["need_unreadable"]))
    print("  control comments   %d readable, %d unreadable"
          % (p["control_readable"], p["control_unreadable"]))
    print("  stories            %d with needs, %d with BOTH arms"
          % (p["stories_in_need_arm"], p["stories_with_both_arms"]))
    po = out["pooled"]
    print("pooled")
    print("  need answered      %d/%d  %.3f  CI95 [%.3f, %.3f]"
          % (po["need_answered"], p["need_readable"], po["need_rate"],
             po["need_ci95"][0], po["need_ci95"][1]))
    print("  control answered   %d/%d  %.3f  CI95 [%.3f, %.3f]"
          % (po["control_answered"], p["control_readable"], po["control_rate"],
             po["control_ci95"][0], po["control_ci95"][1]))
    print("  lift               %.3fx" % po["lift"])
    q = out["paired_within_thread"]
    print("paired within thread")
    print("  need answered      %d/%d  %.3f" % (q["need_answered"], q["need_n"], q["need_rate"]))
    print("  control answered   %d/%d  %.3f" % (q["control_answered"], q["control_n"], q["control_rate"]))
    print("  lift               %.3fx" % q["lift"])
    s = out["sign_test"]
    print("sign test")
    print("  needs higher %d, controls higher %d, tied %d, p=%.3g"
          % (s["threads_needs_higher"], s["threads_controls_higher"],
             s["threads_tied"], s["p_two_sided"]))
    print("gate A2 (>1.0 lift)  %s" % out["gate_a2"])
    print("verdict               %s" % out["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

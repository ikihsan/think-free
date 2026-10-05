#!/usr/bin/env python3
"""E022: is the need-vs-control reply difference explained by comment length?

The depth-stratified lift came out at 0.69x. That would say a comment stating a
need attracts *fewer* replies than its neighbours -- a real finding about how the
world responds. But one rival explains it without any claim about needs at all:

    **length predicts replies.** In the control arm, answered comments average
    446 characters and unanswered ones 329. The need arm's median is 310.

So this stratifies by length *band* as well as depth, and reports the lift inside
each band. If the lift collapses toward 1.0 within a band, the pooled number was
measuring how short the sentences were. If it survives, length is not the
explanation and the negative lift is real.

Bands are quartiles of the pooled population, so both arms are cut at the same
places and no cell is defined by its own distribution.
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def ci(k, n, z=1.96):
    if not n:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - m) / d, 4), round((c + m) / d, 4))


def load(name):
    p = os.path.join(RAW, name)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    outcome = {str(json.loads(l)["comment_id"]): json.loads(l)
               for l in open(os.path.join(RAW, "outcomes.jsonl"))}
    need_len = {str(json.loads(l)["comment_id"]): json.loads(l)
                for l in open(os.path.join(RAW, "need_len.jsonl"))}
    need_depth = {str(json.loads(l)["comment_id"]): json.loads(l)
                  for l in open(os.path.join(RAW, "need_depth.jsonl"))}
    ctrl = load("control_depth.jsonl")
    if ctrl is None:
        print("no depth-matched control capture")
        return 1

    # Pooled quartiles of length across BOTH arms.
    all_len = ([need_len[c]["len"] for c in need_len if need_len[c].get("len") is not None]
               + [r["len"] for r in ctrl if r.get("len") is not None])
    all_len.sort()
    q = [all_len[int(len(all_len) * f)] for f in (0.25, 0.5, 0.75)]
    print("length quartile cuts (pooled): %s  n=%d" % (q, len(all_len)))

    def band(v):
        if v is None:
            return "unknown"
        if v <= q[0]:
            return "Q1 <=%d" % q[0]
        if v <= q[1]:
            return "Q2 %d-%d" % (q[0], q[1])
        if v <= q[2]:
            return "Q3 %d-%d" % (q[1], q[2])
        return "Q4 >%d" % q[2]

    need_by = defaultdict(list)
    for cid in outcome:
        if outcome[cid]["answered"] is None:
            continue
        d = need_depth.get(cid, {}).get("depth")
        need_by[(band(need_len.get(cid, {}).get("len")),
                 "unresolved" if d is None else d)].append(cid)
    ctrl_by = defaultdict(list)
    for r in ctrl:
        if r.get("answered") is None:
            continue
        ctrl_by[(band(r.get("len")), r.get("depth"))].append(r)

    rows = []
    print()
    print("%-14s %-6s %-16s %-16s %8s"
          % ("len band", "depth", "need", "control", "lift"))
    for key in sorted(set(need_by) | set(ctrl_by),
                      key=lambda k: (k[0], k[1] if k[1] != "unresolved" else 99)):
        b, d = key
        nids = need_by.get(key, [])
        crecs = ctrl_by.get(key, [])
        nk = sum(1 for c in nids if outcome[c]["answered"])
        ck = sum(1 for r in crecs if r["answered"])
        pn, qn = len(nids), len(crecs)
        nr = nk / float(pn) if pn else None
        cr = ck / float(qn) if qn else None
        lift = (nr / cr) if (nr is not None and cr) else None
        print("%-14s %-6s %-16s %-16s %8s"
              % (b, d,
                 ("%d/%d=%.3f" % (nk, pn, nr)) if pn else "-",
                 ("%d/%d=%.3f" % (ck, qn, cr)) if qn else "-",
                 ("%.3fx" % lift) if lift else "-"))
        rows.append({"len_band": b, "depth": str(d), "need_n": pn, "need_answered": nk,
                     "control_n": qn, "control_answered": ck,
                     "need_rate": nr, "control_rate": cr, "lift": lift,
                     "need_ci95": ci(nk, pn), "control_ci95": ci(ck, qn)})

    # Pooled within length band, ignoring depth, to state one number per band.
    print()
    print("pooled within length band (depth ignored):")
    agg = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        a = agg[r["len_band"]]
        a[0] += r["need_answered"]; a[1] += r["need_n"]
        a[2] += r["control_answered"]; a[3] += r["control_n"]
    band_rows = []
    for b in sorted(agg):
        nk, pn, ck, qn = agg[b]
        nr = nk / float(pn) if pn else None
        cr = ck / float(qn) if qn else None
        lift = (nr / cr) if (nr is not None and cr) else None
        print("  %-14s need %d/%d=%.3f  control %d/%d=%.3f  lift %s"
              % (b, nk, pn, nr or 0, ck, qn, cr or 0,
                 ("%.3fx" % lift) if lift else "-"))
        band_rows.append({"len_band": b, "need_answered": nk, "need_n": pn,
                          "control_answered": ck, "control_n": qn,
                          "lift": lift})

    out = {"schema": "origin.need-length-adjusted-lift/1",
           "quartile_cuts": q, "cells": rows, "pooled_by_band": band_rows}
    path = os.path.join(HERE, "length_adjusted.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

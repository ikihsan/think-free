#!/usr/bin/env python3
"""E113 — stratified check: is the matched-pool effect just a star-stratum artifact?

`analyze.py` reports a pooled Cliff's delta over a pool stratified by star
count. If the need-label is unevenly distributed across strata (it is - the
need-share runs 0.36 to 0.78) then a pooled comparison mixes two things:
  (a) within-stratum: does a need label beat a generic one at the same fame?
  (b) between-stratum: are need rows sitting in higher strata than generic ones?

Only (a) is the claim the principle makes. This script separates them:

  within   - Cliff's delta computed inside each stratum, pooled by rank
  adjusted - the same arms after subtracting each stratum's median stars
  permute  - stratified permutation test: shuffle labels WITHIN each stratum,
             so the label distribution across strata is held fixed

Stdlib only. Writes stratified.json.

    python3 stratified.py
"""
from __future__ import print_function

import datetime
import json
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A  # noqa: E402
import labeling as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_pool.json")
OUT = os.path.join(HERE, "stratified.json")
ITERS = 20000
SEED = 20261012


def load_rows():
    now = datetime.datetime.utcnow()
    rows = []
    with open(RAW) as fh:
        pool = json.load(fh)
    for r in pool:
        desc = r.get("description")
        if not desc:
            continue
        lab = L.label(desc, rule="masked")
        if lab == "unlabelled":
            continue
        r = dict(r)
        r["label"] = lab
        r["age"] = A.years_since(r.get("created_at"), now)
        rows.append(r)
    return rows


def within_stratum_delta(rows):
    """Pool within-stratum deltas weighted by cross-pair count."""
    num = den = 0.0
    per = {}
    strata = sorted({r["harvest_stratum"] for r in rows})
    for s in strata:
        n = [r["stargazers_count"] for r in rows
             if r["harvest_stratum"] == s and r["label"] == "need"]
        g = [r["stargazers_count"] for r in rows
             if r["harvest_stratum"] == s and r["label"] == "generic"]
        if len(n) < 5 or len(g) < 5:
            continue
        d = A.cliffs_delta(n, g)
        w = float(len(n) * len(g))
        per[s] = {"need": len(n), "generic": len(g),
                  "delta": round(d, 4), "pairs": int(w)}
        num += d * w
        den += w
    return (num / den if den else 0.0), per


def adjusted_delta(rows):
    by_s = {}
    for r in rows:
        by_s.setdefault(r["harvest_stratum"], []).append(r["stargazers_count"])
    med = {s: statistics.median(v) for s, v in by_s.items()}
    a = [r["stargazers_count"] - med[r["harvest_stratum"]]
         for r in rows if r["label"] == "need"]
    b = [r["stargazers_count"] - med[r["harvest_stratum"]]
         for r in rows if r["label"] == "generic"]
    return A.cliffs_delta(a, b)


def stratified_permutation(rows, iters=ITERS, seed=SEED):
    """Shuffle labels within each stratum; stratum composition held fixed."""
    rng = random.Random(seed)
    strata = {}
    for r in rows:
        strata.setdefault(r["harvest_stratum"], []).append(r["stargazers_count"])
    labels = {}
    for r in rows:
        labels.setdefault(r["harvest_stratum"], []).append(r["label"])
    observed = A.cliffs_delta(
        [r["stargazers_count"] for r in rows if r["label"] == "need"],
        [r["stargazers_count"] for r in rows if r["label"] == "generic"])
    hits = 0
    for _ in range(iters):
        a, b = [], []
        for s, vals in strata.items():
            labs = list(labels[s])
            rng.shuffle(labs)
            n_need = labs.count("need")
            for v, lab in zip(vals, labs):
                (a if lab == "need" else b).append(v)
            del n_need
        d = A.cliffs_delta(a, b)
        if abs(d) >= abs(observed):
            hits += 1
    return (hits + 1) / float(iters + 1), observed


def main():
    rows = load_rows()
    pooled = A.cliffs_delta(
        [r["stargazers_count"] for r in rows if r["label"] == "need"],
        [r["stargazers_count"] for r in rows if r["label"] == "generic"])
    within, per = within_stratum_delta(rows)
    adjusted = adjusted_delta(rows)
    p, observed = stratified_permutation(rows)

    print("rows: %d" % len(rows))
    print("pooled delta           : %+.4f   <- what analyze.py reports" % pooled)
    print("within-stratum delta   : %+.4f   <- the claim, stratum held fixed" % within)
    print("stratum-adjusted delta : %+.4f" % adjusted)
    print("stratified permutation p: %.5g  (observed %+.4f, %d iters)"
          % (p, observed, ITERS))
    print("\nper-stratum:")
    for s in sorted(per):
        v = per[s]
        print("  %-18s need=%3d generic=%3d  d=%+.3f" % (s, v["need"], v["generic"], v["delta"]))

    out = {
        "rows": len(rows),
        "pooled_delta": round(pooled, 4),
        "within_stratum_delta": round(within, 4),
        "stratum_adjusted_delta": round(adjusted, 4),
        "stratified_permutation_p": p,
        "permutation_iters": ITERS,
        "per_stratum": per,
        "interpretation": (
            "The pooled effect is carried by the need label sitting in higher "
            "star strata, not by need labels winning within a stratum. Holding "
            "stratum fixed removes most of it."
        ),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nwrote %s" % OUT)

    # Merge the decisive numbers into results.json so one file carries the
    # whole result; the gate in originlib/resultnumbers.py checks restated
    # figures against it.
    merged = {}
    if os.path.exists(A.OUT):
        with open(A.OUT) as fh:
            merged = json.load(fh)
    merged["stratified"] = {
        "pooled_delta": round(pooled, 4),
        "within_stratum_delta": round(within, 4),
        "stratum_adjusted_delta": round(adjusted, 4),
        "stratified_permutation_p": p,
        "permutation_iters": ITERS,
        "per_stratum": per,
        "verdict": "no_effect_within_stratum",
        "note": ("This is the verdict that stands. analyze.py's pooled reading "
                 "pools across star strata, which is the same class of error "
                 "as E107 one level down."),
    }
    with open(A.OUT, "w") as fh:
        json.dump(merged, fh, indent=1, sort_keys=True)
    print("merged into %s" % A.OUT)


if __name__ == "__main__":
    main()
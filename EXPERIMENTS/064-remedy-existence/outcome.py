#!/usr/bin/env python3
"""Recompute every E064-A1 number from the committed raw bytes.

The recorded values are constants in this file; the function exits 1
if the recomputed value disagrees with any of them, so a change in the
raw data is a failing run, not a silent diff.

    python3 outcome.py
"""
from __future__ import print_function

import datetime
import glob
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# --- recorded values (what README.md reports) -------------------
REC_G1_SEEDS = (37, 37, 5)      # seeds resolving, seeds total, ecosystems
REC_G1_MUTATIONS = 576
REC_G5_K, REC_G5_N = 93, 576
REC_G6_RECALL = (69, 93)        # flagged false accepts
REC_G6_SPEC = (29, 30)          # real packages left alone
REC_G6_REAL_FLAGGED = ["zero-fill"]


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return centre - half, centre + half


def load_json(name):
    with open(os.path.join(RAW, name)) as fh:
        return json.load(fh)


def load_mutations():
    return load_json("mutations.json")


def rule_reasons(m, now=datetime.datetime(2026, 10, 8)):
    """The G6 rule, exactly as AMENDMENT-1.md fixed it.

    A clause whose field is None is dropped for that row (D082): a
    missing observation is never a zero and never a denominator.
    `desc-bad` reads "contains a URL" as any http(s):// substring; no
    row in either class carries one, so the stricter reading of "a
    bare URL" changes no verdict.
    """
    reasons = []
    dl = m.get("downloads")
    if dl is not None and dl < 1000:
        reasons.append("downloads<1000")
    desc = m.get("desc") or ""
    if not desc.strip():
        reasons.append("desc-empty")
    low = desc.lower()
    if any(k in low for k in ("img.shields", "badge", "dependabot")) \
            or "http://" in low or "https://" in low:
        reasons.append("desc-bad")
    newest = m.get("newest")
    if newest:
        try:
            when = datetime.datetime.fromisoformat(
                newest.replace("Z", "+00:00")).replace(tzinfo=None)
            if (now - when).days > 365 * 3:
                reasons.append("stale>3y")
        except Exception:
            pass
    if not m.get("repo"):
        reasons.append("no-repo")
    return reasons


def main():
    bad = []

    def check(label, got, want):
        ok = got == want
        if not ok:
            bad.append((label, got, want))
        print("%-34s %-28s %s" % (label, str(got),
                                   "ok" if ok else "!= recorded %s" % (want,)))

    # ---- G1: population -------------------------------------------------
    seeds = load_json("verdicts-seeds.json")
    mut_rows = load_mutations()
    mutated = [r for r in mut_rows if r["arm"] == "mutated"]
    seed_rows = [r for r in mut_rows if r["arm"] == "seed"]
    seed_eco = sorted(set(r["ecosystem"] for r in seeds
                          if r["verdict"] == "exists"))
    check("G1 seeds resolving", (sum(1 for r in seeds
                                       if r["verdict"] == "exists"),
                                 len(seeds), len(seed_eco)), REC_G1_SEEDS)
    check("G1 mutations generated", len(mutated), REC_G1_MUTATIONS)
    assert len(seed_rows) == len(seeds), "seed rows and seed verdicts differ"

    # ---- G5: the false-accept rate --------------------------------------
    verdicts = {}
    for path in sorted(glob.glob(os.path.join(RAW, "verdicts-*.json"))):
        for r in load_json(os.path.basename(path)):
            if r.get("arm") == "mutated":
                verdicts[(r["ecosystem"], r["name"])] = r["verdict"]
    fa = [k for k, v in verdicts.items() if v == "exists"]
    check("G5 false accepts / mutations", (len(fa), len(verdicts)),
          (REC_G5_K, REC_G5_N))
    lo, hi = wilson(len(fa), len(verdicts))
    print("    rate %.4f  Wilson95 [%.4f, %.4f]  (kill line was < 0.05)"
          % (len(fa) / len(verdicts), lo, hi))

    per_eco = {}
    for (eco, _), v in verdicts.items():
        d = per_eco.setdefault(eco, [0, 0])
        d[0] += 1
        if v == "exists":
            d[1] += 1
    for eco in sorted(per_eco):
        n_, k_ = per_eco[eco]
        l, h = wilson(k_, n_)
        print("    %-9s %3d/%3d = %.4f  [%.4f, %.4f]"
              % (eco, k_, n_, k_ / n_, l, h))

    fam = {}
    for r in mutated:
        v = verdicts.get((r["ecosystem"], r["name"]))
        if v is None:
            continue
        d = fam.setdefault(r["mutation"], [0, 0])
        d[0] += 1
        if v == "exists":
            d[1] += 1
    for f_ in sorted(fam):
        n_, k_ = fam[f_]
        print("    family %-9s %3d/%3d = %.4f" % (f_, k_, n_, k_ / n_))

    # ---- G6: discriminability of the declared rule ----------------------
    fa_meta = load_json("metadata-falseaccepts.json")
    real_meta = load_json("metadata-real.json")
    # D082: rows the registry did not answer are not a denominator
    fa_eval = [m for m in fa_meta if m["verdict"] == "exists"]
    real_eval = [m for m in real_meta if m["verdict"] == "exists"]
    print("    evaluable rows: false accepts %d/%d, real %d/%d"
          % (len(fa_eval), len(fa_meta), len(real_eval), len(real_meta)))
    fa_flag = [rule_reasons(m) for m in fa_eval]
    real_flag = [rule_reasons(m) for m in real_eval]
    recall = sum(1 for r in fa_flag if r)
    spec = sum(1 for r in real_flag if not r)
    check("G6 recall arm (FA flagged)", (recall, len(fa_eval)), REC_G6_RECALL)
    check("G6 specificity arm (real left alone)",
          (spec, len(real_eval)), REC_G6_SPEC)
    flagged_real = [m["name"] for m, r in zip(real_eval, real_flag) if r]
    check("G6 real rows flagged", flagged_real, REC_G6_REAL_FLAGGED)
    print("    recall %.4f (gate >= 0.90: %s);  specificity %.4f "
          "(gate >= 0.90: %s)"
          % (recall / len(fa_eval),
             "PASS" if recall / len(fa_eval) >= 0.90 else "FAIL",
             spec / len(real_eval),
             "PASS" if spec / len(real_eval) >= 0.90 else "FAIL"))

    reasons = {}
    for r in fa_flag:
        for x in r:
            reasons[x] = reasons.get(x, 0) + 1
    print("    false-accept flag reasons: %s" % reasons)
    residual = [(m["ecosystem"], m["name"], m.get("downloads"))
                for m, r in zip(fa_eval, fa_flag) if not r]
    print("    residual false accepts the rule misses: %d" % len(residual))
    for eco, name, dl in residual:
        print("      %-9s %-40s downloads=%s" % (eco, name, dl))

    # ---- the recovery the record must carry -----------------------------
    refetch = load_json("refetch-real-12.json")
    check("refetched real rows now resolve",
          sum(1 for r in refetch if r["verdict"] == "exists"), len(refetch))

    if bad:
        print("\noutcome: %d CHECK(S) DISAGREE WITH THE RECORD" % len(bad))
        return 1
    print("\noutcome: every number reproduces from the committed bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

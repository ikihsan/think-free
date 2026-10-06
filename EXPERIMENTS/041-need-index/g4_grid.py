#!/usr/bin/env python3
"""E041 G4 across the grid, because the frozen tau is too low to say anything.

G4 asks whether the *validated* instrument, applied unchanged to E040's arms A
(the 1391 need statements) and B (their matched near-miss controls), still
separates them. At the frozen tau of 0.05 the answer is 0.981 against 0.977 --
both arms saturated, because a threshold that 0 of 77 real controls reach is a
threshold almost nothing reaches.

That is a real reading of a real number and also a reading of nothing, so this
script reports the separation across the whole grid rather than at one point.
D069's rule: where a threshold cannot be calibrated on a valid control, the
dependent claim is restated threshold-free.

Cheap enough to be worth the whole grid: 1391 rows per arm, one index each.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E040 = os.path.join(os.path.dirname(HERE), "040-need-clustering", "raw")
sys.path.insert(0, HERE)
import stream  # noqa: E402

TAUS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]
BAR = 1.5


def arm_rows(arm):
    texts = []
    with open(os.path.join(E040, "arm_%s.jsonl" % arm)) as fh:
        for line in fh:
            texts.append(json.loads(line)["text"])
    return texts[:1391]


def partner_rates(texts, taus):
    idx, wts, keep = stream.stream_vectors(texts, range(len(texts)))
    n = len(texts)
    above = {("%.2f" % t): 0 for t in taus}
    for i in range(n):
        acc = stream.score_row(idx, wts, keep[i], i)
        for k in above:
            if any(v >= float(k) for v in acc.values()):
                above[k] += 1
        acc = None
    return {k: round(v / n, 6) for k, v in above.items()}


def main():
    out = {"taus": TAUS, "bar": BAR, "arms": {}}
    for arm in ("A", "B"):
        out["arms"][arm] = partner_rates(arm_rows(arm), TAUS)
        print(arm, json.dumps(out["arms"][arm], sort_keys=True), flush=True)
    grid = {}
    for t in TAUS:
        k = "%.2f" % t
        a, b = out["arms"]["A"][k], out["arms"]["B"][k]
        grid[k] = {"A": a, "B": b,
                   "ratio": (a / b) if b > 0 else None,
                   "ratio_state": ("evaluated" if b > 0 else
                                   "not_evaluated (control arm is 0 -- F067)"),
                   "met": ((a / b) >= BAR) if b > 0 else "not_evaluated"}
    out["grid"] = grid
    judged = [k for k, v in grid.items() if v["ratio"] is not None]
    out["separation_ever"] = any(grid[k]["ratio"] >= BAR for k in judged)
    out["best_ratio"] = max(((grid[k]["ratio"], k) for k in judged),
                            default=(None, None))
    path = os.path.join(RAW, "g4_grid.json")
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)
    print("\n  tau      A        B     ratio   met")
    for k in [("%.2f" % t) for t in TAUS]:
        v = grid[k]
        print("%6s %8s %8s %8s %6s" % (
            k, v["A"], v["B"],
            "%.3f" % v["ratio"] if v["ratio"] is not None else "-",
            v["met"]))
    print("\nseparation ever reached the 1.5 bar: %s (best %s at tau=%s)"
          % (out["separation_ever"], out["best_ratio"][0], out["best_ratio"][1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

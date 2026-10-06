#!/usr/bin/env python3
"""E041 scaling: does G4 resolution grow with corpus size, or is it bounded?

**Does item 0f's premise survive its own arithmetic?** Item 0f proposes building a
needs index over a *second public venue*, on the reasoning that recognition is "thin
only because 1391 rows is a small population", that recognition is a rate over a
population, and therefore that whether it scales is arithmetic before it is anything
else. `PROTOCOL-scaling.md` fixes that question and the grid.

`clustering.py` holds the primitives and is split from this file **by invariant**:
that one forms clusters, this one decides what the curve means. The reason is in
`DECISIONS-SCREENING-9.md` D069 — a threshold and the statistic it licenses must not be
editable in the same place.

**Two things must hold before any curve is reported**, both from AMENDMENT-3:

1. **Reproduction.** At `n = 1391` the subsample is the whole arm, so the curve's
   rightmost point must reproduce the G4 counts E040 recorded in `raw/tally.json` —
   8 at tau=0.15, 1 at 0.20, 1 at 0.25, 0 above. If it does not, the instrument, the
   clustering or the row selection has drifted, and the run is `not_evaluated`.
2. **Exactness of the optimisation.** The edge list is asserted to give the same
   components as E040's dense O(n^2) `cluster_stats` at every threshold, at full size.

Neither assertion can move a result. They can only stop the run.

The instrument is E040's own, imported from its `gates.py`. A fitted `alpha` over
`n ≤ 1391` is a local exponent, and every `n ≈ 3500` figure below is labelled
`inferred` and never `observed`.
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "040-need-clustering"))

from clustering import (ARMS, BOOT, E040_PUBLISHED, E040_PUBLISHED_SRC,  # noqa: E402
                        N_GRID, QUALIFY, RESAMPLES, SEED, cluster_stats,
                        components, edge_list, load_arm, percentile,
                        subsample_indices, tk)
from gates import TAU_GRID, vectors  # noqa: E402

OUT = os.path.join(RAW, "scaling.json")
MIN_TAU = min(TAU_GRID)
BAR_20 = 20          # E040's G4 bar, unchanged
ALPHA_BAR = 1.0      # S2
ALPHA_CI_FLOOR = 0.75


def curve(arm):
    """Qualifying-cluster count at each (n, tau), mean over RESAMPLES draws."""
    rows, texts = load_arm(arm)
    n_rows = len(rows)
    vecs = vectors(texts)
    ids = [r["id"] for r in rows]

    # AMENDMENT-3 provision 1: the dense pass and the edge list must agree, and at
    # full size the result must be E040's own recorded number.
    full = list(range(n_rows))
    dense = {tk(t): len([c for c in cluster_stats(rows, vecs, t)
                         if c["size"] >= QUALIFY and c["stories"] >= QUALIFY
                         and c["authors"] >= QUALIFY]) for t in TAU_GRID}
    src, dst, val = edge_list(vecs, MIN_TAU)
    fast = {tk(t): len(components(rows, full, src, dst, val, t))
            for t in TAU_GRID}
    checks = {"dense_full_size": dense, "edge_full_size": fast,
              "edge_equals_dense": dense == fast,
              "edges_retained_at_min_tau": len(src)}
    if not checks["edge_equals_dense"]:
        raise SystemExit("not_evaluated: the edge-list optimisation disagrees "
                         "with E040's dense pass: %s vs %s" % (dense, fast))
    if arm == "A":
        want = {tk(t): E040_PUBLISHED[tk(t)] for t in TAU_GRID}
        checks["expected_from_e040_tally_json"] = want
        checks["e040_source"] = E040_PUBLISHED_SRC
        checks["e040_readme_prose_said"] = {
            tk(t): (8 if t == 0.15 else 0) for t in TAU_GRID}
        checks["reproduces_e040_tally_json"] = (fast == want)
        if fast != want:
            raise SystemExit("not_evaluated: the full-size point does not "
                             "reproduce E040's recorded G4 counts: %s vs %s"
                             % (fast, want))

    out = {}
    for n in N_GRID:
        counts = {t: [] for t in TAU_GRID}
        sizes = {t: [] for t in TAU_GRID}
        for rep in range(RESAMPLES):
            members = subsample_indices(ids, n, SEED, rep)
            for t in TAU_GRID:
                q = components(rows, members, src, dst, val, t)
                counts[t].append(len(q))
                sizes[t].append(max([c["size"] for c in q], default=0))
        out[n] = {tk(t): {
            "mean": round(sum(counts[t]) / len(counts[t]), 4),
            "p05": percentile(sorted(counts[t]), 0.05),
            "p95": percentile(sorted(counts[t]), 0.95),
            "max_cluster_mean": round(sum(sizes[t]) / len(sizes[t]), 4),
            "zero_draws": sum(1 for c in counts[t] if c == 0),
        } for t in TAU_GRID}
        print("n=%-5d %s" % (n, "  ".join("%.2f" % out[n][tk(t)]["mean"]
                                          for t in TAU_GRID)), flush=True)
    return out, checks


def fit_alpha(counts_by_n, seed=SEED, nboot=BOOT):
    """OLS slope of log(count+1) on log(n), bootstrap CI over grid points.

    `alpha ≈ 1` is linear: doubling the corpus doubles the clusters. `alpha < 1`
    is sub-linear, and the bar of 20 is not reachable by growing the corpus.
    """
    xs = [(math.log(int(n)), math.log(c + 1.0)) for n, c in counts_by_n.items()]
    if len(xs) < 3:
        return None, None
    mx = sum(x for x, _ in xs) / len(xs)
    my = sum(y for _, y in xs) / len(xs)
    den = sum((x - mx) ** 2 for x, _ in xs)
    if not den:
        return None, None
    slope = sum((x - mx) * (y - my) for x, y in xs) / den
    rnd = random.Random(seed)
    slopes = []
    for _ in range(nboot):
        pick = [xs[rnd.randrange(len(xs))] for _ in range(len(xs))]
        ax = sum(x for x, _ in pick) / len(pick)
        ay = sum(y for _, y in pick) / len(pick)
        d = sum((x - ax) ** 2 for x, _ in pick)
        if d:
            slopes.append(sum((x - ax) * (y - ay) for x, y in pick) / d)
    slopes.sort()
    return (round(slope, 4),
            [round(percentile(slopes, 0.025), 4),
             round(percentile(slopes, 0.975), 4)])


def main():
    report = {"protocol": "EXPERIMENTS/041-need-index/PROTOCOL-scaling.md",
              "amendments": ["AMENDMENT-3.md", "AMENDMENT-5.md"],
              "n_grid": N_GRID, "resamples": RESAMPLES, "seed": SEED,
              "tau_grid": TAU_GRID, "qualify": QUALIFY, "bar": BAR_20}
    curves, alphas, checks = {}, {}, {}
    for arm in ARMS:
        curves[arm], checks[arm] = curve(arm)
        alphas[arm] = {}
        for t in TAU_GRID:
            cb = {str(n): curves[arm][n][tk(t)]["mean"] for n in N_GRID}
            s, ci = fit_alpha(cb)
            alphas[arm][tk(t)] = {"alpha": s, "ci95": ci, "counts": cb}
    report["checks"] = checks
    report["curves"] = curves
    report["alphas"] = alphas

    n_last = N_GRID[-1]
    judged = [tk(t) for t in TAU_GRID
              if max(alphas["A"][tk(t)]["counts"].values()) > 0]
    gates = {}
    gates["S1"] = {
        "met": bool(alphas["A"][tk(MIN_TAU)]["counts"][str(n_last)] > 0),
        "note": "arm A yields a qualifying cluster at full size",
        "observed": alphas["A"][tk(MIN_TAU)]["counts"][str(n_last)]}
    per_tau = {}
    for t in judged:
        a = alphas["A"][t]
        per_tau[t] = {
            "alpha": a["alpha"], "ci95": a["ci95"],
            "met": bool(a["alpha"] is not None and a["alpha"] >= ALPHA_BAR
                        and a["ci95"] and a["ci95"][0] > ALPHA_CI_FLOOR)}
    gates["S2"] = {"met": bool(judged) and all(v["met"] for v in per_tau.values()),
                   "bar": "alpha >= 1.0 and CI95 lower > 0.75, every judged tau",
                   "judged_taus": judged, "per_tau": per_tau}
    b_le = all(curves["B"][n][tk(t)]["mean"] <= curves["A"][n][tk(t)]["mean"]
               for n in N_GRID for t in TAU_GRID)
    a_al = [alphas["A"][t]["alpha"] for t in judged
            if alphas["A"][t]["alpha"] is not None]
    b_al = [alphas["B"][t]["alpha"] for t in judged
            if alphas["B"][t]["alpha"] is not None]
    gates["S3"] = {
        "met": bool(b_le and a_al and b_al and max(b_al) <= max(a_al)),
        "bar": "B's count <= A's at every (n, tau), and max alpha_B <= max alpha_A",
        "b_never_exceeds_a": b_le, "alpha_A": a_al, "alpha_B": b_al}
    report["gates"] = gates

    # Arithmetic on the fitted exponent. `inferred`, never `observed`: a slope
    # fitted over n <= 1391 extrapolated past it.
    reach = {}
    for t in judged:
        c = alphas["A"][t]["counts"][str(n_last)]
        a = alphas["A"][t]["alpha"]
        reach[t] = {
            "observed_at_n_%d" % n_last: c, "alpha": a,
            "implied_n_for_%d" % BAR_20: (round(n_last * (BAR_20 / c) ** (1.0 / a), 1)
                                          if c > 0 and a else None),
            "label": "inferred (extrapolation beyond n=%d)" % n_last}
    report["reach_estimate"] = reach
    tmp = OUT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
    os.replace(tmp, OUT)

    print("\narm A: qualifying clusters (mean of %d draws)" % RESAMPLES)
    print("%6s %s" % ("n", "  ".join("t=%.2f" % t for t in TAU_GRID)))
    for n in N_GRID:
        print("%6d %s" % (n, "  ".join("%.2f " % curves["A"][n][tk(t)]["mean"]
                                        for t in TAU_GRID)))
    print("\narm A vs arm B at full size: %d against %d qualifying clusters"
          % (checks["A"]["edge_full_size"][tk(MIN_TAU)],
             checks["B"]["edge_full_size"][tk(MIN_TAU)]))
    print("\nalpha, arm A / arm B")
    for t in TAU_GRID:
        print("  t=%.2f  A=%-8s %-22s  B=%-8s %s"
              % (t, alphas["A"][tk(t)]["alpha"], alphas["A"][tk(t)]["ci95"],
                 alphas["B"][tk(t)]["alpha"], alphas["B"][tk(t)]["ci95"]))
    print("\ngates: " + json.dumps({k: v["met"] for k, v in gates.items()}))
    print(json.dumps(reach, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

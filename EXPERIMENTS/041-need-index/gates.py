#!/usr/bin/env python3
"""E041 gate evaluation: what the partner ranks in `readout.py` mean.

Split at the 300-line cap **by invariant**. `readout.py` reads a text unit and
produces partner ranks; this file evaluates bars over those ranks. **A threshold and
the statistic it licenses must not be editable in the same place** -- the reasoning
that split E040's `gates.py` from its `tally.py`, and `DECISIONS-SCREENING-9.md`
D069 is the rule behind it: where a threshold cannot be calibrated on a valid
control, the dependent claim is restated threshold-free rather than recalibrated
elsewhere.

Every bar here is the one `PROTOCOL.md` declared: 1.5, 0.20, 0.50, 0.50. Nothing was
moved after a result was read. The one change of *evaluation* is recorded in
`AMENDMENT-7.md`: **a ratio with a zero denominator is `not_evaluated`, not
`False`**, because F067's defect -- a strongly positive result printing red -- made
it into the first version of that code.

`instrument.py` drives the run and imports `evaluate_unit` and `verdict_of` from
here; nothing here knows about processes.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "040-need-clustering"))

from readout import TAUS  # noqa: E402

N0_LOUD_CEILING = 0.05        # frozen-tau rule: strictest tau where N0 is quiet
TOP1_BAR = 0.50               # G2
RECALL_BAR = 0.50             # G3
RATIO_BAR = 1.5               # G1, E040's own bar
DIFF_BAR = 0.20               # G1's absolute bar, E040's own bar
BOOT = 10000
SEED = 20261006


def bootstrap_ci(diffs, seed=SEED, n=BOOT):
    """Percentile CI95 on the mean of paired differences, fixed seed."""
    if len(diffs) < 2:
        return None
    rnd = random.Random(seed)
    k = len(diffs)
    means = []
    for _ in range(n):
        s = 0.0
        for _ in range(k):
            s += diffs[rnd.randrange(k)]
        means.append(s / k)
    means.sort()
    return [means[int(0.025 * n)], means[int(0.975 * n) - 1]]


def summarise(unit_result):
    """Every headline number for one unit, by stratum and by pool size."""
    rows = unit_result["rows"]
    out = {"unit": unit_result["unit"],
           "corpus_rows": unit_result["corpus_rows"],
           "pairs": unit_result["pairs"]}
    for stratum in (None, "S-easy", "S-hard"):
        sub = rows if stratum is None else [r for r in rows
                                           if r["stratum"] == stratum]
        key = "pooled" if stratum is None else stratum
        if not sub:
            out[key] = {"n": 0, "note": "no rows"}
            continue
        ranks = sorted(r["rank"] for r in sub)
        med = (ranks[len(ranks) // 2] if len(ranks) % 2 else
               (ranks[len(ranks) // 2 - 1] + ranks[len(ranks) // 2]) / 2.0)
        out[key] = {
            "n": len(sub), "median_rank": med,
            "top1": round(sum(1 for r in sub if r["top1"]) / len(sub), 6),
            "top10": round(sum(1 for r in sub if r["rank"] <= 10) / len(sub), 6),
            "top100": round(sum(1 for r in sub if r["rank"] <= 100) / len(sub), 6),
            "beats_impostor": round(sum(1 for r in sub if r["beats_impostor"]) /
                                    len(sub), 6),
            "recall_at_tau": {("%.2f" % t): round(
                sum(1 for r in sub if r["target_cos"] >= t) / len(sub), 6)
                for t in TAUS},
            "mean_target_cos": round(sum(r["target_cos"] for r in sub) / len(sub), 6),
            "mean_impostor_cos": round(sum(r["impostor_cos"] for r in sub) /
                                       len(sub), 6),
            "mean_n0_cos": round(sum(r["n0_cos"] or 0.0 for r in sub) / len(sub), 6),
        }
    # AMENDMENT-2: partner rank against the pair's own repository, the easiest
    # pool this design offers, and the pool-size breakdown that shows how much of
    # top1 a small candidate set buys.
    bands = [(0, 250), (250, 1000), (1000, 4000), (4000, 10 ** 9)]
    out["by_own_pool"] = {}
    for lo, hi in bands:
        sub = [r for r in rows if lo <= r["own_repo_pool"] < hi]
        if not sub:
            continue
        out["by_own_pool"]["%d-%d" % (lo, hi if hi < 10 ** 9 else 10 ** 9)] = {
            "n": len(sub),
            "median_own_pool": sorted(r["own_repo_pool"] for r in sub)[len(sub) // 2],
            "top1": round(sum(1 for r in sub if r["top1"]) / len(sub), 6),
            "beats_impostor": round(sum(1 for r in sub if r["beats_impostor"]) /
                                    len(sub), 6),
            "median_rank": sorted(r["rank"] for r in sub)[len(sub) // 2],
        }
    out["per_repo"] = {}
    for repo in sorted({r["repo"] for r in rows}):
        sub = [r for r in rows if r["repo"] == repo]
        out["per_repo"][repo] = {
            "pairs": len(sub),
            "top1": round(sum(1 for r in sub if r["top1"]) / len(sub), 6),
            "beats_impostor": round(sum(1 for r in sub if r["beats_impostor"]) /
                                    len(sub), 6),
        }
    return out


def frozen_tau(rows):
    """The smallest tau on the grid where arm N0 is quiet, chosen without arm P.

    The strictest threshold that still works, so the positive arm gets the least
    room. It never looks at `recall_at_tau(P)`. The denominator is the number of
    rows the rates are over, which is the same count for both arms by construction
    -- every row contributes exactly one N0 draw.
    """
    n = len(rows)
    n0_rec = {("%.2f" % t): sum(1 for r in rows
                                if (r["n0_cos"] or 0.0) >= t) / n
              for t in TAUS}
    frozen = next((t for t in TAUS
                   if n0_rec["%.2f" % t] < N0_LOUD_CEILING), None)
    return frozen, n0_rec


def gate_g1(rows, frozen, n0_rec):
    """G1 — separates judged repeats from matched cross-repository controls."""
    key = "%.2f" % frozen
    rec_p = sum(1 for r in rows if r["target_cos"] >= frozen) / len(rows)
    rec_n0 = n0_rec[key]
    ci = bootstrap_ci([(1.0 if r["target_cos"] >= frozen else 0.0) -
                       (1.0 if (r["n0_cos"] or 0.0) >= frozen else 0.0)
                       for r in rows])
    # AMENDMENT-7. The absolute difference is a subtraction of two measured rates
    # and is defined whenever both rates exist, so it carries no `rec_n0 > 0`
    # guard. The first version of this code guarded it, which turned "no control
    # row reached the frozen tau" into "this condition failed" on a run whose
    # paired difference was +0.74 with a CI95 of [0.64, 0.83] -- F067 again, in
    # the code written to avoid it.
    c_diff = (rec_p - rec_n0) >= DIFF_BAR
    c_ci = ci is not None and ci[0] > 0
    g = {"recall_P": round(rec_p, 6), "recall_N0": rec_n0,
         "paired_diff": round(rec_p - rec_n0, 6), "ci95": ci,
         "bar": "ratio >= 1.5 and diff >= 0.20 and CI95 lower > 0"}
    if rec_n0 > 0:
        ratio = rec_p / rec_n0
        c_ratio = ratio >= RATIO_BAR
        g.update({"ratio": ratio, "ratio_state": "evaluated",
                  "conditions": {"ratio": bool(c_ratio), "diff": bool(c_diff),
                                 "ci": bool(c_ci)},
                  "met": bool(c_ratio and c_diff and c_ci),
                  "met_on_evaluated_conditions": bool(c_diff and c_ci)})
    else:
        g.update({"ratio": None,
                  "ratio_state": ("not_evaluated (no control row reached the "
                                  "frozen tau, so the ratio has no denominator "
                                  "-- F067)"),
                  "conditions": {"ratio": None, "diff": bool(c_diff),
                                 "ci": bool(c_ci)},
                  # Every evaluable condition holds, and the gate as a whole is
                  # not evaluable. Both are reported; neither is read as the other.
                  "met": "not_evaluated",
                  "met_on_evaluated_conditions": bool(c_diff and c_ci)})
    return g


def gate_g2(rows):
    """G2 — the judged partner beats its single best impostor. Threshold-free."""
    n = len(rows)
    return {"top1": round(sum(1 for r in rows if r["top1"]) / n, 6),
            "beats_impostor": round(sum(1 for r in rows
                                        if r["beats_impostor"]) / n, 6),
            "met": (sum(1 for r in rows if r["beats_impostor"]) / n) >= TOP1_BAR,
            "bar": "beats_impostor >= 0.50 (threshold-free)"}


def gate_g3(rows, frozen):
    """G3 — a usable operating point exists at the frozen tau."""
    rec_p = sum(1 for r in rows if r["target_cos"] >= frozen) / len(rows)
    return {"recall_P": round(rec_p, 6), "met": rec_p >= RECALL_BAR,
            "bar": "recall >= 0.50 at the frozen tau"}


def evaluate_unit(res):
    """All three threshold-bearing gates for one unit's rows."""
    rows = res["rows"]
    frozen, n0_rec = frozen_tau(rows)
    g = {"frozen_tau": frozen, "recall_at_tau_N0": n0_rec}
    if frozen is None:
        g["G1"] = g["G2"] = g["G3"] = "not_evaluated"
        g["frozen_tau_note"] = (
            "no tau on the grid makes N0 quieter than %.2f, so the frozen tau "
            "does not exist and G1/G3 are not_evaluated" % N0_LOUD_CEILING)
        return g, None
    g["G1"] = gate_g1(rows, frozen, n0_rec)
    g["G2"] = gate_g2(rows)
    g["G3"] = gate_g3(rows, frozen)
    s = summarise(res)
    g["S_easy"] = {k: v for k, v in s["S-easy"].items() if k != "recall_at_tau"}
    g["S_hard"] = {k: v for k, v in s["S-hard"].items() if k != "recall_at_tau"}
    g["verdict_S_easy"] = all([g["G1"]["met"] is True, g["G2"]["met"],
                               g["G3"]["met"]])
    return g, frozen


def verdict_of(g):
    if g["frozen_tau"] is None:
        return "not_evaluated (no quiet tau)"
    met = [g["G1"]["met"], g["G2"]["met"], g["G3"]["met"]]
    if all(m is True for m in met):
        return "met G1-G3"
    return "; ".join("%s %s" % (nm, m) for nm, m in
                     zip(("G1", "G2", "G3"), met) if m is not True)

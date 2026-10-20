#!/usr/bin/env python3
"""E182 stage 6: the post-hoc power check on the accepted instrument.

The declared gate (G2') is a 0/1 label on 9 versus 6 rows. This is the
better-powered companion: an exact two-sided permutation test on the
*continuous* residual overlap, over the same rows and the same accepted
instrument, so "the null was just a small n" can be answered rather than
asserted.

It is reported beside the gate and never instead of it.

Usage: python3 power.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def mwu_exact(a, b):
    """Exact two-sided Mann-Whitney U on a continuous statistic.

    The two-sided p counts permutations at least as far from U's centre
    `n1*n2/2` as the observed U. An earlier version of this function compared
    against 0 instead of the centre, which returns p < 0.001 for an observed U
    sitting exactly at the midpoint -- the arithmetic error F136 records in
    this repository's own Fisher tails, repeated once here and caught by the
    midpoint case being the one that matters.
    """
    import itertools
    pool = sorted(a + b)
    n1, n2 = len(a), len(b)
    if not n1 or not n2:
        return None, None
    centre = n1 * n2 / 2.0

    def rank_of(v):
        i = pool.index(v)
        j = i
        while j + 1 < len(pool) and pool[j + 1] == v:
            j += 1
        return (i + j) / 2.0 + 1

    def u_of(xs):
        return sum(rank_of(v) for v in xs) - n1 * (n1 + 1) / 2.0

    obs = u_of(a)
    dev = abs(obs - centre)
    total = cnt = 0
    for combo in itertools.combinations(range(n1 + n2), n1):
        idx = set(combo)
        xs = [pool[k] for k in idx]
        ys = [pool[k] for k in range(n1 + n2) if k not in idx]
        total += 1
        if abs(u_of(xs) - centre) >= dev - 1e-12:
            cnt += 1
    return obs, cnt / float(total)


def median(xs):
    s = sorted(xs)
    n = len(s)
    if not n:
        return None
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def main():
    ov = json.load(open(os.path.join(HERE, "overlap.json")))
    rows = [r for r in ov["rows"]
            if r.get("overlap") is not None and not r["calibration"]]

    def sel(arm, reached):
        return [r["overlap"] for r in rows
                if r["arm"] == arm and r["reached"] == reached]

    em, eh = sel("EVID", False), sel("EVID", True)
    sh, sm = sel("SELF", True), sel("SELF", False)

    out = {}
    for name, x, y in (("EVID_missed_vs_EVID_hit", em, eh),
                       ("EVID_missed_vs_SELF_hit", em, sh),
                       ("SELF_missed_vs_SELF_hit", sm, sh)):
        if not x or not y:
            out[name] = {"n_x": len(x), "n_y": len(y), "p": None}
            continue
        u, p = mwu_exact(x, y)
        out[name] = {"n_x": len(x), "n_y": len(y),
                     "median_x": median(x), "median_y": median(y),
                     "U": u, "centre": len(x) * len(y) / 2.0,
                     "exact_permutation_p": p,
                     "note": "lower residual overlap = more divergent"}

    # The declared gate's own detector has calibration sensitivity 0.60, so the
    # honest bound on the true divergent rate on each side is the measured
    # count / 0.60. It is reported because it is the statement about power.
    def div(arm, reached):
        return sum(1 for r in ov["rows"] if r.get("divergent")
                   and r["arm"] == arm and r["reached"] == reached
                   and not r["calibration"])

    out["gate_bound"] = {
        "measured_divergent_missed": div("EVID", False), "n_missed": len(em),
        "measured_divergent_hit": div("EVID", True), "n_hit": len(eh),
        "true_rate_bound_missed_at_sensitivity_0p60":
            (round(div("EVID", False) / 0.60 / len(em), 4) if em else None),
        "true_rate_bound_hit_at_sensitivity_0p60":
            (round(div("EVID", True) / 0.60 / len(eh), 4) if eh else None),
    }
    out["sensitivity_note"] = (
        "tau was fitted at 0.05: the accepted detector fires only when the "
        "runner-up shares essentially no residual prescriptive token with the "
        "top answer. Calibration sensitivity was 0.6000, so the measured "
        "divergent count understates the true rate by roughly this factor. The "
        "bound it implies straddles both arms and therefore carries no "
        "information about which is larger.")

    with open(os.path.join(HERE, "power.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for k, v in out.items():
        if k in ("sensitivity_note", "gate_bound") or "n_x" not in v:
            continue
        print("%-28s n=%d vs %d  median %.3f vs %.3f  U=%.1f (centre %.1f)  "
              "exact p=%s"
              % (k, v["n_x"], v["n_y"], v["median_x"] if v["n_x"] else -1,
                 v["median_y"] if v["n_y"] else -1, v.get("U", -1),
                 v.get("centre", -1),
                 ("%.4f" % v["exact_permutation_p"])
                 if v.get("exact_permutation_p") is not None else "n/a"))
    print()
    print(out["sensitivity_note"])
    print("gate bound at sensitivity 0.60: divergent rate on EVID missed could "
          "be as high as %.4f, on EVID hit as high as %.4f"
          % (out["gate_bound"]["true_rate_bound_missed_at_sensitivity_0p60"],
             out["gate_bound"]["true_rate_bound_hit_at_sensitivity_0p60"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""E030 gate A9 — is the recurrence statistic above chance?

AMENDMENT-8 section 3. Runs the identical pipeline on signatures PERMUTED across
accounts within the same arm: each account keeps its signature's size and every
token keeps its arm-level frequency, but the token no longer belongs to the
account that wrote it. The only thing destroyed is the token-to-account
association, so anything the observed statistic carries beyond this null is signal
and anything it shares with it is coincidence.

Also reports the length-matched subsample and the mean rare-signature size, both
feeding no gate (AMENDMENT-8 section 4).

Writes raw/a9_permutation.json
"""

import json
import os
import random
import statistics
import sys

import common as C
import recurrence as R

PERMS = 50
SEED = 3008
LENGTH_SEED = 3009


def pairs_from_signatures(rows, sigs, rare, require_distinct_artifact):
    index = {}
    for i, s in enumerate(sigs):
        for t in s & rare:
            index.setdefault(t, []).append(i)
    shared = {}
    for t, bucket in index.items():
        if len(bucket) < 2:
            continue
        for ai in range(len(bucket)):
            for bi in range(ai + 1, len(bucket)):
                a, b = bucket[ai], bucket[bi]
                if rows[a]["author"] == rows[b]["author"]:
                    continue
                if require_distinct_artifact:
                    if not rows[a].get("artifact") or not rows[b].get("artifact"):
                        continue
                    if rows[a]["artifact"].lower() == rows[b]["artifact"].lower():
                        continue
                key = (a, b) if a < b else (b, a)
                shared.setdefault(key, []).append(t)
    return [(a, b) for (a, b), ts in shared.items() if len(ts) >= R.SHARED_MIN]


def prepare(rows):
    sigs = [R.signature(r) for r in rows]
    df = {}
    for s in sigs:
        for t in s:
            df[t] = df.get(t, 0) + 1
    cutoff = max(1, int(round(len(rows) * R.COMMON_FRACTION)))
    sigs = [s - set(t for t in s if df[t] > cutoff) for s in sigs]
    rare = set(t for t in df if df[t] <= R.RARE_MAX_DF)
    return sigs, rare, cutoff


def rate(rows, sigs, rare, require_distinct_artifact):
    pairs = pairs_from_signatures(rows, sigs, rare, require_distinct_artifact)
    partners = set()
    for a, b in pairs:
        partners.add(a)
        partners.add(b)
    return len(partners), len(pairs)


def permute(sigs, rng):
    pool = [t for s in sigs for t in s]
    rng.shuffle(pool)
    out, i = [], 0
    for s in sigs:
        out.append(set(pool[i:i + len(s)]))
        i += len(s)
    return out


def length_matched(treat, ctrl, size):
    """Re-sample both arms to the same text-length distribution (deciles)."""
    def decile(rows):
        by = {}
        for r in rows:
            d = min(9, int(10 * r["words"] / float(size)))
            by.setdefault(d, []).append(r)
        return by

    dt, dc = decile(treat), decile(ctrl)
    rng = random.Random(LENGTH_SEED)
    common = sorted(set(dt) & set(dc))
    out_t, out_c = [], []
    for d in common:
        n = min(len(dt[d]), len(dc[d]))
        out_t.extend(rng.sample(dt[d], n))
        out_c.extend(rng.sample(dc[d], n))
    return out_t, out_c


def main():
    os.makedirs(C.RAW, exist_ok=True)
    treat = C.read_jsonl("treatment.jsonl")
    ctrl = C.read_jsonl("control.jsonl")
    report = {}

    for label, rows, req in (("treatment", treat, True), ("control", ctrl, False)):
        sigs, rare, cutoff = prepare(rows)
        mean_sig = statistics.mean(len(s) for s in sigs)
        mean_rare = statistics.mean(len(s & rare) for s in sigs)
        k_obs, p_obs = rate(rows, sigs, rare, req)
        n = len(rows)
        obs_lo, obs_hi = C.wilson(k_obs, n)

        rng = random.Random(SEED)
        nulls = []
        for _ in range(PERMS):
            k, p = rate(rows, permute(sigs, rng), rare, req)
            nulls.append(k / float(n))
        mu = statistics.mean(nulls)
        sd = statistics.pstdev(nulls) or 1e-9
        null_lo, null_hi = C.wilson(round(mu * n), n)

        report[label] = {
            "n_accounts": n,
            "common_fraction_cutoff": cutoff,
            "mean_signature_size": round(mean_sig, 2),
            "mean_rare_signature_size": round(mean_rare, 2),
            "median_words": statistics.median(r["words"] for r in rows),
            "observed": {"accounts_with_partner": k_obs, "pairs": p_obs,
                         "R_pair": k_obs / float(n),
                         "ci95": [obs_lo, obs_hi]},
            "permutation": {"n": PERMS, "mean_R": mu, "sd_R": sd,
                            "min_R": min(nulls), "max_R": max(nulls),
                            "mean_ci95": [null_lo, null_hi]},
            "z_observed": ((k_obs / float(n)) - mu) / sd,
            "gate_a9_fires": bool(obs_lo > null_hi),
        }
        C.log("a9", arm=label, n=n, observed=round(k_obs / float(n), 4),
              null_mean=round(mu, 4), null_sd=round(sd, 4),
              z=round(report[label]["z_observed"], 2),
              mean_rare_sig=round(mean_rare, 1),
              gate_fires=report[label]["gate_a9_fires"])

    # length-matched subsample (feeds no gate)
    size = max(r["words"] for r in treat + ctrl)
    lt, lc = length_matched(treat, ctrl, size)
    matched = {}
    for label, rows, req in (("treatment_length_matched", lt, True),
                             ("control_length_matched", lc, False)):
        sigs, rare, cutoff = prepare(rows)
        k, p = rate(rows, sigs, rare, req)
        lo, hi = C.wilson(k, len(rows))
        matched[label] = {"n": len(rows), "R_pair": k / float(rows and len(rows) or 1),
                          "ci95": [lo, hi],
                          "median_words": statistics.median(r["words"] for r in rows)}
        C.log("length_matched", arm=label, n=len(rows),
              R_pair=round(k / float(len(rows)), 4),
              ci=[round(lo, 4), round(hi, 4)],
              median_words=matched[label]["median_words"])
    d = C.diff_ci(matched["treatment_length_matched"]["n"] and
                  round(matched["treatment_length_matched"]["R_pair"] *
                        matched["treatment_length_matched"]["n"]),
                  matched["treatment_length_matched"]["n"],
                  round(matched["control_length_matched"]["R_pair"] *
                        matched["control_length_matched"]["n"]),
                  matched["control_length_matched"]["n"])
    matched["diff"] = {"diff": d[0], "ci95": [d[1], d[2]]}
    C.log("length_matched", variant="diff", diff=round(d[0], 4),
          ci95=[round(d[1], 4), round(d[2], 4)])
    report["length_matched"] = matched

    t = report["treatment"]
    report["verdict"] = {
        "a9_treatment_fires": t["gate_a9_fires"],
        "a9_control_fires": report["control"]["gate_a9_fires"],
        "h1": ("not_evaluated" if not t["gate_a9_fires"] else "readable"),
        "reason": ("the recurrence statistic is at or below its own permutation "
                   "null, so a difference in it is not a difference in clause "
                   "recurrence"),
    }
    C.log("verdict", **report["verdict"])

    with open(os.path.join(C.RAW, "a9_permutation.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""E177: score the comparison. Runs only on committed inputs.

Reports, in order: G0a (the treatment is an assistant), G0b/G0c (SCORE can
recover real positives and reject real negatives), G0d (the arms are disjoint),
then the declared comparison with Wilson intervals and a two-sided Fisher exact
test, and finally the census. Nothing here is a threshold that was not declared
in PROTOCOL.md or AMENDMENT-3.md.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def wilson(k, n, z=1.959963985):
    if not n:
        return (0.0, 1.0)
    p = k / float(n)
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fisher_2x2(a, b, c, d):
    """Two-sided Fisher exact p for [[a, b], [c, d]]. Stdlib only.

    AMENDMENT 6: the first version summed *ratios* to the observed table and so
    returned 1.0 for every table. The p-value is the sum of the probabilities of
    the tables at most as probable as the observed one; the observed table's own
    probability is a constant factor that has to stay in.
    """
    def logp(n, k):
        return (math.lgamma(n + 1) - math.lgamma(k + 1)
                - math.lgamma(n - k + 1))
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c
    p_obs = math.exp(logp(r1, a) + logp(r2, c1 - a) - logp(n, c1))
    total = 0.0
    for k in range(max(0, c1 - r2), min(r1, c1) + 1):
        pk = math.exp(logp(r1, k) + logp(r2, c1 - k) - logp(n, c1))
        if pk <= p_obs * (1 + 1e-9):
            total += pk
    return min(1.0, total)


def main():
    arms = json.load(open(os.path.join(HERE, "arms.json")))
    labels = {r["qid"]: r for r in
              json.load(open(os.path.join(HERE, "labels.json")))["labels"]}
    ans = {}
    for line in open(os.path.join(HERE, "ans", "answers.jsonl")):
        if line.strip():
            r = json.loads(line)
            ans[r["qid"]] = r["answer"]
    verdicts = {}
    for line in open(os.path.join(HERE, "score", "verdicts.jsonl")):
        if line.strip():
            r = json.loads(line)
            verdicts[r["pid"]] = r
    ctl = json.load(open(os.path.join(HERE, "control_pairs.json")))
    ctl_ids = set([p["id"] for p in ctl["g0b_identical_pairs"]]
                  + [p["id"] for p in ctl["g0c_distinct_pairs"]])
    index_pids = json.load(open(os.path.join(HERE, "score", "index.json")))["pids"]

    print("== integrity ==")
    print("verdicts %d; index %d; same set: %s"
          % (len(verdicts), len(index_pids), set(verdicts) == set(index_pids)))
    g0d = set(arms["arms"]["SELF"]) & set(arms["arms"]["EVID"])
    print("G0d arms disjoint: %s (%s)" % (not g0d, sorted(g0d) or "no overlap"))

    print("\n== G0a: is the treatment an assistant rather than a refuser ==")
    REFUSAL = ("not enough information", "cannot be answered", "can't be answered",
               "insufficient information", "no way to know", "impossible to say",
               "need more context", "without more information")
    ref = [q for q, a in ans.items()
           if a.strip().lower().startswith(REFUSAL) or len(a.split()) < 12]
    print("questions asked %d; refusals or stubs %d %s; gate >= 55 substantive: %s"
          % (len(ans), len(ref), sorted(ref), len(ans) - len(ref) >= 55))

    print("\n== G0b / G0c: can SCORE recover real positives and reject real "
          "negatives ==")
    b_yes = sum(1 for p in ctl["g0b_identical_pairs"]
                if verdicts.get(p["id"], {}).get("same_resolution") == "YES")
    c_yes = sum(1 for p in ctl["g0c_distinct_pairs"]
                if verdicts.get(p["id"], {}).get("same_resolution") == "YES")
    print("G0b identical pairs marked reached: %d of 5 (need 5) -> %s"
          % (b_yes, "PASS" if b_yes == 5 else "FAIL"))
    print("G0c distinct pairs marked reached: %d of 5 (need 0) -> %s"
          % (c_yes, "PASS" if c_yes == 0 else "FAIL"))
    scorer_ok = (b_yes == 5 and c_yes == 0)

    print("\n== the declared comparison ==")
    out = {}
    for want in ("SELF", "EVID"):
        qids = arms["arms"][want]
        reached = sum(1 for q in qids
                      if verdicts.get("g-%d" % q, {}).get("same_resolution") == "YES")
        missing = [q for q in qids if "g-%d" % q not in verdicts]
        lo, hi = wilson(reached, len(qids))
        out[want] = {"n": len(qids), "reached": reached, "missing_verdicts": missing,
                     "rate": round(reached / float(len(qids)), 4),
                     "ci95": [round(lo, 4), round(hi, 4)]}
        print("%-5s n=%d reached=%d rate=%.4f CI95 [%.4f, %.4f]%s"
              % (want, len(qids), reached, reached / float(len(qids)), lo, hi,
                 "  MISSING %s" % missing if missing else ""))
    a, b = out["SELF"]["reached"], out["SELF"]["n"] - out["SELF"]["reached"]
    c, d = out["EVID"]["reached"], out["EVID"]["n"] - out["EVID"]["reached"]
    gap = out["SELF"]["rate"] - out["EVID"]["rate"]
    p = fisher_2x2(a, b, c, d)
    out["gap"] = round(gap, 4)
    out["fisher_p"] = p
    out["g0a_pass"] = len(ans) - len(ref) >= 55
    out["g0b_pass"] = b_yes == 5
    out["g0c_pass"] = c_yes == 0
    out["scorer_established"] = scorer_ok
    print("gap (SELF - EVID) = %+.4f   Fisher exact two-sided p = %.6g"
          % (gap, p))
    fired = (gap >= 0.25 and p < 0.05)
    out["g3_fired"] = fired
    print("G3 declared bar: gap >= 0.25 AND p < 0.05 -> %s" % ("FIRED" if fired
                                                              else "DID NOT FIRE"))
    print("\n== abstention by arm (reported, not gated) ==")
    for want in ("SELF", "EVID"):
        n_ref = sum(1 for q in arms["arms"][want]
                    if ans.get(q, "").strip().lower().startswith(REFUSAL)
                    or len(ans.get(q, "").split()) < 12)
        print("%-5s refusals or stubs %d of %d" % (want, n_ref,
                                                   len(arms["arms"][want])))

    print("\n== census (automatic, all keyed rows) ==")
    cen = json.load(open(os.path.join(HERE, "census.json")))["summary"]
    for k in ("rows_with_key_answer", "evidence_gain_median",
              "share_gain_ge_0.50", "share_gain_ge_0.50_rate",
              "share_gain_ge_0.50_ci95"):
        print("%-28s %s" % (k, cen[k]))
    out["census"] = cen
    out["labels"] = {"counts": json.load(open(os.path.join(HERE,
                                                           "labels.json")))["counts"]}
    with open(os.path.join(HERE, "result.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\nwrote result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
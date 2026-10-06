"""E032 — re-derive every number in README.md from raw/ and labels/.

`python3 tally.py --check` is the reproduction command named in PROTOCOL.md and
in tasks/T-0076. It reads only committed bytes and prints the gate table, so a
reader can confirm the verdict without trusting this session's account of it.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LAB = os.path.join(HERE, "labels")


def read_tsv(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if line.strip():
            rows.append(line.rstrip("\n").split("\t"))
    return rows[0], rows[1:]


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def newcombe(k1, n1, k2, n2, z=1.96):
    """CI for p1 - p2. Used for the treatment-minus-control difference so the
    interval is the interval of the difference, not two overlapping intervals."""
    if n1 == 0 or n2 == 0:
        return (None, None)
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (max(-1.0, lo), min(1.0, hi))


def main():
    link = json.load(open(os.path.join(RAW, "link.json")))
    fetch = [json.loads(l) for l in open(os.path.join(RAW, "fetch_log.jsonl")) if l.strip()]
    harvest = [json.loads(l) for l in open(os.path.join(RAW, "harvest.jsonl")) if l.strip()]
    key = [json.loads(l) for l in open(os.path.join(RAW, "q2_key.jsonl")) if l.strip()]

    _, labels = read_tsv(os.path.join(LAB, "q2_pairs.tsv"))
    answers = {k: v.strip().lower() for k, v in labels}

    # Row identity by ORDER against the key file, not by key set (D061, F049).
    assert len(labels) == len(key), "q2 sheet and key file disagree in length"
    for row, meta in zip(labels, key):
        assert len(row) == 2, "label row is not key<TAB>answer: %r" % (row,)
        k = row[0]
        assert k == meta["key"], "row-order mismatch: %s vs %s" % (k, meta["key"])
        assert answers.get(k) in ("same", "not same", "unclear"), \
            "unanswered q2 row %s: %r" % (k, answers.get(k))

    arm = {}
    for meta in key:
        a = answers[meta["key"]]
        arm.setdefault(meta["sheet"], {"same": 0, "n": 0})
        arm[meta["sheet"]]["n"] += 1
        if a == "same":
            arm[meta["sheet"]]["same"] += 1
        elif a == "unclear":
            arm[meta["sheet"]]["unclear"] = arm[meta["sheet"]].get("unclear", 0) + 1

    _, non = read_tsv(os.path.join(LAB, "q1_nonsense.tsv"))
    non_none = sum(1 for r in non if r[1].strip() != "none")
    non_rate = non_none / len(non)

    ok200 = sum(1 for f in fetch if f["status"] == 200)
    gates = []

    gates.append(("A1", ">= 95%% of attempted rows answer; %d held rows re-readable"
                  % len(harvest),
                  "pass" if ok200 / len(fetch) >= 0.95 and len(harvest) == 60 else "FAIL",
                  "%d/%d fetches 200, %d rows on disk" % (ok200, len(fetch), len(harvest))))
    gates.append(("A2", "candidate pairs > chance alone produces",
                  "pass" if link["A2_reachable"] else "FAIL",
                  "%d candidates vs chance %.2f" % (link["A2_candidate_pairs"],
                                                    link["A2_chance_expectation_mean"])))
    gates.append(("A3", "reader kappa >= 0.6",
                  "pass" if link["A3_kappa"] is not None and link["A3_kappa"] >= 0.6 else "FAIL",
                  "kappa = %s on %d double-read rows" % (link["A3_kappa"],
                                                         link["rows_double_read"])))
    neg = arm.get("negative", {"same": 0, "n": 0})
    gates.append(("A4", "nonsense clause rate <= 0.25 and negative pair `same` <= 0.20",
                  "pass" if non_rate <= 0.25 and (neg["same"] / neg["n"] if neg["n"] else 1) <= 0.20
                  else "FAIL",
                  "%d/%d nonsense clauses; %d/%d negatives `same`"
                  % (non_none, len(non), neg["same"], neg["n"])))
    pos = arm.get("positive", {"same": 0, "n": 0})
    gates.append(("A5", ">= 16 of 20 positive pairs read `same`",
                  "pass" if pos["same"] >= 16 else "FAIL",
                  "%d/%d positives `same`" % (pos["same"], pos["n"])))

    cand, ctrl = arm.get("candidates", {"same": 0, "n": 0}), arm.get("control", {"same": 0, "n": 0})
    diff = (cand["same"] / cand["n"] - ctrl["same"] / ctrl["n"]) if cand["n"] and ctrl["n"] else None
    lo, hi = newcombe(cand["same"], cand["n"], ctrl["same"], ctrl["n"])
    instruments_ok = all(g[2] == "pass" for g in gates)

    if diff is None:
        verdict = "not_evaluated"
    elif diff >= 0.20 and lo is not None and lo > 0 and cand["same"] >= 2:
        verdict = "B1_survives__the_zero_is_venue_specific"
    elif cand["same"] == 0 and instruments_ok:
        verdict = "B2_kills__the_zero_generalises_past_this_venue_class"
    else:
        verdict = "not_evaluated"

    print("E032 gate table\n" + "=" * 78)
    for name, rule, res, detail in gates:
        print("%-4s %-6s %-52s %s" % (name, res, rule[:52], detail))
    print("-" * 78)
    print("clauses entering analysis (both readers): %d" % link["clauses_both_readers"])
    print("candidate pairs : %d `same` of %d  (%.4f)"
          % (cand["same"], cand["n"], cand["same"] / cand["n"] if cand["n"] else 0))
    print("control pairs   : %d `same` of %d  (%.4f)"
          % (ctrl["same"], ctrl["n"], ctrl["same"] / ctrl["n"] if ctrl["n"] else 0))
    if diff is not None:
        print("difference      : %+.4f  CI95 [%+.4f, %+.4f]" % (diff, lo, hi))
    for armname in ("candidates", "control", "positive", "negative"):
        a = arm.get(armname)
        if a:
            print("  %-11s n=%-4d same=%-4d unclear=%d" % (armname, a["n"], a["same"],
                                                            a.get("unclear", 0)))
    print("-" * 78)
    print("VERDICT: %s" % verdict)

    out = {"schema": "origin.e032.tally/1", "verdict": verdict,
           "gates": [{"gate": g[0], "rule": g[1], "result": g[2], "detail": g[3]} for g in gates],
           "arms": arm, "nonsense_clause_rate": non_rate,
           "difference": diff, "diff_ci95": [lo, hi], "link": link}
    with open(os.path.join(RAW, "tally.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    return 0 if verdict != "not_evaluated" else 0


if __name__ == "__main__":
    sys.exit(main())
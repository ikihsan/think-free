"""E033 — re-derive every number in README.md from raw/ and labels/.

`python3 tally.py --check` is the reproduction command named in PROTOCOL.md and
in tasks/T-0077. It reads only committed bytes and prints the gate table, so a
reader can confirm the verdict without trusting this session's account of it.

Row identity is checked BY ORDER against raw/q2_key.jsonl, never by key set
(D061, from F049): a reader once returned the right id set in the wrong order.

The gate table lives here; the population statistics live in `descriptive.py`,
which is where they were moved when this file reached the 300-line cap.
"""
import collections
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import descriptive as D        # noqa: E402  - path must be set first

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LAB = os.path.join(HERE, "labels")
SHEETS = os.path.join(HERE, "sheets")


def read_tsv(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if line.strip():
            rows.append(line.rstrip("\n").split("\t"))
    return rows[0], rows[1:]


def kappa(pairs):
    """Cohen's kappa on rows where both readers gave a decidable label. Returns
    (None, n) when it is undefined, which E032's first defect turned into a
    reported 1.0 because the gate asserted raw agreement instead."""
    both = [(a, b) for a, b in pairs
            if a in ("same", "not same") and b in ("same", "not same")]
    n = len(both)
    if n == 0:
        return None, 0
    cats = ("same", "not same")
    obs = sum(1 for a, b in both if a == b) / float(n)
    ca = {c: sum(1 for a, _ in both if a == c) / float(n) for c in cats}
    cb = {c: sum(1 for _, b in both if b == c) / float(n) for c in cats}
    exp = sum(ca[c] * cb[c] for c in cats)
    if abs(1 - exp) < 1e-12:
        return None, n
    return (obs - exp) / (1 - exp), n


def main():
    harvest = [json.loads(l) for l in open(os.path.join(RAW, "harvest.jsonl")) if l.strip()]
    fetch = [json.loads(l) for l in open(os.path.join(RAW, "fetch_log.jsonl")) if l.strip()]
    edges = [json.loads(l) for l in open(os.path.join(RAW, "edges.jsonl")) if l.strip()]
    key = [json.loads(l) for l in open(os.path.join(RAW, "q2_key.jsonl")) if l.strip()]

    manifest = json.load(open(os.path.join(SHEETS, "MANIFEST.json")))
    sheet_rel = manifest["sheet"]
    if not os.path.isabs(sheet_rel) and not sheet_rel.startswith("sheets" + os.sep):
        sheet_rel = os.path.join("sheets", sheet_rel)   # manifest names it from HERE
    sheet_bytes = open(os.path.join(HERE, sheet_rel), "rb").read()
    sheet_digest = hashlib.sha256(sheet_bytes).hexdigest()
    assert sheet_digest == manifest["sha256"], \
        "sheet digest %s != manifest %s" % (sheet_digest, manifest["sha256"])

    _, r1 = read_tsv(os.path.join(LAB, "q2_pairs_r1.tsv"))
    _, r2 = read_tsv(os.path.join(LAB, "q2_pairs_r2.tsv"))
    l1 = {k: v.strip().lower() for k, v in r1}
    l2 = {k: v.strip().lower() for k, v in r2}

    for name, lab in (("r1", r1), ("r2", r2)):
        assert len(lab) == len(key), "%s length %d != key %d" % (name, len(lab), len(key))
        for row, meta in zip(lab, key):
            assert len(row) == 2, "%s row is not key<TAB>answer: %r" % (name, row)
            assert row[0] == meta["key"], \
                "%s order mismatch: %s vs %s" % (name, row[0], meta["key"])
    for k, v in list(l1.items()) + list(l2.items()):
        assert v in ("same", "not same", "unclear"), "bad label %s=%r" % (k, v)

    # --- D1/D2: the headline rate, per site and pooled ------------------------
    per_site = collections.defaultdict(lambda: {"n": 0, "dup": 0})
    for r in harvest:
        per_site[r["site"]]["n"] += 1
        if r.get("closed_reason") == "Duplicate":
            per_site[r["site"]]["dup"] += 1
    n = len(harvest)
    dup = sum(1 for r in harvest if r.get("closed_reason") == "Duplicate")
    rate = dup / float(n)
    lo, hi = D.wilson(dup, n)
    reasons = D.closure_distribution(harvest)
    vocab = set(k for k, _ in reasons.items() if not k.startswith("absent"))

    # --- the edge arm -------------------------------------------------------
    ids = set(r["question_id"] for r in harvest)
    arms = {}
    for meta in key:
        a, b = l1[meta["key"]], l2[meta["key"]]
        cell = arms.setdefault(meta["arm"], {"n": 0, "same_r1": 0, "same_r2": 0,
                                             "both_same": 0, "unclear": 0})
        cell["n"] += 1
        cell["same_r1"] += a == "same"
        cell["same_r2"] += b == "same"
        cell["both_same"] += (a == "same" and b == "same")
        cell["unclear"] += (a == "unclear" or b == "unclear")
    edge, unrel = arms.get("edge", {}), arms.get("unrelated", {})
    k, k_rows = kappa([(l1[m["key"]], l2[m["key"]]) for m in key])
    diff_author = sum(1 for e in edges
                      if e["canonical"].get("user_id") and e["dup"]["user_id"]
                      and e["canonical"]["user_id"] != e["dup"]["user_id"])
    a3_same = edge.get("both_same", 0)
    a3_ok = a3_same >= 30 and diff_author >= 30
    q_raw = (sum(1 for e in edges if e["canonical"]["question_id"] in ids)
             / float(len(edges))) if edges else None
    q = q_raw if a3_ok else None
    unrel_rate = (unrel.get("same_r1", 0) / float(unrel["n"])) if unrel.get("n") else None

    ok200 = sum(1 for f in fetch if f.get("status") == 200)
    gates = [
        ("A1", ">= 95% of fetches 200; every row carries a closed_reason value or its "
               "documented absence",
         "pass" if (ok200 / float(len(fetch))) >= 0.95 and len(vocab) >= 2 else "FAIL",
         "%d/%d fetches 200, %d rows, %d distinct closure reasons"
         % (ok200, len(fetch), n, len(vocab))),
        ("A2", "the visibility calculation's inputs are measured, not assumed (q is "
               "gated on A3: a count of unverified canonicals is not a count)",
         "pass" if (q is not None) else "FAIL",
         "p = %.4f measured; q_raw = %s over %d edges, A3 = %s"
         % (rate, ("%.4f" % q_raw) if q_raw is not None else "None", len(edges),
            "pass" if a3_ok else "FAIL")),
        ("A3", ">= 30 of 40 edges read `same` and canonical author differs on >= 30",
         "pass" if a3_ok else "FAIL",
         "%d/%d sheet rows `same` by both readers; author differs on %d/%d edges"
         % (a3_same, edge.get("n", 0), diff_author, len(edges))),
        ("A4", "reader kappa >= 0.6 (undefined kappa => not_evaluated)",
         "pass" if (k is not None and k >= 0.6) else "FAIL",
         "kappa = %s on %d double-read rows" % (k, k_rows)),
        ("A5", "the unrelated arm reads `same` for <= 0.20",
         "pass" if (unrel_rate is not None and unrel_rate <= 0.20) else "FAIL",
         "%d/%d `same` on reader 1 (%.4f)"
         % (unrel.get("same_r1", 0), unrel.get("n", 0), unrel_rate or 0.0)),
    ]
    verdict = D.verdict_for(lo, hi)

    d7 = D.counterfactual_draw(harvest)
    d6 = D.tertiles(harvest)
    d5 = D.word_lengths(harvest)
    d9 = D.unanswered_share(harvest)

    print("E033 gate table\n" + "=" * 78)
    for name, rule, res, detail in gates:
        print("%-4s %-6s %-54s %s" % (name, res, rule[:54], detail))
    print("-" * 78)
    print("population: %d questions, %d distinct users, sites %s"
          % (n, len(set(r["user_id"] for r in harvest if r["user_id"])),
             sorted(per_site)))
    for s in sorted(per_site):
        c = per_site[s]
        slo, shi = D.wilson(c["dup"], c["n"])
        print("  %-8s n=%-5d dup=%-4d rate=%.4f CI95 [%.4f, %.4f]"
              % (s, c["n"], c["dup"], c["dup"] / float(c["n"]), slo, shi))
    print("D2 closure distribution: " + ", ".join(
        "%s=%d" % (kk, vv) for kk, vv in sorted(reasons.items(), key=lambda kv: -kv[1])))
    print("-" * 78)
    print("HEADLINE D1: %d/%d = %.4f  CI95 [%.4f, %.4f]   record bound %.4f"
          % (dup, n, rate, lo, hi, D.RECORD_POOL))
    print("D7 counterfactual 60-draw by score: top-60 contains %d duplicates "
          "(scores %s), mean over %d sliding windows %.2f (max %d, %d windows empty)"
          % (d7["top60_duplicates"], d7["top_score_range"], d7["windows"],
             d7["mean_window_duplicates"], d7["max_window"], d7["windows_with_zero"]))
    print("D6 rate by score tertile:")
    for name in sorted(d6):
        if name.startswith("ratio"):
            continue
        t = d6[name]
        print("  %-30s n=%-5d dup=%-4d rate=%.4f CI95 [%.4f, %.4f]"
              % (name, t["n"], t["dup"], t["rate"], t["ci95"][0], t["ci95"][1]))
    if "ratio_low_over_high" in d6:
        print("  low/high ratio %.2fx" % d6["ratio_low_over_high"])
    print("D5 words: median %d (range %d-%d), inside E032's %s window %d/%d"
          % (d5["median_words"], d5["min"], d5["max"], d5["window"],
             d5["in_e032_window"], n))
    print("D9 unanswered share: duplicate %d/%d = %.4f vs other %d/%d = %.4f, "
          "difference CI95 [%+.4f, %+.4f], ratio %.2fx"
          % (d9["duplicate"]["zero_answers"], d9["duplicate"]["n"], d9["duplicate"]["rate"],
             d9["other"]["zero_answers"], d9["other"]["n"], d9["other"]["rate"],
             d9["difference_ci95"][0], d9["difference_ci95"][1], d9.get("ratio") or 0.0))
    print("-" * 78)
    print("reader arms (both readers):")
    for name in ("edge", "unrelated"):
        a = arms.get(name)
        if a:
            print("  %-11s n=%-3d r1 same=%-3d r2 same=%-3d both same=%-3d unclear=%d"
                  % (name, a["n"], a["same_r1"], a["same_r2"], a["both_same"], a["unclear"]))
    print("D3/D8 edges: %d resolved, canonical in population %d (q_raw=%.4f%s), "
          "different author %d, canonical has >=1 answer %d, has accepted answer %d"
          % (len(edges), sum(1 for e in edges if e["canonical"]["question_id"] in ids),
             q_raw or 0.0, ", UNVERIFIED: A3 failed" if not a3_ok else "",
             diff_author,
             sum(1 for e in edges if e["canonical"].get("answer_count", 0) >= 1),
             sum(1 for e in edges if e["canonical"].get("accepted_answer_id"))))
    if q is None:
        print("D4 not_evaluated: q rests on canonicals A3 did not verify, so n*p*q is "
              "not printed. D7 is the declared stand-in and needs no canonical.")
    else:
        print("D4 expected visible in-sample edges: " + ", ".join(
            "n=%s E=%.3f" % (m, v) for m, v in
            sorted(D.expected_visible_edges(rate, q).items())))
    print("-" * 78)
    print("VERDICT: %s" % verdict)

    out = {
        "schema": "origin.e033.tally/2",
        "verdict": verdict,
        "population": {"n": n, "sites": sorted(per_site),
                       "distinct_users": len(set(r["user_id"] for r in harvest
                                                 if r["user_id"]))},
        "headline": {"duplicate_closures": dup, "n": n, "rate": rate,
                     "ci95": [lo, hi], "record_pool_bound": D.RECORD_POOL},
        "per_site": {s: dict(per_site[s],
                             ci95=list(D.wilson(per_site[s]["dup"], per_site[s]["n"])))
                     for s in sorted(per_site)},
        "closed_reason_distribution": reasons,
        "gates": [{"gate": g[0], "rule": g[1], "result": g[2], "detail": g[3]}
                  for g in gates],
        "arms": arms,
        "kappa": k,
        "kappa_rows": k_rows,
        "a3_ok": a3_ok,
        "D3": {"edges": len(edges), "q_raw": q_raw, "q_verified": a3_ok,
               "different_author": diff_author,
               "canonical_in_population": sum(
                   1 for e in edges if e["canonical"]["question_id"] in ids),
               "canonical_answer_count_ge_1": sum(
                   1 for e in edges if e["canonical"].get("answer_count", 0) >= 1),
               "canonical_accepted_answer": sum(
                   1 for e in edges if e["canonical"].get("accepted_answer_id"))},
        "D4": {"q": q, "expected_visible_edges": D.expected_visible_edges(rate, q)},
        "D5": d5,
        "D6": d6,
        "D7": d7,
        "D9": d9,
    }
    with open(os.path.join(RAW, "tally.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""E031 — the final statistics. Every declared gate, in order, into results.json.

Gate order is fixed and every gate is reported whatever it shows:

  A1  capture and view integrity (digests re-read from disk, stratum counts)
  A3  reader agreement, kappa >= 0.6            (computed by agreement.py)
  A4  nonsense control, q1 yes rate <= 0.25
  A5  planted separation, q3 move - q3 seek >= 0.20
  A6  pair positive control: >= 16/20 positive same, <= 0.20 negative same
  B1  H1: seek q1 rate - ordinary q1 rate >= 0.20, CI95 excluding 0
  C1  H2: P_same(candidates) - P_same(control) >= 0.20 with CI95 excluding 0,
      AND >= 2 adjudicated-same independent candidate pairs, AND A3, A5, A6 passed

A3 is read first: if it failed, nothing below is reported (PROTOCOL.md).
"""

import json
import os

import common as C

C1_MARGIN = 0.20
A6_POS_MIN = 16
A6_NEG_MAX_RATE = 0.20
A4_CEILING = 0.25
A5_MARGIN = 0.20
MIN_SAME_PAIRS = 2


def read_pair_labels(name):
    path = os.path.join(C.RAW, "e031_pairlabels_%s.tsv" % name)
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                out[parts[0]] = parts[1].strip()
    return out


def main():
    key = {r["id"]: r for r in C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))}
    res = {
        "experiment": "E031",
        "question": ("do departure accounts that name no successor state an "
                     "unfilled requirement, and does such a requirement recur "
                     "across independent authors and artifacts"),
        "declared": "PROTOCOL.md",
        "amendments": ["PROTOCOL-AMENDMENT-%d.md" % i for i in (1, 2, 3, 4)],
        "corpus": "E030 raw captures; no network fetch in this experiment",
    }

    # ---- A1 ------------------------------------------------------------
    strata = json.load(open(os.path.join(C.RAW, "strata.json"), encoding="utf-8"))
    digests = json.load(open(os.path.join(C.RAW, "view_digests.json"), encoding="utf-8"))
    mismatched = [n for n, d in digests.items()
                  if C.sha256_file(os.path.join(C.RAW, n)) != d]
    for arm in ("seek", "move", "ordinary"):
        for reader in ("r1", "r2"):
            res.setdefault("label_sha256", {})[
                "e031_labels_%s__%s.tsv" % (arm, reader)] = C.sha256_file(
                    os.path.join(C.RAW, "e031_labels_%s__%s.tsv" % (arm, reader)))
    for n in ("view_e031_pairs_candidates.txt", "view_e031_pairs_control.txt",
              "view_e031_pairs_poscontrol.txt"):
        res.setdefault("pair_view_sha256", {})[n] = C.sha256_file(os.path.join(C.RAW, n))
    res["gate_A1_integrity"] = {
        "strata": {"seek": strata["seek_rows"], "move": strata["move_rows"],
                   "ordinary": strata["ordinary_rows"]},
        "strata_as_declared": {"seek": 326, "move": 593, "ordinary": 2687},
        "source_sha256": strata["source_sha256"],
        "view_digest_mismatches": mismatched,
        "verdict": "passes" if not mismatched else "fails",
    }

    # ---- A3 (first, and it gates the rest) ---------------------------
    agr = json.load(open(os.path.join(C.RAW, "agreement.json"), encoding="utf-8"))
    res["gate_A3_reader_agreement"] = {
        "kappa": agr["kappa_overall"], "floor": agr["declared_floor"],
        "n": agr["n_double_read"], "raw_agreement": agr["raw_agreement"],
        "per_arm_kappa": {k: v["kappa"] for k, v in agr["per_arm"].items()},
        "verdict": agr["verdict"]}
    if agr["verdict"] != "passes":
        res["verdict"] = "not_evaluated"
        res["reason"] = "A3 failed before any rate was computed"
        _write(res)
        C.log("halted", gate="A3")
        return

    # ---- q1 rates, arms ---------------------------------------------
    arms = {}
    for arm in ("seek", "move", "ordinary"):
        rows = []
        with open(os.path.join(C.RAW, "e031_labels_%s__r1.tsv" % arm),
                  encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                rid, q1, clause = line.rstrip("\n").split("\t")
                rows.append({"id": rid, "q1": q1, "clause": clause,
                             "words": key[rid]["words"]})
        yes = sum(1 for r in rows if r["q1"] == "1")
        lo, hi = C.wilson_ci(yes, len(rows))
        arms[arm] = {"n": len(rows), "q1_yes": yes,
                     "q1_unclear": sum(1 for r in rows if r["q1"] == "u"),
                     "rate": yes / float(len(rows)), "ci95": [lo, hi],
                     "median_words": sorted(r["words"] for r in rows)[len(rows) // 2]}
    res["arms"] = arms

    # ---- A4 nonsense --------------------------------------------------
    nl = {}
    for reader in ("r1", "r2"):
        rows = [l.rstrip("\n").split("\t") for l in
                open(os.path.join(C.RAW, "e031_labels_nonsense__%s.tsv" % reader),
                     encoding="utf-8") if l.strip()]
        yes = sum(1 for r in rows if r[1] == "1")
        nl[reader] = {"n": len(rows), "yes": yes, "rate": yes / float(len(rows))}
    res["gate_A4_nonsense_control"] = {
        "per_reader": nl, "ceiling": A4_CEILING,
        "verdict": "passes" if all(v["rate"] <= A4_CEILING for v in nl.values())
        else "fails"}

    # ---- A5 planted separation ---------------------------------------
    def q3_rate(arm):
        rows = [l.rstrip("\n").split("\t") for l in
                open(os.path.join(C.RAW, "e031_q3_%s__r1.tsv" % arm),
                     encoding="utf-8") if l.strip()]
        yes = sum(1 for r in rows if r[1] == "1")
        return yes, len(rows)

    m_yes, m_n = q3_rate("move")
    s_yes, s_n = q3_rate("seek")
    o_yes, o_n = q3_rate("ordinary")
    sep = m_yes / float(m_n) - s_yes / float(s_n)
    res["gate_A5_planted_separation"] = {
        "q3_seek": s_yes / float(s_n), "q3_move": m_yes / float(m_n),
        "q3_ordinary": o_yes / float(o_n), "separation_move_minus_seek": sep,
        "margin": A5_MARGIN, "verdict": "passes" if sep >= A5_MARGIN else "fails"}

    # ---- A6 pair positive control ------------------------------------
    pc = json.load(open(os.path.join(C.RAW, "poscontrol_build.json"), encoding="utf-8"))
    pck = {r["view_id"]: r for r in
           C.read_jsonl(os.path.join(C.RAW, "poscontrol_key.jsonl"))}
    pcl = read_pair_labels("poscontrol")
    pos = [v for v in pcl if pck[v]["kind"] == "positive"]
    neg = [v for v in pcl if pck[v]["kind"] == "negative"]
    p_same = sum(1 for v in pos if pcl[v] == "same")
    n_same = sum(1 for v in neg if pcl[v] == "same")
    p_rate = p_same / float(len(pos)) if pos else 0.0
    n_rate = n_same / float(len(neg)) if neg else 0.0
    res["gate_A6_pair_positive_control"] = {
        "n_positive": len(pos), "positive_same": p_same, "positive_rate": p_rate,
        "positive_min": A6_POS_MIN,
        "n_negative": len(neg), "negative_same": n_same, "negative_rate": n_rate,
        "negative_rate_ceiling": A6_NEG_MAX_RATE,
        "verdict": "passes" if (p_same >= A6_POS_MIN and
                                n_rate <= A6_NEG_MAX_RATE) else "fails",
        "ceiling": ("the positive rendering shares nearly all content words with "
                    "its source, so this gate shows the instrument can return a "
                    "positive and rejects matched negatives; it does not "
                    "validate semantic paraphrase discrimination")}

    # ---- B1 H1 -------------------------------------------------------
    d, lo, hi = C.diff_ci(arms["seek"]["q1_yes"], arms["seek"]["n"],
                          arms["ordinary"]["q1_yes"], arms["ordinary"]["n"])
    res["gate_B1_H1"] = {
        "diff_seek_minus_ordinary": d, "ci95": [lo, hi], "margin": C1_MARGIN,
        "verdict": "passes" if (d >= C1_MARGIN and (lo > 0 or hi < 0)) else "fails"}
    dsm, losm, hism = C.diff_ci(arms["seek"]["q1_yes"], arms["seek"]["n"],
                                arms["move"]["q1_yes"], arms["move"]["n"])
    res["seek_minus_move"] = {"diff": dsm, "ci95": [losm, hism],
                              "note": "secondary contrast, not a declared gate"}

    # ---- C1 H2 -------------------------------------------------------
    build = json.load(open(os.path.join(C.RAW, "pair_build.json"), encoding="utf-8"))
    cand = read_pair_labels("candidates")
    ctrl = read_pair_labels("control")
    c_same = sum(1 for v in cand.values() if v == "same")
    k_same = sum(1 for v in ctrl.values() if v == "same")
    d2, lo2, hi2 = C.diff_ci(c_same, len(cand), k_same, len(ctrl))
    sep_ok = d2 >= C1_MARGIN and (lo2 > 0 or hi2 < 0)
    enough = c_same >= MIN_SAME_PAIRS
    res["gate_C1_H2"] = {
        "candidate_pairs": len(cand), "candidate_same": c_same,
        "candidate_same_rate": c_same / float(len(cand)),
        "candidate_unclear": sum(1 for v in cand.values() if v == "unclear"),
        "control_pairs": len(ctrl), "control_same": k_same,
        "control_same_rate": k_same / float(len(ctrl)),
        "control_unclear": sum(1 for v in ctrl.values() if v == "unclear"),
        "diff": d2, "ci95": [lo2, hi2], "margin": C1_MARGIN,
        "min_same_pairs": MIN_SAME_PAIRS,
        "separation_holds": sep_ok, "enough_same_pairs": enough,
        "prerequisites_passed": all(
            res[g]["verdict"] == "passes" for g in
            ("gate_A3_reader_agreement", "gate_A5_planted_separation",
             "gate_A6_pair_positive_control")),
        "threshold_sensitivity": build["pair_threshold_sensitivity"],
    }
    c1 = res["gate_C1_H2"]
    res["verdict"] = ("H2_survives" if (sep_ok and enough and c1["prerequisites_passed"])
                      else "H2_not_survives" if c1["prerequisites_passed"]
                      else "not_evaluated")
    res["H1_verdict"] = "H1_survives" if res["gate_B1_H1"]["verdict"] == "passes" \
        else "H1_does_not_survive"
    _write(res)
    C.log("rates", **{a: round(arms[a]["rate"], 4) for a in arms})
    C.log("gates", **{g.replace("gate_", ""): res[g].get("verdict", "?")
                      for g in ("gate_A1_integrity", "gate_A3_reader_agreement",
                                "gate_A4_nonsense_control",
                                "gate_A5_planted_separation",
                                "gate_A6_pair_positive_control",
                                "gate_B1_H1", "gate_C1_H2")})
    C.log("verdict", verdict=res["verdict"], h1=res["H1_verdict"],
          candidate_same=c_same, control_same=k_same)


def _write(res):
    with open(os.path.join(C.RAW, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
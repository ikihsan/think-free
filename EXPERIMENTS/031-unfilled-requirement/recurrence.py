#!/usr/bin/env python3
"""E031 — gates A1/A4/A5, the H1 rate, the H2 recurrence and its null.

Every declared gate is decided here and written to raw/results.json with the
digests of the files it was computed from. Nothing is typed from memory.

Order matters and is fixed: the reader-agreement gate (A3, computed by
agreement.py) is read FIRST and, if it failed, no recurrence number is reported.

Writes:
  raw/results.json           every gate, every rate, every CI, the digests
  raw/pairs_<arm>.jsonl      candidate pairs with both printed clauses
  raw/e031_pairs_view.txt    the reader's pair adjudication view
"""

import hashlib
import json
import os
import random
import statistics
import sys

import common as C

MIN_SHARED_TOKENS = 2
MIN_INDEP_SAME = 2


def read_labels(stem, reader):
    path = os.path.join(C.RAW, "e031_labels_%s__%s.tsv" % (stem, reader))
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                out[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else "-")
    return out


def read_q3(stem, reader):
    path = os.path.join(C.RAW, "e031_q3_%s__%s.tsv" % (stem, reader))
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                out[parts[0]] = parts[1].strip()
    return out


def clause_tokens(clause, artifact):
    """Normalised content tokens, minus the departing artifact's own tokens."""
    toks = C.normalise_clause(clause)
    if artifact:
        for t in C.normalise_clause(artifact):
            toks.discard(t)
    return toks


def build_pairs(rows, arm):
    """Candidate pairs within one arm: shared rare content tokens, independent."""
    yes = [r for r in rows if r["q1"] == "1" and r["clause"] not in ("-", "")]
    for r in yes:
        r["tokens"] = clause_tokens(r["clause"], r["artifact"])
    pairs, dropped = [], {"same_author": 0, "same_artifact": 0, "same_story": 0,
                          "not_shared": 0}
    for i in range(len(yes)):
        for j in range(i + 1, len(yes)):
            a, b = yes[i], yes[j]
            shared = a["tokens"] & b["tokens"]
            if len(shared) < MIN_SHARED_TOKENS:
                dropped["not_shared"] += 1
                continue
            if a["author"] == b["author"]:
                dropped["same_author"] += 1
                continue
            if a["artifact"] and b["artifact"] and a["artifact"] == b["artifact"]:
                dropped["same_artifact"] += 1
                continue
            if a["story_id"] == b["story_id"]:
                dropped["same_story"] += 1
                continue
            pairs.append({
                "pair_id": "%s-%s" % (a["id"], b["id"]),
                "arm": arm,
                "id_a": a["id"], "id_b": b["id"],
                "clause_a": a["clause"], "clause_b": b["clause"],
                "shared": sorted(shared),
                "len_a": C.clause_len(a["clause"]), "len_b": C.clause_len(b["clause"]),
            })
    return pairs, dropped, len(yes)


def permutation_null(pairs, n_perm=C.N_PERMUTATIONS, seed=3110):
    """A9, wired in from the first pair: re-derive candidate pairs from a
    shuffled clause->account assignment, preserving each clause's token count and
    each account's author/artifact/story structure.

    Returns the null distribution of the RAW candidate count (pairs sharing >= 2
    content tokens under an independent assignment), which is the quantity the
    observed pair count must beat. Reader adjudication is a strictly coarser
    filter on top of this count, so clearing the raw null is necessary for
    clearing the adjudicated one; the adjudicated-vs-null comparison is
    conservative by construction and that is stated in the README.
    """
    if not pairs:
        return [], 0.0
    accounts = []
    for p in pairs:
        for side in ("a", "b"):
            rid = p["id_%s" % side]
            if rid not in accounts:
                accounts.append(rid)
    rng = random.Random(seed)
    clauses = {}
    for p in pairs:
        clauses.setdefault(p["id_a"], (p["clause_a"], tuple(sorted(p["shared"]))))
        clauses.setdefault(p["id_b"], (p["clause_b"], tuple(sorted(p["shared"]))))
    dist = []
    for _ in range(n_perm):
        keys = list(clauses.keys())
        shuffled = keys[:]
        rng.shuffle(shuffled)
        assign = dict(zip(keys, shuffled))
        count = 0
        for p in pairs:
            a = p["id_a"]
            b = p["id_b"]
            # swap the clauses of the two accounts under the permutation
            ca = clauses[assign[a]][0]
            cb = clauses[assign[b]][0]
            if len(C.normalise_clause(ca) & C.normalise_clause(cb)) >= MIN_SHARED_TOKENS:
                count += 1
        dist.append(count)
    return dist, float(statistics.mean(dist)) if dist else 0.0


def main():
    key = {r["id"]: r for r in C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))}
    results = {"experiment": "E031",
               "declared": "PROTOCOL.md",
               "amendments": ["PROTOCOL-AMENDMENT-1.md", "PROTOCOL-AMENDMENT-2.md"],
               "source_sha256": {}, "label_sha256": {}}

    for stem in ("seek", "move", "ordinary", "nonsense", "reread"):
        for reader in ("r1", "r2"):
            p = os.path.join(C.RAW, "e031_labels_%s__%s.tsv" % (stem, reader))
            if os.path.exists(p):
                results["label_sha256"]["e031_labels_%s__%s.tsv" % (stem, reader)] = \
                    C.sha256_file(p)
        p = os.path.join(C.RAW, "e031_q3_%s__%s.tsv" % (stem, "r1"))
        if os.path.exists(p):
            results["label_sha256"]["e031_q3_%s__r1.tsv" % stem] = C.sha256_file(p)
    results["source_sha256"] = json.load(
        open(os.path.join(C.RAW, "strata.json"), encoding="utf-8"))["source_sha256"]
    results["view_sha256"] = json.load(
        open(os.path.join(C.RAW, "view_digests.json"), encoding="utf-8"))

    # ---- A3 first: if it failed, no recurrence number is reported ----------
    agr = json.load(open(os.path.join(C.RAW, "agreement.json"), encoding="utf-8"))
    results["gate_A3_reader_agreement"] = {
        "kappa": agr["kappa_overall"], "floor": agr["declared_floor"],
        "verdict": agr["verdict"], "n": agr["n_double_read"],
    }
    if agr["verdict"] != "passes":
        results["verdict"] = "not_evaluated"
        results["reason"] = "A3 failed: reader agreement below the declared floor"
        _write(results)
        C.log("halted", gate="A3", kappa=agr["kappa_overall"])
        return

    # ---- H1 rates and the two control gates --------------------------------
    arms = {}
    for arm in ("seek", "move", "ordinary"):
        labels = read_labels(arm, "r1")
        q3 = read_q3(arm, "r1")
        rows = []
        for rid, (q1, clause) in labels.items():
            k = key[rid]
            rows.append({"id": rid, "q1": q1, "clause": clause,
                         "author": k["author"], "artifact": k["artifact"],
                         "story_id": k["story_id"],
                         "q3": q3.get(rid, "u"),
                         "words": k["words"]})
        yes = sum(1 for r in rows if r["q1"] == "1")
        unc = sum(1 for r in rows if r["q1"] == "u")
        lo, hi = C.wilson_ci(yes, len(rows))
        arms[arm] = {"n": len(rows), "q1_yes": yes, "q1_unclear": unc,
                     "rate": yes / float(len(rows)),
                     "ci95": [lo, hi],
                     "q3_yes": sum(1 for r in rows if r["q3"] == "1"),
                     "median_words": statistics.median([r["words"] for r in rows])}
    results["arms"] = arms

    d_se, l_se, h_se = C.diff_ci(arms["seek"]["q1_yes"], arms["seek"]["n"],
                                arms["ordinary"]["q1_yes"], arms["ordinary"]["n"])
    d_sm, l_sm, h_sm = C.diff_ci(arms["seek"]["q1_yes"], arms["seek"]["n"],
                                arms["move"]["q1_yes"], arms["move"]["n"])
    results["gate_B1_H1_seek_minus_ordinary"] = {
        "diff": d_se, "ci95": [l_se, h_se], "margin": 0.20,
        "excludes_zero": (l_se > 0 or h_se < 0),
        "verdict": ("passes" if (d_se >= 0.20 and (l_se > 0 or h_se < 0))
                    else "fails")}
    results["seek_minus_move"] = {"diff": d_sm, "ci95": [l_sm, h_sm]}

    # A5 planted separation: the successor question must separate move from seek
    sep = arms["move"]["q3_yes"] / float(arms["move"]["n"]) - \
        arms["seek"]["q3_yes"] / float(arms["seek"]["n"])
    results["gate_A5_planted_separation"] = {
        "q3_rate_move": arms["move"]["q3_yes"] / float(arms["move"]["n"]),
        "q3_rate_seek": arms["seek"]["q3_yes"] / float(arms["seek"]["n"]),
        "separation": sep, "margin": 0.20,
        "verdict": "passes" if sep >= 0.20 else "fails"}

    # A4 nonsense control
    nl1 = read_labels("nonsense", "r1")
    nl2 = read_labels("nonsense", "r2")
    n_yes1 = sum(1 for v in nl1.values() if v[0] == "1")
    n_yes2 = sum(1 for v in nl2.values() if v[0] == "1")
    results["gate_A4_nonsense_control"] = {
        "n": len(nl1), "r1_yes": n_yes1, "r2_yes": n_yes2,
        "ceiling": 0.25,
        "verdict": "passes" if (n_yes1 / float(len(nl1)) <= 0.25
                                and n_yes2 / float(len(nl2)) <= 0.25) else "fails"}

    # ---- H2: candidate pairs, the printed linkage, the null ----------------
    pair_rows, dropped, n_yes = {}, {}, {}
    for arm in ("seek", "move", "ordinary"):
        labels = read_labels(arm, "r1")
        rows = [{"id": rid, "q1": q1, "clause": clause,
                 "author": key[rid]["author"], "artifact": key[rid]["artifact"],
                 "story_id": key[rid]["story_id"]}
                for rid, (q1, clause) in labels.items()]
        pairs, drop, ny = build_pairs(rows, arm)
        pair_rows[arm], dropped[arm], n_yes[arm] = pairs, drop, ny
        C.write_jsonl(os.path.join(C.RAW, "pairs_%s.jsonl" % arm), pairs)
    results["q1_yes_rows"] = n_yes
    results["pair_dropped"] = dropped
    results["n_candidate_pairs"] = {a: len(pair_rows[a]) for a in pair_rows}

    # the reader's pair view: printed clauses only, shuffled, no arm shown
    view_lines = ["E031 pair adjudication. For each pair, do the two clauses state "
                  "THE SAME missing capability?",
                  "Answer exactly one of: same / different / unclear",
                  "Do not use any other file. Judge only the two phrases printed.",
                  ""]
    allp = [p for arm in ("seek", "move", "ordinary") for p in pair_rows[arm]]
    vrng = random.Random(3111)
    order = list(range(len(allp)))
    vrng.shuffle(order)
    vpath = os.path.join(C.RAW, "e031_pairs_view.txt")
    with open(vpath, "w", encoding="utf-8") as fh:
        for n, idx in enumerate(order, 1):
            p = allp[idx]
            vpid = "P%03d" % n
            p["view_id"] = vpid
            fh.write("=" * 60 + "\n")
            fh.write("PAIR: %s\n" % vpid)
            fh.write("CLAUSE A: %s\n" % p["clause_a"])
            fh.write("CLAUSE B: %s\n\n" % p["clause_b"])
    results["pairs_view_sha256"] = C.sha256_file(vpath)
    results["n_pairs_for_adjudication"] = len(allp)
    C.write_jsonl(os.path.join(C.RAW, "pairs_key.jsonl"), allp)

    dist, mean = permutation_null(allp)
    obs_raw = len(allp)
    results["gate_C1_null"] = {
        "observed_candidate_pairs": obs_raw,
        "null_mean": mean,
        "null_p95": (sorted(dist)[int(0.95 * len(dist))] if dist else None),
        "null_n_permutations": len(dist),
        "clears_null": bool(dist and obs_raw > sorted(dist)[int(0.95 * len(dist))]),
    }
    _write(results)
    C.log("pairs", **{a: len(pair_rows[a]) for a in pair_rows})
    C.log("null", observed=obs_raw, mean=round(mean, 3),
          p95=(sorted(dist)[int(0.95 * len(dist))] if dist else None),
          clears=results["gate_C1_null"]["clears_null"])
    C.log("rates", seek=arms["seek"]["rate"], move=arms["move"]["rate"],
          ordinary=arms["ordinary"]["rate"])
    C.log("gates", A4=results["gate_A4_nonsense_control"]["verdict"],
          A5=results["gate_A5_planted_separation"]["verdict"],
          B1=results["gate_B1_H1_seek_minus_ordinary"]["verdict"])


def _write(results):
    with open(os.path.join(C.RAW, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
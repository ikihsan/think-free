#!/usr/bin/env python3
"""E031 — build the candidate and control pair views for reader adjudication.

Per PROTOCOL-AMENDMENT-3.md: lexical overlap only SELECTS candidates; the
reader's answer to q4 decides sameness. Two pair sets of equal size:

  candidate  >= 1 shared content token, plus the author/artifact/story filters
  control    the same three arms, the same filters, no token requirement

Both are drawn by fixed seeds and no pair appears in both sets. The view prints
the two clauses and nothing else — no arm, no author, no story, no artifact.

Writes raw/view_e031_pairs_candidates.txt, raw/view_e031_pairs_control.txt,
       raw/pairs_candidates.jsonl, raw/pairs_control.jsonl,
       raw/pairs_key.jsonl, raw/pair_build.json
"""

import json
import os
import random

import common as C

MIN_SHARED_TOKENS = 1
SEED_CANDIDATES = 3121
SEED_CONTROL = 3122


def clauses_by_arm():
    key = {r["id"]: r for r in C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))}
    out = {}
    for arm in ("seek", "move", "ordinary"):
        rows = []
        with open(os.path.join(C.RAW, "e031_labels_%s__r1.tsv" % arm),
                  encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                rid, q1, clause = line.rstrip("\n").split("\t")
                if q1 != "1" or clause.strip() in ("-", ""):
                    continue
                k = key[rid]
                toks = C.normalise_clause(clause)
                if k["artifact"]:
                    toks = toks - C.normalise_clause(k["artifact"])
                rows.append({"id": rid, "arm": arm, "clause": clause,
                             "author": k["author"], "artifact": k["artifact"],
                             "story_id": k["story_id"], "tokens": toks})
        out[arm] = rows
    return out, key


def independent(a, b):
    if a["author"] == b["author"]:
        return False, "same_author"
    if a["artifact"] and b["artifact"] and a["artifact"] == b["artifact"]:
        return False, "same_artifact"
    if a["story_id"] == b["story_id"]:
        return False, "same_story"
    return True, "independent"


def main():
    arms, key = clauses_by_arm()
    allrows = [r for arm in arms for r in arms[arm]]
    n_clauses = len(allrows)

    dropped = {"same_author": 0, "same_artifact": 0, "same_story": 0}
    cands = []
    for i in range(n_clauses):
        for j in range(i + 1, n_clauses):
            a, b = allrows[i], allrows[j]
            ok, why = independent(a, b)
            if not ok:
                dropped[why] += 1
                continue
            shared = sorted(a["tokens"] & b["tokens"])
            if len(shared) >= MIN_SHARED_TOKENS:
                cands.append({"pair_id": "%s|%s" % (a["id"], b["id"]),
                              "kind": "candidate", "shared": shared,
                              "id_a": a["id"], "id_b": b["id"],
                              "clause_a": a["clause"], "clause_b": b["clause"]})

    # control: every independent pair, minus the candidates, sampled to the same size
    ckeys = set(c["pair_id"] for c in cands)
    pool = []
    for i in range(n_clauses):
        for j in range(i + 1, n_clauses):
            a, b = allrows[i], allrows[j]
            ok, _ = independent(a, b)
            if not ok:
                continue
            pid = "%s|%s" % (a["id"], b["id"])
            if pid in ckeys:
                continue
            pool.append({"pair_id": pid, "kind": "control", "shared": [],
                         "id_a": a["id"], "id_b": b["id"],
                         "clause_a": a["clause"], "clause_b": b["clause"]})
    rng = random.Random(SEED_CONTROL)
    ctrl = rng.sample(pool, min(len(cands), len(pool)))

    rng2 = random.Random(SEED_CANDIDATES)
    order = list(range(len(cands)))
    rng2.shuffle(order)
    cands = [cands[i] for i in order]

    digests = {}
    for name, pairs, prefix in (("candidates", cands, "K"),
                                ("control", ctrl, "N")):
        lines = ["E031 pair adjudication. For each pair, do the two clauses state "
                 "THE SAME missing capability?",
                 "Answer exactly one of: same / different / unclear",
                 "Use only the two phrases printed. Judge nothing else.",
                 ""]
        for n, p in enumerate(pairs, 1):
            p["view_id"] = "%s%03d" % (prefix, n)
            lines.append("=" * 60)
            lines.append("PAIR: %s" % p["view_id"])
            lines.append("CLAUSE A: %s" % p["clause_a"])
            lines.append("CLAUSE B: %s" % p["clause_b"])
            lines.append("")
        body = "\n".join(lines)
        path = os.path.join(C.RAW, "view_e031_pairs_%s.txt" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        digests["view_e031_pairs_%s.txt" % name] = C.sha256_bytes(body)
        C.write_jsonl(os.path.join(C.RAW, "pairs_%s.jsonl" % name), pairs)

    C.write_jsonl(os.path.join(C.RAW, "pairs_key.jsonl"), cands + ctrl)

    # threshold sensitivity, for the README's declared report
    sweep = {}
    for th in (1, 2, 3):
        n = 0
        for i in range(n_clauses):
            for j in range(i + 1, n_clauses):
                a, b = allrows[i], allrows[j]
                ok, _ = independent(a, b)
                if not ok:
                    continue
                if len(a["tokens"] & b["tokens"]) >= th:
                    n += 1
        sweep["ge_%d" % th] = n

    info = {"n_clauses": n_clauses, "min_shared_tokens": MIN_SHARED_TOKENS,
            "n_candidates": len(cands), "n_control": len(ctrl),
            "n_control_pool": len(pool), "dropped": dropped,
            "seed_candidates": SEED_CANDIDATES, "seed_control": SEED_CONTROL,
            "view_sha256": digests,
            "pair_threshold_sensitivity": sweep}
    with open(os.path.join(C.RAW, "pair_build.json"), "w", encoding="utf-8") as fh:
        json.dump(info, fh, indent=2, sort_keys=True)
        fh.write("\n")
    C.log("pairs_built", candidates=len(cands), control=len(ctrl),
          pool=len(pool), sweep=sweep)


if __name__ == "__main__":
    main()
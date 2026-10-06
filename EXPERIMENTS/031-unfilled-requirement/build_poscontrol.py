#!/usr/bin/env python3
"""E031 gate A6 — build the pair instrument's positive and matched-negative control.

Declared in PROTOCOL-AMENDMENT-4.md. 20 positive pairs, each a clause paired with
a deterministic paraphrase of itself (no shared wording beyond the tail), and 20
matched negatives drawn from the same pool at the same clause-length band, across
different stories, authors and artifacts.

Writes raw/view_e031_pairs_poscontrol.txt, raw/poscontrol_key.jsonl,
       raw/poscontrol_build.json
"""

import json
import os
import random
import statistics

import common as C

SEED = 3123
N_PAIRS = 20
MIN_WORDS = 6


def paraphrase(clause, artifact):
    """Declared transform: drop leading stopwords and the artifact's tokens, then
    prepend 'no way to'. Deterministic; produces a second phrasing of the same
    capability without reusing the original's opening wording."""
    text = C.clean(clause).strip().rstrip(".")
    toks = text.split()
    art = set(C.normalise_clause(artifact)) if artifact else set()
    out = []
    for t in toks:
        low = t.lower().strip(".,;:!?()\"'")
        if low in C.STOPWORDS:
            continue
        if low in art:
            continue
        out.append(t)
    body = " ".join(out).strip()
    if not body:
        return None
    return "no way to " + body[0].lower() + body[1:]


def main():
    key = {r["id"]: r for r in C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))}
    pool = []
    for arm in ("seek", "move", "ordinary"):
        with open(os.path.join(C.RAW, "e031_labels_%s__r1.tsv" % arm),
                  encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                rid, q1, clause = line.rstrip("\n").split("\t")
                if q1 != "1" or clause.strip() in ("-", ""):
                    continue
                if C.clause_len(clause) < MIN_WORDS:
                    continue
                pool.append({"id": rid, "arm": arm, "clause": clause,
                             "author": key[rid]["author"],
                             "artifact": key[rid]["artifact"],
                             "story_id": key[rid]["story_id"]})
    rng = random.Random(SEED)
    chosen = rng.sample(pool, N_PAIRS * 2)
    pos_src = chosen[:N_PAIRS]
    neg_src = chosen[N_PAIRS:]

    positives, skipped = [], []
    for r in pos_src:
        p = paraphrase(r["clause"], r["artifact"])
        if p is None:
            skipped.append(r["id"])
            continue
        positives.append({"kind": "positive", "id_a": r["id"], "id_b": r["id"],
                          "clause_a": r["clause"], "clause_b": p})

    # matched negatives: different story, author and artifact, same length band
    band = statistics.median([C.clause_len(r["clause"]) for r in neg_src])
    lo, hi = max(3, band - 3), band + 3
    by_id = {r["id"]: r for r in pool}
    negatives = []
    for a in neg_src:
        if C.clause_len(a["clause"]) < lo or C.clause_len(a["clause"]) > hi:
            continue
        cands = [b for b in pool
                 if b["id"] != a["id"] and b["story_id"] != a["story_id"]
                 and b["author"] != a["author"]
                 and (not a["artifact"] or not b["artifact"]
                      or a["artifact"] != b["artifact"])
                 and lo <= C.clause_len(b["clause"]) <= hi]
        if not cands:
            continue
        b = rng.choice(sorted(cands, key=lambda r: r["id"]))
        negatives.append({"kind": "negative", "id_a": a["id"], "id_b": b["id"],
                          "clause_a": a["clause"], "clause_b": b["clause"]})

    pairs = positives + negatives
    order = list(range(len(pairs)))
    random.Random(SEED + 1).shuffle(order)
    pairs = [pairs[i] for i in order]

    lines = ["E031 pair adjudication. For each pair, do the two clauses state "
             "THE SAME missing capability?",
             "Answer exactly one of: same / different / unclear",
             "Use only the two phrases printed. Judge nothing else.",
             ""]
    for n, p in enumerate(pairs, 1):
        p["view_id"] = "P%03d" % n
        lines += ["=" * 60, "PAIR: %s" % p["view_id"],
                  "CLAUSE A: %s" % p["clause_a"],
                  "CLAUSE B: %s" % p["clause_b"], ""]
    body = "\n".join(lines)
    path = os.path.join(C.RAW, "view_e031_pairs_poscontrol.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    C.write_jsonl(os.path.join(C.RAW, "poscontrol_key.jsonl"), pairs)

    info = {"seed": SEED, "n_positive": len(positives),
            "n_negative": len(negatives), "skipped_paraphrase": skipped,
            "negatives_length_band": [lo, hi],
            "view_sha256": C.sha256_bytes(body),
            "thresholds": {"positive_same_at_least": 16,
                           "negative_same_at_most": 4}}
    with open(os.path.join(C.RAW, "poscontrol_build.json"), "w", encoding="utf-8") as fh:
        json.dump(info, fh, indent=2, sort_keys=True)
        fh.write("\n")
    C.log("poscontrol_built", positive=len(positives), negative=len(negatives),
          band=[lo, hi], skipped=len(skipped))


if __name__ == "__main__":
    main()
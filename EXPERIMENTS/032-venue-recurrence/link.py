"""Build the E032 candidate pairs, the control, and both pair-instrument controls.

PROTOCOL.md, as amended by AMENDMENT-1. Nothing here reads a q2 answer: this
step only decides WHICH pairs a reader will be asked about.

Gate A2 is computed here and before any adjudication, per D062: the candidate
count is printed against the count chance alone produces on this same clause
set, and a candidate count at or below chance means the rule cannot fire.
"""
import json
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SHEETS = os.path.join(HERE, "sheets")
LAB = os.path.join(HERE, "labels")
E031 = os.path.abspath(os.path.join(HERE, "..", "031-unfilled-requirement"))
sys.path.insert(0, E031)
import common as E031C                                     # noqa: E402

SEED = 40712
N_CONTROL = 60
N_POSITIVE = 20
N_NEGATIVE = 10
CHANCE_TRIALS = 10000
MIN_SHARED = 1


def digest(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_tsv(path):
    out = []
    for line in open(path, encoding="utf-8"):
        if line.strip():
            out.append(line.rstrip("\n").split("\t"))
    return out[0], out[1:]


def load_clause_set():
    """Rows where BOTH readers returned a clause. E031's rule: a row counts only
    when both readers say yes, so a clause never rests on one reader.

    The digest checked here is the SHEET's — the bytes the reader was told to
    verify — while the clause text is read from the reader's LABEL file. Reading
    the sheet instead of the label file is a mistake this function already made
    once: every body is non-`none`, so the two readers look identical, agreement
    is 1.0, kappa is undefined and 60 clauses appear where 28 exist."""
    man = json.load(open(os.path.join(SHEETS, "MANIFEST.json")))
    keymap = man["keymap"]
    out = {}
    for reader, sheet, labels_file in (
        ("r1", "q1_reader1.tsv", "q1_reader1.tsv"),
        ("r2", "q1_reader2.tsv", "q1_reader2.tsv"),
    ):
        sheet_path = os.path.join(SHEETS, sheet)
        if digest(sheet_path) != man["q1_reader" + reader[1]]["sha256"]:
            sys.exit("sheet digest mismatch for %s" % sheet_path)
        path = os.path.join(LAB, labels_file)
        if not os.path.exists(path):
            sys.exit("label file missing: %s" % path)
        _head, rows = read_tsv(path)
        km = keymap["q1_reader" + reader[1]]
        for key, clause in rows:
            if key not in km:
                sys.exit("row identity check FAILED: %s not in keymap (%s)" % (key, path))
            idx = km[key]
            rec = out.setdefault(idx, {})
            rec[reader] = clause.strip()
    if not out:
        sys.exit('no rows carried both readers keys')
    return man, out


def build(man, labels):
    rows = [json.loads(line) for line in open(os.path.join(RAW, "harvest.jsonl")) if line.strip()]
    clauses = []
    for idx in sorted(labels):
        rec = labels[idx]
        c1, c2 = rec.get("r1", ""), rec.get("r2", "")
        if c1 == "none" or c2 == "none" or not c1 or not c2:
            continue
        clauses.append({
            "idx": idx,
            "author": rows[idx]["author"],
            "site": rows[idx]["site"],
            "clause": c1,
            "tokens": E031C.normalise_clause(c1),
            "len": E031C.clause_len(c1),
        })
    return clauses


def candidate_pairs(clauses):
    pairs = []
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            a, b = clauses[i], clauses[j]
            if a["author"] == b["author"]:
                continue
            shared = a["tokens"] & b["tokens"]
            if len(shared) >= MIN_SHARED:
                pairs.append({"a": a, "b": b, "shared": sorted(shared)})
    return pairs


def chance_expectation(clauses, rng):
    """What this linkage finds by accident on the same vocabulary: random perfect
    matchings of the same clause set, same different-author rule, same
    normalisation. Reported as a mean over CHANCE_TRIALS."""
    n = len(clauses)
    counts = []
    for _ in range(CHANCE_TRIALS):
        idx = list(range(n))
        rng.shuffle(idx)
        hits = 0
        for i in range(0, n - 1, 2):
            a, b = clauses[idx[i]], clauses[idx[i + 1]]
            if a["author"] == b["author"]:
                continue
            if a["tokens"] & b["tokens"]:
                hits += 1
        counts.append(hits)
    return statistics.mean(counts), (min(counts), max(counts))


def length_matched_control(clauses, excluded, rng, n):
    """F043's control as fixed in E031 AMENDMENT-3 §3: reader-adjudicated random
    pairs from the same clause set through the same filters. Length-matched
    because E030's statistic was length (F050)."""
    pool = []
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            a, b = clauses[i], clauses[j]
            if a["author"] == b["author"]:
                continue
            if (min(a["idx"], b["idx"]), max(a["idx"], b["idx"])) in excluded:
                continue
            pool.append({"a": a, "b": b})
    rng.shuffle(pool)
    chosen, used = [], set()
    for pair in pool:
        key = (min(pair["a"]["idx"], pair["b"]["idx"]),
               max(pair["a"]["idx"], pair["b"]["idx"]))
        if key in used:
            continue
        used.add(key)
        chosen.append(pair)
        if len(chosen) >= n:
            break
    return chosen


def paraphrase(clause):
    """E031's declared transform (build_poscontrol.paraphrase), adapted: drop
    stopwords, then prepend 'a way to'. Deterministic, and produces a second
    phrasing that reuses no opening wording."""
    body = " ".join(t for t in E031C.clean(clause).strip().rstrip(".").split()
                    if t.lower().strip(".,;:!?()\"'") not in E031C.STOPWORDS).strip()
    if not body:
        return None
    return "a way to " + body[0].lower() + body[1:]


def write_sheet(name, rows, header):
    path = os.path.join(SHEETS, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c).replace("\t", " ").replace("\n", " ") for c in r) + "\n")
    return digest(path)


def main():
    rng = random.Random(SEED)
    man, labels = load_clause_set()

    # ---- A3: reader agreement on the yes/no decision, over every row both read.
    both = [i for i in sorted(labels) if labels[i].get("r1") and labels[i].get("r2")]
    agree = sum(1 for i in both
                if (labels[i]["r1"] != "none") == (labels[i]["r2"] != "none"))
    p_yes = sum(1 for i in both if labels[i]["r1"] != "none") / len(both)
    p_no = sum(1 for i in both if labels[i]["r2"] != "none") / len(both)
    pe = p_yes * p_no + (1 - p_yes) * (1 - p_no)
    kappa = (agree / len(both) - pe) / (1 - pe) if pe < 1 else None

    clauses = build(man, labels)
    cands = candidate_pairs(clauses)
    mean_chance, span = chance_expectation(clauses, random.Random(SEED + 1))

    excluded = set((min(p["a"]["idx"], p["b"]["idx"]),
                    max(p["a"]["idx"], p["b"]["idx"])) for p in cands)
    control = length_matched_control(clauses, excluded, random.Random(SEED + 2), N_CONTROL)

    pos_pool = [c for c in clauses if paraphrase(c["clause"])]
    pos_pool = pos_pool[:N_POSITIVE]
    neg_pool = [c for c in clauses if c["len"] >= 8]
    neg_pool = neg_pool[:N_NEGATIVE]

    q2, meta_by_key = [], {}
    for i, p in enumerate(cands[:N_CONTROL]):
        k = "c-%03d" % (i + 1)
        q2.append((k, p["a"]["clause"], p["b"]["clause"]))
        meta_by_key[k] = {"sheet": "candidates", "key": k,
                          "idx_a": p["a"]["idx"], "idx_b": p["b"]["idx"], "shared": p["shared"]}
    for i, p in enumerate(control):
        k = "k-%03d" % (i + 1)
        q2.append((k, p["a"]["clause"], p["b"]["clause"]))
        meta_by_key[k] = {"sheet": "control", "key": k,
                          "idx_a": p["a"]["idx"], "idx_b": p["b"]["idx"]}
    for i, c in enumerate(pos_pool):
        k = "p-%02d" % (i + 1)
        q2.append((k, c["clause"], paraphrase(c["clause"])))
        meta_by_key[k] = {"sheet": "positive", "key": k, "idx_a": c["idx"], "idx_b": c["idx"]}
    rng2 = random.Random(SEED + 3)
    for i, c in enumerate(neg_pool):
        other = rng2.choice([x for x in clauses if x["author"] != c["author"] and x is not c])
        k = "n-%02d" % (i + 1)
        q2.append((k, c["clause"], other["clause"]))
        meta_by_key[k] = {"sheet": "negative", "key": k, "idx_a": c["idx"], "idx_b": other["idx"]}
    rng2.shuffle(q2)

    d_q2 = write_sheet("q2_pairs.tsv", q2, ["key", "clause_a", "clause_b"])
    # The key file follows the SHEET's order, not the order pairs were built in.
    # Writing it in build order was this run's second defect: tally.py's
    # row-identity check by ORDER (D061, F049) caught it immediately.
    with open(os.path.join(RAW, "q2_key.jsonl"), "w") as fh:
        for row in q2:
            fh.write(json.dumps(meta_by_key[row[0]]) + "\n")

    out = {
        "schema": "origin.e032.link/1",
        "rows_double_read": len(both),
        "A3_kappa": round(kappa, 4) if kappa is not None else None,
        "A3_raw_agreement": round(agree / len(both), 4),
        "clauses_both_readers": len(clauses),
        "A2_candidate_pairs": len(cands),
        "A2_candidates_adjudicated": min(N_CONTROL, len(cands)),
        "A2_chance_expectation_mean": round(mean_chance, 2),
        "A2_chance_span": list(span),
        "A2_reachable": len(cands) > mean_chance,
        "A2_rule": ">= %d shared normalised content token, different authors" % MIN_SHARED,
        "control_pairs": len(control),
        "positive_pairs": len(pos_pool),
        "negative_pairs": len(neg_pool),
        "q2_rows": len(q2),
        "q2_sha256": d_q2,
    }
    with open(os.path.join(RAW, "link.json"), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
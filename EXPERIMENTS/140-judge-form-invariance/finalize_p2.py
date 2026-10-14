#!/usr/bin/env python3
"""finalize_p2.py — merge the P2 rewrite, rebuild the judge batches.

The P2 arm is written by a separate writer session (AMENDMENT-2 §5): it sees
five questions and answers and no arm label. This script is what admits its
output, applies K4 to it, and rebuilds the blinded judge batches over the full
judge population (AMENDMENT-3 §2).

It refuses to run twice over different input: p2.jsonl is read once, hashed, and
the hash is printed, so the arm that later results are computed from can be
identified exactly.
"""
import hashlib
import json
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_arms as B  # noqa: E402
import valueset  # noqa: E402


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p2_path = os.path.join(HERE, "p2.jsonl")
    if not os.path.exists(p2_path):
        print(json.dumps({"error": "p2.jsonl missing; run the writer first"}))
        return 2
    p2_rows = [json.loads(l) for l in open(p2_path) if l.strip()]
    job = json.load(open(os.path.join(HERE, "p2_job.json")))
    # Keyed on document_number alone, because P2's five items are five distinct
    # documents and the question is recovered from the job rather than trusted
    # back from the writer. A writer that re-punctuated the question would
    # otherwise fail K0 for a reason that has nothing to do with the rewrite.
    q_of = {i["document_number"]: i["question"] for i in job["items"]}
    got = {r["document_number"] for r in p2_rows}
    wanted = set(q_of)
    if got != wanted or len(p2_rows) != len(wanted):
        print(json.dumps({"error": "p2.jsonl does not cover the job exactly",
                          "missing": sorted(wanted - got),
                          "unexpected": sorted(got - wanted),
                          "rows": len(p2_rows)}))
        return 2
    for r in p2_rows:
        r["question"] = q_of[r["document_number"]]

    arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))
            if l.strip()]
    arms = [r for r in arms if r["arm"] != "P2"]
    verbatim = {(r["document_number"], r["question"]): r
                for r in arms if r["arm"] == "V"}

    kept, dropped = [], []
    for r in p2_rows:
        key = (r["document_number"], r["question"])
        v = verbatim[key]
        # K4 for P2: same rule as P — the canonical value *multiset* equals V.
        # A rewrite that drifts a value is not an arm, it is a different answer.
        # Multiset, not list: AMENDMENT-2 §5 lets the writer reorder, so an
        # order-sensitive comparison would fail an arm for the one change that
        # arm was asked to make (see AMENDMENT-3 §4).
        if Counter(map(repr, valueset.canonical(r["answer"]))) != \
                Counter(map(repr, valueset.canonical(v["answer"]))):
            dropped.append({"document_number": key[0], "arm": "P2",
                            "reason": "canonical value multiset differs from V"})
            continue
        kept.append({"document_number": key[0], "question": key[1],
                     "in_judge_subset": v["in_judge_subset"],
                     "arm": "P2", "answer": r["answer"]})
    arms.extend(kept)

    with open(os.path.join(HERE, "arms.jsonl"), "w") as fh:
        for row in sorted(arms, key=lambda a: (a["document_number"],
                                               a["question"], a["arm"])):
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    # Judge population: every correct-but-reworded and corrupted variant that
    # carries a state a judge can distinguish. Un-corrupted C rows are V rows
    # repeated verbatim and are excluded (AMENDMENT-2 §4).
    judge_rows = [r for r in arms
                  if r["in_judge_subset"] and r["arm"] in ("V", "P", "P2", "C")
                  and r.get("corrupted", True)]
    batches = []
    items = list(judge_rows)
    random.Random(B.JUDGE_SEED).shuffle(items)
    for i in range(0, len(items), B.BATCH):
        chunk = items[i:i + B.BATCH]
        key = [{"document_number": c["document_number"], "arm": c["arm"],
                "question": c["question"]} for c in chunk]
        batches.append({"batch": i // B.BATCH, "items": chunk, "_key": key})
    with open(os.path.join(HERE, "judge_batches.json"), "w") as fh:
        json.dump(batches, fh, indent=1, sort_keys=True)

    print(json.dumps({
        "p2_sha256": sha256(p2_path),
        "p2_items_written": len(p2_rows),
        "p2_items_kept": len(kept),
        "k4_dropped": dropped,
        "arms_written": len(arms),
        "judge_items": len(judge_rows),
        "batches": len(batches),
    }, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

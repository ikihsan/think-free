#!/usr/bin/env python3
"""E126 screening: apply the hand-read classifications to the sheet.

The map in screening-map.json was produced by reading
screening-sheet.txt row by row (title + body only, no answer or
comment read) and classifying each row per PROTOCOL.md's taxonomy:

  question/answerable  remedy is an explanation or snippet; general
                       knowledge suffices
  question/specific    remedy requires the asker's logs, versions or
                       environment, which the post does not contain
  execution/program    remedy is a self-contained program the asker
                       runs (E091's K2 shape)
  execution/manual     remedy is an action needing the asker's
                       judgment or direct system access
  other                meta, opinion, off-topic, purchase, challenge

Dedupes by question_id (the API returned one question on both pages
of Arm A) and emits screening.jsonl plus the per-arm tallies that
gate.py reads.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    sheet = json.load(open(os.path.join(HERE, "screening-sheet.json")))
    mapping = json.load(open(os.path.join(HERE, "screening-map.json")))
    assert len(sheet) == 300, len(sheet)
    assert len(mapping) == 299, len(mapping)  # row 35 is the duplicate

    seen = {}
    rows = []
    for n, r in enumerate(sheet, 1):
        qid = r["question_id"]
        if qid in seen:
            rows.append({**r, "sheet_row": n,
                         "shape": "duplicate", "sub": "",
                         "dropped": True,
                         "duplicate_of": seen[qid]})
            continue
        seen[qid] = n
        shape, sub = mapping[str(n)]
        rows.append({**r, "sheet_row": n, "shape": shape,
                     "sub": sub, "dropped": False})

    with open(os.path.join(HERE, "screening.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    # per-arm tallies over non-duplicate rows
    tally = {}
    for arm in ("A_votes", "B_creation"):
        pool = [r for r in rows
                if r["arm"] == arm and not r["dropped"]]
        t = {"n": len(pool), "question": 0, "execution": 0,
             "other": 0, "answerable": 0, "specific": 0,
             "program": 0, "manual": 0}
        for r in pool:
            t[r["shape"]] = t.get(r["shape"], 0) + 1
            if r["shape"] == "question":
                t[r["sub"]] += 1
            elif r["shape"] == "execution":
                t[r["sub"]] += 1
        tally[arm] = t

    pooled = {"n": sum(t["n"] for t in tally.values())}
    for key in ("question", "execution", "other", "answerable",
                "specific", "program", "manual"):
        pooled[key] = sum(t.get(key, 0) for t in tally.values())

    out = {"tally": tally, "pooled": pooled,
           "duplicate_question_ids": sorted(
               {r["question_id"] for r in rows if r["dropped"]})}
    with open(os.path.join(HERE, "screening-summary.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

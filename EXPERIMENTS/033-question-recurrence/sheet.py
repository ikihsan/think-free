"""E033 — build the blinded 48-row reader sheet.

PROTOCOL.md section 7. One sheet, two arms, one order:

  24 `edge` rows      a resolved duplicate and the API's top-ranked related row
  24 `unrelated` rows pairs from DIFFERENT sites, matched on title length

The sheet is shuffled with a seed recorded in the manifest, hashed, and handed to
every reader with its sha256. The key file is written in the sheet's order, so
tally.py can check row identity by ORDER rather than by key set (D061, from F049).
The reader never sees which arm a row belongs to, nor the site, author or score.
"""
import hashlib
import json
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SHEETS = os.path.join(HERE, "sheets")
MANIFEST = os.path.join(SHEETS, "MANIFEST.json")

SEED = 20261006
EDGE_PER_SITE = 12          # 24 edge rows total
UNRELATED = 24
WORDS = 45                 # body excerpt length, in words
SITES = ["travel", "math"]
TAG = re.compile(r"<[^>]+>")


def excerpt(text, n=WORDS):
    """Tabs and newlines are stripped: the sheet is TSV, and an embedded tab would
    make the row's column count wrong and defeat the reader's own field parsing."""
    words = re.sub(r"\s+", " ", text or "").split()
    return " ".join(words[:n]) + (" ..." if len(words) > n else "")


def title_len(title):
    return len(title.split())


def main():
    os.makedirs(SHEETS, exist_ok=True)
    edges = [json.loads(l) for l in open(os.path.join(RAW, "edges.jsonl")) if l.strip()]
    harvest = [json.loads(l) for l in open(os.path.join(RAW, "harvest.jsonl")) if l.strip()]
    by_id = {r["question_id"]: r for r in harvest}

    # --- edge rows: first EDGE_PER_SITE per site, in file order --------------
    edge_rows, seen = [], set()
    for site in SITES:
        taken = 0
        for e in edges:
            if e["dup"]["site"] != site or taken >= EDGE_PER_SITE:
                continue
            dup, can = e["dup"], e["canonical"]
            if dup["question_id"] in seen or can["question_id"] == dup["question_id"]:
                continue
            seen.add(dup["question_id"])
            taken += 1
            edge_rows.append({
                "a_title": dup["title"], "a_body": excerpt(dup.get("body", "")),
                "b_title": can["title"],
                "b_body": excerpt(by_id[can["question_id"]]["body"])
                if can["question_id"] in by_id else "",
            })
    assert len(edge_rows) == 2 * EDGE_PER_SITE, len(edge_rows)

    # --- unrelated rows: different sites, matched on title length ------------
    pools = {s: [r for r in harvest if r["site"] == s] for s in SITES}
    unrelated = []
    for i in range(UNRELATED):
        want = title_len(edge_rows[i]["a_title"])
        a_site, b_site = (SITES[0], SITES[1]) if i % 2 == 0 else (SITES[1], SITES[0])
        left = [r for r in pools[a_site]
                if abs(title_len(r["title"]) - want) <= 2 and r["question_id"] not in seen]
        right = [r for r in pools[b_site]
                 if abs(title_len(r["title"]) - want) <= 2 and r["question_id"] not in seen]
        if not left or not right:
            continue
        left.sort(key=lambda r: abs(title_len(r["title"]) - want))
        right.sort(key=lambda r: abs(title_len(r["title"]) - want))
        a, b = left[i % len(left)], right[i % len(right)]
        seen.add(a["question_id"])
        seen.add(b["question_id"])
        unrelated.append({
            "a_title": a["title"], "a_body": excerpt(a["body"]),
            "b_title": b["title"], "b_body": excerpt(b["body"]),
        })

    rows = [(("edge", i), r) for i, r in enumerate(edge_rows)]
    rows += [(("unrelated", i), r) for i, r in enumerate(unrelated)]
    rng = random.Random(SEED)
    rng.shuffle(rows)

    sheet_lines = ["key\ta_title\ta_body\tb_title\tb_body"]
    key_rows = []
    for n, (arm, payload) in enumerate(rows, start=1):
        key = "q2-%03d" % n
        sheet_lines.append("\t".join([
            key, payload["a_title"], payload["a_body"],
            payload["b_title"], payload["b_body"]]))
        key_rows.append({"key": key, "arm": arm[0], "arm_index": arm[1]})
    sheet_bytes = ("\n".join(sheet_lines) + "\n").encode("utf-8")
    digest = hashlib.sha256(sheet_bytes).hexdigest()
    sheet_path = os.path.join(SHEETS, "q2_pairs.tsv")
    with open(sheet_path, "wb") as fh:
        fh.write(sheet_bytes)

    # The key file is written in the SHEET's order, which is the defect E032 hit.
    with open(os.path.join(RAW, "q2_key.jsonl"), "w") as fh:
        for r in key_rows:
            fh.write(json.dumps(r) + "\n")

    import collections
    print("sheet: %d rows  (%s)"
          % (len(rows), dict(collections.Counter(r["arm"] for r in key_rows))))
    print("sha256: %s" % digest)
    print("wrote %s and raw/q2_key.jsonl" % os.path.relpath(sheet_path))

    with open(MANIFEST, "w") as fh:
        json.dump({"schema": "origin.e033.sheet/1", "seed": SEED,
                   "sheet": "sheets/q2_pairs.tsv", "sha256": digest,
                   "rows": len(key_rows),
                   "arms": dict(collections.Counter(r["arm"] for r in key_rows)),
                   "double_read_rows": len(key_rows),
                   "body_excerpt_words": WORDS},
                  fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("wrote %s" % os.path.relpath(MANIFEST))


if __name__ == "__main__":
    main()
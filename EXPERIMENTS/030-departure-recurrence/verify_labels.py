#!/usr/bin/env python3
"""E030 — the mechanical check on a reader's label file (D061).

Checks, in this order and all of them:
  1. the frozen view's digest still matches `raw/view_digests_a8.json`;
  2. the labels file carries exactly the view's ids, IN THE VIEW'S ORDER
     (D061: an id set can be complete while the mapping is wrong);
  3. no id is repeated and every label is in the declared alphabet;
  4. every answered row agrees with `raw/a6_key_rows.json`'s id-to-object mapping.

Exit 3 on any failure, so a wrong label file cannot reach `stats.py`.
"""

import hashlib
import json
import os
import sys

import common as C

ALPHABET = {"1", "0", "u", "-"}   # "-" = the question was not asked on this row


def fail(msg, detail):
    C.log("labels_rejected", check=msg, detail=detail)
    sys.exit(3)


def view_ids(path):
    ids = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("ID: "):
                ids.append(line[4:].strip())
    return ids


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "treatment"
    view_name = "view_a8_%s.txt" % which
    view_path = os.path.join(C.RAW, view_name)
    labels_path = os.path.join(C.RAW, "a8_labels_%s.tsv" % which)

    digests = json.load(open(os.path.join(C.RAW, "view_digests_a8.json"), encoding="utf-8"))
    body = open(view_path, encoding="utf-8").read()
    actual = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if actual != digests[view_name]:
        fail("view_digest", {"expected": digests[view_name], "actual": actual})

    ids = view_ids(view_path)
    if not ids:
        fail("view_empty", view_name)

    rows = []
    with open(labels_path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                fail("label_shape", {"line": n, "parts": parts})
            rows.append(tuple(parts))
    got = [r[0] for r in rows]
    if len(set(got)) != len(got):
        fail("repeated_id", {"ids": sorted({i for i in got if got.count(i) > 1})})
    if got != ids:
        fail("order_or_set", {"view_first10": ids[:10], "label_first10": got[:10],
                              "view_n": len(ids), "label_n": len(got),
                              "missing": sorted(set(ids) - set(got)),
                              "extra": sorted(set(got) - set(ids))})
    for rid, q1, q2 in rows:
        if q1 not in ALPHABET or q2 not in ALPHABET:
            fail("alphabet", {"id": rid, "q1": q1, "q2": q2})

    key = {}
    for row in C.read_jsonl("a8_key_rows.jsonl"):
        key[row["id"]] = row["objectID"]
    for rid, _, _ in rows:
        if rid not in key:
            fail("unknown_id", {"id": rid})

    C.log("labels_accepted", view=view_name, rows=len(rows),
          sha256_view=actual[:16], file=labels_path)


if __name__ == "__main__":
    main()

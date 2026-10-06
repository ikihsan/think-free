#!/usr/bin/env python3
"""E031 gate A2 — the mechanical checks on a view and a label file.

Order, all of them, exit 3 on any failure so a bad label file cannot reach
recurrence.py:

  1. the view's digest still matches raw/view_digests.json;
  2. the question block above the first COMMENT: marker is BYTE-IDENTICAL across
     all three arm views (PROTOCOL-AMENDMENT-1.md §3 — the literal whole-file
     reading of "no arm word in a view" could not pass on q3's own wording);
  3. no arm-identifying whole word appears in the header region of any view;
  4. the label file carries exactly the view's ids, IN THE VIEW'S ORDER
     (D061: a complete id set can carry a wrong row-to-id mapping);
  5. no repeated id, every label in the declared alphabet;
  6. every id is in raw/e031_rows.jsonl;
  7. every q2 phrase is a VERBATIM substring of that row's own text (this is what
     makes a printed clause evidence rather than a paraphrase).

Usage: verify_labels.py <view-stem> [r1|r2]
"""

import hashlib
import json
import os
import re
import sys

import common as C

ALPHABET = {"1", "0", "u"}
VIEWS = ["seek", "move", "ordinary"]


def fail(msg, detail):
    C.log("labels_rejected", check=msg, detail=detail)
    sys.exit(3)


def view_path(stem):
    return os.path.join(C.RAW, "view_%s.txt" % stem)


def view_ids(path):
    ids = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("ID: "):
                ids.append(line[4:].strip())
    return ids


def question_block(path):
    """The lines between the first ID: line and the first COMMENT: marker.

    This is the fixed wording a reader reads on every row. The ID line itself is
    excluded because it differs by arm by construction (S01 / M01 / O01), which
    is the defect this function was corrected for after the gate fired on its own
    first run (PROTOCOL-AMENDMENT-1.md §3).
    """
    body = open(path, "r", encoding="utf-8").read()
    head = body.split("COMMENT:")[0]
    lines = head.split("\n")
    out = []
    seen_id = False
    for line in lines:
        if line.startswith("ID: "):
            seen_id = True
            continue
        if seen_id:
            out.append(line)
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        fail("usage", {"argv": sys.argv[1:]})
    stem = sys.argv[1]
    reader = sys.argv[2] if len(sys.argv) > 2 else "r1"
    vpath = view_path(stem)
    if not os.path.exists(vpath):
        fail("view_missing", {"view": stem})

    # 1. digest
    digests = json.load(open(os.path.join(C.RAW, "view_digests.json"), encoding="utf-8"))
    name = "view_%s.txt" % stem
    body = open(vpath, "r", encoding="utf-8").read()
    actual = C.sha256_bytes(body)
    if actual != digests[name]:
        fail("view_digest", {"expected": digests[name], "actual": actual})

    # 2. identical question bytes across the three arm views
    blocks = {v: question_block(view_path(v)) for v in VIEWS}
    if len({b for b in blocks.values()}) != 1:
        fail("question_bytes_differ",
             {v: C.sha256_bytes(b)[:16] for v, b in blocks.items()})

    # 3. no arm-identifying whole word in the question block. Whole-word, because
    # q3's own fixed wording contains "moved" (PROTOCOL-AMENDMENT-1.md §3).
    for v, block in blocks.items():
        words = set(re.findall(r"[A-Za-z0-9]+", block))
        hits = sorted(w for w in C.ARM_WORDS if w in words)
        if hits:
            fail("arm_word_in_question", {"view": v, "words": hits})

    # 4/5/6. label file shape, order, alphabet, known ids
    lpath = os.path.join(C.RAW, "e031_labels_%s__%s.tsv" % (stem, reader))
    if not os.path.exists(lpath):
        fail("labels_missing", {"path": "raw/e031_labels_%s__%s.tsv" % (stem, reader)})
    ids = view_ids(vpath)
    if not ids:
        fail("view_empty", {"view": stem})
    rows = []
    with open(lpath, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                fail("label_shape", {"line": n, "parts": parts})
            rows.append(tuple(parts))
    got = [r[0] for r in rows]
    if len(set(got)) != len(got):
        dup = sorted({i for i in got if got.count(i) > 1})
        fail("repeated_id", {"ids": dup})

    # Reader 2 labels only the declared double-read subset (PROTOCOL-AMENDMENT-1.md),
    # so a partial label file is legal for r2 and illegal for r1. Either way the
    # labelled ids must appear in the view's own relative order (D061: a complete
    # id set can still carry a wrong row-to-id mapping).
    # Rows outside the double-read set by design (the re-read sample and the
    # nonsense rows); for those, r2 must still cover the whole view.
    PARTIAL_OK = ("reread", "nonsense")

    if reader == "r2" and stem not in PARTIAL_OK:
        allowed = set()
        dr_path = os.path.join(C.RAW, "doubleread_ids.txt")
        if os.path.exists(dr_path):
            allowed = set(x.strip() for x in open(dr_path, encoding="utf-8") if x.strip())
        extra = sorted(set(got) - allowed)
        if extra:
            fail("not_in_doubleread_set", {"ids": extra[:10], "n": len(extra)})
        want = [i for i in ids if i in set(got)]
        if got != want:
            fail("order_or_set", {"n_labelled": len(got), "view_first5": want[:5],
                                  "label_first5": got[:5]})
        missing = [] if stem in PARTIAL_OK else sorted(set(ids) - allowed)
    else:
        if got != ids:
            fail("order_or_set", {"view_n": len(ids), "label_n": len(got),
                                  "view_first5": ids[:5], "label_first5": got[:5],
                                  "missing": sorted(set(ids) - set(got)),
                                  "extra": sorted(set(got) - set(ids))})
        missing = []
    for rid, q1, q2 in rows:
        if q1 not in ALPHABET:
            fail("alphabet", {"id": rid, "q1": q1})

    key = {r["id"]: r for r in C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))}
    for rid, _, _ in rows:
        if rid not in key:
            fail("unknown_id", {"id": rid})

    # 7. every q2 phrase is a verbatim substring of its own row's text
    texts = json.load(open(os.path.join(C.RAW, "e031_clause_text.json"), encoding="utf-8"))
    not_verbatim, missing_text = [], []
    for rid, q1, q2 in rows:
        if q1 != "1":
            if q2.strip() != "-":
                not_verbatim.append({"id": rid, "q1": q1, "q2": q2, "why": "q2 given for a non-yes row"})
            continue
        src = texts.get(rid)
        if src is None:
            missing_text.append(rid)
            continue
        if q2.strip() == "-" or q2.strip() == "":
            not_verbatim.append({"id": rid, "q1": q1, "q2": q2, "why": "q2 missing for a yes row"})
            continue
        if not C.is_verbatim(q2.strip(), src):
            not_verbatim.append({"id": rid, "q1": q1, "q2": q2[:80], "why": "not a verbatim substring"})
    if missing_text:
        fail("no_source_text", {"ids": missing_text})
    if not_verbatim:
        fail("q2_not_verbatim", {"n": len(not_verbatim), "examples": not_verbatim[:5]})

    C.log("labels_accepted", view=name, reader=reader, rows=len(rows),
          yes=sum(1 for r in rows if r[1] == "1"),
          sha256_view=actual[:16])


if __name__ == "__main__":
    main()
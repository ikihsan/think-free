#!/usr/bin/env python3
"""E030 gate A6 — freeze the reader views.

D061 requires the input to be identified rather than described, row ids checked
by order rather than by set, and the check to be a command. This writes the two
views, their sha256 digests and the id key. `verify_labels.py` is the command.

Writes raw/view_a6_treatment.txt, raw/view_a6_control.txt,
       raw/view_digests.json, raw/a6_key.json
"""

import hashlib
import json
import os
import random

import common as C

N = 24
SEED = 3006


def render(rows, kind, path):
    lines = []
    for i, row in enumerate(rows, 1):
        rid = "%s%02d" % (kind, i)
        lines.append("=" * 72)
        lines.append("ID: %s" % rid)
        if kind == "T":
            lines.append("DECLARED ARTIFACT CANDIDATE: %s" % row["artifact"])
        lines.append("TEXT:")
        lines.append(row["text"].strip())
        lines.append("")
    body = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return hashlib.sha256(body.encode("utf-8")).hexdigest(), body


def main():
    os.makedirs(C.RAW, exist_ok=True)
    treat = C.read_jsonl("treatment.jsonl")
    ctrl = C.read_jsonl("control.jsonl")

    rng = random.Random(SEED)
    t_rows = sorted(treat, key=lambda r: r["objectID"])
    c_rows = sorted(ctrl, key=lambda r: r["objectID"])
    t_sel = rng.sample(t_rows, N)
    c_sel = rng.sample(c_rows, N)

    key = {"seed": SEED, "n": N,
           "treatment": [r["objectID"] for r in t_sel],
           "control": [r["objectID"] for r in c_sel],
           "questions": {
               "T": ["q1_is_account_of_leaving",
                     "q2_candidate_names_that_artifact"],
               "C": ["q1_is_account_of_leaving"]},
           "labels": {"yes": "1", "no": "0", "unclear": "u"}}
    C.write_jsonl("a6_key_rows.jsonl",
                  [{"kind": "T", "id": "T%02d" % i, "objectID": r["objectID"]}
                   for i, r in enumerate(t_sel, 1)]
                  + [{"kind": "C", "id": "C%02d" % i, "objectID": r["objectID"]}
                     for i, r in enumerate(c_sel, 1)])

    t_digest, _ = render(t_sel, "T", os.path.join(C.RAW, "view_a6_treatment.txt"))
    c_digest, _ = render(c_sel, "C", os.path.join(C.RAW, "view_a6_control.txt"))

    with open(os.path.join(C.RAW, "view_digests.json"), "w", encoding="utf-8") as fh:
        json.dump({"view_a6_treatment.txt": t_digest,
                   "view_a6_control.txt": c_digest,
                   "seed": SEED, "n_rows_each": N}, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(C.RAW, "a6_key.json"), "w", encoding="utf-8") as fh:
        json.dump(key, fh, indent=2, sort_keys=True)
        fh.write("\n")

    C.log("a6_views", treatment_rows=len(t_sel), control_rows=len(c_sel),
          sha256_treatment=t_digest[:16], sha256_control=c_digest[:16])


if __name__ == "__main__":
    main()

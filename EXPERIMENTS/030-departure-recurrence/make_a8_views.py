#!/usr/bin/env python3
"""E030 gate A8 — the held-out reader sample that decides the experiment.

Same two questions as A6, on rows not read by the A6 sample, seed 3007, 30 per
arm. Views are frozen and hashed; `verify_labels.py` checks the label file by
order and not by set (D061).

Writes raw/view_a8_treatment.txt, raw/view_a8_control.txt,
       raw/view_digests_a8.json, raw/a8_key_rows.jsonl
"""

import hashlib
import json
import os
import random

import common as C

N = 30
SEED = 3007


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
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def main():
    os.makedirs(C.RAW, exist_ok=True)
    seen = {r["objectID"] for r in C.read_jsonl("a6_key_rows.jsonl")}
    treat = [r for r in C.read_jsonl("treatment.jsonl") if r["objectID"] not in seen]
    ctrl = [r for r in C.read_jsonl("control.jsonl") if r["objectID"] not in seen]
    C.log("a8_pool", treatment_pool=len(treat), control_pool=len(ctrl),
          excluded_as_already_read=len(seen))

    rng = random.Random(SEED)
    t_sel = rng.sample(sorted(treat, key=lambda r: r["objectID"]), N)
    c_sel = rng.sample(sorted(ctrl, key=lambda r: r["objectID"]), N)

    C.write_jsonl("a8_key_rows.jsonl",
                  [{"kind": "T", "id": "T%02d" % i, "objectID": r["objectID"]}
                   for i, r in enumerate(t_sel, 1)]
                  + [{"kind": "C", "id": "C%02d" % i, "objectID": r["objectID"]}
                     for i, r in enumerate(c_sel, 1)])

    t_digest = render(t_sel, "T", os.path.join(C.RAW, "view_a8_treatment.txt"))
    c_digest = render(c_sel, "C", os.path.join(C.RAW, "view_a8_control.txt"))

    with open(os.path.join(C.RAW, "view_digests_a8.json"), "w", encoding="utf-8") as fh:
        json.dump({"view_a8_treatment.txt": t_digest,
                   "view_a8_control.txt": c_digest,
                   "seed": SEED, "n_rows_each": N}, fh, indent=2, sort_keys=True)
        fh.write("\n")
    C.log("a8_views", treatment_rows=len(t_sel), control_rows=len(c_sel),
          sha256_treatment=t_digest[:16], sha256_control=c_digest[:16])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E141 recall audit: how much does eq_t1 leave on the table?

The protocol declares eq_t1's recovery count a *lower bound* on what a real
equivalence relation could recover. A kill gate evaluated on a lower bound is
only meaningful if the bound is close to the truth, so this emits a
deterministic sample of the wrong rows eq_t1 did NOT recover, with both answers
and both normalized forms, for classification by hand.

The sample is every k-th unrecovered wrong row of P1, plus every one of the
rows with no \\boxed at all in P1 (a separate bucket: the parser found no
answer, so neither did HELM, and a different parser might).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import recover as R                                          # noqa: E402

STEP = 6          # take every 6th unrecovered wrong row -> ~40 rows
NOBOX_CAP = 25    # and up to 25 of the no-\\boxed rows


def main():
    spec = R.CELLS["P1"]
    rows = R.rows_for("P1", spec)

    unrecovered, nobox = [], []
    for cell_id, subject, inst, gold, pred in rows:
        if R.norm_eq(gold, pred):
            continue
        if gold is None or pred is None:
            nobox.append((subject, inst, gold, pred))
            continue
        ok, _ = R.eq_t1(gold, pred)
        if not ok:
            unrecovered.append((subject, inst, gold, pred))

    sampled = unrecovered[::STEP][:80]
    out = {
        "cell": "P1",
        "wrong_rows": len(unrecovered) + len(nobox),
        "unrecovered_by_eq_t1": len(unrecovered),
        "rows_with_no_extractable_answer": len(nobox),
        "sample_step": STEP,
        "sampled": len(sampled),
        "sampled_nobox": min(NOBOX_CAP, len(nobox)),
        "rows": [],
        "nobox_rows": [],
    }

    for subject, inst, gold, pred in sampled:
        out["rows"].append({
            "subject": subject, "instance_id": inst,
            "gold": gold, "pred": pred,
            "norm_gold": R.normalize(gold), "norm_pred": R.normalize(pred),
            "rational_gold": (lambda v: None if v is None else str(v))(
                R.rational_value(R.normalize(gold))),
            "rational_pred": (lambda v: None if v is None else str(v))(
                R.rational_value(R.normalize(pred))),
        })
    for subject, inst, gold, pred in nobox[:NOBOX_CAP]:
        out["nobox_rows"].append({
            "subject": subject, "instance_id": inst, "gold": gold,
            "pred_present": pred is not None})

    with open(os.path.join(HERE, "recall_audit_sample.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")

    print("P1 wrong rows                : %d" % out["wrong_rows"])
    print("  unrecovered by eq_t1       : %d" % len(unrecovered))
    print("  no extractable answer      : %d" % len(nobox))
    print("sampled for hand reading     : %d (every %dth) + %d no-answer rows"
          % (len(sampled), STEP, out["sampled_nobox"]))
    print()
    for r in out["rows"]:
        print("%-24s %-6s gold=%-28r pred=%-28r"
              % (r["subject"], r["instance_id"], r["gold"], r["pred"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
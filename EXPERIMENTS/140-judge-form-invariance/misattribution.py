#!/usr/bin/env python3
"""misattribution.py — the one arm M2 was declared unable to catch.

PROTOCOL.md §M2 declares the weakness: comparing value *multisets* binds nothing
to what the value is said to be about. This builds the arm that tests it, so the
RESULT can say `observed` where it would otherwise have to say `inferred`.

Construction rule, fixed here before the arm is run and applied mechanically:

  split the verbatim answer into clauses; keep clauses holding exactly one
  numeric value; swap the two values between the first two such clauses that
  both carry a value of the same kind; leave every other character untouched.

The result carries exactly the same value multiset as V, so K4 passes, and every
value is still correctly *written* — each is simply attached to the wrong
subject. That is the arm E114's `ungrounded_claim` verdict exists for and the arm
`valueset.compare` cannot see.

This arm is exploratory and carries no gate. It was built after the measured
gates (AMENDMENT-5).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "114-value-grounding"))

import ground      # noqa: E402
import valueset    # noqa: E402
from collections import Counter  # noqa: E402

CLAUSE = re.compile(r"[^.;]+[.;]?")


def clauses(text):
    return [(m.start(), m.group(0)) for m in CLAUSE.finditer(text)
            if m.group(0).strip()]


def single_value_clauses(text):
    """(offset, clause, value) for clauses holding exactly one extracted value."""
    out = []
    for start, body in clauses(text):
        found = ground.extract(body)
        if len(found) == 1:
            kind, raw = found[0]
            if raw.strip():
                out.append((start, body, kind, raw))
    return out


def build(text):
    """The value-transposed arm, or None when the item cannot carry one."""
    cands = single_value_clauses(text)
    for i in range(len(cands)):
        for j in range(i + 1, len(cands)):
            a, b = cands[i], cands[j]
            if a[2] != b[2]:
                continue
            va, vb = a[3], b[3]
            if va == vb:
                continue
            # Replace the later occurrence first so the earlier offset stays valid.
            new_b = b[1].replace(vb, va, 1)
            new_a = a[1].replace(va, vb, 1)
            out = (text[:a[0]] + new_a
                   + text[a[0] + len(a[1]):b[0]] + new_b
                   + text[b[0] + len(b[1]):])
            return out, {"donor_offset": a[0], "receiver_offset": b[0],
                         "value_moved_from": va, "value_moved_to": vb}
    return None, None


def main():
    arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))
            if l.strip()]
    verbatim = {(r["document_number"], r["question"]): r["answer"]
                for r in arms if r["arm"] == "V"}
    E114 = os.path.join(HERE, "..", "114-value-grounding")

    rows, dropped = [], []
    for key in sorted(verbatim):
        text = verbatim[key]
        new, info = build(text)
        if new is None:
            dropped.append({"document_number": key[0],
                            "reason": "no two single-value clauses of one kind"})
            continue
        # K4: the arm must be value-preserving, or it is a different arm.
        same = (Counter(map(repr, valueset.canonical(new)))
                == Counter(map(repr, valueset.canonical(text))))
        if not same:
            dropped.append({"document_number": key[0],
                            "reason": "canonical multiset changed"})
            continue
        rows.append({"document_number": key[0], "question": key[1],
                     "arm": "X", "answer": new, "move": info})

    out = {"built": len(rows), "dropped": dropped,
           "k4_all_preserved": all(
               Counter(map(repr, valueset.canonical(r["answer"])))
               == Counter(map(repr, valueset.canonical(verbatim[
                   (r["document_number"], r["question"])])))
               for r in rows)}

    # What each instrument says about the arm.
    sys.path.insert(0, E114)
    from collections import Counter as C
    docs = {}
    m2_detected = m1_detected = 0
    per_item = []
    for r in rows:
        ref = verbatim[(r["document_number"], r["question"])]
        m2_detected += valueset.compare(ref, r["answer"])["verdict"] == "mismatch"
        num = r["document_number"]
        if num not in docs:
            docs[num] = ground.load_doc(num, os.path.join(E114, "raw"))
        verdicts = ground.judge(docs[num], r["answer"])
        flags = [v for v in verdicts if v["verdict"] != "grounded"]
        m1_detected += bool(flags)
        per_item.append({"document_number": num,
                         "values": len(verdicts), "flagged": len(flags),
                         "m2": "mismatch" if valueset.compare(
                             ref, r["answer"])["verdict"] == "mismatch"
                             else "match"})
    out["items"] = len(rows)
    out["m2_detected"] = m2_detected
    out["m1_flagged_any"] = m1_detected
    out["per_item"] = per_item
    with open(os.path.join(HERE, "misattribution.json"), "w") as fh:
        json.dump({"summary": out, "arms": rows}, fh, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

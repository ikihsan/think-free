#!/usr/bin/env python3
"""verify_flags.py — check every `ungrounded_value` verdict against the raw bytes.

The checker's own verdict is not evidence. For each value it reports as absent
from the document, this asks a weaker and more mechanical question: do all of
the value's digit groups and alphabetic tokens occur somewhere in the document?

It cannot decide whether the value is *correct* — only whether it is *there*.
A value whose parts all occur but whose meaning was invented would pass this
test, so this is a necessary condition, and the hand-read in RESULT.md covers
the 50 sampled `ungrounded_claim` values that this test does not reach.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ground import normalize  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load_doc(num):
    with open(os.path.join(HERE, "raw", "text", num + ".txt"), "rb") as fh:
        return normalize(fh.read().decode("utf-8", "replace"))


def main():
    rows = [json.loads(l) for l in open(os.path.join(HERE, "checked.jsonl")) if l.strip()]
    docs = {}
    out, absent = [], 0
    for r in rows:
        num = r["document_number"]
        if num not in docs:
            docs[num] = load_doc(num).lower()
        low = docs[num]
        for v in r["checked"]:
            if v["verdict"] != "ungrounded_value":
                continue
            groups = re.findall(r"\d+", v["value"])
            toks = [t for t in re.findall(r"[A-Za-z]{3,}", v["value"])]
            missing = [g for g in groups if g not in low]
            missing += [t for t in toks if t.lower() not in low]
            absent += bool(missing)
            out.append({"document": num, "value": v["value"], "kind": v["kind"],
                        "all_parts_present": not missing, "missing": missing})
    print(json.dumps({"ungrounded_value_verdicts": len(out),
                      "with_every_part_present_in_document": len(out) - absent,
                      "genuinely_absent": absent}, sort_keys=True))
    with open(os.path.join(HERE, "flags-verified.jsonl"), "w") as fh:
        for o in out:
            fh.write(json.dumps(o, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

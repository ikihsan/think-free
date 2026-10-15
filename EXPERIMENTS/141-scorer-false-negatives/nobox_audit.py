#!/usr/bin/env python3
"""E141 second recall bucket: the 95 P1 rows with no extractable answer.

39% of P1's wrong rows are rows where neither the model nor the parser produced
a `\\boxed{...}`. HELM scores them 0. A weaker extractor -- the last number in
the completion -- might find a correct answer the `\\boxed` parser missed, and
that gap is the other half of the under-crediting question.

Rows recovered here are *candidates*, not findings: taking the last number of a
chain of thought can pick up an intermediate value, so every recovered row is
emitted for hand reading rather than counted as a false negative.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import recover as R                                          # noqa: E402

E136 = "/tmp/opencode/e136"
SUBJECTS = R.MATH_SUBJECTS


def last_expression(text):
    """The last token that could be an answer, from a free-text completion.

    In order of preference: the last `\\boxed{}`-free `\\frac{a}{b}` or `$...$`
    span, else the last decimal or fraction-shaped run of characters.
    """
    if not text:
        return None
    tail = text.strip()
    # A trailing "the answer is X" / "answer: X" is the strongest signal.
    for pat in (r"[Tt]he answer is\s*\$?([^\n\.\$]{1,40})",
                r"[Aa]nswer:?\s*\$?([^\n\.\$]{1,40})"):
        hits = re.findall(pat, tail)
        if hits:
            return hits[-1].strip().rstrip("$ .")
    m = re.findall(r"\\(?:d?frac)\s*\{[^{}]*\}\s*\{[^{}]*\}", tail)
    if m:
        return m[-1]
    m = re.findall(r"-?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?", tail)
    if m:
        return m[-1]
    return None


def main():
    rows_by_subject = {}
    for subject in SUBJECTS:
        tag = ("math__math:subject=%s,level=1,use_official_examples=False,"
               "use_chain_of_thought=True" % subject)
        state = json.load(open(os.path.join(E136, tag + "__scenario_state.json")))
        for rs in state["request_states"]:
            inst = rs["instance"]
            refs = [r for r in inst.get("references", [])
                    if "correct" in r.get("tags", [])]
            comps = rs.get("result", {}).get("completions", [])
            if not refs or not comps:
                continue
            gb = R.boxed_all(refs[0].get("output", {}).get("text", ""))
            pb = R.boxed_all(comps[0].get("text", ""))
            if pb:
                continue                       # this row had an answer
            rows_by_subject.setdefault(subject, []).append({
                "subject": subject,
                "instance_id": inst.get("id"),
                "gold": gb[-1] if gb else None,
                "completion": comps[0].get("text", ""),
            })

    total = sum(len(v) for v in rows_by_subject.values())
    candidates = []
    for subject in sorted(rows_by_subject):
        for row in rows_by_subject[subject]:
            guess = last_expression(row["completion"])
            row["last_expression"] = guess
            if guess is None or row["gold"] is None:
                continue
            ok, reason = R.eq_t1(row["gold"], guess)
            if ok and R.normalize(guess) != R.normalize(row["gold"]):
                candidates.append(row)

    out = {"no_boxed_rows": total, "candidates": len(candidates),
           "rows": candidates,
           "caveat": "a candidate recovered by last-expression extraction is not "
                     "a false negative until read: the last number of a chain of "
                     "thought can be an intermediate value"}
    with open(os.path.join(HERE, "nobox_candidates.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")

    print("P1 rows with no \\boxed at all : %d" % total)
    print("  candidate recoveries        : %d" % len(candidates))
    print()
    for r in candidates:
        print("%-24s %-6s gold=%-16r last=%-16r  ...%s"
              % (r["subject"], r["instance_id"], r["gold"],
                 r["last_expression"], r["completion"][-70:].replace("\n", " ")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
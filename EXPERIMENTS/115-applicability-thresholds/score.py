#!/usr/bin/env python3
"""Score E115 M2 against the committed reference key.

The key lives in M2-CASES.md's table and was committed before any answer
existed.  This script does not re-derive the key and does not judge the
reasoning; it only compares the recorded answer to the recorded key, so a
disagreement cannot be argued away after the fact.

`answers.jsonl` rows whose case_id is not in the key are counted as
`unkeyed`, never dropped -- a scorer that silently ignores rows it cannot
place reports a clean rate over a population it did not measure (F116).
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Transcribed from the table in M2-CASES.md at commit ab5f9de8.  Kept as a
# literal here rather than parsed out of the Markdown so that an edit to the
# prose cannot silently change the key; check_key.py asserts the two agree.
KEY = {
    "P1": "YES",
    "P2": "NO",
    "P3": "NO",
    "P4": "48",
    "P5": "YES",
    "P6": "NO",
    "P7": "YES",
    "P7b": "SAME",
    "P8": "NO",
    "P9": "YES",
    "P10": "YES",
    "P11": "NO",
    "P12": "YES",
    "P13": "NO",
}

# Which cases the naive "count today's employees" reading gets wrong, as
# stated in M2-CASES.md before any answer existed.
NAIVE_WRONG = {"P2", "P4", "P6", "P8", "P10", "P7b"}

KILL_GATE = 0.95

CELL_RE = re.compile(r"^\|\s*\*\*(P\d+b?)\*\*\s*\|(.*)$", re.M)


def key_from_markdown():
    """Recover the key table from M2-CASES.md, for the cross-check."""
    with open(os.path.join(HERE, "M2-CASES.md")) as fh:
        text = fh.read()
    out = {}
    for match in CELL_RE.finditer(text):
        cid, rest = match.group(1), match.group(2)
        cells = [c.strip() for c in rest.split("|")]
        # cells[0] = facts, cells[1] = question, cells[2] = key
        if len(cells) >= 3:
            key = re.sub(r"\*", "", cells[2]).strip()
            key = re.match(r"(YES|NO|\d+|SAME)", key).group(1)
            out[cid] = key
    return out


def normalize(ans):
    a = re.sub(r"[*`]", "", ans).strip()
    m = re.match(r"(YES|NO|\d+|SAME)", a.upper())
    return m.group(1) if m else None


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default="answers.jsonl")
    ap.add_argument("--gate", type=float, default=KILL_GATE)
    ap.add_argument("--arm", default="M2")
    args = ap.parse_args()

    md = key_from_markdown()
    if md != KEY:
        print("KEY MISMATCH between M2-CASES.md and check_key.py")
        print("  md :", md)
        print("  py :", KEY)
        return 3

    path = os.path.join(HERE, args.answers)
    answers = {}
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec["case_id"] in answers:
                print("DUPLICATE answer for", rec["case_id"])
                return 3
            answers[rec["case_id"]] = rec

    unkeyed = sorted(set(answers) - set(KEY))
    unanswered = sorted(set(KEY) - set(answers))
    rows = []
    agree = 0
    for cid in sorted(KEY):
        if cid not in answers:
            continue
        got = normalize(answers[cid]["assistant_answer"])
        want = KEY[cid]
        ok = got == want
        agree += 1 if ok else 0
        rows.append(
            {
                "case_id": cid,
                "key": want,
                "assistant": got,
                "correct": ok,
                "in_naive_wrong_set": cid in NAIVE_WRONG,
            }
        )

    n = agree + sum(1 for r in rows if not r["correct"])
    acc = (agree / float(n)) if n else 0.0
    lo, hi = wilson(agree, n)

    # The subpopulation that matters for a tool: only the cases where the
    # counting rule changes the answer.  Reported separately because the
    # overall figure is mostly made of cases any incumbent gets.
    div = [r for r in rows if r["in_naive_wrong_set"]]
    div_agree = sum(1 for r in div if r["correct"])
    dlo, dhi = wilson(div_agree, len(div))

    result = {
        "arm": args.arm,
        "answers_file": args.answers,
        "cases_keyed": len(KEY),
        "cases_answered": n,
        "unkeyed_answers": unkeyed,
        "unanswered_cases": unanswered,
        "correct": agree,
        "accuracy": round(acc, 6),
        "accuracy_ci95": [round(lo, 6), round(hi, 6)] if n else None,
        "kill_gate": args.gate,
        "kill_gate_met": acc >= args.gate,
        "verdict": "served_closed" if acc >= args.gate else "population_open",
        "divergent_subset": {
            "n": len(div),
            "correct": div_agree,
            "accuracy": round(div_agree / float(len(div)), 6) if div else None,
            "accuracy_ci95": [round(dlo, 6), round(dhi, 6)] if div else None,
            "kill_gate_met": (div_agree / float(len(div)) >= args.gate) if div else None,
        },
        "rows": rows,
    }
    out_name = "%s-result.json" % args.arm.lower().replace("-", "")
    with open(os.path.join(HERE, out_name), "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")

    for r in rows:
        flag = "OK " if r["correct"] else "X  "
        tag = "  <- counting-rule case" if r["in_naive_wrong_set"] else ""
        print("%s %-5s key=%-5s got=%-5s%s" % (flag, r["case_id"], r["key"], r["assistant"], tag))
    print()
    print("accuracy %d/%d = %.4f  CI95 [%.4f, %.4f]" % (agree, n, acc, lo, hi))
    print(
        "counting-rule subset %d/%d = %.4f"
        % (div_agree, len(div), (div_agree / float(len(div)) if div else 0.0))
    )
    print(
        "kill gate %.2f met: %s -> %s"
        % (args.gate, result["kill_gate_met"], result["verdict"])
    )
    if unkeyed:
        print("UNKEYED ANSWERS (excluded, not dropped):", unkeyed)
    if unanswered:
        print("UNANSWERED CASES (counted as incorrect):", unanswered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
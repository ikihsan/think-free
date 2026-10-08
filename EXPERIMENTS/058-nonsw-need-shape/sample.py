#!/usr/bin/env python3
"""E058 sampling: four deterministic views over the two populations.

Nothing here is random in the sense of unrepeatable. Every view is selected by
sorting the population on question_id and taking a fixed stride, so a reader who
re-runs this gets byte-identical files.

Views written to raw/:

| file | rows | what it is |
|---|---|---|
| `sample-arm1.tsv` | 60 | non-software sites, 10 per site, score tail |
| `sample-arm2.tsv` | 60 | `stackoverflow` tail rows from E034's committed harvest, software tags only |
| `g2a-positive.tsv` | 20 | tool-shaped **by a mechanical rule**, drawn from the population |
| `g2b-negative.tsv` | 20 | not-tool-shaped **by a mechanical rule**, drawn from the same population |

The two G2 views are the positive and negative controls the rubric has to pass.
They are selected by regex over the title, never by the reader, so they test the
reader rather than agreeing with it (E041's G3 lesson: an instrument that cannot
recover a known positive has no floor).

**Titles only, in both arms.** Arm 2's committed corpus has no bodies and no
quota remained to fetch them, so reading bodies in arm 1 and titles in arm 2
would compare two different instruments. The rubric reads titles in both arms and
the bodies are unused for the fraction.

Standard library only. Reproduce:

    python3 EXPERIMENTS/058-nonsw-need-shape/sample.py
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

ARM1_PER_SITE = 10
ARM2_N = 60
CONTROL_N = 20

# Mechanical, written before the rows were read. A title matching this is
# asking for a program, by construction of the words, not by a reader's opinion.
POSITIVE = re.compile(
    r"\b(is|are) there (any |an? )?(library|libraries|tool|tools|package|"
    r"packages|script|scripts|cli|command|app|application|api|sdk|framework|"
    r"plugin|extension|module)\b"
    r"|\bhow (do|can|would) i (write|build|make|create|automate|parse|convert|"
    r"generate|extract)\b"
    r"|\bautomate\b|\bscript (that|to|for)\b", re.I)

# Asking for a product, a material, a place, a price, or a person's judgement.
NEGATIVE = re.compile(
    r"\b(where can i|where do i|what (brand|type|kind|model|material|variety|"
    r"store|shop))\b"
    r"|\bhow much (does|do|is|are|should)\b"
    r"|\b(recommend|suggestion|advice|any advice|thoughts|opinion)\b"
    r"|\b(is it (worth|normal|ok|okay|bad|good|possible|safe)|should i|"
    r"am i (wrong|crazy|doing))\b", re.I)

SOFTWARE_TAGS = {"docker", "git", "python", "regex", "excel-formula"}


def stride(rows, n):
    rows = sorted(rows, key=lambda r: r["question_id"])
    if n >= len(rows):
        return rows
    step = len(rows) / float(n)
    return [rows[int(i * step)] for i in range(n)]


def write_tsv(path, rows, extra=()):
    with open(path, "w") as fh:
        fh.write("\t".join(["qid", "site", "tags", "score", "title"] +
                           list(extra)) + "\n")
        for r in rows:
            fh.write("\t".join([
                str(r["question_id"]), r.get("_site", r.get("site", "")),
                "|".join(sorted(r.get("tags") or [])) if r.get("tags")
                else (r.get("tag") or ""),
                str(r.get("score")), (r.get("title") or "").replace("\t", " "),
            ] + [str(x) for x in extra]) + "\n")


def main():
    # ---- arm 1: the six non-software sites, this session's own harvest
    arm1 = [json.loads(l) for l in open(os.path.join(RAW, "arm1.jsonl"))]
    a1 = []
    for site in sorted(set(r["_site"] for r in arm1)):
        rows = [r for r in arm1 if r["_site"] == site]
        a1.extend(stride(rows, ARM1_PER_SITE))
    write_tsv(os.path.join(RAW, "sample-arm1.tsv"), a1)

    # ---- arm 2: E034's committed stackoverflow tail, software tags only
    e034 = [json.loads(l) for l in
            open(os.path.join(HERE, "..", "034-reask-tail", "raw", "harvest.jsonl"))]
    pool2 = [r for r in e034
             if r.get("arm") == "tail" and r.get("site") == "stackoverflow"
             and r.get("tag") in SOFTWARE_TAGS]
    a2 = stride(pool2, ARM2_N)
    write_tsv(os.path.join(RAW, "sample-arm2.tsv"), a2)

    # ---- G2 controls. Attempt 1 drew them from arm 2's 425-row pool and got 7
    # positive-rule and 6 negative-rule rows against a declared 20 each. The
    # rules are not being loosened to hit a target -- that would fit the
    # instrument to the answer. The pool is enlarged instead, to every row this
    # repository holds on the platform: E034's 2124-row harvest plus arm 1's
    # 1200. The control tests the reader, so it does not need to be drawn from
    # the measured population.
    ctrl_pool = list(e034) + list(arm1)
    pos = [r for r in ctrl_pool if POSITIVE.search(r.get("title") or "")]
    neg = [r for r in ctrl_pool if NEGATIVE.search(r.get("title") or "")]
    write_tsv(os.path.join(RAW, "g2a-positive.tsv"), stride(pos, CONTROL_N))
    write_tsv(os.path.join(RAW, "g2b-negative.tsv"), stride(neg, CONTROL_N))

    print("arm1 pool %d -> view %d" % (len(arm1), len(a1)))
    print("arm2 pool %d (stackoverflow tail, %s) -> view %d"
          % (len(pool2), ",".join(sorted(SOFTWARE_TAGS)), len(a2)))
    print("G2a positive-rule pool %d -> %d" % (len(pos), CONTROL_N))
    print("G2b negative-rule pool %d -> %d" % (len(neg), CONTROL_N))


if __name__ == "__main__":
    main()

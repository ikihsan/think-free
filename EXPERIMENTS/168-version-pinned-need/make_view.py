#!/usr/bin/env python3
"""E168 step 1: emit a compact, readable view of the E126 pool for blind
classification.

Writes `pool_view.tsv` with one line per row: idx, question_id, arm,
view_count, answer_count, tags, title, and the first BODY_CHARS characters
of the body, plus two derived shortlist hints that are *not* the classifier:

  vhit  - a literal version-like token in title+body
  chit  - a literal change-word in title+body

The hints exist so the reader can check the classifier's coverage, not to
decide it. `classify.py` requires every row to carry an explicit label.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(HERE, "..", "126-stackoverflow-service-test",
                    "screening.jsonl")
GRADED = os.path.join(HERE, "..", "126-stackoverflow-service-test",
                      "grading-results.jsonl")
OUT = os.path.join(HERE, "pool_view.tsv")

# NOTE: `pool_view.tsv` is a regenerated reading aid, not tracked evidence.
# It is 301 lines and would breach the 300-line cap on a file that carries no
# observation. `classified.jsonl` is the artifact that is tracked; re-run this
# script to reproduce the view.
BODY_CHARS = 320
V_TOKEN = re.compile(r"(?<![\w.])v?\d+\.\d+(?:\.\d+)?(?![\w.])")
V_WORD = re.compile(
    r"\b(version|release|breaking|deprecat\w*|migrat\w*|renam\w*|moved|"
    r"removed in|since|upgrade|downgrade|legacy|api key|sdk)\b", re.I)


def clean(text, limit=None):
    text = re.sub(r"\s+", " ", text or "").strip()
    if limit and len(text) > limit:
        text = text[:limit] + "…"
    return text


def main():
    # E126 wrote question ids as STRINGS in grading-results.jsonl and as INTS
    # in screening.jsonl. Comparing them directly intersects zero rows, which
    # would silently report "none of the graded rows are in the pool" and
    # silently drop this protocol's blinding. Normalise both sides to int.
    graded = set()
    with open(GRADED) as fh:
        for line in fh:
            graded.add(int(json.loads(line)["question_id"]))

    rows = []
    with open(POOL) as fh:
        for i, line in enumerate(fh):
            r = json.loads(line)
            r["question_id"] = int(r["question_id"])
            hay = "%s %s" % (r.get("title", ""), r.get("body", ""))
            rows.append({
                "idx": i,
                "qid": r["question_id"],
                "arm": r.get("arm", ""),
                "views": r.get("view_count", 0),
                "answers": r.get("answer_count", 0),
                "tagstr": ",".join(r.get("tags", []))[:60],
                "title": clean(r.get("title", ""), 160),
                "body": clean(r.get("body", ""), BODY_CHARS),
                "in_graded40": r["question_id"] in graded,
                "dropped": bool(r.get("dropped")),
                "vhint": bool(V_TOKEN.search(hay) or V_WORD.search(hay)),
            })

    rows.sort(key=lambda r: -r["views"])

    with open(OUT, "w") as fh:
        fh.write("idx\tqid\tarm\tviews\tans\tgraded\thint\ttags\t"
                 "title\tbody\n")
        for r in rows:
            fh.write("%d\t%d\t%s\t%d\t%d\t%d\t%d\t%s\t%s\t%s\n" % (
                r["idx"], r["qid"], r["arm"], r["views"], r["answers"],
                int(r["in_graded40"]), int(r["vhint"]), r["tagstr"],
                r["title"], r["body"]))

    print(json.dumps({
        "rows": len(rows),
        "dropped": sum(1 for r in rows if r["dropped"]),
        "in_e126_graded40": sum(1 for r in rows if r["in_graded40"]),
        "eligible_ungraded": sum(1 for r in rows
                                 if r["in_graded40"] or r["dropped"]) and
                             sum(1 for r in rows
                                 if not r["in_graded40"] and not r["dropped"]),
        "version_hint_hits": sum(1 for r in rows if r["vhint"]),
        "out": os.path.relpath(OUT, HERE),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
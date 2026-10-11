#!/usr/bin/env python3
"""E092 grades: served/unserved per sample row.

Each grade is written against the thread's own convergence
(its highest-scored answers, its accepted answer, and the
asker's follow-up where one exists), with the reason the
attempt did or did not meet the protocol's served definition.

Grading rules (declared in PROTOCOL.md):
  served = the attempt names the likely fault and the action
  that resolves it, at the specificity the thread's own
  resolution reaches, and is consistent with the thread's
  converged answer.

The 40 grades are ~330 lines as one dict, past the
300-line cap, so they live in two sibling modules split
at the sample's midpoint in rank order (screening rank
ascending): `grades_sample_1_20.py` holds the first
20 rows and `grades_sample_21_40.py` the rest. The
split is positional; grades were written row by row
against the threads, and attempts.py wrote the sample
order this writer reads.
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from grades_sample_1_20 import GRADES_FIRST  # noqa: E402
from grades_sample_21_40 import GRADES_SECOND  # noqa: E402

GRADES = {}
GRADES.update(GRADES_FIRST)
GRADES.update(GRADES_SECOND)


def main():
    attempts = [json.loads(l) for l in open("attempts.jsonl")]
    out = []
    for a in attempts:
        served, resolution, reason = GRADES[a["qid"]]
        out.append({**a, "served": served,
                    "thread_resolution": resolution,
                    "grade_reason": reason})
    with open("grades.jsonl", "w") as f:
        for g in out:
            f.write(json.dumps(g) + "\n")
    n = len(out)
    served = sum(1 for g in out if g["served"])
    print("graded %d rows: %d served, %d unserved"
          % (n, served, n - served))
    for g in out:
        if not g["served"]:
            print("  unserved: rank %d qid %d (%s)"
                  % (g["rank"], g["qid"], g["remedy"]))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E092 attempt arm.

One attempt per sample row, written from the question's
title and body only, from general knowledge. No answer,
comment, or accepted flag has been read at the time of
writing. Each row carries attempt_first=True.

The attempts are the instrument's output; grades.py scores
them against the thread after the threads are read.

The 40 attempts are ~360 lines as one dict, past the
300-line cap, so they live in two sibling modules split
at the sample's midpoint in rank order (screening rank
ascending): `attempts_sample_1_20.py` holds the first
20 rows and `attempts_sample_21_40.py` the rest, so the
screening rank a reader wants names the file that holds
it. The split is positional; the attempts were written in
one pass before any thread was read, and grades.py scores
the merged dict exactly as it scored the original.
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from attempts_sample_1_20 import ATTEMPTS_FIRST  # noqa: E402
from attempts_sample_21_40 import ATTEMPTS_SECOND  # noqa: E402

ATTEMPTS = {}
ATTEMPTS.update(ATTEMPTS_FIRST)
ATTEMPTS.update(ATTEMPTS_SECOND)


def main():
    sample = [l.split("\t") for l in
              open("sample.tsv").read().strip().split("\n")[1:]]
    out = []
    for row in sample:
        rank, qid, views, shape, remedy, note = row
        qid = int(qid)
        assert qid in ATTEMPTS, "missing attempt for %d" % qid
        cls, attempt = ATTEMPTS[qid]
        assert cls == remedy, (qid, cls, remedy)
        out.append({"rank": int(rank), "qid": qid,
                    "views": int(views), "shape": shape,
                    "remedy": remedy, "attempt": attempt,
                    "attempt_first": True})
    with open("attempts.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    print("attempts written: %d rows, all attempt_first=True" % len(out))


if __name__ == "__main__":
    main()

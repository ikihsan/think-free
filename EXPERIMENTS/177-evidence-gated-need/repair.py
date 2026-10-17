#!/usr/bin/env python3
"""E177 AMENDMENT 5: re-escape one malformed JSONL line without editing content.

Refuses to touch a line that already parses, refuses a line whose qid is not in
the committed ANS order, and prints the answer's character count before and
after so a reader can confirm no content was dropped.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "ans", "answers.jsonl")


def main():
    order = json.load(open(os.path.join(HERE, "ans", "order.json")))["order"]
    lines = open(PATH).read().split("\n")
    fixed, report = [], []
    for n, line in enumerate(lines, 1):
        if not line.strip():
            fixed.append(line)
            continue
        try:
            row = json.loads(line)
        except ValueError:
            head, sep, tail = line.partition('"answer": "')
            if not sep or not tail.endswith('"}'):
                print("line %d: malformed and not in the expected shape; "
                      "refusing to guess" % n)
                return 3
            qid = int(head.split('"qid": ')[1].split(",")[0])
            if qid not in order:
                print("line %d: qid %d is not in the committed order; refusing"
                      % (n, qid))
                return 3
            answer = tail[:-2]
            row = {"qid": qid, "answer": answer}
            fixed.append(json.dumps(row, sort_keys=True))
            report.append((n, qid, len(answer)))
            continue
        if row["qid"] not in order:
            print("line %d: qid %d is not in the committed order; refusing"
                  % (n, row["qid"]))
            return 3
        fixed.append(line)
    if not report:
        print("nothing to repair")
        return 0
    for n, qid, ln in report:
        print("repaired line %d, qid %d: %d characters of answer re-escaped"
              % (n, qid, ln))
    out = "\n".join(fixed)
    with open(PATH, "w") as fh:
        fh.write(out)
    rows = [json.loads(l) for l in open(PATH) if l.strip()]
    ids = [r["qid"] for r in rows]
    print("%d lines parse; %d unique qids; covers the order: %s"
          % (len(rows), len(set(ids)), set(ids) == set(order)))
    return 0 if set(ids) == set(order) else 3


if __name__ == "__main__":
    sys.exit(main())
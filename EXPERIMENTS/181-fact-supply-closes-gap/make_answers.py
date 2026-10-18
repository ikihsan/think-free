#!/usr/bin/env python3
"""E181: `ANS`. The reader's answers, keyed by (arm, qid) and checked against the render.

`ANS` was given one rendered input file at a time from `ans-input/`, in sequence,
with no retrieval and no tools, and saw no accepted answer, no comment outside
its own file, no fact file, and no other arm's answer for the same row. This
script types what was written and then refuses to emit anything unless the
keyset is exactly the keyset of `ans-index.json` - so an arm cannot be silently
missing, duplicated, or attached to the wrong row, which is the one failure that
would quietly turn the treatment into noise.

Run: python3 EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# The 52 answers live in `answers-data.json`, keyed "ARM|qid". They are
# reader output, not code, and the 300-line cap exempts .json by suffix.
ANSWERS = None


def main():
    global ANSWERS
    raw = json.load(open(os.path.join(HERE, "answers-data.json")))
    ANSWERS = dict((tuple(k.split("|", 1)[0:1] + [int(k.split("|", 1)[1])]), v)
                   for k, v in raw.items())
    idx = json.load(open(os.path.join(HERE, "ans-index.json")))["index"]
    want = set((e["arm"], e["qid"]) for e in idx)
    assert want == set(ANSWERS), ("key mismatch: missing %r extra %r"
                            % (sorted(want - set(ANSWERS)), sorted(set(ANSWERS) - want)))
    with open(os.path.join(HERE, "answers.jsonl"), "w") as fh:
        for e in sorted(idx, key=lambda x: x["seq"]):
            fh.write(json.dumps({"seq": e["seq"], "arm": e["arm"], "qid": e["qid"],
                                 "answer": ANSWERS[(e["arm"], e["qid"])]},
                                sort_keys=True) + "\n")
    by = {}
    for e in idx:
        by[e["arm"]] = by.get(e["arm"], 0) + 1
    print("answers %d, by arm %s" % (len(idx), by))


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""E177: build SCORE's input. One file, 60 graded pairs plus 15 controls, shuffled.

SCORE must not be able to tell a graded pair from a control pair, and must not
see which arm any row is in. So every pair is `{pid, left, right, right_label}`
with `right_label` blank for graded rows, and the whole set is shuffled by seed.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    sys.path.insert(0, HERE)
    from roles import text                                     # noqa: E402
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(HERE, "rows.json")))["rows"]}
    arms = json.load(open(os.path.join(HERE, "arms.json")))
    ans = {}
    for line in open(os.path.join(HERE, "ans", "answers.jsonl")):
        if line.strip():
            r = json.loads(line)
            ans[r["qid"]] = r["answer"]
    ctl = json.load(open(os.path.join(HERE, "control_pairs.json")))
    ctl_texts = json.load(open(os.path.join(HERE, "score",
                                            "control_key_texts.json")))

    items = []
    for want in ("SELF", "EVID"):
        for q in arms["arms"][want]:
            items.append({"pid": "g-%d" % q,
                          "left": ans[q],
                          "right": text(rows[q]["key_body"])})
    for p in ctl["g0b_identical_pairs"]:
        items.append({"pid": p["id"],
                      "left": ctl_texts[str(p["a_qid"])],
                      "right": ctl_texts[str(p["b_qid"])]})
    for p in ctl["g0c_distinct_pairs"]:
        items.append({"pid": p["id"],
                      "left": ctl_texts[str(p["a_qid"])],
                      "right": ctl_texts[str(p["b_qid"])]})
    random.Random(17720261018).shuffle(items)
    os.makedirs(os.path.join(HERE, "score", "pairs"), exist_ok=True)
    for it in items:
        # AMENDMENT 4's lesson applied before SCORE ran: one wrapped file per
        # pair. The longest pair line here is 17,003 characters, and a reader
        # that caps a line at 2,000 would lose the comparison.
        with open(os.path.join(HERE, "score", "pairs", "%s.txt" % it["pid"]),
                  "w") as fh:
            fh.write("pid: %s\n\n=== LEFT ===\n" % it["pid"])
            for ln in it["left"].split("\n") or [""]:
                for i in range(0, max(len(ln), 1), 90):
                    fh.write(ln[i:i + 90] + "\n")
            fh.write("\n=== RIGHT ===\n")
            for ln in it["right"].split("\n") or [""]:
                for i in range(0, max(len(ln), 1), 90):
                    fh.write(ln[i:i + 90] + "\n")
    with open(os.path.join(HERE, "score", "index.json"), "w") as fh:
        json.dump({"pids": [it["pid"] for it in items],
                   "seed": 17720261018}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %d pairs (%d graded, 5 identical controls, 5 distinct "
          "controls), shuffled" % (len(items), len(items) - 10))
    print("control qids come from outside the CLF population: %s"
          % (ctl["g0b_identical_pairs"][0]["a_qid"],))
    return 0


if __name__ == "__main__":
    sys.exit(main())
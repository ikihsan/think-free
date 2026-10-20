#!/usr/bin/env python3
"""E177: merge the two CLF passes, commit the arms, and cut the ANS population.

Runs only after `clf/labels-a.jsonl` and `clf/labels-b.jsonl` exist, and writes
`labels.json` and `arms.json`. Committed before any assistant answer exists --
that ordering is the protocol's first forced step and a reader can check it from
git rather than from PROTOCOL.md.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PER_ARM = 30


def main():
    pop = json.load(open(os.path.join(HERE, "clf_population.json")))
    labels = {}
    dupes = []
    for name in ("a", "b"):
        path = os.path.join(HERE, "clf", "labels-%s.jsonl" % name)
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row["qid"] in labels:
                dupes.append(row["qid"])
            labels[row["qid"]] = row
    expect = set(pop["qids"])
    got = set(labels)
    print("population %d; labelled %d; missing %s; extra %s; duplicates %s"
          % (len(expect), len(got), sorted(expect - got) or "none",
             sorted(got - expect) or "none", dupes or "none"))
    if expect != got:
        print("REFUSING: the two passes do not cover the committed population")
        return 3
    counts = {}
    kinds = {}
    for qid in pop["qids"]:
        arm = labels[qid]["arm"]
        counts[arm] = counts.get(arm, 0) + 1
        if arm == "EVID":
            kinds[labels[qid]["kind"]] = kinds.get(labels[qid]["kind"], 0) + 1
    print("arms: %s" % counts)
    print("EVID kinds: %s" % kinds)

    with open(os.path.join(HERE, "labels.json"), "w") as fh:
        json.dump({"population_sha256": pop["sha256"], "counts": counts,
                   "kinds": kinds,
                   "labels": [labels[q] for q in pop["qids"]]}, fh,
                  indent=1, sort_keys=True)
        fh.write("\n")

    # Arm assignment is by arrival within the arm, using the committed
    # view_counts order; no label content enters the selection.
    vc = dict(zip(pop["qids"], pop["view_counts"]))
    arms = {}
    for want in ("SELF", "EVID"):
        qids = [q for q in pop["qids"] if labels[q]["arm"] == want]
        qids.sort(key=lambda q: (-vc[q], q))
        arms[want] = qids[:PER_ARM]
    overlap = set(arms["SELF"]) & set(arms["EVID"])
    if overlap:
        print("REFUSING: arms overlap on %s" % sorted(overlap))
        return 3
    print("ANS population: SELF %d, EVID %d, overlap 0 (G0d)"
          % (len(arms["SELF"]), len(arms["EVID"])))
    if min(len(arms["SELF"]), len(arms["EVID"])) < PER_ARM:
        print("K1 FIRES: an arm is short of %d; the comparison does not run"
              % PER_ARM)
        print("short arm sizes: SELF %d EVID %d"
              % (len(arms["SELF"]), len(arms["EVID"])))
        with open(os.path.join(HERE, "arms.json"), "w") as fh:
            json.dump({"per_arm_requested": PER_ARM, "short": True,
                       "counts": counts, "arms": arms}, fh,
                      indent=1, sort_keys=True)
            fh.write("\n")
        return 0
    with open(os.path.join(HERE, "arms.json"), "w") as fh:
        json.dump({"per_arm_requested": PER_ARM, "short": False,
                   "counts": counts, "arms": arms}, fh,
                  indent=1, sort_keys=True)
        fh.write("\n")
    os.makedirs(os.path.join(HERE, "ans"), exist_ok=True)
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(HERE, "rows.json")))["rows"]}
    # One file, one order, and the order is a seeded shuffle of the 60 rather
    # than arm-by-arm: a reader handed `self.txt` and `evid.txt` learns the arm
    # from the filename, which is exactly the blinding PROTOCOL.md requires.
    sys.path.insert(0, HERE)
    from roles import text                                    # noqa: E402
    import random                                            # noqa: E402
    order = arms["SELF"] + arms["EVID"]
    random.Random(17720261017).shuffle(order)
    with open(os.path.join(HERE, "ans", "questions.txt"), "w") as fh:
        fh.write("# %d Stack Overflow questions, in shuffled order.\n"
                 "# Answer every one from your own knowledge. No retrieval,\n"
                 "# no tools, no files other than this one.\n" % len(order))
        for q in order:
            fh.write("\n===== qid %d | %s =====\n"
                     % (q, rows[q]["title"]))
            body = text(rows[q]["body"])
            for ln in body.split("\n") or [""]:
                for i in range(0, max(len(ln), 1), 90):
                    fh.write(ln[i:i + 90] + "\n")
    with open(os.path.join(HERE, "ans", "order.json"), "w") as fh:
        json.dump({"order": order, "seed": 17720261017}, fh,
                  indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote ans/questions.txt: %d questions, shuffled by seed" % len(order))
    return 0


if __name__ == "__main__":
    sys.exit(main())
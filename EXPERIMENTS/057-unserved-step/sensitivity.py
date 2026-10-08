"""E057 sensitivity check: can the clustering instrument recover a cluster of the
*same step* from distinct requesters, and does it report the user count correctly?

Two controls, both run on this instrument, neither on a hand-built cluster list:

  P1 synthetic-insert : inject 12 titles describing one step, from 12 distinct
                        synthetic user_ids, into one real arm. The instrument must
                        return them as (at least) one cluster containing all 12 ids.
                        This tests the mechanics only.
  P2 real face-validity: for the top real clusters, a human reads the titles and
                        records whether the cluster is ONE step. Sensitivity of the
                        *semantic* judgment is measured here, and is reported as a
                        hand-read count, never as an automatic score.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cluster as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

INJECT = [
    "How do I true a steel frame before mounting the derailleur?",
    "Truing a steel frame: which gauge do I use for the wheel?",
    "How should I true this steel bicycle frame?",
    "What is the correct way to true a steel frame?",
    "Frame truing without a truing stand, is it possible?",
    "I need to true my steel frame, what tools are required?",
    "Truing a steel frame with a dish gauge",
    "How do I true a steel frame that has a warp in the seat tube?",
    "Advice on truing a steel frame spoke tension",
    "Can I true a steel frame myself or must I pay a shop?",
    "My steel frame is out of true, how do I fix it?",
    "Truing a steel frame after replacing a rear hub",
]
INJECT_IDS = list(range(9000001, 9000013))


def main():
    idx = json.load(open(os.path.join(RAW, "index.json")))
    site = next(s for s in idx["sites"] if s["arm"] == "tail")
    rows = json.load(open(os.path.join(RAW, site["file"])))
    print("P1 into %s (%s) %d real rows" % (site["name"], site["arm"], len(rows)))

    before = C.run([(site["name"], rows)], C.__dict__.get("TAU", 0.34), "tail", 8, 8)
    injected = rows + [{"title": t, "owner": {"user_id": u}, "question_id": 0}
                       for t, u in zip(INJECT, INJECT_IDS)]
    after = C.run([(site["name"], injected)], 0.34, "tail", 8, 8)
    added = [c for c in after if c not in before]

    found = 0
    for c in added:
        got = set()
        for tid in c["titles"]:
            pass
        found += 1
    # membership check needs indices, so re-derive directly
    mem = None
    for m in C.agglomerate(injected, 0.34):
        titles = [injected[i]["title"] for i in m]
        if sum(1 for t in titles if t in INJECT) >= 2:
            mem = m
            break
    if mem is None:
        print("P1 FAIL: the 12 injected titles did not land in one cluster")
        return 1
    got_ids = set(injected[i]["owner"]["user_id"] for i in mem
                  if injected[i]["owner"]["user_id"] in INJECT_IDS)
    print("P1 injected ids recovered: %d of 12 ; cluster size %d ; users reported %d"
          % (len(got_ids), len(mem), C.users(injected, mem)))
    print("P1 terms:", ",".join(C.describe(injected, mem)[:8]))
    print("P1 verdict:", "PASS" if len(got_ids) == 12 else "PARTIAL")

    res = json.load(open(os.path.join(RAW, "clusters.json")))
    top = res["chosen"]["arms"]["tail"][:25]
    with open(os.path.join(HERE, "handread-template.md"), "w") as fh:
        fh.write("# E057 hand-read sheet (P2 face validity)\n\n")
        fh.write("One row per top real cluster. `one-step` = the titles describe a "
                 "single step the asker is trying to perform, not a topic, not a "
                 "product choice, not a fact lookup. Recorded before reading any "
                 "body text.\n\n")
        fh.write("| # | users | site | terms | one-step (y/n) | the step, in my words |\n")
        fh.write("|---|---|---|---|---|---|\n")
        for i, c in enumerate(top, 1):
            fh.write("| %d | %d | %s | %s |  |  |\n"
                     % (i, c["users"], c["site"], ", ".join(c["terms"][:6])))
    print("\nwrote handread-template.md for the top %d tail clusters" % len(top))
    for i, c in enumerate(top, 1):
        print("%2d  %3d users  %-26s %s" % (i, c["users"], c["site"][:26],
                                            ", ".join(c["terms"][:7])))
        print("     e.g. %s" % (c["titles"][0][:110] if c["titles"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

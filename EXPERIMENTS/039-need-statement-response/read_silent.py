#!/usr/bin/env python3
"""E039: read the residual by hand, in the order the protocol says it must be.

The protocol is explicit that the residual is offered as a population to read,
not as a queue. This prints the silent needs with their own words, so that what
"unanswered" means can be read rather than counted: a need whose thread simply
ended, a need that got an answer in a sibling comment, a need that is a
comment in a thread about something else entirely, and a need nobody could
answer are four different things and the counts cannot tell them apart.

Reads raw/ only. Prints, does not judge.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
TAG = re.compile(r"<[^>]+>")


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    need = {str(json.loads(l)["id"]): json.loads(l) for l in open(corpus)}
    arms = {}
    p = os.path.join(RAW, "arms.jsonl")
    if os.path.exists(p):
        for line in open(p):
            d = json.loads(line)
            arms[d["id"]] = d
    order = json.load(open(os.path.join(HERE, "read_order.json")))

    shown = 0
    for cid in order:
        a = arms.get(cid)
        if a is None or a["has_subtree"]:
            continue
        n = need[cid]
        body = TAG.sub(" ", n["text"]).strip()
        print("=" * 78)
        print("id %s  %s  trigger=%r  story=%r (%d comments, %d peers replied)"
              % (cid, n["created"][:10], n["trigger"], (n["story"] or "")[:60],
                 a["story_total"], a["story_total"] - 1))
        print(body[:700])
        shown += 1
        if shown >= 40:
            break
    print("\nprinted %d silent needs" % shown)


if __name__ == "__main__":
    main()
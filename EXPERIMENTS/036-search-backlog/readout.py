#!/usr/bin/env python3
"""E036 readout: the prototype is a URL, and this prints the evidence for that.

Runs offline on the committed response of raw/measures.jsonl. It makes no network
request, so its output is reproducible and diffable against the digests in README.md.

  python3 readout.py            # the first-party URL, and the duplicate worklist it returned
  python3 readout.py --url      # the URL alone, no rows

The point of this file is not the worklist. It is that the worklist is what
api.stackexchange.com returns from a documented, unauthenticated route, with
Stack Overflow's own closure label already in the payload.
"""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
DUP = ("Duplicate", "exact duplicate")


def r0():
    for line in open(os.path.join(RAW, "measures.jsonl")):
        rec = json.loads(line)
        if rec["measure"] == "r0-no-closed-param":
            return rec
    raise SystemExit("no r0-no-closed-param record in raw/measures.jsonl")


def main(argv):
    rec = r0()
    url = rec["url"]
    items = json.loads(rec["body"]).get("items", [])
    print(url)
    if "--url" in argv:
        return
    dup = [it for it in items if it.get("closed_reason") in DUP]
    scored = [it.get("score") for it in items if "score" in it]
    print()
    print("returned by that one request   %d rows" % len(items))
    print("ordered by score               %s .. %s, non-decreasing: %s"
          % (scored[0], scored[-1], all(a <= b for a, b in zip(scored, scored[1:]))))
    print("rows carrying closed_reason    %d  (the key's absence means not closed)"
          % sum(1 for it in items if "closed_reason" in it))
    print("closed as a duplicate          %d" % len(dup))
    print()
    print("  score  views    closure             title")
    for it in sorted(dup, key=lambda i: i["score"]):
        print("  %5d  %6d  %-18s  %s"
              % (it["score"], it.get("view_count", -1), it["closed_reason"],
                 it["title"][:58]))
    print()
    print("Nothing above was computed here. Every row is a field of one response.")


if __name__ == "__main__":
    main(sys.argv[1:])

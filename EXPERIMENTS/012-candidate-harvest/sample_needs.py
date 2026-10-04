#!/usr/bin/env python3
"""Select a mechanically-chosen screening sample from the harvested need corpus.

The point of this script is that the sample must NOT be chosen by taste. It is
drawn by a stated rule so that a later reader can re-derive the same 60 items,
and so that the screening rate cannot be inflated by picking easy cases.

Rule (v1):
  1. keep a comment only if its need clause -- the text between the matched
     trigger phrase and the first sentence break -- is at least 6 words long;
  2. sort the survivors by (created date, comment id), newest first;
  3. take every Nth survivor so the sample is spread across the whole date range
     rather than clustered at one end.

Writes raw/sample.jsonl and prints the counts each filter removed.
"""
import json
import re
import sys

import os

HERE = os.path.dirname(os.path.abspath(__file__))


def path(*parts):
    """Resolve a data path next to this script.

    The evidence is only reproducible if it can be re-run from anywhere, so the
    raw files are addressed relative to the script rather than to the caller's
    working directory.
    """
    return os.path.join(HERE, *parts)

RAW = "raw/hn_needs_2026-10-04.jsonl"  # joined by path() below
OUT = "raw/sample.jsonl"
STEP = 21
WANT = 60

WORD = re.compile(r"[a-z][a-z0-9+#.]{2,}")


def clause(text, trigger):
    i = text.lower().find(trigger)
    if i < 0:
        return ""
    s = text[i + len(trigger):]
    s = re.split(r"[.?!\n]", s)[0]
    return re.sub(r"\s+", " ", s).strip()


def main():
    rows = [json.loads(l) for l in open(path(RAW))]
    kept = []
    short = 0
    for r in rows:
        c = clause(r["text"], r["trigger"])
        if len(WORD.findall(c)) < 6:
            short += 1
            continue
        kept.append({"id": r["id"], "trigger": r["trigger"], "date": r["created"][:10],
                     "story": (r["story"] or "")[:110], "clause": c[:300],
                     "text": r["text"][:900]})
    # newest first, id as the tiebreak so the order is total
    kept.sort(key=lambda r: (r["date"], r["id"]), reverse=True)
    sample = kept[::STEP][:WANT]
    with open(path(OUT), "w") as f:
        for r in sample:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print("corpus          %d" % len(rows))
    print("dropped <6 words %d" % short)
    print("eligible        %d" % len(kept))
    print("sample          %d (every %dth, newest first)" % (len(sample), STEP))
    print("date range      %s .. %s" % (sample[-1]["date"], sample[0]["date"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

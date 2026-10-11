#!/usr/bin/env python3
"""E092 grading helper: dump each sample thread's answers
and comments as compact text, in chunks, for hand grading."""
import html
import json
import re
import sys

TAG = re.compile(r"<[^>]+>")


def strip(h):
    h = TAG.sub(" ", h or "")
    h = html.unescape(h)
    return re.sub(r"\s+", " ", h).strip()


def main():
    lo = int(sys.argv[1])
    hi = int(sys.argv[2])
    sample = [json.loads(l) for l in open("attempts.jsonl")]
    pool = {json.loads(l)["question_id"]: json.loads(l)
            for l in open("pool.jsonl")}
    threads = {json.loads(l)["qid"]: json.loads(l)
               for l in open("threads.jsonl")}
    for r in sample[lo:hi]:
        t = threads[r["qid"]]
        print("=" * 72)
        print("[%d] qid=%d views=%d remedy=%s"
              % (r["rank"], r["qid"], r["views"], r["remedy"]))
        print("TITLE: " + strip(pool[r["qid"]].get("title", "")))
        print("ATTEMPT: " + strip(r["attempt"])[:300])
        for a in sorted(t["answers"], key=lambda x: -(x.get("score") or 0)):
            acc = " [ACCEPTED]" if a.get("is_accepted") else ""
            print("  -- answer%s score=%s:%s"
                  % (acc, a.get("score"), strip(a.get("body"))[:500]))
        for c in t["comments"][:6]:
            print("  ~~ comment: " + strip(c.get("body"))[:200])


if __name__ == "__main__":
    main()

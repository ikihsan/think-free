#!/usr/bin/env python3
"""E092 screening helper: dump the top-N pool rows as compact text
for hand classification. HTML is stripped to keep the symptom text.

Usage: python3 screen.py [N] [OFFSET]
"""
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    off = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    rows = [json.loads(l) for l in open("pool.jsonl")]
    rows = rows[off:off + n]
    for i, r in enumerate(rows):
        print("=" * 70)
        print("[%d] qid=%s views=%s score=%s ans=%s closed=%s"
              % (off + i, r["question_id"], r.get("view_count"),
                 r.get("score"), r.get("answer_count"),
                 r.get("closed_reason") or "-"))
        print("TITLE: " + strip(r.get("title", "")))
        print("BODY: " + strip(r.get("body", ""))[:600])


if __name__ == "__main__":
    main()

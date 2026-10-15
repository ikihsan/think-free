#!/usr/bin/env python3
"""E143 make-sheet: dump a compact screening sheet of all fetched rows.

Output: screening-sheet.txt with one block per row:
  idx | arm | views | score | answers | title | body(truncated)
Screening reads title+body only (PROTOCOL.md). The agent classifies
each row and writes screening.jsonl.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main():
    d = json.load(open(os.path.join(HERE, "pool-raw.json")))
    rows = []
    idx = 0
    for arm in ("A_votes", "B_creation"):
        for page in d[arm]:
            for it in page.get("items", []):
                rows.append({
                    "idx": idx,
                    "arm": arm,
                    "question_id": it["question_id"],
                    "view_count": it["view_count"],
                    "score": it["score"],
                    "answer_count": it["answer_count"],
                    "title": strip_html(it["title"]),
                    "body": strip_html(it.get("body", ""))[:700],
                    "tags": it.get("tags", []),
                })
                idx += 1
    with open(os.path.join(HERE, "screening-sheet.txt"), "w") as fh:
        for r in rows:
            fh.write(f"[{r['idx']}] {r['arm']} views={r['view_count']} "
                     f"score={r['score']} ans={r['answer_count']} "
                     f"tags={','.join(r['tags'][:4])}\n")
            fh.write(f"  T: {r['title']}\n")
            fh.write(f"  B: {r['body']}\n\n")
    with open(os.path.join(HERE, "screening-rows.json"), "w") as fh:
        json.dump(rows, fh)
    print(f"wrote {len(rows)} rows to screening-sheet.txt")


if __name__ == "__main__":
    main()

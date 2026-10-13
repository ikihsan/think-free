#!/usr/bin/env python3
"""E126 screening sheet: title + body (HTML stripped) per row.

Screening is done by the model reading this sheet, row by row --
not by a keyword classifier (E113/F116: an unanchored substring
classifier labelled only 28% of a representative pool). The sheet
is committed; classifications land in screening.jsonl.
"""
import html
import json
import os
import re

TAG = re.compile(r"<[^>]+>")
HERE = os.path.dirname(os.path.abspath(__file__))


def strip(body):
    text = TAG.sub(" ", body or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def main():
    d = json.load(open(os.path.join(HERE, "pool-raw.json")))
    rows = []
    for arm, pages in d.items():
        for page in pages:
            for it in page["items"]:
                rows.append({
                    "question_id": it["question_id"],
                    "arm": arm,
                    "view_count": it["view_count"],
                    "answer_count": it["answer_count"],
                    "tags": it.get("tags", []),
                    "title": html.unescape(it["title"]),
                    "body": strip(it.get("body", ""))[:500],
                })
    rows.sort(key=lambda r: (r["arm"], -r["view_count"]))
    with open(os.path.join(HERE, "screening-sheet.json"), "w") as fh:
        json.dump(rows, fh, indent=1)
    with open(os.path.join(HERE, "screening-sheet.txt"), "w") as fh:
        for n, r in enumerate(rows, 1):
            fh.write(f"### {n} | id={r['question_id']} | {r['arm']} | "
                     f"views={r['view_count']} | answers={r['answer_count']} | "
                     f"tags={','.join(r['tags'])}\n")
            fh.write(f"TITLE: {r['title']}\n")
            fh.write(f"BODY: {r['body']}\n\n")
    print(f"wrote {len(rows)} rows")


if __name__ == "__main__":
    main()

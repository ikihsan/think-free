#!/usr/bin/env python3
"""E070 - build the classification sample (AMENDMENT-1).

Top 10 items per query in the API's own order (the first
page a browser sees), deduplicated across queries and
venues by the venue's own id, first query owns the row.
Writes raw/sample.tsv: id, venue, qclass, query, title,
body excerpt (first 1500 chars, newlines folded).

The API responses in raw/api/ are the only input; this
script adds no judgment. Stdlib only.
"""
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
API = os.path.join(HERE, "raw", "api")
# Amendment 4: controls (PC) are classified to the full
# fetched page; the prevalence sample (G) and placebo (PL)
# keep the 12-row cap of Amendment 1.
PER_QUERY = {"PC": 25, "G": 12, "PL": 12}
BODY_CHARS = 1500


def fold(text, n):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:n]


def main():
    files = sorted(glob.glob(os.path.join(API, "se-*.json")))
    files += sorted(glob.glob(os.path.join(API, "gh-*.json")))
    seen = {}
    order = []
    for path in files:
        if path.endswith("manifest.json"):
            continue
        d = json.load(open(path))
        venue = "stackexchange" if "se-" in os.path.basename(path) \
            else "github"
        cap = PER_QUERY.get(d["class"], 12)
        for it in d["items"][:cap]:
            rid = str(it.get("question_id") or it.get("id")
                      or it.get("number"))
            if rid in seen:
                continue
            seen[rid] = True
            order.append({
                "id": rid, "venue": venue,
                "qclass": d["class"], "query": d["query"],
                "title": fold(it.get("title"), 200),
                "body": fold(it.get("body")
                             or it.get("body_text"), BODY_CHARS),
            })
    out = os.path.join(HERE, "raw", "sample.tsv")
    with open(out, "w") as f:
        f.write("id\tvenue\tqclass\tquery\ttitle\tbody\n")
        for r in order:
            f.write("\t".join(
                str(r[k]).replace("\t", " ").replace("\n", " ")
                for k in ("id", "venue", "qclass", "query",
                          "title", "body")) + "\n")
    import collections
    c = collections.Counter(r["qclass"] for r in order)
    print("sample rows:", len(order), dict(c))
    print("wrote", out)


if __name__ == "__main__":
    main()

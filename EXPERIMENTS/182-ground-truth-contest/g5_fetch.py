#!/usr/bin/env python3
"""E182 G5: fetch answer bodies for the 5 most contested and 5 most decisive
rows, so the measure can be checked against real answers rather than against
near-copies of itself.

This is the only stage that puts an answer body on disk, and it does so for
10 named rows chosen by states.json -- never by arm, never by the assistant's
verdict. Bodies go to raw/se-bodies.jsonl with URL and quota beside them.

Usage: python3 g5_fetch.py
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SE = "https://api.stackexchange.com/2.3"
UA = "think-free-e182/1.0"

# qids in order: 5 highest runner_up/top among `contested`, then 5 highest
# runner_up/top among `decisive`. Fixed here rather than recomputed so a
# change in states.json cannot silently change what the reader checked.
G5_QIDS = [79824381, 79408101, 79537353, 79796450, 79663905,
           79589468, 79791886, 79556333, 79843062, 79600161]

# See bodies.py: the only match in this corpus is a public answer naming an
# environment variable, and the suppression is declared and logged.
ALLOW = "# origin-allow-secret-patterns: assigned-credential\n"

def se(path, params, note=None):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=60) as fh:
        body = json.loads(fh.read().decode("utf-8"))
    rec = {"url": url, "note": note, "body": body}
    target = os.path.join(RAW, "se-bodies.jsonl")
    if not os.path.exists(target):
        with open(target, "w") as out:
            out.write(ALLOW)
    with open(target, "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return body


def main():
    states = {r["qid"]: r for r in json.load(open(
        os.path.join(HERE, "states.json")))["rows"]}
    missing = [q for q in G5_QIDS if q not in states]
    if missing:
        raise SystemExit("qids absent from states.json: %s" % missing)

    out = {}
    for q in G5_QIDS:
        body = se("questions/%d/answers" % q,
                  {"site": "stackoverflow", "filter": "withbody",
                   "pagesize": 100, "sort": "votes"},
                  note="G5 body fetch qid=%d" % q)
        items = body.get("items", [])
        by_score = sorted(items, key=lambda a: (-(a.get("score") or 0),
                                                a.get("creation_date") or 0,
                                                a.get("answer_id") or 0))
        out[str(q)] = [{"answer_id": a.get("answer_id"),
                        "score": a.get("score"),
                        "is_accepted": a.get("is_accepted"),
                        "body": a.get("body", "")} for a in by_score]
        top = out[str(q)][0]["score"] if out[str(q)] else None
        ru = out[str(q)][1]["score"] if len(out[str(q)]) > 1 else None
        print("  qid %d: %d answers, scores.json said top=%s ru=%s -> %s/%s"
              % (q, len(out[str(q)]), states[q]["top"], states[q]["runner_up"],
                 top, ru))

    with open(os.path.join(HERE, "g5-bodies.json"), "w") as fh:
        json.dump({"rows": out, "qids": G5_QIDS}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("g5-bodies.json: %d rows" % len(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
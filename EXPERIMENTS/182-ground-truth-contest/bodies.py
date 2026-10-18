#!/usr/bin/env python3
"""E182 stage 3: fetch answer bodies for all 60 scored rows, for the
prescriptive-overlap instrument declared in AMENDMENT 1.

Reads no assistant answer and no arm label: the qid list comes from scores.json
and nothing else is joined until stage 4. Bodies go to raw/se-bodies.jsonl
with their URL, quota probe beside them, so the bytes are auditable (D061).

Usage: python3 bodies.py [--limit N]
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
CHUNK = 20


def se(path, params, note=None):
    url = "%s/%s?%s" % (SE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/json"})
    os.makedirs(RAW, exist_ok=True)
    with urllib.request.urlopen(req, timeout=60) as fh:
        body = json.loads(fh.read().decode("utf-8"))
        head = {k: v for k, v in fh.headers.items()}
    rec = {"url": url, "note": note, "headers": head, "body": body}
    with open(os.path.join(RAW, "se-bodies.jsonl"), "a") as out:
        out.write(json.dumps(rec, sort_keys=True) + "\n")
    time.sleep(1.2)
    return body, rec


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    qids = sorted(int(k) for k in json.load(
        open(os.path.join(HERE, "scores.json")))["rows"])
    if limit:
        qids = qids[:limit]
    print("population: %d qids" % len(qids))

    out = {}
    for i in range(0, len(qids), CHUNK):
        part = qids[i:i + CHUNK]
        page, more, got = 1, True, 0
        while more:
            body, _ = se("questions/%s/answers" % ";".join(str(q) for q in part),
                         {"site": "stackoverflow", "filter": "withbody",
                          "pagesize": 100, "sort": "votes", "page": page},
                         note="overlap instrument body fetch")
            items = body.get("items", [])
            for a in items:
                out.setdefault(str(a["question_id"]), []).append(
                    {"answer_id": a.get("answer_id"),
                     "score": a.get("score"),
                     "creation_date": a.get("creation_date"),
                     "is_accepted": a.get("is_accepted"),
                     "body": a.get("body", "")})
                got += 1
            more = bool(body.get("has_more"))
            if more:
                page += 1
        print("  chunk %d: qids %d..%d -> %d answers" % (i // CHUNK + 1,
                                                          part[0], part[-1], got))

    # One ordered list per question: top-voted first, then earliest, then
    # lowest id -- E177's own tie-break, so answer[0] is the key answer whose
    # score scores.json already reproduced.
    for q, answers in out.items():
        answers.sort(key=lambda a: (-(a["score"] or 0), a["creation_date"] or 0,
                                    a["answer_id"] or 0))

    with open(os.path.join(HERE, "bodies.json"), "w") as fh:
        json.dump({"rows": out, "qids": qids}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("bodies.json: %d rows, %d answers total"
          % (len(out), sum(len(v) for v in out.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
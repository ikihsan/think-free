#!/usr/bin/env python3
"""E026 fetch: the text of each of E022's 1401 need comments.

Same endpoint and same failure discipline as EXPERIMENTS/022: a failed read is
`unreadable`, never `answered`/`unanswered`; a decided row is never
overwritten; concurrency bounded; partial capture is a fact about how far the
run got.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
OUT = os.path.join(os.path.dirname(__file__), "raw", "texts.jsonl")
SRC = os.path.join(os.path.dirname(__file__), "..", "022-need-outcomes", "raw", "outcomes.jsonl")


def fetch(cid):
    try:
        with urllib.request.urlopen(FIREBASE % cid, timeout=25) as r:
            item = json.load(r)
        if item is None:
            return {"comment_id": str(cid), "status": "missing"}
        return {
            "comment_id": str(cid),
            "status": "ok",
            "text": item.get("text", ""),
            "dead": bool(item.get("dead")),
            "deleted": bool(item.get("deleted")),
        }
    except urllib.error.HTTPError as e:
        return {"comment_id": str(cid), "status": "http_%s" % e.code}
    except Exception as e:  # noqa: BLE001
        return {"comment_id": str(cid), "status": "error:%s" % type(e).__name__}


def main():
    rows = [json.loads(l) for l in open(SRC)]
    done = {}
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            if r["status"] == "ok":
                done[r["comment_id"]] = r
    todo = [r for r in rows if str(r["comment_id"]) not in done]
    print("todo:", len(todo), "done:", len(done))
    with open(OUT, "a") as f:
        with ThreadPoolExecutor(max_workers=8) as ex:
            for r in ex.map(lambda r: fetch(r["comment_id"]), todo):
                f.write(json.dumps(r) + "\n")
                f.flush()


if __name__ == "__main__":
    main()

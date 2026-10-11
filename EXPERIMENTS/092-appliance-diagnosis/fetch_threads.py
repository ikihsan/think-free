#!/usr/bin/env python3
"""E092 thread fetch: answers and comments for the 40 sample rows.

The first read of thread content. Two batched requests:
/2.3/questions/{ids}/answers and /2.3/questions/{ids}/comments.
"""
import json
import sys
import time
import urllib.error
import urllib.request

SITE = "diy"


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            d = json.loads(r.read().decode())
        return d.get("items", []), {"status": 200,
                                    "quota_remaining": d.get("quota_remaining"),
                                    "error": None}
    except urllib.error.HTTPError as e:
        return [], {"status": e.code, "quota_remaining": None,
                    "error": e.read().decode()[:200]}


def main():
    sample = [json.loads(l) for l in open("attempts.jsonl")]
    ids = [str(r["qid"]) for r in sample]
    assert len(ids) == 40
    log = []

    def fetch_all(kind):
        items = []
        for page in (1, 2, 3):
            url = ("https://api.stackexchange.com/2.3/questions/%s/%s"
                   "?site=%s&pagesize=100&page=%d&filter=withbody"
                   % (";".join(ids), kind, SITE, page))
            page_items, meta = get(url)
            meta["page"] = page
            meta["items_returned"] = len(page_items)
            log.append({"what": kind, "url": url, **meta})
            items.extend(page_items)
            if len(page_items) < 100:
                break
            time.sleep(0.5)
        return items

    answers = fetch_all("answers")
    print("answers: %d items, quota %s"
          % (len(answers), log[-1]["quota_remaining"]))
    time.sleep(0.5)
    comments = fetch_all("comments")
    print("comments: %d items, quota %s"
          % (len(comments), log[-1]["quota_remaining"]))

    with open("threads.jsonl", "w") as f:
        for r in sample:
            f.write(json.dumps({
                "qid": r["qid"],
                "answers": [a for a in answers
                            if a.get("question_id") == r["qid"]],
                "comments": [c for c in comments
                             if c.get("post_id") == r["qid"]],
            }) + "\n")
    with open("thread-fetch-log.jsonl", "w") as f:
        for e in log:
            f.write(json.dumps(e) + "\n")
    covered = 0
    for r in sample:
        a = [x for x in answers if x.get("question_id") == r["qid"]]
        if a:
            covered += 1
    print("threads with >=1 answer: %d of 40" % covered)


if __name__ == "__main__":
    main()

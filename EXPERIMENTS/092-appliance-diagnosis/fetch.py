#!/usr/bin/env python3
"""E092 fetch: the unanswered `appliances` pool on Home Improvement SE.

Fetches every page of /2.3/search/advanced (site=diy, tagged=appliances,
answered=false), ranked locally by view_count. Records each request's
metadata so the harvest reconciles against the API's own counts (D082:
a route that returns nothing is a missing observation, never a zero).

Usage:
    python3 fetch.py            # fetch the pool -> pool.jsonl, fetch-log.jsonl
    python3 fetch.py --verify   # re-check every recorded request against the API
"""
import json
import sys
import time
import urllib.error
import urllib.request

API = "https://api.stackexchange.com/2.3/search/advanced"
PARAMS = ("site=diy&tagged=appliances&answered=false"
          "&sort=votes&order=desc&pagesize=100&filter=withbody")
OUT = "pool.jsonl"
LOG = "fetch-log.jsonl"


def get(url):
    """One request. Returns (items, meta). HTTP errors are recorded, not raised."""
    meta = {"url": url, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        meta.update(status=e.code, error=e.read().decode()[:300],
                    items_returned=0, has_more=None, quota_remaining=None)
        return [], meta
    meta.update(status=200, bytes=len(json.dumps(d)),
                items_returned=len(d.get("items", [])),
                has_more=d.get("has_more"),
                quota_remaining=d.get("quota_remaining"),
                quota_max=d.get("quota_max"),
                backoff=d.get("backoff"), error=None)
    return d.get("items", []), meta


def main():
    verify = "--verify" in sys.argv
    if verify:
        log = [json.loads(l) for l in open(LOG)]
        bad = 0
        for entry in log:
            if entry.get("status") != 200:
                continue
            items, meta = get(entry["url"])
            if items != entry.get("_items"):
                bad += 1
                print("MISMATCH", entry["url"], "got", len(items))
        print("verify: %d recorded 200-requests, %d mismatches" % (len(log), bad))
        return

    seen = {}
    log = []
    page = 1
    while True:
        url = "%s?%s&page=%d" % (API, PARAMS, page)
        items, meta = get(url)
        meta["page"] = page
        log.append(meta)
        print("page %d: %d items, has_more=%s, quota=%s"
              % (page, meta["items_returned"], meta["has_more"],
                 meta["quota_remaining"]))
        for it in items:
            seen[it["question_id"]] = it
        if not meta["has_more"] or not items:
            break
        page += 1
        time.sleep(0.3)

    with open(OUT, "w") as f:
        for qid in sorted(seen, key=lambda q: -seen[q].get("view_count", 0)):
            f.write(json.dumps(seen[qid]) + "\n")
    with open(LOG, "w") as f:
        for e in log:
            f.write(json.dumps(e) + "\n")

    rows = list(seen.values())
    print("pool: %d unique questions, %d with body text"
          % (len(rows), sum(1 for r in rows if r.get("body"))))
    print("top view_count: %s" % [r.get("view_count") for r in rows[:5]])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Arm B — fresh needs from three Stack Exchange sites E062 did not use.

Unauthenticated /search/advanced, as F059 recorded, with the site's own fields.
Declared populations: `outdoor`, `knitting`, `space` -- none of them is one of
E062's six (cooking, gardening, bicycles, woodworking, diy, astronomy), so this
arm is a different population and not a re-read.

Sites are queried oldest-first inside a fixed window so the sample is not the
Active tab, which E034 measured hides the tail. Every response is reconciled
against the API's own `items_returned`; `total_count` is requested and, where the
route does not return it, its absence is recorded as a missing observation
(D082), never as a zero.

Stdlib only. Run from this directory.
"""
from __future__ import print_function

import gzip
import io
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

SITES = ["outdoor", "knitting", "space"]
PER_SITE = 12
# 2023-01-01 .. 2024-12-31 creation window: old enough to have a settled outcome
# field, recent enough to avoid the archaic tail E062's "cooking" rows carried.
AFTER = 1672531200
BEFORE = 1735689600
UA = "think-free-remedy-existence/0.1 (research; no tracking)"
CTX = ssl.create_default_context()


def search(site, pages=3):
    rows, total = [], None
    for page in range(1, pages + 1):
        q = {
            "site": site,
            "pagesize": "50",
            "order": "asc",
            "sort": "creation",
            "fromdate": str(AFTER),
            "todate": str(BEFORE),
            "filter": "withbody",
            "page": str(page),
        }
        url = "https://api.stackexchange.com/2.3/search/advanced?" + \
              urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=40, context=CTX) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
        except Exception as exc:                        # noqa: BLE001
            print("  %s page %d: %s" % (site, page, exc))
            continue
        if "total" in data:
            total = data["total"]
        items = data.get("items", [])
        print("  %s page %d: %d items (quota %s)"
              % (site, page, len(items), data.get("quota_remaining")))
        rows.extend(items)
        if data.get("backoff"):
            time.sleep(data["backoff"] + 1)
        time.sleep(0.3)
    return rows, total


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    out = []
    for site in SITES:
        print("== %s" % site)
        rows, total = search(site)
        kept = 0
        for q in rows:
            if kept >= PER_SITE:
                break
            body = q.get("body", "") or ""
            if len(body) < 400:
                continue
            out.append({
                "site": site,
                "question_id": q.get("question_id"),
                "title": q.get("title", ""),
                "body": " ".join(body.split())[:1200],
                "view_count": q.get("view_count"),
                "answer_count": q.get("answer_count"),
                "score": q.get("score"),
                "link": q.get("link"),
            })
            kept += 1
        print("  kept %d of %d fetched; API total_count=%s"
              % (kept, len(rows), total))
    path = os.path.join(RAW, "needs-B.jsonl")
    with open(path, "w") as fh:
        for r in out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print("wrote %s (%d rows)" % (path, len(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

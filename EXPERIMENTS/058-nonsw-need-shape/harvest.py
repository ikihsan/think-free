#!/usr/bin/env python3
"""E058 arm 1 harvest: never-answered questions on six non-software Stack
Exchange sites.

Declared in EXPERIMENTS/058-nonsw-need-shape/PROTOCOL.md and restated for this
venue in AMENDMENT-1.md. Writes every request, its status and its body to
raw/requests.jsonl, and every recovered row to raw/arm1.jsonl.

Standard library only. Reproduce:

    python3 EXPERIMENTS/058-nonsw-need-shape/harvest.py
"""

import gzip
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

SITES = ["cooking", "gardening", "bicycles", "woodworking", "diy", "astronomy"]

# ATTEMPT 1 used filter=!nNPvSNdWme and recovered 1200 rows with every outcome
# field but **no body**, because a custom filter replaces the default field set.
# The rubric reads the question's text, so the population was unusable. Kept in
# raw/attempt1-*.jsonl. Attempt 2 names the fields it needs instead.
#
# G1 also asked for reconciliation against each site's own total_count. That
# field is **not returned by the /questions route at all** -- only /search/* and
# /questions/{ids} carry it -- so it is recorded as a missing observation, never
# as a zero (D081). The reconciliation that is available is has_more plus
# items_returned per request, and both are written per row.
FILTER = "withbody"

# sort=votes&order=asc is the score tail: the questions nobody upvoted, which is
# the population E034 and E035 already used for the software arm. Two pages per
# site, 100 rows each.
PAGES = 2
PER_PAGE = 100
UA = "think-free-E058/1.0 (research harvest; unauthenticated)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return resp.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:  # network, DNS, timeout: recorded, never counted as a zero
        return "ERR", repr(exc)


def main():
    os.makedirs(RAW, exist_ok=True)
    reqs = open(os.path.join(RAW, "requests.jsonl"), "a")
    rows = open(os.path.join(RAW, "arm1.jsonl"), "a")
    recovered = 0
    for site in SITES:
        for page in range(1, PAGES + 1):
            url = ("https://api.stackexchange.com/2.3/questions"
                   "?site=%s&pagesize=%d&page=%d&sort=votes&order=asc"
                   "&filter=%s" % (site, PER_PAGE, page, FILTER))
            status, body = fetch(url)
            parsed, err = None, None
            try:
                parsed = json.loads(body)
            except Exception as exc:
                err = repr(exc)
            items = (parsed or {}).get("items") or []
            rec = {"url": url, "site": site, "page": page, "status": status,
                   "bytes": len(body), "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                             time.gmtime()),
                   "has_more": (parsed or {}).get("has_more"),
                   "quota_max": (parsed or {}).get("quota_max"),
                   "backoff": (parsed or {}).get("backoff"),
                   "total_count": (parsed or {}).get("total_count"),  # null on this route by design; see D081 note
                   "items_with_body": sum(1 for x in items if x.get("body")),
                   "items_returned": len(items),
                   "parse_error": err,
                   "error_items": (parsed or {}).get("error_id")}
            reqs.write(json.dumps(rec) + "\n")
            reqs.flush()
            for it in items:
                it["_site"] = site
                it["_page"] = page
                rows.write(json.dumps(it) + "\n")
                recovered += 1
            print("%-12s page %d status %s items %d total_count %s" %
                  (site, page, status, len(items), rec["total_count"]))
            time.sleep(1.2)  # stay well inside the unauthenticated quota
    reqs.close()
    rows.close()
    print("rows recovered: %d" % recovered)


if __name__ == "__main__":
    main()

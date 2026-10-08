#!/usr/bin/env python3
"""E058 arm 2 harvest: the matched software-domain control.

Arm 1 is six non-software Stack Exchange sites in their score tail. Arm 2 is
four software/IT sites, same route, same filter, same pages, same tail -- so the
only thing that differs is the domain. That is what makes the two fractions
comparable; see PROTOCOL.md and AMENDMENT-2.md for why the Hacker News need
corpus could not serve as this control.

Standard library only. Reproduce:

    python3 EXPERIMENTS/058-nonsw-need-shape/harvest2.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harvest  # noqa: E402  (same directory, deliberate)

SITES = ["stackoverflow", "superuser", "serverfault", "unix"]
# Attempt 1 asked for two pages per site and the unauthenticated route answered
# 400 then 429: the first site returned one page, the rest returned nothing.
# Per D081 those responses are **missing observations, not zeros**, and they are
# in raw/requests-arm2.jsonl as they happened. Attempt 2 asks for one page per
# site, honours the API's own `backoff` field, and retries a 429 rather than
# reading it as an absence.
PAGES = 1
SLEEP = 6.0
RETRIES = 3


def fetch_with_backoff(url):
    """One logical request. Returns (status, body, record). A 429 or a 400 is
    retried after the API's own backoff; if it never succeeds it is returned as
    the failure it is, and the caller records it as a missing observation."""
    rec = {"url": url}
    for attempt in range(1, RETRIES + 1):
        status, body = harvest.fetch(url)
        rec["attempt"] = attempt
        rec["status"] = status
        rec["bytes"] = len(body)
        if status == 200:
            return status, body, rec
        time.sleep(8.0 * attempt)
    return status, body, rec


def main():
    os.makedirs(harvest.RAW, exist_ok=True)
    reqs = open(os.path.join(harvest.RAW, "requests-arm2.jsonl"), "a")
    rows = open(os.path.join(harvest.RAW, "arm2.jsonl"), "a")
    recovered = 0
    for site in SITES:
        for page in range(1, PAGES + 1):
            url = ("https://api.stackexchange.com/2.3/questions"
                   "?site=%s&pagesize=%d&page=%d&sort=votes&order=asc"
                   "&filter=%s" % (site, harvest.PER_PAGE, page, harvest.FILTER))
            status, body, base = fetch_with_backoff(url)
            parsed, err = None, None
            try:
                parsed = json.loads(body)
            except Exception as exc:
                err = repr(exc)
            items = (parsed or {}).get("items") or []
            rec = dict(base)
            rec.update({"site": site, "page": page,
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "has_more": (parsed or {}).get("has_more"),
                        "quota_max": (parsed or {}).get("quota_max"),
                        "quota_remaining": (parsed or {}).get("quota_remaining"),
                        "total_count": (parsed or {}).get("total_count"),
                        "items_returned": len(items),
                        "items_with_body": sum(1 for x in items if x.get("body")),
                        "parse_error": err,
                        "error_items": (parsed or {}).get("error_id"),
                        "error_message": (parsed or {}).get("error_message")})
            reqs.write(json.dumps(rec) + "\n")
            reqs.flush()
            if status != 200:
                print("%-14s page %d status %s -- NO OBSERVATION, not a zero"
                      % (site, page, status))
                continue
            for it in items:
                it["_site"] = site
                it["_page"] = page
                rows.write(json.dumps(it) + "\n")
                recovered += 1
            print("%-14s page %d status %s items %d"
                  % (site, page, status, len(items)))
            time.sleep(SLEEP)
    reqs.close()
    rows.close()
    print("rows recovered: %d" % recovered)


if __name__ == "__main__":
    main()

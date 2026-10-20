#!/usr/bin/env python3
"""E143 fetch: two declared arms of Cross Validated's unanswered pool.

Arm A: sort=votes   (2 pages of 100) -- the vote stratum, limitation declared.
Arm B: sort=creation (1 page of 100) -- the newest stratum.

Both: accepted=false (no accepted answer), fromdate=2025-01-01,
site=stats, filter=withbody. Raw JSON is committed verbatim;
screening happens in screen.py from title+body only.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.stackexchange.com/2.3/search/advanced"
FROMDATE = 1735689600  # 2025-01-01T00:00:00Z, declared in PROTOCOL.md


def fetch(arm, sort, page):
    params = {
        "site": "stats",
        "accepted": "false",
        "fromdate": str(FROMDATE),
        "sort": sort,
        "order": "desc",
        "pagesize": "100",
        "page": str(page),
        "filter": "withbody",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        req = urllib.request.Request(
            url, headers={"User-Agent": "think-free-e143/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            for _ in range(1):  # backoff handled inline
                if data.get("backoff"):
                    print(f"backoff {data['backoff']}s", file=sys.stderr)
                    time.sleep(data["backoff"])
            return data
        except urllib.error.HTTPError as exc:
            body = exc.read().decode()[:200]
            print(f"HTTP {exc.code} on {arm} p{page}: {body}",
                  file=sys.stderr)
            if exc.code in (400, 429, 502) and attempt < 5:
                wait = 20 * (attempt + 1)
                print(f"waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("unreachable")


def main():
    out = {}
    for arm, sort, pages in (("A_votes", "votes", 2), ("B_creation", "creation", 1)):
        pages_out = []
        for page in range(1, pages + 1):
            data = fetch(arm, sort, page)
            pages_out.append(data)
            print(f"{arm} page {page}: {len(data.get('items', []))} items, "
                  f"quota {data.get('quota_remaining')}", file=sys.stderr)
        out[arm] = pages_out
    import os
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "pool-raw.json")
    with open(outpath, "w") as fh:
        json.dump(out, fh)
    print(f"wrote {outpath}", file=sys.stderr)


if __name__ == "__main__":
    main()

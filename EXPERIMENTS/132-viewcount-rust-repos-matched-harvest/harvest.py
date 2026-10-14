#!/usr/bin/env python3
"""E132 — harvest ONE matched pool for the view-count control (Rust repos).

Stdlib only. Writes raw_pool.json.
"""
from __future__ import print_function

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_pool.json")

# One query. Identical for both arms by construction - there is only one arm.
STRATA = [
    (100, 200), (200, 500), (500, 1000), (1000, 2000),
    (2000, 5000), (5000, 10000), (10000, 20000),
]
PER_STRATUM = 100
HEADERS = {
    "User-Agent": "origin-mission-E132",
    "Accept": "application/vnd.github.v3+json",
}

# Fields kept.
KEEP = (
    "full_name", "stargazers_count", "forks_count", "open_issues_count",
    "created_at", "pushed_at", "updated_at", "description", "topics",
    "language", "archived", "fork", "size",
)


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print("  HTTP %s %s" % (exc.code, exc.reason))
        return {}
    except Exception as exc:  # noqa: BLE001 - network failure is data here
        print("  error: %s" % exc)
        return {}


def main():
    pool = []
    seen = set()
    for low, high in STRATA:
        stratum = "stars:%d..%d" % (low, high)
        params = {
            "q": "language:rust " + stratum,
            "sort": "stars",
            "order": "desc",
            "per_page": PER_STRATUM,
        }
        url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(params)
        print("stratum %s" % stratum)
        data = fetch(url)
        items = data.get("items") or []
        added = 0
        for item in items:
            name = item.get("full_name")
            if not name or name in seen:
                continue
            seen.add(name)
            row = {k: item.get(k) for k in KEEP}
            row["harvest_query"] = "language:rust " + stratum
            row["harvest_stratum"] = stratum
            pool.append(row)
            added += 1
        print("  +%d rows" % added)
        time.sleep(3)

    with open(RAW, "w") as fh:
        json.dump(pool, fh, indent=1, sort_keys=True)
    print("pool rows: %d -> %s" % (len(pool), RAW))
    if pool:
        stars = sorted(r["stargazers_count"] for r in pool)
        print("star range observed: %d .. %d (median %d)"
              % (stars[0], stars[-1], stars[len(stars) // 2]))
        for low, high in STRATA:
            stratum = "stars:%d..%d" % (low, high)
            n = sum(1 for r in pool if r["harvest_stratum"] == stratum)
            print("  %-18s %d rows" % (stratum, n))


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""E041 screening (AMENDMENT-1): which repositories can supply a positive control?

Ten search requests, no capture. The platform's own `reason:duplicate` label says
which repositories actually duplicate-close; counting the rows that name a
parseable target per repository says which ones can supply a *pair*, which is the
thing the control needs and the thing a by-name list of famous libraries got wrong
by a factor of ~1800.

The six reference patterns are imported from arms.py, so the screening and the
capture parse targets with the same rule and cannot disagree.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from arms import target_ref  # noqa: E402

UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}
# AMENDMENT-1 CORRECTION: `stars:>500` is withdrawn. Measured, not assumed --
# it takes this population from 358,471 to 107 and to 0 with `in:body`. A
# qualifier that looks like a free precision filter and discards the population
# is a property of the instrument's selection, and this is the tenth instance of
# that shape (F055, F058, F059) and the first caught before the measurement.
QUERY = 'is:issue reason:duplicate "duplicate of #"'
PAGES = 10
PAGE = 100
MIN_INTERVAL = 6.6

# Declared in AMENDMENT-1 "The by-name list", so screening and capture agree.
BY_NAME = ["pallets/click", "tiangolo/typer", "psf/requests", "pytest-dev/pytest",
           "vuejs/vue", "d3/d3", "rust-lang/cargo", "scrapy/scrapy",
           "tornado/tornado", "jupyter/notebook"]
TAKE = 6


def search(page):
    url = ("https://api.github.com/search/issues?q=%s&per_page=%d&page=%d"
           % (urllib.parse.quote_plus(QUERY), PAGE, page))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=90) as r:
                return json.load(r), None
        except urllib.error.HTTPError as exc:
            # AMENDMENT-1: a non-retryable status is recorded, not slept on.
            if exc.code in (403, 422, 400, 401):
                return None, "HTTPError %s" % exc.code
            time.sleep(15.0 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001
            time.sleep(15.0 * (attempt + 1))
            last = repr(exc)[:160]
    return None, "exhausted"


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    rows = []
    total = None
    for page in range(1, PAGES + 1):
        d, err = search(page)
        if d is None:
            print("page %d failed: %s" % (page, err))
            break
        total = d.get("total_count")
        items = d.get("items") or []
        if not items:
            break
        rows.extend(items)
        print("page %d: %d rows (search reports %s total)" % (page, len(items), total))
        with open(os.path.join(RAW, "screen_raw.json"), "w") as fh:
            json.dump({"query": QUERY, "total_count": total, "items": rows}, fh)
        time.sleep(MIN_INTERVAL)

    refs = Counter()
    dups = Counter()
    for it in rows:
        repo = it["repository_url"].split("/repos/")[-1]
        dups[repo] += 1
        if target_ref(it.get("body") or "") is not None:
            refs[repo] += 1

    ranked = sorted(refs.items(), key=lambda kv: (-kv[1], kv[0]))
    picked = []
    for repo, n in ranked:
        if repo in BY_NAME:
            continue          # already captured by the declared list
        picked.append(repo)
        if len(picked) >= TAKE:
            break

    out = {"query": QUERY, "search_total_count": total, "rows": len(rows),
           "distinct_repos": len(dups), "rows_with_parseable_ref": sum(refs.values()),
           "parseable_rate": round(sum(refs.values()) / len(rows), 4) if rows else None,
           "ranked_by_refs": ranked[:40],
           "dup_rows_by_repo": dups.most_common(20),
           "by_name_already_captured": BY_NAME,
           "picked": picked,
           "note": "take = %d repositories by descending parseable-ref count, "
                   "ties by name ascending, excluding the by-name list" % TAKE}
    with open(os.path.join(RAW, "screen.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nparseable-ref rate over %d rows: %s" % (len(rows), out["parseable_rate"]))
    print("distinct repositories: %d" % len(dups))
    print("\ntop by parseable references:")
    for repo, n in ranked[:15]:
        print("  %-45s %3d refs  %3d dup rows" % (repo, n, dups[repo]))
    print("\npicked for complete capture: %s" % ", ".join(picked))
    return 0


if __name__ == "__main__":
    sys.exit(main())

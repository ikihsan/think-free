#!/usr/bin/env python3
"""E041 capture: the complete issue space of the declared and screened repositories.

One JSON line per issue, written to raw/corpus.jsonl before anything is computed.

Why complete rather than sampled: the positive control needs **both** members of a
judged pair inside one capture, and E040's control failed precisely because the
second member was not in the arm (F064). A repository's duplicate points at
another issue in the same repository, so capturing the repository whole guarantees
the target is present whenever it exists.

Two things this file had to learn from the platform, both recorded rather than
assumed:

  * **403 is the rate limit here, not a permission error.** The search API's
    unauthenticated limit is 10 requests per minute; a 403 carrying
    `X-RateLimit-Remaining: 0` is slept through until its reset, while any other
    403 is fatal. Treating all 403s as fatal -- the first version of this file --
    silently abandoned four repositories mid-run.
  * **A year-per-query split is mostly empty queries.** Ranges are split
    recursively instead: a range whose `total_count` exceeds the index's 1000-hit
    paging ceiling is halved and both halves are queued, so a repository whose
    history spans fifteen years costs a handful of requests rather than nineteen.

Resumable, and a repository whose captured count does not reconcile against the
API's own `total_count` is reported as unreconciled rather than padded.
"""
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CORPUS = os.path.join(RAW, "corpus.jsonl")
LOG = os.path.join(RAW, "capture_log.json")
SCREEN = os.path.join(RAW, "screen.json")
UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}

# Declared in PROTOCOL.md, in this order, not replaced by better yield.
BY_NAME = ["pallets/click", "tiangolo/typer", "psf/requests", "pytest-dev/pytest",
           "vuejs/vue", "d3/d3", "rust-lang/cargo", "scrapy/scrapy",
           "tornado/tornado", "jupyter/notebook"]

PAGE = 100
SPLIT_ABOVE = 950         # the search index refuses to page past 1000 hits
MIN_INTERVAL = 6.8        # seconds between search requests (limit is 10/min)
REQUEST_BUDGET = 1000
EPOCH = datetime.date(2000, 1, 1)
LAST = datetime.date(2026, 12, 31)
# Statuses that are never retried: 422 is a renamed repository, 401 is no token.
FATAL_STATUS = (401, 422)
SEARCH = "https://api.github.com/search/issues"


def _url(q, page):
    return ("%s?q=%s&per_page=%d&page=%d&sort=created&order=asc"
            % (SEARCH, urllib.parse.quote_plus(q), PAGE, page))


def _snooze(headers):
    """Pace from the platform's own headers, not from a guessed interval."""
    remaining = headers.get("X-RateLimit-Remaining")
    reset = headers.get("X-RateLimit-Reset")
    if remaining is not None and reset is not None:
        try:
            if int(remaining) <= 1:
                wait = int(reset) - int(time.time()) + 3
                return max(0, min(120, wait))
        except ValueError:
            pass
    return MIN_INTERVAL


def search(q, page, tries=4):
    """One search request. Returns (payload, headers, error).

    A 403 carrying `X-RateLimit-Remaining: 0` is the rate limit and is slept
    through; any other 403, and 401/422, are returned as errors so the caller
    records and skips instead of spinning.
    """
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(_url(q, page),
                                                               headers=UA),
                                        timeout=90) as r:
                return json.load(r), dict(r.headers), None
        except urllib.error.HTTPError as exc:
            headers = dict(exc.headers or {})
            remaining = headers.get("X-RateLimit-Remaining")
            if exc.code == 403 and remaining == "0":
                reset = headers.get("X-RateLimit-Reset")
                wait = (int(reset) - int(time.time()) + 5) if reset else 65
                print("  rate limited: sleeping %ds" % max(1, wait))
                time.sleep(max(1, min(180, wait)))
                continue
            if exc.code in FATAL_STATUS or (exc.code == 403 and remaining != "0"):
                return None, headers, "HTTPError %s" % exc.code
            last = "HTTPError %s" % exc.code
            time.sleep(20.0 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            last = repr(exc)[:200]
            time.sleep(20.0 * (attempt + 1))
    return None, {}, last or "exhausted"


def row(it, repo):
    return {"repo": repo, "number": it.get("number"),
            "title": it.get("title") or "", "body": it.get("body") or "",
            "state_reason": it.get("state_reason"), "state": it.get("state"),
            "author": (it.get("user") or {}).get("login"),
            "comments": it.get("comments"), "created_at": it.get("created_at"),
            "html_url": it.get("html_url")}


def page_query(q, repo, log, sink):
    rows, total, pages, errs = [], None, 0, []
    page = 1
    while True:
        d, headers, err = search(q, page)
        log["requests"] += 1
        if d is None:
            errs.append({"query": q, "page": page, "error": err})
            break
        if total is None:
            total = d.get("total_count")
        items = d.get("items") or []
        for it in items:
            r = row(it, repo)
            sink.write(json.dumps(r, sort_keys=True) + "\n")
            rows.append(r)
        pages += 1
        if not items or len(items) < PAGE or pages >= 11:
            break
        page += 1
        time.sleep(_snooze(headers))
    if len(rows) != (total or -1):
        log.setdefault("reconcile_mismatch", []).append(
            {"query": q, "repo": repo, "captured": len(rows), "total_count": total})
    return {"query": q, "pages": pages, "captured": len(rows),
            "total_count": total, "errors": errs,
            "duplicate_labelled": sum(1 for r in rows
                                      if r["state_reason"] == "duplicate")}


def _half(lo, hi):
    mid = lo + (hi - lo) // 2
    return (lo, mid), (mid + datetime.timedelta(days=1), hi)


def capture_repo(repo, log, sink):
    """Every issue in the repository, by recursive date-range paging."""
    d, headers, err = search("repo:%s is:issue" % repo, 1)
    log["requests"] += 1
    if d is None:
        return {"error": err}
    total = d.get("total_count")
    entry = {"total_count": total, "queries": []}
    if total <= SPLIT_ABOVE:
        entry["queries"].append(page_query("repo:%s is:issue" % repo, repo, log, sink))
        return entry

    queue = [(EPOCH, LAST)]
    while queue and log["requests"] < REQUEST_BUDGET:
        lo, hi = queue.pop(0)
        if lo > hi:
            continue
        q = "repo:%s is:issue created:%s..%s" % (repo, lo.isoformat(), hi.isoformat())
        c, ch, cerr = search(q, 1)
        log["requests"] += 1
        if c is None:
            entry["queries"].append({"query": q, "pages": 0, "captured": 0,
                                     "total_count": None, "errors": [{"error": cerr}],
                                     "duplicate_labelled": 0})
            continue
        n = c.get("total_count") or 0
        if n == 0:
            continue
        if n > SPLIT_ABOVE:
            a, b = _half(lo, hi)
            queue.extend([a, b])
            time.sleep(_snooze(ch))
            continue
        entry["queries"].append(page_query(q, repo, log, sink))
        time.sleep(_snooze(ch))
    return entry


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    log = {"requests": 0, "repos": {},
           "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if os.path.exists(LOG):
        try:
            with open(LOG) as fh:
                log = json.load(fh)
        except ValueError:
            pass

    screened = []
    if os.path.exists(SCREEN):
        with open(SCREEN) as fh:
            screened = json.load(fh).get("picked") or []
    order = [r for r in screened if r not in BY_NAME] + \
            [r for r in BY_NAME if r not in screened]

    # Only a reconciled repository is skipped. A previous run recorded four
    # repositories as HTTPError 403 and that set them to done, which meant the
    # rate-limit bug silently ended their capture instead of deferring it.
    done = {r for r, v in log["repos"].items() if v.get("reconciled")}

    with open(CORPUS, "a") as sink:
        for repo in order:
            if repo in done:
                print("skip %-42s already captured" % repo)
                continue
            if log["requests"] >= REQUEST_BUDGET:
                print("budget reached, stopping before %s" % repo)
                break
            entry = capture_repo(repo, log, sink)
            entry["set"] = "screened" if repo in screened else "by-name"
            if entry.get("error"):
                log["repos"][repo] = entry
                print("%-42s FAILED: %s" % (repo, entry["error"]))
                continue
            sink.flush()
            captured = sum(q.get("captured", 0) for q in entry["queries"])
            dups = sum(q.get("duplicate_labelled", 0) for q in entry["queries"])
            share = round(dups / captured, 4) if captured else None
            entry["captured"] = captured
            entry["duplicate_labelled"] = dups
            entry["duplicate_share"] = share
            entry["reconciled"] = captured == entry["total_count"]
            entry["excluded_automation"] = bool(share is not None and share > 0.20)
            log["repos"][repo] = entry
            with open(LOG, "w") as fh:
                json.dump(log, fh, indent=1, sort_keys=True)
            print("%-42s captured=%-6d total=%-6d dups=%-5d share=%-7s %s" % (
                repo, captured, entry["total_count"], dups, share,
                "EXCLUDED>0.20" if entry["excluded_automation"] else
                ("reconciled" if entry["reconciled"] else "UNRECONCILED")))

    log["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG, "w") as fh:
        json.dump(log, fh, indent=1, sort_keys=True)
    print("\nrequests=%d repos=%d corpus_lines=%d" % (
        log["requests"], len(log["repos"]),
        sum(1 for _ in open(CORPUS))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""E061 population probe, part 2: the incumbent trackers, with the repository
names corrected after part 1's 422s.

Part 1 recorded `repo:nedbat/coveragepy is:issue "without running"` and
`repo:jendriksegers/vulture is:issue "without running"` as HTTP 422 — the
`repo:` qualifier named a repository that does not exist under that owner
(coveragepy is `coveragepy/coveragepy`, 301-redirected from `nedbat/coveragepy`;
vulture is `jendrikseipp/vulture`, 4835 stars). A 422 is a defect in the
instrument, not a zero, so those two arms are re-run here and both are kept.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "raw")
API = "https://api.github.com/search/issues"

QUERIES = [
    ("inc:coveragepy-without-running", 'repo:coveragepy/coveragepy is:issue "without running"'),
    ("inc:vulture-without-running", 'repo:jendrikseipp/vulture is:issue "without running"'),
    ("voc:no-executed-tests", 'is:issue "0 tests" "exited" OR "exit code 0" "no tests"'),
]


def get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json", "User-Agent": "think-free-probe"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        return None, {"error": repr(exc)}


def main():
    path = os.path.join(OUT, "requests-2.jsonl")
    with open(path, "w") as fh:
        for i, (label, q) in enumerate(QUERIES):
            url = API + "?" + urllib.parse.urlencode({"q": q, "per_page": 30})
            status, body = get(url)
            items = body.get("items") or []
            rec = {"label": label, "query": q, "url": url, "status": status,
                   "total_count": body.get("total_count"), "error": body.get("error"),
                   "items": [{"id": it.get("id"), "title": it.get("title"),
                              "state": it.get("state"), "created_at": it.get("created_at"),
                              "comments": it.get("comments"), "url": it.get("html_url"),
                              "repo": "/".join((it.get("repository_url") or "").split("/")[-2:]),
                              "body": (it.get("body") or "")[:3000]} for it in items]}
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            print("%-30s status=%s total=%s items=%d %s"
                  % (label, status, rec["total_count"], len(items), rec["error"] or ""))
            sys.stdout.flush()
            if i != len(QUERIES) - 1:
                time.sleep(8)
    print("wrote", path)


if __name__ == "__main__":
    main()
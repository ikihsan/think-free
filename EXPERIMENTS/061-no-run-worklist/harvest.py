#!/usr/bin/env python3
"""E061 population probe.

Question: does a population exist of requesters who must locate *unexercised*
code without running the test suite, in a form the incumbents do not serve?

Method: public unauthenticated GitHub issue search (10 req/min), one query per
vocabulary used by a requester, one query per incumbent tracker. Every request
and its body are written to raw/requests.jsonl so a reader can check the
instrument.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUT, exist_ok=True)
API = "https://api.github.com/search/issues"

# (label, query).  Vocabulary first, then incumbent trackers: a request that names
# the incumbent is the strongest form of the population, a request that names the
# difficulty in the requester's own words is the weakest.
QUERIES = [
    ("voc:static-untested",
     'is:issue "without running the tests" untested'),
    ("voc:coverage-no-run",
     'is:issue "coverage" "without running the tests"'),
    ("voc:never-called",
     'is:issue "never called" "statically"'),
    ("voc:static-dead-code",
     'is:issue "find" "dead code" "statically" -label:good-first-issue'),
    ("inc:coveragepy",
     'repo:nedbat/coveragepy is:issue "without running"'),
    ("inc:pytest-cov",
     'repo:pytest-dev/pytest-cov is:issue "without running"'),
    ("inc:vulture",
     'repo:jendriksegers/vulture is:issue "without running"'),
]


def get(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "think-free-probe",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - record the failure, do not hide it
        return None, {"error": repr(exc)}


def main():
    path = os.path.join(OUT, "requests.jsonl")
    rows = []
    with open(path, "w") as fh:
        for i, (label, q) in enumerate(QUERIES):
            url = API + "?" + urllib.parse.urlencode({"q": q, "per_page": 30})
            status, body = get(url)
            total = body.get("total_count")
            items = body.get("items") or []
            rec = {
                "label": label,
                "query": q,
                "url": url,
                "status": status,
                "total_count": total,
                "incomplete_results": body.get("incomplete_results"),
                "items": [
                    {
                        "id": it.get("id"),
                        "title": it.get("title"),
                        "state": it.get("state"),
                        "created_at": it.get("created_at"),
                        "comments": it.get("comments"),
                        "repo": "/".join((it.get("repository_url") or "").split("/")[-2:]),
                        "url": it.get("html_url"),
                        "body_head": (it.get("body") or "")[:1200],
                    }
                    for it in items
                ],
                "error": body.get("error"),
            }
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            rows.append(rec)
            print("%-22s status=%s total=%s items=%d" % (label, status, total, len(items)))
            sys.stdout.flush()
            if i != len(QUERIES) - 1:
                time.sleep(7)
    print("wrote", path, len(rows), "requests")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Fetch the two primary facts 016 classifies on: a repository's root file
listing, and whether it has published a release.

Why these two and not the repository's name, description or topics: those are the
fields the phrase query matched on. Reading them back and calling the result "the
artifact's type" would be this experiment measuring its own subject.

The unauthenticated GitHub core budget is 60 requests an hour and this experiment
needs 2 per row over 56 rows, so every response is cached on disk under `raw/`
and a re-run costs nothing. A partial cache is a partial result and is reported as
one; `--only` restricts the work so the run can be spread across budget windows
without changing what any row means.

    python3 rootlisting.py --fetch
    python3 rootlisting.py --status
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CACHE = os.path.join(RAW, "rootlistings.json")
PREV = os.path.join(os.path.dirname(HERE), "015-incumbent-serving")

# The transport and its three-way answer (body / absent / refused) are shared with
# 015 rather than copied: a refusal must mean the same thing in both experiments
# or the join below compares two different vocabularies.
for path in (PREV, HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import attribution  # noqa: E402

EMPTY = "empty_or_missing"
REFUSED = "refused"


def contents(full_name):
    """Root file names and entry types, or a status string.

    `attribution.get` answers None for a genuine 404, and GitHub returns 404 for a
    repository with no commits. That is not an absence of content to classify —
    it is a repository this instrument cannot read — so it is named rather than
    folded into the document class, which is 015's own instrument correction
    (`verdict.INSTRUMENT_CORRECTION`) not repeated.
    """
    data = attribution.jget("https://api.github.com/repos/%s/contents/" % full_name,
                            timeout=30)
    if data is attribution.REFUSED:
        return REFUSED
    if data is None:
        return EMPTY
    if not isinstance(data, list):
        return REFUSED
    return [{"name": e.get("name"), "type": e.get("type"),
             "path": e.get("path")} for e in data if isinstance(e, dict)]


def releases(full_name):
    """How many releases exist, capped by the request at 1 page of 100.

    Existence is what the classification needs; the exact number is not read, so
    one request answers it and `per_page=100` is the cheap form of that question.
    """
    data = attribution.jget(
        "https://api.github.com/repos/%s/releases?per_page=100" % full_name,
        timeout=30)
    if data is attribution.REFUSED:
        return REFUSED
    if data is None:
        return 0
    if not isinstance(data, list):
        return REFUSED
    return len(data)


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE) as fh:
                cached = json.load(fh)
            if isinstance(cached, dict):
                return cached
        except ValueError:
            pass
    return {}


def population():
    """The 56 rows: 015's 30 mature incumbents, its 18 young cluster, its 5
    declared placebos and its 8 rebuilt placebo controls, each with its arm.

    Reused rather than re-searched. GitHub's unauthenticated search budget is 10
    a minute, so a fresh population would have been smaller and would not have
    been comparable to the serving figures already measured against these rows.
    """
    with open(os.path.join(PREV, "results.json")) as fh:
        prev = json.load(fh)
    rows = []
    for key, arm in (("incumbents", "mature"), ("cluster", "young")):
        for r in prev[key]:
            rows.append({"repo": r["repo"], "stars": r["stars"], "arm": arm,
                         "need": (r.get("needs") or [None])[0],
                         "group": key, "served": None})
    for r in prev.get("placebo", []):
        rows.append({"repo": r["repo"], "stars": r["stars"], "arm": "placebo",
                     "need": (r.get("needs") or [None])[0], "group": "placebo",
                     "served": None})
    for r in (prev.get("placebo_control") or {}).get("controls", []):
        rows.append({"repo": r["repo"], "stars": r["stars"], "arm": "placebo",
                     "need": r.get("need"), "group": "placebo_control",
                     "served": r.get("served")})
    return rows


def fetch(rows, only=None):
    os.makedirs(RAW, exist_ok=True)
    cache = load_cache()
    todo = [r for r in rows
            if only is None or r["arm"] in only or r["group"] in only]
    fetched = 0
    for row in todo:
        name = row["repo"]
        entry = cache.get(name)
        if isinstance(entry, dict) and "contents" in entry and "releases" in entry:
            continue
        root = contents(name)
        time.sleep(0.3)
        rel = releases(name)
        time.sleep(0.3)
        cache[name] = {"contents": root, "releases": rel}
        fetched += 1
        with open(CACHE, "w") as fh:
            json.dump(cache, fh, indent=1, sort_keys=True)
    return fetched, len(todo)


def status(rows):
    cache = load_cache()
    have = sum(1 for r in rows
               if isinstance(cache.get(r["repo"]), dict)
               and "contents" in cache[r["repo"]])
    return have, len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()
    rows = population()
    if args.fetch:
        got, considered = fetch(rows, args.only)
        print("fetched %d of %d considered rows; cache now %d entries"
              % (got, considered, len(load_cache())))
    if args.status:
        have, total = status(rows)
        print("cached %d of %d rows" % (have, total))
    if not (args.fetch or args.status):
        ap.print_help()
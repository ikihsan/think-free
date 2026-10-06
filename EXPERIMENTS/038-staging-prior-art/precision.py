#!/usr/bin/env python3
"""E038 precision check: does the keyword classifier recover independent real rows?

The readout in E038 classified 195 GitHub issues by keyword and reported 100
"in-population". That number is not a finding until the classifier is shown to find
the rows a person would call the thing, and not the rows it happens to match. The
rows above are visibly mixed -- `nextpnr`'s 'Max frequency' and `meridun`'s 'stage'
are not the need -- so the 100 is an upper bound on a number nothing has measured.

The check: take a pre-named, mechanically selected sample, read the text, and label
each row by hand against the question a reader would ask. Two readers, because one
reader on this population has produced several wrong readings in this record (F026,
F029, F048).

Selection is mechanical and declared before reading: rows are sorted by
(query order, then GitHub's own rank) and every k-th row is taken. No choosing after
seeing the content.

  python3 precision.py          # print the sample for reading
  python3 precision.py --json   # print it with bodies, for the second reader
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Same vocabulary the readout used, kept here so a disagreement can be traced to
# which rule fired rather than to a difference of opinion about the topic.
WANT = re.compile(r"st(age|aged|aging|ages)\b", re.I)
COORD = re.compile(
    r"(line\s*(number|range|ranges)?\b|specific line|single line|one line|part of a "
    r"file|by line|per line|partial)", re.I)
GITCTX = re.compile(
    r"(git\s+add|git add|-p\b|patch mode|hunk|commit|index|working tree|diff)", re.I)
NOTIT = re.compile(
    r"(blame|diff viewer|linter|eslint|merge conflict|stack ?trace|traceback|"
    r"line ?length|line ?count|char ?limit|max.?line|line ?wrap|80 ?char)", re.I)


def rules(title, body):
    """Which rules fired, so a hand label can be compared against the mechanism."""
    text = (title or "") + "\n" + (body or "")
    return {
        "notit": bool(NOTIT.search(text)),
        "want": bool(WANT.search(text)),
        "gitctx": bool(GITCTX.search(text)),
        "coord": bool(COORD.search(text)),
    }


def keyword_label(r):
    if r["notit"]:
        return "other-topic"
    if not r["want"]:
        return "no-stage-verb"
    if not r["gitctx"]:
        return "no-git-context"
    if not r["coord"]:
        return "stage-but-no-coordinate"
    return "in-population"


def sample(step=3):
    """Every step-th row, in query order then GitHub's rank. No content consulted."""
    out = []
    seen = set()
    for rec in _requests():
        if rec.get("index") != "github-issues":
            continue
        try:
            items = json.loads(rec["body"]).get("items", [])
        except ValueError:
            continue
        kept = 0
        for rank, it in enumerate(items):
            key = it.get("html_url")
            if key in seen:
                continue
            seen.add(key)
            kept += 1
            if kept % step:
                continue
            r = rules(it.get("title", ""), it.get("body") or "")
            out.append({
                "n": len(out) + 1,
                "keyword_label": keyword_label(r),
                "rules": r,
                "repo": (it.get("repository_url") or "").rsplit("/", 1)[-1],
                "number": it.get("number"),
                "title": it.get("title"),
                "state": it.get("state"),
                "comments": it.get("comments"),
                "url": it.get("html_url"),
                "body": (it.get("body") or "")[:700],
            })
    return out


def _requests():
    p = os.path.join(RAW, "requests.jsonl")
    with open(p) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


if __name__ == "__main__":
    rows_ = sample()
    if "--json" in sys.argv:
        print(json.dumps(rows_, indent=1))
        sys.exit(0)
    print("mechanical sample: every 3rd distinct issue, %d rows\n" % len(rows_))
    for r in rows_:
        fired = ",".join(k for k, v in r["rules"].items() if v) or "-"
        print("[%2d] %-22s %-24s %s" % (r["n"], r["keyword_label"], fired, r["repo"]))
        print("     %s" % r["title"])
        print("     %s  [%s, %d comments]" % (r["url"], r["state"], r["comments"]))
        body = " ".join(r["body"].split())
        if body:
            print("     > %s" % body[:300])
        print()

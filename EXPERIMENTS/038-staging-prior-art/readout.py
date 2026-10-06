#!/usr/bin/env python3
"""E038 readout: read the raw request log, derive nothing from a search engine's count.

The counts GitHub and Stack Exchange return are their own labels, the same class of
evidence as `closed_reason` in E034 -- a label, not a measurement. What a route
returns is only a candidate list. This file reports the list, and reads each row
against a declared vocabulary.

The vocabulary is the instrument, so it is printed with the result and the rows it
could not place are printed too. A classifier that cannot say "unclear" reports a
rate it has not measured.

  python3 readout.py issues      # Pool C, GitHub issues
  python3 readout.py sources     # Pool A, what the primary sources say
  python3 readout.py all
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-research/1.0 (E038)"

# What the row must be about for it to be in the population. Declared before reading
# any row, and deliberately narrow: a row about line numbers in a file, in a staging
# or commit context. A row about line numbers in a diff viewer, a blame tool, a linter
# or a merge conflict is a different need and is counted separately.
WANT = re.compile(
    r"st(age|aged|aging|ages)\b", re.I)
COORD = re.compile(
    r"(line\s*(number|range|ranges)?\b|specific line|single line|one line|part of a "
    r"file|by line|per line|partial)", re.I)
GITCTX = re.compile(
    r"(git\s+add|git add|-p\b|patch mode|hunk|commit|index|working tree|diff)", re.I)
# Present in the row but about something else.
NOTIT = re.compile(
    r"(blame|diff viewer|linter|eslint|merge conflict|stack ?trace|traceback|"
    r"line ?length|line ?count|char ?limit|max.?line|line ?wrap|80 ?char)", re.I)


def rows():
    p = os.path.join(RAW, "requests.jsonl")
    with open(p) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def classify(title, body):
    """-> (label, why). 'unclear' is an allowed and expected answer."""
    text = (title or "") + "\n" + (body or "")
    if NOTIT.search(text):
        return "other-topic", "matches a non-staging sense of line/partial"
    if not WANT.search(text):
        return "no-stage-verb", "never says stage/staged/staging"
    if not GITCTX.search(text):
        return "no-git-context", "staging verb without a git/diff context"
    if not COORD.search(text):
        return "stage-but-no-coordinate", "staging in git, but not by line"
    return "in-population", "staging in git, addressed by line"


def show_issues():
    recs = [r for r in rows() if r.get("index") == "github-issues"]
    if not recs:
        print("no github-issues rows on disk")
        return
    tally = {}
    per_query = {}
    examples = {"in-population": [], "stage-but-no-coordinate": []}
    for r in recs:
        try:
            items = json.loads(r["body"]).get("items", [])
        except ValueError:
            continue
        q = r.get("phrase", "?")
        counts = per_query.setdefault(q, {})
        for it in items:
            body = it.get("body") or ""
            label, why = classify(it.get("title", ""), body)
            counts[label] = counts.get(label, 0) + 1
            tally[label] = tally.get(label, 0) + 1
            if label in examples and len(examples[label]) < 12:
                examples[label].append({
                    "label": label, "why": why, "repo": it.get("repository_url", "").rsplit("/", 1)[-1],
                    "title": it.get("title"), "state": it.get("state"),
                    "comments": it.get("comments"), "url": it.get("html_url"),
                })
    print("rows read: %d requests, %d issues" % (
        len(recs), sum(tally.values())))
    print("\nlabel totals (an issue can match several queries, so these overlap):")
    for k in sorted(tally, key=lambda k: -tally[k]):
        print("  %-24s %d" % (k, tally[k]))
    print("\nper query:")
    for q in sorted(per_query):
        print("  %-42s %s" % (q, per_query[q]))
    print("\nthe vocabulary, in full:")
    print("  in-population           = says stage* AND git/diff context AND a line coordinate")
    print("  stage-but-no-coordinate = says stage* AND git/diff context, but not by line")
    print("  no-git-context          = stage* with no git/diff context")
    print("  no-stage-verb           = never says stage/staged/staging")
    print("  other-topic             = matched a non-staging sense of line/partial")
    for label in ("in-population", "stage-but-no-coordinate"):
        print("\n%s -- %d shown:" % (label, len(examples[label])))
        for e in examples[label]:
            print("  [%s/%s c=%s] %s" % (e["repo"], e["state"], e["comments"], e["title"]))
            print("      %s" % e["url"])


def show_sources():
    for r in rows():
        if r.get("arm") != "source":
            continue
        print("%-26s %3d %8d bytes" % (r["measure"], r["status"], len(r["body"])))


def show_index():
    """Which declared requests actually reached a server."""
    print("declared requests on disk:")
    seen = {}
    for r in rows():
        seen[r["measure"]] = r
    ok = sum(1 for r in seen.values() if r["status"] == 200)
    print("  %d distinct measures, %d answered 200, %d did not"
          % (len(seen), ok, len(seen) - ok))
    for m in sorted(seen):
        r = seen[m]
        if r["status"] != 200:
            print("    %-52s %3d %s" % (m[:52], r["status"],
                                        (r.get("error_message") or "")[:70]))


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg in ("issues", "all"):
        show_issues()
        print()
    if arg in ("index", "all"):
        show_index()
        print()
    if arg in ("sources", "all"):
        show_sources()

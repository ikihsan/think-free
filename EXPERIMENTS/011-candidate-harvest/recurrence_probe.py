#!/usr/bin/env python3
"""Third probe: is the recurrence signal the HN corpus lacks obtainable elsewhere?

The screening of 50 harvested needs found no way to tell a shared problem from
one person's wish. That is a property of the corpus, not a fact about the world:
a single comment carries no information about how many people want the thing.
This probe asks whether a *countable* corpus supplies it, using the one cluster
in the harvest that recurred by eye -- coding agents making changes nobody asked
for, which appears independently in at least four separate HN threads.

The measurement is not "how many issues mention this" but "in how many distinct
repositories", because a thousand issues in one repository is one project's
problem and a hundred issues in a hundred repositories is a cross-project one.
Both numbers are printed: the second is the one that would justify treating the
problem as shared, and a low second number would refute it.

Limits, stated before the numbers are read: GitHub's issue search is full text
over titles and bodies, so a query's phrasing decides what it finds; a problem
discussed in a forum, a mailing list or an issue tracker that is not GitHub does
not appear; and issue text is self-selected, so a count is a floor. This can
refute a claim of recurrence. It cannot establish one.

    python3 recurrence_probe.py
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import os


HERE = os.path.dirname(os.path.abspath(__file__))


def path(*parts):
    """Resolve a data path next to this script.

    The evidence is only reproducible if it can be re-run from anywhere, so the
    raw files are addressed relative to the script rather than to the caller's
    working directory.
    """
    return os.path.join(HERE, *parts)


UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}
# (label, issue query)
QUERIES = [
    ("agent-unrequested-edits",
     'is:issue is:open created:>2025-01-01 "not asked for" in:title,body'),
    ("agent-unrelated-changes",
     'is:issue is:open created:>2025-01-01 "unrelated changes" in:title,body'),
    ("agent-scope-creep",
     'is:issue is:open created:>2025-01-01 "scope creep" agent in:title,body'),
    ("copilot-unrelated-file",
     'is:issue is:open created:>2025-01-01 "unrelated file" copilot in:title,body'),
]


def search(q):
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "per_page": 30})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    out = []
    for label, q in QUERIES:
        try:
            d = search(q)
        except urllib.error.HTTPError as e:
            print("HTTP %s on %s" % (e.code, label), file=sys.stderr)
            time.sleep(65)
            continue
        items = d.get("items", [])
        repos = sorted(set(it["repository_url"].rsplit("/", 1)[-1] for it in items))
        rec = {"label": label, "query": q, "total_count": d.get("total_count"),
               "incomplete_results": d.get("incomplete_results"),
               "distinct_repos_in_first_page": len(repos),
               "repos": repos[:20]}
        out.append(rec)
        print("%-30s issues=%-7s distinct_repos(first 30)=%d" % (
            label, d.get("total_count"), len(repos)))
        time.sleep(7)
    with open(path("raw", "recurrence_probe.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
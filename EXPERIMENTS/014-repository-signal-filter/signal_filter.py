#!/usr/bin/env python3
"""E014 step 1: how many of the recurrent cluster's repositories survive a
repository-signal filter?

E012 found one cluster that recurs by repository (issues about coding agents
making changes nobody asked for), but its issue counts are full-text and
self-selected: 14510 issues in "unrelated changes" could be one aspect of one
tooling niche, or noise. D049 requires a repository-signal filter before the
count means anything.

The filter is stated before it is applied. A repository passes when its own
metadata (name, description, topics) says it belongs to the coding-agent
problem area, matched case-insensitively against:

    agent, copilot, claude, llm, coding assistant, ai coding, ai-agent,
    ai assistant, pair-programming, cursor

This can be wrong in both directions: a coding-agent tool described as
"developer productivity" fails, and a personal project named after an LLM
passes. The asymmetry that matters for the verdict: if the filtered count
collapses to a handful of repositories, the cluster is a few projects'
problem, and the cross-project claim dies. If many repos pass, the claim
survives this filter and earns the next one.

Steps: re-run E012's four queries (keeping owner/name this time), fetch
metadata for each unique repository, apply the filter, and re-count each
query restricted to passing repositories.

    python3 signal_filter.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "think-free-research", "Accept": "application/vnd.github+json"}

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

TERMS = ["agent", "copilot", "claude", "llm", "coding assistant", "ai coding",
         "ai-agent", "ai agent", "ai assistant", "pair-programming", "cursor"]


def path(*parts):
    return os.path.join(HERE, *parts)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search(q):
    url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
        {"q": q, "per_page": 30})
    return get(url)


def passes(meta):
    hay = " ".join([meta.get("full_name", ""), meta.get("description") or ""]
                   + (meta.get("topics") or [])).lower()
    return any(t in hay for t in TERMS)


def main():
    now = {}
    for label, q in QUERIES:
        try:
            d = search(q)
        except urllib.error.HTTPError as e:
            print("HTTP %s on %s" % (e.code, label), file=sys.stderr)
            time.sleep(65)
            d = search(q)
        repos = sorted({it["repository_url"].split("/repos/")[-1]
                        for it in d.get("items", [])})
        now[label] = {"query": q, "total_count": d.get("total_count"),
                      "repos_full": repos}
        print("%-30s issues=%-7s repos(first 30)=%d"
              % (label, d.get("total_count"), len(repos)))
        time.sleep(7)

    unique = sorted({r for v in now.values() for r in v["repos_full"]})
    print("unique repos to classify:", len(unique))
    classified = {}
    for i, full in enumerate(unique):
        for attempt in range(4):
            try:
                meta = get("https://api.github.com/repos/" + full)
                classified[full] = {"description": meta.get("description"),
                                    "topics": meta.get("topics") or [],
                                    "pass": passes(meta)}
                break
            except urllib.error.HTTPError as e:
                if e.code in (403, 429) and attempt < 3:
                    print("HTTP %s on %s; sleeping 65s" % (e.code, full),
                          file=sys.stderr)
                    time.sleep(65)
                else:
                    classified[full] = {"error": "HTTP %s" % e.code,
                                        "pass": None}
                    break
        time.sleep(1.2)
        if (i + 1) % 10 == 0:
            print("classified", i + 1, flush=True)
            with open(path("raw", "signal_filter_partial.json"), "w") as f:
                json.dump({"queries": now, "classified": classified}, f,
                          indent=1)

    passing = {r for r, c in classified.items() if c.get("pass")}
    print("repositories passing the filter:", len(passing), "of", len(unique))

    filtered = {}
    for label, v in now.items():
        keep = [r for r in v["repos_full"] if r in passing]
        rec = {"query": v["query"], "unfiltered_total": v["total_count"],
               "passing_repos_in_first_page": len(keep), "passing_repos": keep}
        if keep:
            qualifiers = " ".join("repo:" + r for r in keep[:10])
            fq = v["query"] + " " + qualifiers
            try:
                d = search(fq)
                rec["filtered_total_count"] = d.get("total_count")
            except urllib.error.HTTPError as e:
                rec["filtered_error"] = "HTTP %s" % e.code
            time.sleep(7)
        filtered[label] = rec
        print("%-30s filtered issues=%s (first-page passing repos %d)"
              % (label, rec.get("filtered_total_count", "?"), len(keep)))

    out = {"terms": TERMS, "queries": now, "classified": classified,
           "filtered": filtered}
    with open(path("raw", "signal_filter.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

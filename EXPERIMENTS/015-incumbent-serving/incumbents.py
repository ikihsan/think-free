#!/usr/bin/env python3
"""Build the incumbent population the mission's own prior-art screen names.

F029's screen killed 19 of 50 harvested needs with one cause of death: "a tool
already serves it". Those verdicts were re-checked against star counts, and F032
then measured that stars do not predict use in any niche. So the population this
module builds is the population the screen itself consulted: for each killed
need, the repositories a GitHub phrase query surfaces.

Two things are fixed here, before any figure is read, because F030 showed a
single query decides a prior-art verdict wrongly in both directions:

  * **two phrasings per need**, written out, and `in:name,description` only --
    `in:readme` returned 502 hits that were `awesome-go` (F030);
  * **the sample rule**: the 30 highest-starred incumbents, deduplicated across
    phrasings, ties broken by name. Highest-starred is deliberately the sample
    most likely to *be* serving, because a finding of "not served" from a
    low-starred sample would be uninterpretable.
  * **a placebo arm**: the lowest-starred repositories the same queries return
    in reverse order. Nobody uses them, so any serving figure found there is an
    instrument defect and not a fact about the world.

The verdict module is named `verdict.py` and not `stats.py`: a sibling experiment
already owns `stats.py`, and two modules of that name in one interpreter means
the second import is silently shadowed. The first full-suite run of these tests
passed in isolation and failed with `module 'stats' has no attribute 'classify'`
because it had imported the other one.

`placebo.py` re-runs that arm after the fact, because the first placebo turned
out to be unreadable and therefore incapable of catching anything.

    python3 incumbents.py            # writes raw/incumbents.json
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

# The 19 `prior_art` kills, with the two phrasings each. The first is the screen's
# own phrasing where `verify_prior_art.py` recorded one, so the population is the
# population that instrument consulted rather than a fresh opinion.
KILLS = [
    ("hn-client", ["hacker news api client", "hn api reader"]),
    ("atomic-distro", ["immutable linux system", "atomic linux distro"]),
    ("webp-encode", ["webp encoder", "image encoder webp"]),
    ("agent-memory", ["ai agent memory server", "agent memory store"]),
    ("runtime-instrumentation", ["ebpf tracing runtime", "runtime instrumentation profiler"]),
    ("flashcards", ["flashcard spaced repetition", "flashcards anki"]),
    ("hn-tagging", ["hacker news client tags", "hn favorites reader"]),
    ("atproto-pds", ["atproto pds server", "activitypub server implementation"]),
    ("word-game", ["word game", "wordle clone"]),
    ("scraper-trap", ["web scraper", "scraping tool"]),
    ("bulk-seed-books", ["ebook library server calibre", "ebook server opds"]),
    ("url-popularity", ["url popularity", "link popularity"]),
    ("cpp-subset-linter", ["c++ include linter", "clang tidy include"]),
    ("s3-alternative", ["s3 object storage server", "minio alternative s3"]),
    ("cheap-monitoring", ["uptime monitor", "monitoring status page self hosted"]),
    ("interest-field", ["atproto interests", "mastodon tags schema"]),
    ("selective-stage", ["version control partial stage", "git interactive staging"]),
    ("model-changelog", ["llm model changelog tracker", "model release notes tracker"]),
    ("gdrive-disk-usage", ["gdrive disk usage", "google drive storage analyzer"]),
]

# The contrast arm. F029 named this cluster as the one with the strongest measured
# recurrence, and it is a young vocabulary, which is where T-0059 measured almost
# no adoption at all. A premise that holds in a mature vocabulary and fails in a
# young one is a different finding from one that fails everywhere.
CLUSTER = [
    ("agent-unrequested-edits", ["ai agent change control", "coding agent guardrails"]),
    ("agent-review", ["agent code review tool", "ai agent diff review"]),
    ("agent-hooks", ["claude code hooks", "agent pre-commit hook"]),
]

# Five of the kills, re-asked in reverse star order, for the placebo arm.
PLACEBO_QUERIES = ["flashcard spaced repetition", "web scraper", "uptime monitor",
                   "s3 object storage server", "ebook library server calibre"]

PER_PHRASING = 3
SAMPLE_SIZE = 30
PLACEBO_SIZE = 5


def search(q, order="desc"):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q + " in:name,description", "per_page": PER_PHRASING,
         "sort": "stars", "order": order})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def row(it):
    return {"repo": it["full_name"], "stars": it["stargazers_count"],
            "pushed": (it.get("pushed_at") or "")[:10],
            "archived": bool(it.get("archived")),
            "desc": (it.get("description") or "")[:90]}


def collect(groups, order="desc"):
    """Every repository a phrasing surfaced, with the kill and phrasing recorded."""
    out = []
    for name, phrasings in groups:
        for phrasing in phrasings:
            try:
                data = search(phrasing, order)
            except urllib.error.HTTPError as e:
                print("HTTP %s on %r" % (e.code, phrasing), file=sys.stderr)
                time.sleep(20)
                continue
            items = [row(it) for it in data.get("items", [])]
            out.append({"need": name, "phrasing": phrasing, "order": order,
                        "total_count": data.get("total_count"), "items": items})
            print("  %-24s %-40s %d hits -> %s" % (
                name, phrasing[:40], data.get("total_count") or 0,
                ", ".join("%s(%s*)" % (i["repo"], i["stars"]) for i in items) or "-"))
            time.sleep(6.2)          # unauthenticated search is 10/minute
    return out


def dedupe(blocks):
    """One row per repository, keeping every need and phrasing that named it."""
    merged = {}
    for b in blocks:
        for it in b["items"]:
            rec = merged.setdefault(it["repo"], dict(it, needs=[], phrasings=[]))
            if b["need"] not in rec["needs"]:
                rec["needs"].append(b["need"])
            if b["phrasing"] not in rec["phrasings"]:
                rec["phrasings"].append(b["phrasing"])
    return merged


def main():
    print("incumbents named by the 19 prior_art kills:")
    kill_blocks = collect(KILLS)
    incumbents = dedupe(kill_blocks)
    ranked = sorted(incumbents.values(), key=lambda r: (-r["stars"], r["repo"]))
    sample = ranked[:SAMPLE_SIZE]
    print("\n%d distinct repositories; sample is the %d highest-starred"
          % (len(ranked), len(sample)))

    print("\ncontrast arm, the young vocabulary the mission has not screened:")
    cluster_blocks = collect(CLUSTER)
    cluster = sorted(dedupe(cluster_blocks).values(),
                     key=lambda r: (-r["stars"], r["repo"]))[:SAMPLE_SIZE]
    print("%d distinct repositories" % len(cluster))

    print("\nplacebo arm, the same queries in reverse star order:")
    placebo_blocks = collect([(q.split()[0], [q]) for q in PLACEBO_QUERIES], order="asc")
    placebo_pool = dedupe(placebo_blocks)
    placebo = sorted(placebo_pool.values(), key=lambda r: (r["stars"], r["repo"]))
    placebo = [r for r in placebo if r["stars"] < 100][:PLACEBO_SIZE]
    print("%d candidates under 100 stars: %s" % (
        len(placebo), ", ".join("%s(%s*)" % (r["repo"], r["stars"]) for r in placebo)))

    out = {"rule": "30 highest-starred incumbents of the 19 prior_art kills, two "
                   "phrasings each, deduplicated; placebo = lowest-starred from five "
                   "of the same queries, under 100 stars",
           "incumbents": sample, "incumbents_total_distinct": len(ranked),
           "cluster": cluster, "cluster_total_distinct": len(dedupe(cluster_blocks)),
           "placebo": placebo, "search_blocks": kill_blocks + cluster_blocks}
    with open(os.path.join(HERE, "raw", "incumbents.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("\nwrote raw/incumbents.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
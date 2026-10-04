#!/usr/bin/env python3
"""Measure every repository in the population and cache the result per row.

One call to `serving.measure` per repository is a few seconds and the search API
allows ten queries a minute, so this is paced and re-runnable: a row already in
the cache is skipped, and a row whose every channel refused is retried rather
than cached, because a refusal is not an answer.

    python3 measure.py              # fill raw/serving.json
    python3 measure.py --only-cluster
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "raw", "serving.json")
# The instrument's own release channel reads the GitHub core API, which allows
# 60 requests an hour unauthenticated and is shared with every other task on this
# VM. Each repository costs one. The population is sized so one full pass fits.
PACE = 2.0


def load_cache():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except (IOError, OSError, ValueError):
        return {}


def main():
    argv = sys.argv[1:]
    with open(os.path.join(HERE, "raw", "incumbents.json")) as f:
        pop = json.load(f)
    groups = [("incumbents", pop["incumbents"]), ("placebo", pop["placebo"])]
    if "--only-cluster" in argv:
        groups = [("cluster", pop["cluster"])]
    elif "--cluster" in argv:
        groups.append(("cluster", pop["cluster"]))

    cache = load_cache()
    skip_cluster_measured = "--cluster" in argv
    todo = []
    for g, rows in groups:
        for r in rows:
            have = cache.get(r["repo"], {})
            # A row already measured with the release channel is complete. A row
            # measured without it is re-measurable, but only if this pass has the
            # channel available, and skipping it is recorded rather than assumed.
            if have.get("rate") or any(c.get("value", 0) > 0 for c in have.get("cumulative") or []):
                continue
            if skip_cluster_measured and have.get("channels_absent"):
                continue
            todo.append((g, r))
    print("population: %s" % ", ".join("%s=%d" % (g, len(rows)) for g, rows in groups))
    print("to measure: %d" % len(todo))

    names = sorted({n for _, r in todo for n in __import__("serving").guesses(r["repo"])})
    from serving import npm_bulk
    npm_cache = npm_bulk(names)

    # `--no-releases` skips the GitHub release channel, which is the only channel
    # that reads the core API (60 requests an hour, shared with every task on this
    # VM). The contrast arm is measured without it and its absence is recorded per
    # row rather than being read as a zero.
    releases = "--no-releases" not in argv

    for i, (group, repo) in enumerate(todo):
        import serving
        rec = serving.measure(repo["repo"], npm_cache=npm_cache, releases=releases)
        rec["stars"] = repo["stars"]
        rec["group"] = group
        rec["needs"] = repo.get("needs", [])
        rec["phrasings"] = repo.get("phrasings", [])
        cache[repo["repo"]] = rec
        if not releases:
            rec.setdefault("channels_absent", []).append("ghreleases")
        marks = [("%s=%s" % (r["channel"], "{:,}".format(r["value"]))) for r in rec["rate"]]
        marks += [("%s=%s" % (c["channel"], "{:,}".format(c["value"])))
                  for c in rec["cumulative"]]
        print("  [%2d/%2d] %-42s %s%s%s" % (
            i + 1, len(todo), repo["repo"], " ".join(marks) or "no reading",
            " refused=%d" % len(rec["refused"]) if rec["refused"] else "",
            " unverified=%d" % len(rec["unverified"]) if rec["unverified"] else ""))
        sys.stdout.flush()
        with open(CACHE, "w") as f:
            json.dump(cache, f, indent=1, sort_keys=True)
            f.write("\n")
        time.sleep(PACE)

    print("cached %d repositories" % len(cache))
    return 0


if __name__ == "__main__":
    sys.exit(main())
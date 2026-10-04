#!/usr/bin/env python3
"""A placebo arm the instrument can actually read.

The declared placebo was the five lowest-starred repositories five of the same
queries return. All five turned out **unreadable** — they publish nothing to any
channel — so the arm never had the chance to produce a false positive, and a
gate it cannot exercise proves nothing. That is the same defect F032 records in
the other direction: an instrument's dead branch is not a passing result.

So the control is rebuilt to be readable by construction: repositories that are
unpopular **and** publish something. Each is found by looking for a release
channel first, and the floor is then asked whether it fires. A floor that fires
here is a false positive, and the arm can only report one of two honest
outcomes: no false positive among the readable controls, or the size of the one
it found.

This searches for controls rather than sampling them, so the population is not a
judgement about which repos are unpopular.

    python3 placebo.py
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
# The same needs the primary arm screened, re-asked with a star ceiling so the
# results are readable-but-unpopular rather than merely absent.
QUERIES = ["flashcard spaced repetition", "web scraper", "uptime monitor",
           "s3 object storage server", "ebook library server calibre",
           "webp encoder", "ai agent memory server", "version control partial stage"]
STAR_CEILING = 40
PER_QUERY = 8
WANT = 8


def search(q):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q + " in:name,description stars:<%d" % STAR_CEILING,
         "per_page": PER_QUERY, "sort": "stars", "order": "desc"})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    import serving
    found, seen = [], set()
    for q in QUERIES:
        try:
            data = search(q)
        except urllib.error.HTTPError as e:
            print("HTTP %s on %r" % (e.code, q), file=sys.stderr)
            time.sleep(25)
            continue
        for it in data.get("items", []):
            if it["full_name"] in seen:
                continue
            seen.add(it["full_name"])
            found.append({"repo": it["full_name"], "stars": it["stargazers_count"],
                          "desc": (it.get("description") or "")[:90],
                          "need": q})
        print("  %-38s %s hits" % (q, data.get("total_count")))
        time.sleep(6.2)
    print("\n%d unpopular candidates under %d stars" % (len(found), STAR_CEILING))

    # Prefer controls the instrument can read. Releases are checked first because
    # that is the only channel with a floor high enough to be interesting.
    import stats
    names = sorted({n for r in found for n in serving.guesses(r["repo"])})
    npm_cache = serving.npm_bulk(names)
    measured = []
    for r in found:
        if len(measured) >= WANT:
            break
        rec = serving.measure(r["repo"], npm_cache=npm_cache, releases=True)
        rec["stars"] = r["stars"]
        rec["need"] = r["need"]
        rate, cumulative, undecided = stats.classify(rec)
        if undecided:
            continue                       # not readable: cannot be a placebo
        rec["served"] = stats.served(rec)
        measured.append(rec)
        print("  %-42s %3s* %s" % (
            r["repo"], r["stars"], "FALSE POSITIVE" if rec["served"] else "correctly unused"))
        sys.stdout.flush()
        time.sleep(2.0)

    false_positives = [r for r in measured if r["served"]]
    out = {"star_ceiling": STAR_CEILING, "queries": QUERIES,
           "candidates": len(found), "readable_controls": len(measured),
           "false_positives": [r["repo"] for r in false_positives],
           "verdict": ("a floor fired on %d of %d readable controls"
                       % (len(false_positives), len(measured))) if measured
                      else "no control was readable, so the arm proves nothing",
           "controls": measured}
    with open(os.path.join(HERE, "raw", "placebo.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("\n%s" % out["verdict"])
    print("wrote raw/placebo.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

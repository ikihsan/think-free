#!/usr/bin/env python3
"""Second prior-art pass, with narrower queries and no `in:readme`.

The first pass (`prior_art_probe.py`) put `in:name,description,readme` on the
age-assurance query and got 502 hits whose top three were awesome-go, a
self-hosting guide and a Discord bot: the phrase appeared in their READMEs.
That is a measurement of GitHub's full-text index, not of prior art, so this
pass drops `readme` and asks several phrasings per cluster.

Read the result as a population count only. A thin count means "nobody is
serving this on GitHub", which is not the same as "it does not exist" -- a
commercial product, a library published only to PyPI or npm, or a tool nobody
indexes would all read as zero here. The count can disqualify a cluster. It
cannot support a novelty claim, and nothing in this repository will treat it as
one.
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
GROUPS = {
    "agent-memory-portable": [
        "agent memory",
        "portable agent memory",
        "ai agent memory server",
        "claude code memory",
        "agent context portable format",
        "mcp memory",
    ],
    "url-popularity": [
        "url popularity",
        "link popularity",
        "web link graph pagerank",
        "url citation graph",
        "backlink counter open source",
    ],
}


def line(*parts):
    """One row, with no trailing whitespace when a field is empty.

    `print` with a trailing format field emitted 'total=0     ' when a query
    returned nothing; that reached a committed file and git 2.25 refuses to
    apply such a patch during a rebase, so the formatting moved here.
    """
    return "  ".join(str(p) for p in parts if str(p)).rstrip()


def search(q):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q + " in:name,description", "per_page": 5, "sort": "stars",
         "order": "desc"})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    out = {}
    for cluster, queries in GROUPS.items():
        out[cluster] = []
        for q in queries:
            try:
                d = search(q)
            except urllib.error.HTTPError as e:
                print("HTTP %s on %r" % (e.code, q), file=sys.stderr)
                time.sleep(65)
                continue
            items = [{"repo": it["full_name"], "stars": it["stargazers_count"],
                      "pushed": it["pushed_at"][:10], "archived": it["archived"],
                      "desc": (it["description"] or "")[:100]}
                     for it in d.get("items", [])]
            out[cluster].append({"query": q, "total_count": d.get("total_count"),
                                 "top": items[:3]})
            print(line("%-18s" % cluster, "%-34s" % q[:34],
                        "total=%s" % d.get("total_count"), ", ".join(
                            "%s(%s*)" % (t["repo"], t["stars"])
                            for t in items[:2])))
            time.sleep(7)
        print("")
    with open(path("raw", "prior_art_probe2.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
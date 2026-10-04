#!/usr/bin/env python3
"""Count prior art for a named cluster, from GitHub's public search API.

Why this exists: the screening of the 50-item sample in ../README.md assigns a
cause of death to each need, and 20 of the 50 are "a tool already owns this".
A verdict asserted from memory is exactly the error F025 records its author
making twice, so each prior-art verdict that could carry weight is re-checked
here against a countable source, and the count is written down with the date.

What it measures: how many public repositories GitHub's search returns for a
phrase. That is a *lower bound* on existing work, not a novelty check -- a
project that exists and is not on GitHub is invisible here, and an abandoned
prototype counts the same as a widely used tool. It is used only to separate
"nobody has built this" from "this is well populated", never to claim novelty.

Unauthenticated search is rate limited to roughly 10 requests a minute, so the
script sleeps between calls. Run from this directory:

    python3 prior_art_probe.py
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
# (cluster id, what was claimed, the query used to check it)
CHECKS = [
    ("age-assurance-anonymous",
     "no tool provides age proof without deanonymisation",
     "age assurance privacy preserving anonymous in:name,description,readme"),
    ("url-popularity",
     "no tool gives URLs a popularity score like GitHub stars",
     "url popularity backlinks in:name,description"),
    ("agent-memory-portable",
     "agent memory cannot move between vendors",
     "agent memory portable format in:name,description"),
    ("cpp-subset-linter",
     "no linter enforces a subset of C++",
     "c++ subset linter in:name,description"),
    ("gdrive-disk-usage",
     "no WinDirStat equivalent exists for Google Drive",
     "google drive disk usage analyzer in:name,description"),
    ("cheap-monitoring",
     "no very cheap uptime monitor exists",
     "uptime monitor self-hosted in:name,description"),
]


def line(*parts):
    """One row, with no trailing whitespace when a field is empty.

    `print` with a trailing format field emitted 'total=0     ' when the query
    returned nothing; that reached a committed file and git 2.25 refuses to
    apply such a patch during a rebase, so the formatting moved here.
    """
    return "  ".join(str(p) for p in parts if str(p)).rstrip()


def search(q, page=1):
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q, "per_page": 10, "page": page,
         "sort": "stars", "order": "desc"})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    out = []
    for i, (cid, claim, q) in enumerate(CHECKS):
        try:
            d = search(q)
        except urllib.error.HTTPError as e:
            print("HTTP %s on %s" % (e.code, cid), file=sys.stderr)
            if e.code in (403, 429):
                time.sleep(65)
                continue
            raise
        items = [{"repo": it["full_name"], "stars": it["stargazers_count"],
                  "pushed": it["pushed_at"][:10], "archived": it["archived"],
                  "desc": (it["description"] or "")[:110]} for it in d.get("items", [])]
        rec = {"cluster": cid, "claim": claim, "query": q,
               "total_count": d.get("total_count"),
               "incomplete_results": d.get("incomplete_results"),
               "top": items[:5]}
        out.append(rec)
        print(line("%-22s" % cid, "total=%s" % d.get("total_count"), "top=%s" % (
            ", ".join("%s(%s*)" % (t["repo"], t["stars"]) for t in items[:3]))))
        time.sleep(7)
    with open(path("raw", "prior_art_probe.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
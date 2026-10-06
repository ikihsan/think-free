#!/usr/bin/env python3
"""E041 step 1: which surfaces can this host actually read?

Two questions, both answered before any population is measured, because D067
requires a candidate's mechanism to be tested against that mechanism's existing
source first and F066/D070 closed one line for reaching the wrong answer about
its own host's egress.

  Q1 (positive control, instrument validity). Where can a *real, human-judged*
  repeat be read together with **both members of the pair**, without
  authentication? E040's G2 never fired because its control arm held one member
  per row (F064) and the target was unreachable (F066). A control that holds
  only one member cannot validate a similarity instrument at all, so this is the
  first question, not the second.

  Q2 (second venue, item 0f). Where can practitioners state a need in their own
  words, publicly, at a population large enough to test whether recognition
  scales with population size?

Every surface below is named explicitly rather than discovered by trial, which
is the form D066 asks for. Writes every response to raw/ before anything is
computed. Budget-capped.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = {"User-Agent": "think-free-research", "Accept": "*/*"}
BUDGET = 40

# Declared surfaces. `want` is what a usable answer must contain, so a 200 that
# is irrelevant to the query cannot be scored as reachable (F036).
SURFACES = [
    # --- Q1: surfaces that could serve a real repeat pair, both members present ---
    {"id": "gh-search-dup",
     "url": "https://api.github.com/search/issues?"
            "q=is%3Aissue+reason%3Aduplicate+%22duplicate+of%22+in%3Abody&per_page=3",
     "want": "total_count",
     "note": "GitHub issue search, issues the platform itself closed as duplicates"},
    {"id": "gh-issue-read",
     "url": "https://api.github.com/repos/rust-lang/rust/issues/1",
     "want": "number",
     "note": "can the *target* of a duplicate pointer be read by number"},
    {"id": "se-closed-details",
     "url": "https://api.stackexchange.com/2.3/questions/17531?"
            "site=stackoverflow&filter=!nNPvSNdWme",
     "want": "items",
     "note": "re-probe F066 route 1: closed_details on the question type"},
    {"id": "stackprinter-so",
     "url": "http://stackprinter.appspot.com/export?question=15969848&service=stackoverflow"
            "&language=en&hideAnswers=false&showAll=true&width=640",
     "want": "Question",
     "note": "third-party HTML export of an SO question incl. its duplicate notice"},
    {"id": "askubuntu-html",
     "url": "https://askubuntu.com/questions/1",
     "want": "question",
     "note": "a non-stackoverflow SE host, to separate 'SE blocked' from 'blocked'"},
    {"id": "wiki-redirects",
     "url": "https://en.wikipedia.org/w/api.php?action=query&prop=redirects"
            "&titles=Mercury%20planet|Crocodile&redirects=1&format=json",
     "want": "query",
     "note": "real human-judged aliases; both members named in one request"},

    # --- Q2: candidate second venues for public need statements ---
    {"id": "reddit-json",
     "url": "https://www.reddit.com/r/programming/new.json?limit=3",
     "want": "data",
     "note": "Reddit listing JSON, unauthenticated"},
    {"id": "discourse-latest",
     "url": "https://discourse.python.org/latest.json",
     "want": "topic_list",
     "note": "Discourse forum listing JSON"},
    {"id": "lobsters-json",
     "url": "https://lobste.rs/newest.json",
     "want": "",
     "note": "Lobsters listing JSON"},
    {"id": "devto-articles",
     "url": "https://dev.to/api/articles?per_page=3",
     "want": "",
     "note": "DEV article listing JSON"},
    {"id": "gh-issues-need",
     "url": "https://api.github.com/search/issues?"
            "q=is%3Aissue+%22is+there+a+tool+for%22&per_page=3",
     "want": "total_count",
     "note": "GitHub issue search as a need-statement venue"},
    {"id": "hn-algolia",
     "url": "https://hn.algolia.com/api/v1/search?tags=comment&hitsPerPage=3&query=tool",
     "want": "nbHits",
     "note": "control: the surface E012/E040 used"},
]


def fetch(url, tries=2):
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=45) as r:
                return r.getcode(), r.read(), dict(r.headers), None
        except urllib.error.HTTPError as exc:
            return exc.code, b"", {}, "HTTPError %s" % exc.code
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            last = repr(exc)[:160]
            time.sleep(1.5 * (attempt + 1))
    return None, b"", {}, last


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    out = []
    for i, s in enumerate(SURFACES):
        if i >= BUDGET:
            out.append(dict(s, status="budget_skipped"))
            continue
        code, body, headers, err = fetch(s["url"])
        head = body[:4000].decode("utf-8", "replace")
        with open(os.path.join(RAW, "probe_%s.txt" % s["id"]), "wb") as fh:
            fh.write(body[:200000])
        hit = s["want"] in head if s["want"] else len(body) > 0
        out.append({
            "id": s["id"], "url": s["url"], "note": s["note"],
            "status_code": code, "bytes": len(body),
            "error": err,
            "limit": headers.get("X-RateLimit-Remaining") or headers.get("Retry-After"),
            "content_type": (headers.get("Content-Type") or "")[:60],
            "wanted_marker": s["want"], "marker_present": bool(hit),
            "reachable": bool(code == 200 and hit),
            "head": head[:300].replace("\n", " "),
        })
        print("%-18s code=%-4s bytes=%-8s marker=%-5s %s" % (
            s["id"], code, len(body), hit, (err or "")))
        time.sleep(1.0)
    with open(os.path.join(RAW, "probe_results.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    ok = [r["id"] for r in out if r.get("reachable")]
    print("\nreachable: %s" % ", ".join(ok))
    return 0


if __name__ == "__main__":
    sys.exit(main())

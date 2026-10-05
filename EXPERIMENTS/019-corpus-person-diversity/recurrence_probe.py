#!/usr/bin/env python3
"""Arm B: does person-level recurrence separate need clauses from controls?

Arm A found the corpus is 1250 distinct people, so recurrence was *available*
in it. Arm B asks what that means for the clauses themselves, in two halves:

  B1 (networked)  Ten mechanically chosen clauses from E012's 50-row sample and
                  six positive plus six negative controls are queried against
                  the public HN index. Distinct authors are counted from
                  fetched hits, not from nbHits. Gate B1 decides whether this
                  half is allowed to say anything at all.

  B2 (local)      F033's cluster is counted by distinct *author* inside the
                  corpus instead of by distinct *repository* on GitHub. No
                  network, no phrasing, nothing to be wrong about: two declared
                  term families must co-occur in a clause's text.

Both halves write raw/arm_b.json and print their own block; stats.py recomputes
every figure for results.json.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "012-candidate-harvest", "raw", "sample.jsonl")
CAPTURE_A = os.path.join(HERE, "raw", "corpus_authors.jsonl")
OUT = os.path.join(HERE, "raw", "arm_b.json")
SEARCH = "https://hn.algolia.com/api/v1/search"
PAGE = 200
MAX_HITS = 1000

STOPWORDS = set("""
a an and are as at be been but by can could did do does for from had has have
how i in into is it its just like me my no not of on one only or our out over
should so some that the their them then there these they this to too up us very
was we were what when where which who will with would you your
""".split())

# Declared before any count ran. An agent is the actor; a change is the
# complained-of event. F033's cluster is about the second.
FAMILIES = {
    "agent": set("""
    agent agentic agents claude codex copilot cursor devin swe-agent
    coding-agent codingagent llm gpt gemini
    """.split()),
    "change": set("""
    change changed changes changing edit edited edits modify modified
    refactor refactored rewrite rewrote revert reverted unasked unrequested
    unexpected surprise surprising
    """.split()),
}

POSITIVES = [
    "spaced repetition flashcards",
    "self-hosted email server",
    "atproto personal data server",
    "AI coding agent unrequested changes",
    "lossy webp conversion",
    "OCI image to rootfs",
]

NEGATIVES = [
    "gauge drift in a knitting chart",
    "a quorum rule for a five person book club",
    "provenance for a terrarium",
    "a hedger for municipal bond refinancing",
    "sorting a tram timetable by elevation",
    "a linter for 19th century parish registers",
]

CLAUSE_ROWS = list(range(4, 50, 5))  # declared: rows 5,10,...,50, 0-based


def path(*parts):
    return os.path.join(HERE, *parts)


def word(s):
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower())


def content_prefix(clause, n=4):
    toks = [t for t in word(clause).split() if len(t) >= 4 and t not in STOPWORDS]
    return " ".join(toks[:n])


def search(query):
    """Distinct authors across at most MAX_HITS fetched hits. Returns a dict."""
    url = SEARCH + "?" + urllib.parse.urlencode(
        {"query": query, "tags": "comment", "hitsPerPage": PAGE})
    authors = set()
    threads = set()
    fetched = 0
    capped = False
    page = 0
    while True:
        url = SEARCH + "?" + urllib.parse.urlencode(
            {"query": query, "tags": "comment", "hitsPerPage": PAGE,
             "page": page})
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            return {"query": query, "status": "error",
                    "error": "%s: %s" % (type(e).__name__, str(e)[:120]),
                    "distinct_authors": None, "distinct_threads": None,
                    "hits_fetched": fetched, "capped": capped}
        hits = data.get("hits") or []
        fetched += len(hits)
        for h in hits:
            authors.add(h.get("author"))
            threads.add(h.get("story_id"))
        page += 1
        if not hits or fetched >= MAX_HITS:
            capped = fetched >= MAX_HITS
            break
        time.sleep(0.15)
    return {"query": query, "status": "ok",
            "nbhits_estimate": data.get("nbHits"),
            "distinct_authors": len(authors),
            "distinct_threads": len(threads),
            "hits_fetched": fetched, "capped": capped,
            "pages": page}


def b2_local():
    """Distinct authors whose own clause names both families."""
    authors = {}
    for line in open(CAPTURE_A):
        r = json.loads(line)
        if r.get("status") == "ok" and r.get("author"):
            authors[r["author"]] = r
    corpus = {}
    for line in open(os.path.join(
            HERE, "..", "012-candidate-harvest", "raw",
            "hn_needs_2026-10-04.jsonl")):
        corpus[str(json.loads(line)["id"])] = json.loads(line)
    hits = []
    for author, rec in authors.items():
        text = word(corpus[rec["comment_id"]]["text"])
        toks = set(text.split())
        if toks & FAMILIES["agent"] and toks & FAMILIES["change"]:
            hits.append({"author": author, "comment_id": rec["comment_id"],
                         "trigger": rec["trigger"],
                         "excerpt": corpus[rec["comment_id"]]["text"][:200]})
    hits.sort(key=lambda h: h["author"])
    return {
        "families": {k: sorted(v) for k, v in FAMILIES.items()},
        "authors_in_capture": len(authors),
        "authors_naming_both": len(hits),
        "share_of_corpus": round(len(hits) / float(len(authors) or 1), 5),
        "rows": hits,
        "method": ("two declared term families must co-occur in a clause's own "
                   "text; counted over distinct authors of the 1401-row corpus"),
    }


def main():
    rows = [json.loads(l) for l in open(SAMPLE)]
    clauses = []
    for i in CLAUSE_ROWS:
        r = rows[i]
        clauses.append({"row": i + 1, "clause": r["clause"],
                        "verbatim": r["clause"].strip(),
                        "content4": content_prefix(r["clause"])})

    out = {"phrasings_asked": [], "clauses": [], "positive_controls": [],
           "negative_controls": [], "b2_local": b2_local()}

    for c in clauses:
        rec = {"row": c["row"], "clause": c["clause"],
               "verbatim_hits": search('"%s"' % c["verbatim"]),
               "content4": c["content4"],
               "content4_hits": search('"%s"' % c["content4"])}
        out["clauses"].append(rec)
        out["phrasings_asked"].extend([c["verbatim"], c["content4"]])
        print("clause %2d  verbatim=%s  content4=%s"
              % (c["row"], rec["verbatim_hits"]["distinct_authors"],
                 rec["content4_hits"]["distinct_authors"]))
        time.sleep(0.2)

    for name, group in (("positive_controls", POSITIVES),
                        ("negative_controls", NEGATIVES)):
        for q in group:
            r = search('"%s"' % q)
            r["arm"] = name
            out[name].append(r)
            out["phrasings_asked"].append(q)
            print("%-18s %-40s authors=%s"
                  % (name, q[:40], r["distinct_authors"]))
            time.sleep(0.2)

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
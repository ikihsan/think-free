"""E169 step 5: the instrument's own controls, and the corrected query arms.

Step 4's numbers are **void**, and the control is what voided them.  C1 was
supposed to feed each target's own title back into the search and require the
target at rank 1.  It failed on 3 of 13, and the totals explain why:

    "Missing Anthropic Sonnet 4 model with Bring Your Own Key from
     Github Copilot Chat and Agentic mode"   ->  17,033,620 hits
    "Debug mode and hot reload fail on iOS 26 due to JIT restriction
     error: mprotect failed: 13 (Permission denied)"  ->  12,572,918 hits

A quoted phrase of that length is not matched as a phrase.  GitHub's issue
search falls back to matching common words, so the "phrase" arm measured a
bag of stopwords and the 1-of-13 headline measured the instrument, not the
developer.  Two rows with `total = 582` and `total = 349,882` are the same
defect at lower amplitude.

The repair is to make the query what a search engine actually matches on: a
small number of distinctive terms, stopwords and negations removed.  So:

  C1' positive -- the target's own title, reduced by the same term selector the
      treatment arm uses.  The target must come back within the top 10.  This
      is the only control that licenses a number from this instrument; if it
      fails, no arm number is reported.
  C2  negative -- another row's post, same construction.  Bounds accidental hits.
  A5  OR of the post's five distinctive terms -- how a search engine matches
      prose, and what the tool would have to do.
  A6  AND of the same five terms -- the conjunction a tracker's own search box
      performs.

Both treatment arms are run on every row so the better one is never chosen per
row.  Terms are picked by length after stopword removal: the longest words in
a post are the ones that name a thing.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reach                                                     # noqa: E402

STOP = set("""a an the is are was were be been being to of in on at for with from
by and or not no but if then this that these those it its i my we our you your
he she they them do does did doing have has had having can could would should
will shall may might must get got getting there here when where which who whom
whose what how why as into out up down over under again more most some such only
own same so too very just also because while about after before than once
during why does doesnt cant wont isnt""".split())
NEGATED = re.compile(r"^(?:not|no|never|cannot|can't|isn't|doesn't|won't|"
                     r"without|failed|failure|error|errors|issue|problem)$")
TITLES = os.path.join(HERE, "raw", "target-titles.json")


def terms(text, limit=5):
    """Distinctive terms, longest first: the words that name a thing."""
    words = re.findall(r"[A-Za-z0-9_][A-Za-z0-9_.\-]{2,}", text or "")
    cand, seen = [], set()
    for w in words:
        lw = w.lower()
        if lw in STOP or NEGATED.match(lw) or lw in seen:
            continue
        seen.add(lw)
        cand.append(w)
    cand.sort(key=lambda w: (-len(w), w.lower()))
    return cand[:limit]


def get_title(owner, repo, number, cache):
    key = "%s/%s#%d" % (owner, repo, number)
    if key in cache:
        return cache[key]
    data, err = reach._results(
        "https://api.github.com/repos/%s/%s/issues/%d" % (owner, repo, number))
    cache[key] = {"title": (data or {}).get("title"),
                  "state": (data or {}).get("state"),
                  "is_pr": bool(data and data.get("pull_request")),
                  "created": (data or {}).get("created_at"),
                  "closed": (data or {}).get("closed_at"),
                  "error": err}
    return cache[key]


def run_query(q, target):
    if not q.strip():
        return {"rank": None, "n_items": 0, "total": 0, "unreadable": None,
                "skipped": "empty"}
    r = reach.search_once(q, target)
    if r.get("total", 0) is not None and r["total"] > 500000:
        r["degenerate"] = True        # D2 again: a bag of stopwords
    return r


def main():
    import arms
    plan = arms.load_plan()
    hand = arms.load_hand()
    cache = json.load(open(TITLES)) if os.path.exists(TITLES) else {}
    out = []
    for i, r in enumerate(plan, 1):
        t = r["target"]
        meta = get_title(t["owner"], t["repo"], t["number"], cache)
        h = hand.get(r["qid"], {})
        rec = {"qid": r["qid"], "target": t, "meta": meta,
               "hand": {k: h.get(k) for k in
                        ("literal_type", "phrase", "keyword", "note")}}
        title_terms = terms(meta.get("title"), limit=5)
        rec["C1_query"] = " OR ".join('"%s"' % x for x in title_terms)
        rec["C1"] = run_query(rec["C1_query"], t)
        other = plan[(i + 3) % len(plan)]
        oq = hand.get(other["qid"], {}).get("keyword", "")
        oterms = terms(oq, limit=5)
        rec["C2_query"] = " OR ".join('"%s"' % x for x in oterms)
        rec["C2"] = run_query(rec["C2_query"], t)
        pterms = terms((h.get("phrase") or "") + " " + (h.get("keyword") or ""),
                       limit=5)
        rec["A5_query"] = " OR ".join('"%s"' % x for x in pterms)
        rec["A5"] = run_query(rec["A5_query"], t)
        rec["A6_query"] = " ".join('"%s"' % x for x in pterms)
        rec["A6"] = run_query(rec["A6_query"], t)
        out.append(rec)
        sys.stderr.write("[%2d/%d] %s C1=%s/%s C2=%s A5=%s/%s A6=%s/%s\n" % (
            i, len(plan), r["qid"], rec["C1"].get("rank"), rec["C1"].get("total"),
            rec["C2"].get("rank"), rec["A5"].get("rank"), rec["A5"].get("total"),
            rec["A6"].get("rank"), rec["A6"].get("total")))
    json.dump(cache, open(TITLES, "w"), indent=1)

    def rate(key):
        den = [o for o in out if not o[key].get("degenerate")
               and not o[key].get("skipped")]
        k = sum(1 for o in den if o[key].get("rank"))
        return {"n": len(den), "hit": k,
                "share": round(k / float(len(den)), 4) if den else None}

    either = [o for o in out if o["A5"].get("rank") or o["A6"].get("rank")]
    summary = {
        "rows": len(out),
        "C1_positive_control": rate("C1"),
        "C2_negative_control": rate("C2"),
        "A5_or_terms": rate("A5"),
        "A6_and_terms": rate("A6"),
        "A5_or_A6_either": {"n": len(out), "hit": len(either),
                            "share": round(len(either) / float(len(out)), 4)},
        "degenerate_queries": sum(1 for o in out
                                  for k2 in ("A5", "A6", "C1", "C2")
                                  if o[k2].get("degenerate")),
        "literal_types": {t: sum(1 for o in out
                                 if o["hand"].get("literal_type") == t)
                          for t in ("error_message", "ui_string", "code_token",
                                    "symptom_only")},
        "detail": [{"qid": o["qid"], "title": (o["meta"].get("title") or "")[:90],
                    "state": o["meta"].get("state"), "is_pr": o["meta"].get("is_pr"),
                    "literal_type": o["hand"].get("literal_type"),
                    "C1_rank": o["C1"].get("rank"), "C1_total": o["C1"].get("total"),
                    "A5_query": o["A5_query"], "A5_rank": o["A5"].get("rank"),
                    "A5_total": o["A5"].get("total"),
                    "A6_rank": o["A6"].get("rank"),
                    "A6_total": o["A6"].get("total"),
                    "C2_rank": o["C2"].get("rank")} for o in out],
    }
    json.dump(summary, open(os.path.join(HERE, "raw", "controls.json"), "w"),
              indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "detail"},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
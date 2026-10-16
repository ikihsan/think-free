"""E169 step 6: reachability as containment in the fix's own text.

AMENDMENT 2, recorded after two instrument failures and before this ran.

Step 4 measured reachability by querying GitHub's issue search and got 1 of 13.
Step 5 ran the control that was supposed to license that number -- feed each
target its own title and require it back at rank 1 -- and the control failed
first on 3 of 13 and then on 13 of 13.  A measurement whose own positive
control cannot pass is not a measurement, so the step-4 and step-5 numbers are
**withdrawn**, not adjusted.  The reasons are worth recording because they are
what forced the change:

  * `/search/issues` accepts `sort=best-match` and ignores it.  There is no
    usable relevance ordering from here.
  * A quoted phrase is not matched as a phrase.  The target issue's own title,
    `"Missing Anthropic Sonnet 4 model with Bring Your Own Key from Github
    Copilot Chat and Agentic mode"`, returns **17,033,706** hits.
  * A colon inside a quoted phrase appears to break the parse:
    `"error: mprotect failed: 13 (Permission denied)"` returns 8,041,878,
    while the same words unquoted return 532.
  * `A OR B` is not honoured: `"Sonnet" OR "Copilot"` and `Sonnet OR Copilot`
    both return 11,087,649.
  * General web search is unavailable from this VM (`Web search cancelled`;
    DuckDuckGo and Bing both refuse, and Bing answers 200 with results
    unrelated to the query, which is worse than a refusal).

The replacement instrument is **containment**, and it is deterministic.  For a
developer's query to return a document, the document must contain something the
query names.  So for each row: fetch the tracker item the thread points at, and
ask what share of the post's distinctive terms its text actually contains.

  * containment is the **necessary** condition for retrieval.  A term absent
    from the fix's text cannot be matched by any query that names it, so a miss
    here is a real obstruction rather than a failure of ranking.
  * a hit is a **lower bound** on reachability: the fix is findable by
    whatever engine indexes that tracker, whatever this VM can or cannot do.
  * it needs no search engine, no ranking, and no credential, so it is
    reproducible on any machine with the public API.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arms                                                     # noqa: E402
import controls                                                  # noqa: E402
import reach                                                     # noqa: E402

API = "https://api.github.com"


def norm(s):
    """Alphanumeric-only, lowercased: quotes, colons and backticks cannot hide."""
    s = (s or "").lower().replace("\u2019", "'").replace("\u201c", '"') \
                     .replace("\u201d", '"').replace("\u2014", "-")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def words(s):
    return [w for w in norm(s).split() if w]


def terms_norm(text, limit=8):
    """Distinctive terms, each normalised the same way the fix text is.

    DEFECT FOUND AND REPAIRED on the first run of this module: a term was
    compared raw against a text that had been normalised, so every dotted
    identifier (`Docker.app`, `libgfortran.5.dylib`) was scored as absent
    however prominently it appeared.  Four rows read zero coverage partly
    because of the instrument and partly because of the world, and the two
    were not separable until this was fixed.
    """
    return [t for t in controls.terms(text or "", limit=limit) if t]


def covered_terms(post_terms, fix_words):
    fixset = set(fix_words)
    out = []
    for t in post_terms:
        for piece in norm(t).split():
            if piece and piece in fixset:
                out.append(t)
                break
    return out


def longest_run(a_words, b_set_seq):
    """Longest run of consecutive words shared with the other sequence."""
    best = 0
    for i in range(len(a_words)):
        for j in range(i + best + 1, len(a_words) + 1):
            if tuple(a_words[i:j]) in b_set_seq:
                best = j - i
            else:
                break
    return best


def fetch_item(t):
    url = "%s/repos/%s/%s/issues/%d" % (API, t["owner"], t["repo"], t["number"])
    data, err = reach._results(url)
    if err:
        return None, None, err
    item = {"title": data.get("title") or "", "body": data.get("body") or "",
            "state": data.get("state"), "comments": data.get("comments")}
    cdata, cerr = reach._results("%s/repos/%s/%s/issues/%d/comments?per_page=3"
                                 % (API, t["owner"], t["repo"], t["number"]))
    # This endpoint returns a bare JSON array; only the Stack Exchange and the
    # search endpoints wrap in {"items": ...}.  DEFECT FOUND AND REPAIRED on
    # the first run: the wrapper assumption raised AttributeError on every row.
    items = cdata if isinstance(cdata, list) else (cdata or {}).get("items", [])
    comments = [c.get("body") or "" for c in items if isinstance(c, dict)]
    return item, comments, cerr


def main():
    import run as runmod
    threads = json.load(open(os.path.join(HERE, "threads-all.json")))
    plan = arms.load_plan()
    for r in plan:
        t = threads.get(r["qid"], {})
        parts = [t.get("body") or ""]
        for a in (t.get("answers") or []):
            parts.append(a.get("body") or "")
        r["thread_text"] = " ".join(parts)
    rows = []
    for i, r in enumerate(plan, 1):
        t = r["target"]
        item, comments, cerr = fetch_item(t)
        if item is None:
            rows.append({"qid": r["qid"], "error": cerr})
            sys.stderr.write("[%2d/%d] %s FETCH ERROR\n" % (i, len(plan), r["qid"]))
            continue
        fix_text = norm(item["title"] + " " + (item["body"] or "") +
                        " " + " ".join(comments))
        fix_seq = set(tuple(words(item["title"] + " " + (item["body"] or "") +
                                  " " + " ".join(comments))[i:i + k])
                      for k in (2, 3, 4, 5)
                      for i in range(len(words(item["title"] + " " +
                                               (item["body"] or "") + " " +
                                               " ".join(comments))) - k + 1))
        hand = r.get("hand", {})
        post_literal = hand.get("phrase") or hand.get("keyword") or ""
        post_terms = terms_norm(post_literal, limit=8)
        lit_words = words(post_literal)
        fix_words = words(fix_text)
        covered = covered_terms(post_terms, fix_words)
        thread_text = r.get("thread_text") or ""
        thread_words = words(thread_text) if thread_text else []
        run = longest_run(lit_words, fix_seq)
        rows.append({
            "qid": r["qid"], "target": t, "state": item["state"],
            "literal_type": hand.get("literal_type"),
            "post_literal": post_literal,
            "post_terms": post_terms,
            "terms_covered": covered,
            "term_coverage": round(len(covered) / float(len(post_terms)), 4)
            if post_terms else None,
            "literal_words": len(lit_words),
            "longest_shared_word_run": run,
            "literal_contained": " ".join(lit_words) in fix_text
            if lit_words else None,
            "fix_title": item["title"],
            "fix_text_words": len(fix_words),
            "comments_fetched": len(comments), "comments_error": cerr,
            # Decomp: a low fix-coverage row is only an obstruction if the
            # thread did not already state the resolution inline.  Coverage
            # against the whole thread separates "the tracker is unreachable"
            # from "the answer never needed a tracker".
            "thread_coverage": round(
                len(covered_terms(post_terms, thread_words)) / float(len(post_terms)), 4)
            if post_terms else None,
        })
        sys.stderr.write("[%2d/%d] %s cov=%.2f run=%d\n" % (
            i, len(plan), r["qid"], rows[-1]["term_coverage"] or 0.0, run))

    ok = [r for r in rows if "error" not in r]
    covs = [r["term_coverage"] for r in ok if r["term_coverage"] is not None]
    runs = [r["longest_shared_word_run"] for r in ok]
    contained = [r for r in ok if r["literal_contained"]]
    summary = {
        "rows": len(ok), "fetch_errors": [r["qid"] for r in rows
                                          if "error" in r],
        "median_term_coverage": round(sorted(covs)[len(covs) // 2], 4)
        if covs else None,
        "rows_term_coverage_ge_half": sum(1 for c in covs if c >= 0.5),
        "rows_term_coverage_zero": sum(1 for c in covs if c == 0.0),
        "median_longest_shared_run": sorted(runs)[len(runs) // 2] if runs else None,
        "rows_shared_run_ge_3": sum(1 for x in runs if x >= 3),
        "rows_literal_fully_contained": len(contained),
        "by_literal_type": {t: {
            "n": sum(1 for r in ok if r["literal_type"] == t),
            "cov_ge_half": sum(1 for r in ok if r["literal_type"] == t
                               and (r["term_coverage"] or 0) >= 0.5)}
            for t in ("error_message", "ui_string", "code_token", "symptom_only")},
        "detail": [{"qid": r["qid"], "lit": r["literal_type"],
                    "cov": r["term_coverage"], "run": r["longest_shared_word_run"],
                    "contained": r["literal_contained"],
                    "terms": r["post_terms"],
                    "covered": r["terms_covered"],
                    "fix_title": (r["fix_title"] or "")[:80],
                    "fix_words": r["fix_text_words"]} for r in ok],
    }
    json.dump({"summary": summary, "rows": rows},
              open(os.path.join(HERE, "raw", "containment.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "detail"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""E022 arm C: did the requester build it?

The other two arms measure what the thread did. This one asks about the person:
of the needs that were **not** served by any reply, did the requester go and
build the thing themselves?

This is the only arm that can produce something buildable, and it is also the
arm most likely to be wrong, so its limits are stated before it runs:

  * **A false positive is worse than a false negative here.** Any person who
    posted any story after the need comment counts as a candidate builder, and
    most of them posted something unrelated. So the arm produces a *candidate
    list to be hand-checked*, never a rate. The gate below demands the hand check
    exist before any number is computed.
  * **It cannot see a build posted anywhere else.** Someone who built the thing
    and put it on GitHub rather than HN reads as `did_not_build`. The arm
    measures self-disclosure on one site, which is a floor on building and not an
    estimate of it.
  * **Algolia caps paging.** Asking for a thousand hits returns a hundred and
    would read as "this person posted one thing", so paging stops on a short
    page and the cap is recorded.

Sampling: the `not_served` rows of the hand-labelled sample, because the arm's
question is conditional on the thread having failed to serve the need. Running it
over all 1250 authors would cost an hour to answer a question about a population
whose other two arms are already measured.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:  # pragma: no cover
    ThreadPoolExecutor = None

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
LABELS = os.path.join(HERE, "raw", "labels.tsv")
PARENTS = os.path.join(HERE, "..", "019-corpus-person-diversity",
                       "raw", "corpus_authors.jsonl")
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(RAW, "author_stories.jsonl")
ALGOLIA_AUTHOR = ("https://hn.algolia.com/api/v1/search_by_date"
                  "?tags=author_%s&hitsPerPage=100&page=%d")
WORKERS = 8
TRIES = 3
PAGE_CAP = 10
HTMLISH = re.compile(r"<(?:!doctype|html|head|body|title)\b", re.I)
TAG = re.compile(r"<[^>]+>")


def text_of(t):
    t = TAG.sub(" ", t or "")
    for a, b in (("&#x27;", "'"), ("&#39;", "'"), ("&quot;", '"'),
                 ("&gt;", ">"), ("&lt;", "<"), ("&amp;", "&")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def get(url, timeout=25):
    for attempt in range(TRIES):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception:
            if attempt + 1 == TRIES:
                return None, ""
            time.sleep(0.4 * (attempt + 1))
    return None, ""


def stories_after(author, need_epoch):
    """Stories this author posted after the need statement."""
    rows = []
    pages = 0
    truncated = False
    for page in range(PAGE_CAP):
        st, body = get(ALGOLIA_AUTHOR % (author, page))
        pages += 1
        if st != 200:
            return ("read_failed" if page == 0 else "read_partial"), rows, pages, truncated
        if HTMLISH.search(body[:400]):
            return "challenge", rows, pages, truncated
        try:
            data = json.loads(body)
        except ValueError:
            return "not_json", rows, pages, truncated
        hits = data.get("hits") or []
        if not hits:
            break
        for h in hits:
            created = h.get("created_at_i")
            # The discriminator is `_tags`, not `type`.
            #
            # Algolia's `search_by_date` returns a `type` field on some routes
            # and omits it on this one, where every hit carries a null `type`
            # and the real kind lives in `_tags` as the literal `story` or
            # `comment`. Reading `type` therefore yields *zero* story rows for
            # every author, and the arm reports "nobody built anything" with
            # total confidence -- the same shape as F002, where a schema
            # mismatch between two APIs for the same site recorded 1313 of 1313
            # rows as successful with a null value. A guard asserts the tags
            # really do carry the discriminator rather than assuming it.
            tags = h.get("_tags") or []
            if created and created > need_epoch and "story" in tags:
                rows.append({
                    "id": h.get("objectID"),
                    "title": h.get("title"),
                    "url": h.get("url"),
                    "created_at": h.get("created_at"),
                    "points": h.get("points"),
                    "text": text_of(h.get("comment_text") or h.get("story_text") or "")[:200],
                })
        if len(hits) < 100:
            break
    else:
        truncated = True
    return "ok", rows, pages, truncated


def assert_tag_discriminator(sample_author="pg"):
    """Falsify the `_tags` rule against a known story-poster.

    The bug this replaces was invisible: it returned zero rows and read as a
    finding about the world. This asks the reader for a page whose kind it
    claims to be able to tell, and fails loudly if it cannot. Run before the
    arm's numbers are believed.
    """
    st, body = get(ALGOLIA_AUTHOR % (sample_author, 0))
    if st != 200:
        return False, "reader returned %s" % st
    data = json.loads(body)
    hits = data.get("hits") or []
    if not hits:
        return False, "no hits for the known-poster control"
    kinds = set()
    for h in hits[:50]:
        tags = h.get("_tags") or []
        kinds.add("story" if "story" in tags else
                  ("comment" if "comment" in tags else "unknown"))
    if "unknown" in kinds:
        return False, "_tags does not discriminate: saw %s" % sorted(kinds)
    return True, "kinds seen in first 50 hits: %s" % sorted(kinds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--check", default="raw/build_check.tsv",
                    help="hand-checked table of candidate builders")
    args = ap.parse_args()

    labels = {}
    for line in open(LABELS):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2 and p[1]:
            labels[p[0]] = p[1]
    outcome = {str(json.loads(l)["comment_id"]): json.loads(l)
               for l in open(OUTCOMES)}
    parents = {str(json.loads(l)["comment_id"]): json.loads(l)
               for l in open(PARENTS)}

    # The arm's population: need statements the thread did NOT serve.
    targets = [(cid, lab) for cid, lab in labels.items()
               if lab in ("not_served", "partial")]
    targets.sort(key=lambda t: int(t[0]))

    if args.verify:
        return verify(targets)

    ok, why = assert_tag_discriminator()
    print("_tags discriminator control: %s (%s)" % ("PASS" if ok else "FAIL", why))
    if not ok:
        print("CONTROL FAILED: the arm cannot tell a story from a comment.")
        return 1

    os.makedirs(RAW, exist_ok=True)
    got = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        def work(t):
            cid, lab = t
            author = parents.get(cid, {}).get("author")
            need_epoch = outcome[cid].get("time")
            if not author or not need_epoch:
                return {"comment_id": cid, "label": lab, "status": "no_author"}
            st, rows, pages, trunc = stories_after(author, need_epoch)
            return {
                "comment_id": cid, "label": lab, "author": author,
                "status": st, "pages_read": pages, "truncated": trunc,
                "n_stories_after": len(rows), "stories": rows[:20],
            }
        for n, rec in enumerate(pool.map(work, targets), 1):
            got.append(rec)
            if n % 10 == 0:
                sys.stderr.write("%d/%d %.0fs\n" % (n, len(targets), time.time() - t0))

    with open(OUT, "w") as f:
        for rec in sorted(got, key=lambda r: int(r["comment_id"])):
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    cand = sum(1 for r in got if r.get("n_stories_after"))
    print("population (not_served + partial) %d" % len(got))
    print("readable %d" % sum(1 for r in got if r["status"].startswith("ok")))
    print("with >=1 story posted after the need  %d" % cand)
    print("truncated at the page cap              %d"
          % sum(1 for r in got if r.get("truncated")))
    print("candidate builders -- HAND CHECK REQUIRED, see %s" % args.check)
    return 0


def verify(targets):
    rows = []
    if os.path.exists(OUT):
        rows = [json.loads(l) for l in open(OUT)]
    problems = []
    missing = [c for c, _ in targets if str(c) not in
               {str(r["comment_id"]) for r in rows}]
    if missing:
        problems.append("%d targets absent from the arm's capture" % len(missing))
    cand = [r for r in rows if r.get("n_stories_after")]
    check_path = os.path.join(HERE, args_check_default())
    checked = set()
    if os.path.exists(check_path):
        for line in open(check_path):
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2 and p[1]:
                checked.add(str(p[0]))
    unchecked = [r for r in cand if str(r["comment_id"]) not in checked]
    print("population            %d" % len(targets))
    print("captured rows         %d" % len(rows))
    print("candidate builders    %d" % len(cand))
    print("hand-checked          %d" % len(checked))
    print("awaiting a hand check %d" % len(unchecked))
    if cand and unchecked:
        problems.append("%d candidate builders are unchecked, so no rate may be "
                        "computed from this arm" % len(unchecked))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


def args_check_default():
    return os.path.join(RAW, "build_check.tsv")


if __name__ == "__main__":
    sys.exit(main())

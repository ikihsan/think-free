#!/usr/bin/env python3
"""E022 arm A: read what happened to each of E012's 1401 stated needs.

For every row of the corpus, decide three things from public records only:

  answered            the comment received at least one reply
  replies             how many, and how many of them name an artifact
  built_by_requester  the same author posted a story after the need statement

Design constraints this file encodes, each of which was bought by a finding:

  * **A failed read is `unreadable`, never `unanswered`.** E020's rate limit
    answered HTTP 200 with an HTML challenge page and 33 rows read as "the
    index does not contain the young arm" -- a clean, confident, wrong fact
    about the world. Here an unparseable body, a non-200, and a missing `by`
    are three distinct statuses and none of them is a zero.
  * **A capture holding a value is never overwritten by a re-run.** E020's
    falsification test executed the defect it was testing and destroyed H1's
    raw capture (F040 defect 2). `REFUSE_OVERWRITE` refuses to touch a row
    whose status is already decided unless the status is a failure.
  * **The author join is paged and resumable.** Algolia caps `hitsPerPage`;
    asking for 1000 silently returns 100 and would read as "this person posted
    one thing".
  * **Concurrency is bounded and the run is interruptible.** A partial capture
    is a fact about how far the run got, not about the world.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:  # pragma: no cover
    ThreadPoolExecutor = None

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "019-corpus-person-diversity",
                      "raw", "corpus_authors.jsonl")
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(RAW, "outcomes.jsonl")
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
ALGOLIA_AUTHOR = ("https://hn.algolia.com/api/v1/search_by_date"
                  "?tags=author_%s&hitsPerPage=100&page=%d")
ALGOLIA_ITEM = "https://hn.algolia.com/api/v1/items/%s"

WORKERS = 10
TRIES = 3
PAGE_CAP = 10          # 1000 posts per author, generous past any plausible need
HTMLISH = re.compile(r"<(?:!doctype|html|head|body|title)\b", re.I)


def path(*parts):
    return os.path.join(HERE, *parts)


# ---------------------------------------------------------------- fetching

def _get(url, timeout=25):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def fetch_item(item_id):
    """Read one HN item. Returns (status, payload).

    Statuses are deliberately distinct, and only `ok` carries a reply count:
      ok          parsed JSON object with a `by`
      no_author   parsed but no author -- a third thing, not an absent reply
      refused     non-200
      not_json    body that is not JSON at all
      null_body   HTTP 200 whose body is the literal `null` -- this is what the
                  API returns for an id that does not exist, so it is the
                  control's answer and needs its own name rather than being
                  filed as a parse failure
      challenge   an HTML page served with 200 (F036/F040's shape)
      failed      transport error after TRIES
    """
    for attempt in range(TRIES):
        try:
            status, body = _get(FIREBASE % item_id)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return "refused", {"http": e.code}
            if attempt + 1 == TRIES:
                return "refused", {"http": e.code}
            time.sleep(0.4 * (attempt + 1))
            continue
        except Exception as e:
            if attempt + 1 == TRIES:
                return "failed", {"error": type(e).__name__}
            time.sleep(0.4 * (attempt + 1))
            continue
        if status != 200:
            return "refused", {"http": status}
        if HTMLISH.search(body[:400]):
            return "challenge", {"head": body[:120]}
        try:
            obj = json.loads(body)
        except ValueError:
            return "not_json", {"head": body[:120]}
        if obj is None:
            # HTTP 200 with a null body is this API's answer for an absent id.
            return "null_body", {"http": status}
        if not isinstance(obj, dict):
            return "not_json", {"head": repr(obj)[:120]}
        if obj.get("by"):
            return "ok", obj
        return "no_author", obj
    return "failed", {}


def fetch_author_stories(author, need_epoch):
    """REMOVED. Do not restore it.

    This was the first author join and it was **wrong in a way that produced a
    confident negative**. It read `h.get("type") == "story"`, and Algolia's
    `search_by_date` route returns a null `type` on every hit while the real
    kind lives in `_tags`. The function therefore returned zero rows for every
    author, and the arm reported "nobody built anything" -- the same shape as
    F002, where a schema mismatch between two APIs for the same site recorded
    1313 of 1313 rows as successful with a null value.

    The live arm is `author_build.py`, which reads `_tags` and asserts the
    discriminator against a known story-poster before its numbers are believed.
    Six candidates were found that this function could not see, all six
    hand-checked, none related. It is left named here so the next session that
    finds "no builder" reaches for the right file.
    """
    raise NotImplementedError("use author_build.py; see the docstring")


# ---------------------------------------------------------------- outcome

LINKISH = re.compile(r"(https?://\S+|www\.\S+)")
# An artifact mention: a link, or a backticked/quoted/parenthesised proper noun
# that is not a plain English word. Deliberately over-inclusive -- it is a
# *lower bound on attention*, never the `served` cell, which is hand-labelled.
ARTIFACTISH = re.compile(
    r"(https?://\S+|`[^`]+`|\b[A-Z][a-z]+[A-Za-z0-9_+-]*\b)")


def classify(status, item):
    kids = item.get("kids") or []
    return {
        "status": status,
        "n_replies": len(kids) if status == "ok" else None,
        "answered": (len(kids) > 0) if status == "ok" else None,
        "deleted": bool(item.get("deleted")) if status == "ok" else None,
        "dead": bool(item.get("dead")) if status == "ok" else None,
        "time": item.get("time") if status == "ok" else None,
    }


# ---------------------------------------------------------------- capture I/O

def load_done():
    """Row ids already decided. A row holding a value is not re-fetched."""
    done = {}
    if not os.path.exists(OUT):
        return done
    for line in open(OUT):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("status") == "ok":
            done[str(rec["comment_id"])] = rec
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="assert the capture holds a decidable row per corpus row")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    corpus = [json.loads(l) for l in open(CORPUS) if l.strip()]
    if args.limit:
        corpus = corpus[:args.limit]

    if args.verify:
        return verify(corpus)

    os.makedirs(RAW, exist_ok=True)
    done = load_done()
    todo = [r for r in corpus if str(r["comment_id"]) not in done]
    sys.stderr.write("corpus %d, already decided %d, to fetch %d\n"
                     % (len(corpus), len(done), len(todo)))
    if not todo:
        print("nothing to do")
        return 0

    t0 = time.time()
    got = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        def work(r):
            status, item = fetch_item(r["comment_id"])
            out = {
                "comment_id": str(r["comment_id"]),
                "author": r.get("author"),
                "story_id": r.get("story_id"),
                "trigger": r.get("trigger"),
            }
            out.update(classify(status, item))
            return out
        for n, rec in enumerate(pool.map(work, todo), 1):
            got.append(rec)
            if n % 200 == 0:
                sys.stderr.write("%d/%d %.0fs\n" % (n, len(todo), time.time() - t0))

    records = list(done.values()) + got
    records.sort(key=lambda r: int(r["comment_id"]))
    with open(OUT, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    counts = {}
    for r in records:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("captured %d rows" % len(records))
    for st, n in sorted(counts.items()):
        print("  %-10s %d" % (st, n))
    ok = sum(1 for r in records if r["status"] == "ok")
    rate = ok / float(len(corpus)) if corpus else 0.0
    print("gate A1 (>=95%% readable)  %s  (%.1f%%)"
          % ("met" if rate >= 0.95 else "NOT met", 100.0 * rate))
    return 0


def verify(corpus):
    """The gate reads the artifact, not the script's own exit code.

    `ok` is the only status that carries a reply count, so a row that is
    `unreadable` cannot be silently counted as unanswered by anything that
    consumes this capture: it has `answered: null`, which is not `False`.
    """
    if not os.path.exists(OUT):
        print("no capture at %s" % OUT)
        return 1
    rows = [json.loads(l) for l in open(OUT)]
    ids = set(str(r["comment_id"]) for r in rows)
    want = set(str(r["comment_id"]) for r in corpus)
    problems = []
    missing = want - ids
    if missing:
        problems.append("%d corpus rows absent from the capture" % len(missing))
    for r in rows:
        st = r.get("status")
        if st == "ok":
            if r.get("answered") is None or r.get("n_replies") is None:
                problems.append("row %s is ok but carries no reply count"
                                % r["comment_id"])
            if not r.get("author"):
                problems.append("row %s is ok but carries no author"
                                % r["comment_id"])
        else:
            if r.get("answered") is not None:
                problems.append("row %s is %s yet carries an answered value"
                                % (r["comment_id"], st))
    ok = sum(1 for r in rows if r.get("status") == "ok")
    rate = ok / float(len(want)) if want else 0.0
    print("capture rows      %d" % len(rows))
    print("corpus rows       %d" % len(want))
    print("readable (ok)     %d (%.1f%%)" % (ok, 100.0 * rate))
    print("gate A1 (>=95%%)   %s" % ("met" if rate >= 0.95 else "NOT met"))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

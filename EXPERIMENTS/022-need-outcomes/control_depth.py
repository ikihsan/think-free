#!/usr/bin/env python3
"""E022 arm B2: the depth-matched control.

The first control compared 1401 need comments against 13409 non-trigger
siblings and found a lift of 0.81x. That number cannot be reported yet, because
**the control is structurally top-level only** -- `sibling_candidates` reads the
story's kid list -- while 760 of the 1401 need comments are replies to another
comment. Depth is a known driver of reply probability, so the pooled comparison
confounds "carries a need trigger" with "sits at the top of a thread".

This arm removes the confound by collecting non-trigger comments at **both**
depths and recording each one's own depth, so the comparison can be stratified.
It also records comment length, because a trigger phrase mid-sentence and a
30-word aside are not comparable contributions to a thread.

Method, stated rather than taste:
  * for each story the corpus drew from, walk its top-level comments and then
    one level of replies beneath them,
  * keep comments carrying none of the 24 trigger phrases,
  * record depth (0 = direct reply to the story) and length,
  * cap per story per depth so one thread cannot dominate.
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
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
NEEDS = os.path.join(HERE, "..", "012-candidate-harvest",
                     "raw", "hn_needs_2026-10-04.jsonl")
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(RAW, "control_depth.jsonl")
CORPUS_PARENTS = os.path.join(HERE, "..", "019-corpus-person-diversity",
                              "raw", "corpus_authors.jsonl")

FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 10
TRIES = 3
STORY_CHILD_CAP = 60
CAP_PER_DEPTH = 12
KIDS_PER_PARENT = 12
# Stories sampled for the depth-matched arm. The full 1276 takes hours on two
# CPUs; the arm only needs enough stories to fill both strata, so a stated
# stride is used and the sampling rule is recorded with the result.
STORY_STRIDE = int(os.environ.get("E022_STORY_STRIDE", "1"))
HTMLISH = re.compile(r"<(?:!doctype|html|head|body|title)\b", re.I)


def _get(url, timeout=25):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def fetch(url, timeout=25):
    for attempt in range(TRIES):
        try:
            status, body = _get(url, timeout)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404) or attempt + 1 == TRIES:
                return ("refused", {"http": e.code})
            time.sleep(0.4 * (attempt + 1))
            continue
        except Exception as e:
            if attempt + 1 == TRIES:
                return ("failed", {"error": type(e).__name__})
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
            return "null_body", {"http": status}
        if not isinstance(obj, dict):
            return "not_json", {"head": repr(obj)[:120]}
        return "ok", obj
    return "failed", {}


def trigger_phrases():
    """Read from E012's own capture -- never a second copy of the rule (E020)."""
    return set(json.loads(l)["trigger"].lower()
               for l in open(NEEDS) if l.strip())


def text_of(item):
    t = item.get("text") or ""
    t = re.sub(r"<[^>]+>", " ", t)
    t = (t.replace("&#x27;", "'").replace("&#39;", "'")
          .replace("&quot;", '"').replace("&gt;", ">")
          .replace("&lt;", "<").replace("&amp;", "&"))
    return re.sub(r"\s+", " ", t).strip()


def walk(story_id, phrases):
    """Non-trigger comments at depth 0 and depth 1, with depth and length.

    One fetch per top-level comment, then one per reply beneath each. The
    per-depth cap is applied by the caller so a single 500-comment thread cannot
    decide a stratum.
    """
    status, story = fetch(FIREBASE % story_id)
    if status != "ok":
        return status, []
    top = (story.get("kids") or [])[:STORY_CHILD_CAP]
    if not top:
        return "empty", []
    rows = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        items = list(pool.map(lambda k: fetch(FIREBASE % k), top))
    # Collect the ids to descend into first, so one thread pool covers both
    # depths rather than opening a second pool per top-level comment.
    descend = []
    for st, item in items:
        if st != "ok":
            continue
        txt = text_of(item)
        if any(p in txt.lower() for p in phrases):
            continue
        kids = item.get("kids") or []
        rows.append({
            "comment_id": str(item.get("id")),
            "story_id": story_id,
            "depth": 0,
            "n_replies": len(kids),
            "answered": len(kids) > 0,
            "len": len(txt),
            "has_trigger": False,
        })
        descend.extend(kids[:KIDS_PER_PARENT])
    if not descend:
        return "ok", rows
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for st, kid in pool.map(lambda k: fetch(FIREBASE % k), descend):
            if st != "ok":
                continue
            t2 = text_of(kid)
            if any(p in t2.lower() for p in phrases):
                continue
            k2 = kid.get("kids") or []
            rows.append({
                "comment_id": str(kid.get("id")),
                "story_id": story_id,
                "depth": 1,
                "n_replies": len(k2),
                "answered": len(k2) > 0,
                "len": len(t2),
                "has_trigger": False,
            })
    return "ok", rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if args.verify:
        return verify()

    need = [json.loads(l) for l in open(OUTCOMES)]
    stories = sorted(set(r["story_id"] for r in need))
    if STORY_STRIDE > 1:
        stories = stories[::STORY_STRIDE]
    if args.limit:
        stories = stories[:args.limit]
    phrases = trigger_phrases()
    sys.stderr.write("stories %d, phrases %d\n" % (len(stories), len(phrases)))
    os.makedirs(RAW, exist_ok=True)

    # Resume: a story already walked is not walked again, so an interrupted run
    # keeps what it fetched. E020 lost nine counts to a clobbering capture; a
    # capture that is only ever appended to cannot lose them.
    walked = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            walked.add(str(rec.get("story_id")))
    todo = [s for s in stories if str(s) not in walked]
    sys.stderr.write("stories %d, already walked %d, to walk %d\n"
                     % (len(stories), len(stories) - len(todo), len(todo)))

    got = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        def work(sid):
            st, rows = walk(sid, phrases)
            # cap per depth so one thread cannot dominate either stratum
            capped, seen = [], {}
            for r in rows:
                seen[r["depth"]] = seen.get(r["depth"], 0) + 1
                if seen[r["depth"]] <= CAP_PER_DEPTH:
                    capped.append(r)
            return sid, st, capped
        for n, (sid, st, rows) in enumerate(pool.map(work, todo), 1):
            got.extend(rows)
            if n % 25 == 0:
                sys.stderr.write("%d/%d stories %.0fs, %d rows this run\n"
                                 % (n, len(todo), time.time() - t0, len(got)))
                # flush so an interruption keeps progress
                _write(got)

    _write(got)
    total = _count()
    print("depth-matched control rows: %d total, %d this run"
          % (total, len(got)))
    print("story stride %d" % STORY_STRIDE)
    return 0


def _write(new_rows):
    """Merge into the capture without losing what an earlier run fetched."""
    uniq = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            uniq[str(rec["comment_id"])] = rec
    for r in new_rows:
        uniq[str(r["comment_id"])] = r
    ordered = [uniq[k] for k in sorted(uniq, key=int)]
    tmp = OUT + ".tmp"
    with open(tmp, "w") as f:
        for r in ordered:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    os.replace(tmp, OUT)


def _count():
    if not os.path.exists(OUT):
        return 0
    return sum(1 for _ in open(OUT))


def verify():
    if not os.path.exists(OUT):
        print("no depth control capture")
        return 1
    rows = [json.loads(l) for l in open(OUT)]
    problems = []
    depths = set()
    for r in rows:
        depths.add(r.get("depth"))
        if r.get("depth") not in (0, 1):
            problems.append("row %s has depth %r" % (r.get("comment_id"), r.get("depth")))
        if r.get("has_trigger") is not False:
            problems.append("row %s does not assert has_trigger=False" % r.get("comment_id"))
        if r.get("answered") is None or r.get("len") is None:
            problems.append("row %s is missing an outcome or a length" % r.get("comment_id"))
    d0 = sum(1 for r in rows if r.get("depth") == 0)
    d1 = sum(1 for r in rows if r.get("depth") == 1)
    print("rows %d  depth0 %d  depth1 %d  depths %s"
          % (len(rows), d0, d1, sorted(x for x in depths if x is not None)))
    print("gate A1 analogue: both depths present -> %s"
          % ("met" if d0 and d1 else "NOT met"))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

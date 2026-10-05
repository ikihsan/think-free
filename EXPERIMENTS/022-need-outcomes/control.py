#!/usr/bin/env python3
"""E022 arm B: the within-thread control, and the negative control C2.

The claim under test is that *stating a need* makes a comment more likely to be
answered. The obvious rival is that some threads are simply busy. So this fetches
the sibling comments of every story the corpus drew from -- comments that do not
carry any of the 23 trigger phrases -- and compares reply rates **inside the same
thread**.

  lift = P(replied-to | comment carries a need trigger)
       / P(replied-to | comment in the same thread carries no trigger)

A lift at or below 1.0 means the trigger vocabulary carries no information about
being answered, and PROTOCOL.md gate A2 declares that `not informative`.

Sampling is stated rather than taste: every non-trigger sibling of every story
the corpus used, capped per story so one 500-comment thread cannot dominate.
The cap and the cap's effect on the estimate are both reported.
"""
import argparse
import collections
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
OUT = os.path.join(RAW, "control.jsonl")

FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 10
TRIES = 3
PER_STORY_CAP = 12        # siblings sampled per story
STORY_CHILD_CAP = 120     # deepest sibling id list read per story
HTMLISH = re.compile(r"<(?:!doctype|html|head|body|title)\b", re.I)


def _get(url, timeout=25):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def fetch(url, timeout=25):
    """Same status discipline as run.py: an unread is never a zero."""
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
    """The 23 phrases E012 harvested with, read from its own capture.

    Not restated here. A second copy of a naming rule is one of the six
    instrument defects E020 recorded: when the capture format changed, all 22
    configurations became `no_origin` because the rule lived in two places.
    """
    phrases = set()
    with open(NEEDS) as f:
        for line in f:
            if line.strip():
                phrases.add(json.loads(line)["trigger"].lower())
    return phrases


def has_trigger(text, phrases):
    t = (text or "").lower()
    return any(p in t for p in phrases)


def sibling_candidates(story_id, phrases):
    """Top-level comments of a story that carry no trigger phrase."""
    status, story = fetch(FIREBASE % story_id)
    if status != "ok":
        return status, []
    kids = (story.get("kids") or [])[:STORY_CHILD_CAP]
    if not kids:
        return "empty", []
    out = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for st, item in pool.map(lambda k: fetch(FIREBASE % k), kids):
            if st != "ok":
                continue
            if has_trigger(item.get("text"), phrases):
                continue
            out.append((item.get("id"), len(item.get("kids") or [])))
    return "ok", out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(OUTCOMES)]
    stories = sorted(set(r["story_id"] for r in rows))
    if args.limit:
        stories = stories[:args.limit]
    phrases = trigger_phrases()
    sys.stderr.write("stories %d, trigger phrases %d\n" % (len(stories), len(phrases)))

    if args.verify:
        return verify()

    os.makedirs(RAW, exist_ok=True)
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("status") == "ok":
                done.add(rec["comment_id"])

    t0 = time.time()
    got = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        def work(sid):
            st, sibs = sibling_candidates(sid, phrases)
            return sid, st, sibs[:PER_STORY_CAP]
        for n, (sid, st, sibs) in enumerate(pool.map(work, stories), 1):
            for cid, nreplies in sibs:
                if str(cid) in done:
                    continue
                got.append({
                    "comment_id": str(cid),
                    "story_id": sid,
                    "status": "ok",
                    "n_replies": nreplies,
                    "answered": nreplies > 0,
                    "has_trigger": False,
                })
            if n % 100 == 0:
                sys.stderr.write("%d/%d stories %.0fs, %d siblings\n"
                                 % (n, len(stories), time.time() - t0, len(got)))

    records = got + [json.loads(l) for l in open(OUT)] if os.path.exists(OUT) else got
    uniq = {}
    for rec in records:
        uniq[str(rec["comment_id"])] = rec
    ordered = [uniq[k] for k in sorted(uniq, key=int)]
    with open(OUT, "w") as f:
        for rec in ordered:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("control siblings captured: %d" % len(ordered))
    return 0


def verify():
    if not os.path.exists(OUT):
        print("no control capture")
        return 1
    rows = [json.loads(l) for l in open(OUT)]
    problems = []
    for r in rows:
        if r.get("has_trigger") is not False:
            problems.append("control row %s does not assert has_trigger=False"
                            % r.get("comment_id"))
        if r.get("answered") is None:
            problems.append("control row %s carries no answered value"
                            % r.get("comment_id"))
    print("control rows %d, stories %d"
          % (len(rows), len(set(r["story_id"] for r in rows))))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

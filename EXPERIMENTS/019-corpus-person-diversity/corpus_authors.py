#!/usr/bin/env python3
"""Arm A: count the people in E012's need corpus.

The corpus is 1401 rows. Nobody has counted how many people wrote them, and
every conclusion the mission draws from this corpus depends on that number. This
script fetches each comment's primary source record -- Hacker News's own item
API -- and reports authorship, not a text statistic.

Design notes that matter for reading the output:

  * **The author field is ``by`` on the Firebase API.** The first attempt of
    this script asked for ``author``, which is Algolia's name for the same
    field, and therefore recorded 1313 of 1313 rows as ``ok`` with a null
    author. That capture is kept at ``raw/corpus_authors.attempt1.jsonl``
    because the shape of that failure -- a schema mismatch between two APIs for
    the same site -- is part of the evidence, not a nuisance.
  * A failed fetch is recorded as ``failed``, never as an absent author. Gate
    A1 (>=95% recovered) is what stops a partial fetch from reading as a small
    audience. A *recovered null* author is a third thing, kept as its own
    status, because that is what the first attempt produced in bulk.
  * The fetch is concurrent and resumable: ~0.8 s per request serially is 19
    minutes for 1401 rows, which is longer than a foreground tool timeout.
"""
import json
import os
import sys
import time
import urllib.request

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:  # pragma: no cover - Python 2 shape, unused here
    ThreadPoolExecutor = None

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(
    HERE, "..", "012-candidate-harvest", "raw", "hn_needs_2026-10-04.jsonl")
OUT = os.path.join(HERE, "raw", "corpus_authors.jsonl")
ITEM = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 12
TRIES = 3


def path(*parts):
    return os.path.join(HERE, *parts)


def fetch(item_id):
    """Return (status, item). status is ok / null_author / failed."""
    for attempt in range(TRIES):
        try:
            with urllib.request.urlopen(ITEM % item_id, timeout=20) as r:
                if r.status != 200:
                    return "failed", None
                item = json.loads(r.read().decode("utf-8"))
            if not isinstance(item, dict):
                return "failed", None
            if item.get("by"):
                return "ok", item
            return "null_author", item
        except Exception:
            if attempt + 1 == TRIES:
                return "failed", None
            time.sleep(0.4 * (attempt + 1))
    return "failed", None


def main():
    rows = [json.loads(l) for l in open(CORPUS) if l.strip()]
    seen = set()
    ordered = []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        ordered.append(r)

    done = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("status") == "ok":
                done[rec["comment_id"]] = rec
    todo = [r for r in ordered if str(r["id"]) not in done]
    print("corpus %d, already recovered %d, to fetch %d"
          % (len(ordered), len(done), len(todo)))

    os.makedirs(path("raw"), exist_ok=True)
    got = []
    if todo:
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            for n, (status, item) in enumerate(
                    pool.map(lambda r: fetch(r["id"]), todo), 1):
                src = todo[n - 1]
                rec = {
                    "comment_id": str(src["id"]),
                    "story_id": src.get("story_id"),
                    "trigger": src.get("trigger"),
                    "corpus_date": src.get("created"),
                    "status": status,
                }
                if item is not None:
                    rec["author"] = item.get("by")
                    rec["type"] = item.get("type")
                    rec["parent"] = item.get("parent")
                    rec["posted"] = item.get("time")
                    rec["deleted"] = bool(item.get("deleted"))
                    rec["dead"] = bool(item.get("dead"))
                got.append(rec)
                if n % 200 == 0:
                    sys.stderr.write("%d/%d %.0fs\n"
                                     % (n, len(todo), time.time() - t0))
    records = list(done.values()) + got
    records.sort(key=lambda r: (int(r["comment_id"]),))
    with open(OUT, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    total = len(ordered)
    ok = [r for r in records if r.get("status") == "ok" and r.get("author")]
    rate = len(ok) / float(total) if total else 0.0
    print("comments            %d" % total)
    print("captured rows       %d" % len(records))
    print("author recovered    %d (%.1f%%)" % (len(ok), 100.0 * rate))
    print("gate A1 (>=95%%)     %s" % ("met" if rate >= 0.95 else "NOT met"))
    for st in ("failed", "null_author"):
        n = sum(1 for r in records if r.get("status") == st)
        if n:
            print("%-19s %d" % (st, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
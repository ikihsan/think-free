#!/usr/bin/env python3
"""E022: add comment length to the need arm, so the lift can be checked against it.

The depth-stratified lift came out at 0.69x -- need comments attract *fewer*
replies than their thread neighbours. Before that is reported as a fact about
stating needs, one rival has to be ruled out, and it is a strong one: **comment
length predicts reply count.** In the control arm, answered comments average 446
characters and unanswered ones 329, and a 122-character difference separates the
two groups.

Need statements are plausibly short -- "I wish there was X" is a clause, not an
essay -- so a length mismatch would manufacture the entire effect.

The outcome capture never recorded length, so this fetches the need arm's texts
and joins them. The comparison that matters is **within a length band**: if the
lift survives there, length is not the explanation.
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
NEEDS = os.path.join(HERE, "..", "012-candidate-harvest",
                     "raw", "hn_needs_2026-10-04.jsonl")
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(RAW, "need_len.jsonl")
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 10
TRIES = 3
TAG = re.compile(r"<[^>]+>")


def text_of(t):
    t = TAG.sub(" ", t or "")
    for a, b in (("&#x27;", "'"), ("&#39;", "'"), ("&quot;", '"'),
                 ("&gt;", ">"), ("&lt;", "<"), ("&amp;", "&")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def fetch_text(item_id):
    for attempt in range(TRIES):
        try:
            with urllib.request.urlopen(FIREBASE % item_id, timeout=25) as r:
                if r.status != 200:
                    return "refused", None
                obj = json.loads(r.read().decode("utf-8", "replace"))
            if isinstance(obj, dict) and obj.get("text"):
                return "ok", text_of(obj.get("text"))
            return "no_text", None
        except Exception:
            if attempt + 1 == TRIES:
                return "failed", None
            time.sleep(0.4 * (attempt + 1))
    return "failed", None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(OUTCOMES)]
    if args.verify:
        return verify(len(rows))

    os.makedirs(RAW, exist_ok=True)
    done = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("len") is not None:
                done[str(rec["comment_id"])] = rec
    todo = [r for r in rows if str(r["comment_id"]) not in done]
    sys.stderr.write("need arm %d, have length %d, to fetch %d\n"
                     % (len(rows), len(done), len(todo)))

    got = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for n, (r, (st, txt)) in enumerate(
                zip(todo, pool.map(lambda x: fetch_text(str(x["comment_id"])), todo)), 1):
            got.append({
                "comment_id": str(r["comment_id"]),
                "status": st,
                "len": len(txt) if txt else None,
            })
            if n % 200 == 0:
                sys.stderr.write("%d/%d\n" % (n, len(todo)))

    records = list(done.values()) + got
    with open(OUT, "w") as f:
        for rec in sorted(records, key=lambda r: int(r["comment_id"])):
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    have = sum(1 for r in records if r.get("len") is not None)
    print("need comments %d, with a length %d (%.1f%%)"
          % (len(records), have, 100.0 * have / max(1, len(records))))
    return 0


def verify(n):
    if not os.path.exists(OUT):
        print("no length capture")
        return 1
    rows = [json.loads(l) for l in open(OUT)]
    have = [r for r in rows if r.get("len") is not None]
    problems = []
    if len(rows) < n:
        problems.append("%d rows for a population of %d" % (len(rows), n))
    if not have:
        problems.append("no row carries a length")
    print("rows %d, with a length %d (%.1f%%)"
          % (len(rows), len(have), 100.0 * len(have) / max(1, len(rows))))
    if have:
        ls = sorted(r["len"] for r in have)
        print("need length median %d, p25 %d, p75 %d, mean %.0f"
              % (ls[len(ls) // 2], ls[len(ls) // 4], ls[3 * len(ls) // 4],
                 sum(ls) / float(len(ls))))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

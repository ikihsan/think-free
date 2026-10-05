#!/usr/bin/env python3
"""E022: resolve the remaining need-comment depths.

434 of the 1401 need comments came back with `depth: null`, and the verify gate
correctly refuses to pass while that is true.

**The first diagnosis of that residue was wrong, and it is recorded here because
the wrong diagnosis is what a later session would have inherited.** It read the
ancestors as unreadable-but-fetchable: a pass fetched 432 of them with status
`ok` and resolved nothing, which looked like "it only advanced one hop per round
and gave up when the next round had no *new* ancestors to fetch". Every one of
those 432 was already in `parent`, so the next round correctly had nothing new to
fetch. **The loop never re-appended the chain's next node -- it re-appended the
same node with a larger hop count** -- so `node == sid` was never true for any
chain longer than one hop, and the run printed "no new ancestors" 29 times and
gave up. The first three chains sampled resolve live at 4, 2 and 3 hops.

That is not neutral. `null` rows are excluded from the depth strata, and the ones
being excluded are the *deeply nested* ones -- systematically different comments.
Leaving them out would reweight the population toward shallow comments, which is
the stratum with the highest reply rate, in the direction that manufactures a
result.

`depth(c) = 0` when `parent(c)` is the story, and `depth(c) = 1 + depth(parent(c))`
otherwise, so this walks each chain up to the story and counts the hops, memoising
each `(node, story)` pair because threads share ancestors. Every fetch is recorded
in `raw/depth_walk_fetches.jsonl`, so any residue left `null` is a fact about the
API rather than about this walk.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from collections import Counter

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:  # pragma: no cover
    ThreadPoolExecutor = None

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
PARENTS = os.path.join(HERE, "..", "019-corpus-person-diversity",
                       "raw", "corpus_authors.jsonl")
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(RAW, "need_depth.jsonl")
FETCHLOG = os.path.join(RAW, "depth_walk_fetches.jsonl")
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 12
TRIES = 3
HARD_CAP = 30          # no real thread nests a comment 30 replies deep


def fetch_parent(item_id):
    for attempt in range(TRIES):
        try:
            with urllib.request.urlopen(FIREBASE % item_id, timeout=25) as r:
                if r.status != 200:
                    return "refused", None
                obj = json.loads(r.read().decode("utf-8", "replace"))
            if obj is None:
                return "null_body", None
            if not isinstance(obj, dict):
                return "not_json", None
            p = obj.get("parent")
            return ("ok", str(p)) if p is not None else ("ok_no_parent", None)
        except Exception:
            if attempt + 1 == TRIES:
                return "failed", None
            time.sleep(0.4 * (attempt + 1))
    return "failed", None


def climb(node, sid, parent):
    """Edges from `node` up to its story, which *is* the comment's depth.

    `node` is the need comment's own parent, so a parent that is the story
    gives 0 and each further reply adds one. Returns None when the chain cannot
    be closed -- an ancestor's parent is not known yet, or the chain hit a
    self-reference -- and the caller leaves those rows `null` rather than
    guessing, because `null` drops a row from the strata while a wrong 0 puts it
    in the stratum with the highest reply rate.
    """
    hops = 0
    seen = set()
    while node != sid:
        if node in seen or hops >= HARD_CAP:
            return None
        seen.add(node)
        up = parent.get(node)
        if up is None:
            return None
        node = str(up)
        hops += 1
    return hops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    need = {str(r["comment_id"]): r for r in
            (json.loads(l) for l in open(OUTCOMES))}
    par = {str(r["comment_id"]): r for r in
           (json.loads(l) for l in open(PARENTS))}
    prev = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            rec = json.loads(line)
            prev[str(rec["comment_id"])] = rec

    if args.verify:
        return verify(need, prev)

    depth = {c: r["depth"] for c, r in prev.items() if r.get("depth") is not None}
    # Known parent links: from the local capture, plus everything this run learns.
    parent = {}
    for cid, r in par.items():
        if r.get("parent") is not None:
            parent[str(cid)] = str(r["parent"])
    fetched_at = {}
    if os.path.exists(FETCHLOG):
        for line in open(FETCHLOG):
            rec = json.loads(line)
            fetched_at[str(rec["id"])] = rec
            if rec.get("parent"):
                parent.setdefault(str(rec["id"]), str(rec["parent"]))

    unresolved = sorted((c for c in need if c not in depth), key=int)
    sys.stderr.write("carrying %d resolved, walking %d unresolved\n"
                     % (len(depth), len(unresolved)))

    # work: list of (node, story, hops, waiting_comments)
    work = []
    for cid in unresolved:
        p = parent.get(cid)
        sid = str((par.get(cid) or {}).get("story_id"))
        if p is None or not sid:
            continue
        work.append([p, sid, 1, [cid]])
    t0 = time.time()
    rounds = 0
    while work and rounds < HARD_CAP:
        rounds += 1
        need_fetch = sorted({n for n, _s, h, _w in work
                             if n not in parent and h < HARD_CAP})
        if need_fetch:
            sys.stderr.write("round %d: %d chains, %d ancestors to fetch\n"
                             % (rounds, len(work), len(need_fetch)))
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for pid, (st, p) in zip(need_fetch, pool.map(fetch_parent, need_fetch)):
                    rec = {"id": pid, "status": st, "parent": p}
                    fetched_at[pid] = rec
                    if p:
                        parent.setdefault(pid, str(p))
        else:
            sys.stderr.write("round %d: %d chains, no new ancestors\n"
                             % (rounds, len(work)))
        # Advance each chain: the node's own parent becomes the next node. The
        # first version of this loop re-appended the *same* node with a larger hop
        # count, so `node == sid` was never true for a chain longer than one hop,
        # and the run printed "no new ancestors" for 29 rounds and then gave up --
        # reading as 434 unreadable comments when all three sampled chains resolve
        # live at 4, 2 and 3 hops. `climb` now closes a chain outright, which is
        # the shape the test asserts.
        nxt = []
        for node, sid, hops, waiting in work:
            d = climb(node, sid, parent)
            if d is not None:
                for c in waiting:
                    depth[c] = d
                continue
            up = parent.get(node)
            if up is None or str(up) == str(node):
                continue                      # chain ends above the story
            nxt.append([str(up), sid, hops + 1, waiting])
        work = [w for w in nxt if w[2] < HARD_CAP]

    with open(OUT, "w") as f:
        for cid in sorted(need, key=int):
            f.write(json.dumps({
                "comment_id": cid,
                "story_id": str(need[cid].get("story_id")),
                "depth": depth.get(cid),
                "answered": need[cid].get("answered"),
                "trigger": need[cid].get("trigger"),
            }, sort_keys=True) + "\n")
    with open(FETCHLOG, "w") as f:
        for pid in sorted(fetched_at, key=lambda x: int(x)):
            f.write(json.dumps(fetched_at[pid], sort_keys=True) + "\n")

    vals = [d for d in depth.values() if d is not None]
    print("resolved %d of %d (%.1f%%) in %.0fs"
          % (len(vals), len(need), 100.0 * len(vals) / max(1, len(need)),
             time.time() - t0))
    print("depth distribution %s" % dict(sorted(Counter(vals).items())))
    print("ancestors fetched %d, statuses %s"
          % (len(fetched_at),
             dict(Counter(r["status"] for r in fetched_at.values()))))
    return 0


def verify(need, prev):
    unresolved = [c for c, v in prev.items() if v.get("depth") is None]
    dist = dict(sorted(Counter(v["depth"] for v in prev.values()
                               if v.get("depth") is not None).items()))
    print("need comments %d, with a depth %d (%.1f%%)"
          % (len(prev), len(prev) - len(unresolved),
             100.0 * (len(prev) - len(unresolved)) / max(1, len(prev))))
    print("depth null   %d" % len(unresolved))
    print("distribution %s" % dist)
    problems = []
    if len(prev) < len(need):
        problems.append("%d need comments absent" % (len(need) - len(prev)))
    # The gate: unresolved rows must be few enough that dropping them cannot
    # reweight the population. 10% is the line, asserted in
    # tests/test_need_depth_gate.py.
    if len(unresolved) > 0.10 * len(prev):
        problems.append("%d unresolved rows is more than 10%% of the population; "
                        "the depth strata would be biased" % len(unresolved))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

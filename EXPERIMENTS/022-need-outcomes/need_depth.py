#!/usr/bin/env python3
"""E022: resolve the true depth of every need comment.

The first control was structurally top-level while most of the 1401 need comments
are replies to another comment. Depth drives reply probability -- 0.672 at depth
0 against 0.544 at depth 1 in the 12-story pilot -- so a pooled lift confounds
"carries a need trigger" with "sits near the top of a thread". Without this the
headline number would be reporting depth rather than need.

`corpus_authors.jsonl` records each need comment's `parent`, so depth 0 is
decidable locally with no request. Deeper comments need their ancestor chain
walked, and ancestors are shared, so memoising turns hundreds of nested comments
into a few hundred distinct fetches.

Two things this had to get right, both found by watching it fail:

  * **An ancestor's story must be inherited, not looked up.** The Firebase item
    record has no `story_id` field, so an ancestor fetched on its own has nothing
    to terminate the walk against and the chain runs to MAX_DEPTH. Every ancestor
    reached from a need comment belongs to that comment's story.
  * **An unreadable ancestor yields `null`, never 0.** Placing an unresolved
    comment at depth 0 would move it into the stratum with the highest reply
    rate, which is the direction that manufactures a result.
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
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
WORKERS = 12
TRIES = 3
MAX_DEPTH = 20


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    need = {str(r["comment_id"]): r for r in
            (json.loads(l) for l in open(OUTCOMES))}
    par = {str(r["comment_id"]): r for r in
           (json.loads(l) for l in open(PARENTS))}

    if args.verify:
        return verify(need)

    os.makedirs(RAW, exist_ok=True)

    story = {}    # id -> story it belongs to (inherited down the chain)
    parent = {}   # id -> parent id
    depth = {}    # id -> int or None

    for cid, r in par.items():
        sid = str(r.get("story_id"))
        p = r.get("parent")
        story[cid] = sid
        if p is None:
            depth[cid] = None
            continue
        parent[cid] = str(p)
        if str(p) == sid:
            depth[cid] = 0

    unresolved = set(cid for cid in need if cid not in depth)
    sys.stderr.write("depth 0 decided locally: %d; to walk: %d\n"
                     % (sum(1 for v in depth.values() if v == 0), len(unresolved)))

    t0 = time.time()
    for rnd in range(1, MAX_DEPTH + 1):
        if not unresolved:
            break
        progressed = False
        for cid in list(unresolved):
            p = parent.get(cid)
            if p is not None and p in depth:
                depth[cid] = depth[p] + 1
                unresolved.discard(cid)
                progressed = True
        if progressed:
            continue

        # Fetch unknown ancestors, inheriting the story of the comment that
        # referenced them -- this is what terminates the walk.
        wanted = {}   # ancestor id -> story
        for cid in unresolved:
            p = parent.get(cid)
            if p is not None and p not in depth:
                wanted.setdefault(p, story.get(cid))
        if not wanted:
            for cid in list(unresolved):
                depth[cid] = None
            break
        ids = sorted(wanted, key=int)
        sys.stderr.write("round %d: %d unresolved, fetching %d ancestors\n"
                         % (rnd, len(unresolved), len(ids)))
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            for aid, (st, p) in zip(ids, pool.map(fetch_parent, ids)):
                story[aid] = wanted[aid]
                if st.startswith("ok") and p is not None:
                    parent[aid] = p
                    if p == wanted[aid]:
                        depth[aid] = 0
        if not any(a in depth for a in ids):
            # Nothing this round was anchorable; anything left is unreadable.
            for cid in list(unresolved):
                depth[cid] = None
            break

    with open(OUT, "w") as f:
        for cid in sorted(need, key=int):
            f.write(json.dumps({
                "comment_id": cid,
                "story_id": str(need[cid].get("story_id")),
                "depth": depth.get(cid),
                "answered": need[cid].get("answered"),
                "trigger": need[cid].get("trigger"),
            }, sort_keys=True) + "\n")

    resolved = [v for v in depth.values() if v is not None]
    print("need comments %d, depth resolved %d (%.1f%%) in %.0fs"
          % (len(need), len(resolved), 100.0 * len(resolved) / max(1, len(need)),
             time.time() - t0))
    print("depth distribution %s" % dict(sorted(Counter(resolved).items())))
    return 0


def verify(need):
    if not os.path.exists(OUT):
        print("no depth capture")
        return 1
    got = {}
    for line in open(OUT):
        rec = json.loads(line)
        got[str(rec["comment_id"])] = rec
    missing = [c for c in need if c not in got]
    unresolved = [k for k, v in got.items() if v.get("depth") is None]
    print("need comments    %d" % len(need))
    print("with a depth     %d" % (len(got) - len(unresolved)))
    print("absent           %d" % len(missing))
    print("depth null       %d" % len(unresolved))
    print("distribution     %s"
          % dict(sorted(Counter(v["depth"] for v in got.values()
                                if v.get("depth") is not None).items())))
    problems = []
    if missing:
        problems.append("%d need comments have no depth row" % len(missing))
    if unresolved:
        problems.append("%d rows have depth null" % len(unresolved))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

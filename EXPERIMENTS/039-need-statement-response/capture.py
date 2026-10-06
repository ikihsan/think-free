#!/usr/bin/env python3
"""E039 capture: every comment row of every story the need corpus sits in.

One row per comment: objectID, parent_id, author, created_at_i and the comment
text, taken from the public Algolia search index in the same request that
supplies the row. The `items` endpoint was tried first and rejected: its subtree
for a need undercounts by up to 2 (calibration.py, 2 of 12 rows), and its per-id
cost would have been one request per comment across ~350k comments.

From the parent_id edges the reply subtree of each need comment is reconstructed
exactly, and every other comment in the same stories becomes the matched control.

Paced, resumable, append-only. A refused answer is recorded as a failure row and
is never counted as an absent reply. Workers are threads because the cost is
network wait, not CPU: a serial run took 4 minutes for 14 of 1276 stories, which
is 6 hours for the ledger.
"""
import json, os, sys, time, threading, queue, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = {"User-Agent": "think-free-research"}
SEARCH = "https://hn.algolia.com/api/v1/search"
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"

# The public index serves pages up to 1000 hits and then returns empty, so a
# larger story is captured only to that ceiling and the truncation is written
# down rather than passed off as a complete thread.
PAGE_CAP_HITS = 1000
WORKERS = 8
PAGE_SLEEP = 0.12
STORY_SLEEP = 0.0


def get(url, tries=4):
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=90) as r:
                return json.load(r), None
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            last = repr(exc)[:200]
            time.sleep(2 * (attempt + 1))
    return None, last


def story_rows(story_id):
    """All comment rows for one story, plus a record of what was not obtainable."""
    sid = str(story_id)
    rows, pages, total, log = [], 0, None, []
    while len(rows) < PAGE_CAP_HITS:
        p = {"tags": "comment,story_%s" % sid, "hitsPerPage": "100",
             "page": str(pages)}
        d, err = get(SEARCH + "?" + urllib.parse.urlencode(p))
        if d is None:
            log.append({"kind": "fetch_failed", "story_id": sid, "page": pages,
                        "error": err, "rows_so_far": len(rows)})
            return rows, log
        hits = d.get("hits") or []
        if total is None:
            total = d.get("nbHits")
        if not hits:
            if pages == 0:
                probe, perr = get(FIREBASE % sid)
                kind = "story_id_is_comment" if (probe and probe.get("type") == "comment") \
                    else "empty_story"
                log.append({"kind": kind, "story_id": sid,
                            "firebase_type": (probe or {}).get("type"),
                            "firebase_descendants": (probe or {}).get("descendants"),
                            "error": perr, "rows_so_far": 0})
            break
        for h in hits:
            rows.append({
                "id": str(h.get("objectID")),
                "parent_id": str(h.get("parent_id")) if h.get("parent_id") is not None else None,
                "author": h.get("author"),
                "created_at_i": h.get("created_at_i"),
                "story_id": sid,
                "text": h.get("comment_text") or "",
            })
        pages += 1
        time.sleep(PAGE_SLEEP)
    if total is not None and total > len(rows):
        log.append({"kind": "truncated", "story_id": sid, "nbHits": total,
                    "captured": len(rows), "cap": PAGE_CAP_HITS})
    return rows, log


def worker(q, wid, lock, state):
    out = os.path.join(RAW, "shard-%02d.jsonl" % wid)
    logf = os.path.join(RAW, "log-%02d.jsonl" % wid)
    with open(out, "a") as cf, open(logf, "a") as lf:
        while True:
            try:
                sid = q.get_nowait()
            except queue.Empty:
                return
            rows, log = story_rows(sid)
            for r in rows:
                cf.write(json.dumps(r, sort_keys=True) + "\n")
            for e in log:
                lf.write(json.dumps(e, sort_keys=True) + "\n")
            cf.flush()
            lf.flush()
            with lock:
                state["done"].add(sid)
                state["rows"] += len(rows)
                with open(os.path.join(RAW, "stories.done"), "a") as df:
                    df.write(sid + "\n")
                n = len(state["done"])
                if n % 100 == 0:
                    print("stories %d/%d rows=%d" % (n, state["total"], state["rows"]),
                          flush=True)
            time.sleep(STORY_SLEEP)


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    needs = [json.loads(l) for l in open(corpus)]
    story_ids, seen = [], set()
    for r in needs:
        if str(r["story_id"]) not in seen:
            seen.add(str(r["story_id"]))
            story_ids.append(str(r["story_id"]))

    os.makedirs(RAW, exist_ok=True)
    done_path = os.path.join(RAW, "stories.done")
    done = set()
    if os.path.exists(done_path):
        done = {l.strip() for l in open(done_path) if l.strip()}

    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    else:
        limit = len(story_ids)
    todo = [s for s in story_ids if s not in done][:limit]
    print("todo %d of %d stories (%d already done)" % (len(todo), len(story_ids), len(done)),
          flush=True)

    q = queue.Queue()
    for s in todo:
        q.put(s)
    lock = threading.Lock()
    state = {"done": set(), "rows": 0, "total": len(todo)}
    threads = [threading.Thread(target=worker, args=(q, i, lock, state), daemon=True)
               for i in range(WORKERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("capture complete: %d stories this run, %d rows" % (len(state["done"]), state["rows"]))


if __name__ == "__main__":
    main()
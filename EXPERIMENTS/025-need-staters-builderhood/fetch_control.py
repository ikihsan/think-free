#!/usr/bin/env python3
"""E025 -- the control arm, streamed.

Written after the original fetcher proved the wrong shape: it resolved all 13409
control comments before probing a single one, which costs far more than the gate
needs and produces no figure until the end.

PROTOCOL.md's stopping rule, declared before any control-arm count existed: stop
at the first of 500 probed control authors or an exhausted capture. Control
authors are taken in the capture's own order, deduplicated.

Raw captures are append-only and a capture holding an answer is never overwritten.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
CONTROL = os.path.join(
    os.path.dirname(ROOT), "022-need-outcomes", "raw", "control.jsonl"
)

STOP_AT = 500  # PROTOCOL.md stopping rule
BASE = "https://hn.algolia.com/api/v1/search"
UA = "think-free-e025/1.0 (research instrument; stdlib urllib)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8", "replace")), "ok"
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(2 * (attempt + 1))
                continue
            return None, "http_%d" % e.code
        except Exception as e:
            if attempt == 2:
                return None, "error_%s" % type(e).__name__
            time.sleep(1.5)
    return None, "rate_limited"


def append(path, row):
    with open(path, "a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def load_done(path):
    done = {}
    if not os.path.exists(path):
        return done
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            done[d["author"]] = d
    return done


def probe(author, out_path):
    url = "%s?tags=author_%s,show_hn&hitsPerPage=1" % (BASE, urllib.parse.quote(author))
    doc, status = get(url)
    row = {
        "arm": "control",
        "author": author,
        "status": status,
        "nb_show_hn": doc.get("nbHits") if (status == "ok" and isinstance(doc, dict)) else None,
        "total_items_by_author": None,
    }
    append(out_path, row)
    return row


def resolve_authors(limit_comments):
    """comment_id -> author, one item fetch each, in the capture's own order."""
    path = os.path.join(RAW, "control_authors.jsonl")
    done = load_done(path)
    cids = []
    with open(CONTROL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("status") == "ok" and d.get("comment_id"):
                cids.append(str(d["comment_id"]))
    cids = sorted(set(cids))
    # ~1.02 authors per comment in this capture, so oversample requests slightly
    # above the stop target rather than discovering the shortfall at the end.
    need = min(len(cids), int(limit_comments * 1.15))
    for cid in cids[:need]:
        if cid in done and done[cid].get("author"):
            continue
        doc, status = get("https://hn.algolia.com/api/v1/items/%s" % cid)
        author = doc.get("author") if (status == "ok" and isinstance(doc, dict)) else None
        append(path, {"comment_id": cid, "author": author, "status": status})
        time.sleep(0.1)
    authors = []
    seen = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            a = d.get("author")
            if a and a not in seen:
                seen.add(a)
                authors.append(a)  # capture order is cids sorted ascending
    return authors


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    out_path = os.path.join(RAW, "control_arm.jsonl")

    authors = resolve_authors(STOP_AT + 120)
    print("resolved %d distinct control authors" % len(authors))

    done = load_done(out_path)
    probed = 0
    for a in authors:
        if probed >= STOP_AT:
            break
        if a in done and done[a].get("status") == "ok":
            probed += 1
            continue
        probe(a, out_path)
        probed += 1
        if probed % 100 == 0:
            print("  control probed %d" % probed)
        time.sleep(0.12)

    # The confounder, reported not corrected: total HN footprint, sampled.
    rows = load_done(out_path)
    for a in list(rows)[:40]:
        if rows[a].get("total_items_by_author") is not None:
            continue
        doc, status = get("%s?tags=author_%s&hitsPerPage=0" % (BASE, urllib.parse.quote(a)))
        if status == "ok" and isinstance(doc, dict):
            append(out_path, {"arm": "control", "author": a, "status": "ok",
                              "nb_show_hn": rows[a].get("nb_show_hn"),
                              "total_items_by_author": doc.get("nbHits")})
    print("control arm complete: %d probed (stop rule: %d)" % (probed, STOP_AT))


if __name__ == "__main__":
    main()

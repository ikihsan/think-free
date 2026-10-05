#!/usr/bin/env python3
"""E025 -- fetch the show_hn tag for the need arm and the control arm.

Protocol: EXPERIMENTS/025-need-staters-builderhood/PROTOCOL.md (written before
the first fetch).

One request per author to the Hacker News Algolia index, asking for items
carrying both the author and the ``show_hn`` tag. The tag is assigned by HN, not
by the author, so this is a floor on disclosure and the protocol says so.

Raw captures are append-only. A capture holding an answer is never overwritten,
which is the repair recorded for the copy-count instrument (F041 defect 1).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")

CORPUS = os.path.join(
    os.path.dirname(ROOT), "019-corpus-person-diversity", "raw", "corpus_authors.jsonl"
)
CONTROL = os.path.join(
    os.path.dirname(ROOT), "022-need-outcomes", "raw", "control.jsonl"
)

# Named in PROTOCOL.md Gate A1. The first four were believed positive by
# assertion; two of them were not, and that is a recorded instrument defect (see
# PROTOCOL.md's Gate A1 correction and README.md). The originals stay in the
# capture with their 0s. These six were sampled from the show_hn tag itself, so
# each is verified positive by the same evidence the gate tests.
POSITIVE_CONTROLS_ORIGINAL = ["pg", "patio11", "chromium", "antirez"]
POSITIVE_CONTROLS = [
    "olalonde",     # Show HN: This up votes itself
    "keepamovin",   # Show HN: Gemini Pro 3 imagines the HN front page
    "byran",        # Show HN: I made an open-source laptop from scratch
    "jart",         # Show HN: Redbean -- single-file distributable web server
    "mikemcquaid",  # Show HN: Homebrew 6.0.0
    "erohead",      # Show HN: Beeper Mini -- iMessage client for Android
]
NONSENSE_CONTROL = "zzqqxxnonsensecontrol"

BASE = "https://hn.algolia.com/api/v1/search"
UA = "think-free-e025/1.0 (research instrument; stdlib urllib)"


def get(url):
    """Return (parsed_json_or_None, status_str). A refusal is never an absence."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
                return json.loads(body), "ok"
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(2 * (attempt + 1))
                continue
            return None, "http_%d" % e.code
        except Exception as e:  # network, timeout, malformed JSON
            if attempt == 2:
                return None, "error_%s" % type(e).__name__
            time.sleep(1.5)
    return None, "rate_limited"


def append(path, row):
    with open(path, "a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def load_done(path):
    """Author -> capture already on disk. Never refetched."""
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


def probe(arm, author, out_path):
    """Fetch one author. Records nbHits, which is the count that answers the gate."""
    url = "%s?tags=author_%s,show_hn&hitsPerPage=1" % (BASE, urllib.parse.quote(author))
    doc, status = get(url)
    if status != "ok" or not isinstance(doc, dict):
        row = {"arm": arm, "author": author, "status": status, "nb_show_hn": None}
    else:
        row = {
            "arm": arm,
            "author": author,
            "status": "ok",
            "nb_show_hn": doc.get("nbHits"),
            "total_items_by_author": None,
        }
    append(out_path, row)
    return row


def total_items(author):
    """An author's total HN footprint. Used only to report the confounder."""
    url = "%s?tags=author_%s&hitsPerPage=0" % (BASE, urllib.parse.quote(author))
    doc, status = get(url)
    if status == "ok" and isinstance(doc, dict):
        return doc.get("nbHits")
    return None


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)

    # ---- Gate A1 controls, fetched first and in order, before either arm. ----
    ctrl_path = os.path.join(RAW, "gate_a1_controls.jsonl")
    done = load_done(ctrl_path)
    for a in POSITIVE_CONTROLS_ORIGINAL + POSITIVE_CONTROLS + [NONSENSE_CONTROL]:
        if a in done:
            print("control cached: %s -> %s" % (a, done[a].get("nb_show_hn")))
            continue
        r = probe("gate_a1", a, ctrl_path)
        print("control %-28s -> nb_show_hn=%s (%s)" % (a, r.get("nb_show_hn"), r["status"]))
        time.sleep(0.35)
    print("gate A1 controls complete")

    # ---- need arm: every distinct author in E019's capture. ----
    need = []
    seen = set()
    with open(CORPUS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            a = d.get("author")
            if a and a not in seen:
                seen.add(a)
                need.append(a)
    need.sort()
    print("need arm: %d distinct authors" % len(need))

    need_path = os.path.join(RAW, "need_arm.jsonl")
    done = load_done(need_path)
    for i, a in enumerate(need):
        if a in done and done[a].get("status") == "ok":
            continue
        r = probe("need", a, need_path)
        if (i + 1) % 100 == 0:
            print("  need %d/%d" % (i + 1, len(need)))
        time.sleep(0.12)
    print("need arm complete")

    # ---- control arm: authors of E022's control comments. These carry no author
    # field (they are comment ids), so each author's name is fetched from HN. ----
    ctl_path = os.path.join(RAW, "control_authors.jsonl")
    out_path = os.path.join(RAW, "control_arm.jsonl")
    done = load_done(out_path)
    if not done:
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
        print("control arm: %d control comments to resolve" % len(cids))

        # Resolve comment_id -> author with one item fetch each, batched politely.
        for i, cid in enumerate(cids):
            if os.path.exists(ctl_path):
                d2 = load_done(ctl_path)
            else:
                d2 = {}
            if cid in d2:
                continue
            url = "https://hn.algolia.com/api/v1/items/%s" % cid
            doc, status = get(url)
            author = None
            if status == "ok" and isinstance(doc, dict):
                author = doc.get("author")
            append(ctl_path, {"comment_id": cid, "author": author, "status": status})
            if (i + 1) % 200 == 0:
                print("  control authors %d/%d" % (i + 1, len(cids)))
            time.sleep(0.1)

        ctl_authors = set()
        with open(ctl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                if d.get("author"):
                    ctl_authors.add(d["author"])
        ctl_authors = sorted(ctl_authors)
        print("control arm: %d distinct authors" % len(ctl_authors))

        for i, a in enumerate(ctl_authors):
            if a in done and done[a].get("status") == "ok":
                continue
            probe("control", a, out_path)
            if (i + 1) % 100 == 0:
                print("  control %d/%d" % (i + 1, len(ctl_authors)))
            time.sleep(0.12)
    print("control arm complete")

    # ---- the confounder, reported not corrected: how big is each author's
    # overall HN footprint. A show_hn rate that tracks total items is HN's
    # selection, not builderhood.
    for arm, path in (("need", need_path), ("control", out_path)):
        if not os.path.exists(path):
            continue
        rows = load_done(path)
        want = [a for a, r in rows.items() if r.get("total_items_by_author") is None]
        for a in want[:40]:
            r = rows[a]
            r["total_items_by_author"] = total_items(a)
            append(path, r)
    print("footprint sample recorded")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E029 -- fetch what each need-stater shipped, and the thread they asked in.

Protocol: EXPERIMENTS/029-need-build-match/PROTOCOL.md.

Two requests per eligible builder, both against the Hacker News Algolia index:

  1. tags=author_X,show_hn   -- the items they shipped, title and url
  2. items/<story_id>        -- the title of the story the need was posted in,
                                which is the control arm that can kill H1

The comma form is the intersection. Repeated `tags=` parameters are OR-ed by this
API, which turns an intersection into a union of ~59 items per author instead of 1;
that is recorded in the README as a trap, not as a defect of an earlier run.

Captures are append-only and a capture holding an answer is never overwritten
(F041 defect 1). A refusal is written beside the answer, never in place of it.
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
POPULATION = os.path.join(RAW, "population.jsonl")
BUILDS = os.path.join(RAW, "builds.jsonl")
STORIES = os.path.join(RAW, "stories.jsonl")
CONTROLS = os.path.join(RAW, "gate_a2_controls.jsonl")

# Gate A2. E025's corrected set, sampled from the show_hn tag itself, so each is
# verified positive by the same evidence the gate tests (F036's lesson). The two
# E025 found were not positive stay named in its README; they are not reused.
POSITIVE_CONTROLS = ["olalonde", "keepamovin", "byran", "jart", "mikemcquaid", "erohead"]
NONSENSE_CONTROL = "zzqqxxnonsensecontrol"

BASE = "https://hn.algolia.com/api/v1"
UA = "think-free-e029/1.0 (research instrument; stdlib urllib)"


def get(url):
    """Return (parsed_json_or_None, status_str). A refusal is never an absence."""
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


def load_done(path, key):
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
            if key in d:
                done[d[key]] = d
    return done


def fetch_builds(author):
    url = "%s/search?tags=author_%s,show_hn&hitsPerPage=100" % (
        BASE, urllib.parse.quote(author))
    doc, status = get(url)
    if status != "ok" or not isinstance(doc, dict):
        return None, status
    hits = []
    for h in doc.get("hits") or []:
        if "show_hn" not in (h.get("_tags") or []):
            continue          # the tag filter is re-checked on the answer
        hits.append({"id": str(h.get("objectID")), "title": h.get("title"),
                     "url": h.get("url")})
    return {"nb_show_hn": doc.get("nbHits"), "items": hits}, "ok"


def fetch_story(story_id):
    doc, status = get("%s/items/%s" % (BASE, urllib.parse.quote(story_id)))
    if status != "ok" or not isinstance(doc, dict):
        return None, status
    return {"title": doc.get("title"), "url": doc.get("url")}, "ok"


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)

    # ---- Gate A2 first, in order, before any arm row. ----
    done = load_done(CONTROLS, "account")
    for a in POSITIVE_CONTROLS + [NONSENSE_CONTROL]:
        if a in done:
            print("control cached: %-26s -> %s" % (a, done[a].get("n_items")))
            continue
        payload, status = fetch_builds(a)
        n = None if payload is None else len(payload["items"])
        append(CONTROLS, {"account": a, "status": status, "n_items": n,
                          "expectation": "positive" if a in POSITIVE_CONTROLS else "nonsense"})
        print("control %-26s -> n=%s (%s)" % (a, n, status))
        time.sleep(0.3)
    print("gate A2 controls complete")

    rows = [json.loads(l) for l in open(POPULATION) if l.strip()]

    done_b = load_done(BUILDS, "author")
    done_s = load_done(STORIES, "story_id")
    for i, r in enumerate(rows):
        a = r["author"]
        if a not in done_b:
            payload, status = fetch_builds(a)
            if payload is None:
                append(BUILDS, {"author": a, "status": status, "n_items": None,
                                "nb_show_hn": None, "items": []})
            else:
                append(BUILDS, {"author": a, "status": status,
                                "n_items": len(payload["items"]),
                                "nb_show_hn": payload["nb_show_hn"],
                                "items": payload["items"]})
            time.sleep(0.12)
        sid = r["need"]["story_id"]
        if sid not in done_s:
            payload, status = fetch_story(sid)
            if payload is None:
                append(STORIES, {"story_id": sid, "status": status,
                                 "title": None, "url": None})
            else:
                append(STORIES, {"story_id": sid, "status": status,
                                 "title": payload["title"], "url": payload["url"]})
            time.sleep(0.1)
        if (i + 1) % 50 == 0:
            print("  %d/%d" % (i + 1, len(rows)))
    print("fetch complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())

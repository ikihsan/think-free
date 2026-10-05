#!/usr/bin/env python3
"""E022: build the sample that a human labels for `served`.

`answered` is cheap and nearly worthless on its own: a comment can receive three
replies that all ignore it. F036 recorded a web instrument answering HTTP 200
with ten well-formed results for each of 38 queries, every one unrelated to its
query -- nothing inside such a capture distinguishes it from a real one. The same
shape applies to a reply count.

So the cell that carries meaning is `served`: **a reply that names an artifact
which actually serves what was asked.** That is a judgement, so it is labelled by
hand, on a sample drawn by a rule stated in the protocol rather than chosen by
taste.

This module only *draws and presents* the sample. It does not label. Writing a
label is a human act and belongs in `raw/labels.tsv`, which carries the label and
nothing else. A row with no label reads as `unlabelled`, never as `not served`.

The automatic lexical rule is computed alongside, because its agreement with the
labels is itself worth having: an over-inclusive rule that agrees on nearly
everything tells us the labels are doing no work, and one that disagrees tells
us where the judgement lives.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = os.path.join(HERE, "raw", "outcomes.jsonl")
NEEDS = os.path.join(HERE, "..", "012-candidate-harvest",
                     "raw", "hn_needs_2026-10-04.jsonl")
RAW = os.path.join(HERE, "raw")
SAMPLE = os.path.join(RAW, "serve_sample.tsv")
LABELS = os.path.join(RAW, "labels.tsv")
ALGOLIA_ITEM = "https://hn.algolia.com/api/v1/items/%s"
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"

SAMPLE_N = 40          # declared in PROTOCOL.md before observing
SEED = 20261005        # fixed so the sample is reproducible

# Over-inclusive on purpose: this is a floor on "did anyone point at a thing",
# not the served cell. Backticked spans, bare URLs, and hyphenated proper nouns.
ARTIFACTISH = re.compile(
    r"(https?://[^\s<>]+|`[^`]{2,40}`|\b(?:[A-Z][a-z0-9]+){1,}[A-Za-z0-9_+.-]*\b)")
TAG = re.compile(r"<[^>]+>")


def html_to_text(t):
    t = TAG.sub(" ", t or "")
    t = (t.replace("&#x27;", "'").replace("&#39;", "'")
          .replace("&quot;", '"').replace("&gt;", ">")
          .replace("&lt;", "<").replace("&amp;", "&")
          .replace("&gt;", ">"))
    return re.sub(r"\s+", " ", t).strip()


def fetch(url, timeout=25):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(0.4)
    return None, ""



def choose_sample():
    """A fixed rule: among comments that received a reply, take the first
    SAMPLE_N by a seeded shuffle. Restricting to answered comments is deliberate
    -- `served` is conditional on there being a reply at all, and sampling the
    unanswered would label rows that cannot be served by anything."""
    rows = [json.loads(l) for l in open(OUTCOMES)]
    answered = [r for r in rows if r["answered"]]
    import random
    rng = random.Random(SEED)
    idx = list(range(len(answered)))
    rng.shuffle(idx)
    picked = [answered[i] for i in idx[:SAMPLE_N]]
    return answered, picked


def replies_for(cid):
    """Depth-1 replies with their text, via Algolia's tree endpoint."""
    st, body = fetch(ALGOLIA_ITEM % cid)
    if st != 200:
        return None, []
    try:
        obj = json.loads(body)
    except ValueError:
        return None, []
    kids = obj.get("children") or []
    out = []
    for c in kids[:6]:
        out.append({
            "author": c.get("author"),
            "text": html_to_text(c.get("text"))[:400],
        })
    return obj, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    answered, picked = choose_sample()
    if args.verify:
        return verify(picked)

    os.makedirs(RAW, exist_ok=True)
    text_of = {}
    with open(os.path.join(HERE, "..", "012-candidate-harvest",
                           "raw", "hn_needs_2026-10-04.jsonl")) as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                text_of[str(rec["id"])] = rec

    rows = []
    for n, r in enumerate(picked, 1):
        cid = str(r["comment_id"])
        src = text_of.get(cid, {})
        obj, replies = replies_for(cid)
        if obj is None:
            rows.append({"comment_id": cid, "status": "unreadable", "replies": 0,
                         "lex_hits": 0, "need": src.get("text", "")[:600],
                         "reply_texts": []})
        else:
            joined = " ".join(x["text"] for x in replies)
            rows.append({
                "comment_id": cid,
                "status": "ok",
                "author": src.get("id"),
                "story": src.get("story"),
                "trigger": r.get("trigger"),
                "need": src.get("text", "")[:600],
                "n_replies_seen": len(replies),
                "lex_hits": len(ARTIFACTISH.findall(joined)),
                "reply_texts": [x["text"] for x in replies],
            })
        if n % 10 == 0:
            sys.stderr.write("%d/%d\n" % (n, len(picked)))

    with open(SAMPLE, "w") as f:
        f.write("comment_id\ttrigger\tlex_hits\tn_replies_seen\tneed\treplies\n")
        for r in rows:
            f.write("\t".join([
                r["comment_id"],
                (r.get("trigger") or "").replace("\t", " "),
                str(r.get("lex_hits")),
                str(r.get("n_replies_seen", 0)),
                (r.get("need") or "").replace("\t", " ").replace("\n", " ")[:600],
                (" ||| ".join(r.get("reply_texts") or [])).replace("\t", " ")[:900],
            ]) + "\n")

    unreadable = sum(1 for r in rows if r["status"] != "ok")
    print("answered comments in population %d" % len(answered))
    print("sample drawn %d (seed %d), unreadable %d" % (len(rows), SEED, unreadable))
    print("lexical rule fires on %d of %d"
          % (sum(1 for r in rows if r.get("lex_hits")), len(rows)))
    print("labels file: %s (empty until a human writes it)"
          % os.path.relpath(LABELS, HERE))
    return 0


def verify(picked):
    """The gate reads the artifact. A sample with no labels reports unlabelled."""
    if not os.path.exists(SAMPLE):
        print("no sample at %s" % SAMPLE)
        return 1
    with open(SAMPLE) as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    problems = []
    if len(rows) < SAMPLE_N:
        problems.append("sample holds %d rows, fewer than the declared %d"
                        % (len(rows), SAMPLE_N))
    labelled = {}
    if os.path.exists(LABELS):
        with open(LABELS) as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[1]:
                    labelled[parts[0]] = parts[1]
    print("sample rows     %d" % len(rows))
    print("declared n      %d" % SAMPLE_N)
    print("labelled        %d" % len(labelled))
    print("unlabelled      %d" % (len(rows) - len(labelled)))
    if labelled:
        served = sum(1 for v in labelled.values() if v == "served")
        print("labelled served %d of %d (%.0f%%)"
              % (served, len(labelled), 100.0 * served / len(labelled)))
    for p in problems:
        print("PROBLEM: %s" % p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

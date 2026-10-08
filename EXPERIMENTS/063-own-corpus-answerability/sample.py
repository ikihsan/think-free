#!/usr/bin/env python3
"""Build E063's labelled queue from the two need corpora already on disk.

Deterministic stride sampling, no screening: every row in the stride is put in the
queue, including the ones that look hopeless. Writes

  raw/sample-armA.tsv   70 Hacker News need statements   (every 20th of 1401)
  raw/sample-armB.tsv   31 GitHub issues                 (every  6th of 189)
  raw/controls.tsv      20 seeded needs, blind, same format
  raw/control-key.json  answer key, not read until the queue is labelled
  raw/queue.tsv         arms A and B plus the controls, interleaved and blind

Stdlib only. Run from this directory.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "raw")
HN = os.path.join(REPO, "EXPERIMENTS/012-candidate-harvest/raw/"
                         "hn_needs_2026-10-04.jsonl")
GH = os.path.join(REPO, "EXPERIMENTS/045-demand-evidence/raw/issues.jsonl")

TEXT_CAP = 700


def rows(path):
    with open(path) as fh:
        return [json.loads(line) for line in fh]


def flatten(text):
    return " ".join(str(text).split())[:TEXT_CAP]


def write_tsv(name, header, records):
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    path = os.path.join(RAW, name)
    with open(path, "w") as fh:
        fh.write("\t".join(header) + "\n")
        for rec in records:
            fh.write("\t".join(str(rec.get(col, "")).replace("\t", " ")
                               for col in header) + "\n")
    return path, len(records)


# --- arm A: Hacker News need statements -------------------------------------
hn = rows(HN)
arm_a = []
for i in range(0, len(hn), 20):
    r = hn[i]
    arm_a.append({
        "arm": "A",
        "row": i,
        "trigger": r["trigger"],
        "story": flatten(r["story"])[:160],
        "text": flatten(r["text"]),
    })

# --- arm B: GitHub issues behind the stg demand claim ----------------------
gh = rows(GH)
arm_b = []
for i in range(0, len(gh), 6):
    r = gh[i]
    arm_b.append({
        "arm": "B",
        "row": i,
        "trigger": "issue",
        "story": "%s#%s (%s, %s comments, %s)" % (
            r["repo"], r["number"], r["state"], r["comments"],
            r["created_at"][:10]),
        "text": flatten((r.get("title") or "") + " || " + (r.get("lead") or "")),
    })

# --- arm C: seeded controls, blind ------------------------------------------
# 10 must be labelled served, 10 must not be. The mix is interleaved so the
# labeller cannot tell which is which from position.
CONTROLS = [
    ("served", "I wish there was a tool that converts a JSON array of ISO-8601 "
     "timestamps to a single UTC-normalised CSV with one column per day."),
    ("unserved", "I wish there was a tool that tells me whether the drum bearing "
     "on my 2013 Bosch washing machine is worn, from the noise it makes."),
    ("served", "I wish there was a tool that renames every photo in a folder to "
     "its EXIF DateTimeOriginal, numbered per day."),
    ("unserved", "I wish there was a tool that finds out who has been using my "
     "work laptop at home and what they did, from last month's logs."),
    ("served", "I wish there was a tool that diffs two SQL schemas and emits the "
     "ALTER TABLE statements to migrate one to the other."),
    ("unserved", "I wish there was a tool that can tell me which of these 300 "
     "second-hand bikes in the classifieds is stolen, from the serial numbers."),
    ("served", "I wish there was a tool that extracts every table from a PDF "
     "annual report into clean CSV with the page numbers kept."),
    ("unserved", "I wish there was a tool that decides my tax return for the "
     "2023 tax year for a freelancer in three countries with crypto income."),
    ("served", "I wish there was a tool that watches a directory for new .mp4 "
     "files and transcodes them to AV1 in the background."),
    ("unserved", "I wish there was a tool that tells me the structural condition "
     "of the house I am bidding on from the photographs the estate agent took."),
    ("served", "I wish there was a tool that turns a messy CSV of addresses into "
     "a geocoded list with the coordinates in a new column."),
    ("unserved", "I wish there was a tool that finds the recording of a 1994 "
     "local council planning meeting that mentioned my street, and names it."),
    ("served", "I wish there was a tool that takes a long YouTube URL list and "
     "writes an RSS feed of their metadata without downloading the video."),
    ("unserved", "I wish there was a tool that knows which of my mother's old "
     "knives are the good ones, from photographs of the blades."),
    ("served", "I wish there was a tool that checks a Kubernetes manifest against "
     "the cluster's actual admission webhooks and reports what would be rejected."),
    ("unserved", "I wish there was a tool that predicts my toddler's sleep "
     "schedule from her own last three weeks of handwritten logs."),
    ("served", "I wish there was a tool that finds every place in a git history "
     "where a function's behaviour changed, and writes the before/after examples."),
    ("unserved", "I wish there was a tool that works out why my car insurance "
     "renewal jumped 40% this year, from the insurer's own internal file."),
    ("served", "I wish there was a tool that turns a chess PGN file into a "
     "clickable board replay in a static HTML page."),
    ("unserved", "I wish there was a tool that finds my grandmother's will in a "
     "county record office that stopped publishing its index in 1998."),
]

controls = []
for n, (expect, text) in enumerate(CONTROLS):
    controls.append({"blind_id": "C%02d" % (n + 1), "expect": expect, "text": text})
# deterministic blind order: even slots served-ish mix, then a fixed rotation
order = [3, 0, 8, 5, 1, 11, 6, 9, 14, 2, 17, 7, 10, 13, 4, 16, 19, 12, 15, 18]
blinded = [controls[i] for i in order]

write_tsv("sample-armA.tsv", ["arm", "row", "trigger", "story", "text"], arm_a)
write_tsv("sample-armB.tsv", ["arm", "row", "trigger", "story", "text"], arm_b)
write_tsv("controls.tsv", ["blind_id", "text"], blinded)

with open(os.path.join(RAW, "control-key.json"), "w") as fh:
    json.dump({c["blind_id"]: c["expect"] for c in blinded}, fh, indent=1,
              sort_keys=True)

# --- the queue: arms A and B, controls interleaved deterministically ---------
queue = []
for rec in arm_a:
    queue.append({"blind_id": "A%03d" % rec["row"], "arm": "A", "text":
                  "[%s] %s || %s" % (rec["trigger"], rec["story"], rec["text"])})
for rec in arm_b:
    queue.append({"blind_id": "B%03d" % rec["row"], "arm": "B", "text":
                  "[issue] %s || %s" % (rec["story"], rec["text"])})
for rec in blinded:
    queue.append({"blind_id": rec["blind_id"], "arm": "C", "text": rec["text"]})

# interleave the 20 controls evenly through the 101 corpus rows
merged = []
ci = 0
step = len(queue) // (len(blinded) + 1)
for pos, rec in enumerate(queue):
    merged.append(rec)
    while ci < len(blinded) and (pos + 1) * (len(blinded) + 1) // len(queue) > ci:
        merged.append({"blind_id": blinded[ci]["blind_id"], "arm": "C",
                       "text": blinded[ci]["text"]})
        ci += 1
while ci < len(blinded):
    merged.append({"blind_id": blinded[ci]["blind_id"], "arm": "C",
                   "text": blinded[ci]["text"]})
    ci += 1

write_tsv("queue.tsv", ["blind_id", "arm", "text"], merged)
print("armA %d  armB %d  controls %d  queue %d  (stride %d)" % (
    len(arm_a), len(arm_b), len(blinded), len(merged), step))

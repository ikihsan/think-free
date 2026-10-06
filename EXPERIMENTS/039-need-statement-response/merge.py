#!/usr/bin/env python3
"""E039: merge the capture's per-worker shards into the two files the arms read.

Kept separate from capture.py so that a re-capture never has to re-derive
structure, and so the merge is one auditable step. Deduplicates on comment id:
a story re-fetched after an interruption contributes its rows once.
"""
import glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def main():
    seen = set()
    comments = []
    for path in sorted(glob.glob(os.path.join(RAW, "shard-*.jsonl"))):
        for line in open(path):
            d = json.loads(line)
            if d["id"] in seen:
                continue
            seen.add(d["id"])
            comments.append(d)
    comments.sort(key=lambda r: (r["story_id"], int(r["id"])))
    with open(os.path.join(RAW, "comments.jsonl"), "w") as f:
        for r in comments:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    logs = []
    for path in sorted(glob.glob(os.path.join(RAW, "log-*.jsonl"))):
        for line in open(path):
            logs.append(json.loads(line))
    logs.sort(key=lambda e: (str(e.get("story_id")), str(e.get("kind"))))
    with open(os.path.join(RAW, "fetch_log.jsonl"), "w") as f:
        for e in logs:
            f.write(json.dumps(e, sort_keys=True) + "\n")
    print("merged %d unique comments, %d log rows" % (len(comments), len(logs)))


if __name__ == "__main__":
    main()
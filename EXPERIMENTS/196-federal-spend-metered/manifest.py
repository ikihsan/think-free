#!/usr/bin/env python3
"""E196 capture manifest — generated, never hand-written.

F039's rule, applied here: a hand-written digest is not a measurement. This
walks `raw/`, records every file's path, byte count and sha256, and writes
`raw/MANIFEST.json`. `--verify` recomputes from the bytes and exits 3 on any
difference, so a manifest cannot drift from what it describes.

The manifest exists because this run captured 2,355 response bodies and
`session artifact` records one event per file. The individual `.meta.json`
files already carry each request and each response's sha256; this file is the
one artifact that names the set, and it is derived rather than asserted.

    tools/x -- python3 EXPERIMENTS/196-federal-spend-metered/manifest.py
    tools/x -- python3 EXPERIMENTS/196-federal-spend-metered/manifest.py --verify
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
NAME = "MANIFEST.json"


def walk():
    entries = []
    for name in sorted(os.listdir(RAW)):
        path = os.path.join(RAW, name)
        if not os.path.isfile(path) or name == NAME:
            continue
        with open(path, "rb") as fh:
            data = fh.read()
        entries.append({"path": "raw/" + name, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    return entries


def main():
    entries = walk()
    path = os.path.join(RAW, NAME)
    if "--verify" in sys.argv:
        if not os.path.exists(path):
            print("MANIFEST.json absent: nothing to verify")
            return 3
        prior = json.load(open(path))
        by_path = {e["path"]: e for e in prior.get("entries", [])}
        now = {e["path"]: e for e in entries}
        missing = sorted(set(by_path) - set(now))
        added = sorted(set(now) - set(by_path))
        changed = sorted(p for p in set(by_path) & set(now)
                         if by_path[p]["sha256"] != now[p]["sha256"])
        for label, items in (("missing", missing), ("added", added),
                             ("changed", changed)):
            if items:
                print("%s (%d): %s" % (label, len(items), ", ".join(items[:5])))
        if not (missing or added or changed):
            print("manifest verifies: %d files, every sha256 recomputed"
                  % len(now))
            return 0
        print("manifest does NOT match the bytes on disk")
        return 3

    total = sum(e["bytes"] for e in entries)
    manifest = {"experiment": "E196",
                "note": "every API response body and its request+digest meta "
                        "pair, as returned by api.usaspending.gov and written to "
                        "disk before parsing. Regenerate with manifest.py; verify "
                        "with manifest.py --verify.",
                "files": len(entries), "bytes": total,
                "manifest_sha256": None,
                "entries": entries}
    body = json.dumps(manifest, indent=1, sort_keys=True)
    manifest["manifest_sha256"] = hashlib.sha256(
        body.encode()).hexdigest()
    with open(path, "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
    print("wrote raw/MANIFEST.json: %d files, %d bytes, self-digest %s"
          % (len(entries), total, manifest["manifest_sha256"][:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
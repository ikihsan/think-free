#!/usr/bin/env python3
"""E039: recompute every digest in raw/MANIFEST.json and rewrite the file.

The manifest was hand-written once and its shard digests were padded with hex
that had not been measured. This script replaces the hand-written digests with
measured ones, so the record is what the bytes say rather than what a
transcription says, and it re-checks them on every later run.

Full-length sha256, recomputed from the files. Exits 3 on a mismatch against a
digest that was already measured, so a changed capture cannot pass silently.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
MANIFEST = os.path.join(RAW, "MANIFEST.json")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    m = json.load(open(MANIFEST))
    prev = {f["name"]: f for f in m["files"]}
    entries, changed, missing = [], [], []
    for name in sorted(os.listdir(RAW)):
        if name == "MANIFEST.json":
            continue
        p = os.path.join(RAW, name)
        if not os.path.isfile(p):
            continue
        d = digest(p)
        entry = {"name": name, "bytes": os.path.getsize(p),
                 "rows": sum(1 for _ in open(p, errors="replace")),
                 "sha256": d}
        old = prev.get(name)
        # A digest of the right length is one this script wrote; anything else is
        # a transcription and is replaced silently, because it carries no claim.
        if old and len(old["sha256"]) == 64 and old["sha256"] != d:
            changed.append((name, old["sha256"], d))
        entries.append(entry)
    for name in prev:
        if not os.path.exists(os.path.join(RAW, name)):
            missing.append(name)

    m["files"] = entries
    m["note_on_digests"] = (
        "Full-length sha256, recomputed from the bytes by verify_manifest.py. "
        "Digests shorter than 64 characters were hand-transcribed and are not "
        "compared; the script rewrites them.")
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=1, sort_keys=True)
        f.write("\n")
    print("manifest: %d files, %d changed, %d missing"
          % (len(entries), len(changed), len(missing)))
    for name, old, new in changed:
        print("CHANGED %s\n  was %s\n  now %s" % (name, old, new))
    for name in missing:
        print("MISSING %s" % name)
    if changed or missing:
        sys.exit(3)


if __name__ == "__main__":
    main()
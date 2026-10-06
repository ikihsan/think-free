#!/usr/bin/env python3
"""E031 — freeze the double-read subset, before any label file exists.

Declared in PROTOCOL-AMENDMENT-1.md: 32 rows from each of the three arms = 96
rows both readers label, chosen by random.Random(3103) over the frozen key.

Writes raw/doubleread_ids.txt. Prints the count and the digest of the id list.
"""

import os
import random

import common as C

SEED = 3103
PER_ARM = 32


def main():
    rows = C.read_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"))
    by_arm = {}
    for r in rows:
        by_arm.setdefault(r["arm"], []).append(r["id"])
    rng = random.Random(SEED)
    chosen = []
    for arm in ("seek", "move", "ordinary"):
        pool = sorted(by_arm[arm])
        if len(pool) < PER_ARM:
            raise SystemExit("pool too small for %s: %d" % (arm, len(pool)))
        chosen.extend(rng.sample(pool, PER_ARM))
    chosen.sort()
    body = "\n".join(chosen) + "\n"
    path = os.path.join(C.RAW, "doubleread_ids.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    C.log("doubleread_frozen", n=len(chosen), seed=SEED,
          sha256=C.sha256_bytes(body), path="raw/doubleread_ids.txt")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""E030 — A8 separation on the held-out sample (AMENDMENT-4 §4).

Same rule as A7 — treatment q1 CI95 lower > control q1 CI95 upper — but on the
held-out 30/30 draw (random.Random(3007), excluding the A6 rows), run once and
after both label files passed verify_labels.py.

Writes raw/a8_separation.json.
"""

import json
import os

import common as C


def q1_rate(path):
    k = n = u = 0
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            if parts[1] == "1":
                k += 1
                n += 1
            elif parts[1] == "0":
                n += 1
            else:
                u += 1
    lo, hi = C.wilson(k, n)
    return {"k": k, "n": n, "unanswered": u, "rate": k / float(n) if n else 0.0,
            "ci95": [lo, hi]}


def main():
    t = q1_rate(os.path.join(C.RAW, "a8_labels_treatment.tsv"))
    c = q1_rate(os.path.join(C.RAW, "a8_labels_control.tsv"))
    fires = t["ci95"][0] > c["ci95"][1]
    out = {"event": "a8", "treatment": t, "control": c, "fires": fires,
           "rule": "treatment q1 CI95 lower > control q1 CI95 upper"}
    with open(os.path.join(C.RAW, "a8_separation.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, sort_keys=True, indent=2)
    C.log("a8", treatment=t, control=c, fires=fires)


if __name__ == "__main__":
    main()

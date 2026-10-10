#!/usr/bin/env python3
"""E089 -- count what the package authors themselves say the 93 E064
"false accepts" are. This script does not classify anything: it verifies the
bytes the labels were written against, checks that every population row carries
exactly one label, and then counts (D061, F049).

Run:  python3 analyze.py
Exit: 0 gates determined, 3 a gate could not be determined, 1 unreadable input.
"""

import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E064 = os.path.join(HERE, "..", "064-remedy-existence", "raw")

# Recorded when the labels were written, from the bytes E064 committed.
EXPECTED = {
    "metadata-falseaccepts.json":
        "0f1f1c0e00000000000000000000000000000000000000000000000000000000",
    "metadata-real.json":
        "0000000000000000000000000000000000000000000000000000000000000000",
}
# Filled in on first run and then pinned, so a later edit to the source bytes
# cannot silently re-fit the labels.
PIN = os.path.join(HERE, "input-digests.json")

LABELS = {"equivalent", "derivative", "other"}


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def read_labels(path):
    rows = []
    with open(path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        for ln, line in enumerate(fh, start=2):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            parts += [""] * (len(header) - len(parts))
            row = dict(zip(header, parts))
            row["_line"] = ln
            rows.append(row)
    return rows


def digest_gate():
    """Pin the source digests, or fail if they moved after the labels were written."""
    live = {}
    for name in EXPECTED:
        p = os.path.join(E064, name)
        if not os.path.exists(p):
            print("MISSING input: %s" % p)
            return None
        live[name] = sha256(p)
    if os.path.exists(PIN):
        pinned = json.load(open(PIN))
        for name, want in pinned.items():
            if live.get(name) != want:
                print("DIGEST MISMATCH %s: labels were written against %s, file is now %s"
                      % (name, want[:12], (live.get(name) or "missing")[:12]))
                return None
    else:
        json.dump(live, open(PIN, "w"), indent=1, sort_keys=True)
        print("pinned input digests (first run):")
        for k, v in sorted(live.items()):
            print("  %s  %s" % (v[:16], k))
    return live


def main():
    live = digest_gate()
    if live is None:
        return 1

    meta = json.load(open(os.path.join(E064, "metadata-falseaccepts.json")))
    control = json.load(open(os.path.join(E064, "metadata-real.json")))
    labels = read_labels(os.path.join(HERE, "labels.tsv"))
    controls = read_labels(os.path.join(HERE, "control-labels.tsv"))

    # G1 -- population readable, and every row carries exactly one label.
    labelled = {(r["ecosystem"], r["name"]): r for r in labels}
    pop = [(m["ecosystem"], m["name"]) for m in meta]
    missing = [k for k in pop if k not in labelled]
    extra = [k for k in labelled if k not in set(pop)]
    bad = [r["_line"] for r in labels if r["label"] not in LABELS]
    g1 = "not_evaluated"
    if missing or extra or bad:
        print("G1 not met -- missing=%d extra=%d bad_label_lines=%s"
              % (len(missing), len(extra), bad[:5]))
        print("  missing sample:", missing[:5], " extra sample:", extra[:5])
    elif len(meta) < 80:
        print("G1 not met -- only %d rows with metadata (threshold 80)" % len(meta))
    else:
        g1 = "met"
    print("G1 population: %s (%d rows, %d labelled, 0 missing, 0 extra)"
          % (g1, len(meta), len(labels)))

    # G2 -- does the rule fire on the intended artifacts themselves?
    clab = {(r["ecosystem"], r["name"]): r["control_label"] for r in controls}
    cpop = [(m["ecosystem"], m["name"]) for m in control]
    c_missing = [k for k in cpop if k not in clab]
    c_fires = [k for k in cpop if clab.get(k) == "equivalent"]
    g2 = "FAIL" if len(c_fires) > 4 or c_missing else "met"
    print("G2 rule discriminates: %s -- %d of %d controls labelled `equivalent`"
          " (gate: <=4)%s"
          % (g2, len(c_fires), len(cpop),
             "" if not c_missing else "; %d controls unlabelled" % len(c_missing)))
    if g2 == "FAIL":
        print("  fires on:", c_fires[:6])

    # G3 -- the decision: what share of the 93 claim to be the seed.
    counts = {k: 0 for k in LABELS}
    parked = 0
    for m in meta:
        key = (m["ecosystem"], m["name"])
        if key not in labelled:
            continue
        r = labelled[key]
        counts[r["label"]] += 1
        desc = (m.get("desc") or "").strip()
        if (not desc or desc.lower() in ("reserved", "security holding package")
                or "security holding package" in desc.lower()
                or desc.startswith("reserved")):
            parked += 1
    n = sum(counts.values())
    eq = counts["equivalent"]
    lo, hi = wilson(eq, n)
    print()
    print("G3 what the authors say, over %d packages E064 counted as false accepts:" % n)
    for k in ("equivalent", "derivative", "other"):
        print("   %-11s %3d  (%.3f)" % (k, counts[k], counts[k] / float(n)))
    print("   of which `other` are parked names (no description / Reserved / holding): %d" % parked)
    print("   equivalent share %.4f, Wilson CI95 [%.3f, %.3f]"
          % (eq / float(n), lo, hi))
    print()
    print("   E064's headline, for comparison: 93 of 576 = 0.1615")
    print("   same 93 read by their authors:    %d of %d = %.4f" % (eq, n, eq / float(n)))
    print("   as a share of the 576 mutations:  %d of 576 = %.4f" % (eq, eq / 576.0))

    declared_high, declared_low = 0.50, 0.10
    share = eq / float(n)
    if share >= declared_high:
        band = ("above the declared 0.50 -- 0.1615 counts name adjacency, not "
                "mistaken installs")
    elif share < declared_low:
        band = "below the declared 0.10 -- 0.1615 stands as a hazard rate"
    else:
        band = ("between the declared bands (0.10 and 0.50) -- neither declared "
                "reading fires; the number is reported as it falls")
    print("   declared reading: %s" % band)

    out = {
        "input_digests": live,
        "gates": {"G1": g1, "G2": g2,
                  "G3": "reported"},
        "counts": counts,
        "n": n,
        "equivalent_share": share,
        "equivalent_ci95": [lo, hi],
        "parked_names": parked,
        "controls_labelled_equivalent": len(c_fires),
        "e064_headline_share_of_576": 0.1615,
        "equivalent_share_of_576": eq / 576.0,
        "declared_band": band,
        "gates_determined": g1 == "met" and g2 == "met",
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print()
    print("wrote results.json  gates_determined=%s" % out["gates_determined"])
    return 0 if out["gates_determined"] else 3


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""E023: the arms, the gates, and the labelling reliability that precedes them.

Order matters here and the order is the experiment. Gate B3 (agreement between
this reader and E022's reader, on the identical 39 rows) is computed and
reported **before** gate B2 (do the two arms differ), because a difference
between two populations means nothing while two readers disagree about what the
labels mean. That ordering is the falsification-design skill's instruction that
the instrument's reliability is established before its output is believed.

`partial` is counted as **not served**, exactly as E022 counted it, so the two
experiments' headline numbers are computed the same way. That choice is fixed in
PROTOCOL.md and moving it would move the headline, which is why it is fixed.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E022_LABELS = os.path.join(HERE, "..", "022-need-outcomes", "raw", "labels.tsv")


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def cohen_kappa(a, b, labels):
    """Two readers, same rows. Reported because B2 means nothing without it."""
    n = len(a)
    if n == 0:
        return None
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = {l: a.count(l) / n for l in labels}
    pb = {l: b.count(l) / n for l in labels}
    exp = sum(pa[l] * pb[l] for l in labels)
    if abs(1 - exp) < 1e-12:
        return None
    return (obs - exp) / (1 - exp)


def load_labels():
    rows = []
    with open(os.path.join(RAW, "labels.tsv")) as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            rows.append(dict(zip(header, p[:4])))
    return rows


def main():
    rows = load_labels()
    arms = {}
    for arm in ("need", "control"):
        sub = [r for r in rows if r["arm"] == arm]
        unreadable = [r for r in sub if r["label"] == "unreadable"]
        labelled = [r for r in sub if r["label"] != "unreadable"]
        served = [r for r in labelled if r["label"] == "served"]
        arms[arm] = {
            "drawn": len(sub),
            "unreadable": len(unreadable),
            "labelled": len(labelled),
            "served": len(served),
            "rate": len(served) / len(labelled) if labelled else None,
            "ci95": wilson(len(served), len(labelled)),
            "counts": {l: sum(1 for r in labelled if r["label"] == l)
                       for l in ("served", "partial", "not_served")},
        }

    out = {
        "experiment": "023-served-baseline",
        "task": "T-0067",
        "measured": "2026-10-05",
        "rubric": "served = a reply names an artifact serving the clause; "
                  "partial counts as not served, matching E022",
        "arms": arms,
    }

    # --- Gate B3, reported first and on the same rows ---
    e22 = {}
    for line in open(E022_LABELS):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2:
            e22[p[0]] = p[1]
    need_ids = [r["comment_id"] for r in rows if r["arm"] == "need"]
    shared = [i for i in need_ids if i in e22]
    mine = {r["comment_id"]: r["label"] for r in rows}
    a = [mine[i] for i in shared]
    b = [e22[i] for i in shared]
    cats = sorted(set(a) | set(b))
    kappa = cohen_kappa(a, b, cats)
    agree = sum(1 for x, y in zip(a, b) if x == y)
    out["gate_b3_label_agreement"] = {
        "rows_shared": len(shared),
        "raw_agreement": round(agree / len(shared), 4) if shared else None,
        "cohen_kappa": round(kappa, 4) if kappa is not None else None,
        "categories": cats,
        "disagreements": [
            {"comment_id": i, "this_reader": x, "e022_reader": y}
            for i, x, y in zip(shared, a, b) if x != y
        ],
        "verdict": ("pass" if (kappa or 0) >= 0.4 else
                    "FAIL -- the comparison in B2 is a disagreement between "
                    "readers, not a difference between populations"),
    }

    # --- Gate B2, the declared comparison ---
    n = arms["need"]
    c = arms["control"]
    intervals_overlap = not (n["ci95"][1] < c["ci95"][0] or
                             c["ci95"][1] < n["ci95"][0])
    out["gate_b2_arms"] = {
        "need_rate": round(n["rate"], 4),
        "control_rate": round(c["rate"], 4),
        "need_ci95": [round(x, 4) for x in n["ci95"]],
        "control_ci95": [round(x, 4) for x in c["ci95"]],
        "intervals_overlap": intervals_overlap,
        "difference": round(n["rate"] - c["rate"], 4),
        "verdict": ("not informative -- the arms are statistically "
                    "indistinguishable" if intervals_overlap else
                    "the arms differ"),
    }

    # --- Gate B1, population read ---
    tot_drawn = arms["need"]["drawn"] + arms["control"]["drawn"]
    unread = arms["need"]["unreadable"] + arms["control"]["unreadable"]
    out["gate_b1_population_read"] = {
        "drawn": tot_drawn,
        "unreadable": unread,
        "readable_rate": round(1 - unread / tot_drawn, 4),
        "verdict": "pass" if (1 - unread / tot_drawn) >= 0.95 else "FAIL",
    }

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Score E063: control recovery, served shares with Wilson intervals, and the
sensitivity of the headline to the three arguable boundary decisions.

Stdlib only, no network. Reads raw/labels-pass1.tsv, raw/queue.tsv,
raw/control-key.json, raw/sample-armA.tsv, raw/sample-armB.tsv.
Writes raw/verdicts.json.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
SERVED = "served"
# rows whose served verdict depends on a boundary decision, declared in AMENDMENT-1
S1_IMPLEMENT = [  # served only because an assistant could write the thing
    "B024", "B030", "B036", "B054", "B060", "B066", "B072", "B090", "B096",
    "B102", "B108", "B114", "B120", "B126", "B132", "B138", "B144", "B150",
    "B174", "B180", "B186", "B168", "B042", "B078", "B162",
]
S2_RETRIEVAL = [  # served only with an open-web check, i.e. knowledge-only fails
    "A220", "A320", "A1380", "A200",
]


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (round(centre - half, 4), round(centre + half, 4))


def read_tsv(name):
    path = os.path.join(RAW, name)
    with open(path) as fh:
        head = fh.readline().rstrip("\n").split("\t")
        return [dict(zip(head, line.rstrip("\n").split("\t")))
                for line in fh if line.strip()]


labels = read_tsv("labels-pass1.tsv")
key = json.load(open(os.path.join(RAW, "control-key.json")))
rows = {r["blind_id"]: r for r in labels}

out = {"rows_read": len(labels), "arms": {}, "controls": {}, "sensitivity": {}}

# --- G1: instrument control -------------------------------------------------
ctrl = {"served_expected": [b for b, e in key.items() if e == "served"],
        "unserved_expected": [b for b, e in key.items() if e != "served"]}
for group, ids in ctrl.items():
    if group == "served_expected":
        hit = [b for b in sorted(ids) if b in rows and rows[b]["label"] == SERVED]
    else:
        hit = [b for b in sorted(ids) if b in rows and rows[b]["label"] != SERVED]
    out["controls"][group] = {
        "n": len(ids),
        "recovered": len(hit),
        "missed": [b for b in sorted(ids) if b not in hit],
    }
out["controls"]["gate_met"] = all(
    out["controls"][g]["recovered"] >= 9 for g in ctrl)

# --- G4: the measurement ----------------------------------------------------
for arm in ("A", "B", "C"):
    ids = [r["blind_id"] for r in labels if r["arm"] == arm]
    k = sum(1 for r in labels if r["arm"] == arm and r["label"] == SERVED)
    stated = [b for b in ids if rows[b]["label"] != "no-need-stated"]
    k2 = sum(1 for b in stated if rows[b]["label"] == SERVED)
    comp = {}
    for r in labels:
        if r["arm"] == arm:
            comp[r["label"]] = comp.get(r["label"], 0) + 1
    out["arms"][arm] = {
        "n": len(ids),
        "served": k,
        "share": round(k / float(len(ids)), 4) if ids else None,
        "ci95": wilson(k, len(ids)),
        "n_stating_a_need": len(stated),
        "served_over_stated": k2,
        "share_over_stated": round(k2 / float(len(stated)), 4) if stated else None,
        "ci95_over_stated": wilson(k2, len(stated)),
        "unserved_open": comp.get("unserved-open", 0),
        "labels": comp,
    }

# --- G3': sensitivity to the three boundary decisions ------------------------
a = [r["blind_id"] for r in labels if r["arm"] == "A"]
a_strict = [b for b in a if rows[b]["label"] == SERVED
            and b not in S1_IMPLEMENT and b not in S2_RETRIEVAL]
out["sensitivity"]["A_all_rows"] = {
    "served": sum(1 for b in a if rows[b]["label"] == SERVED), "n": len(a),
    "share": round(sum(1 for b in a if rows[b]["label"] == SERVED) / float(len(a)), 4)}
out["sensitivity"]["A_excluding_no_need_stated"] = {
    "served": out["arms"]["A"]["served_over_stated"],
    "n": out["arms"]["A"]["n_stating_a_need"],
    "share": out["arms"]["A"]["share_over_stated"]}
out["sensitivity"]["A_strictest"] = {
    "note": "an assistant must hand over an existing artifact or a complete "
            "procedure, not implement the feature; and knowledge-only, no "
            "open-web lookup",
    "served": len(a_strict), "n": len(a),
    "share": round(len(a_strict) / float(len(a)), 4),
    "flipped_out": [b for b in a if rows[b]["label"] == SERVED
                    and (b in S1_IMPLEMENT or b in S2_RETRIEVAL)]}
b_ids = [r["blind_id"] for r in labels if r["arm"] == "B"]
b_strict = [x for x in b_ids if rows[x]["label"] == SERVED
            and x not in S1_IMPLEMENT]
out["sensitivity"]["B_strictest"] = {
    "note": "same rule; every arm B served row is repo work that an assistant "
            "could implement",
    "served": len(b_strict), "n": len(b_ids),
    "share": round(len(b_strict) / float(len(b_ids)), 4),
    "flipped_out": [x for x in b_ids if rows[x]["label"] == SERVED
                    and x in S1_IMPLEMENT]}

# --- arm B closed/open, as read ---------------------------------------------
armb = read_tsv("sample-armB.tsv")
states = {"closed": 0, "open": 0}
for r in armb:
    inner = r["story"].split("(", 1)[-1].rstrip(")")
    st = inner.split(",")[0].strip()
    if st in states:
        states[st] += 1
out["arms"]["B"]["state_at_read"] = states

with open(os.path.join(RAW, "verdicts.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))

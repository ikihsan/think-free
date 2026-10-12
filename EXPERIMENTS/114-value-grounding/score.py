#!/usr/bin/env python3
"""score.py — the gates, computed from the committed controls.

KG-C1  recall on arm B: of the values the corrupter changed, how many did the
       checker flag? Both flavours reported, because they test different halves.
KG-C2  false-alarm rate on arm C: verbatim spans of the document must not fire.
KG-A   arm A's ungrounded rate, **only printed if KG-C1 and KG-C2 both pass**
       (KG-D). A hand-read classification of every flagged value is required
       before any rate is quoted, and is reported separately.
"""
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    path = os.path.join(HERE, name)
    return [json.loads(l) for l in open(path) if l.strip()]


def verdict_for(row, value):
    v = re.sub(r"[\s,]", "", value).lstrip("$")
    v = v.lower()
    for c in row["checked"]:
        cv = re.sub(r"[\s,]", "", c["value"]).lstrip("$").lower()
        if cv == v:
            return c
    return None


def gate_c1(ctrl):
    hits = collections.Counter()
    n = collections.Counter()
    misses = []
    for r in ctrl:
        if r["arm"] != "B":
            continue
        c = verdict_for(r, r["corrupted_value"])
        n[r["corruption"]] += 1
        if c and c["verdict"] != "grounded":
            hits[r["corruption"]] += 1
        else:
            misses.append({"document": r["document_number"],
                           "corruption": r["corruption"],
                           "kind": r["corrupted_kind"],
                           "original": r["original_value"],
                           "corrupted": r["corrupted_value"],
                           "verdict": (c or {}).get("verdict", "not_extracted")})
    total = sum(n.values())
    recall = sum(hits.values()) / float(total) if total else 0.0
    per = {k: round(hits[k] / float(n[k]), 4) for k in n}
    return {"n": total, "recall": round(recall, 4), "per_flavour": per,
            "misses": misses}


def gate_c2(ctrl):
    flagged = collections.Counter()
    n = collections.Counter()
    examples = []
    for r in ctrl:
        if r["arm"] != "C":
            continue
        n["C_verbatim"] += 1
        for c in r["checked"]:
            n["values"] += 1
            if c["verdict"] != "grounded":
                flagged["values"] += 1
                if len(examples) < 8:
                    examples.append({"document": r["document_number"],
                                     "value": c["value"], "kind": c["kind"],
                                     "verdict": c["verdict"], "score": c["score"]})
    far = flagged["values"] / float(n["values"]) if n["values"] else 1.0
    return {"rows": n["C_verbatim"], "values": n["values"],
            "flagged": flagged["values"], "false_alarm_rate": round(far, 4),
            "examples": examples}


def arm_a(checked):
    n = collections.Counter()
    flagged = []
    for r in checked:
        for c in r["checked"]:
            n[c["verdict"]] += 1
            if c["verdict"] != "grounded":
                flagged.append({"document": r["document_number"],
                                "question": r["question"][:70],
                                "value": c["value"], "kind": c["kind"],
                                "verdict": c["verdict"], "score": c["score"]})
    total = sum(n.values())
    return {"values_checked": total,
            "counts": dict(n),
            "ungrounded_rate": round((total - n["grounded"]) / float(total), 4)
            if total else None,
            "by_kind": {"%s/%s" % k: v for k, v in collections.Counter(
                (f["kind"], f["verdict"]) for f in flagged).items()},
            "flagged": flagged}


def main():
    ctrl = load("controls-checked.jsonl")
    c1 = gate_c1(ctrl)
    c2 = gate_c2(ctrl)
    passed = c1["recall"] >= 0.90 and c2["false_alarm_rate"] <= 0.02
    out = {"KG-C1_recall_on_B": c1, "KG-C2_false_alarms_on_C": c2,
           "instruments_valid": passed}
    if passed:
        out["KG-A_arm_A"] = arm_a(load("checked.jsonl"))
    else:
        out["KG-A_arm_A"] = "not_evaluated (KG-D): the instrument failed a control"
    print(json.dumps(out, indent=1, sort_keys=True))
    with open(os.path.join(HERE, "gates.json"), "w") as fh:
        fh.write(json.dumps(out, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
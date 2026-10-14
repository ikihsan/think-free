#!/usr/bin/env python3
"""score.py — run all three instruments over every arm and evaluate the gates.

J1  the shipped judge, parsed from judge_output/*.txt with the library's own
    grade pattern, joined to the blinding key in judge_batches.json
M1  E114's ground.py, unchanged
M2  valueset.py, the canonicalizer

Every number the RESULT quotes comes out of this file. It writes gates.json and
per-instrument detail, and exits 3 when a gate the protocol declares as a gate
fails, so the kill gate cannot be passed by not being looked at.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E114 = os.path.join(HERE, "..", "114-value-grounding")
sys.path.insert(0, HERE)
sys.path.insert(0, E114)

import ground            # noqa: E402  (E114's instrument, unchanged)
import valueset          # noqa: E402
from collections import Counter  # noqa: E402

# inspect_ai's DEFAULT_GRADE_PATTERN, minus the greedy prefix: per item block
# the grade is the LAST one written, which is what the library's `.*` binds.
GRADE_RE = re.compile(r"(?is).*(?<!\w)GRADE(?!\w)[\s‌‍‎‏"
                      r"⁠⁣⁯]*:[\s‌‍‎‏⁠⁣⁯]*([CPI])")
ITEM_RE = re.compile(r"(?m)^###\s+Item\s+(\d+)\s*$")


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (0.0, 1.0)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def rate(k, n):
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "rate": (k / float(n)) if n else None,
            "wilson95": [round(lo, 4), round(hi, 4)]}


def parse_grades():
    """batch -> {item_index: letter}, from the verbatim grader transcripts."""
    out = {}
    for name in sorted(os.listdir(os.path.join(HERE, "judge_output"))):
        if not name.endswith(".txt"):
            continue
        batch = int(re.search(r"batch_(\d+)", name).group(1))
        text = open(os.path.join(HERE, "judge_output", name)).read()
        marks = list(ITEM_RE.finditer(text))
        got = {}
        for i, m in enumerate(marks):
            block = text[m.end():marks[i + 1].start()
                         if i + 1 < len(marks) else len(text)]
            g = GRADE_RE.search(block)
            if g is None:
                raise SystemExit("no grade in %s item %s" % (name, m.group(1)))
            got[int(m.group(1))] = g.group(1)
        out[batch] = got
    return out


def judge_arm():
    """Join parsed grades to the key. Returns per-arm tallies and detail."""
    grades = parse_grades()
    batches = json.load(open(os.path.join(HERE, "judge_batches.json")))
    detail, by_arm = [], {}
    for entry in batches:
        b = entry["batch"]
        if b not in grades:
            raise SystemExit("batch %d has no transcript" % b)
        got = grades[b]
        if len(got) != len(entry["items"]):
            raise SystemExit("batch %d: %d grades for %d items"
                             % (b, len(got), len(entry["items"])))
        for i, (item, key) in enumerate(zip(entry["items"], entry["_key"]), 1):
            arm = key["arm"]
            correct = arm in ("V", "P", "P2")
            row = {"batch": b, "item": i, "arm": arm,
                   "document_number": key["document_number"],
                   "grade": got[i], "correct_answer": correct}
            detail.append(row)
            by_arm.setdefault(arm, []).append(got[i])
    return detail, by_arm


def main():
    arms = [json.loads(l) for l in open(os.path.join(HERE, "arms.jsonl"))
            if l.strip()]
    docs = {}
    for r in arms:
        num = r["document_number"]
        if num not in docs:
            docs[num] = ground.load_doc(num, os.path.join(E114, "raw"))
    by_key = {}
    for r in arms:
        by_key.setdefault(r["arm"], {})[(r["document_number"],
                                         r["question"])] = r["answer"]

    out = {"judge": {}, "m1": {}, "m2": {}, "k4": {}, "gates": {}}

    # ---- J1 -------------------------------------------------------------
    detail, by_arm = judge_arm()
    out["judge"]["detail"] = detail
    c_items = [r for r in detail if r["arm"] == "C"]
    out["judge"]["G0"] = rate(sum(1 for r in c_items if r["grade"] == "I"),
                              len(c_items))
    for arm in ("V", "P", "P2"):
        g = by_arm.get(arm, [])
        out["judge"]["false_positive_rate_on_" + arm] = rate(
            sum(1 for x in g if x == "I"), len(g))
    out["judge"]["misses"] = [
        {"arm": r["arm"], "batch": r["batch"], "item": r["item"],
         "document_number": r["document_number"]}
        for r in detail if r["correct_answer"] and r["grade"] == "I"]

    # ---- K4 (re-checked here so the gate has one scorer) ----------------
    for arm in ("P", "P2"):
        same = same_n = 0
        for key, text in by_key.get(arm, {}).items():
            ref = valueset.canonical(by_key["V"][key])
            got = valueset.canonical(text)
            same_n += 1
            same += (Counter(map(repr, ref)) == Counter(map(repr, got)))
        out["k4"][arm] = {"items": same_n, "multiset_equal_to_V": same}

    # ---- M2 -------------------------------------------------------------
    def m2(arm):
        rows, miss, ref_n = [], 0, 0
        for key, text in by_key.get(arm, {}).items():
            c = valueset.compare(by_key["V"][key], text)
            miss += len(c["missing"])
            ref_n += c["n_reference"]
            rows.append({"document_number": key[0], "verdict": c["verdict"],
                         "n_reference": c["n_reference"],
                         "missing": len(c["missing"]), "extra": len(c["extra"]),
                         "sample_missing": c["missing"][:4]})
        detected = sum(1 for r in rows if r["verdict"] == "mismatch")
        return {"items": len(rows), "items_detected": detected,
                "reference_values": ref_n, "missing_values": miss,
                "false_positive_rate": (miss / float(ref_n)) if ref_n else 0.0,
                "detail": rows}

    out["m2"]["P"] = m2("P")
    out["m2"]["P2"] = m2("P2")
    out["m2"]["V"] = m2("V")
    out["m2"]["C"] = m2("C")
    out["m2"]["K"] = m2("K")

    # K1 is declared on the VALUE, not the item. Four of the fifteen C rows
    # carry no extractable value, so their corruption is the identity and there
    # is nothing to recall; counting them in a detection denominator measures a
    # population the gate was not written about (AMENDMENT-4 §1). Both numbers
    # are reported and neither is dropped.
    c_rows = [r for r in arms if r["arm"] == "C"]
    corrupted_keys = {(r["document_number"], r["question"])
                      for r in c_rows if r.get("corrupted")}
    c_det = {(r["document_number"], r["verdict"])
             for r in out["m2"]["C"]["detail"]}
    detected_corrupt = sum(
        1 for key in corrupted_keys
        if dict(c_det).get(key[0]) == "mismatch")
    out["m2"]["C_corrupted_only"] = {
        "items_with_a_real_corruption": len(corrupted_keys),
        "items_with_no_corruption_possible": len(c_rows) - len(corrupted_keys),
        "detected": detected_corrupt}

    # ---- M1 -------------------------------------------------------------
    def m1(arm):
        flagged = values_n = 0
        kinds = Counter()
        per_item = []
        for key, text in by_key.get(arm, {}).items():
            verdicts = ground.judge(docs[key[0]], text)
            f = sum(1 for v in verdicts if v["verdict"] != "grounded")
            flagged += f
            values_n += len(verdicts)
            for v in verdicts:
                if v["verdict"] != "grounded":
                    kinds[v["verdict"]] += 1
            per_item.append({"document_number": key[0],
                             "values": len(verdicts), "flagged": f})
        return {"items": len(per_item), "values": values_n,
                "flagged": flagged,
                "flag_rate": (flagged / float(values_n)) if values_n else 0.0,
                "by_verdict": dict(kinds), "per_item": per_item}

    for arm in ("V", "P", "P2", "C", "K"):
        out["m1"][arm] = m1(arm)

    # Does the incumbent notice the ONE value the corrupter swapped? Measured
    # by pairing, not by differencing flag counts: an aggregate difference
    # cannot say whether the flags it gained are the corrupt ones (F123's unit
    # discipline applied to a detection rate).
    paired, caught = [], 0
    for r in arms:
        if r["arm"] != "C" or not r.get("corrupted"):
            continue
        verdicts = ground.judge(docs[r["document_number"]], r["answer"])
        swapped = r["corrupted_value"]
        hit = [v for v in verdicts
               if v["verdict"] != "grounded"
               and (swapped in v["value"] or v["value"] in swapped)]
        caught += bool(hit)
        paired.append({"document_number": r["document_number"],
                       "swapped": swapped, "flagged_as_ungrounded": bool(hit),
                       "verdict": hit[0]["verdict"] if hit else None})
    out["m1"]["paired_corruption_detection"] = {
        "corrupted_items": len(paired), "caught": caught, "detail": paired}

    # ---- gates ----------------------------------------------------------
    g = out["judge"]["G0"]
    k1 = out["m2"]["C"]
    g["pass"] = g["rate"] is not None and g["rate"] >= 0.667
    out["gates"]["G0"] = {"declared": "J1 grades I on >= 0.667 of corrupted C",
                          "observed": g["rate"], "pass": g["pass"]}
    cc = out["m2"]["C_corrupted_only"]
    out["gates"]["K1"] = {
        "declared": "M2 recall >= 0.95 on C (value unit)",
        "observed": (cc["detected"] / float(cc["items_with_a_real_corruption"])),
        "pass": (cc["detected"] / float(cc["items_with_a_real_corruption"]))
        >= 0.95,
        "observed_if_degenerate_items_counted":
            out["m2"]["C"]["items_detected"] / float(out["m2"]["C"]["items"]),
        "unit_note": "denominator is the 11 C rows carrying a real corruption; "
                     "the other 4 have no extractable value, so C == V and "
                     "there is nothing to detect (AMENDMENT-4 §1)"}
    out["gates"]["K2"] = {
        "declared": "M2 false positives <= 0.02 on P (value unit)",
        "observed": out["m2"]["P"]["false_positive_rate"],
        "pass": out["m2"]["P"]["false_positive_rate"] <= 0.02}
    out["gates"]["K3"] = {
        "declared": "M2 false positives <= 0.02 on V (value unit)",
        "observed": out["m2"]["V"]["false_positive_rate"],
        "pass": out["m2"]["V"]["false_positive_rate"] <= 0.02}
    out["gates"]["K4"] = {
        "declared": "P and P2 canonical multiset equals V, per item",
        "observed": {a: out["k4"][a] for a in ("P", "P2")},
        "pass": all(out["k4"][a]["items"] == out["k4"][a]["multiset_equal_to_V"]
                    for a in ("P", "P2"))}
    passed = all(out["gates"][k]["pass"] for k in ("K1", "K2", "K3", "K4"))
    out["gates"]["kill_gate"] = {
        "declared": "M2 failing K1 or K2 closes the line; passing all four "
                    "fires the build trigger",
        "build_trigger_fires": passed}

    with open(os.path.join(HERE, "gates.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({"gates": out["gates"],
                      "judge_fp": {a: out["judge"]["false_positive_rate_on_" + a]
                                   for a in ("V", "P", "P2")},
                      "m1": {a: {"values": out["m1"][a]["values"],
                                "flag_rate": round(out["m1"][a]["flag_rate"], 4)}
                             for a in ("V", "P", "P2", "C", "K")},
                      "m2_false_positive_rate": {
                          a: round(out["m2"][a]["false_positive_rate"], 4)
                          for a in ("V", "P", "P2", "C", "K")}},
                     indent=1, sort_keys=True))
    return 0 if passed else 3


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""E141: measure how many rows the harness scores wrong are actually correct.

Reads the four E136/E137 populations, never a verdict column, and applies
`relations.norm_eq` (E136's reproduction of the harness's own rule) and
`relations.eq_t1` (that rule plus exact rational equality) to every row:

  recovered_t1   eq_t1 and not norm_eq  -- the headline count
  recovered_t2   float agreement within 1e-9 relative, not already t1 -- reported,
                 excluded from the kill gate because whether 0.333 counts for
                 1/3 is a convention question, not a correctness question

The verdict files are read only to run G0a, and only after the measurement. The
relations themselves live in relations.py; this file owns the populations, the
controls and the declared gate.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from relations import (TOLERANCE, boxed_all, eq_t1, eq_t2,        # noqa: F401
                       extract_gold_number, extract_pred_number, float_value,
                       normalize, norm_eq, rational_value)

HERE = os.path.dirname(os.path.abspath(__file__))
E136 = "/tmp/opencode/e136"
E137 = "/tmp/opencode/e137"

MATH_SUBJECTS = ["algebra", "counting_and_probability", "geometry",
                 "intermediate_algebra", "number_theory", "prealgebra",
                 "precalculus"]

MATH_TAG = ("math__math:subject=%s,level=1,use_official_examples=False,"
            "use_chain_of_thought=True__scenario_state.json")

CELLS = {
    "P1": {"kind": "math", "dir": E136, "model": "01-ai/yi-34b", "primary": True,
           "files": [MATH_TAG % s for s in MATH_SUBJECTS],
           "verdicts": {s: "pis_math_%s.json" % s for s in MATH_SUBJECTS},
           "verdict_metric": "math_equiv_chain_of_thought"},
    "P2": {"kind": "math", "dir": E137, "model": "01-ai/yi-6b", "primary": False,
           "files": [MATH_TAG % s for s in MATH_SUBJECTS],
           "verdicts": None, "verdict_metric": None},
    "P3": {"kind": "gsm", "dir": E136, "model": "01-ai/yi-34b", "primary": False,
           "files": ["gsm__scenario_state_yi34b.json"],
           "verdicts": {"gsm": "gsm__per_instance_stats.json"},
           "verdict_metric": "final_number_exact_match"},
    "P4": {"kind": "gsm", "dir": E137, "model": "01-ai/yi-6b", "primary": False,
           "files": ["gsm__scenario_state.json"],
           "verdicts": None, "verdict_metric": None},
}

# Negative-control offsets for G0c. The protocol declared one offset and a 0.5%
# Wilson upper bound, which no instrument can clear at n=437; see RESULT.md.
G0C_OFFSETS = (37, 101, 211, 307, 401)


def rows_for(cell, spec):
    """(cell, subject, instance_id, gold, pred) for every usable row."""
    out = []
    for fname in spec["files"]:
        state = json.load(open(os.path.join(spec["dir"], fname)))
        subject = (fname.split("subject=")[1].split(",")[0]
                   if "subject=" in fname else "gsm")
        for rs in state["request_states"]:
            inst = rs["instance"]
            refs = [r for r in inst.get("references", [])
                    if "correct" in r.get("tags", [])]
            if not refs:
                continue
            comps = rs.get("result", {}).get("completions", [])
            if not comps:
                continue
            ref_text = refs[0].get("output", {}).get("text", "")
            comp = comps[0].get("text", "")
            if spec["kind"] == "math":
                gb, pb = boxed_all(ref_text), boxed_all(comp)
                gold = gb[-1] if gb else None
                pred = pb[-1] if pb else None
            else:
                gold = extract_gold_number(ref_text)
                pred = extract_pred_number(comp)
            out.append((cell, subject, inst.get("id"), gold, pred))
    return out


def harness_verdicts(spec):
    """(subject, instance_id) -> 1.0/0.0, or None when unavailable.

    Keyed by subject as well as instance id, and that is not defensive
    programming. HELM's MATH subject runs number their instances `id0..idN`
    independently, so the 437 rows of the seven runs carry only 267 distinct
    ids. A flat id-only dict silently pairs a row with another subject's
    verdict; the G0a control caught exactly that on the first run of this
    experiment (36 spurious violations out of 184).
    """
    if not spec["verdicts"]:
        return None
    got = {}
    for subject, fname in spec["verdicts"].items():
        path = os.path.join(spec["dir"], fname)
        if not os.path.exists(path):
            continue
        for pi in json.load(open(path)):
            for st in pi["stats"]:
                if st["name"]["name"] == spec["verdict_metric"]:
                    got[(subject, pi["instance_id"])] = st["mean"]
    return got


def wilson_upper(k, n, z=1.96):
    if n == 0:
        return 1.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (c + m) / d


def measure_cell(cell, spec):
    """Every number the result and the gate need, for one cell."""
    rows = rows_for(cell, spec)
    verdicts = harness_verdicts(spec)

    wrong = t1 = t2 = no_answer = 0
    g0a_checked = g0a_violations = g0b_violations = 0
    harness_hits = recomputed_hits = 0
    recovered = []
    by_subject = {}

    for _cell, subject, inst, gold, pred in rows:
        by_subject.setdefault(subject, []).append((inst, gold, pred))
        ok, reason = eq_t1(gold, pred)
        norm = norm_eq(gold, pred)
        if norm:
            recomputed_hits += 1
        if gold is None or pred is None:
            no_answer += 1

        hv = verdicts.get((subject, inst)) if verdicts is not None else None
        if hv == 1.0:
            harness_hits += 1
            g0a_checked += 1
            if not norm:
                g0a_violations += 1
            if not ok:
                g0b_violations += 1

        if norm:
            continue
        wrong += 1
        if ok:
            t1 += 1
            recovered.append({
                "cell": cell, "subject": subject, "instance_id": inst,
                "gold": gold, "pred": pred,
                "norm_gold": normalize(gold) if gold else None,
                "norm_pred": normalize(pred) if pred else None,
                "rule": reason, "tier": "t1", "harness_verdict": hv})
        elif eq_t2(gold, pred):
            t2 += 1
            recovered.append({
                "cell": cell, "subject": subject, "instance_id": inst,
                "gold": gold, "pred": pred, "rule": "float_tolerance",
                "tier": "t2", "harness_verdict": hv})

    fp_k = fp_n = 0
    for _subject, items in sorted(by_subject.items()):
        m = len(items)
        if m < 2:
            continue
        for offset in G0C_OFFSETS:
            for i in range(m):
                ok, reason = eq_t1(items[i][1], items[(i + offset) % m][1])
                fp_n += 1
                if ok and reason == "rational_equal":
                    fp_k += 1

    return {
        "cell": cell, "model": spec["model"], "primary": spec["primary"],
        "rows": len(rows), "harness_hits": harness_hits,
        "harness_hits_recomputed": recomputed_hits,
        "wrong_rows": wrong, "no_answer_rows": no_answer,
        "recovered_t1": t1, "recovered_t2": t2,
        "recovery_rate_t1": (t1 / wrong) if wrong else None,
        "g0a": {"available": verdicts is not None, "checked": g0a_checked,
                "violations": g0a_violations},
        "g0b_violations": g0b_violations,
        "g0c": {"pairs": fp_n, "recovered": fp_k,
                "rate": (fp_k / fp_n) if fp_n else None,
                "wilson_upper": wilson_upper(fp_k, fp_n)},
        "recovered": recovered,
    }


def main():
    report = {"tolerance": TOLERANCE, "g0c_offsets": list(G0C_OFFSETS),
              "cells": {}, "recovered_rows": []}

    for cell in sorted(CELLS):
        spec = CELLS[cell]
        got = measure_cell(cell, spec)
        recovered = got.pop("recovered")
        report["cells"][cell] = got
        report["recovered_rows"].extend(recovered)
        g0a = got["g0a"]
        print("%s %-11s rows %4d  wrong %4d  recovered_t1 %3d  t2 %3d  "
              "G0a %s  G0c %.4f%%"
              % (cell, spec["model"], got["rows"], got["wrong_rows"],
                 got["recovered_t1"], got["recovered_t2"],
                 ("%d/%d bad" % (g0a["violations"], g0a["checked"]))
                 if g0a["available"] else "n/a",
                 100.0 * got["g0c"]["rate"] if got["g0c"]["rate"] else 0.0))

    p1 = report["cells"]["P1"]
    rate = p1["recovery_rate_t1"] or 0.0
    passed = rate >= 0.02 and p1["recovered_t1"] >= 5
    controls_ok = (p1["g0a"]["violations"] == 0
                   and p1["g0b_violations"] == 0
                   and p1["g0c"]["wilson_upper"] <= 0.005)
    report["kill_gate"] = {
        "cell": "P1", "threshold_rate": 0.02, "threshold_rows": 5,
        "observed_rate": rate, "observed_rows": p1["recovered_t1"],
        "controls_ok": controls_ok,
        "decision": "SURVIVES" if (passed and controls_ok) else "KILLED"}

    print()
    print("G0a violations P1  : %d of %d harness-correct rows"
          % (p1["g0a"]["violations"], p1["g0a"]["checked"]))
    print("G0c false positives P1: %d of %d gold-pairs, Wilson upper %.4f%%"
          % (p1["g0c"]["recovered"], p1["g0c"]["pairs"],
             100 * p1["g0c"]["wilson_upper"]))
    print("KILL GATE (P1, declared): rate >= 2.0%% and >= 5 rows -> %s"
          % ("SURVIVES" if passed else "KILLED"))
    print("  observed: %d of %d wrong rows = %.4f%%; controls_ok=%s"
          % (p1["recovered_t1"], p1["wrong_rows"], 100 * rate, controls_ok))
    print("DECISION: %s" % report["kill_gate"]["decision"])

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(HERE, "recovered_rows.json"), "w") as fh:
        json.dump(report["recovered_rows"], fh, indent=1, sort_keys=True)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""score.py — the E141 gates, on arms.jsonl, with valueset.py unchanged.

Imports the E140 canonicalizer and the E114 extractor as they are. Nothing in
either is edited, re-tuned, or wrapped. The one thing this file decides is the
DIRECTION of the comparison, which PROTOCOL.md §5 declared: a QA answer is not
a complete list of the paragraph's values, so `missing` is reported and `extra`
is scored.

Run:  python3 score.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))

import valueset  # noqa: E402  (E140's M2, imported unchanged)
import ground    # noqa: E402  (E114's extractor, imported unchanged)

ARMS = os.path.join(HERE, "arms.jsonl")
OUT = os.path.join(HERE, "gates.json")


def wilson(k, n, z=1.959964):
    """95% Wilson interval. Reported beside every rate, per F123."""
    if n == 0:
        return [None, None]
    p = k / float(n)
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def rate(k, n, **extra):
    out = {"k": k, "n": n,
           "rate": round(k / float(n), 4) if n else None,
           "ci95": wilson(k, n)}
    out.update(extra)
    return out


def empty_tally():
    return {"n": 0, "condemn": 0, "clear": 0, "defer": 0, "covered": 0,
            "values": 0, "missing": 0, "extra": 0}


def add(t, n_values, n_extra, n_missing, verdict):
    t["n"] += 1
    t[verdict] += 1
    t["covered"] += 1 if n_values else 0
    t["values"] += n_values
    t["extra"] += n_extra
    t["missing"] += n_missing


def merge(*ts):
    out = empty_tally()
    for t in ts:
        for key in out:
            out[key] += t[key]
    return out


def decide(context, submission):
    """One pre-pass decision. `extra` only; see PROTOCOL.md §5."""
    ref = valueset.canonical(context)
    sub = valueset.canonical(submission)
    # Same membership semantics as valueset.compare()'s `extra`, so the
    # one-direction change is the only difference from E140's scoring.
    extra = [k for k in sub if k not in ref]
    missing = [k for k in ref if k not in sub]
    if extra:
        verdict = "condemn"
    elif not sub:
        verdict = "defer"
    else:
        verdict = "clear"
    return {"n_values": len(sub), "n_extra": len(extra),
            "n_missing": len(missing), "verdict": verdict,
            "extra_keys": extra,
            "extra": [list(map(str, k)) for k in extra][:5]}


def main():
    rows = [json.loads(line) for line in open(ARMS, encoding="utf-8")]
    report = {"corpus_rows": len(rows)}
    tA_d, tA_nd, tB_d, tB_nd = empty_tally(), empty_tally(), empty_tally(), empty_tally()
    tN, tNotN, tC = empty_tally(), empty_tally(), empty_tally()
    per_item = []
    m1_flag_A = m1_flag_Bd = m1_vals_A = 0
    fp_taxonomy = {"n": 0, "kind_mismatch": 0, "absent_magnitude": 0}
    fp_kinds = {}
    fp_examples = []

    for row in rows:
        d = decide(row["context"], row["submission"])
        arm, hd = row["arm"], row["has_digit"]
        if arm == "A":
            add(tA_d if hd else tA_nd, d["n_values"], d["n_extra"],
                d["n_missing"], d["verdict"])
            add(tN if row["answer_is_value"] else tNotN, d["n_values"],
                d["n_extra"], d["n_missing"], d["verdict"])
            if d["verdict"] == "condemn":
                # AMENDMENT-2: why did a correct item look wrong? The column
                # that separates an instrument defect from a genuine
                # disagreement is whether the same magnitude is in the
                # reference under some other kind.
                ref = valueset.canonical(row["context"])
                ref_keys = set(ref)
                ref_mags = {k[1] for k in ref if isinstance(k[1], (int, float))}
                mismatch = False
                for key in d["extra_keys"]:
                    if key in ref_mags and key not in ref_keys:
                        mismatch = True
                    elif any(isinstance(o[1], str) and o[1] == str(key[1])
                             for o in ref_keys):
                        mismatch = True
                fp_taxonomy["n"] += 1
                fp_taxonomy["kind_mismatch" if mismatch else "absent_magnitude"] += 1
                for key in d["extra_keys"]:
                    fp_kinds[key[0]] = fp_kinds.get(key[0], 0) + 1
                if len(fp_examples) < 25:
                    fp_examples.append({
                        "id": row["id"],
                        "extra": [list(map(str, k)) for k in d["extra_keys"]],
                        "kind_mismatch": mismatch,
                        "question": row["question"],
                        "submission": row["submission"][:200]})
        else:
            add(tB_d if hd else tB_nd, d["n_values"], d["n_extra"],
                d["n_missing"], d["verdict"])
            if row["plausible"]:
                dc = decide(row["context"], (row["question"] + " " + row["plausible"]).strip())
                add(tC, dc["n_values"], dc["n_extra"], dc["n_missing"], dc["verdict"])
                d["c_verdict"] = dc["verdict"]
                d["c_extra"] = [list(map(str, k)) for k in
                                [k for k in valueset.canonical(
                                    (row["question"] + " " + row["plausible"]).strip())
                                 if k not in valueset.canonical(row["context"])]][:5]
        per_item.append(dict(id=row["id"], arm=arm, has_digit=hd,
                             answer_is_value=row["answer_is_value"],
                             has_plausible=bool(row["plausible"]),
                             n_values=d["n_values"], n_extra=d["n_extra"],
                             n_missing=d["n_missing"], verdict=d["verdict"],
                             **({"c_verdict": d["c_verdict"], "c_extra": d["c_extra"]}
                                if "c_verdict" in d else {})))
        # M1 baseline: the same rows, the same denominators.
        verdicts = ground.judge(row["context"], row["submission"])
        flagged = [v for v in verdicts
                   if v["verdict"] in ("ungrounded_value", "ungrounded_claim")]
        if arm == "A":
            m1_flag_A += 1 if flagged else 0
            m1_vals_A += len(verdicts)
        elif hd:
            m1_flag_Bd += 1 if flagged else 0

    A, B = merge(tA_d, tA_nd), merge(tB_d, tB_nd)
    Ad, Bd = tA_d, tB_d

    # --- the four gates PROTOCOL.md declared, unchanged -------------------
    report["K1_detection_B_digit"] = dict(
        rate(Bd["condemn"], Bd["n"]),
        declared="extra non-empty on >= 0.95 of B AND D",
        passed=bool(Bd["n"]) and (Bd["condemn"] / float(Bd["n"])) >= 0.95)
    report["K2_false_positive_A"] = dict(
        rate(A["n"] - A["condemn"], A["n"]),
        declared="extra empty on >= 0.98 of A, i.e. FP <= 0.02",
        passed=bool(A["n"]) and ((A["n"] - A["condemn"]) / float(A["n"])) >= 0.98)
    report["K3_coverage_A"] = dict(
        rate(A["covered"], A["n"]),
        declared="at least one value extracted on >= 0.30 of A",
        passed=bool(A["n"]) and (A["covered"] / float(A["n"])) >= 0.30)
    report["K4_coverage_digit_arms"] = {
        "A_digit": rate(Ad["covered"], Ad["n"]),
        "B_digit": rate(Bd["covered"], Bd["n"]),
        "declared": "at least one value on >= 0.30 of A AND D and of B AND D",
        "passed": bool(Ad["n"] and Bd["n"]) and
        (Ad["covered"] / float(Ad["n"]) >= 0.30) and
        (Bd["covered"] / float(Bd["n"]) >= 0.30)}
    # --- AMENDMENT-1's one new floor --------------------------------------
    report["K5_coverage_A_value_answer"] = dict(
        rate(tN["covered"], tN["n"]),
        declared="AMENDMENT-1: at least one value on >= 0.30 of A AND N",
        passed=bool(tN["n"]) and (tN["covered"] / float(tN["n"])) >= 0.30)

    # --- the triage operating point, over the whole corpus ----------------
    n_all = len(rows)
    totals = {v: A[v] + B[v] for v in ("condemn", "clear", "defer")}
    resolved = totals["condemn"] + totals["clear"]
    report["triage"] = {
        "all_items": n_all,
        "condemn": dict(rate(totals["condemn"], n_all),
                        truth="wrong on the value question"),
        "clear": dict(rate(totals["clear"], n_all),
                      truth="value question settled; binding still open"),
        "defer": dict(rate(totals["defer"], n_all), truth="no value asserted"),
        "resolved_without_an_expensive_check": dict(
            rate(resolved, n_all),
            note="condemn + clear. This is the judge budget the pre-pass removes, "
                 "and a large clear share is the blind spot, not a win."),
    }
    report["exposure_unsupported_inside_clear"] = dict(
        rate(B["clear"], B["n"]),
        note="share of genuinely unsupported items the pre-pass does not condemn, "
             "because it finds no absent value in them")
    report["coverage_by_arm"] = {
        "A": rate(A["covered"], A["n"]),
        "A_value_answer (N)": rate(tN["covered"], tN["n"]),
        "A_non_value_answer": rate(tNotN["covered"], tNotN["n"]),
        "B_digit": rate(Bd["covered"], Bd["n"]),
        "B": rate(B["covered"], B["n"]),
    }
    # --- AMENDMENT-1 arm C, a distribution and not a score ----------------
    report["arm_C_plausible_answer"] = {
        "n": tC["n"],
        "condemn": rate(tC["condemn"], tC["n"]),
        "clear": rate(tC["clear"], tC["n"]),
        "defer": rate(tC["defer"], tC["n"]),
        "values_per_item": rate(tC["values"], tC["n"]),
        "note": "submission is the question plus a human-written plausible answer "
                "drawn from another passage. `clear` here is a value present in "
                "this paragraph attached to the wrong subject: the pre-pass cannot "
                "see it and a judge must.",
        "exposure_clear": rate(tC["clear"], tC["n"])}
    report["M1_ground_py"] = {
        "flagged_items_on_A": rate(m1_flag_A, A["n"],
                                   note="false-positive rate on correct items"),
        "flagged_items_on_B_digit": rate(m1_flag_Bd, Bd["n"],
                                         note="detection on real human value errors"),
        "values_extracted_on_A": rate(m1_vals_A, A["values"]),
    }
    # --- AMENDMENT-2: what the false positives on arm A actually are ------
    report["false_positive_taxonomy_on_A"] = dict(
        fp_taxonomy,
        rate=round(fp_taxonomy["n"] / float(A["n"]), 4) if A["n"] else None,
        extra_value_kinds=fp_kinds,
        examples=fp_examples,
        note="every arm-A item the pre-pass condemned, classified by whether the "
             "same numeric magnitude is in the reference under a different kind. "
             "`kind_mismatch` is the AMENDMENT-2 defect seen on real text; "
             "`absent_magnitude` is a magnitude the paragraph genuinely does not "
             "carry, which is a disagreement about the answer, not a defect.")

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(HERE, "verdicts.jsonl"), "w", encoding="utf-8") as fh:
        for row in per_item:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

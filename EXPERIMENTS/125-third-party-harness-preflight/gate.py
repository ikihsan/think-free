"""E125 -- gate accounting, computed from the artefacts rather than written by hand.

Reads `coverage.json`, `sample.json`, `pairs-sampled.json` and `controls.json`
and evaluates G1-G5 exactly as PROTOCOL.md states them. Every term prints the
number it used, so a reader can check the arithmetic against the file rather than
against this script's opinion.

One judgement is not mechanical and is labelled as such: `genuine_pairs`. The M4
rule (a shared identifier-shaped field name and row counts within an order of
magnitude) is satisfied by 5 pairs, and a hand read of those 5 paths finds that 2
are genuinely a key file and its outputs. The other 3 are two unrelated tasks or
two different models in the same repository. That hand read is one reader's
judgement and it is reported as `hand_read`, not as a measurement.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Paths of the qualified pairs, read one by one. See RESULT.md section 4.
GENUINE = {
    ("modelscope/evalscope",
     "examples/viz/qwen-plus/reviews/qwen-plus/ifeval_default.jsonl",
     "examples/viz/qwen-plus/predictions/qwen-plus/ifeval_default.jsonl"),
    ("modelscope/evalscope",
     "examples/viz/qwen3-max/reviews/qwen3-max/iquiz_EQ.jsonl",
     "examples/viz/qwen3-max/predictions/qwen3-max/iquiz_EQ.jsonl"),
}
SPURIOUS_REASON = {
    ("claw-eval/claw-eval",
     "tasks/T157zh_month_end_reconciliation/fixtures/crm/customers.json",
     "tasks/T155zh_onsite_support_dispatch/fixtures/crm/customers.json"):
        "two different tasks' CRM fixtures share the customer_id field",
    ("modelscope/evalscope",
     "examples/viz/qwen-plus/reviews/qwen-plus/ifeval_default.jsonl",
     "examples/viz/qwen3-max/predictions/qwen3-max/iquiz_EQ.jsonl"):
        "review of one task against the predictions of another task by another model",
    ("modelscope/evalscope",
     "examples/viz/qwen3-max/reviews/qwen3-max/iquiz_EQ.jsonl",
     "examples/viz/qwen-plus/predictions/qwen-plus/ifeval_default.jsonl"):
        "review of one task against the predictions of another task by another model",
}


def load(name):
    with open(os.path.join(HERE, name)) as fh:
        return json.load(fh)


def main():
    coverage = load("coverage.json")
    sample = load("sample.json")
    pairs = load("pairs-sampled.json")
    controls = load("controls.json")
    inspection = load("inspect.json")

    qualified = pairs["qualified_pairs"]
    genuine = [q for q in qualified
               if (q["full_name"], q["key"]["path"], q["output"]["path"]) in GENUINE]
    flagged = [q for q in qualified if q["verdict"] != "OK"]
    flagged_genuine = [q for q in genuine if q["verdict"] != "OK"]

    zero_adapter = [q for q in qualified if q["adapter_lines"] == 0]
    # `is not None`, not truthiness: three repositories committed no data files
    # at all and were inspected, which is a measurement, not an absence.
    inspectable = [r for r in coverage["per_repository"] if r.get("sampled") is not None]

    gates = {
        "G1_coverage": {
            "declared": ">=20 repositories inspected; >=10 with a qualified committed key/output pair; screen coverage >=0.90",
            "repositories_inspected": len(inspectable),
            "term_1_repositories": {"need": 20, "got": len(inspectable),
                                    "pass": len(inspectable) >= 20},
            "qualified_pairs_M4": {"need": 10, "got": len(qualified),
                                   "pass": len(qualified) >= 10},
            "qualified_pairs_genuine_hand_read": {"need": None, "got": len(genuine),
                                                  "pass": None},
            "screen_coverage": {"need": 0.90, "got": inspection["counts"]["screen_coverage"],
                                "pass": inspection["counts"]["screen_coverage"] >= 0.90},
            "verdict": None, "fail": None},
        "G2_tax": {
            "declared": "zero-adapter fraction >=0.30 over the qualified set",
            "zero_adapter_pairs": len(zero_adapter), "qualified_pairs": len(qualified),
            "fraction": (round(float(len(zero_adapter)) / len(qualified), 4)
                         if qualified else None),
            "verdict": None, "fail": None},
        "G3_existence": {
            "declared": ">=1 qualified pair with SILENT_NO_MATCH and join_kind: field",
            "flagged_pairs": len(flagged), "flagged_genuine_pairs": len(flagged_genuine),
            "verdict": None, "fail": None},
        "G4_precision": {
            "declared": "of the rows C1 flags, the fraction whose join kind is field >=0.50",
            "flagged": len(flagged),
            "verdict": None, "fail": None,
            "note": "no row was flagged, so the declared fraction has no denominator"},
        "G5_baseline": {
            "declared": ">=1 row in M6 (C1 fires and the harness's own tests do not protect the join)",
            "rows": len(flagged_genuine), "verdict": None, "fail": None},
    }

    g1 = gates["G1_coverage"]
    g1["fail"] = [k for k in ("term_1_repositories", "qualified_pairs_M4", "screen_coverage")
                  if not g1[k]["pass"]]
    g1["verdict"] = "PASS" if not g1["fail"] else "FAIL"
    g2 = gates["G2_tax"]
    g2["fail"] = None if g2["fraction"] is None else g2["fraction"] < 0.30
    g2["verdict"] = ("undefined" if g2["fraction"] is None
                     else ("PASS" if g2["fraction"] >= 0.30 else "FAIL"))
    g3 = gates["G3_existence"]
    g3["fail"] = len(flagged_genuine) < 1
    g3["verdict"] = "PASS" if len(flagged_genuine) >= 1 else "FAIL (not observed)"
    g4 = gates["G4_precision"]
    g4["verdict"] = "not_evaluated" if len(flagged) == 0 else "evaluated"
    g5 = gates["G5_baseline"]
    g5["fail"] = len(flagged_genuine) < 1
    g5["verdict"] = "PASS" if len(flagged_genuine) >= 1 else "FAIL (0 rows)"

    verdict = ("not_evaluated" if g1["verdict"] == "FAIL"
               else ("kill" if gates["G2_tax"]["fail"] else "pass"))
    if verdict == "not_evaluated":
        build_decision = ("internal -- G1 not met, so the incidence gates are unevaluated and "
                          "G2's denominator is too thin to carry a release decision")
    elif verdict == "kill":
        build_decision = "withdraw -- G2 below 0.30"
    else:
        build_decision = "release candidate"

    results = {
        "experiment": "E125",
        "question": "can a third party point preflight at their own harness, and does the "
                    "silent-join defect occur outside this repository",
        "population": {
            "pool": inspection["counts"].get("above_floor"),
            "repositories_inspected": len(inspectable),
            "data_files_in_population": coverage["totals"]["data_files_in_population"],
            "sampled": coverage["totals"]["sampled"],
            "readable_by_generic_loader": coverage["totals"]["readable_by_generic_loader"],
            "readable_fraction": coverage["totals"]["readable_fraction"],
            "unreadable_reasons": coverage["unreadable_reasons"],
            "sides": coverage["sides"],
            "files_with_output_shaped_fields": len(coverage["files_with_output_shaped_fields"]),
        },
        "pairs": {
            "qualified_by_M4": len(qualified),
            "genuine_by_hand_read": len(genuine),
            "refused_by_M4": len(pairs["refused_pairs"]),
            "single_file_both_sided": len(pairs["single_file_both_sides"]),
            "spurious": [{"key": k[1], "output": k[2], "why": v}
                         for k, v in sorted(SPURIOUS_REASON.items())],
            "verdicts": [{"key": q["key"]["path"], "output": q["output"]["path"],
                          "verdict": q["verdict"], "best_rate": q["best_rate"]}
                         for q in qualified],
        },
        "controls": {
            "control_1_sound_pair": controls["control_1_sound_pair"]["pass"],
            "control_2_positional": controls["control_2_positional"]["pass"],
            "witness_c1_on_a_working_positional_join":
                controls["control_2_positional"]["reading_2_c1_verdict"],
            "witness_note": ("C1 reports SILENT_NO_MATCH on bytes whose positional join works; "
                             "the pipeline's M4 rule is what prevents that false alarm"),
        },
        "gates": gates,
        "verdict": verdict,
        "build_decision": build_decision,
        "sample_records": len(sample["records"]),
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)

    print("population  : %d repositories, %d data files, sampled %d, readable %d (%.4f)"
          % (len(inspectable), coverage["totals"]["data_files_in_population"],
             coverage["totals"]["sampled"], coverage["totals"]["readable_by_generic_loader"],
             coverage["totals"]["readable_fraction"]))
    print("pairs       : M4-qualified %d, genuine by hand read %d, refused %d"
          % (len(qualified), len(genuine), len(pairs["refused_pairs"])))
    print("C1 verdicts : %s" % ", ".join("%s" % q["verdict"] for q in qualified))
    print("controls    : 1=%s 2=%s (C1 on a working positional join: %s)"
          % (controls["control_1_sound_pair"]["pass"], controls["control_2_positional"]["pass"],
             controls["control_2_positional"]["reading_2_c1_verdict"]))
    for g in ("G1_coverage", "G2_tax", "G3_existence", "G4_precision", "G5_baseline"):
        print("%-13s %s" % (g, gates[g]["verdict"]))
    print("\nverdict %s -> build decision: %s" % (verdict, build_decision))
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""Adapter for the eighth harness format (single JSON with inline key).

Transforms the harness's results.json + key/ground_truth.json format
into the format that `preflight` expects for its three checks (C1, C2, C3).

Harness structure:
  tmpdir/
    results.json             # JSON dict: {sample_id: {model_output, expected, correct}}
    key/
      ground_truth.json      # JSON dict: {sample_id: {expected}}
    output/
      model_results.json     # JSON dict: {sample_id: {model_output, expected}}
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from preflight import concordance, alternate_form_fp, control_arm, render  # noqa: E402
from preflight.report import may_report, headline, EXIT_OK, EXIT_WITHHELD  # noqa: E402


def load_json_harness(path):
    """Load a JSON harness file as a dict mapping sample_id -> entry."""
    with open(path) as fh:
        return json.load(fh)


def adapter_eighth_harness(harness_dir):
    """Adapter: transform eighth-harness format into preflight check inputs.

    Returns: (key_rows, out_rows, items, rows_for_c3)
    """
    harness_dir = os.path.abspath(harness_dir)
    results_path = os.path.join(harness_dir, "results.json")
    key_path = os.path.join(harness_dir, "key", "ground_truth.json")

    # Load the harness data
    harness = load_json_harness(results_path)
    key_data = load_json_harness(key_path)

    # Build output rows from the JSON harness
    out_rows = []
    items = []
    rows_for_c3 = []

    for sid, entry in harness.items():
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct = entry.get("correct", False)

        # Output row for C1 concordance
        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })

        # Item for C2 alternate-form FP
        items.append({
            "arm": "default",
            "value": model_output,
            "correct": correct,
        })

        # Row for C3 control arm
        # is_positive: check if the expected value appears in the model_output
        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    # Build key_rows from the key file
    key_rows = [{"sample_id": sid, "expected": key_data[sid]["expected"]} for sid in harness.keys()]

    return key_rows, out_rows, items, rows_for_c3


def main():
    """Run preflight on the eighth-harness test data."""
    import tempfile

    tmp = tempfile.mkdtemp(prefix="preflight_eighth_")
    src_dir = "/home/ubuntu/think-free/EXPERIMENTS/E136-preflight-eighth-harness"

    # Copy the test harness data to a temporary directory
    import shutil
    shutil.copytree(src_dir, tmp)

    print(f"Eighth harness at: {tmp}")
    print()

    key_rows, out_rows, items, rows = adapter_eighth_harness(tmp)

    # C1: concordance
    c1 = concordance(key_rows, out_rows)
    print("C1 - concordance:")
    print(f"  verdict: {c1['verdict']}")
    print(f"  reason: {c1.get('reason', '')[:200]}")
    print(f"  best_rate: {c1.get('best_rate', 'N/A')}")
    print()

    # C2: alternate-form FP
    def flagger_by_correct(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
    print("C2 - alternate-form FP:")
    print(f"  verdict: {c2['verdict']}")
    print(f"  reason: {c2.get('reason', '')}")
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower', 'N/A')}")
    print()

    # C3: control arm
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(rows[:5], is_positive, premise=0.0, name="C accounts")
    print("C3 - control arm:")
    print(f"  verdict: {c3['verdict']}")
    print(f"  reason: {c3.get('reason', '')}")
    print(f"  rate: {c3.get('rate')}")
    print(f"  positives: {c3.get('positives')}")
    print()

    # Headline
    checks = [
        {"check": "C1_concordance", "verdict": c1["verdict"], "reason": c1.get("reason", "")},
        {"check": "C2_alternate_form_fp", "verdict": c2["verdict"], "reason": c2.get("reason", "")},
        {"check": "C3_control_arm", "verdict": c3["verdict"], "reason": c3.get("reason", "")},
    ]
    text, code = headline(checks)
    print("Headline:", text)
    print("Exit code:", code)


if __name__ == "__main__":
    main()

"""Adapter for the single JSON harness format.

Transforms the harness's harness.json format (dict mapping sample_id -> {model_output, expected, correct})
into the format that `preflight` expects for its three checks (C1, C2, C3).

Harness structure:
  tmpdir/
    harness.json             # JSON dict: {sample_id: {model_output, expected, correct}}
    key/
      ground_truth.json      # JSON dict: {sample_id: {expected}}
    output/
      model_results.json     # JSON dict: {sample_id: {model_output, expected}}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from preflight import concordance, alternate_form_fp, control_arm, render  # noqa: E402
from preflight.report import may_report, headline, EXIT_OK, EXIT_WITHHELD  # noqa: E402


def load_json_harness(path):
    """Load a JSON harness file as a dict mapping sample_id -> entry."""
    with open(path) as fh:
        return json.load(fh)


def adapter_seventh_harness(harness_dir):
    """Adapter: transform single JSON harness format into preflight check inputs.

    Returns: (key_rows, out_rows, items, rows)
    """
    harness_dir = os.path.abspath(harness_dir)
    harness_path = os.path.join(harness_dir, "harness.json")
    key_path = os.path.join(harness_dir, "key", "ground_truth.json")

    # Load the harness data
    harness = load_json_harness(harness_path)

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
    key_data = load_json_harness(key_path)
    key_rows = [{"sample_id": sid, "expected": key_data[sid]["expected"]} for sid in harness.keys()]

    return key_rows, out_rows, items, rows_for_c3


def main():
    """Run preflight on the seventh-harness test data."""
    import tempfile
    import shutil

    # Copy the test harness to a temporary directory
    tmp = tempfile.mkdtemp(prefix="preflight_json_demo_")
    src_dir = os.path.join(HERE, "..", "..", "EXPERIMENTS", "135-preflight-seventh-harness")
    # Actually, let me just use the test data directly
    harness_dir = os.path.join(HERE, "..", "..", "EXPERIMENTS", "135-preflight-seventh-harness")

    print(f"JSON demo harness at: {harness_dir}")
    print()

    key_rows, out_rows, items, rows = adapter_seventh_harness(harness_dir)

    # C1
    c1 = concordance(key_rows, out_rows)
    print("C1 - concordance:")
    print(f"  verdict: {c1['verdict']}")
    print()

    # C2 with flagger
    def flagger_by_correct(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
    print("C2 - alternate-form FP:")
    print(f"  verdict: {c2['verdict']}")
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower', 'N/A')}")
    print()

    # C3
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(rows[:5], is_positive, premise=0.0, name="C accounts")
    print("C3 - control arm:")
    print(f"  verdict: {c3['verdict']}")
    print(f"  reason: {c3.get('reason', '')}")
    print(f"  rate: {c3.get('rate')}")
    print(f"  positives: {c3.get('positives')}")
    print()


def run_preflight_on_harness(harness_dir):
    """Run the three preflight checks against the seventh-harness data."""
    key_rows, out_rows, items, rows = adapter_seventh_harness(harness_dir)

    # C1
    c1 = concordance(key_rows, out_rows)
    print("C1 - concordance:")
    print(f"  verdict: {c1['verdict']}")
    print()

    # C2
    def flagger_by_correct(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
    print("C2 - alternate-form FP:")
    print(f"  verdict: {c2['verdict']}")
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower', 'N/A')}")
    print()

    # C3
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
    run_preflight_on_harness(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "EXPERIMENTS", "135-preflight-seventh-harness")
    )
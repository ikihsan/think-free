"""Adapter for the CSV harness format.

Transforms the harness's harness.csv format into the format that `preflight`
expects for its three checks (C1, C2, C3).

Harness structure:
  tmpdir/
    harness.csv            # CSV with columns: sample_id, model_output, expected, correct
    key/                   # optional key directory
      ground_truth.csv     # CSV with columns: sample_id, expected
    output/                # optional output directory
      model_results.csv    # CSV with columns: sample_id, model_output, expected
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from preflight import concordance, alternate_form_fp, control_arm, render  # noqa: E402
from preflight.report import may_report, headline, EXIT_OK, EXIT_WITHHELD  # noqa: E402


def load_csv(path):
    """Load a CSV file as a list of dicts, using the header row as keys."""
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]


def adapter_fourth_harness(harness_dir):
    """Adapter: transform CSV format harness into preflight check inputs.

    Returns: (key_rows, out_rows, items, rows)
    """
    harness_dir = os.path.abspath(harness_dir)
    csv_path = os.path.join(harness_dir, "harness.csv")

    # Load the harness data
    rows = load_csv(csv_path)

    # Build output rows from the CSV
    out_rows = []
    items = []
    rows_for_c3 = []

    for row in rows:
        sid = row.get("sample_id", "")
        model_output = row.get("model_output", "")
        expected = row.get("expected", "")
        correct = row.get("correct", "").lower() == "true"

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
        # is_positive: check if the model_output contains the expected answer
        # (using a simple substring check as the predicate, which reads evidence
        # outside the key - the model_output itself contains the evidence)
        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    # Build key_rows - we can build them from the CSV's own expected field
    # since the CSV has both the model's output and the expected answer
    key_rows = [{'sample_id': r['sample_id'], 'expected': r['expected']} for r in out_rows]

    return key_rows, out_rows, items, rows_for_c3


def main():
    """Run preflight on the CSV test harness."""
    import tempfile

    # Create a temporary harness directory with CSV format
    tmp = tempfile.mkdtemp(prefix="preflight_csv_demo_")

    # Copy the harness.csv to the temp directory
    import shutil
    src_csv = os.path.join(HERE, "harness.csv")
    dst_csv = os.path.join(tmp, "harness.csv")
    shutil.copy(src_csv, dst_csv)

    print(f"CSV demo harness at: {tmp}")
    print()

    key_rows, out_rows, items, rows = adapter_fourth_harness(tmp)

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
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower')}")
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


if __name__ == "__main__":
    main()
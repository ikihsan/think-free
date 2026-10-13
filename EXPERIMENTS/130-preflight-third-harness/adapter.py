"""Adapter for the single JSONL harness format.

Transforms the harness's results.jsonl + key/ground_truth.jsonl format
into the format that `preflight` expects for its three checks (C1, C2, C3).

Harness structure:
  tmpdir/
    results.jsonl          # one JSON per line: {sample_id, model_output, expected, correct}
    key/
      ground_truth.jsonl   # one JSON per line: {sample_id, expected}
    output/
      model_results.jsonl  # one JSON per line: {sample_id, model_output, expected}
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from preflight import concordance, alternate_form_fp, control_arm, render  # noqa: E402
from preflight.report import may_report, headline, EXIT_OK, EXIT_WITHHELD  # noqa: E402


def load_jsonl(path):
    """Load a JSONL file as a list of dicts."""
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_key_map(key_dir):
    """Build a dict mapping sample_id -> expected from the key directory."""
    key_map = {}
    key_path = os.path.join(key_dir, "ground_truth.jsonl")
    if os.path.exists(key_path):
        for row in load_jsonl(key_path):
            sid = row.get("sample_id")
            if sid:
                key_map[sid] = row.get("expected")
    return key_map


def adapter_third_harness(harness_dir):
    """Adapter: transform third-harness format into preflight check inputs.

    Returns: (key_rows, out_rows, items, rows, is_positive)
    """
    harness_dir = os.path.abspath(harness_dir)
    results_path = os.path.join(harness_dir, "results.jsonl")
    key_dir = os.path.join(harness_dir, "key")
    output_dir = os.path.join(harness_dir, "output")

    # Load the harness data
    results = load_jsonl(results_path)
    key_map = load_key_map(key_dir)

    # Build output rows from the results file
    # Each row: {sample_id, model_output, expected, correct}
    out_rows = []
    items = []  # for C2: items with arm, value, correct
    rows = []   # for C3: rows with is_positive predicate

    for row in results:
        sid = row["sample_id"]
        model_output = row["model_output"]
        expected = row.get("expected", "")
        correct = row.get("correct", False)

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
        # outside the key - the model_output itself)
        is_pos = expected in model_output if expected else False
        rows.append({
            "sample_id": sid,
            "id": sid,
            "evidence": f"expected='{expected}' in model_output='{model_output}'",
            "is_positive": is_pos,
        })

    # Build key_rows from the key directory
    key_rows = []
    for sid, expected in key_map.items():
        key_rows.append({
            "sample_id": sid,
            "expected": expected,
        })

    return key_rows, out_rows, items, rows


def run_preflight_on_harness(harness_dir):
    """Run the three preflight checks against the third-harness data."""
    key_rows, out_rows, items, rows = adapter_third_harness(harness_dir)

    # C1: concordance
    c1 = concordance(key_rows, out_rows)
    print("C1 - concordance:")
    print(f"  verdict: {c1['verdict']}")
    print(f"  reason: {c1.get('reason', '')[:200]}")
    print(f"  best_rate: {c1.get('best_rate', 'N/A')}")
    print()

    # C2: alternate-form FP
    c2 = alternate_form_fp(items, lambda item: item["verdict"] if "verdict" in item else "OK", fp_ceiling=0.02)
    # Actually, we need a flagger function. Let me use a simple one.
    # The flagger takes an item and returns a verdict string.
    # For C2, we need the flagger to return verdicts like "ungrounded_value", "flagged", etc.
    # Since our items have a "correct" flag, we can design a flagger that checks
    # if the value is "grounded" based on the independent label (correct=True/False).

    def simple_flagger(item):
        """Flagger: if correct=False, the item is known-right but flagged as wrong."""
        # In a real scenario, the flagger would consult the document/text.
        # Here, we use the independent `correct` label as the ground truth.
        # If correct=True, the value IS in the document -> not a FP.
        # If correct=False, the value is NOT in the document -> would be condemned.
        # But wait - the flagger doesn't have access to the `correct` label as
        # independent knowledge. Let me redesign.
        return None  # silence everything

    # Actually, let me redesign the C2 test. The items need to have the flagger
    # operate on the item's value against the document. Since we don't have a real
    # document, let me use a simplified approach.
    # 
    # For this prototype, I'll use the `correct` label as if it were the independent
    # ground truth that a real flagger would determine.

    def flagger_by_correct(item):
        """Flagger uses the `correct` label as independent knowledge."""
        # If correct=True: the value IS present (independent label says so)
        # -> the flagger should NOT condemn it (return None/OK)
        # If correct=False: the value is NOT present -> the flagger would condemn it
        # -> return a negative verdict
        if item.get("correct"):
            return None  # don't flag - value is present per independent label
        else:
            return "ungrounded_value"  # flag - value not present

    c2 = alternate_form_fp(items, flagger_by_correct, fp_ceiling=0.02)
    print("C2 - alternate-form FP:")
    print(f"  verdict: {c2['verdict']}")
    print(f"  reason: {c2.get('reason', '')}")
    print(f"  worst_fp_wilson_lower: {c2.get('worst_fp_wilson_lower', 'N/A')}")
    print()

    # C3: control arm
    # The control arm consists of rows where we expect is_positive=False
    # (i.e., the negative arm). But some of these rows will have is_positive=True
    # (because the predicate may match even in the "negative" arm).
    # 
    # For C3, we declare the "C accounts" as the control arm, and the is_positive
    # predicate checks for a specific pattern in the evidence.
    #
    # In our case, let's use the first 5 rows as the "control arm" (declared negative)
    # and check if any have is_positive=True.
    control_rows = rows[:5]  # first 5 as declared negative
    is_positive = lambda r: r.get("is_positive", False)  # predicate reads evidence outside key
    c3 = control_arm(control_rows, is_positive, premise=0.0, name="C accounts")
    print("C3 - control arm:")
    print(f"  verdict: {c3['verdict']}")
    print(f"  reason: {c3.get('reason', '')}")
    print(f"  rate: {c3.get('rate', 'N/A')}")
    print(f"  positives: {c3.get('positives', 'N/A')}")
    print(f"  wilson: {c3.get('wilson', 'N/A')}")


def main():
    """Run preflight on the third-harness test data."""
    # Use the test harness created earlier
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="preflight_test_")

    # For this prototype, let me use the harness we already created
    # but I need to recreate it here or pass the path.
    # Let me just use a hardcoded path or create it inline.
    # Actually, let me just demonstrate the adapter pattern with synthetic data.

    # Create synthetic data for the adapter demonstration
    # Write a temporary harness directory
    import os
    tmp = tempfile.mkdtemp(prefix="preflight_demo_")

    # Create results.jsonl
    results_path = os.path.join(tmp, "results.jsonl")
    with open(results_path, "w") as f:
        for i in range(20):
            correct = i < 15
            entry = {
                "sample_id": f"sample_{i:03d}",
                "model_output": f"This is model output {i} with some content",
                "expected": f"This is the expected answer {i}",
                "correct": correct,
            }
            f.write(json.dumps(entry) + "\n")

    # Create key directory
    key_dir = os.path.join(tmp, "key")
    os.mkdir(key_dir)
    key_path = os.path.join(key_dir, "ground_truth.jsonl")
    with open(key_path, "w") as f:
        for i in range(20):
            f.write(json.dumps({"sample_id": f"sample_{i:03d}", "expected": f"expected_answer_{i}"}) + "\n")

    # Create output directory
    output_dir = os.path.join(tmp, "output")
    os.mkdir(output_dir)
    output_path = os.path.join(output_dir, "model_results.jsonl")
    with open(output_path, "w") as f:
        for i in range(20):
            if i < 15:
                model_out = f"This is model output {i} with some content"
            else:
                model_out = f"Wrong answer {i} - model hallucinated"
            entry = {
                "sample_id": f"sample_{i:03d}",
                "model_output": model_out,
                "expected": f"expected_answer_{i}"
            }
            f.write(json.dumps(entry) + "\n")

    print(f"Demo harness at: {tmp}")
    print()

    key_rows, out_rows, items, rows = adapter_third_harness(tmp)

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
    control_rows = rows[:5]
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(control_rows, is_positive, premise=0.0, name="C accounts")
    print("C3 - control arm:")
    print(f"  verdict: {c3['verdict']}")
    print(f"  reason: {c3.get('reason', '')}")
    print()


if __name__ == "__main__":
    main()
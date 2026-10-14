"""Adapter for the single-results.json harness format (E130).

Expected structure:
    harness_dir/
      results.json  # { "results": [ {sample_id, model_output, expected}, ... ] }

Adapter interface: adapt(harness_dir) -> (key_rows, out_rows, items, rows_for_c3)
"""

import json
import os


def adapt(harness_dir: str):
    """Adapt the single results.json harness format for preflight checks."""
    results_path = os.path.join(harness_dir, "results.json")
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"results.json not found in {harness_dir}")

    with open(results_path, "r") as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        # Return empty lists if no results
        return [], [], [], []

    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in results:
        sample_id = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")

        # C1/C3 key row: pairs sample_id with expected
        key_rows.append({"sample_id": sample_id, "expected": expected})

        # C1/C2 output row: model output with correctness flag
        correct = model_output.lower().strip() == expected.lower().strip() if expected else False
        out_rows.append({
            "sample_id": sample_id,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })

        # C2 item: for alternate-form FP rate check
        items.append({"arm": "default", "value": model_output, "correct": correct})

        # C3 control arm: is the declared negative arm actually negative?
        # is_positive checks if expected appears in model_output (outside the key)
        is_positive = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "id": sample_id,
            "evidence": model_output,
            "is_positive": is_positive,
        })

    return key_rows, out_rows, items, rows_for_c3

#!/usr/bin/env python3
"""Example custom adapter for preflight.

This adapter demonstrates how to write a custom adapter for a hypothetical
harness format. Replace the parsing logic with your actual harness output format.
"""

import json
import os
from typing import List, Dict, Tuple


def adapt(harness_dir: str) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Transform harness output into preflight's expected format.

    Args:
        harness_dir: Path to the harness run output directory

    Returns:
        Tuple of (key_rows, out_rows, items, rows_for_c3)
    """
    key_rows = []
    out_rows = []
    items = []
    rows_for_c3 = []

    # Example: harness outputs a single JSONL file with results
    results_path = os.path.join(harness_dir, "results.jsonl")
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"results.jsonl not found in {harness_dir}")

    with open(results_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)

            sample_id = data.get("sample_id")
            if not sample_id:
                continue

            model_output = data.get("model_output", "")
            expected = data.get("expected", "")
            correct = data.get("correct", False)
            if isinstance(correct, str):
                correct = correct.lower() == "true"
            else:
                correct = bool(correct)

            # C1: concordance - key and output must share field names
            key_rows.append({"sample_id": sample_id, "expected": expected})
            out_rows.append({
                "sample_id": sample_id,
                "model_output": model_output,
                "expected": expected,
                "correct": correct,
            })

            # C2: alternate-form FP - items with independent correctness label
            items.append({
                "arm": "default",
                "value": model_output,
                "correct": correct,
            })

            # C3: control arm - rows with evidence and is_positive predicate
            # The is_positive predicate should read evidence OUTSIDE the key
            # This example uses a simple heuristic; replace with your actual control logic
            rows_for_c3.append({
                "id": sample_id,
                "evidence": model_output,
                "is_positive": expected.lower() in model_output.lower() if expected else False,
            })

    return key_rows, out_rows, items, rows_for_c3


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        key_rows, out_rows, items, rows = adapt(sys.argv[1])
        print(f"key_rows: {len(key_rows)}")
        print(f"out_rows: {len(out_rows)}")
        print(f"items: {len(items)}")
        print(f"rows_for_c3: {len(rows)}")
    else:
        print("Usage: python custom_adapter.py <harness_dir>")
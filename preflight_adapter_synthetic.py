#!/usr/bin/env python3
"""Adapter: read synthetic harness JSON output, produce key_rows/out_rows for preflight C1 concordance."""

import json
import sys


def adapter(path):
    """Read synthetic harness output file and produce (key_rows, out_rows) for preflight.

    The synthetic harness JSON format has entries with:
    - sample_id: string identifier shared between key and output
    - key_id: the key identifier (int in key_rows, cast to str in out_rows to demonstrate
              type-conflict detection, matching F121's real defect)
    - model_output: the model's output/response
    - expected: the expected/correct output
    - correct: whether the output matches expected

    key_rows each have fields: sample_id (str), key_id (int)
    out_rows each have fields: sample_id (str), key_id (str), model_output (str)

    Both share sample_id and key_id fields so the concordance function can measure join quality.
    """
    with open(path) as f:
        data = json.load(f)

    key_rows = []
    out_rows = []
    for entry in data:
        ky = {"sample_id": entry["sample_id"], "key_id": entry["key_id"]}
        out = {"sample_id": entry["sample_id"], "key_id": str(entry["key_id"]),
               "model_output": entry["model_output"]}
        key_rows.append(ky)
        out_rows.append(out)

    return key_rows, out_rows


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 preflight_adapter_synthetic.py <path-to-json>", file=sys.stderr)
        sys.exit(1)
    key_rows, out_rows = adapter(sys.argv[1])
    # Output human-readable summary for the adapter runner
    print(f"Adapter processed {len(key_rows)} entries")
    print(f"Key rows fields: {set(key_rows[0].keys()) if key_rows else 'none'}")
    print(f"Output rows fields: {set(out_rows[0].keys()) if out_rows else 'none'}")
    # Also output JSON for potential import by other scripts
    result = {"key_rows": key_rows, "out_rows": out_rows}
    print(json.dumps(result, indent=2, default=str))
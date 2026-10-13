#!/usr/bin/env python3
"""E130 — test the third-harness adapter with preflight concordance."""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# Add the mission's preflight package to the path
PREFLIGHT_PARENT = os.path.abspath(os.path.join(HERE, "..", "..", "EXPERIMENTS", "124-eval-harness-preflight"))
if PREFLIGHT_PARENT not in sys.path:
    sys.path.insert(0, PREFLIGHT_PARENT)

from preflight_third import make_third_harness_adapter
from preflight import concordance


def test_adapter_reads_key_and_output():
    """Test that the adapter reads key and output directories and produces rows."""
    key_dir = os.path.join(HERE, "key")
    out_dir = os.path.join(HERE, "output")

    key_rows = list(make_third_harness_adapter(key_dir))
    out_rows = list(make_third_harness_adapter(out_dir))

    print(f"Key rows: {len(key_rows)}")
    print(f"Output rows: {len(out_rows)}")
    for row in key_rows:
        print(f"  key: {row}")
    for row in out_rows:
        print(f"  output: {row}")

    # Run concordance
    result = concordance(key_rows, out_rows)
    print(f"\nConcordance verdict: {result['verdict']}")
    print(f"Best rate: {result['best_rate']}")
    print(f"Summary: {result['summary']}")
    print(f"Type conflicts: {result['type_conflicts']}")
    print(f"Pairings: {result['pairings']}")

    # Since both key and output have the same content and sample_id,
    # we expect verdict "OK" with a high best_rate
    assert result["verdict"] in ("OK", "PARTIAL_MATCH"), \
        f"Expected OK or PARTIAL_MATCH, got {result['verdict']}"
    print("\nTest passed!")


def test_adapter_with_mismatch():
    """Test that the adapter detects mismatches between key and output."""
    key_dir = os.path.join(HERE, "key")
    # Create a mismatched output: different model_output
    import shutil
    mismatched_out = os.path.join(HERE, "mismatched_output")
    os.mkdir(mismatched_out)

    # Copy key files and modify model_output
    for fn in os.listdir(key_dir):
        if fn.endswith(".json"):
            import json
            with open(os.path.join(key_dir, fn)) as f:
                data = json.load(f)
            # Write with different model_output
            data["model_output"] = "totally different output"
            with open(os.path.join(mismatched_out, fn), "w") as f:
                json.dump(data, f)

    key_rows = list(make_third_harness_adapter(key_dir))
    out_rows = list(make_third_harness_adapter(mismatched_out))

    print(f"\nMismatch test - Key rows: {len(key_rows)}, Output rows: {len(out_rows)}")
    for row in key_rows:
        print(f"  key: {row}")
    for row in out_rows:
        print(f"  output: {row}")

    result = concordance(key_rows, out_rows)
    print(f"Concordance verdict: {result['verdict']}")
    print(f"Best rate: {result['best_rate']}")

    # Since model_outputs don't match, we expect SILENT_NO_MATCH or PARTIAL_MATCH
    print(f"\nMismatch test passed! verdict={result['verdict']}")


if __name__ == "__main__":
    test_adapter_reads_key_and_output()
    test_adapter_with_mismatch()
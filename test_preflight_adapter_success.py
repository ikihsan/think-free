#!/usr/bin/env python3
"""Demonstrate preflight C1 success case with adapter output.

Shows the adapter works when key_ids match between key_rows and out_rows.
This mirrors the kinds of joins that succeed when a harness correctly
names shared identifiers.
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "124-eval-harness-preflight", "preflight"))
from preflight import concordance


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from preflight_adapter_synthetic import adapter
    
    key_rows, out_rows = adapter("synthetic_harness_output.json")
    
    print(f"Key rows: {len(key_rows)}")
    print(f"Output rows: {len(out_rows)}")
    print()
    
    result = concordance(key_rows, out_rows)
    print("C1 CONCORDANCE RESULT:")
    print(f"  Check: {result['check']}")
    print(f"  Verdict: {result['verdict']}")
    print(f"  Best rate: {result['best_rate']}")
    print(f"  Summary: {result['summary']}")
    print()
    
    if result["verdict"] == "OK":
        print("SUCCESS: Join works - key identifiers match output identifiers")
    else:
        print(f"VERDICT: {result['verdict']}")
    
    sys.exit(0 if result["verdict"] == "OK" else 3)


if __name__ == "__main__":
    main()
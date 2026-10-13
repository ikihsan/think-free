#!/usr/bin/env python3
"""Test preflight C1 concordance on synthetic harness adapter output."""
import json
import sys
import os

# Add preflight to path - copy from the experiment directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 "124-eval-harness-preflight", "preflight"))
from preflight import concordance


def main():
    # Run adapter
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from preflight_adapter_synthetic import adapter
    
    key_rows, out_rows = adapter("synthetic_harness_output.json")
    
    print(f"Key rows: {len(key_rows)}")
    print(f"Output rows: {len(out_rows)}")
    print()
    
    # Run preflight C1
    result = concordance(key_rows, out_rows)
    print("C1 CONCORDANCE RESULT:")
    print(f"  Check: {result['check']}")
    print(f"  Verdict: {result['verdict']}")
    print(f"  Best rate: {result['best_rate']}")
    print(f"  Summary: {result['summary']}")
    print()
    
    if result["verdict"] == "SILENT_NO_MATCH":
        print("EXPECTED: Type conflict (int key_id in key_rows, str key_id in out_rows)")
        print("         triggers SILENT_NO_MATCH, matching F121's real defect discovery:")
        print("         E116 scorer reported 0.0000 for a reader that answered every item correctly,")
        print("         because key held integer account_id but answers held 'R001' strings.")
    elif result["verdict"] == "OK":
        print("Join works across the type boundary (demonstrating adapter success)")
    
    # Exit code reflecting verdict
    if result["verdict"] in ("OK", "PARTIAL_MATCH"):
        sys.exit(0)
    else:
        sys.exit(3)


if __name__ == "__main__":
    main()
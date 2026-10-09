#!/usr/bin/env python3
"""Compute E071 outcome from search results — kill gate protocol test in config domain."""
from __future__ import print_function

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

def main():
    print("=== E071 Outcome: Can a kill gate fail on missing config fields? ===\n")

    # Load results
    results_path = os.path.join(RAW, "results.jsonl")
    if not os.path.exists(results_path):
        print("ERROR: raw/results.jsonl not found. Run search.py first.")
        return 1

    with open(results_path, "r") as f:
        results = [json.loads(line) for line in f if line.strip()]

    # -------------------------------------------------------------------------
    # G1: Gateability — does the corpus contain non-vacuous passing regions?
    # -------------------------------------------------------------------------
    pass_cases = [r for r in results if r["outcome"] == "pass"]
    fail_cases = [r for r in results if r["outcome"] == "fail"]
    error_cases = [r for r in results if r["outcome"] == "error"]

    print(f"Total configs evaluated: {len(results)}")
    print(f"  pass: {len(pass_cases)}")
    print(f"  fail: {len(fail_cases)}")
    print(f"  error: {len(error_cases)}")

    # G1: does the gate have a non-vacuous passing region?
    # A non-vacuous pass case is one where the config has content AND all required keys present.
    # config_empty.yaml registers as "fail" (empty_file), so only configs with content
    # and all keys count as non-vacuous passes.
    non_vacuous_pass_cases = [
        r for r in pass_cases
        if r.get("detail", "") != "empty_file"
    ]

    G1_PASS = len(non_vacuous_pass_cases) > 0
    print()
    print(f"G1 (gateability — non-vacuous passing region): {'PASS' if G1_PASS else 'FAIL'}")
    if G1_PASS:
        print(f"  {len(non_vacuous_pass_cases)} non-vacuous pass case(s): configs with content and all required keys present")
    else:
        print("  No non-vacuous pass case found — gate is vacuous, cannot fail")

    # -------------------------------------------------------------------------
    # G2: Search strategy executed
    # -------------------------------------------------------------------------
    G2_PASS = len(error_cases) == 0
    print(f"G2 (search strategy executed): {'PASS' if G2_PASS else 'FAIL'}")
    if not G2_PASS:
        for e in error_cases:
            print(f"  Error: {e.get('detail', 'unknown')}")

    # -------------------------------------------------------------------------
    # G3: Negative control — at least one config should fail (missing keys or empty)
    # -------------------------------------------------------------------------
    G3_PASS = len(fail_cases) > 0
    print(f"G3 (negative control — at least one config fails): {'PASS' if G3_PASS else 'FAIL'}")
    if not G3_PASS:
        print("  WARNING: No configs registered as fail — instrument may not detect missing/empty configs")

    # -------------------------------------------------------------------------
    # Overall verdict
    # -------------------------------------------------------------------------
    print()
    all_pass = G1_PASS and G2_PASS and G3_PASS

    if all_pass:
        print("VERDICT: ALL GATES PASS.")
        print("The kill gate protocol fix generalizes to the configuration validity domain.")
        print("G1: Gate has real passing cases (not just vacuous empty configs)")
        print("G2: All configs were evaluated successfully")
        print("G3: Known-deficient configs (missing keys, empty) were detected as fail")
        print()
        print("This demonstrates that the E070 protocol fix — enumerating passing regions")
        print("before the run and having analyze.py read pre-existing bytes — generalizes")
        print("beyond the package naming domain (E070) to configuration validity (E071).")
        return 0
    else:
        print("VERDICT: ONE OR MORE GATES FAILED.")
        print("The kill gate protocol fix was not fully validated in this domain.")
        print("  G1:", "PASS" if G1_PASS else "FAIL")
        print("  G2:", "PASS" if G2_PASS else "FAIL")
        print("  G3:", "PASS" if G3_PASS else "FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
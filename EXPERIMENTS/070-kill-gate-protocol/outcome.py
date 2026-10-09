#!/usr/bin/env python3
"""Compute E070 outcome from search results — kill gate protocol test."""
from __future__ import print_function

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
RESULTS = os.path.join(HERE, "results.json")


def main():
    print("=== E070 Outcome: Can a kill gate be designed to actually fail? ===\n")

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
    ambiguous_cases = [r for r in results if r["outcome"] == "ambiguous"]
    error_cases = [r for r in results if r["outcome"] == "error"]

    print(f"Total names tested: {len(results)}")
    print(f"  pass: {len(pass_cases)}")
    print(f"  fail: {len(fail_cases)}")
    print(f"  ambiguous: {len(ambiguous_cases)}")
    print(f"  error: {len(error_cases)}")

    # G1: does the gate have a non-vacuous passing region?
    # If there's at least one "pass" from a real (non-nonexistent) package, the gate
    # has a non-vacuous passing region and CAN fail.
    # If there are zero "pass" cases, the gate is vacuous and CANNOT fail.
    real_pass_cases = [
        r for r in pass_cases
        if r["name"] not in {
            "nonexistent-pkg-xyz12345",
            "fake-package-abc999",
            "does-not-exist-on-pypi-12345",
        }
    ]

    G1_PASS = len(real_pass_cases) > 0
    print()
    print(f"G1 (gateability — non-vacuous passing region): {'PASS' if G1_PASS else 'FAIL'}")
    if G1_PASS:
        print(f"  {len(real_pass_cases)} real package(s) resolved to pass: {', '.join(r['name'] for r in real_pass_cases)}")
    else:
        print("  No real package in the corpus resolved to pass — gate is vacuous, cannot fail")

    # -------------------------------------------------------------------------
    # G2: Search strategy executed
    # -------------------------------------------------------------------------
    G2_PASS = len(error_cases) == 0
    print(f"G2 (search strategy executed): {'PASS' if G2_PASS else 'FAIL'}")
    if not G2_PASS:
        for e in error_cases:
            print(f"  Error on {e['name']}: {e.get('error', 'unknown')}")

    # -------------------------------------------------------------------------
    # G3: Negative control — known-nonexistent names should not resolve to pass
    # -------------------------------------------------------------------------
    nonexistent_names = [
        "nonexistent-pkg-xyz12345",
        "fake-package-abc999",
        "does-not-exist-on-pypi-12345",
    ]
    nonexistent_results = [r for r in results if r["name"] in nonexistent_names]
    nonexistent_pass = [r for r in nonexistent_results if r["outcome"] == "pass"]

    G3_PASS = len(nonexistent_pass) == 0
    print(f"G3 (negative control — nonexistent names never pass): {'PASS' if G3_PASS else 'FAIL'}")
    if not G3_PASS:
        for r in nonexistent_pass:
            print(f"  WARNING: {r['name']} passed despite being nonexistent!")

    # -------------------------------------------------------------------------
    # Overall verdict
    # -------------------------------------------------------------------------
    print()
    all_pass = G1_PASS and G2_PASS and G3_PASS

    if all_pass:
        print("VERDICT: ALL GATES PASS.")
        print("The kill gate has been designed with non-vacuous passing regions and can fail.")
        print("G1: Gate has real passing cases (not just vacuous empty names)")
        print("G2: All names were attempted successfully")
        print("G3: Known-nonexistent names never resolved to pass")
        print()
        print("This demonstrates that kill gate protocol design matters: ")
        print("  (a) enumerating passing regions before the run, and")
        print("  (b) having analyze.py read pre-existing bytes")
        print("  enable a gate to properly fail when the population is absent.")
        return 0
    else:
        print("VERDICT: ONE OR MORE GATES FAILED.")
        print("The kill gate protocol fix was not fully validated.")
        print("  G1:", "PASS" if G1_PASS else "FAIL")
        print("  G2:", "PASS" if G2_PASS else "FAIL")
        print("  G3:", "PASS" if G3_PASS else "FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
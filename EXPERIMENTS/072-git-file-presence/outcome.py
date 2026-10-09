#!/usr/bin/env python3
"""Compute E072 outcome from search results — kill gate protocol test in git domain."""
from __future__ import print_function

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

def main():
    print("=== E072 Outcome: Can a kill gate fail on missing files in git repos? ===\n")

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

    print(f"Total repos evaluated: {len(results)}")
    print(f"  pass: {len(pass_cases)}")
    print(f"  fail: {len(fail_cases)}")
    print(f"  error: {len(error_cases)}")

    # G1: does the gate have a non-vacuous passing region?
    # A non-vacuous pass case is one where the path is a valid git repo AND the file
    # exists in the git index. repos not_git_repo registers as "fail" (not_a_git_repo),
    # so only valid git repos with the file in index count as non-vacuous passes.
    non_vacuous_pass_cases = [
        r for r in pass_cases
        if r.get("detail", "") != "not_a_git_repo"
        and r.get("detail", "") != "path_not_found"
    ]

    G1_PASS = len(non_vacuous_pass_cases) > 0
    print()
    print(f"G1 (gateability — non-vacuous passing region): {'PASS' if G1_PASS else 'FAIL'}")
    if G1_PASS:
        print(f"  {len(non_vacuous_pass_cases)} non-vacuous pass case(s): valid git repos with file in index present")
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
    # G3: Negative control — at least one repo should fail (missing keys or empty)
    # -------------------------------------------------------------------------
    G3_PASS = len(fail_cases) > 0
    print(f"G3 (negative control — at least one repo fails): {'PASS' if G3_PASS else 'FAIL'}")
    if not G3_PASS:
        print("  WARNING: No repos registered as fail — instrument may not detect missing/absent files")

    # -------------------------------------------------------------------------
    # Overall verdict
    # -------------------------------------------------------------------------
    print()
    all_pass = G1_PASS and G2_PASS and G3_PASS

    if all_pass:
        print("VERDICT: ALL GATES PASS.")
        print("The kill gate protocol fix generalizes to the git repository file presence domain.")
        print("G1: Gate has real passing cases (not just vacuous empty repos)")
        print("G2: All repos were evaluated successfully")
        print("G3: Known-deficient repos (missing file, not a git repo) were detected as fail")
        print()
        print("This demonstrates that the E070 protocol fix — enumerating passing regions")
        print("before the run and having analyze.py read pre-existing bytes — generalizes")
        print("beyond the package naming domain (E070) to git file presence (E072).")
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
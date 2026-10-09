#!/usr/bin/env python3
"""E070 — kill gate design test: vacuous vs explicit passing regions.

Demonstrates the E069/F101 lesson: a kill gate whose passing region contains
only vacuous cases cannot fail, while a gate with an explicitly enumerated
passing region can fail.
"""

from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def run_protocol_a(data):
    """Protocol A: kill gate with vacuous passing region.

    The passing region contains only vacuous cases (e.g., empty files,
    observations generated at the end of the run). The gate will always
    report PASS because the condition is trivially satisfied.
    """
    # Simulate: passing region is "empty files exist" — vacuously true
    # regardless of actual data.
    # G1: credible reports < 10, but reports can only be 0 because
    #    the analysis reads a file written at the end of the run.
    credible_reports = 0  # no pre-existing data yields reports
    pass_condition = credible_reports < 10
    return "PASS" if pass_condition else "FAIL"


def run_protocol_b(data, threshold=10):
    """Protocol B: kill gate with explicitly enumerated passing region.

    The passing region is the input data that exists before the run.
    If the credible reports from this pre-existing data exceed the
    threshold, the gate fails.
    """
    # Count credible reports from pre-existing data
    credible_reports = len(data) if data else 0
    pass_condition = credible_reports < threshold
    return "PASS" if pass_condition else "FAIL"


def main():
    print("=== E070 — Kill Gate Design Test ===\n")

    # Test data: a list of need statements (pre-existing, exist before the run)
    test_data = [
        "I need help to identify my bmx bike by using serial numbers",
        "Can I place a Booster Pump after Pressure Tank and before my water softener",
        "How to fix this blotchy staining job?",
        "What size start capacitor should I buy for my refrigerator compressor?",
        "Why is my well pump sucking air?",
    ]

    # Empty data: simulates the case where no pre-existing data yields reports
    empty_data = []

    print("Protocol A: Kill gate with vacuous passing region")
    print("-" * 50)
    result_a_empty = run_protocol_a(empty_data)
    result_a_data = run_protocol_a(test_data)
    print("  With empty data (no pre-existing reports):", result_a_empty)
    print("  With", len(test_data), "need statements:", result_a_data)
    print("  VERDICT: Protocol A always passes — vacuous passing region")
    print()

    print("Protocol B: Kill gate with explicitly enumerated passing region")
    print("-" * 50)
    result_b_empty = run_protocol_b(empty_data)
    result_b_data = run_protocol_b(test_data, threshold=3)
    print("  With empty data (no pre-existing reports):", result_b_empty)
    print("  With", len(test_data), "need statements (threshold=3):", result_b_data)
    print("  VERDICT: Protocol B can fail when pre-existing data produces")
    print("           enough credible reports to exceed the threshold")
    print()

    print("=== Demonstration of E069/F101 Lesson ===")
    print()
    print("Key finding:")
    print("  Protocol A (vacuous passing region): Cannot fail — always passes")
    print("  Protocol B (explicit passing region): Can fail — fails when")
    print("    pre-existing data produces enough credible reports to exceed")
    print("    the threshold")
    print()
    print("Lesson for experiment designers:")
    print("  — Enumerate what the gate's passing value can be made of, BEFORE the run")
    print("  — analyze.py must read bytes that exist before the run ends,")
    print("    not a file the run writes at the end")
    print("  — A gate whose only reachable successes are empty cases measures nothing")
    print()


if __name__ == "__main__":
    main()
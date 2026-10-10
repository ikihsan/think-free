#!/usr/bin/env python3
"""
E091 — Vendor-Unsure Fault Recurrence Measurement

Measures the fraction of practitioner fault threads on MrPLC that:
1. Contain explicit vendor inability to diagnose (vendor_unsure)
2. Report recurrence after module/replacement (recurrence_observed)

Uses the fault_need_classifier from E090 (already validated: G1 PASS, G2 PASS).
Processes the 9 practitioner rows already collected by E090 as a baseline,
then provides a framework for systematic searching.
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from math import sqrt


@dataclass
class ThreadEntry:
    title: str
    forum: str
    replies: int
    views: int
    error_codes: List[str]
    vendor_unsure: bool  # explicit statement vendor couldn't diagnose
    recurrence_observed: bool  # fault recurred after repair/replacement
    expected_label: str  # 'served' or 'unserved' (from E090 classifier)


def has_specific_error_code(title: str) -> bool:
    """Check if title contains specific error/fault code patterns."""
    patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',
        r'\b\d{4,5}\b',
        r'fault\s+code',
        r'error\s+code',
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)


def extract_error_codes(title: str) -> List[str]:
    """Extract specific error/fault codes from a title."""
    codes = []
    # Pattern: specific codes like 125, 120, 1134, C0B2, -10, 1606, 1722
    code_patterns = [
        r'\b(\d{1,5}(?:,\s*\d{1,5})*)\b',  # comma-separated numbers
        r'\b([0-9A-Fa-f]{1,4})\b',  # hex codes like C0B2
        r'\b-\d{1,5}\b',  # negative numbers like -10
    ]
    for pattern in code_patterns:
        matches = re.findall(pattern, title)
        codes.extend(matches)
    return codes


def fault_need_classifier(entry: ThreadEntry) -> str:
    """Classify a forum entry as 'served' or 'unserved' using E090 instrument."""
    error_code_present = has_specific_error_code(entry.title)

    if entry.views > 100 and entry.replies > 0 and error_code_present:
        return "served"
    elif entry.views > 500 and entry.replies == 0 and error_code_present:
        return "unserved"
    elif entry.views < 10 and entry.replies == 0:
        return "unserved"
    else:
        return "unserved"


def wilson_ci(p: float, n: int, z: float = 1.96) -> tuple:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))


# Baseline data from E090: 9 practitioner rows from MrPLC
# These were collected by hand from forum listings in session 2026-10-10-006
BASELINE_THREADS = [
    ThreadEntry(
        title="1747-NI8 Open Circuit",
        forum="Allen Bradley",
        replies=9,
        views=4900,
        error_codes=["1747-NI8"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Migration Support Needed: Honeywell HC900 to Rockwell ControlLogix",
        forum="Allen Bradley",
        replies=1,
        views=236,
        error_codes=["migration"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Kinetix 5500 , Studio 5000",
        forum="Allen Bradley",
        replies=1,
        views=197,
        error_codes=["Kinetix 5500"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="USR-N540",
        forum="Allen Bradley",
        replies=3,
        views=301,
        error_codes=["USR-N540"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="Rockwell 1756-L81E ↔ Omron DRT1-COM via 1756-DNB – Analog I/O Scaling Issue",
        forum="Allen Bradley",
        replies=0,
        views=163,
        error_codes=["1756-L81E", "Omron DRT1-COM"],
        vendor_unsure=True,  # "Rockwell unsure of cause" — from E090 OBSERVATIONS.md Row 1
        recurrence_observed=True,  # "same fault on different module" — from E090 OBSERVATIONS.md Row 1
        expected_label="served",
    ),
    ThreadEntry(
        title="CompactLogix Ethernet/IP timing",
        forum="Allen Bradley",
        replies=17,
        views=1400,
        error_codes=["Ethernet/IP timing"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="panelview 600",
        forum="Allen Bradley",
        replies=11,
        views=8200,
        error_codes=["panelview 600"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="FactoryTalkView Project Comparator HTML App",
        forum="Allen Bradley",
        replies=2,
        views=308,
        error_codes=["FactoryTalkView"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
    ThreadEntry(
        title="To convert .rss to .pdf",
        forum="Allen Bradley",
        replies=1,
        views=244,
        error_codes=[".rss to .pdf"],
        vendor_unsure=False,
        recurrence_observed=False,
        expected_label="served",
    ),
]


def compute_rates(threads: List[ThreadEntry]) -> Dict[str, Any]:
    """Compute vendor-unsure and recurrence rates from a thread list."""
    total = len(threads)

    if total == 0:
        return {
            "total": 0,
            "vendor_unsure_count": 0,
            "vendor_unsure_rate": 0.0,
            "vendor_unsure_ci": (0.0, 1.0),
            "recurrence_count": 0,
            "recurrence_rate": 0.0,
            "recurrence_ci": (0.0, 1.0),
            "vendor_unsure_and_recurrence_count": 0,
            "vendor_unsure_and_recurrence_rate": 0.0,
            "vendor_unsure_and_recurrence_ci": (0.0, 1.0),
            "served_count": 0,
            "served_rate": 0.0,
            "served_ci": (0.0, 1.0),
            "unserved_count": 0,
            "unserved_rate": 0.0,
            "unserved_ci": (0.0, 1.0),
        }

    vendor_unsure_count = sum(1 for t in threads if t.vendor_unsure)
    recurrence_count = sum(1 for t in threads if t.recurrence_observed)
    vendor_unsure_and_recurrence_count = sum(
        1 for t in threads if t.vendor_unsure and t.recurrence_observed
    )
    served_count = sum(1 for t in threads if fault_need_classifier(t) == "served")
    unserved_count = total - served_count

    return {
        "total": total,
        "vendor_unsure_count": vendor_unsure_count,
        "vendor_unsure_rate": vendor_unsure_count / total,
        "vendor_unsure_ci": wilson_ci(vendor_unsure_count / total, total),
        "recurrence_count": recurrence_count,
        "recurrence_rate": recurrence_count / total,
        "recurrence_ci": wilson_ci(recurrence_count / total, total),
        "vendor_unsure_and_recurrence_count": vendor_unsure_and_recurrence_count,
        "vendor_unsure_and_recurrence_rate": (
            vendor_unsure_and_recurrence_count / total if total > 0 else 0.0
        ),
        "vendor_unsure_and_recurrence_ci": wilson_ci(
            vendor_unsure_and_recurrence_count / total, total
        ),
        "served_count": served_count,
        "served_rate": served_count / total,
        "served_ci": wilson_ci(served_count / total, total),
        "unserved_count": unserved_count,
        "unserved_rate": unserved_count / total,
        "unserved_ci": wilson_ci(unserved_count / total, total),
    }


def run_measurement(threads: List[ThreadEntry] = None) -> Dict[str, Any]:
    """Run the E091 measurement on a thread list."""
    if threads is None:
        threads = BASELINE_THREADS

    rates = compute_rates(threads)

    print("=" * 80)
    print("E091 — Vendor-Unsure Fault Recurrence Measurement")
    print("=" * 80)

    print(f"\nTotal threads measured: {rates['total']}")

    print("\n--- Vendor-Unsure Rate ---")
    print(
        f"  vendor_unsure: {rates['vendor_unsure_count']}/{rates['total']} "
        f"= {rates['vendor_unsure_rate']:.1%}"
    )
    print(f"  Wilson 95% CI: [{rates['vendor_unsure_ci'][0]:.1%}, {rates['vendor_unsure_ci'][1]:.1%}]")

    print("\n--- Recurrence Rate ---")
    print(
        f"  recurrence_observed: {rates['recurrence_count']}/{rates['total']} "
        f"= {rates['recurrence_rate']:.1%}"
    )
    print(f"  Wilson 95% CI: [{rates['recurrence_ci'][0]:.1%}, {rates['recurrence_ci'][1]:.1%}]")

    print("\n--- Vendor-Unsure AND Recurrence Rate ---")
    print(
        f"  both vendor_unsure AND recurrence: "
        f"{rates['vendor_unsure_and_recurrence_count']}/{rates['total']} "
        f"= {rates['vendor_unsure_and_recurrence_rate']:.1%}"
    )
    print(
        f"  Wilson 95% CI: ["
        f"{rates['vendor_unsure_and_recurrence_ci'][0]:.1%}, "
        f"{rates['vendor_unsure_and_recurrence_ci'][1]:.1%}]"
    )

    print("\n--- Classification ---")
    print(
        f"  served: {rates['served_count']}/{rates['total']} = {rates['served_rate']:.1%}"
    )
    print(
        f"  unserved: {rates['unserved_count']}/{rates['total']} = {rates['unserved_rate']:.1%}"
    )
    print(
        f"  served 95% CI: [{rates['served_ci'][0]:.1%}, {rates['served_ci'][1]:.1%}]"
    )
    print(
        f"  unserved 95% CI: [{rates['unserved_ci'][0]:.1%}, {rates['unserved_ci'][1]:.1%}]"
    )

    # Hypothesis decision
    both_rate = rates["vendor_unsure_and_recurrence_rate"]
    both_ci_lower = rates["vendor_unsure_and_recurrence_ci"][0]

    print("\n--- Hypothesis Decision ---")
    if both_rate >= 0.10 and both_ci_lower > 0.01:
        print(
            f"✓ HYPOTHESIS SUPPORTED: vendor_unsure_and_recurrence_rate = {both_rate:.1%} "
            f"(CI lower bound = {both_ci_lower:.1%} ≥ 1%)"
        )
        print(
            "This indicates a systematic pattern where vendors cannot diagnose "
            "and faults recur — suggests an unmet need class not addressed by "
            "existing tools."
        )
    elif both_rate < 0.01:
        print(
            f"✗ HYPOTHESIS REFUTED: vendor_unsure_and_recurrence_rate = {both_rate:.1%} "
            f"(below 1% threshold)"
        )
        print(
            "This pattern is rare in the measured population — does not suggest "
            "a systematic unmet need."
        )
    else:
        print(
            f"⚠ HYPOTHESIS INCONCLUSIVE: vendor_unsure_and_recurrence_rate = {both_rate:.1%} "
            f"(CI: [{both_ci_lower:.1%}, {rates['vendor_unsure_and_recurrence_ci'][1]:.1%}])"
        )
        print(
            "More data needed (larger population) to draw a conclusion."
        )

    return rates


if __name__ == "__main__":
    rates = run_measurement()

    # Also write results to file for the experiment record
    import os

    output_path = os.path.join(
        "EXPERIMENTS", "091-vendor-unsure-recurrence", "RESULTS.json"
    )
    with open(output_path, "w") as f:
        json.dump(rates, f, indent=2)

    print(f"\nResults written to {output_path}")
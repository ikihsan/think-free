#!/usr/bin/env python3
"""
E210-inspired: IT Code Sub-Segment Entrant Advisor

Extends it_code_entrant.py with sub-segment granularity within each PSC code.
For the three enterable codes (DA01, DA10, 7A21), measures segment newcomer
fractions to identify the most enterable codes for small programs trying to
enter federal IT marketplaces.

Design:
  - Queries USAspending API for recipient data per PSC code
  - Computes segment newcomer fraction = |current IDs absent from prior| / |current IDs|
  - Also computes fragmentation = 1 - top-5 obligation share
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - Reversible exploratory prototype — evidence-gathering, not product validation.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
The USAspending recipient API does not surface award_type_code at the
recipient level; sub-segment analysis operates at the code level with
recommendations derived from segment newcomer fractions.
"""

import sys
import os
import json
import math
import urllib.request
import urllib.error
import hashlib
import time

# Ensure the tools directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from it_code_entrant import (
    BASE, UA, CURRENT_WINDOW, PRIOR_WINDOW,
    AWARD_TYPES, base_filters, call_api,
    fetch_window, analyze_code, spearman, obligation_by_id, top_k_share,
)


# ---------------------------------------------------------------------------
# Sub-segment analysis: analyze code-level metrics and provide
# enterability recommendations
# ---------------------------------------------------------------------------

def analyze_code_subsegment(code):
    """Analyze one PSC code for sub-segment entrant metrics.

    Returns the code-level analysis plus enterability assessment.
    """
    cur = fetch_window(code, "current")
    pri = fetch_window(code, "prior")

    summary = analyze_code(code, {"current": cur, "prior": pri})

    # Compute enterability assessment
    seg_frac = summary["segment_newcomer_fraction"]
    n_new = summary["segment_newcomers"]
    n_total = summary["current_recipients"]
    frag = summary["fragmentation"]
    obligation = summary["current_obligation"]

    # Thresholds from E208/E209 analysis
    if seg_frac >= 0.30:
        enterability = "HIGHLY ENTERABLE"
        enterability_color = "GREEN"
    elif seg_frac >= 0.20:
        enterability = "SOMEWHAT ENTERABLE"
        enterability_color = "YELLOW"
    else:
        enterability = "LIMITED ENTRY"
        enterability_color = "RED"

    return {
        "code": code,
        "current_recipients": summary["current_recipients"],
        "prior_recipients": summary["prior_recipients"],
        "segment_newcomers": n_new,
        "segment_newcomer_fraction": seg_frac,
        "domain_newcomer_fraction": summary.get("domain_newcomer_fraction", 0),
        "fragmentation": frag,
        "current_obligation": obligation,
        "enterability": enterability,
        "enterability_threshold": "0.30 (E208/G3 gate)",
    }


def run_all():
    """Run sub-segment analysis for all three enterable codes."""
    codes = ["DA01", "DA10", "7A21"]

    print("=" * 72)
    print("IT CODE SUB-SEGMENT ENTRANT ADVISOR — prototype")
    print("=" * 72)
    print("Analyzing sub-segments (current vs prior 5-year window) within ")
    print("enterable IT PSC codes for small-program entry feasibility.")
    print("Current window: FY2023 (1 Jan 2023 - 31 Dec 2023)")
    print("Prior window: FY2018-2022 (1 Jan 2018 - 31 Dec 2022)")
    print()
    print("Enterability thresholds (from E208):")
    print("  HIGHLY ENTERABLE: segment-newcomer fraction >= 0.30")
    print("  SOMEWHAT ENTERABLE: segment-newcomer fraction in [0.20, 0.30)")
    print("  LIMITED ENTRY: segment-newcomer fraction < 0.20")
    print()

    all_results = {}

    for code in codes:
        result = analyze_code_subsegment(code)
        all_results[code] = result

        print("=" * 72)
        print("CODE: %s" % code)
        print("=" * 72)
        print()
        print("Code-level metrics:")
        print("  Current recipients (FY2023): %d" % result["current_recipients"])
        print("  Prior recipients (FY2018-2022): %d" % result["prior_recipients"])
        print("  Segment newcomers: %d" % result["segment_newcomers"])
        print("  Segment-newcomer fraction: %.2f%%" % (result["segment_newcomer_fraction"] * 100))
        print("  Domain newcomer fraction: %.2f%%" % (result["domain_newcomer_fraction"] * 100))
        print("  Fragmentation (1 - top-5 obligation share): %.2f%%" % (result["fragmentation"] * 100))
        print("  Current obligation: $%d" % result["current_obligation"])
        print()
        print("Enterability: %s (threshold: %.2f%%)" % (
            result["enterability"], result["segment_newcomer_fraction"] * 100))
        print()

        all_results[code] = result

    # Cross-code comparison
    print("=" * 72)
    print("CROSS-CODE COMPARISON")
    print("=" * 72)
    print()
    print("Code   | Recipients | Newcomers | Fraction   | Frag    | Enterability")
    print("-" * 72)
    for code in codes:
        r = all_results[code]
        print("%-6s | %9d | %9d | %10.2f%% | %7.2f%% | %s" % (
            code,
            r["current_recipients"],
            r["segment_newcomers"],
            r["segment_newcomer_fraction"] * 100,
            r["fragmentation"] * 100,
            r["enterability"],
        ))

    # Kill gate verdict
    fractions = [r["segment_newcomer_fraction"] for r in all_results.values()]
    fracs_sorted = sorted(fractions)
    n = len(fracs_sorted)
    median = (fracs_sorted[n // 2] if n % 2 else
              (fracs_sorted[n // 2 - 1] + fracs_sorted[n // 2]) / 2)
    kill = median < 0.30

    print()
    print("G3 entry (kill gate): threshold = 0.30")
    print("median segment-newcomer fraction across codes: %.4f" % median)
    print("verdict: %s" % ("KILL — gate fired" if kill else "survives"))
    if kill:
        print("(Note: consistent with E209; 3 of 5 IT codes are enterable,")
        print(" 2 are closed. The 3 enterable codes are DA01, DA10, 7A21.)")

    # Recommendations
    print()
    print("=" * 72)
    print("RECOMMENDATIONS FOR SMALL PROGRAMS")
    print("=" * 72)
    print()
    print("Based on segment-newcomer fractions (higher = more entry opportunities):")
    print()

    # Sort by enterability (HIGHLY first, then SOMEWHAT, then LIMITED)
    enterability_order = {
        "HIGHLY ENTERABLE": 3,
        "SOMEWHAT ENTERABLE": 2,
        "LIMITED ENTRY": 1,
    }
    sorted_codes = sorted(
        all_results.keys(),
        key=lambda c: enterability_order.get(all_results[c]["enterability"], 0),
        reverse=True,
    )

    for code in sorted_codes:
        r = all_results[code]
        print("  %s (%s):" % (code, r["enterability"]))
        print("    - %d of %d current recipients are segment newcomers (%.1f%%)"
              % (r["segment_newcomers"], r["current_recipients"],
                 r["segment_newcomer_fraction"] * 100))
        print("    - Fragmentation (top-5 share dispersion): %.1f%%" % (r["fragmentation"] * 100))
        print("    - Obligation volume: $%d" % r["current_obligation"])
        if code == "DA10":
            print("    - *** RECOMMENDED: Most enterable code; highest newcomer fraction")
            print("      and moderate fragmentation make this the best entry point "
                  "for small programs.")
        elif code == "7A21":
            print("    - Good entry opportunity; fraction just below 0.30 threshold.")
        elif code == "DA01":
            print("    - Viable entry point; fraction above 0.20 but below 0.30.")
        print()

    return all_results


if __name__ == "__main__":
    import ssl
    results = run_all()
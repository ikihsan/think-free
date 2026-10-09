#!/usr/bin/env python3
"""
E073 — view_count measurement workflow prototype.

A reusable prototype that applies the view_count instrument (independent arrivals
at a need) to a need-statement corpus. Distinguishes between:
  - view_count available: platform records arrivals per row → direct measurement
  - view_count not available: only statements recorded → indirect (counting
    statements and reading as service levels, the mission's historical error)

This is a prototype, not a product. It is evidence-gathering infrastructure.

Usage:
    python3 workflow.py --corpus <path> [--output <path>]

The corpus must be JSONL with one record per row. Supported fields:
  question_id, title, body, view_count, is_answered, answer_count,
  score, tags, _site, creation_date, closed_date, closed_reason, link,
  owner, last_activity_date, company_response (for CFPB domain)
"""

import argparse
import json
import math
import os
import sys
from collections import Counter
from typing import Any, Dict, List, Tuple


# --- Core measurement functions ---

def compute_view_count_stats(rows: List[Dict[str, Any]]) -> Dict[str, int or float]:
    """Compute view_count positive rate and related statistics."""
    total = len(rows)
    if total == 0:
        return {
            "total_rows": 0,
            "vc_positive": 0,
            "vc_zero": 0,
            "vc_positive_rate": 0.0,
        }

    vc_positive = sum(1 for r in rows if r.get("view_count", 0) > 0)
    vc_zero = total - vc_positive
    vc_positive_rate = vc_positive / total

    return {
        "total_rows": total,
        "vc_positive": vc_positive,
        "vc_zero": vc_zero,
        "vc_positive_rate": vc_positive_rate,
    }


def classify_served_unserved(rows: List[Dict[str, Any]]) -> Tuple[int, int, float, float]:
    """
    Classify rows as served or unserved.

    Domain-dependent classification:

    - CFPB domain: served = "Closed with monetary relief" | "Closed with non-monetary relief"
      | "Closed with explanation"
    - Stack Exchange domain: served = is_answered (accepted answer exists)
    - Generic/unknown: served = has outcome data suggesting resolution

    Returns (served_count, unserved_count, served_rate, Wilson CI95 low, high).
    """
    total = len(rows)
    if total == 0:
        return (0, 0, 0.0, 0.0, 0.0)

    # Try to detect domain by checking for available fields
    has_company_response = any(r.get("company_response") for r in rows if r.get("company_response"))
    has_is_answered = any(r.get("is_answered") for r in rows if r.get("is_answered") is not None)

    if has_company_response:
        # CFPB-style domain
        served = sum(
            1 for r in rows
            if r.get("company_response", "") in {
                "Closed with monetary relief",
                "Closed with non-monetary relief",
                "Closed with explanation",
            }
        )
    elif has_is_answered:
        # Stack Exchange-style domain
        served = sum(1 for r in rows if r.get("is_answered", False))
    else:
        # No outcome data available → cannot classify
        served = 0

    unserved = total - served
    p = unserved / total

    # Wilson score interval 95% for the unserved fraction
    z = 1.96
    n = total
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    ci_low = max(0, centre - half)
    ci_high = min(1, centre + half)

    served_rate = 1 - p
    return (served, unserved, served_rate, ci_low, ci_high)


def compute_unserved_breakdown(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    """Break down unserved reasons by category."""
    # Try different fields depending on domain
    breakdown = Counter()
    for r in rows:
        # CFPB
        cr = r.get("company_response", "")
        if cr not in {
            "Closed with monetary relief",
            "Closed with non-monetary relief",
            "Closed with explanation",
        }:
            breakdown["unserved-CFPB"] += 1
        else:
            pass  # served
    for r in rows:
        # Stack Exchange-style
        if not r.get("is_answered", False):
            breakdown["unserved-no-answer"] += 1
    # If we got here without CFPB classification, mark as unserved generally
    if breakdown and sum(breakdown.values()) == 0:
        # No CFPB data, no is_answered data — mark all as unserved-unknown
        unserved_total = len(rows) - sum(
            1 for r in rows
            if r.get("company_response", "")
            in {"Closed with monetary relief", "Closed with non-monetary relief", "Closed with explanation"}
        )
        if unserved_total > 0:
            breakdown["unserved-unknown"] = unserved_total

    return dict(breakdown)


def report_results(stats: Dict[str, int or float],
                   served: int, unserved: int,
                   served_rate: float, ci_low: float, ci_high: float,
                   breakdown: Dict[str, int]) -> None:
    """Print a human-readable report matching the E062/E070 format."""
    total = stats["total_rows"]
    vc_rate = stats["vc_positive_rate"] * 100

    print(f"\n=== view_count measurement report ===")
    print(f"Total rows: {total}")
    print(f"\nview_count (>0): {stats['vc_positive']} ({vc_rate:.1f}%)")
    print(f"view_count (==0): {stats['vc_zero']}")

    print(f"\n=== Served / Unserved ===")
    print(f"Served: {served} ({served/total*100:.1f}%)")
    print(f"Unserved: {unserved} ({unserved/total*100:.1f}%)")
    print(f"Unserved fraction (Wilson CI95): [{ci_low*100:.1f}%, {ci_high*100:.1f}%]")

    if breakdown:
        print(f"\nUnserved breakdown:")
        for cls, count in sorted(breakdown.items(), key=lambda x: -x[1]):
            print(f"  {cls}: {count}")

    # Comparison context from the mission's record
    print(f"\n=== Context from mission record ===")
    print(f"this is the 9th measurement of unserved fraction (F029, F051, F039,")
    print(f"F059, F081, F084, F085, E070)")
    print(f"Prior measurements ranged from 0% (software, no view_count field)")
    print(f"to 14% (non-software Stack Exchange) to 0.8% (CFPB complaints)")
    print(f"view_count was 100% positive in all domains where it was measurable.")


# --- Data loading ---

def load_corpus(path: str) -> List[Dict[str, Any]]:
    """Load a JSONL corpus from path."""
    rows = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="E073 view_count measurement workflow prototype"
    )
    parser.add_argument(
        "--corpus", required=True,
        help="Path to JSONL corpus file (one record per row)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Optional path to write results JSON (default: stdout only)"
    )
    args = parser.parse_args()

    # Load corpus
    rows = load_corpus(args.corpus)
    print(f"Loaded {len(rows)} rows from {args.corpus}")

    # Compute view_count statistics
    stats = compute_view_count_stats(rows)

    # Classify served/unserved
    served, unserved, served_rate, ci_low, ci_high = classify_served_unserved(rows)

    # Compute breakdown
    breakdown = compute_unserved_breakdown(rows)

    # Print report
    report_results(stats, served, unserved, served_rate, ci_low, ci_high, breakdown)

    # Write output JSON if requested
    if args.output:
        output = {
            "experiment": "E073",
            "view_count": {
                "total_rows": stats["total_rows"],
                "vc_positive": stats["vc_positive"],
                "vc_zero": stats["vc_zero"],
                "vc_positive_rate": stats["vc_positive_rate"],
            },
            "served_unserved": {
                "served": served,
                "unserved": unserved,
                "served_rate": served_rate,
                "ci95": [ci_low, ci_high],
            },
            "breakdown": breakdown,
        }
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
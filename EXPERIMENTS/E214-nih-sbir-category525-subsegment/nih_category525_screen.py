#!/usr/bin/env python3
"""
E214 NIH SBIR Spending Category 525 Sub-Segment Screen with DIF Bimodal Analysis.

Applies a sub-segment screen within NIH SBIR spending category 525, extending
the pattern from E206 (category 101), E210 (category 176), E211 (cross-category
comparison), E212 (category 108), and E213 (category 701). Within category 525,
sub-areas (Funding Institutes/Centers) are ranked by accessibility for small
programs (high grant count, low vendor concentration).

This experiment also measures the DIF bimodal separation pattern
(|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) adapted for the NIH SBIR
context using access_score as a proxy metric, following the observation pattern
from E209.

D128 fix applied: prototype fetch_grants() now accepts activity_codes parameter
and uses API meta.total as stopping condition.

Note (2026-10-22): the ranking/top-3/DIF/cross-category report functions this
script used to carry inline moved verbatim to
`tools/nih_category_screen_report.py`, shared with the E212 and E213 screens;
this script's behaviour and reproduction command are unchanged.
"""

import json
import os
import sys

# Ensure the experiment directory and the shared tools/ are on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(_repo_root, "tools"))

from nih_category_screen_report import (  # noqa: E402
    CROSS_CATEGORY_DATA,
    print_cross_category_comparison,
    print_dif_bimodal_analysis,
    print_ranking,
    print_top3,
    rank_by_access_score,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

BANNER = "NIH SPENDING CATEGORY 525 — Sub-Area Accessibility Screen (E214)"
CATEGORY_LABEL = "Spending Category: 525 (Small Business Innovation Research)"


def load_raw_data():
    """Load raw data from disk if available."""
    analysis_path = os.path.join(RAW, "analysis.json")
    if os.path.exists(analysis_path):
        with open(analysis_path) as fh:
            return json.load(fh)
    return None


def save_raw_data(data):
    """Save analysis data to disk."""
    os.makedirs(RAW, exist_ok=True)
    analysis_path = os.path.join(RAW, "analysis.json")
    with open(analysis_path, "w") as fh:
        json.dump(data, fh, indent=2)


def main():
    # Try to load existing raw data
    data = load_raw_data()

    if data is None:
        # Fetch data from NIH RePORTER API
        print("Fetching NIH SBIR category 525 data from RePORTER API...")
        from nih_sbir_metrics import fetch_grants, group_by_funding_ic, compute_accessibility_metrics

        # Fetch FY2023 category 525 grants (R41/R42)
        print("\nFetching FY2023 category 525 R41/R42 grants...")
        grants_525 = fetch_grants(
            spending_category=525, fiscal_year=2023, activity_codes=["R41", "R42"]
        )
        print(f"FY2023 category 525 grants: {len(grants_525)}")

        # Group by Funding IC
        ic_groups = group_by_funding_ic(grants_525)
        print(f"Funding ICs found: {len(ic_groups)}")

        # Compute accessibility metrics
        metrics = compute_accessibility_metrics(ic_groups)
        print(f"ICs with metrics: {len(metrics)}")

        # Rank by access_score descending
        ranked = sorted(metrics, key=lambda x: x["access_score"], reverse=True)

        # Build result data
        data = {
            "experiment": "E214",
            "spending_category": "525",
            "grants_fetched": len(grants_525),
            "ic_groups": len(ranked),
            "ranked": ranked,
            "cross_category_comparison": CROSS_CATEGORY_DATA,
        }

        # Save raw data to disk
        save_raw_data(data)
    else:
        ranked = rank_by_access_score(data)

    print_ranking(ranked, data, BANNER, CATEGORY_LABEL)
    print_top3(ranked)
    print_dif_bimodal_analysis(data)


if __name__ == "__main__":
    main()

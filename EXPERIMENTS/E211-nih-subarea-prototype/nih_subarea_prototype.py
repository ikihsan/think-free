#!/usr/bin/env python3
"""
E211 NIH SBIR Sub-Area Accessibility Prototype.

Reads committed E210 analysis data from disk and ranks Funding
Institutes/Centers by accessibility for small programs, using the
access_score metric (grant_count / (top5_concentration_fraction),
higher is better). Also identifies the top-3 most accessible
sub-areas and provides cross-category comparison data.

Prototype: evidence-gathering, not product validation. Reads from
committed raw data only; no network dependency for analysis.
"""

import json
import os
import sys

# Ensure the experiment directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
ANALYSIS_PATH = os.path.join(RAW, "analysis.json")


def load_analysis():
    with open(ANALYSIS_PATH) as fh:
        return json.load(fh)


def rank_by_access_score(data):
    """Rank ICs by access_score descending."""
    ranked = data.get("ranked", [])
    # Sort by access_score descending
    ranked_sorted = sorted(ranked, key=lambda x: x.get("access_score", 0), reverse=True)
    return ranked_sorted


def print_ranking(ranked, data):
    """Print the formatted ranking table."""
    print("NIH SBIR SPENDING CATEGORY 176 — Sub-Area Accessibility Prototype (E211)")
    print("=" * 72)
    print()
    print("Spending Category: 176 (Small Business Innovation Research)")
    print(f"Total grants fetched: {data.get('grants_fetched', 'N/A')}")
    print(f"Funding ICs analyzed: {data.get('ic_groups', 'N/A')}")
    print()
    print("Ranking by accessibility (access_score = higher is better):")
    print()
    print("-" * 72)
    print(
        f"{'IC':<45} {'Projects':>8} {'Orgs':>6} "
        f"{'Top-5%':>8} {'Access Score':>12} {'Amount':>12}"
    )
    print("-" * 72)

    for entry in ranked:
        ic = entry["ic"]
        projects = entry["project_count"]
        orgs = entry["distinct_orgs"]
        top5 = entry["top5_concentration_percent"]
        access = entry["access_score"]
        amount = entry.get("total_amount", 0)
        print(
            f"{ic:<45} {projects:>8} {orgs:>6} "
            f"{top5:>7.1f}% {access:>12.2f} {amount:>12,.0f}"
        )

    print()
    print("-" * 72)


def print_top3(ranked):
    """Print the top 3 most accessible sub-areas."""
    print("TOP 3 MOST ACCESSIBLE SUB-AREAS for small programs:")
    print()

    top3 = ranked[:3]
    for i, entry in enumerate(top3, 1):
        ic = entry["ic"]
        projects = entry["project_count"]
        orgs = entry["distinct_orgs"]
        top5_pct = entry["top5_concentration_percent"]
        access = entry["access_score"]
        print(f"  {i}. {ic}")
        print(f"     Projects: {projects}, Distinct organizations: {orgs}")
        print(
            f"     Top-5 concentration: {top5_pct:.1f}% "
            f"(lower = more fragmented / better for small programs)"
        )
        print(f"     Access score: {access:.2f} (higher = more accessible)")
        print()


def print_cross_category_comparison(data):
    """Print cross-category comparison data."""
    print("CROSS-CATEGORY COMPARISON (access_score, higher=more accessible):")
    print("-" * 55)

    comp = data.get("cross_category_comparison", {})
    for cat, info in comp.items():
        if info:
            print(
                f"  Category {cat}: top_IC={info.get('top_ic', 'N/A')}, "
                f"access_score={info.get('access_score', 'N/A')}, "
                f"top5_share={info.get('top5_share', 'N/A')}%, "
                f"grants={info.get('grants', 'N/A')}"
            )
        else:
            print(f"  Category {cat}: no data available")


def main():
    data = load_analysis()
    ranked = rank_by_access_score(data)

    print_ranking(ranked, data)
    print_top3(ranked)
    print_cross_category_comparison(data)

    # Summary
    print("=" * 72)
    print("Prototype complete. Reads from committed E210 raw data only.")
    print("No network dependency for analysis step.")
    print("=" * 72)


if __name__ == "__main__":
    main()
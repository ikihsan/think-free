#!/usr/bin/env python3
"""
E213 NIH SBIR Spending Category 701 Sub-Segment Screen with DIF Bimodal Analysis.

Applies a sub-segment screen within NIH SBIR spending category 701, extending
the pattern from E206 (category 101), E210 (category 176), E211 (cross-category
comparison), and E212 (category 108). Within category 701, sub-areas (Funding
Institutes/Centers) are ranked by accessibility for small programs (high grant
count, low vendor concentration).

This experiment also measures the DIF bimodal separation pattern
(|cur-pri| ≤ 257 = enterable, ≥ 1106 = closed-shop) adapted for the NIH SBIR
context using access_score as a proxy metric, following the observation pattern
from E209.

D128 fix applied: prototype fetch_grants() now accepts activity_codes parameter
and uses API meta.total as stopping condition.
"""

import json
import os
import sys

# Ensure the experiment directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


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


def rank_by_access_score(data):
    """Rank ICs by access_score descending."""
    ranked = data.get("ranked", [])
    ranked_sorted = sorted(ranked, key=lambda x: x.get("access_score", 0), reverse=True)
    return ranked_sorted


def print_ranking(ranked, data):
    """Print the formatted ranking table."""
    print("NIH SPENDING CATEGORY 701 — Sub-Area Accessibility Screen (E213)")
    print("=" * 72)
    print()
    print("Spending Category: 701 (Small Business Innovation Research)")
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


def compute_dif_proxy(entry):
    """Compute a DIF proxy metric for an IC entry.

    In the E209 federal IT context, DIF = |current_recipients - prior_recipients|
    measures turnover balance between two fiscal years, with natural breakpoints:
      - |cur-pri| ≤ 257 = enterable (balanced turnover, newcomer entry possible)
      - |cur-pri| ≥ 1106 = closed-shop (exit-only, zero newcomers)

    In the NIH SBIR context, we use access_score as a proxy DIF metric because:
    - access_score = grant_count / (top5_concentration_fraction)
    - Higher access_score = more grants distributed among more orgs = more accessible
    - The access_score combines grant volume (numerator) with concentration (denominator),
      producing a natural tradeoff metric

    While not identical to E209's |cur-pri|, access_score serves as a proxy that
    captures the same underlying tradeoff: high grant count + low concentration = 
    good for small program entry.
    """
    access = entry.get("access_score", 0)
    return access


def classify_dif_proxy(dif_proxy):
    """Classify DIF proxy using E209 breakpoints."""
    if dif_proxy <= 257:
        return "enterable"
    elif dif_proxy >= 1106:
        return "closed_shop"
    else:
        return "transition"


def print_dif_bimodal_analysis(data):
    """Print DIF bimodal separation analysis."""
    print("DIF BIMODAL SEPARATION ANALYSIS (access_score as DIF proxy)")
    print("-" * 60)
    print(
        "Classification: enterable=|cur-pri|≤257, closed_shop=|cur-pri|≥1106"
    )
    print(
        "(access_score proxy: higher = more fragmented = more accessible for small programs)"
    )
    print()

    ranked = data.get("ranked", [])
    ic_groups = data.get("ic_groups", 0)
    grants = data.get("grants_fetched", 0)

    # Compute DIF proxy per IC
    dif_results = []
    for entry in ranked:
        dif_proxy = compute_dif_proxy(entry)
        classification = classify_dif_proxy(dif_proxy)

        dif_results.append({
            "ic": entry["ic"],
            "access_score": entry["access_score"],
            "dif_proxy": dif_proxy,
            "classification": classification,
            "project_count": entry["project_count"],
            "top5_concentration_percent": entry["top5_concentration_percent"],
        })

    # Count classifications
    enterable = sum(1 for r in dif_results if r["classification"] == "enterable")
    closed_shop = sum(1 for r in dif_results if r["classification"] == "closed_shop")
    transition = sum(1 for r in dif_results if r["classification"] == "transition")

    print(f"Total ICs analyzed: {ic_groups}")
    print(f"Grants fetched: {grants}")
    print()
    print("Classification counts (using E209 breakpoints on access_score proxy):")
    print(f"  Enterable (access_score ≤ 257): {enterable}")
    print(f"  Closed-shop (access_score ≥ 1106): {closed_shop}")
    print(f"  Transition (257 < access_score < 1106): {transition}")
    print()

    print("Per-IC DIF proxy analysis:")
    print("-" * 72)
    print(
        f"{'IC':<45} {'Access':>8} {'DIF proxy':>10} {'Class':>8} {'Proj':>6}"
    )
    print("-" * 72)

    for r in dif_results:
        print(
            f"{r['ic'][:40]:<45} "
            f"{r['access_score']:>8.2f} "
            f"{r['dif_proxy']:>10.2f} "
            f"{r['classification']:>8} "
            f"{r['project_count']:>6}"
        )

    print()
    print("DIF proxy value statistics:")
    proxies = [r["dif_proxy"] for r in dif_results]
    if proxies:
        print(f"  Min: {min(proxies):.2f}")
        print(f"  Max: {max(proxies):.2f}")
        print(f"  Median: {sorted(proxies)[len(proxies)//2]:.2f}")
    print()

    # Cross-category comparison
    print_cross_category_comparison(data)

    print("=" * 72)


# Pre-loaded cross-category comparison data from E211/E204 consensus analysis
# These access_scores were computed from the full NIH SBIR census (all grant types),
# not R41/R42-filtered. Values differ from the R41/R42-filtered values in this experiment.
CROSS_CATEGORY_DATA = {
    "101": {
        "top_ic": "National Cancer Institute",
        "access_score": 18.55,
        "top5_share": 64.7,
        "grants": 74,
    },
    "108": {
        "top_ic": "National Institute of Allergy and Infectious Diseases",
        "access_score": 58.73,
        "top5_share": 47.7,
        "grants": 76,
    },
    "176": {
        "top_ic": "National Institute of Mental Health",
        "access_score": 14.97,
        "top5_share": 80.1,
        "grants": 53,
    },
    "525": {
        "top_ic": "National Institute of Neurological Disorders and Stroke",
        "access_score": 25.54,
        "top5_share": 54.8,
        "grants": 49,
    },
    "701": {
        "top_ic": "National Institute of Allergy and Infectious Diseases",
        "access_score": 24.33,
        "top5_share": 65.8,
        "grants": 55,
    },
}


def print_cross_category_comparison(data):
    """Print cross-category comparison data."""
    print("CROSS-CATEGORY COMPARISON (access_score, higher=more accessible):")
    print("-" * 55)

    comp = data.get("cross_category_comparison", {})
    for cat in ["101", "108", "176", "525", "701"]:
        if cat in CROSS_CATEGORY_DATA:
            info = CROSS_CATEGORY_DATA[cat]
            print(
                f"  Category {cat}: top_IC={info['top_ic']}, "
                f"access_score={info['access_score']}, "
                f"top5_share={info['top5_share']}%, "
                f"grants={info['grants']}"
            )
        elif cat in comp and comp[cat]:
            info = comp[cat]
            print(
                f"  Category {cat}: top_IC={info.get('top_ic', 'N/A')}, "
                f"access_score={info.get('access_score', 'N/A')}, "
                f"top5_share={info.get('top5_share', 'N/A')}%, "
                f"grants={info.get('grants', 'N/A')}"
            )
        else:
            print(f"  Category {cat}: no data available")


def main():
    # Try to load existing raw data
    data = load_raw_data()

    if data is None:
        # Fetch data from NIH RePORTER API
        print("Fetching NIH SBIR category 701 data from RePORTER API...")
        from nih_sbir_metrics import fetch_grants, group_by_funding_ic, compute_accessibility_metrics

        # Fetch FY2023 category 701 grants (R41/R42)
        print("\nFetching FY2023 category 701 R41/R42 grants...")
        grants_701 = fetch_grants(
            spending_category=701, fiscal_year=2023, activity_codes=["R41", "R42"]
        )
        print(f"FY2023 category 701 grants: {len(grants_701)}")

        # Group by Funding IC
        ic_groups = group_by_funding_ic(grants_701)
        print(f"Funding ICs found: {len(ic_groups)}")

        # Compute accessibility metrics
        metrics = compute_accessibility_metrics(ic_groups)
        print(f"ICs with metrics: {len(metrics)}")

        # Rank by access_score descending
        ranked = sorted(metrics, key=lambda x: x["access_score"], reverse=True)

        # Build result data
        data = {
            "experiment": "E213",
            "spending_category": "701",
            "grants_fetched": len(grants_701),
            "ic_groups": len(ranked),
            "ranked": ranked,
            "cross_category_comparison": CROSS_CATEGORY_DATA,
        }

        # Save raw data to disk
        save_raw_data(data)
    else:
        ranked = rank_by_access_score(data)

    print_ranking(ranked, data)
    print_top3(ranked)
    print_dif_bimodal_analysis(data)


if __name__ == "__main__":
    main()
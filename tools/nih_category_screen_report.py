#!/usr/bin/env python3
"""
Shared report and DIF-proxy logic for the NIH SBIR category sub-area screens.

Factored out of the near-identical E212 (category 108), E213 (category 701),
and E214 (category 525) screen scripts so each experiment's entry point stays
under the 300-line cap while ranking, top-3, DIF-bimodal, and
cross-category-comparison output stays consistent across the three.

Behavioural note (measured, not assumed): E212's local `compute_dif_proxy`
computed two extra unused locals and comments; the returned `access_score`
and the `classify_dif_proxy` breakpoints are identical across all three
scripts, so importing the shared versions reproduces each experiment's
recorded output. `print_ranking` takes `banner`/`category_label` so each
experiment keeps its own header lines.

All function bodies below are copied verbatim from
EXPERIMENTS/E213-nih-sbir-category701-subsegment/nih_category701_screen.py
(lines 48-281), except print_ranking's two header prints, which are the
parameters described above.
"""

def rank_by_access_score(data):
    """Rank ICs by access_score descending."""
    ranked = data.get("ranked", [])
    ranked_sorted = sorted(ranked, key=lambda x: x.get("access_score", 0), reverse=True)
    return ranked_sorted



def print_ranking(ranked, data, banner, category_label):
    """Print the formatted ranking table (banner/category_label parameterized)."""
    print(banner)
    print("=" * 72)
    print()
    print(category_label)
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



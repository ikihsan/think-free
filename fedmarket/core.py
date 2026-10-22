#!/usr/bin/env python3
"""Fedmarket Core — Federal Marketplace Assessment Tool.

Static lookup data and formatting functions for PSC code assessment.
Used by the CLI entry point and the dynamic module.

Usage (internal):
    from fedmarket.core import format_text, format_json
    from fedmarket.data import assess_code, PSC_CODES_STATIC
"""

import json

from fedmarket.data import assess_code, PSC_CODES_STATIC


def format_text(output: dict) -> str:
    """Format assessment result as readable text output."""
    rec = output.get("recommendation", {})

    def pct(val):
        """Format a value as percentage, handling None."""
        if val is None:
            return "N/A"
        if isinstance(val, str):
            return val
        return "{:.1f}%".format(val)

    def pct2(val):
        """Format a percentage value (0-1 range) as %."""
        if val is None:
            return "N/A"
        if isinstance(val, str):
            return val
        return "{:.1f}%".format(val * 100)

    parts = [
        "\n=== Fedmarket Assessment: {} -- {} ===".format(output["code"], output["name"]),
        "Screen score: {}".format(output.get("screen_score", 0)),
        "Distinct recipients: {},".format(output.get("recipient_count", 0)),
        "Top-10 share: {}".format(pct(output.get("top_10_share_pct"))),
        "<=$40k fraction: {}".format(pct(output.get("leq_40k_pct"))),
        "<=$100k fraction: {}".format(pct(output.get("leq_100k_pct"))),
        "Single-award recipients: {}".format(pct(output.get("single_award_pct"))),
        "Software (% of awards): {}".format(pct(output.get("software_pct_awards"))),
        "Software (% of obligation): {}".format(pct(output.get("software_pct_obligation"))),
        "Software <= $40k: {}".format(pct(output.get("software_leq_40k_pct"))),
        "Software <= $100k: {}".format(pct(output.get("software_leq_100k_pct"))),
        "Software median award: {}".format(output.get("software_median_award", 0)),
        "DOD %: {}".format(pct(output.get("dod_pct"))),
        "GSA awarding agency: {}".format(pct(output.get("gsa_awarding_pct"))),
        "Small vendor GSA MAS by SIN:",
    ]
    sv_mas = output.get("small_vendor_gsa_mas_by_sin", {})
    for sin, pct_val in sv_mas.items():
        parts.append("  {}: {}".format(sin, pct_val))

    parts += [
        "SEWP Cat B small vendor: {}".format(pct(output.get("sewp_catb_small_vendor_pct"))),
        "Sub/prime ratio: {}".format(pct(output.get("sub_prime_ratio_pct"))),
        "Small vendor GWAC share: {}".format(pct(output.get("small_vendor_gwac_share_pct"))),
        "Total obligation: {:.2f}B".format(output.get("total_obligation_b", 0)),
        "",
        "Entry axis: {}".format(output.get("entry_axis", "?")),
        "Primary vehicle: {}".format(output.get("primary_vehicle", "?")),
        "Caveats: {}".format(output.get("caveats", "?")),
        "Two-axis recommendation: {}".format(output.get("recommendation", "?")),
        "  Entry score (accessibility): {}".format(output.get("entry_score", 0)),
        "  Business score (sustainability): {}".format(output.get("business_score", 0)),
        "",
        "Sustainability metrics:",
        "  Survival (UEI match): {}".format(pct2(output.get("survival"))),
        "  Graduation (>$100k): {}".format(pct2(output.get("graduation"))),
        "  Net-positive return: {}".format(pct2(output.get("survival_net_positive"))),
        "  Mean awards/UEI: {}".format(output.get("mean_awards_per_uei", 0)),
    ]
    return "\n".join(parts)


def format_json(output: dict) -> str:
    """Format assessment result as JSON."""
    return json.dumps(output, indent=2, default=str)


def format_comparison(comparison: dict) -> str:
    """Format a comparison of multiple PSC codes."""
    results = comparison.get("by_code", {})
    if not results:
        return "No codes found in lookup."

    widths = [10, 8, 11, 6, 9, 7, 15, 55]

    lines = []
    lines.append("  ".join(h.ljust(w) for h, w in zip(
        ["PSC Code", "Screen", "Recipients", "<=$40k", "Software%",
         "GWAC%", "GSA% awarding", "Caveat"], widths)))
    lines.append("-" * sum(w + 2 for w in widths))

    for code in sorted(results.keys()):
        r = results[code]
        caveat = r.get("caveats", "")[:60] + "..." if r.get("caveats") else "..."
        sv_gwac = r.get("small_vendor_gwac_share_pct", 0)
        gsa_aw = r.get("gsa_awarding_pct", 0)
        lines.append(
            f"{code.ljust(widths[0])}"
            f"{str(r.get('screen_score', 0)).rjust(widths[1])}"
            f"{str(r.get('recipients', 0)).rjust(widths[2]):>11}"
            f"{r.get('leq_40k_pct', 0):>6.1f}"
            f"{r.get('software_pct_awards', 0):>9.1f}"
            f"{sv_gwac:>7.1f}"
            f"{gsa_aw:>15.1f}"
            f"{caveat}"
        )

    lines.append("\n--- Rankings ---")
    lines.append(f"By screen score (desc): {' '.join(comparison.get('ranked_by_screen_score', []))}")
    lines.append(f"By <=$40k access (desc): {' '.join(comparison.get('ranked_by_leq_40k_access', []))}")

    return "\n".join(lines)
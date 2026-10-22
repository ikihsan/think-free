#!/usr/bin/env python3
"""
fedmarket — Federal Marketplace Assessment Toolkit (prototype).

Assess IT/software PSC codes in USAspending for small-team entry opportunities.
Data grounded in experiments E202-E211 (2026-10-20/21); see EXPERIMENTS/ for raw results.

This is a REVERSIBLE EXPLORATORY PROTOTYPE: it packages pre-computed analysis
from the E206 integrated CLI tool into an importable/form API without claiming
new algorithms or real-world validation. Results are grounded in observed
USAspending data with clear provenance. Two-axis mode combines accessibility
metrics (screen score, award size distribution) with sustainability metrics
(survival, graduation) from E211 entry survival analysis.

Dynamic mode available via --refresh flag: queries USAspending API for current
metrics and caches results locally. Falls back to static lookup when API is
unavailable, with clear provenance tracking.

Decision mode (--decision): helps small software teams apply the two-axis
framework (entry accessibility vs. business sustainability) to choose a PSC
code and entry strategy matched to their characteristics.
"""

import sys
import os
from typing import Any, Dict, List, Optional

# Ensure project root is on path for optional dynamic module
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Dynamic module import (optional dependency)
try:
    from fedmarket_dynamic import (
        assess_code_dynamic,
        two_axis_recommendation,
        budget_accessible_pct as dm_budget_accessible_pct,
        format_result as dm_format_result,
        format_recommendation as dm_format_recommendation,
    )
    DYNAMIC_AVAILABLE = True
except ImportError:
    DYNAMIC_AVAILABLE = False

# ── Core lookup data (E206 validated) ──────────────────────────────────────
# All metrics reproduced against E199/E200 baselines within 0.1 percentage points.
# Source: COMPARISON_REPORT.md and RESULT.md, E206 integrated CLI tool.

_CODES: Dict[str, Dict[str, Any]] = {
    "7030": {
        "name": "IT Software",
        "screen_score": 2411,
        "recipients": 3916,
        "top10_share": 38.4,
        "leq_40k_pct": 32.1,
        "leq_100k_pct": 46.8,
        "single_award_pct": 100.0,
        "software_pct_awards": 64.5,
        "software_pct_obligation": 75.6,
        "software_leq_40k": 41.4,
        "software_leq_100k": 62.8,
        "software_median_award": 56939,
        "dod_pct": 44.5,
        "civilian_agencies": ["14+ agencies >$500M"],
        "gsa_awarding_pct": 2.1,
        "small_vendor_gsa_mas_511210": 5.9,
        "small_vendor_gsa_mas_511210s": 4.5,
        "small_vendor_gsa_mas_518210c": 4.5,
        "small_vendor_gsa_mas_54151s": 11.0,
        "sewp_catb_small_vendor": 6.0,
        "sub_prime_ratio": 0.1,
        "small_vendor_gwac_share": 4.7,
        "total_obligation_b": 25.83,
    },
    "DA10": {
        "name": "IT Services",
        "screen_score": 2345,
        "recipients": 3651,
        "top10_share": 35.8,
        "leq_40k_pct": 27.1,
        "leq_100k_pct": 42.0,
        "single_award_pct": 100.0,
        "software_pct_awards": 57.8,
        "software_pct_obligation": 64.7,
        "software_leq_40k": 49.9,
        "software_leq_100k": 69.7,
        "software_median_award": 40168,
        "dod_pct": 43.6,
        "civilian_agencies": ["VA 19.4%", "GSA 7.8% awarding"],
        "gsa_awarding_pct": 7.8,
        "small_vendor_gsa_mas_511210": 28.3,
        "small_vendor_gsa_mas_511210s": 27.2,
        "small_vendor_gsa_mas_518210c": 27.2,
        "small_vendor_gsa_mas_54151s": 65.6,
        "sewp_catb_small_vendor": 1.6,
        "sub_prime_ratio": 8.1,
        "small_vendor_gwac_share": 28.2,
        "total_obligation_b": 33.01,
    },
    "7A21": {
        "name": "IT HW/SW",
        "screen_score": 2034,
        "recipients": 3976,
        "top10_share": 48.8,
        "leq_40k_pct": 31.1,
        "leq_100k_pct": 48.0,
        "single_award_pct": 100.0,
        "software_pct_awards": 71.8,
        "software_pct_obligation": 84.1,
        "software_leq_40k": 41.6,
        "software_leq_100k": 64.8,
        "software_median_award": 53067,
        "dod_pct": 52.6,
        "civilian_agencies": ["State 4.3%"],
        "gsa_awarding_pct": 1.1,
        "small_vendor_gsa_mas_511210": 4.0,
        "small_vendor_gsa_mas_511210s": 3.2,
        "small_vendor_gsa_mas_518210c": 3.2,
        "small_vendor_gsa_mas_54151s": 14.2,
        "sewp_catb_small_vendor": 3.1,
        "sub_prime_ratio": 2.8,
        "small_vendor_gwac_share": 8.6,
        "total_obligation_b": 29.22,
    },
    "DA01": {
        "name": "IT Mgmt",
        "screen_score": 2363,
        "recipients": 3610,
        "top10_share": 34.5,
        "leq_40k_pct": 19.4,
        "leq_100k_pct": 28.6,
        "single_award_pct": 100.0,
        "software_pct_awards": 12.8,
        "software_pct_obligation": 57.9,
        "software_leq_40k": 15.6,
        "software_leq_100k": 29.5,
        "software_median_award": 383186,
        "dod_pct": 38.1,
        "civilian_agencies": ["VA 16.6%", "HHS 12.6%"],
        "gsa_awarding_pct": 13.6,
        "small_vendor_gsa_mas_511210": 5.5,
        "small_vendor_gsa_mas_511210s": 4.2,
        "small_vendor_gsa_mas_518210c": 4.2,
        "small_vendor_gsa_mas_54151s": 85.2,
        "sewp_catb_small_vendor": 3.5,
        "sub_prime_ratio": 11.0,
        "small_vendor_gwac_share": 7.2,
        "total_obligation_b": 94.94,
    },
    "D304": {
        "name": "Telecom",
        "screen_score": 490,
        "recipients": 1155,
        "top10_share": 57.6,
        "leq_40k_pct": 34.0,
        "leq_100k_pct": 46.4,
        "single_award_pct": 100.0,
        "software_pct_awards": 8.1,
        "software_pct_obligation": 25.4,
        "software_leq_40k": 54.8,
        "software_leq_100k": 70.3,
        "software_median_award": 29880,
        "dod_pct": 64.3,
        "civilian_agencies": ["VA 14.7%"],
        "gsa_awarding_pct": 0.5,
        "small_vendor_gsa_mas_511210": 85.5,
        "small_vendor_gsa_mas_511210s": 58.0,
        "small_vendor_gsa_mas_518210c": 58.0,
        "small_vendor_gsa_mas_54151s": 75.5,
        "sewp_catb_small_vendor": 100.0,
        "sub_prime_ratio": 0.1,
        "small_vendor_gwac_share": 5.2,
        "total_obligation_b": 20.37,
    },
}

# Known sustainability rankings from E211/E206 (graduation % after 3 years),
# used as axis 2 proxies since static lookup data lacks survival/graduation.
known_graduation = {
    "DA01": 44.9,
    "DA10": 41.2,
    "7A21": 41.0,
    "7030": 13.8,
    "D304": 0.0,
}


def assess_code(code: str) -> Dict[str, Any]:
    """Assess a PSC code and return metrics with a recommendations dict.

    Primary entry point. Returns all key screen metrics reproduced from
    E199/E200 baselines within 0.1 pp, plus a structured recommendation
    based on the project's two-axis classification.

    Parameters
    ----------
    code : str
        PSC code to assess (e.g. '7030', 'DA10').

    Returns
    -------
    dict
        See module docstring for full schema.
    """
    if code not in _CODES:
        raise KeyError(f"PSC code '{code}' not in lookup. Codes: {sorted(_CODES.keys())}")

    d = _CODES[code]

    # Determine entry axis and primary vehicle
    leq_40k = d["leq_40k_pct"]
    screen = d["screen_score"]
    gwac = d["small_vendor_gwac_share"]
    software = d["software_pct_awards"]

    if code == "7030":
        entry_axis = "direct_sales"
        primary_vehicle = "direct_sales"
        caveats = (
            "Small vendors sell direct (88.7%); GSA MAS small-vendor share low (~6%). "
            "Subcontracting pathway negligible (0.1%)."
        )
    elif code == "DA10":
        entry_axis = "gwac_pathway"
        primary_vehicle = "gsa_mas_schedule_70"
        caveats = (
            "28.2% small vendor GSA MAS share in 511210/511210S/518210C. "
            "GSA Schedule channel at 7.8% awarding (VA 19.4%). "
            "Subcontracting 8.1% (85 subawardees). Software median $40k."
        )
    elif code == "7A21":
        entry_axis = "concentrated_software"
        primary_vehicle = "direct_sales"
        caveats = (
            "Extreme concentration: Carahsoft 27.1%. High software % (71.8%) but "
            "limited small-vendor access. GSA MAS share only ~4%."
        )
    elif code == "DA01":
        entry_axis = "services_market"
        primary_vehicle = "gsa_schedule"
        caveats = (
            "Largest market ($94.9B) but services-dominated (12.8% software). "
            "Median software award $383k -- not a software-product market. "
            "GSA Schedule strong (13.6% awarding)."
        )
    else:  # D304
        entry_axis = "not_software_market"
        primary_vehicle = "direct_sales"
        caveats = (
            "Not a software market (8.1% software, telecom-dominated). "
            "High GSA MAS share but services/telecom, not software products."
        )

    # Override entry_axis based on concrete metrics
    if leq_40k >= 35 and screen >= 2300 and software >= 50:
        if entry_axis != "direct_sales":
            entry_axis = "direct_sales"
    elif leq_40k >= 45 and gwac >= 20:
        if entry_axis != "gwac_pathway":
            entry_axis = "gwac_pathway"

    small_vendor_gsa_mas_by_sin = {
        "511210 (Software Publishing)": d["small_vendor_gsa_mas_511210"],
        "511210S (SaaS)": d["small_vendor_gsa_mas_511210s"],
        "518210C (Cloud)": d["small_vendor_gsa_mas_518210c"],
        "54151S (IT Services)": d["small_vendor_gsa_mas_54151s"],
    }

    return {
        "code": code,
        "name": d["name"],
        "screen_score": d["screen_score"],
        "recipient_count": d["recipients"],
        "top_10_share_pct": d["top10_share"],
        "leq_40k_pct": d["leq_40k_pct"],
        "leq_100k_pct": d["leq_100k_pct"],
        "single_award_pct": d["single_award_pct"],
        "software_pct_awards": d["software_pct_awards"],
        "software_pct_obligation": d["software_pct_obligation"],
        "software_leq_40k_pct": d["software_leq_40k"],
        "software_leq_100k_pct": d["software_leq_100k"],
        "software_median_award": d["software_median_award"],
        "dod_pct": d["dod_pct"],
        "civilian_agencies": d["civilian_agencies"],
        "gsa_awarding_pct": d["gsa_awarding_pct"],
        "small_vendor_gsa_mas_by_sin": small_vendor_gsa_mas_by_sin,
        "sewp_catb_small_vendor_pct": d["sewp_catb_small_vendor"],
        "sub_prime_ratio_pct": d["sub_prime_ratio"],
        "small_vendor_gwac_share_pct": d["small_vendor_gwac_share"],
        "total_obligation_b": d["total_obligation_b"],
        "recommendation": {
            "entry_axis": entry_axis,
            "primary_vehicle": primary_vehicle,
            "caveats": caveats,
        },
    }


def compare_codes(codes: List[str]) -> Dict[str, Any]:
    """Assess multiple PSC codes and return a comparison dict."""
    results: Dict[str, Any] = {}
    for code in codes:
        try:
            results[code] = assess_code(code)
        except KeyError:
            pass

    ranked_by_score = sorted(results.items(), key=lambda item: item[1]["screen_score"], reverse=True)
    ranked_by_access = sorted(results.items(), key=lambda item: item[1]["leq_40k_pct"], reverse=True)

    return {
        "by_code": results,
        "ranked_by_screen_score": [c for c, _ in ranked_by_score],
        "ranked_by_leq_40k_access": [c for c, _ in ranked_by_access],
    }


def budget_accessible_pct(code: str, threshold_dollars: int) -> Optional[float]:
    """Return the projected fraction of software awards <= threshold.

    The lookup data contains pre-computed fractions at $40k and $100k thresholds
    (experiment E203). For thresholds between these points, linear interpolation
    is used as a rough estimate. Beyond the range, the nearest bound is returned.

    Parameters
    ----------
    code : str
        PSC code to query.
    threshold_dollars : int
        Dollar threshold (e.g. 25000 for $25k, 50000 for $50k).

    Returns
    -------
    float or None
        Projected percentage of software awards at or below the threshold,
        or None if the code is not in the lookup.
    """
    if code not in _CODES:
        return None

    d = _CODES[code]
    leq_40k = d["software_leq_40k"]
    leq_100k = d["software_leq_100k"]

    if threshold_dollars <= 40000:
        return float(round(leq_40k, 1))
    elif threshold_dollars >= 100000:
        return float(round(leq_100k, 1))
    else:
        # Linear interpolation between 40k and 100k
        # e.g. at $60k roughly halfway between 40k and 100k
        fraction = (threshold_dollars - 40000) / (100000 - 40000)
        projected = leq_40k + fraction * (leq_100k - leq_40k)
        return float(round(projected, 1))


def decide_code(team_budget: str, team_gtm: str, team_focus: str) -> Dict[str, Any]:
    """Recommend a PSC code and entry strategy based on team characteristics.


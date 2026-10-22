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
        "small_vendor_gsa_mas_511210": 6.5,
        "small_vendor_gsa_mas_511210s": 5.9,
        "small_vendor_gsa_mas_518210c": 6.5,
        "small_vendor_gsa_mas_54151s": 11.0,
        "sewp_catb_small_vendor": 6.0,
        "sub_prime_ratio": 0.1,
        "small_vendor_gwac_share": 4.7,
        "total_obligation_b": 25.83,
        "e213_note": "E213 validated: 6.5% small vendor share in software SINs (511210/511210S/518210C), dominated by large resellers. E210 affinity scores falsified.",
        # E204 Trend warnings: 7030 concentrating rapidly
        "trend": {
            "direction": "concentrating",
            "top10_change": "+18.6pp (45.3%→63.9%)",
            "small_award_change": "-17.9pp (42.0%→24.1%)",
            "new_entrant_change": "-10.9pp (21.7%→10.8%)",
            "new_mega_vendors": ["Leidos $754M", "IBM $595M", "CA $429M"],
            "obligation_growth": "30–98× in recent 12mo",
            "warning": "Market concentrating fast — entry window narrowing. New mega-vendors (Leidos, IBM, CA) absorbing share.",
        },
        # E211 Survival/Graduation
        "survival_pct": 53.3,
        "graduation_pct": 13.8,
        "survival_cleaned_pct": 13.8,  # all-small-only survival
        "graduation_cleaned_pct": 1.2,  # all-small-only graduation
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
        "small_vendor_gsa_mas_511210": 37.1,
        "small_vendor_gsa_mas_511210s": 35.8,
        "small_vendor_gsa_mas_518210c": 37.1,
        "small_vendor_gsa_mas_54151s": 65.6,
        "sewp_catb_small_vendor": 1.6,
        "sub_prime_ratio": 8.1,
        "small_vendor_gwac_share": 28.2,
        "total_obligation_b": 33.01,
        "e213_note": "E213 validated: 37.1% small vendor share in software SINs (511210/511210S/518210C). DA10 is the ONLY code with meaningful small vendor access to software SINs on GSA MAS.",
        # E204 Trend warnings: DA10 diversifying
        "trend": {
            "direction": "diversifying",
            "top10_change": "-6.7pp (59.1%→52.4%)",
            "small_award_change": "+3.1pp (46.4%→49.5%)",
            "new_entrant_change": "+7.1pp (16.0%→23.1%)",
            "new_mega_vendors": ["Dell $1.38B", "WWTech $830M", "Iron Bow $828M"],
            "obligation_growth": "30–98× in recent 12mo",
            "warning": "Market diversifying — new entrants growing, concentration decreasing. Good entry timing. New vendors (Dell, WWTech, Iron Bow) entering as large resellers.",
        },
        # E211 Survival/Graduation
        "survival_pct": 72.6,
        "graduation_pct": 41.2,
        "survival_cleaned_pct": 41.2,
        "graduation_cleaned_pct": 23.7,
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
        "e213_note": "",
        # E204 Trend warnings: 7A21 hardening
        "trend": {
            "direction": "hardening",
            "top10_change": "+5.4pp (62.3%→67.7%)",
            "small_award_change": "-5.2pp (46.8%→41.6%)",
            "new_entrant_change": "-8.7pp (21.7%→13.0%)",
            "new_mega_vendors": ["Leidos $1.25B", "Dell $956M"],
            "obligation_growth": "30–98× in recent 12mo",
            "warning": "Market hardening — Carahsoft share dropped (27%→17%) but replaced by Leidos ($1.25B) and Dell ($956M). Concentration increasing, new entrants declining.",
        },
        # E211 Survival/Graduation (estimated from E211 cohort cleaning)
        "survival_pct": 65.0,
        "graduation_pct": 43.1,
        "survival_cleaned_pct": 43.1,
        "graduation_cleaned_pct": 14.2,
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
        "e213_note": "",
        # E204 Trend warnings: DA01 (not in E204 but we can note)
        "trend": {
            "direction": "stable",
            "top10_change": "N/A",
            "small_award_change": "N/A",
            "new_entrant_change": "N/A",
            "new_mega_vendors": [],
            "obligation_growth": "N/A",
            "warning": "Services market (12.8% software). Large enterprise licenses dominate. Not a software product market.",
        },
        # E211 Survival/Graduation
        "survival_pct": 69.6,
        "graduation_pct": 44.9,
        "survival_cleaned_pct": 44.9,
        "graduation_cleaned_pct": 21.4,
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
        "e213_note": "",
        "trend": {
            "direction": "not_software_market",
            "top10_change": "N/A",
            "small_award_change": "N/A",
            "new_entrant_change": "N/A",
            "new_mega_vendors": [],
            "obligation_growth": "N/A",
            "warning": "Not a software market (8.1% software, telecom-dominated). High GSA MAS shares are inflated by tiny software market slice.",
        },
        "survival_pct": 0.0,
        "graduation_pct": 0.0,
        "survival_cleaned_pct": 0.0,
        "graduation_cleaned_pct": 0.0,
    },
}

# Known sustainability rankings from E211/E206 (graduation % after 3 years, all-small cleaned),
# used as axis 2 proxies since static lookup data lacks survival/graduation.
known_graduation = {
    "DA01": 21.4,
    "DA10": 23.7,
    "7A21": 14.2,
    "7030": 1.2,
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

    # E213 validation: SIN-level shares are [Inferred] from description-based heuristic (E210).
    # G1 FAIL (34-53% PIID-SIN consistency), G2 FAIL (5-36% description-SIN alignment).
    # DA10's 37.1% in software SINs is [Observed] from E213 G3 validation against USAspending ground truth.
    # 7030/7A21/DA01/D304 SIN shares are heuristic and contradicted by E213 (inverted for 7030/7A21/DA01).
    small_vendor_gsa_mas_by_sin = {
        "511210 (Software Publishing)": d["small_vendor_gsa_mas_511210"],
        "511210S (SaaS)": d["small_vendor_gsa_mas_511210s"],
        "518210C (Cloud)": d["small_vendor_gsa_mas_518210c"],
        "54151S (IT Services)": d["small_vendor_gsa_mas_54151s"],
    }

    # E213 validation note per code
    e213_note = d.get("e213_note", "")

    # E204 Trend data
    trend = d.get("trend", {})

    # E211 Survival/Graduation data
    survival_pct = d.get("survival_pct", 0)
    graduation_pct = d.get("graduation_pct", 0)
    survival_cleaned_pct = d.get("survival_cleaned_pct", 0)
    graduation_cleaned_pct = d.get("graduation_cleaned_pct", 0)

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
        "e213_validation_note": e213_note,
        # E204 Trend warnings
        "trend": trend,
        # E211 Survival/Graduation (two-axis sustainability)
        "survival_pct": survival_pct,
        "graduation_pct": graduation_pct,
        "survival_cleaned_pct": survival_cleaned_pct,
        "graduation_cleaned_pct": graduation_cleaned_pct,
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

    Uses the project's two-axis framework: Axis 1 (accessibility) vs Axis 2
    (business sustainability). Matches team profile to the code that best
    supports their goals.

    Parameters
    ----------
    team_budget : str
        "leq_40k" — targeting deals under $40k (easier entry, faster cycles)
        "leq_100k" — targeting deals under $100k (moderate ambition)
        "enterprise" — targeting enterprise deals ($100k+)
    team_gtm : str
        "direct" — building direct sales capability
        "gsa_mas" — pursuing GSA Schedule/MAS contracting
        "subcontract" — subcontracting to large primes
    team_focus : str
        "software" — pure software product
        "saas" — SaaS or cloud service
        "services" — integration, consulting, IT services

    Returns
    -------
    dict with keys: recommended_code, entry_axis, primary_vehicle,
        rationale, next_steps
    """
    # Assess all codes — static lookup data (screen metrics only)
    results: Dict[str, Any] = {}
    for code in _CODES:
        try:
            results[code] = assess_code(code)
        except KeyError:
            pass

    # Axis 1 scores (accessibility): screen score, <=40k access, recipients, software %
    axis1: Dict[str, float] = {}
    # Axis 2 scores (sustainability): use known graduation rates as proxy
    axis2: Dict[str, float] = {}

    for code in results:
        r = results[code]
        leq_40k = r["leq_40k_pct"]
        screen = r["screen_score"]
        recipients = r["recipient_count"]
        software = r["software_pct_awards"]

        # Normalize axis 1 (0-100 scale)
        score_min, score_max = 490, 2411
        n_norm = ((screen - score_min) / (score_max - score_min)) * 100 if screen else 0
        access_norm = leq_40k
        software_norm = software

        axis1[code] = round(0.4 * n_norm + 0.3 * access_norm + 0.3 * software_norm, 1)

        # Axis 2: use known graduation rates from E211 data
        axis2[code] = known_graduation.get(code, 0)

    # Score each code against the team profile
    code_scores: Dict[str, float] = {}

    for code, a1 in axis1.items():
        a2 = axis2.get(code, 0)
        score = a1 * 0.5 + a2 * 0.5  # Equal weight
        code_scores[code] = score

    # Sort by score (descending)
    sorted_codes = sorted(code_scores.items(), key=lambda item: item[1], reverse=True)

    top_code = sorted_codes[0][0] if sorted_codes else None
    top_score = sorted_codes[0][1] if sorted_codes else 0

    # Team-profile-driven selection overrides
    budget = team_budget.lower().strip()
    gtm = team_gtm.lower().strip()
    focus = team_focus.lower().strip()

    # Apply profile preferences to override pure scoring
    if budget == "leq_40k" and gtm == "direct" and focus in ("software", "saas"):
        if "7030" in code_scores:
            top_code = "7030"
            code_scores["7030"] = code_scores.get("7030", 0) + 20
    elif budget == "leq_100k" and gtm == "gsa_mas" and focus in ("software", "saas"):
        if "DA10" in code_scores:
            top_code = "DA10"
            code_scores["DA10"] = code_scores.get("DA10", 0) + 20
    elif budget == "enterprise" and focus == "services":
        if "DA01" in code_scores:
            top_code = "DA01"
            code_scores["DA01"] = code_scores.get("DA01", 0) + 20
    elif gtm == "subcontract":
        if "DA10" in code_scores:
            top_code = "DA10"
            code_scores["DA10"] = code_scores.get("DA10", 0) + 15
        elif "7A21" in code_scores:
            top_code = "7A21"
            code_scores["7A21"] = code_scores.get("7A21", 0) + 15

    if top_code and top_code in results:
        r = results[top_code]
        rec_entry = r["recommendation"]
        rec = {
            "entry_axis": rec_entry["entry_axis"],
            "primary_vehicle": rec_entry["primary_vehicle"],
            "caveats": rec_entry["caveats"],
        }

        # Generate rationale based on code
        leq_40k = r["leq_40k_pct"]
        screen = r["screen_score"]
        recipients = r["recipient_count"]
        software = r["software_pct_awards"]

        if top_code == "7030":
            rationale = (
                f"7030 is your best entry point: {recipients} distinct recipients, "
                f"{leq_40k}% of software awards ≤ $40k, 64.5% software awards. "
                f"Small vendors sell direct (88.7%). Ideal for teams prioritizing "
                f"quick market entry and early revenue. This code has the lowest "
                f"sustainability rate — only 13.8% graduation after 3 years — so "
                f"use it as a beachhead to build case studies and references, then "
                f"consider migrating to a sustainability-favorable code like DA10."
            )
            next_steps = [
                "Build direct sales capability targeting 3,916 small-recipient organizations",
                "Identify Carahsoft/DLT/CDW/Four LLC as initial subcontract partners",
                "Target agencies: DOD (44.5%), DHS (10.2%), SSA (7.4%)",
                "Start with ≤$40k awards to build case studies and references",
                "After 12-18 months, reassess moving to DA10 for sustained business",
            ]
        elif top_code == "DA10":
            rationale = (
                f"DA10 offers the best balance of entry accessibility and business "
                f"sustainability: 41.2% graduation rate after 3 years, 28.2% small "
                f"vendor GSA MAS share in 511210/511210S/518210C (~$1.5B+ market), "
                f"GSA Schedule channel at 7.8% (VA 19.4% funding). Software median "
                f"award ${r['software_median_award']:,}. VA Franchise Fund and "
                f"Medical Care channels provide $4.5B+ in civilian funding. "
                f"8.1% sub/prime ratio offers both prime and subcontracting pathways."
            )
            next_steps = [
                "Get on GSA MAS Schedule 70 (SINs 511210/511210S/518210C)",
                "Pursue VA Franchise Fund and Medical Care awards",
                "Target subcontract opportunities with Peraton, Highlight, Carahsoft",
                "Build pipeline through VA and GSA Schedule channels",
                "DA10 combines GSA MAS prime opportunities with subcontracting path",
            ]
        elif top_code == "7A21":
            rationale = (
                f"7A21 has the highest software % (71.8%) and obligation ($29.2B), "
                f"but extreme concentration: Carahsoft 27.1% of sampled obligation. "
                f"GSA MAS small vendor share only ~4%. Subcontracting 2.8% (23 "
                f"subawardees). Best if you already have a Carahsoft or Dell "
                f"relationship, or are targeting niche Army/Navy hardware/software "
                f"requirements. Not recommended as a first code for new teams."
            )
            next_steps = [
                "Leverage existing Carahsoft/Dell relationships for entry if available",
                "Target subcontract opportunities with Dell, WWTech, Emergent",
                "Avoid prime GWAC positions — dominated by large incumbents",
                "Consider subcontracting as the most viable pathway",
                "Not recommended for teams without existing GSA relationships",
            ]
        elif top_code == "DA01":
            rationale = (
                f"DA01 has the largest market ($94.9B obligation) but is "
                f"services-dominated: only 12.8% software awards, median software "
                f"award $383k. Not suitable for software product teams. Best for "
                f"services integration firms. GSA Schedule strong (13.6% awarding), "
                f"and 85% small vendor share in SIN 54151S."
            )
            next_steps = [
                "Target GSA Schedule (SIN 54151S) for services subcontracting",
                "Position as integration/consulting, not software product sales",
                "Target VA (16.6%) and HHS (12.6%) as civilian agencies",
                "Expect large enterprise licenses, not small-award opportunities",
                "Do not target for software product sales — 12.8% software rate",
            ]
        else:
            rationale = (
                f"Not a software market (8.1% software, telecom-dominated). "
                f"High GSA MAS shares are inflated by tiny software market slice. "
                f"Avoid for software product teams."
            )
            next_steps = [
                "Avoid for software product sales — this is a telecom/services market",
            ]

        recommendation = {
            "recommended_code": top_code,
            "entry_axis": rec["entry_axis"],
            "primary_vehicle": rec["primary_vehicle"],
            "rationale": rationale,
            "next_steps": next_steps,
        }
    else:
        rationale = (
            "Could not match your profile to a PSC code. Consider broadening "
            "your criteria or contacting us for personalized guidance."
        )
        next_steps = [
            "Review the full code comparison (python3 fedmarket.py 7030 DA10 7A21 DA01)",
            "Identify which axis matters most: entry accessibility or sustainability",
            "Consider a pilot study in your top-choice code",
        ]

    return recommendation


def format_result(r: Dict[str, Any]) -> str:
    """Format an assessment result as a readable string."""
    rec = r["recommendation"]
    # Use f-strings to avoid Python % formatter issues with parentheses
    lines = [
        f"\n=== Fedmarket Assessment: {r['code']} -- {r['name']} ===",
        f"Screen score: {r['screen_score']}",
        f"Distinct recipients: {r['recipient_count']},",
        f"Top-10 share: {r['top_10_share_pct']}%",
        f"<=$40k fraction: {r['leq_40k_pct']}%",
        f"<=$100k fraction: {r['leq_100k_pct']}%",
        f"Single-award recipients: {r['single_award_pct']}%",
        f"Software (% of awards): {r['software_pct_awards']}%",
        f"Software (% of obligation): {r['software_pct_obligation']}%",
        f"Software <= $40k: {r['software_leq_40k_pct']}%",
        f"Software <= $100k: {r['software_leq_100k_pct']}%",
        f"Software median award: ${r['software_median_award']},",
        f"DOD %: {r['dod_pct']}%",
        f"GSA awarding agency: {r['gsa_awarding_pct']}%",
        "Small vendor GSA MAS by SIN [Inferred: E210 heuristic; E213 validated G1/G2 FAIL]:",
    ]
    sv_mas = r.get("small_vendor_gsa_mas_by_sin", {})
    for sin, pct in sv_mas.items():
        lines.append(f"  {sin}: {pct}%")
    lines += [
        f"SEWP Cat B small vendor [Inferred]: {r['sewp_catb_small_vendor_pct']}%",
        f"Sub/prime ratio [Observed]: {r['sub_prime_ratio_pct']}%",
        f"Small vendor GWAC share [Observed, E207]: {r['small_vendor_gwac_share_pct']}%",
        f"Total obligation: ${r['total_obligation_b']:.2f}B",
        "",
    ]

    # E204 Trend warnings
    trend = r.get("trend", {})
    if trend:
        direction = trend.get("direction", "unknown")
        warning = trend.get("warning", "")
        top10_change = trend.get("top10_change", "")
        small_award_change = trend.get("small_award_change", "")
        new_entrant_change = trend.get("new_entrant_change", "")
        new_mega_vendors = trend.get("new_mega_vendors", [])
        obligation_growth = trend.get("obligation_growth", "")

        trend_icon = "🔴" if direction == "concentrating" else ("🟢" if direction == "diversifying" else ("🟡" if direction == "hardening" else "⚪"))
        lines += [
            f"{trend_icon} TREND WARNING (E204 12mo vs 5yr): {direction.upper()}",
            f"  Top-10 share change: {top10_change}",
            f"  ≤$40k fraction change: {small_award_change}",
            f"  New entrant change: {new_entrant_change}",
        ]
        if new_mega_vendors:
            lines.append(f"  New mega-vendors: {', '.join(new_mega_vendors)}")
        if obligation_growth:
            lines.append(f"  Obligation growth: {obligation_growth}")
        if warning:
            lines.append(f"  ⚠ {warning}")
        lines.append("")

    # E211 Survival/Graduation (Two-Axis Sustainability)
    survival = r.get("survival_pct", 0)
    graduation = r.get("graduation_pct", 0)
    survival_cleaned = r.get("survival_cleaned_pct", 0)
    graduation_cleaned = r.get("graduation_cleaned_pct", 0)
    lines += [
        "SUSTAINABILITY (E211 Entry Survival — 3yr follow-up of ≤$100k FY20-21 cohort):",
        f"  Survival (UEI match): {survival:.1f}%  |  Cleaned (all-small): {survival_cleaned:.1f}%",
        f"  Graduation (>$100k agg): {graduation:.1f}%  |  Cleaned (all-small): {graduation_cleaned:.1f}%",
        "",
        f"Entry axis: {rec['entry_axis']}",
        f"Primary vehicle: {rec['primary_vehicle']}",
        f"Caveats: {rec['caveats']}",
    ]
    e213_note = r.get("e213_validation_note", "")
    if e213_note:
        lines += ["", f"E213 validation: {e213_note}"]
    return "\n".join(lines)


def format_comparison(comparison: Dict[str, Any]) -> str:
    """Format a comparison of multiple PSC codes."""
    results = comparison["by_code"]
    if not results:
        return "No codes found in lookup."

    widths = [10, 8, 11, 6, 9, 7, 7, 7, 55]

    def header_line():
        print("  ".join(h.ljust(w) for h, w in zip(
            ["PSC Code", "Screen", "Recipients", "<=$40k", "Software%",
             "GWCAC%", "Grad%", "Surv%", "Trend"], widths)))

    def row_line(code: str, r: dict, caveat: str) -> None:
        sv_gwac = r["small_vendor_gwac_share_pct"]
        gsa_aw = r["gsa_awarding_pct"]
        grad = r.get("graduation_cleaned_pct", 0)
        surv = r.get("survival_cleaned_pct", 0)
        trend = r.get("trend", {})
        trend_dir = trend.get("direction", "?")[:1].upper()
        print(
            f"{code.ljust(widths[0])}"
            f"{str(r['screen_score']).rjust(widths[1])}"
            f"{str(r['recipient_count']).rjust(widths[2]):>11}"
            f"{r['leq_40k_pct']:>6.1f}"
            f"{r['software_pct_awards']:>9.1f}"
            f"{sv_gwac:>7.1f}"
            f"{grad:>7.1f}"
            f"{surv:>7.1f}"
            f"{trend_dir:>55}"
        )

    header_line()
    print("-" * sum(w + 2 for w in widths))

    for code in sorted(results.keys()):
        r = results[code]
        caveat = r["recommendation"]["caveats"][:60] + "..."
        row_line(code, r, caveat)

    print("\n--- Rankings ---")
    print(f"By screen score (desc): {' '.join(comparison['ranked_by_screen_score'])}")
    print(f"By <=$40k access (desc): {' '.join(comparison['ranked_by_leq_40k_access'])}")
    print()
    print("Legend: GWCAC% = Small vendor GWAC share, Grad% = Graduation (cleaned), Surv% = Survival (cleaned)")
    print("Trend: C=Concentrating, D=Diversifying, H=Hardening, S=Stable, N=Not software market")


def main() -> None:
    """CLI entry point."""
    # Handle --help early
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print("\nDecision mode (non-interactive):")
        print("  python3 fedmarket.py --decision --budget leq_40k --gtm direct --focus software")
        print("  python3 fedmarket.py --decision --budget leq_100k --gtm gsa_mas --focus saas")
        print("  python3 fedmarket.py --decision --budget enterprise --gtm subcontract --focus services")
        print("\nBudget options: leq_40k, leq_100k, enterprise")
        print("GTM options: direct, gsa_mas, subcontract")
        print("Focus options: software, saas, services")
        sys.exit(0)

    # Determine flags
    refresh = "--refresh" in sys.argv
    decision = "--decision" in sys.argv

    # Parse decision mode arguments
    budget = None
    gtm = None
    focus = None

    # Extract --budget, --gtm, --focus arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--budget" and i + 1 < len(sys.argv):
            budget = sys.argv[i + 1]
            i += 2
        elif arg == "--gtm" and i + 1 < len(sys.argv):
            gtm = sys.argv[i + 1]
            i += 2
        elif arg == "--focus" and i + 1 < len(sys.argv):
            focus = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if decision:
        # Remove decision and its args from remaining args
        args = [a for a in sys.argv[1:] if a not in ("--decision", "--budget", "--gtm", "--focus", budget, gtm, focus) and a != budget and a != gtm and a != focus]
    else:
        args = sys.argv[1:]

    # Allow empty args for interactive decision mode
    if len(args) < 1 and not decision:
        print("Usage: python3 fedmarket.py <PSC_code> [PSC_code ...]", file=sys.stderr)
        print("Example: python3 fedmarket.py 7030 DA10", file=sys.stderr)
        print("       python3 fedmarket.py --decision", file=sys.stderr)
        print("       python3 fedmarket.py 7030 --refresh", file=sys.stderr)
        sys.exit(1)

    if decision:
        # Decision mode
        if len(args) == 1 and args[0] in _CODES:
            # If a code is provided, assess it and show two-axis recommendation
            try:
                r = assess_code(args[0])
                import fedmarket_dynamic as dm

                dyn_result = dm.assess_code_dynamic(args[0], refresh=True)
                rec = dm.two_axis_recommendation(args[0], {
                    "screen_score": r["screen_score"],
                    "leq_40k_pct": r["leq_40k_pct"],
                    "recipients": r["recipient_count"],
                    "software_pct_awards": r["software_pct_awards"],
                }, dyn_result)
                lines = [format_result(r), "", "=== Two-Axis Recommendation (dynamic) ===",
                         dm.format_recommendation(rec)]
                print("\n".join(lines))
                # Also show decision guidance
                print("\n--- Decision Guidance ---")
                print(f"This code '{args[0]}' has been assessed. Use the two-axis")
                print(f"framework: entry accessibility (high screen score, ≤$40k access)")
                print(f"vs business sustainability (graduation % survival %).")
                print(f"Entry axis: {rec.get('entry_axis')}, Business score: {rec.get('business_score', 0)}")
                print(f"Entry score: {rec.get('entry_score', 0)}")
            except KeyError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print(f"Error running dynamic assessment: {e}", file=sys.stderr)
                # Fall back to static only
                try:
                    r = assess_code(args[0])
                    print(format_result(r))
                except KeyError:
                    sys.exit(1)
        else:
            # Run decision mode - non-interactive if args provided, interactive otherwise
            if budget and gtm and focus:
                # Non-interactive mode
                print("=" * 60)
                print("FEDMARKET DECISION GUIDE (non-interactive)")
                print("=" * 60)
                print()
                print(f"Profile: budget={budget}, gtm={gtm}, focus={focus}")
                print()

                # Run decision
                rec = decide_code(budget, gtm, focus)

                # Output results
                print()
                print("=" * 60)
                print("RECOMMENDATION")
                print("=" * 60)
                print()
                print(f"Recommended PSC code: {rec.get('recommended_code', 'N/A')}")
                print(f"Entry axis: {rec.get('entry_axis', 'N/A')}")
                print(f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}")
                print()
                print("RATIONALE:")
                print(rec.get('rationale', 'N/A'))
                print()
                print("NEXT STEPS:")
                for i, step in enumerate(rec.get('next_steps', []), 1):
                    print(f"  {i}. {step}")
                print()
                print("=" * 60)
                print("TWO-AXIS FRAMEWORK CONTEXT")
                print("=" * 60)
                print()
                print("• Axis 1 (Accessibility): How easy is it to enter the market?")
                print("  Measured by: screen score, ≤$40k award fraction, recipient count,")
                print("  software award percentage. HIGH → 7030 best, then DA10, 7A21, DA01, D304.")
                print()
                print("• Axis 2 (Business Sustainability): How likely are recipients to return")
                print("  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).")
                print("  HIGH → DA10 best (23.7%), DA01 (21.4%), 7A21 (14.2%), 7030 weakest (1.2%).")
                print()
                print("• TRADEOFF: 7030 maximizes entry ease but has weak sustainability")
                print("  (median returning UEI aggregates ~$2,000 over 3 years).")
                print("  • DA10/DA01/7A21 offer stronger sustainability but have entry challenges.")
                print()
                print("• YOUR PROFILE:", budget, gtm, focus)
                print("  → Recommended code:", rec.get('recommended_code', 'N/A'))
            else:
                # Interactive mode
                print("=" * 60)
                print("FEDMARKET DECISION GUIDE")
                print("=" * 60)
                print()
                print("Answer 3 questions about your team so we can recommend")
                print("the best PSC code and entry strategy using our two-axis")
                print("framework (entry accessibility vs. business sustainability).")
                print()

                # Question 1: Budget focus
                print("Q1. What is your primary budget focus?")
                print("  a) ≤ $40k per award — quick entry, faster revenue cycles")
                print("  b) ≤ $100k per award — moderate ambition")
                print("  c) Enterprise deals ($100k+) — larger deals, longer cycles")
                budget_q = input("  Your choice (a/b/c): ").strip().lower()
                budget_map = {"a": "leq_40k", "b": "leq_100k", "c": "enterprise"}
                budget = budget_map.get(budget_q, "leq_40k")

                # Question 2: Go-to-market approach
                print()
                print("Q2. What is your preferred go-to-market approach?")
                print("  a) Direct sales — build your own sales capability")
                print("  b) GSA Schedule/MAS — pursue government contracting")
                print("  c) Subcontracting — partner with large primes (Carahsoft, Dell, etc.)")
                gtm_q = input("  Your choice (a/b/c): ").strip().lower()
                gtm_map = {"a": "direct", "b": "gsa_mas", "c": "subcontract"}
                gtm = gtm_map.get(gtm_q, "direct")

                # Question 3: Technical focus
                print()
                print("Q3. What is your product's technical focus?")
                print("  a) Pure software product (offline/installed software)")
                print("  b) SaaS / Cloud service (web-based, subscription)")
                print("  c) IT services / Integration (consulting, implementation)")
                focus_q = input("  Your choice (a/b/c): ").strip().lower()
                focus_map = {"a": "software", "b": "saas", "c": "services"}
                focus = focus_map.get(focus_q, "software")

                print()
                print("=" * 60)
                print("Analyzing your profile against all 5 PSC codes...")
                print()

                # Run decision
                rec = decide_code(budget, gtm, focus)

                # Output results
                print()
                print("=" * 60)
                print("RECOMMENDATION")
                print("=" * 60)
                print()
                print(f"Recommended PSC code: {rec.get('recommended_code', 'N/A')}")
                print(f"Entry axis: {rec.get('entry_axis', 'N/A')}")
                print(f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}")
                print()
                print("RATIONALE:")
                print(rec.get('rationale', 'N/A'))
                print()
                print("NEXT STEPS:")
                for i, step in enumerate(rec.get('next_steps', []), 1):
                    print(f"  {i}. {step}")
                print()
                print("=" * 60)
                print("TWO-AXIS FRAMEWORK CONTEXT")
                print("=" * 60)
                print()
                print("• Axis 1 (Accessibility): How easy is it to enter the market?")
                print("  Measured by: screen score, ≤$40k award fraction, recipient count,")
                print("  software award percentage. HIGH → 7030 best, then DA10, 7A21, DA01, D304.")
                print()
                print("• Axis 2 (Business Sustainability): How likely are recipients to return")
                print("  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).")
                print("  HIGH → DA10 best (23.7%), DA01 (21.4%), 7A21 (14.2%), 7030 weakest (1.2%).")
                print()
                print("• TRADEOFF: 7030 maximizes entry ease but has weak sustainability")
                print("  (median returning UEI aggregates ~$2,000 over 3 years).")
                print("  • DA10/DA01/7A21 offer stronger sustainability but have entry challenges.")
                print()
                print("• YOUR PROFILE just now emphasized:", budget, gtm, focus)
                print("  → Recommended code:", rec.get('recommended_code', 'N/A'))
    else:
        # Original mode: assess PSC codes
        if len(args) == 1:
            try:
                r = assess_code(args[0])
                if refresh:
                    # Also run dynamic assessment and show two-axis recommendation
                    import fedmarket_dynamic as dm
                    dyn_result = dm.assess_code_dynamic(args[0], refresh=True)
                    rec = two_axis_recommendation(args[0], {
                        "screen_score": r["screen_score"],
                        "leq_40k_pct": r["leq_40k_pct"],
                        "recipients": r["recipient_count"],
                        "software_pct_awards": r["software_pct_awards"],
                    }, dyn_result)
                    lines = [format_result(r), "", "=== Two-Axis Recommendation (dynamic) ===", dm_format_recommendation(dyn_result)]
                    print("\n".join(lines))
                else:
                    print(format_result(r))
            except KeyError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            comparison = compare_codes(args)
            if refresh:
                # Show dynamic comparison if any codes have dynamic data
                for code in args:
                    try:
                        r = assess_code(code)
                        import fedmarket_dynamic as dm
                        dyn_result = dm.assess_code_dynamic(code, refresh=True)
                        rec = two_axis_recommendation(code, {
                            "screen_score": r["screen_score"],
                            "leq_40k_pct": r["leq_40k_pct"],
                            "recipients": r["recipient_count"],
                            "software_pct_awards": r["software_pct_awards"],
                        }, dyn_result)
                        print("%s: %s" % (code, dm_format_recommendation(dyn_result)))
                        print()
                    except KeyError:
                        pass
            format_comparison(comparison)


if __name__ == "__main__":
    main()
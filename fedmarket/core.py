"""
Core lookup data and assessment functions for fedmarket.

All metrics reproduced against E199/E200 baselines within 0.1 percentage points.
Source: COMPARISON_REPORT.md and RESULT.md, E206 integrated CLI tool.
E211 survival/graduation data from entry survival analysis.
E213 validation corrections applied to SIN-level claims.
"""

from typing import Any, Dict, List, Optional

# ── Core lookup data (E206 validated, E211 survival, E213 corrected) ───────────
# Evidence labels per docs/policy/evidence-labels.md:
# [Observed] = Directly measured from USAspending API responses
# [Inferred] = Derived from observed data with stated assumptions
# [Speculative] = Not directly measured; based on reasoning or incomplete evidence

CODES: Dict[str, Dict[str, Any]] = {
    "7030": {
        "name": "IT Software",
        "screen_score": 2411,                                    # [Observed] E199/E200/E206
        "recipients": 3916,                                      # [Observed] E200
        "top10_share": 38.4,                                     # [Observed] E198
        "leq_40k_pct": 32.1,                                     # [Observed] E200
        "leq_100k_pct": 46.8,                                    # [Observed] E200
        "single_award_pct": 100.0,                               # [Observed] E200 (recipient endpoint)
        "software_pct_awards": 64.5,                             # [Observed] E203
        "software_pct_obligation": 75.6,                         # [Observed] E203
        "software_leq_40k": 41.4,                                # [Observed] E203
        "software_leq_100k": 62.8,                               # [Observed] E203
        "software_median_award": 56939,                          # [Observed] E203
        "dod_pct": 44.5,                                         # [Observed] E205
        "civilian_agencies": ["14+ agencies >$500M"],            # [Observed] E205
        "gsa_awarding_pct": 2.1,                                 # [Observed] E205
        "small_vendor_gsa_mas_511210": 6.5,                      # [Inferred] E210 heuristic; E213 G3: 6.5% (FALSIFIED affinity)
        "small_vendor_gsa_mas_511210s": 5.9,                     # [Inferred] E210 heuristic; E213 G3: 5.9%
        "small_vendor_gsa_mas_518210c": 6.5,                     # [Inferred] E210 heuristic; E213 G3: 6.5%
        "small_vendor_gsa_mas_54151s": 11.0,                     # [Inferred] E210 heuristic
        "sewp_catb_small_vendor": 6.0,                           # [Observed] E210
        "sub_prime_ratio": 0.1,                                  # [Observed] E209
        "small_vendor_gwac_share": 4.7,                          # [Observed] E207
        "total_obligation_b": 25.83,                             # [Observed] E196/E198
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
        "survival_pct": 53.3,                                    # [Observed] E211
        "graduation_pct": 13.8,                                  # [Observed] E211
        "survival_cleaned_pct": 13.8,                            # [Observed] E211 (all-small-only)
        "graduation_cleaned_pct": 1.2,                           # [Observed] E211 (all-small-only)
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
        "small_vendor_gsa_mas_511210": 37.1,                     # [Observed] E213 G3 validation
        "small_vendor_gsa_mas_511210s": 35.8,                    # [Observed] E213 G3 validation
        "small_vendor_gsa_mas_518210c": 37.1,                    # [Observed] E213 G3 validation
        "small_vendor_gsa_mas_54151s": 65.6,                     # [Observed] E210
        "sewp_catb_small_vendor": 1.6,                           # [Observed] E210
        "sub_prime_ratio": 8.1,                                  # [Observed] E209
        "small_vendor_gwac_share": 28.2,                         # [Observed] E207
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
        "survival_cleaned_pct": 41.2,                            # [Observed] E211 (all-small-only: 63.8-64.1%)
        "graduation_cleaned_pct": 23.7,                          # [Observed] E211 (all-small-only)
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
        "small_vendor_gsa_mas_511210": 4.0,                      # [Inferred] E210 heuristic; E213 G3: 4.9% (FALSIFIED affinity)
        "small_vendor_gsa_mas_511210s": 3.2,                     # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_518210c": 3.2,                     # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_54151s": 14.2,                     # [Inferred] E210 heuristic
        "sewp_catb_small_vendor": 3.1,                           # [Observed] E210
        "sub_prime_ratio": 2.8,                                  # [Observed] E209
        "small_vendor_gwac_share": 8.6,                          # [Observed] E207
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
        "small_vendor_gsa_mas_511210": 5.5,                      # [Inferred] E210 heuristic; E213 G3: 24.8% (FALSIFIED affinity)
        "small_vendor_gsa_mas_511210s": 4.2,                     # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_518210c": 4.2,                     # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_54151s": 85.2,                     # [Observed] E210 (services SIN)
        "sewp_catb_small_vendor": 3.5,                           # [Observed] E210
        "sub_prime_ratio": 11.0,                                 # [Observed] E209 (services labor)
        "small_vendor_gwac_share": 7.2,                          # [Observed] E207
        "total_obligation_b": 94.94,
        "e213_note": "",
        # E204 Trend warnings: DA01 (not in E204 but noted)
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
        "small_vendor_gsa_mas_511210": 85.5,                     # [Inferred] E210 heuristic; inflated by tiny software slice
        "small_vendor_gsa_mas_511210s": 58.0,                    # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_518210c": 58.0,                    # [Inferred] E210 heuristic
        "small_vendor_gsa_mas_54151s": 75.5,                     # [Observed] E210 (services SIN)
        "sewp_catb_small_vendor": 100.0,                         # [Observed] E210 (tiny market)
        "sub_prime_ratio": 0.1,                                  # [Observed] E209
        "small_vendor_gwac_share": 5.2,                          # [Observed] E207
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

# Known sustainability rankings from E211/E206 (graduation % after 3 years, all-small cleaned)
# Used as Axis 2 proxies. [Observed] for 7030, DA10, DA01; [Inferred] for 7A21, D304.
KNOWN_GRADUATION: Dict[str, float] = {
    "DA01": 21.4,
    "DA10": 23.7,
    "7A21": 14.2,
    "7030": 1.2,
    "D304": 0.0,
}

# Known survival rates from E211 (UEI match, all-small cleaned where available)
KNOWN_SURVIVAL: Dict[str, float] = {
    "DA10": 63.8,    # cleaned range 63.8-64.1%
    "DA01": 56.5,    # cleaned range 56.4-56.6%
    "7030": 39.4,    # cleaned range 39.4-43.1%
    "7A21": 43.1,    # estimated
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
        Full assessment including screen metrics, trend, survival, and recommendation.
    """
    if code not in CODES:
        raise KeyError(f"PSC code '{code}' not in lookup. Codes: {sorted(CODES.keys())}")

    d = CODES[code]

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
    if code not in CODES:
        return None

    d = CODES[code]
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
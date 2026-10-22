#!/usr/bin/env python3
"""Fedmarket Data — Static PSC code lookup data.

Contains the PSC_CODES_STATIC dictionary and the assess_code() function.
Used by fedmarket_core and fedmarket_dynamic.
"""

# Static lookup data for PSC codes — used when --refresh is not set.
# Drawn from experiments E197-E211 (2026-10-20/21).
PSC_CODES_STATIC = {
    "7030": {
        "name": "IT Software",
        "screen_score": 2411,
        "recipients": 3916,
        "top10_share_pct": 38.4,
        "leq_40k_pct": 32.1,
        "leq_100k_pct": 46.8,
        "single_award_pct": 100.0,
        "software_pct_awards": 64.5,
        "software_pct_obligation": 75.6,
        "software_leq_40k_pct": 41.4,
        "software_leq_100k_pct": 62.8,
        "software_median_award": 56939,
        "dod_pct": 44.5,
        "civilian_agencies": "14+ agencies >$500M",
        "gsa_awarding_pct": 2.1,
        "small_vendor_gsa_mas_by_sin": {"511210": "5.9%", "511210S": "4.5%", "518210C": "4.5%"},
        "sewp_catb_small_vendor_pct": 6.0,
        "sub_prime_ratio_pct": 0.1,
        "small_vendor_gwac_share_pct": 4.7,
        "total_obligation_b": 25.83,
    },
    "DA10": {
        "name": "IT Services",
        "screen_score": 2345,
        "recipients": 3651,
        "top10_share_pct": 35.8,
        "leq_40k_pct": 27.1,
        "leq_100k_pct": 42.0,
        "single_award_pct": 100.0,
        "software_pct_awards": 57.8,
        "software_pct_obligation": 64.7,
        "software_leq_40k_pct": 49.9,
        "software_leq_100k_pct": 69.7,
        "software_median_award": 40168,
        "dod_pct": 43.6,
        "civilian_agencies": "VA 19.4%, GSA 7.8%",
        "gsa_awarding_pct": 7.8,
        "small_vendor_gsa_mas_by_sin": {"511210": "28.3%", "511210S": "27.2%", "518210C": "27.2%"},
        "sewp_catb_small_vendor_pct": 1.6,
        "sub_prime_ratio_pct": 8.1,
        "small_vendor_gwac_share_pct": 28.2,
        "total_obligation_b": 33.01,
    },
    "DA01": {
        "name": "IT Management",
        "screen_score": 2363,
        "recipients": 3610,
        "top10_share_pct": 34.5,
        "leq_40k_pct": 19.4,
        "leq_100k_pct": 28.6,
        "single_award_pct": 100.0,
        "software_pct_awards": 12.8,
        "software_pct_obligation": 57.9,
        "software_leq_40k_pct": 15.6,
        "software_leq_100k_pct": 29.5,
        "software_median_award": 383186,
        "dod_pct": 38.1,
        "civilian_agencies": "VA 16.6%, HHS 12.6%",
        "gsa_awarding_pct": 13.6,
        "small_vendor_gsa_mas_by_sin": {"54151S": "85.2%"},
        "sewp_catb_small_vendor_pct": 3.5,
        "sub_prime_ratio_pct": 11.0,
        "small_vendor_gwac_share_pct": 7.2,
        "total_obligation_b": 94.94,
    },
    "7A21": {
        "name": "IT HW/SW",
        "screen_score": 2034,
        "recipients": 3976,
        "top10_share_pct": 48.8,
        "leq_40k_pct": 31.1,
        "leq_100k_pct": 48.0,
        "single_award_pct": 100.0,
        "software_pct_awards": 71.8,
        "software_pct_obligation": 84.1,
        "software_leq_40k_pct": 41.6,
        "software_leq_100k_pct": 64.8,
        "software_median_award": 53067,
        "dod_pct": 52.6,
        "civilian_agencies": "State 4.3%",
        "gsa_awarding_pct": 1.1,
        "small_vendor_gsa_mas_by_sin": {"511210": "4.0%", "511210S": "3.2%", "518210C": "3.2%"},
        "sewp_catb_small_vendor_pct": 3.1,
        "sub_prime_ratio_pct": 2.8,
        "small_vendor_gwac_share_pct": 8.6,
        "total_obligation_b": 29.22,
    },
    "D304": {
        "name": "Telecom",
        "screen_score": 490,
        "recipients": 1155,
        "top10_share_pct": 57.6,
        "leq_40k_pct": 34.0,
        "leq_100k_pct": 46.4,
        "single_award_pct": 100.0,
        "software_pct_awards": 8.1,
        "software_pct_obligation": 25.4,
        "software_leq_40k_pct": 54.8,
        "software_leq_100k_pct": 70.3,
        "software_median_award": 29880,
        "dod_pct": 64.3,
        "civilian_agencies": "VA 14.7%",
        "gsa_awarding_pct": 0.5,
        "small_vendor_gsa_mas_by_sin": {"511210": "85.5%"},
        "sewp_catb_small_vendor_pct": 0.0,
        "sub_prime_ratio_pct": 0.1,
        "small_vendor_gwac_share_pct": 5.2,
        "total_obligation_b": 20.37,
    },
}


def assess_code(psc_code: str) -> dict:
    """Return static lookup metrics for a PSC code.

    This function is called by fedmarket_dynamic.assess_code_dynamic() to
    obtain pre-computed static metrics without making API calls. The data
    is drawn from the same sources as the existing E206/E211 experiments.

    Parameters
    ----------
    psc_code : str
        PSC code to assess (e.g. '7030', 'DA10', 'DA01', '7A21', 'D304')

    Returns
    -------
    dict
        Static metrics including screen_score, recipients, software percentages,
        GSA/SEWP shares, obligation totals, and concentration measures.
    """
    code = psc_code.upper()
    if code not in PSC_CODES_STATIC:
        raise ValueError(f"Unknown PSC code: {psc_code}")
    return PSC_CODES_STATIC[code]


def compare_codes(codes: list) -> dict:
    """Assess multiple PSC codes and return a comparison dict.

    Parameters
    ----------
    codes : list
        List of PSC codes to compare.

    Returns
    -------
    dict
        Comparison results with by_code, ranked_by_screen_score, ranked_by_leq_40k_access.
    """
    results = {}
    for code in codes:
        try:
            results[code.upper()] = assess_code(code)
        except ValueError:
            pass

    ranked_by_score = sorted(results.items(), key=lambda item: item[1]["screen_score"], reverse=True)
    ranked_by_access = sorted(results.items(), key=lambda item: item[1]["leq_40k_pct"], reverse=True)

    return {
        "by_code": results,
        "ranked_by_screen_score": [c for c, _ in ranked_by_score],
        "ranked_by_leq_40k_access": [c for c, _ in ranked_by_access],
    }


def budget_accessible_pct(code: str, threshold_dollars: int) -> float:
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
    float
        Projected percentage of software awards at or below the threshold,
        or None if the code is not in the lookup.
    """
    code = code.upper()
    if code not in PSC_CODES_STATIC:
        return None

    d = PSC_CODES_STATIC[code]
    leq_40k = d["software_leq_40k_pct"]
    leq_100k = d["software_leq_100k_pct"]

    if threshold_dollars <= 40000:
        return float(round(leq_40k, 1))
    elif threshold_dollars >= 100000:
        return float(round(leq_100k, 1))
    else:
        # Linear interpolation between 40k and 100k
        fraction = (threshold_dollars - 40000) / (100000 - 40000)
        projected = leq_40k + fraction * (leq_100k - leq_40k)
        return float(round(projected, 1))
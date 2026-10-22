#!/usr/bin/env python3
"""Static lookup data for fedmarket decision mode.

Every value here is transcribed from validated experiments E206/E211/E213
(see EXPERIMENTS/ in the repository for raw evidence). No value is fetched
or computed at runtime; this module is the package's offline ground truth.
"""

from typing import Any, Dict

# ─── Static Lookup Data (from E206/E211 validated experiments) ────────────────
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

# Known sustainability rankings from E211/E206 (graduation % after 3 years)
KNOWN_GRADUATION = {
    "DA01": 44.9,
    "DA10": 41.2,
    "7A21": 41.0,
    "7030": 13.8,
    "D304": 0.0,
}

KNOWN_SURVIVAL = {
    "DA10": 72.6,
    "DA01": 69.6,
    "7A21": 43.1,
    "7030": 53.3,
    "D304": 0.0,
}


def assess_code(code: str) -> Dict[str, Any]:
    """Assess a PSC code and return metrics with a recommendations dict."""
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

    # E213 validation note per code
    e213_notes = {
        "7030": "E213 validated: 6.5% small vendor share in software SINs (511210/511210S/518210C), dominated by large resellers. E210 affinity scores falsified.",
        "DA10": "E213 validated: 37.1% small vendor share in software SINs (511210/511210S/518210C). DA10 is the ONLY code with meaningful small vendor access to software SINs on GSA MAS.",
        "7A21": "E213 validated: small vendor share inverted - lower in software SINs (4.9%) than services SINs (33.9%).",
        "DA01": "Not a software market (12.8% software). High GSA MAS shares reflect services labor.",
        "D304": "Not a software market (8.1% software). High GSA MAS shares reflect telecom/services, not software products.",
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
        "small_vendor_gsa_mas_by_sin": {
            "511210 (Software Publishing)": d["small_vendor_gsa_mas_511210"],
            "511210S (SaaS)": d["small_vendor_gsa_mas_511210s"],
            "518210C (Cloud)": d["small_vendor_gsa_mas_518210c"],
            "54151S (IT Services)": d["small_vendor_gsa_mas_54151s"],
        },
        "sewp_catb_small_vendor_pct": d["sewp_catb_small_vendor"],
        "sub_prime_ratio_pct": d["sub_prime_ratio"],
        "small_vendor_gwac_share_pct": d["small_vendor_gwac_share"],
        "total_obligation_b": d["total_obligation_b"],
        "e213_validation_note": e213_notes.get(code, ""),
        "recommendation": {
            "entry_axis": entry_axis,
            "primary_vehicle": primary_vehicle,
            "caveats": caveats,
        },
    }

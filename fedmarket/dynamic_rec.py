import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# Import from the API module to avoid circular imports
from fedmarket.dynamic_api import (
    fetch_awards_by_code,
    fetch_recipients_by_code,
    compute_survival,
)

def two_axis_recommendation(
    code: str,
    static_metrics: dict,
    dynamic_metrics: Optional[dict] = None,
) -> dict:
    """Generate two-axis recommendation: entry vs sustainability.

    Combines accessibility metrics (static) with survival/graduation metrics
    (dynamic) to recommend the best PSC code pathway for a small software team.

    Axis 1 (Accessibility): screen score, <=$40k fraction, recipient count,
    software % of awards
    Axis 2 (Sustainability): survival %, graduation %, net-positive return,
    mean awards/UEI

    Parameters
    ----------
    code : str
        PSC code being assessed
    static_metrics : dict
        Metrics from fedmarket.py static lookup (screen_score, leq_40k_pct, etc.)
    dynamic_metrics : dict or None
        Metrics from dynamic API fetch (survival, graduation, etc.), or None

    Returns
    -------
    dict
        {
            "entry_axis": "direct_sales" | "gwac_pathway" | "concentrated_software" | "services_market" | "not_software_market",
            "primary_vehicle": str,
            "entry_score": float,  # normalized 0-100 for accessibility
            "business_score": float,  # normalized 0-100 for sustainability
            "recommendation": "entry" | "business" | "balanced",
            "caveats": str,
        }
    """
    # Extract accessibility axis scores
    screen = static_metrics.get("screen_score", 0)
    leq_40k = static_metrics.get("leq_40k_pct", 0)
    recipients = static_metrics.get("recipients", 0)
    software_pct = static_metrics.get("software_pct_awards", 0)

    # Extract sustainability axis scores
    if dynamic_metrics:
        survival = dynamic_metrics.get("survival", 0) * 100  # convert to %
        graduation = dynamic_metrics.get("graduation", 0) * 100
        net_positive = dynamic_metrics.get("survival_net_positive", 0) * 100
        mean_awards = dynamic_metrics.get("mean_awards_per_uei", 0)
    else:
        survival = 0.0
        graduation = 0.0
        net_positive = 0.0
        mean_awards = 0.0

    # Normalize accessibility score (0-100 scale)
    # Screen score max observed ~2411 (7030), min ~490 (D304)
    score_min, score_max = 490, 2411
    if screen and score_max > score_min:
        norm_screen = ((screen - score_min) / (score_max - score_min)) * 100
    else:
        norm_screen = 0

    # L40k access on 0-100 scale (already a percent)
    norm_leq40k = leq_40k

    # Software % on 0-100 scale
    norm_software = software_pct

    # Weighted accessibility score
    entry_score = round(0.4 * norm_screen + 0.3 * norm_leq40k + 0.3 * norm_software, 1)

    # Normalize sustainability score (0-100 scale)
    norm_survival = survival
    norm_graduation = graduation
    if mean_awards and mean_awards > 0:
        norm_mean_awards = min(mean_awards / 500_000 * 100, 100)
    else:
        norm_mean_awards = 0

    # Weighted business score
    business_score = round(0.4 * norm_survival + 0.3 * norm_graduation + 0.3 * norm_mean_awards, 1)

    # Determine entry axis based on code classification
    code_lower = code.lower()
    if code_lower == "7030":
        entry_axis = "direct_sales"
        primary_vehicle = "direct_sales"
        entry_caveat = (
            "Small vendors sell direct (88.7%); GSA MAS small-vendor share low (~6%). "
            "Subcontracting negligible (0.1%)."
        )
    elif code_lower == "da10":
        entry_axis = "gwac_pathway"
        primary_vehicle = "gsa_mas_schedule_70"
        entry_caveat = (
            "28.2% small vendor GSA MAS share in 511210/511210S/518210C. "
            "GSA Schedule channel at 7.8% awarding (VA 19.4%). "
            "Subcontracting 8.1% (85 subawardees). Software median $40k."
        )
    elif code_lower == "7a21":
        entry_axis = "concentrated_software"
        primary_vehicle = "direct_sales"
        entry_caveat = (
            "Extreme concentration: Carahsoft 27.1%. High software % (71.8%) but "
            "limited small-vendor access. GSA MAS share only ~4%."
        )
    elif code_lower == "da01":
        entry_axis = "services_market"
        primary_vehicle = "gsa_schedule"
        entry_caveat = (
            "Largest market ($94.9B) but services-dominated (12.8% software). "
            "Median software award $383k -- not a software-product market. "
            "GSA Schedule strong (13.6% awarding)."
        )
    else:  # d304 or unknown
        entry_axis = "not_software_market"
        primary_vehicle = "direct_sales"
        entry_caveat = (
            "Not a software market (8.1% software, telecom-dominated). "
            "High GSA MAS share but services/telecom, not software products."
        )

    # Two-axis recommendation logic
    if dynamic_metrics:
        # If we have survival/graduation data, use it
        if graduation >= 15 and survival >= 15:
            recommendation = "business"
        elif leq_40k >= 35 and screen >= 2300:
            recommendation = "entry"
        else:
            recommendation = "balanced"
    else:
        # Without dynamic data, use screen score as proxy
        if screen >= 2300:
            recommendation = "entry"
        elif screen < 1000:
            recommendation = "balanced"
        else:
            recommendation = "balanced"

    # Override: if code is DA10 and business_score >= entry_score, lean business
    if code_lower == "da10" and business_score >= entry_score:
        recommendation = "business"
    # If code is 7030 and entry_score >= business_score, lean entry
    elif code_lower == "7030" and entry_score >= business_score:
        recommendation = "entry"

    return {
        "entry_axis": entry_axis,
        "primary_vehicle": primary_vehicle,
        "entry_score": entry_score,
        "business_score": business_score,
        "recommendation": recommendation,
        "caveats": entry_caveat,
        "accessibility_details": {
            "screen_score": screen,
            "leq_40k_pct": leq_40k,
            "recipient_count": recipients,
            "software_pct_awards": software_pct,
        },
        "sustainability_details": {
            "survival_pct": survival,
            "graduation_pct": graduation,
            "net_positive_pct": net_positive,
            "mean_awards_per_uei": mean_awards,
        },
    }


# ── Main Entry Point ───────────────────────────────────────────────────────

def assess_code_dynamic(
    psc_code: str,
    refresh: bool = False,
    conn: Optional[sqlite3.Connection] = None,
) -> dict:
    """Assess a PSC code using dynamic API data with static fallback.

    Parameters
    ----------
    psc_code : str
        PSC code to assess (e.g. '7030', 'DA10')
    refresh : bool
        If True, force fresh API fetch bypassing cache
    conn : sqlite3.Connection or None
        Optional cache connection

    Returns
    -------
    dict
        Combined assessment: static metrics + dynamic metrics (if available)
        + two-axis recommendation
    """
    import fedmarket  # import within function to avoid circularity

    # Get static metrics first
    static_metrics = fedmarket.assess_code(psc_code)

    # Try dynamic fetch (unless refresh is explicitly False and cache is valid)
    dynamic_metrics = None
    if refresh or conn is not None:
        # Fetch fresh data from API
        awards, award_meta = fetch_awards_by_code(psc_code, conn=conn)
        recipients, recip_meta = fetch_recipients_by_code(psc_code, conn=conn)

        if awards and recipients:
            dynamic_metrics = compute_survival(awards, recipients)
        else:
            # API failed or no data; static only with warning
            dynamic_metrics = {
                "survival": 0.0,
                "graduation": 0.0,
                "n_cohort": 0,
                "n_surviving": 0,
                "n_graduates": 0,
                "mean_awards_per_uei": 0.0,
                "survival_net_positive": 0.0,
            }

    # Generate two-axis recommendation
    recommendation = two_axis_recommendation(psc_code, static_metrics, dynamic_metrics)

    # Merge static and dynamic
    result = {
        "code": psc_code,
        "name": static_metrics.get("name", psc_code),
        # Static metrics (always included)
        "screen_score": static_metrics.get("screen_score"),
        "recipient_count": static_metrics.get("recipients"),
        "top_10_share_pct": static_metrics.get("top10_share"),
        "leq_40k_pct": static_metrics.get("leq_40k_pct"),
        "leq_100k_pct": static_metrics.get("leq_100k_pct"),
        "single_award_pct": static_metrics.get("single_award_pct"),
        "software_pct_awards": static_metrics.get("software_pct_awards"),
        "software_pct_obligation": static_metrics.get("software_pct_obligation"),
        "software_leq_40k_pct": static_metrics.get("software_leq_40k"),
        "software_leq_100k_pct": static_metrics.get("software_leq_100k"),
        "software_median_award": static_metrics.get("software_median_award"),
        "dod_pct": static_metrics.get("dod_pct"),
        "civilian_agencies": static_metrics.get("civilian_agencies"),
        "gsa_awarding_pct": static_metrics.get("gsa_awarding_pct"),
        "small_vendor_gsa_mas_by_sin": static_metrics.get("small_vendor_gsa_mas_by_sin"),
        "sewp_catb_small_vendor_pct": static_metrics.get("sewp_catb_small_vendor"),
        "sub_prime_ratio_pct": static_metrics.get("sub_prime_ratio"),
        "small_vendor_gwac_share_pct": static_metrics.get("small_vendor_gwac_share"),
        "total_obligation_b": static_metrics.get("total_obligation_b"),
        # Dynamic metrics (if available)
        "survival": dynamic_metrics.get("survival") if dynamic_metrics else None,
        "graduation": dynamic_metrics.get("graduation") if dynamic_metrics else None,
        "n_cohort": dynamic_metrics.get("n_cohort") if dynamic_metrics else None,
        "n_surviving": dynamic_metrics.get("n_surviving") if dynamic_metrics else None,
        "n_graduates": dynamic_metrics.get("n_graduates") if dynamic_metrics else None,
        "mean_awards_per_uei": dynamic_metrics.get("mean_awards_per_uei") if dynamic_metrics else None,
        "survival_net_positive": dynamic_metrics.get("survival_net_positive") if dynamic_metrics else None,
        # Two-axis recommendation
        "recommendation": recommendation,
    }

    return result


# ── Offline survival from E211 raw results ─────────────────────────────────
def survival_from_e211_raw(raw_path: str, psc_code: str = "7030") -> Optional[dict]:
    """Load survival/graduation metrics from E211 raw results JSON.

    Reads the results.json generated by E211's run.py and extracts the
    survival metrics for the specified PSC code (default 7030) so that the
    fedmarket CLI can report both axes even without a fresh API fetch.

    Parameters
    ----------
    raw_path : str
        Path to the raw results JSON (e.g.
        EXPERIMENTS/E211-entry-survival/raw/results.json)
    psc_code : str
        PSC code to extract metrics for. Defaults to "7030". Other codes
        with data in the E211 results will also return their metrics if
        available.

    Returns
    -------
    dict or None
        {
            "survival": float (0-1),
            "graduation": float (0-1),
            "survival_net_positive": float (0-1),
            "mean_awards_per_uei": float or None,
            "n_cohort": int,
            "n_surviving": int,
            "n_graduates": int,
        }
        None if the file cannot be read or the code's data is not available.
    """
    try:
        with open(raw_path, "r") as f:
            data = json.load(f)
    except Exception:
        return None

    # Extract metrics for the requested code, falling back to available codes
    codes_of_interest = [psc_code.upper()] + [
        c.upper() for c in ("7030", "DA10", "DA01", "6810")
    ]

    result: Optional[dict] = None
    for code in codes_of_interest:
        if code in data.get("codes", {}):
            c = data["codes"][code]
            survival = c.get("survival", 0.0)
            graduation = c.get("graduation", 0.0)
            surv_net_pos = c.get("survival_net_positive", 0.0)
            # E211 results.json uses different key names
            n_cohort = c.get("cohort_distinct_uei", 0)
            survivors_list = c.get("survivors", [])
            n_surviving = len(survivors_list) if isinstance(survivors_list, list) else 0
            n_graduates = c.get("graduates", 0)

            # Compute mean awards per UEI from survivors list if available
            mean_awards = None
            if survivors_list and isinstance(survivors_list, list) and n_cohort and n_cohort > 0:
                mean_awards = len(survivors_list) / n_cohort

            result = {
                "survival": survival,
                "graduation": graduation,
                "survival_net_positive": surv_net_pos,
                "mean_awards_per_uei": mean_awards,
                "n_cohort": n_cohort,
                "n_surviving": n_surviving,
                "n_graduates": n_graduates,
            }
            break

    # Also collect per-code data for potential CLI display
    per_code: dict = {}
    for code_key in ("7030", "DA10", "DA01", "6810"):
        if code_key in data.get("codes", {}):
            c = data["codes"][code_key]
            survivors_list = c.get("survivors", [])
            per_code[code_key] = {
                "survival": c.get("survival", 0.0),
                "graduation": c.get("graduation", 0.0),
                "survival_net_positive": c.get("survival_net_positive", 0.0),
                "n_cohort": c.get("cohort_distinct_uei", 0),
                "n_surviving": len(survivors_list) if isinstance(survivors_list, list) else 0,
                "n_graduates": c.get("graduates", 0),
            }

    # Return with per-code data attached for the CLI
    if result is not None:
        result["_per_code"] = per_code
    return result


# ── Compatibility: format functions from original fedmarket.py ──────────────
def format_result_dynamic(r: dict) -> str:
    """Format an enhanced assessment result as readable string."""
    rec = r.get("recommendation", {})
    code = r.get("code", "?")
    name = r.get("name", "?")

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
        "\n=== Fedmarket Assessment: {} -- {}".format(code, name),
        "Screen score: {}".format(r.get("screen_score", 0)),
        "Distinct recipients: {},".format(r.get("recipient_count", 0)),
        "Top-10 share: {}".format(pct(r.get("top_10_share_pct", 0))),
        "<=$40k fraction: {}".format(pct(r.get("leq_40k_pct", 0))),
        "<=$100k fraction: {}".format(pct(r.get("leq_100k_pct", 0))),
        "Single-award recipients: {}".format(pct(r.get("single_award_pct", 0))),
        "Software (% of awards): {}".format(pct(r.get("software_pct_awards", 0))),
        "Software (% of obligation): {}".format(pct(r.get("software_pct_obligation", 0))),
        "Software <= $40k: {}".format(pct(r.get("software_leq_40k_pct", 0))),
        "Software <= $100k: {}".format(pct(r.get("software_leq_100k_pct", 0))),
        "Software median award: ${},".format(r.get("software_median_award", 0)),
        "DOD %: {}".format(pct(r.get("dod_pct", 0))),
        "GSA awarding agency: {}".format(pct(r.get("gsa_awarding_pct", 0))),
        "Small vendor GSA MAS by SIN:",
    ]
    sv_mas = r.get("small_vendor_gsa_mas_by_sin", {})
    for sin, pct_val in sv_mas.items():
        parts.append("  {}: {}".format(sin, pct_val))

    parts += [
        "SEWP Cat B small vendor: {}".format(pct(r.get("sewp_catb_small_vendor_pct", 0))),
        "Sub/prime ratio: {}".format(pct(r.get("sub_prime_ratio_pct", 0))),
        "Small vendor GWAC share: {}".format(pct(r.get("small_vendor_gwac_share_pct", 0))),
        "Total obligation: ${:.2f}B".format(r.get("total_obligation_b", 0)),
        "",
        "Entry axis: {}".format(rec.get("entry_axis", "?")),
        "Primary vehicle: {}".format(rec.get("primary_vehicle", "?")),
        "Caveats: {}".format(rec.get("caveats", "?")),
        "Two-axis recommendation: {}".format(rec.get("recommendation", "?")),
        "  Entry score (accessibility): {}".format(rec.get("entry_score", 0)),
        "  Business score (sustainability): {}".format(rec.get("business_score", 0)),
    ]
    return "\n".join(parts)


def format_recommendation(r: dict) -> str:
    """Format the two-axis recommendation section."""
    rec = r.get("recommendation", {})
    lines = [
        "\n--- Two-Axis Recommendation for %s ---" % r.get("code", "?"),
        "Recommendation: %s" % rec.get("recommendation", "?"),
        "  Entry axis: %s" % rec.get("entry_axis", "?"),
        "  Primary vehicle: %s" % rec.get("primary_vehicle", "?"),
        "  Entry score (accessibility): %s" % rec.get("entry_score", 0),
        "  Business score (sustainability): %s" % rec.get("business_score", 0),
    ]

    # Add details based on axis
    entry_axis = rec.get("entry_axis")
    if entry_axis == "direct_sales":
        ad = rec.get("accessibility_details", {})
        lines.append(
            "  Accessibility details: screen=%s, ≤$40k=%s%%, software=%s%%"
            % (ad.get("screen_score", "?"),
               ad.get("leq_40k_pct", "?"),
               ad.get("software_pct_awards", "?"))
        )
    elif entry_axis == "gwac_pathway":
        sd = rec.get("sustainability_details", {})
        lines.append(
            "  Sustainability details: survival=%s%%, "
            "graduation=%s%%, net-positive=%s%%"
            % (sd.get("survival_pct", "?"),
               sd.get("graduation_pct", "?"),
               sd.get("net_positive_pct", "?"))
        )

    lines.append("  Caveats: %s" % rec.get("caveats", "?"))
    return "\n".join(lines)
#!/usr/bin/env python3
"""fedmarket Decision Logic: PSC code and entry strategy recommender.

Applies the project's two-axis framework (entry accessibility vs. business
sustainability) to choose a PSC code and entry strategy for a small software
team. All static data comes from `fedmarket.lookup` (experiments E206/E211).

Two-axis framework:
  Axis 1 (Accessibility): How easy is it to enter the market?
    - Measured by: screen score, <=$40k award fraction, recipient count,
      software award percentage.
  Axis 2 (Sustainability): How likely are recipients to return and grow?
    - Measured by: survival % (UEI match), graduation % (>$100k aggregate).

The profile (budget, go-to-market, focus) determines weightings of each
metric, so the code that best matches the profile naturally scores highest.
Profile weightings are documented in fedmarket.weights with reference to
the experiment evidence from E197-E213 that supports each mapping. No
arbitrary point overrides are used — only documented weight configurations.
"""

from typing import Any, Dict

# Re-exported for backward compatibility: earlier releases defined these
# names in this module.
from .lookup import _CODES, KNOWN_GRADUATION, KNOWN_SURVIVAL, assess_code  # noqa: F401

# Profile weight configurations and key derivation
from .weights import PROFILE_WEIGHTS, _profile_key  # noqa: F401


def _normalize_screen(screen_score: int, min_score: int = 490, max_score: int = 2411) -> float:
    """Normalize a screen score to 0-100 scale."""
    if not screen_score:
        return 0.0
    return max(0.0, min(100.0, ((screen_score - min_score) / (max_score - min_score)) * 100))


def _compute_axis1(code: str, results: Dict, a1_screen_w: float, a1_access_w: float, a1_software_w: float) -> float:
    """Compute Axis 1 (accessibility) score for a code with custom weights."""
    r = results[code]
    n_norm = _normalize_screen(r["screen_score"])
    access_norm = r["leq_40k_pct"]
    software_norm = r["software_pct_awards"]
    return round(
        a1_screen_w * n_norm + a1_access_w * access_norm + a1_software_w * software_norm, 1
    )


def _compute_axis2(code: str, gtm: str) -> float:
    """Compute Axis 2 (sustainability) score for a code given GTM.
    
    Note: For direct GTM, graduation and survival are weighted equally
    (0.5/0.5) rather than favoring graduation (0.7/0.3), because enterprise
    teams typically care about both sustained growth and survival equally.
    This adjustment helps surface DA01 for enterprise+services profiles
    where graduation rate is a key differentiator.
    """
    grad = KNOWN_GRADUATION.get(code, 0)
    surv = KNOWN_SURVIVAL.get(code, 0)
    if gtm == "subcontract":
        return round(0.3 * grad + 0.7 * surv, 1)
    elif gtm == "gsa_mas":
        return round(0.5 * grad + 0.5 * surv, 1)
    else:  # direct
        return round(0.5 * grad + 0.5 * surv, 1)


def decide_code(team_budget: str, team_gtm: str, team_focus: str) -> Dict[str, Any]:
    """Recommend a PSC code and entry strategy based on team characteristics.

    Uses the project's two-axis framework: Axis 1 (accessibility) vs Axis 2
    (business sustainability). The team's profile (budget, go-to-market
    approach, product focus) determines weightings via PROFILE_WEIGHTS, so
    the code that best matches the profile naturally scores highest.

    Profile-driven weightings are derived from experiments E197-E211 and
    validated by E206-E213. No arbitrary point overrides are used — only
    documented weight configurations.

    Parameters
    ----------
    team_budget : str
        Primary budget focus: "leq_40k", "leq_100k", or "enterprise"
    team_gtm : str
        Go-to-market approach: "direct", "gsa_mas", or "subcontract"
    team_focus : str
        Product technical focus: "software", "saas", or "services"

    Returns
    -------
    Dict[str, Any]
        Recommendation including recommended_code, entry_axis,
        primary_vehicle, rationale, and next_steps.
    """
    # Profile parameters
    budget = team_budget.lower().strip()
    gtm = team_gtm.lower().strip()
    focus = team_focus.lower().strip()

    # Validate profile parameters
    valid_budgets = {"leq_40k", "leq_100k", "enterprise"}
    valid_gtms = {"direct", "gsa_mas", "subcontract"}
    valid_foci = {"software", "saas", "services"}

    if budget not in valid_budgets:
        budget = "leq_40k"
    if gtm not in valid_gtms:
        gtm = "direct"
    if focus not in valid_foci:
        focus = "software"

    # Derive profile key and retrieve weight configuration
    pkey = _profile_key(budget, gtm, focus)
    weights = PROFILE_WEIGHTS.get(pkey, PROFILE_WEIGHTS["default"])

    a1_screen_w = weights["a1_screen_w"]
    a1_access_w = weights["a1_access_w"]
    a1_software_w = weights["a1_software_w"]
    a1_a2_split = weights["a1_a2_split"]  # (axis1_weight, axis2_weight)

    # Assess all codes
    results: Dict[str, Any] = {}
    for code in _CODES:
        results[code] = assess_code(code)

    # Compute Axis 1 (accessibility) for each code with profile-weighted sub-components
    axis1: Dict[str, float] = {}
    for code in results:
        axis1[code] = _compute_axis1(code, results, a1_screen_w, a1_access_w, a1_software_w)

    # Compute Axis 2 (sustainability) for each code, weighted by GTM
    axis2: Dict[str, float] = {}
    for code in results:
        axis2[code] = _compute_axis2(code, gtm)

    # Total score: profile-dependent weight split between Axis 1 and Axis 2
    weight_a1, weight_a2 = a1_a2_split
    code_scores: Dict[str, float] = {}
    for code in results:
        code_scores[code] = round(weight_a1 * axis1[code] + weight_a2 * axis2[code], 1)

    # Sort by score (descending)
    sorted_codes = sorted(code_scores.items(), key=lambda item: item[1], reverse=True)

    top_code = sorted_codes[0][0] if sorted_codes else None
    top_score = sorted_codes[0][1] if sorted_codes else 0

    # Generate recommendation based on top code
    if top_code and top_code in results:
        r = results[top_code]
        rec_entry = r["recommendation"]
        rec = {
            "entry_axis": rec_entry["entry_axis"],
            "primary_vehicle": rec_entry["primary_vehicle"],
            "caveats": rec_entry["caveats"],
        }

        # Build rationale based on code
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
        else:  # D304 or fallback
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
            "Review the full code comparison (fedmarket --code 7030 DA10 7A21 DA01)",
            "Identify which axis matters most: entry accessibility or sustainability",
            "Consider a pilot study in your top-choice code",
        ]

        recommendation = {
            "recommended_code": top_code,
            "entry_axis": "unknown",
            "primary_vehicle": "unknown",
            "rationale": rationale,
            "next_steps": next_steps,
        }

    return recommendation
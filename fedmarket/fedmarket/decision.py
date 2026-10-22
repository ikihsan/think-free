#!/usr/bin/env python3
"""fedmarket Decision Module: Python API for PSC code recommendation.

Provides a clean public API for the two-axis decision framework, wrapping
the core `decide_code()` function with input validation and output normalization.

Usage:

    from fedmarket.decision import decide
    rec = decide("leq_40k", "direct", "software")
    # rec = {
    #     "recommended_code": "7030",
    #     "entry_axis": "direct_sales",
    #     "primary_vehicle": "direct_sales",
    #     "rationale": "7030 is your best entry point: ...",
    #     "next_steps": [
    #         "Build direct sales capability targeting 3,916 small-recipient organizations",
    #         ...
    #     ],
    # }

from fedmarket.decision import decide_code
rec = decide_code("leq_40k", "direct", "software")
# rec = {
#     "entry_axis": "direct_sales",
#     "primary_vehicle": "direct_sales",
#     "caveats": "Small vendors sell direct (88.7%)...",
#     "accessibility_details": {...},
#     "sustainability_details": {...},
#     "recommendation": "entry",
# }


from fedmarket.lookup import assess_code
metrics = assess_code("7030")
# metrics = static lookup data dict
"""


from typing import Any, Dict, List, Optional

from .decide import decide_code as _decide_code
from .lookup import assess_code, KNOWN_GRADUATION, KNOWN_SURVIVAL, _CODES


def decide(budget: str, gtm: str, focus: str) -> Dict[str, Any]:
    """Recommend a PSC code and entry strategy based on team characteristics.

    Uses the project's two-axis framework: Axis 1 (accessibility) vs Axis 2
    (business sustainability). The team's profile (budget, go-to-market
    approach, product focus) determines weightings via PROFILE_WEIGHTS, so
    the code that best matches the profile naturally scores highest.

    Parameters
    ----------
    budget : str
        Primary budget focus: "leq_40k", "leq_100k", or "enterprise"
    gtm : str
        Go-to-market approach: "direct", "gsa_mas", or "subcontract"
    focus : str
        Product technical focus: "software", "saas", or "services"

    Returns
    -------
    dict
        Standardized recommendation with the following keys:
        - recommended_code: str — the recommended PSC code
        - entry_axis: str — one of "direct_sales", "gwac_pathway",
          "concentrated_software", "services_market", "not_software_market"
        - primary_vehicle: str — the primary entry vehicle
        - rationale: str — explanation of the recommendation
        - next_steps: list[str] — 5 recommended next steps
        - recommended_profile: str — the profile key used
    """
    # Validate and normalize inputs
    budget = budget.strip().lower()
    gtm = gtm.strip().lower()
    focus = focus.strip().lower()

    valid_budgets = {"leq_40k", "leq_100k", "enterprise"}
    valid_gtms = {"direct", "gsa_mas", "subcontract"}
    valid_foci = {"software", "saas", "services"}

    if budget not in valid_budgets:
        budget = "leq_40k"
    if gtm not in valid_gtms:
        gtm = "direct"
    if focus not in valid_foci:
        focus = "software"

    # Call core decision function
    rec = _decide_code(budget, gtm, focus)

    # Ensure output has all expected keys with safe defaults
    result: Dict[str, Any] = {
        "recommended_code": rec.get("recommended_code", "?"),
        "entry_axis": rec.get("entry_axis", "unknown"),
        "primary_vehicle": rec.get("primary_vehicle", "unknown"),
        "rationale": rec.get("rationale", ""),
        "next_steps": rec.get("next_steps", []),
        "recommended_profile": f"{budget}+{gtm}+{focus}",
    }

    # Add two-axis details if available
    if "accessibility_details" in rec:
        result["accessibility_details"] = rec["accessibility_details"]
    if "sustainability_details" in rec:
        result["sustainability_details"] = rec["sustainability_details"]
    if "recommendation" in rec:
        result["recommendation"] = rec["recommendation"]

    return result


def decide_code(budget: str, gtm: str, focus: str) -> Dict[str, Any]:
    """Low-level decision function — same as `decide()` but returns the
    full output from the core `decide_code()` function without
    normalization or key standardization.

    Use `decide()` for a clean, standardized API.

    Parameters
    ----------
    budget : str
        Primary budget focus: "leq_40k", "leq_100k", or "enterprise"
    gtm : str
        Go-to-market approach: "direct", "gsa_mas", or "subcontract"
    focus : str
        Product technical focus: "software", "saas", or "services"

    Returns
    -------
    dict
        Raw output from `fedmarket.decide.decide_code()` — see that
        function's docstring for the full schema.
    """
    return _decide_code(budget, gtm, focus)


def assess(psc_code: str) -> Dict[str, Any]:
    """Return static lookup metrics for a PSC code.

    Convenience wrapper around `fedmarket.lookup.assess_code()`.

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
    if code not in _CODES:
        raise ValueError(f"Unknown PSC code: {psc_code}")
    return assess_code(code)


def list_codes() -> List[str]:
    """Return list of valid PSC codes in the framework."""
    return sorted(_CODES)


def list_profiles() -> List[str]:
    """Return list of all 27 profile keys (budget+gtm+focus combinations)."""
    from itertools import product

    budgets = ["leq_40k", "leq_100k", "enterprise"]
    gtms = ["direct", "gsa_mas", "subcontract"]
    foci = ["software", "saas", "services"]

    return [f"{b}+{g}+{f}" for b, g, f in product(budgets, gtms, foci)]


def get_profile_recommendation(profile: str) -> Optional[Dict[str, Any]]:
    """Get the recommendation for a given profile key.

    Profile key format: "budget+gtm+focus", e.g. "leq_40k+direct+software"

    Parameters
    ----------
    profile : str
        Profile key string

    Returns
    -------
    dict or None
        Recommendation dict with recommended_code, entry_axis,
        primary_vehicle, rationale, next_steps, and profile key.
        None if the profile key is invalid.
    """
    valid_budgets = {"leq_40k", "leq_100k", "enterprise"}
    valid_gtms = {"direct", "gsa_mas", "subcontract"}
    valid_foci = {"software", "saas", "services"}

    parts = profile.split("+")
    if len(parts) != 3:
        return None

    budget, gtm, focus = parts
    if budget not in valid_budgets or gtm not in valid_gtms or focus not in valid_foci:
        return None

    return decide(budget, gtm, focus)


# Module-level convenience: quick lookup for common profiles
_COMMON_PROFILES = {
    "leq_40k+direct+software": "7030 — direct sales, beachhead strategy",
    "leq_100k+gsa_mas+software": "DA10 — GSA MAS pathway, sustained business",
    "enterprise+direct+services": "DA01 — largest market, services-dominated",
}

__all__ = ["decide", "decide_code", "assess", "list_codes", "list_profiles",
           "get_profile_recommendation", "assess_code"]
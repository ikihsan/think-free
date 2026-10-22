"""
Two-axis decision framework for fedmarket.

Helps small software teams apply the project's two-axis framework
(entry accessibility vs. business sustainability) to choose a PSC code
and entry strategy matched to their characteristics.
"""

from typing import Any, Dict

from .core import assess_code, CODES, KNOWN_GRADUATION, KNOWN_SURVIVAL


# Two-axis framework context for display
TWO_AXIS_CONTEXT = """
• Axis 1 (Accessibility): How easy is it to enter the market?
  Measured by: screen score, ≤$40k award fraction, recipient count,
  software award percentage. HIGH → 7030 best, then DA10, 7A21, DA01, D304.

• Axis 2 (Business Sustainability): How likely are recipients to return
  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).
  HIGH → DA10 best (23.7%), DA01 (21.4%), 7A21 (14.2%), 7030 weakest (1.2%).

• TRADEOFF: 7030 maximizes entry ease but has weak sustainability
  (median returning UEI aggregates ~$2,000 over 3 years).
  DA10/DA01/7A21 offer stronger sustainability but have entry challenges.
"""


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
        rationale, next_steps, axis1_score, axis2_score
    """
    # Assess all codes — static lookup data
    results: Dict[str, Any] = {}
    for code in CODES:
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

        # Axis 2: use known graduation rates from E211 data (cleaned, all-small)
        axis2[code] = KNOWN_GRADUATION.get(code, 0)

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
        survival_cleaned = r.get("survival_cleaned_pct", 0)
        graduation_cleaned = r.get("graduation_cleaned_pct", 0)

        if top_code == "7030":
            rationale = (
                f"7030 is your best entry point: {recipients} distinct recipients, "
                f"{leq_40k}% of software awards ≤ $40k, 64.5% software awards. "
                f"Small vendors sell direct (88.7%). Ideal for teams prioritizing "
                f"quick market entry and early revenue. This code has the lowest "
                f"sustainability rate — only {graduation_cleaned:.1f}% graduation after 3 years (cleaned) — so "
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
                f"sustainability: {graduation_cleaned:.1f}% graduation rate after 3 years (cleaned), "
                f"{r['small_vendor_gwac_share_pct']}% small vendor GSA MAS share in "
                f"511210/511210S/518210C (~$1.5B+ market), "
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
            "axis1_score": round(axis1.get(top_code, 0), 1),
            "axis2_score": round(axis2.get(top_code, 0), 1),
        }
    else:
        rationale = (
            "Could not match your profile to a PSC code. Consider broadening "
            "your criteria or contacting us for personalized guidance."
        )
        next_steps = [
            "Review the full code comparison (fedmarket compare 7030 DA10 7A21 DA01)",
            "Identify which axis matters most: entry accessibility or sustainability",
            "Consider a pilot study in your top-choice code",
        ]

        recommendation = {
            "recommended_code": None,
            "entry_axis": None,
            "primary_vehicle": None,
            "rationale": rationale,
            "next_steps": next_steps,
            "axis1_score": 0,
            "axis2_score": 0,
        }

    return recommendation


def format_recommendation(rec: Dict[str, Any]) -> str:
    """Format a recommendation dict as a readable string."""
    lines = [
        "",
        "=" * 60,
        "RECOMMENDATION",
        "=" * 60,
        "",
        f"Recommended PSC code: {rec.get('recommended_code', 'N/A')}",
        f"Entry axis: {rec.get('entry_axis', 'N/A')}",
        f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}",
        f"Axis 1 (Accessibility) score: {rec.get('axis1_score', 0)}",
        f"Axis 2 (Sustainability) score: {rec.get('axis2_score', 0)}",
        "",
        "RATIONALE:",
        rec.get('rationale', 'N/A'),
        "",
        "NEXT STEPS:",
    ]
    for i, step in enumerate(rec.get('next_steps', []), 1):
        lines.append(f"  {i}. {step}")
    lines += [
        "",
        "=" * 60,
        "TWO-AXIS FRAMEWORK CONTEXT",
        "=" * 60,
        TWO_AXIS_CONTEXT,
    ]
    return "\n".join(lines)
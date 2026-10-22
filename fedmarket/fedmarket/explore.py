#!/usr/bin/env python3
"""fedmarket Exploration Mode: PSC code ranking under different profile priorities.

Shows how all 5 IT/software PSC codes (7030, DA10, 7A21, DA01, D304) rank
by total two-axis score under different priority weight configurations.
The profile (budget, go-to-market, focus) determines weightings via
PROFILE_WEIGHTS, so the exploration reveals which codes best match each
team's characteristics.

This is a reversible exploratory prototype — it gathers evidence about
the framework's behavior across profiles without claiming adoption or
user numbers.
"""

from typing import Any, Dict, List

from .decide import decide_code, _profile_key, PROFILE_WEIGHTS, _CODES
from .lookup import KNOWN_GRADUATION, KNOWN_SURVIVAL, assess_code


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
    """Compute Axis 2 (sustainability) score for a code given GTM."""
    grad = KNOWN_GRADUATION.get(code, 0)
    surv = KNOWN_SURVIVAL.get(code, 0)
    if gtm == "subcontract":
        return round(0.3 * grad + 0.7 * surv, 1)
    elif gtm == "gsa_mas":
        return round(0.5 * grad + 0.5 * surv, 1)
    else:  # direct
        return round(0.7 * grad + 0.3 * surv, 1)


def explore_rankings(
    budget: str = "leq_40k",
    gtm: str = "direct",
    focus: str = "software",
    include_metrics: bool = True,
) -> Dict[str, Any]:
    """Rank all 5 PSC codes by two-axis score for a given profile.

    Parameters
    ----------
    budget : str
        Primary budget focus: "leq_40k", "leq_100k", or "enterprise"
    gtm : str
        Go-to-market approach: "direct", "gsa_mas", or "subcontract"
    focus : str
        Product technical focus: "software", "saas", or "services"
    include_metrics : bool
        If True, include Axis 1 and Axis 2 scores in the output.

    Returns
    -------
    dict with keys:
      - "profile": the profile key derived from (budget, gtm, focus)
      - "budget": the budget parameter
      - "gtm": the gtm parameter
      - "focus": the focus parameter
      - "rankings": list of (code, total_score, axis1, axis2) tuples, sorted by score desc
      - "weights": the weight configuration applied
      - "evidence": brief summary of which metrics drive the ranking
    """
    # Derive profile key and retrieve weight configuration
    pkey = _profile_key(budget, gtm, focus)
    weights = PROFILE_WEIGHTS.get(pkey, PROFILE_WEIGHTS["default"])

    a1_screen_w = weights["a1_screen_w"]
    a1_access_w = weights["a1_access_w"]
    a1_software_w = weights["a1_software_w"]
    weight_a1, weight_a2 = weights["a1_a2_split"]

    # Assess all codes
    results: Dict[str, Any] = {}
    for code in _CODES:
        results[code] = assess_code(code)

    # Compute Axis 1 for each code
    axis1: Dict[str, float] = {}
    for code in results:
        axis1[code] = _compute_axis1(code, results, a1_screen_w, a1_access_w, a1_software_w)

    # Compute Axis 2 for each code
    axis2: Dict[str, float] = {}
    for code in results:
        axis2[code] = _compute_axis2(code, gtm)

    # Total score
    code_scores: Dict[str, float] = {}
    for code in results:
        code_scores[code] = round(weight_a1 * axis1[code] + weight_a2 * axis2[code], 1)

    # Sort by score (descending)
    rankings = sorted(
        [(code, code_scores[code], axis1[code], axis2[code]) for code in _CODES],
        key=lambda x: x[1],
        reverse=True,
    )

    # Build evidence summary
    top_code = rankings[0][0]
    top_score = rankings[0][1]
    second_code = rankings[1][0]
    second_score = rankings[1][1]

    evidence_parts = []
    if include_metrics:
        evidence_parts.append(
            f"Axis 1 (accessibility) range: {min(axis1.values()):.1f} - {max(axis1.values()):.1f}"
        )
        evidence_parts.append(
            f"Axis 2 (sustainability) range: {min(axis2.values()):.1f} - {max(axis2.values()):.1f}"
        )
        evidence_parts.append(
            f"Top code {top_code} leads by {top_score - second_score:.1f} points"
        )
        # Identify top contributors
        top_a1 = max(axis1, key=axis1.get)
        top_a2 = max(axis2, key=axis2.get)
        evidence_parts.append(
            f"  Strongest Axis 1: {top_a1} (score: {axis1[top_a1]})"
        )
        evidence_parts.append(
            f"  Strongest Axis 2: {top_a2} (score: {axis2[top_a2]})"
        )

    evidence = "; ".join(evidence_parts) if evidence_parts else ""

    return {
        "profile": pkey,
        "budget": budget,
        "gtm": gtm,
        "focus": focus,
        "rankings": rankings,
        "weights": weights,
        "evidence": evidence,
    }


def explore_all_profiles() -> Dict[str, Dict[str, Any]]:
    """Run exploration for all 27 profile combinations (3 budgets × 3 GTMs × 3 foci).

    Returns a dict mapping profile description to exploration results.
    """
    from itertools import product

    budgets = ["leq_40k", "leq_100k", "enterprise"]
    gtms = ["direct", "gsa_mas", "subcontract"]
    foci = ["software", "saas", "services"]

    results = {}
    for budget, gtm, focus in product(budgets, gtms, foci):
        key = _profile_key(budget, gtm, focus)
        desc = f"{budget}+{gtm}+{focus}"
        results[desc] = explore_rankings(budget, gtm, focus, include_metrics=True)

    return results


def format_rankings_table(results: Dict[str, Any]) -> str:
    """Format exploration results as a CLI-friendly table."""
    r = results
    lines = [
        f"\n=== fedmarket Exploration: {r['profile']} ===",
        f"Budget: {r['budget']} | GTM: {r['gtm']} | Focus: {r['focus']}",
        f"Weights: A1-screen={r['weights']['a1_screen_w']}, "
        f"A1-access={r['weights']['a1_access_w']}, "
        f"A1-software={r['weights']['a1_software_w']}, "
        f"A1/A2={r['weights']['a1_a2_split'][0]}/{r['weights']['a1_a2_split'][1]}",
        "",
        "  Rank  Code  Total  A1    A2",
        "  ----  ----  -----  ---  ---",
    ]

    for i, (code, total, a1, a2) in enumerate(r["rankings"], 1):
        lines.append(f"  {i:4d}  {code}  {total:5.1f}  {a1:3.1f}  {a2:3.1f}")

    # Add evidence summary
    lines.append("")
    lines.append(f"Evidence: {r['evidence']}")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="fedmarket-explore",
        description="Explore PSC code rankings under different profile priorities",
    )
    parser.add_argument(
        "--budget", choices=["leq_40k", "leq_100k", "enterprise"],
        default="leq_40k", help="Primary budget focus"
    )
    parser.add_argument(
        "--gtm", choices=["direct", "gsa_mas", "subcontract"],
        default="direct", help="Go-to-market approach"
    )
    parser.add_argument(
        "--focus", choices=["software", "saas", "services"],
        default="software", help="Product technical focus"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all 27 profile combinations",
    )
    args = parser.parse_args()

    if args.all:
        results = explore_all_profiles()
        for desc, result in results.items():
            print(format_rankings_table(result))
    else:
        result = explore_rankings(args.budget, args.gtm, args.focus)
        print(format_rankings_table(result))
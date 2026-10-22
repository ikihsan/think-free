#!/usr/bin/env python3
"""fedmarket Enhanced Decision CLI: improved interactive or scripted PSC code recommender.

Extends the original fedmarket-decide with better prompts, formatted output,
two-axis framework context, and profile/comparison flags.

Interactive (default):
    fedmarket-decide

Scripted (non-interactive; any omitted attribute is prompted for):
    fedmarket-decide --budget leq_40k --gtm direct --focus software
    fedmarket-decide --budget leq_100k --gtm gsa_mas --focus software --json
    fedmarket-decide --compare leq_40k direct software  # show all codes ranked

"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from .decide import decide_code
from .explore import explore_rankings, format_rankings_table
from .lookup import _CODES, KNOWN_GRADUATION, KNOWN_SURVIVAL, assess_code

BUDGET_CHOICES = ("leq_40k", "leq_100k", "enterprise")
GTM_CHOICES = ("direct", "gsa_mas", "subcontract")
FOCUS_CHOICES = ("software", "saas", "services")


def format_recommendation(rec: Dict[str, Any]) -> str:
    """Format a recommendation for display."""
    lines = [
        f"\nRecommended PSC code: {rec.get('recommended_code', 'N/A')}",
        f"Entry axis: {rec.get('entry_axis', 'N/A')}",
        f"Primary vehicle: {rec.get('primary_vehicle', 'N/A')}",
        "",
        "RATIONALE:",
        rec.get('rationale', 'N/A'),
        "",
        "NEXT STEPS:",
    ]
    for i, step in enumerate(rec.get('next_steps', []), 1):
        lines.append(f"  {i}. {step}")
    return "\n".join(lines)


def format_two_axis_context(rec: Dict[str, Any], profile: str) -> str:
    """Format the two-axis framework context section."""
    code = rec.get('recommended_code', '?')
    r = assess_code(code) if code != '?' else {}

    leq_40k = r.get("leq_40k_pct", 0)
    screen = r.get("screen_score", 0)
    recipients = r.get("recipient_count", 0)
    software = r.get("software_pct_awards", 0)

    gtm = profile.split("+")[1] if "+" in profile else "direct"
    budget = profile.split("+")[0] if "+" in profile else "leq_40k"
    focus = profile.split("+")[2] if "+" in profile else "software"

    # Determine the code's position in the exploration
    gtm_map = {"direct": "Direct Sales", "gsa_mas": "GSA MAS/Schedule", "subcontract": "Subcontracting"}
    focus_map = {"software": "Pure Software", "saas": "SaaS/Cloud", "services": "IT Services"}

    lines = [
        "",
        "=TWO-AXIS FRAMEWORK CONTEXT=",
        "",
        f"* Budget focus: {budget}  |  Go-to-market: {gtm_map.get(gtm, gtm)}  |  Product focus: {focus_map.get(focus, focus)}",
        "",
        "* Axis 1 (Accessibility): How easy is it to enter the market?",
        "  Measured by: screen score, ≤$40k award fraction, recipient count,",
        "  software award percentage. HIGH → 7030 best, then DA10, 7A21, DA01, D304.",
        "",
        "* Axis 2 (Business Sustainability): How likely are recipients to return",
        "  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).",
        "  HIGH → DA10 best (41.2%), DA01 (44.9%), 7A21 (43.1%), 7030 weakest (13.8%).",
        "",
        f"* TRADEOFF for {code.upper()}: ",
    ]

    # Add code-specific tradeoff text
    if code == "7030":
        lines.append(
            "  7030 maximizes entry ease but has weak sustainability "
            "(median returning UEI aggregates ~$2,000 over 3 years). "
            "Use it as a beachhead to build case studies and references, then "
            "consider migrating to a sustainability-favorable code like DA10."
        )
    elif code == "DA10":
        lines.append(
            "  DA10 offers the best balance of entry accessibility and business "
            "sustainability: 41.2% graduation rate after 3 years, 28.2% small "
            "vendor GSA MAS share in 511210/511210S/518210C (~$1.5B+ market), "
            "GSA Schedule channel at 7.8% (VA 19.4% funding). Software median "
            f"award ${r.get('software_median_award', 0):,}. VA Franchise Fund and "
            "Medical Care channels provide $4.5B+ in civilian funding. "
            "8.1% sub/prime ratio offers both prime and subcontracting pathways."
        )
    elif code == "7A21":
        lines.append(
            "  7A21 has the highest software % (71.8%) and obligation ($29.2B), "
            "but extreme concentration: Carahsoft 27.1% of sampled obligation. "
            "GSA MAS small vendor share only ~4%. Subcontracting 2.8% (23 "
            "subawardees). Best if you already have a Carahsoft or Dell "
            "relationship, or are targeting niche Army/Navy hardware/software "
            "requirements. Not recommended as a first code for new teams."
        )
    elif code == "DA01":
        lines.append(
            "  DA01 has the largest market ($94.9B obligation) but is "
            "services-dominated: only 12.8% software awards, median software "
            f"award ${r.get('software_median_award', 0):,}. Not suitable for "
            "software product teams. Best for services integration firms. GSA "
            "Schedule strong (13.6% awarding), and 85% small vendor share in SIN 54151S."
        )
    else:  # D304 or fallback
        lines.append(
            "  Not a software market (8.1% software, telecom-dominated). "
            "High GSA MAS shares are inflated by tiny software market slice. "
            "Avoid for software product teams."
        )

    lines.append("")
    lines.append("* General guidance: ")
    if budget == "leq_40k" and gtm == "direct" and focus == "software":
        lines.append(
            "  If quick entry is your priority and you have ≤$40k budget with "
            "pure software, 7030 is the best beachhead. Plan to reassess after "
            "12-18 months for migration to DA10 for sustained business."
        )
    elif gtm == "gsa_mas":
        lines.append(
            "  If you can pursue GSA Schedule/MAS, DA10 is the only code where "
            "small software vendors meaningfully use GSA MAS (28% share in "
            "511210/511210S/518210C). The VA channel (19.4% funding) and "
            "subcontracting pathway (8.1%) provide additional entry points."
        )
    else:
        lines.append(
            "  Review the full 27-profile comparison to identify which axis "
            "matters most for your team: entry accessibility or business "
            "sustainability."
        )

    lines.append("")
    return "\n".join(lines)


def ask_choice(flag_value: Optional[str], question: str, options: tuple,
               mapping: Dict[str, str]) -> str:
    """Return the scripted value when given, else prompt interactively."""
    if flag_value is not None:
        return flag_value
    print(question)
    letters = sorted(mapping.keys())
    for letter in letters:
        print(f"  {letter}) {options[letters.index(letter)]}")
    answer = input("  Your choice (" + "/".join(letters) + "): ").strip().lower()
    return mapping.get(answer, mapping[letters[0]])


def run_comparison(profile: str) -> None:
    """Show how all codes rank for a given profile."""
    results = explore_rankings(*profile.split("+"), include_metrics=True)
    print(format_rankings_table(results))


def main(argv: Optional[list] = None) -> None:
    """Enhanced decision mode CLI: interactive by default, scripted with flags."""
    parser = argparse.ArgumentParser(
        prog="fedmarket-decide",
        description="Recommend a PSC code and entry strategy for a small software team",
    )
    parser.add_argument("--budget", choices=BUDGET_CHOICES,
                        help="Primary budget focus (skip the interactive question)")
    parser.add_argument("--gtm", choices=GTM_CHOICES,
                        help="Go-to-market approach (skip the interactive question)")
    parser.add_argument("--focus", choices=FOCUS_CHOICES,
                        help="Product technical focus (skip the interactive question)")
    parser.add_argument("--json", action="store_true",
                        help="Emit the recommendation as JSON instead of prose")
    parser.add_argument("--profile", type=str,
                        help="Specify profile as budget+gtm+focus (e.g., leq_40k+direct+software)")
    parser.add_argument("--compare", action="store_true",
                        help="Show all codes ranked by two-axis score for the given profile")
    parser.add_argument("--help-profile", action="store_true",
                        help="Show examples of profile combinations")

    args = parser.parse_args(argv)

    # Determine profile from args or ask interactively
    if args.profile:
        profile = args.profile
        budget, gtm, focus = profile.split("+")
    elif args.help_profile:
        print("Profile examples:")
        print("  leq_40k+direct+software    → 7030 (direct sales, quick entry)")
        print("  leq_100k+gsa_mas+software  → DA10 (GWA/MAS pathway, sustained business)")
        print("  enterprise+direct+services → DA01 (largest market, services-dominated)")
        print()
        print("All 27 combinations (budget × gtm × focus):")
        for budget in BUDGET_CHOICES:
            for gtm in GTM_CHOICES:
                for focus in FOCUS_CHOICES:
                    print(f"    {budget}+{gtm}+{focus}")
        return

    if not args.budget and not args.gtm and not args.focus and not args.profile and not args.compare:
        # Interactive mode
        print("=" * 60)
        print("FEDMARKET DECISION GUIDE")
        print("=" * 60)
        print()
        print("Answer 3 questions about your team so we can recommend")
        print("the best PSC code and entry strategy using our two-axis")
        print("framework (entry accessibility vs. business sustainability).")
        print()

        budget = ask_choice(
            args.budget,
            "Q1. What is your primary budget focus?",
            ("≤ $40k per award — quick entry, faster revenue cycles",
             "≤ $100k per award — moderate ambition",
             "Enterprise deals ($100k+) — larger deals, longer cycles"),
            {"a": "leq_40k", "b": "leq_100k", "c": "enterprise"},
        )

        gtm = ask_choice(
            args.gtm,
            "Q2. What is your preferred go-to-market approach?",
            ("Direct sales — build your own sales capability",
             "GSA Schedule/MAS — pursue government contracting",
             "Subcontracting — partner with large primes (Carahsoft, Dell, etc.)"),
            {"a": "direct", "b": "gsa_mas", "c": "subcontract"},
        )

        focus = ask_choice(
            args.focus,
            "Q3. What is your product's technical focus?",
            ("Pure software product (offline/installed software)",
             "SaaS / Cloud service (web-based, subscription)",
             "IT services / Integration (consulting, implementation)"),
            {"a": "software", "b": "saas", "c": "services"},
        )
    else:
        # Scripted mode from flags
        budget = args.budget or "leq_40k"
        gtm = args.gtm or "direct"
        focus = args.focus or "software"
        profile = f"{budget}+{gtm}+{focus}"

    scripted = bool(args.budget) or bool(args.gtm) or bool(args.focus) or bool(args.profile)

    rec: Dict[str, Any] = decide_code(budget, gtm, focus)

    if args.json:
        # Output as JSON with added profile info
        output = {
            "recommended_code": rec.get("recommended_code"),
            "entry_axis": rec.get("entry_axis"),
            "primary_vehicle": rec.get("primary_vehicle"),
            "rationale": rec.get("rationale"),
            "next_steps": rec.get("next_steps"),
            "profile": profile,
        }
        print(json.dumps(output, indent=2))
        return

    if args.compare:
        run_comparison(profile)
        return

    # Display recommendation
    print()
    print("=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print(format_recommendation(rec))
    print()

    # Two-axis framework context
    print("=" * 60)
    print("TWO-AXIS FRAMEWORK CONTEXT")
    print("=" * 60)
    print()
    print(format_two_axis_context(rec, profile))
    print()


if __name__ == "__main__":
    main()
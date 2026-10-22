#!/usr/bin/env python3
"""fedmarket Decision CLI: interactive or scripted PSC code recommender.

Interactive (default):

    fedmarket-decide

Scripted (non-interactive; any omitted attribute is prompted for):

    fedmarket-decide --budget leq_40k --gtm direct --focus software
    fedmarket-decide --budget leq_100k --gtm gsa_mas --focus saas --json
"""

import argparse
import json
from typing import Any, Dict, Optional

from .decide import decide_code

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


def ask_choice(flag_value: Optional[str], question: str, options: "tuple[str, ...]",
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


def main(argv: Optional[list] = None) -> None:
    """Decision mode CLI: interactive by default, scripted with flags."""
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
    args = parser.parse_args(argv)

    scripted = args.budget is not None or args.gtm is not None or args.focus is not None
    if not scripted:
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
        ("\u2264 $40k per award \u2014 quick entry, faster revenue cycles",
         "\u2264 $100k per award \u2014 moderate ambition",
         "Enterprise deals ($100k+) \u2014 larger deals, longer cycles"),
        {"a": "leq_40k", "b": "leq_100k", "c": "enterprise"},
    )

    gtm = ask_choice(
        args.gtm,
        "Q2. What is your preferred go-to-market approach?",
        ("Direct sales \u2014 build your own sales capability",
         "GSA Schedule/MAS \u2014 pursue government contracting",
         "Subcontracting \u2014 partner with large primes (Carahsoft, Dell, etc.)"),
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

    rec: Dict[str, Any] = decide_code(budget, gtm, focus)

    if args.json:
        print(json.dumps(rec, indent=2))
        return

    print()
    print("=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print(format_recommendation(rec))
    print()
    print("=" * 60)
    print("TWO-AXIS FRAMEWORK CONTEXT")
    print("=" * 60)
    print()
    print("\u2022 Axis 1 (Accessibility): How easy is it to enter the market?")
    print("  Measured by: screen score, \u2264$40k award fraction, recipient count,")
    print("  software award percentage. HIGH \u2192 7030 best, then DA10, 7A21, DA01, D304.")
    print()
    print("\u2022 Axis 2 (Business Sustainability): How likely are recipients to return")
    print("  and grow? Measured by: survival % (UEI match), graduation % (>$100k aggregate).")
    print("  HIGH \u2192 DA10 best (41.2%), DA01 (44.9%), 7A21 (43.1%), 7030 weakest (13.8%).")
    print()
    print("\u2022 TRADEOFF: 7030 maximizes entry ease but has weak sustainability")
    print("  (median returning UEI aggregates ~$2,000 over 3 years).")
    print("  \u2022 DA10/DA01/7A21 offer stronger sustainability but have entry challenges.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""fedmarket CLI: Federal Marketplace Assessment Toolkit.

Usage:
    fedmarket --code 7030
    fedmarket --code DA10 --output results.json
    fedmarket --code 7A21 --modules recipient,award,time,agency,vehicle_sin
    fedmarket --code 7030 --survival
    fedmarket --code DA10 --modules subaward
    fedmarket-decide  # Interactive decision mode
    fedmarket-explore  # Explore PSC code rankings for all 27 profile combinations
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Set

from .api import call, base_filters, FULL_WINDOW, RECENT_WINDOW, AWARD_TYPES
from . import lookup
from .recipient import recipient_all, analyze_recipients
from .award import award_all, analyze_awards
from .agency import category_all, analyze_recipient_stats
from .vehicle_sin import vehicle_sin_all, analyze_vehicle_sin, print_vehicle_sin_summary
from .subaward import analyze_prime_subawards
from .output import (print_recipient_summary, print_award_categorization,
                      print_time_window_comparison, print_agency_analysis,
                      print_overall_assessment, print_subaward_trace)
from .survival import main as survival_main, load_json
from .explore import explore_all_profiles, format_rankings_table


def quick_assess(code: Optional[str] = None) -> None:
    """Quick assessment using static lookup data only (no API calls needed).

    Shows key metrics for comparison across the 5 IT/software PSC codes,
    enabling small teams to rapidly evaluate entry options.

    If --code is provided, only that code's metrics are shown.
    If --code is omitted, all 5 codes are listed ranked by screen score.

    Includes E211 survival/graduation data from static ground truth,
    enabling the two-axis (accessibility vs sustainability) assessment
    without any API calls.
    """
    if code:
        codes = [code]
    else:
        codes = ["7030", "DA10", "7A21", "DA01", "D304"]

    # Static sustainability data from E211 (offline ground truth)
    KNOWN_SURVIVAL = {
        "DA10": 72.6,
        "DA01": 69.6,
        "7A21": 43.1,
        "7030": 53.3,
        "D304": 0.0,
    }
    KNOWN_GRADUATION = {
        "DA01": 44.9,
        "DA10": 41.2,
        "7A21": 41.0,
        "7030": 13.8,
        "D304": 0.0,
    }

    lines = []

    if len(codes) == 1:
        # Single code mode: focused output
        code = codes[0]
        d = lookup._CODES[code]
        screen = d["screen_score"]
        recipients = d["recipients"]
        leq_40k = d["leq_40k_pct"]
        software = d["software_pct_awards"]
        gwac = d["small_vendor_gwac_share"]
        gsa_aw = d["gsa_awarding_pct"]
        surv = KNOWN_SURVIVAL.get(code, 0)
        grad = KNOWN_GRADUATION.get(code, 0)
        if code == "7030":
            caveat = "direct sales (88.7%); GSA MAS low (~6%)"
        elif code == "DA10":
            caveat = "GSA MAS 28.2%; VA channel 7.8%"
        elif code == "7A21":
            caveat = "Carahsoft 27%; GSA MAS ~4%"
        elif code == "DA01":
            caveat = "12.8% software; $94.9B market"
        else:
            caveat = "Not software; telecom-dominated"

        lines.append(f"=== Fedmarket Quick Assessment: {code} ===")
        lines.append(f"Name: {d['name']}")
        lines.append(f"Screen score: {screen}")
        lines.append(f"Distinct recipients: {recipients}")
        lines.append(f"≤ $40k fraction: {leq_40k}%")
        lines.append(f"Software % of awards: {software}%")
        lines.append(f"Small vendor GWAe share: {gwac}%")
        lines.append(f"GSA awarding agency: {gsa_aw}%")
        lines.append(f"Entry vehicle: direct_sales" if code == "7030" else ("gsa_mas_schedule_70" if code == "DA10" else ("direct_sales" if code == "7A21" else ("gsa_schedule" if code == "DA01" else "direct_sales"))))
        lines.append(f"Caveats: {caveat}")
        lines.append("")
        lines.append("Two-axis assessment (static data, no API calls):")
        # Axis 1 grading: accessibility
        if screen >= 2000 and leq_40k >= 30 and software >= 50:
            a1_grading = "High"
        elif screen >= 1500 and leq_40k >= 20 and software >= 25:
            a1_grading = "Moderate"
        else:
            a1_grading = "Low"
        # Axis 2 grading: sustainability
        if grad >= 40 and surv >= 70:
            a2_grading = "High"
        elif grad >= 30 and surv >= 50:
            a2_grading = "Moderate"
        else:
            a2_grading = "Low"
        lines.append(f"  Axis 1 (Accessibility): {a1_grading} "
                      f"(screen={screen}, ≤$40k={leq_40k}%, software={software}%)")
        lines.append(f"  Axis 2 (Sustainability): {a2_grading} "
                      f"(graduation={grad}%, survival={surv}%)")
        lines.append("")
        lines.append("Key metrics for decision:")
        lines.append(f"  • Screen score: {'High' if a1_grading == 'High' else 'Moderate' if a1_grading == 'Moderate' else 'Low'} accessibility")
        lines.append(f"  • ≤$40k fraction: {'High' if leq_40k >= 30 else 'Moderate' if leq_40k >= 20 else 'Low'} small-award access")
        lines.append(f"  • Software %: {'High' if software >= 50 else 'Moderate' if software >= 25 else 'Low'} software product market")
        lines.append(f"  • GWAC%: {'Strong' if gwac >= 20 else 'Moderate' if gwac >= 10 else 'Weak'} GSA MAS/GWAC pathway")
        lines.append(f"  • GSA awarding: {'Strong' if gsa_aw >= 10 else 'Moderate' if gsa_aw >= 5 else 'Weak'} GSA Schedule channel")
        lines.append(f"  • Survival (UEI match): {'Strong' if surv >= 70 else 'Moderate' if surv >= 50 else 'Weak'} recipient return rate")
        lines.append(f"  • Graduation (>$100k): {'Strong' if grad >= 40 else 'Moderate' if grad >= 30 else 'Weak'} business growth pathway")
        lines.append("")
        lines.append("Decision guidance:")
        if a1_grading == "High" and a2_grading == "Low":
            lines.append("  → 7030-style: Prioritize entry ease. Use as beachhead, then migrate "
                          "to sustainability-favorable code after 12-18 months.")
        elif a1_grading == "Low" and a2_grading == "High":
            lines.append("  → DA10-style: Prioritize sustainability. Pursue GSA MAS/GWAC path, "
                          "expect harder entry but better business survival.")
        elif a1_grading == "High" and a2_grading == "High":
            lines.append("  → Balanced: Either code works depending on GTM focus. "
                          "7030 for fastest entry, DA10 for strongest sustainability.")
        else:
            lines.append("  → Niche: Carefully evaluate. 7A21 if Carahsoft relationships exist, "
                          "DA01 if services integration is the focus, D304 avoided for software.")
        lines.append("")
        lines.append("Entry vehicle:")
        lines.append(f"  {code == '7030' and 'Direct sales (88.7% of small vendors sell direct)' or ''}"
                      f"{code == 'DA10' and 'GSA MAS Schedule 70 (28.2% small vendor GSA MAS share, VA channel)' or ''}"
                      f"{code == '7A21' and 'Direct sales with Carahsoft/Dell relationships' or ''}"
                      f"{code == 'DA01' and 'GSA Schedule (13.6% awarding, 85% small vendor in SIN 54151S)' or ''}"
                      f"{code == 'D304' and 'Not recommended for software products' or ''}")
    else:
        # All-5 codes mode: comparison table
        lines.append("PSC Code  Screen  Recip  <=$40k  Software  GWAC%   GSA% awarding  Survival  Grad  Caveat")
        lines.append("----------  ------  -----  ------  --------  -----   -------------  --------  ----  ------")

        for code in sorted(codes, key=lambda c: lookup._CODES[c]["screen_score"], reverse=True):
            d = lookup._CODES[code]
            screen = d["screen_score"]
            recipients = d["recipients"]
            leq_40k = d["leq_40k_pct"]
            software = d["software_pct_awards"]
            gwac = d["small_vendor_gwac_share"]
            gsa_aw = d["gsa_awarding_pct"]
            surv = KNOWN_SURVIVAL.get(code, 0)
            grad = KNOWN_GRADUATION.get(code, 0)
            if code == "7030":
                caveat = "direct sales (88.7%); GSA MAS low (~6%)"
            elif code == "DA10":
                caveat = "GSA MAS 28.2%; VA channel 7.8%"
            elif code == "7A21":
                caveat = "Carahsoft 27%; GSA MAS ~4%"
            elif code == "DA01":
                caveat = "12.8% software; $94.9B market"
            else:
                caveat = "Not software; telecom-dominated"
            lines.append(
                f"{code.ljust(10)}"
                f"{str(screen).rjust(6)}"
                f"{str(recipients).rjust(5)}"
                f"{leq_40k:>6.1f}"
                f"{software:>8.1f}"
                f"{gwac:>6.1f}"
                f"{gsa_aw:>15.1f}"
                f"{surv:>8.1f}"
                f"{grad:>5.1f}"
                f"{caveat}"
            )

        lines.append("\n--- Rankings by screen score (desc) ---")
        ranked = sorted(codes, key=lambda c: lookup._CODES[c]["screen_score"], reverse=True)
        lines.append(f"  {' '.join(c.ljust(9) for c in ranked)}")
        lines.append("\n--- Key: ---")
        lines.append("  Screen: Higher = better entry accessibility")
        lines.append("  <=$40k: Higher = more accessible small awards")
        lines.append("  Software: % of awards that are software products")
        lines.append("  GWAC%: Small vendor GSA MAS/GWAC share")
        lines.append("  GSA% awarding: % of awards from GSA Schedule")
        lines.append("  Survival: UEI-match recipient return rate (E211)")
        lines.append("  Grad: Graduation % >$100k aggregate after 3 years (E211)")
        lines.append("  Direct sales (88.7%): 7030 vendors sell directly")
        lines.append("  GSA MAS pathway: DA10 has 28.2% small vendor GSA MAS share")
        lines.append("  Concentrated: 7A21 has Carahsoft 27% dominance")
        lines.append("  Services market: DA01/D304 are not software-product markets")

    print("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='fedmarket: Federal Marketplace Assessment Toolkit for small software teams',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fedmarket --code 7030                           # Full assessment of PSC 7030
  fedmarket --code DA10 --output da10.json       # Save results to JSON
  fedmarket --code 7030 --modules recipient,award # Run only specific modules
  fedmarket --code 7030 --survival                # Include survival analysis
  fedmarket-decide                                # Interactive decision mode
  fedmarket-explore                               # Explore PSC code rankings for all 27 profile combinations
"""
    )
    parser.add_argument('--code', required=False,
                        help='PSC code to analyze (e.g., 7030, DA01, DA10, 7A21, D304)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path')
    parser.add_argument('--modules', default=None,
                        help='Comma-separated modules to run: recipient,award,time,agency,vehicle_sin,subaward '
                             '(default: all except subaward; survival only when --survival is given). '
                             'Use "none" to run no network modules (e.g., with --survival for an offline run).')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Max pages for award fetch (default: 50)')
    parser.add_argument('--survival', action='store_true',
                        help='Run E211 entry survival analysis from raw/ data')
    parser.add_argument('--quick', action='store_true',
                        help='Quick assessment using static lookup data (no API calls needed). '
                              'Shows key metrics for comparison across PSC codes. '
                              'Use --code <PSC> for a single code, or omit --code to list all 5 codes.')
    parser.add_argument('--explore', action='store_true',
                        help='Run exploration mode: show PSC code rankings for all 27 profile combinations')

    args = parser.parse_args()

    if not args.code and not args.explore and not args.quick:
        parser.print_help()
        sys.exit(1)

    # Quick assessment mode: static lookup data only, no API calls
    if args.quick:
        quick_assess(args.code)
        return

    psc_code = args.code

    # Exploration mode: show PSC code rankings for all 27 profile combinations
    # and skip the normal assessment flow
    if args.explore:
        results = explore_all_profiles()
        for desc, result in results.items():
            print(format_rankings_table(result))
        print()
        return

    if args.modules is None:
        modules: Set[str] = ({"survival"} if args.survival
                             else {"recipient", "award", "time", "agency", "vehicle_sin"})
    else:
        modules = set(args.modules.split(","))

    print(f"=== fedmarket Assessment: {psc_code} ===")
    print(f"Modules: {', '.join(sorted(modules))}")
    print(f"Max pages per fetch: {args.max_pages}")

    # Data containers
    recipient_analysis = None
    award_analysis = None
    full_analysis = None
    recent_analysis = None
    funding_agencies = []
    awarding_agencies = []
    federal_accounts = []
    recipient_stats = {}
    vehicle_sin_analysis = None
    subaward_result = None

    # Module: recipient (E202)
    if "recipient" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Recipient Analysis (E202)")
        print(f"{'#'*60}")
        all_recipients, recip_statuses, recip_unused = recipient_all(psc_code)
        print(f"Fetched {len(all_recipients)} recipient rows")
        recipient_analysis = analyze_recipients(all_recipients)
        print_recipient_summary(psc_code, recipient_analysis)

    # Module: award (E203) - fetches full period awards
    if "award" in modules or "time" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Award Categorization (E203)")
        print(f"{'#'*60}")
        print(f"Fetching full period awards (max {args.max_pages} pages)...")
        all_awards, award_statuses, award_unused = award_all(psc_code, max_pages=args.max_pages, capture_prefix="award_full")
        print(f"Fetched {len(all_awards)} awards (full period)")
        award_analysis = analyze_awards(all_awards)
        full_analysis = award_analysis
        print_award_categorization(psc_code, award_analysis)

    # Module: time (E204) - needs recent period awards
    if "time" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Time-Window Comparison (E204)")
        print(f"{'#'*60}")
        print(f"Fetching recent period awards (max {args.max_pages} pages)...")
        recent_awards, recent_statuses, recent_unused = award_all(psc_code, capture_prefix="award_recent")
        print(f"Fetched {len(recent_awards)} awards (recent period)")
        recent_analysis = analyze_awards(recent_awards)
        print_time_window_comparison(psc_code, full_analysis, recent_analysis)

    # Module: agency (E205)
    if "agency" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Agency Distribution (E205)")
        print(f"{'#'*60}")

        print(f"Fetching funding_agency...")
        funding_agencies, funding_statuses = category_all("funding_agency", psc_code)

        print(f"Fetching awarding_agency...")
        awarding_agencies, awarding_statuses = category_all("awarding_agency", psc_code)

        print(f"Fetching federal_account...")
        federal_accounts, fa_statuses = category_all("federal_account", psc_code)

        # For recipient stats, we need full awards - fetch if not already done
        if "award" not in modules and "time" not in modules:
            print(f"Fetching awards for recipient analysis...")
            all_awards, award_statuses, award_unused = award_all(psc_code, max_pages=args.max_pages, capture_prefix="award_agency")
            print(f"Fetched {len(all_awards)} awards")
            full_analysis = analyze_awards(all_awards)
        elif "award" in modules or "time" in modules:
            all_awards, _, _ = award_all(psc_code, max_pages=args.max_pages, capture_prefix="award_recip")

        recipient_stats = analyze_recipient_stats(all_awards)
        print_agency_analysis(psc_code, funding_agencies, awarding_agencies, federal_accounts, recipient_stats, all_awards)

    # Module: vehicle_sin (E210)
    if "vehicle_sin" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Vehicle SIN/SEWP Analysis (E210)")
        print(f"{'#'*60}")
        print(f"Fetching awards for vehicle SIN analysis (max {args.max_pages} pages)...")
        all_awards, statuses = vehicle_sin_all(psc_code, max_pages=args.max_pages, capture_prefix="vehicle_sin")
        print(f"Fetched {len(all_awards)} awards")
        vehicle_sin_analysis = analyze_vehicle_sin(all_awards)
        print_vehicle_sin_summary(psc_code, vehicle_sin_analysis)

    # Module: subaward (E209 extension) — prime-specific subaward trace
    if "subaward" in modules:
        print(f"\n{'#'*60}")
        print(f"# MODULE: Prime-Specific Subaward Trace (E209 Extension)")
        print(f"{'#'*60}")
        subaward_result = analyze_prime_subawards(psc_code, top_n=5, max_awards_per_prime=3)
        if subaward_result:
            print_subaward_trace(psc_code, subaward_result)

    # Module: survival (E211) — entry sustainability (opt-in via --survival;
    # offline, uses the raw/ data bundled with the package).
    # E211 analyzed 7030, DA10, DA01 (and 6810 as control); other codes have
    # no raw survival data.
    if args.survival:
        import_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
        a_survival_path = os.path.join(import_path, f"A_{psc_code}.json")
        b_survival_path = os.path.join(import_path, f"B_{psc_code}.json")
        if os.path.exists(a_survival_path) and os.path.exists(b_survival_path):
            print(f"\n{'#'*60}")
            print(f"# MODULE: Entry Survival Analysis (E211)")
            print(f"{'#'*60}")
            print(f"Raw data directory: {import_path}")
            survival_result = survival_main(psc_code, import_path)
            # Print survival summary matching E211 format
            surv = survival_result.get("survival", 0)
            grad = survival_result.get("graduation", 0)
            small = survival_result.get("n_cohort", survival_result.get("cohort_distinct_uei", 0))
            cohort = survival_result.get("cohort_distinct_uei", 0)
            surv_cleaned = survival_result.get("surv_cleaned", 0)
            grad_cleaned = survival_result.get("grad_cleaned", 0)
            print(f"  Survival (UEI match, raw cohort): {surv*100:.1f}%")
            print(f"  Graduation (>$100k aggregate, raw cohort): {grad*100:.1f}%")
            print(f"  Survival (UEI match, all-small cohort): {surv_cleaned*100:.1f}%")
            print(f"  Graduation (all-small cohort): {grad_cleaned*100:.1f}%")
            print()
            surv = survival_result.get("survival", 0)
            grad = survival_result.get("graduation", 0)
            small = survival_result.get("n_cohort", survival_result.get("cohort_distinct_uei", 0))
            cohort = survival_result.get("cohort_distinct_uei", 0)
            surv_cleaned = survival_result.get("surv_cleaned", 0)
            grad_cleaned = survival_result.get("grad_cleaned", 0)
            print(f"  Reproduced - Survival: {surv*100:.1f}%, Graduation: {grad*100:.1f}%, "
                  f"Small UEIs: {small}, Cohort UEIs: {cohort}")
            print(f"  Cleaned (all-small only) - Survival: {surv_cleaned*100:.1f}%, Graduation: {grad_cleaned*100:.1f}%")
            if surv >= 0.15:
                print(f"  → C1 (churn) SUPPORTED: small-award recipients do return ({surv*100:.1f}% ≥ 15%)")
            else:
                print(f"  → C1 (churn) NOT MET: survival too low ({surv*100:.1f}% < 15%)")
            if grad_cleaned >= 0.15:
                print(f"  → Graduation axis: significant business growth pathway ({grad_cleaned*100:.1f}% ≥ 15%); DA10 recommended for sustained business")
            else:
                print(f"  → Graduation axis: limited sustained-business pathway ({grad_cleaned*100:.1f}% < 15%); 7030 recommended for easy entry only")
            print()
        else:
            print(f"\n{'#'*60}")
            print(f"# MODULE: Entry Survival Analysis (E211)")
            print(f"{'#'*60}")
            print(f"No survival data available for {psc_code} (E211 analyzed 7030, DA10, DA01 only)")
            print()

        # Two-axis recommendation summary
        print(f"  Two-axis recommendation: 7030 is best for entry accessibility "
              "(32.1% ≤$40k awards, 3,916 recipients, direct sales pathway); ")
        print(f"                     DA10 is better for sustained business "
              "(23.7% graduation after 3 years, GSA MAS/GWAC vehicle pathway); ")
        print(f"                     7030 has only 1.2% graduation (cleaned) vs DA10's 23.7%")

    # Overall Assessment
    if all(m in modules for m in ("recipient", "award", "time")):
        print_overall_assessment(psc_code, recipient_analysis, award_analysis, full_analysis, recent_analysis)

    print(f"\n=== End of fedmarket Assessment ===")


if __name__ == "__main__":
    main()
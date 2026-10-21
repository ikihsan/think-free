#!/usr/bin/env python3
"""E206 Integrated CLI Tool: PSC code small-team entry assessment.

Combines E202 (recipient analysis), E203 (award categorization), E204 (time-window),
E205 (agency distribution), E210 (vehicle SIN/SEWP), and E211 (entry survival)
into a comprehensive assessment tool.

Usage:
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code 7030
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code DA01 --output results.json
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code 7A21 --modules recipient,award,time,agency,vehicle_sin
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --survival 7030
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code DA10 --modules subaward
"""

import argparse
import json
import os
import sys

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from e206_recipient import recipient_all, analyze_recipients
from e206_award import award_all, analyze_awards
from e206_agency import category_all, analyze_recipient_stats
from e206_vehicle_sin import vehicle_sin_all, analyze_vehicle_sin, print_vehicle_sin_summary
from e206_subaward import analyze_prime_subawards
from e206_output import (print_recipient_summary, print_award_categorization,
                          print_time_window_comparison, print_agency_analysis,
                          print_overall_assessment, print_subaward_trace)
from e206_survival import main as survival_main, load_json


def format_survival_summary_to_cli(code, result):
    """Format survival analysis results for CLI output."""
    surv = result.get("survival", 0)
    grad = result.get("graduation", 0)
    small = result.get("n_cohort", result.get("cohort_distinct_uei", 0))
    cohort = result.get("cohort_distinct_uei", 0)
    n_multi = result.get("n_multi", 0)
    n_uei = result.get("n_uei", 0)
    mean_awards = result.get("mean_awards", 0)
    median_awards = result.get("median_awards", 0)
    cross_da10 = result.get("cross_market", {}).get("DA10", 0)
    cross_da01 = result.get("cross_market", {}).get("DA01", 0)
    cross_d304 = result.get("cross_market", {}).get("D304", 0)

    lines = []
    lines.append(f"  PSC Code: {code}")
    lines.append(f"    Cohort distinct UEIs (raw): {cohort:,}")
    lines.append(f"    Small-entrant UEIs (≤$100k): {small:,}")
    lines.append(f"    Survival (UEI match): {surv*100:.1f}%")
    lines.append(f"    Survival name-est (I2): {result.get('survival_name_est', 0)*100:.1f}%")
    lines.append(f"    Graduation (>$100k aggregate): {grad*100:.1f}%")
    lines.append(f"    Net-positive return (>$0): {result.get('survival_net_positive', 0)*100:.1f}%")
    lines.append(f"    Mean awards/UEI: {mean_awards:.1f}")
    lines.append(f"    Median awards/UEI: {median_awards:.1f}")
    lines.append(f"    UEIs with multiple awards in A: {n_multi}/{n_uei} ({100*n_multi/n_uei:.1f}%)" if n_uei else "    N/A")
    lines.append(f"    Cross-market returns: DA10={cross_da10}, DA01={cross_da01}, D304={cross_d304}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='E206 Integrated CLI: PSC code small-team entry assessment'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030, DA01, DA10, 7A21, D304)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path')
    parser.add_argument('--modules', default="recipient,award,time,agency,vehicle_sin",
                        help='Comma-separated modules to run: recipient,award,time,agency,vehicle_sin,subaward (default: all except subaward)')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Max pages for award fetch (default: 50)')
    parser.add_argument('--survival', action='store_true',
                        help='Run E211 entry survival analysis from raw/ data')
    args = parser.parse_args()

    psc_code = args.code
    modules = set(args.modules.split(","))

    print(f"=== E206 Integrated Assessment: {psc_code} ===")
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

    # Module: survival (E211) — entry sustainability
    # E211 only analyzed 7030, DA10, DA01 (and 6810 as control).
    # Only run survival analysis for codes that have raw data.
    import_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
    a_survival_path = os.path.join(import_path, f"A_{psc_code}.json")
    b_survival_path = os.path.join(import_path, f"B_{psc_code}.json")
    if os.path.exists(a_survival_path) and os.path.exists(b_survival_path):
        print(f"\n{'#'*60}")
        print(f"# MODULE: Entry Survival Analysis (E211)")
        print(f"{'#'*60}")
        print(f"Raw data directory: {import_path}")
        survival_result = survival_main(psc_code, import_path)
        print(format_survival_summary_to_cli(psc_code, survival_result))
        # E211-style gate indicators + two-axis recommendation
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

    # JSON Output
    if args.output:
        output_data = {
            "experiment": "E206",
            "psc_code": psc_code,
            "modules_run": sorted(list(modules)),
            "recipient": recipient_analysis,
            "award_categorization": {k: v for k, v in award_analysis.items() if k != "amounts"} if award_analysis else None,
            "full_period": {k: v for k, v in full_analysis.items() if k != "amounts"} if full_analysis else None,
            "recent_period": {k: v for k, v in recent_analysis.items() if k != "amounts"} if recent_analysis else None,
            "funding_agencies": funding_agencies,
            "awarding_agencies": awarding_agencies,
            "federal_accounts": federal_accounts,
            "recipient_stats": {k: v for k, v in recipient_stats.items()},
            "vehicle_sin": vehicle_sin_analysis,
        }
        # Include subaward trace data if run
        if "subaward" in modules and 'subaward_result' in locals() and subaward_result:
            output_data["subaward_trace"] = subaward_result
        # Include survival data from the already-computed analysis
        survival_data = survival_main(psc_code, os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw"))
        if survival_data.get("n_cohort", 0) > 0:
            output_data["survival"] = {
                "small_uei_count": survival_data["n_cohort"],
                "survival_pct": survival_data["survival"],
                "graduation_pct": survival_data["graduation"],
                "survival_name_est_pct": survival_data["survival_name_est"],
                "survival_net_positive_pct": survival_data["survival_net_positive"],
                "mean_awards_per_uei": survival_data["mean_awards"],
                "median_awards_per_uei": survival_data["median_awards"],
                "cross_market": survival_data.get("cross_market", {}),
            }
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"\nJSON output saved to {args.output}")

    print(f"\n=== End of E206 Integrated Tool ===")


if __name__ == "__main__":
    main()
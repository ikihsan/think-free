#!/usr/bin/env python3
"""E206 Integrated CLI Tool: PSC code small-team entry assessment.

Combines E202 (recipient analysis), E203 (award categorization), E204 (time-window),
E205 (agency distribution), and E210 (vehicle SIN/SEWP analysis) into a single 
comprehensive assessment tool.

Usage:
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code 7030
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code DA01 --output results.json
    python3 EXPERIMENTS/E206-integrated-cli-tool/run.py --code 7A21 --modules recipient,award,time,agency,vehicle_sin
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
from e206_output import (print_recipient_summary, print_award_categorization,
                          print_time_window_comparison, print_agency_analysis,
                          print_overall_assessment)


def main():
    parser = argparse.ArgumentParser(
        description='E206 Integrated CLI: PSC code small-team entry assessment'
    )
    parser.add_argument('--code', required=True,
                        help='PSC code to analyze (e.g., 7030, DA01, DA10, 7A21, D304)')
    parser.add_argument('--output', default=None,
                        help='Output JSON file path')
    parser.add_argument('--modules', default="recipient,award,time,agency,vehicle_sin",
                        help='Comma-separated modules to run: recipient,award,time,agency,vehicle_sin (default: all)')
    parser.add_argument('--max-pages', type=int, default=50,
                        help='Max pages for award fetch (default: 50)')
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
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"\nJSON output saved to {args.output}")

    print(f"\n=== End of E206 Integrated Tool ===")


if __name__ == "__main__":
    main()
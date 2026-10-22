#!/usr/bin/env python3
"""CLI entry point for usaspending-assess.

Assesses a USAspending PSC code for small-team software entry.
Provides a quick assessment of market fit, small-award accessibility,
and entry survival metrics.
"""

import argparse
import json
import sys
import os

# Add parent EXPERIMENTS directory to path for e206 modules
_HERE = os.path.dirname(os.path.abspath(__file__))
_SYS_PATH_ADD = os.path.join(_HERE, "..", "EXPERIMENTS", "E206-integrated-cli-tool")
if _SYS_PATH_ADD not in sys.path:
    sys.path.insert(0, _SYS_PATH_ADD)

from usaspending_assess.assess import assess_code


def print_assessment_summary(psc_code, result):
    """Print a concise assessment summary from the full result dict."""
    surv = result.get("survival", {})
    award = result.get("award", {})
    recipient = result.get("recipient", {})

    print(f"\n=== PSC Code Assessment: {psc_code} ===")

    # Screen score components from the award analysis
    n_recipients = award.get("n_awards", 0)
    top10_share = award.get("top10_share_pct", 0)
    software_pct = award.get("software_award_pct", 0)
    small_award_pct = award.get("award_size_dist", {}).get("small_pct_40k", 0) if isinstance(award.get("award_size_dist"), dict) else "N/A"

    print(f"  Distinct recipients: {n_recipients:,}")
    print(f"  Top-10 share: {top10_share:.1f}%")
    print(f"  Software awards: {software_pct:.1f}%")
    print(f"  Small awards (<=40k): {small_award_pct:.1f}%" if small_award_pct != "N/A" else "  Small awards: N/A")

    # Survival metrics
    survival_raw = surv.get("survival", 0) * 100
    survival_small = surv.get("survival_small", 0) * 100 if "survival_small" in surv else "N/A"
    graduation = surv.get("graduation", 0) * 100

    print(f"  Survival (UEI match): {survival_raw:.1f}%")
    print(f"  Survival (small-only): {survival_small:.1f}%" if survival_small != "N/A" else "  Survival (small-only): N/A")
    print(f"  Graduation (>$100k): {graduation:.1f}%")

    # Two-axis recommendation
    if graduation >= 20 and survival_raw >= 50:
        print(f"  Recommendation: DA10 — strong for sustained business (GWAC/MAS pathway)")
    elif survival_raw >= 50:
        print(f"  Recommendation: 7030 — best for entry accessibility (direct sales)")
    else:
        print(f"  Recommendation: Limited entry pathway — consider other codes")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Assess a USAspending PSC code for small-team software entry."
    )
    parser.add_argument(
        "--code", required=True, help="PSC code to analyze (e.g., 7030, DA01, DA10, 7A21, D304)"
    )
    parser.add_argument(
        "--max-pages", type=int, default=50,
        help="Max pages per API fetch (default: 50)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output JSON file path"
    )

    args = parser.parse_args(argv)

    psc_code = args.code
    result = assess_code(psc_code, max_pages=args.max_pages)

    print_assessment_summary(psc_code, result)

    # JSON output
    if args.output:
        # Store the full result plus the code
        output_data = {
            "experiment": "E206-assess",
            "psc_code": psc_code,
            "result": result,
        }
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        print(f"\nFull JSON output saved to {args.output}")

    print(f"\n=== End of assessment ===")


if __name__ == "__main__":
    main()
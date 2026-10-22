#!/usr/bin/env python3
"""
Small Program Entrant Advisor — Integrated Prototype

Dispatches to either the IT Code Entrant Advisor v3 or the NIH SBIR Category
Advisor v3 based on CLI arguments. Evidence-gathering prototype, not product
validation. Fixes D128 defect (activity_codes + meta.total).

Usage:
    python3 tools/small_program_advisor.py --it-codes [code1 code2 ...]
    python3 tools/small_program_advisor.py --category-code CATEGORY_CODE [--activity-codes R41 R42]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def main():
    """CLI entry point for the integrated small program entrant advisor."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Small Program Entrant Advisor — integrated prototype'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--it-codes',
        nargs='+',
        help='ITA PSC codes to analyze (e.g. DA01 DA10 7A21). Uses E209 design with '
             'meta.total census and award-type sub-segment analysis.'
    )
    group.add_argument(
        '--category-code',
        type=str,
        help='NIH SBIR spending category code (e.g. 101). Uses E204/E206/E212 design '
             'with activity_codes filtering and meta.total census.'
    )
    parser.add_argument(
        '--fiscal-year',
        type=int,
        default=2023,
        help='Fiscal year to screen (default: 2023)'
    )
    parser.add_argument(
        '--activity-codes',
        nargs='+',
        help='NIH activity codes to filter by (e.g. R41 R42 for SBIR). Per D128, '
             'when specified, only grants matching these codes are fetched.'
    )

    args = parser.parse_args()

    if args.it_codes:
        # Dispatch to IT Code Entrant Advisor v3
        from it_entrant_advisor_v3 import main as it_main
        # Override the default codes with user-specified codes
        import it_entrant_advisor_v3 as ieav3
        ieav3.DEFAULT_CODES = args.it_codes
        it_main()
    elif args.category_code is not None:
        # Dispatch to NIH SBIR Category Advisor v3
        from nih_small_program_advisor_v3 import main as nih_main
        nih_main()


if __name__ == '__main__':
    main()

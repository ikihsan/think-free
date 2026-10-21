#!/usr/bin/env python3
"""
NIH SBIR Small-Program Accessibility Screener

Core screener logic: screens NIH SBIR spending categories for small-program
accessibility, computes metrics per Funding IC, ranks categories and ICs.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis) and the spending category screen from E204.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import sys
import os

# Ensure the tools directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from nih_sbir_metrics import (
    fetch_grants, group_by_funding_ic, compute_accessibility_metrics,
)


# ============================================================
# Consensus ICs (from 5-category analysis E206)
# ============================================================

CONSENSUS_ICs = [
    'NIAID',
    'NCI',
    'NHLB',
    'NIA',
]

CONSENSUS_RATIONALE = (
    "Based on an analysis of 5 NIH SBIR spending categories "
    "(101, 108, 525, 701, 176): NIAID appears in 4/5 categories, "
    "NCI in 4/5, NHLB in 4/5, and NIA in 4/5, making them the "
    "most consistently accessible Funding ICs for small programs "
    "across multiple spending categories. Category 176 is the most "
    "accessible overall (NCI: 43.9% top-5 share, access score 157.20), "
    "while Category 101 is the least accessible of the five "
    "(NIAID: 64.1% top-5 share, access score 34.34)."
)


# ============================================================
# Screening functions
# ============================================================

def screen_category(spending_category, fiscal_year=2023, max_total=500):
    """Screen one NIH SBIR spending category for small-program accessibility."""
    print('\n=== NIH SBIR Spending Category Screen ===')
    print('Spending Category: %s' % spending_category)
    print('Fiscal Year: %s' % fiscal_year)
    print('=' * 50)

    # Fetch grants in category
    print('\nFetching grants from NIH RePORTER...')
    grants = fetch_grants(spending_category=spending_category, fiscal_year=fiscal_year, max_total=max_total)
    print('Grants with category %s: %d' % (spending_category, len(grants)))

    if len(grants) == 0:
        print('No grants found with category %s.' % spending_category)
        return None

    # Group by Funding IC
    ic_groups = group_by_funding_ic(grants)
    print('Funding ICs found: %d' % len(ic_groups))

    # Compute metrics
    metrics = compute_accessibility_metrics(ic_groups)

    # Rank by access score (higher = more accessible)
    ranked = sorted(metrics, key=lambda x: x['access_score'], reverse=True)

    # Print results table
    print()
    print('%-55s %6s %5s %8s %8s' % ('IC', 'Proj', 'Orgs', 'Top-5%', 'Access'))
    print('-' * 55)

    for rd in ranked:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('%-55s %6d %5d %7.1f%% %7.2f' %
              (ic, rd['project_count'], rd['distinct_orgs'],
               rd['top5_concentration_percent'], rd['access_score']))

    print()
    print('Most accessible ICs for small programs (highest access_score):')
    for rd in ranked[:5]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share, access score %.2f'
              % (ic, rd['project_count'], rd['distinct_orgs'],
                 rd['top5_concentration_percent'], rd['access_score']))

    print()
    print('Least accessible ICs (most concentrated, hardest for small programs):')
    for rd in ranked[-3:]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share'
              % (ic, rd['project_count'], rd['distinct_orgs'],
                 rd['top5_concentration_percent']))

    return ranked


def screen_categories(category_codes, fiscal_year=2023):
    """Screen multiple NIH SBIR spending categories and compare accessibility."""
    print('\n=== Multi-Category NIH SBIR Accessibility Screen ===')
    print('Fiscal Year: %s' % fiscal_year)
    print('=' * 50)
    print()

    results = {}

    for cat_code in category_codes:
        print('Screening category %s...' % cat_code)
        ranked = screen_category(cat_code, fiscal_year=fiscal_year, max_total=500)
        if ranked is not None:
            results[cat_code] = ranked
        print()

    # Cross-category comparison
    print('=' * 50)
    print('CROSS-CATEGORY COMPARISON')
    print('=' * 50)

    # Sort categories by most accessible IC's access score
    comparison_rows = []
    for cat_code, ranked in results.items():
        if ranked and len(ranked) > 0:
            top_ic = ranked[0]
            comparison_rows.append({
                'category': cat_code,
                'top_ic': top_ic['ic'],
                'top_ic_access_score': top_ic['access_score'],
                'top_ic_top5_share': top_ic['top5_concentration_percent'],
                'total_grants': top_ic['project_count'],
                'total_orgs': top_ic['distinct_orgs'],
            })

    # Sort by access_score descending (most accessible first)
    comparison_rows.sort(key=lambda x: x['top_ic_access_score'], reverse=True)

    print('%-12s %15s %8s %8s %8s %8s' % (
        'Category', 'Top IC', 'Access Score', 'Top-5%', 'Grants', 'Orgs'))
    print('-' * 70)
    for row in comparison_rows:
        print('%-12s %15s %8.2f %8.1f%% %8d %8d' % (
            row['category'], row['top_ic'],
            row['top_ic_access_score'], row['top_ic_top5_share'],
            row['total_grants'], row['total_orgs']))

    print()
    print('Summary: Higher access_score = more fragmented = more accessible for small programs.')
    print('Lower top-5% concentration = more distributed funding = better for small programs.')

    return results


# ============================================================
# Recommendations
# ============================================================

def get_category_recommendations(category_code):
    """Get small-program accessibility recommendations for a spending category.

    Uses the 5-category consensus pattern to identify ICs that are
    consistently accessible across multiple spending categories.
    """
    recommendations = []

    for ic in CONSENSUS_ICs:
        recommendations.append({
            'ic': ic,
            'consensus_rank': CONSENSUS_ICs.index(ic),
            'rationale': CONSENSUS_RATIONALE,
        })

    # Sort by consensus rank (NIAID=0 is highest consensus)
    recommendations.sort(key=lambda x: x['consensus_rank'])

    return recommendations[:3]


def print_recommendations(category_code):
    """Print IC recommendations for a given spending category."""
    recs = get_category_recommendations(category_code)

    print('\nIC Recommendations (based on 5-category consensus pattern):')
    print('-' * 55)
    for i, rec in enumerate(recs):
        ic_display = rec['ic']
        rationale_display = rec['rationale'][:100] + '...' if len(rec['rationale']) > 100 else rec['rationale']
        print('  %d. %s' % (i + 1, ic_display))
        print('     Rationale: %s' % rationale_display)


def run_screener(category_codes=None, fiscal_year=2023, multi_mode=False):
    """Run the small-program accessibility screener.

    Delegates to screen_categories for multi-mode or screen_category for single mode.
    """
    if multi_mode:
        return screen_categories(category_codes, fiscal_year=fiscal_year)
    else:
        if category_codes is None:
            category_codes = ['101', '108', '176']
        for cat_code in category_codes:
            print('\n' + '=' * 60)
            screen_category(cat_code, fiscal_year=fiscal_year)
            print_recommendations(cat_code)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='NIH SBIR Small-Program Accessibility Screener'
    )
    parser.add_argument(
        'category_codes',
        nargs='*',
        help='NIH SBIR spending category codes to screen (default: 101 108 176)'
    )
    parser.add_argument(
        '--fiscal-year',
        type=int,
        default=2023,
        help='Fiscal year to screen (default: 2023)'
    )
    parser.add_argument(
        '--multi',
        action='store_true',
        help='Run multi-category comparison mode'
    )

    args = parser.parse_args()

    # Use provided category codes or defaults
    category_codes = args.category_codes if args.category_codes else None

    run_screener(
        category_codes=category_codes,
        fiscal_year=args.fiscal_year,
        multi_mode=args.multi,
    )
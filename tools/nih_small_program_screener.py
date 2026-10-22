#!/usr/bin/env python3
"""
NIH SBIR Small-Program Screener

Core screener logic: screens NIH SBIR spending categories for small-program
accessibility, computes metrics per Funding IC, ranks categories and ICs.

Builds on the sub-segment screen methodology from E206 (NIH SBIR category 101
sub-segment analysis) and the spending category screen from E204.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from nih_sbir_metrics import (
    fetch_grants, group_by_funding_ic, compute_accessibility_metrics,
)

# Consensus ICs from 5-category analysis (E206: categories 101, 108, 525, 701, 176)
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
    "accessible overall, while Category 101 is the least accessible "
    "of the five tested."
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
    "accessible overall, while Category 101 is the least accessible "
    "of the five tested."
)


# ============================================================
# Screening functions
# ============================================================

def screen_category(spending_category, fiscal_year=2023, activity_codes=None):
    """Screen one NIH SBIR spending category for small-program accessibility.

    Key fix for D128: activity_codes filtering and meta.total for complete census
    instead of arbitrary 2,000-row cap.
    """
    cat_code = int(spending_category) if isinstance(spending_category, str) else spending_category

    print('\n=== NIH SBIR Spending Category Screen ===')
    print('Spending Category: %s' % cat_code)
    print('Fiscal Year: %s' % fiscal_year)
    if activity_codes:
        print('Activity Codes: %s' % activity_codes)
    print('=' * 55)

    print('\nFetching grants from NIH RePORTER...')
    all_grants = fetch_grants(
        spending_category=cat_code,
        fiscal_year=fiscal_year,
        activity_codes=activity_codes,
        max_total=None
    )
    print('Total unique grants fetched: %d' % len(all_grants))

    category_grants = [g for g in all_grants
                       if g.get('spending_categories') and cat_code in g['spending_categories']]

    print('Grants with category %s: %d' % (cat_code, len(category_grants)))

    if len(category_grants) == 0:
        print('No grants found with category %s.' % cat_code)
        if all_grants:
            for g in all_grants[:3]:
                ic = g.get('agency_ic_admin', {}).get('name', 'Unknown')
                cats = g.get('spending_categories', [])
                print('  %s: category=%s' % (ic, cats))
        return None

    ic_groups = group_by_funding_ic(category_grants)
    print('Funding ICs found: %d' % len(ic_groups))

    metrics = compute_accessibility_metrics(ic_groups)
    ranked = sorted(metrics, key=lambda x: x['access_score'], reverse=True)

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

    print()
    print('Consensus ICs (consistently accessible across categories):')
    for ic in CONSENSUS_ICs:
        print('  %s: historically accessible across multiple spending categories' % ic)

    print()
    return ranked


def screen_categories(category_codes, fiscal_year=2023, activity_codes=None):
    """Screen multiple NIH SBIR spending categories and compare accessibility."""
    print('\n=== Multi-Category NIH SBIR Accessibility Screen ===')
    print('Fiscal Year: %s' % fiscal_year)
    if activity_codes:
        print('Activity Codes: %s' % activity_codes)
    print('=' * 50)
    print()

    results = {}

    for cat_code in category_codes:
        print('Screening category %s...' % cat_code)
        ranked = screen_category(cat_code, fiscal_year=fiscal_year,
                                  activity_codes=activity_codes)
        if ranked is not None:
            results[cat_code] = ranked
        print()

    print('=' * 50)
    print('CROSS-CATEGORY COMPARISON')
    print('=' * 50)
    print()

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
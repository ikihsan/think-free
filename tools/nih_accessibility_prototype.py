#!/usr/bin/env python3
"""
NIH SBIR Small-Program Accessibility Prototype

A reversible exploratory prototype that helps small programs identify the most
accessible NIH SBIR Funding Institutes/Centers within a given spending category.

This builds on the sub-segment screen methodology from E206: classify grants by
Funding IC and measure accessibility via grant count, distinct organizations,
top-N concentration, and access score. Higher access_score = more fragmented
(more distinct orgs sharing the load) = better for small programs entering the
market without being subcontractors to primes.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import json
import urllib.request
import time
import sys


def fetch_grants(fiscal_year=2023, max_total=2000):
    """Fetch grants from NIH RePORTER API across pages."""
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    all_results = []
    seen_ids = set()
    offset = 0

    while len(all_results) < max_total:
        payload = json.dumps({
            'criteria': {
                'fiscal_years': [fiscal_year],
                'limit': 100,
            },
            'offset': offset,
        }).encode()

        req = urllib.request.Request(
            url, data=payload,
            headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                results = data.get('results', [])
                if not results:
                    break

                for r in results:
                    aid = r.get('appl_id')
                    if aid and aid not in seen_ids:
                        seen_ids.add(aid)
                        all_results.append(r)

                meta = data.get('meta', {})
                total = meta.get('total', 0)
                if len(all_results) >= total:
                    break

        except urllib.error.HTTPError as e:
            print('HTTP error: %s' % e.code)
            break
        except Exception as e:
            print('Error: %s' % e)
            break

        offset += 100
        time.sleep(0.05)

    return all_results


def group_by_funding_ic(grants):
    """Group grants by Funding Institute/Center."""
    ic_groups = {}
    for g in grants:
        ic_admin = g.get('agency_ic_admin', {})
        ic_name = ic_admin.get('name', 'Unknown IC')
        if ic_name not in ic_groups:
            ic_groups[ic_name] = []
        ic_groups[ic_name].append(g)
    return ic_groups


def compute_accessibility_metrics(ic_groups):
    """Compute accessibility metrics for each Funding IC sub-area."""
    results = []

    for ic, projects in ic_groups.items():
        orgs = set()
        org_amounts = {}
        total_amount = 0

        for p in projects:
            org_name = p.get('organization', {}).get('org_name', 'N/A')
            orgs.add(org_name)
            amount = p.get('award_amount', 0) or 0
            total_amount += amount

            if org_name not in org_amounts:
                org_amounts[org_name] = 0
            org_amounts[org_name] += amount

        # Compute top-3 and top-5 concentration
        sorted_orgs = sorted(org_amounts.items(), key=lambda x: x[1], reverse=True)
        top3_sum = sum(amount for _, amount in sorted_orgs[:3])
        top3_share = (top3_sum / total_amount * 100) if total_amount else 0
        top5_sum = sum(amount for _, amount in sorted_orgs[:5])
        top5_share = (top5_sum / total_amount * 100) if total_amount else 0

        # Access score: higher = more accessible (more grants distributed among more orgs)
        # = grant_count / (top5_share_fraction). Higher = more distributed.
        access_score = len(projects) / (top5_share / 100) if top5_share > 0 else float('inf')

        results.append({
            'ic': ic,
            'project_count': len(projects),
            'distinct_orgs': len(orgs),
            'top3_concentration_percent': top3_share,
            'top5_concentration_percent': top5_share,
            'access_score': access_score,
            'total_amount': total_amount,
        })

    return results


def run_prototype(category_code, fiscal_year=2023, max_total=500):
    """Run the small-program accessibility prototype for a given spending category."""
    print('\nNIH SBIR Small-Program Accessibility Prototype')
    print('Spending Category: %s' % category_code)
    print('Fiscal Year: %s' % fiscal_year)
    print('=' * 55)

    # Fetch grants
    print('\nFetching grants from NIH RePORTER...')
    all_grants = fetch_grants(fiscal_year=fiscal_year, max_total=max_total)
    print('Total unique grants fetched: %d' % len(all_grants))

    # Filter for the specified spending category
    category_grants = [g for g in all_grants
                       if g.get('spending_categories') and category_code in g['spending_categories']]

    print('Grants with category %s: %d' % (category_code, len(category_grants)))

    if len(category_grants) == 0:
        print('No grants found with category %s.' % category_code)
        # Try showing a few grants to see available categories
        if all_grants:
            print('Sample grant categories:')
            for g in all_grants[:3]:
                cats = g.get('spending_categories', [])
                print('  %s: %s' % (g.get('agency_ic_admin', {}).get('name', 'Unknown'), cats))
        return []

    # Group by Funding IC
    ic_groups = group_by_funding_ic(category_grants)
    print('Funding ICs found: %d' % len(ic_groups))

    # Compute metrics
    metrics = compute_accessibility_metrics(ic_groups)

    # Rank by access score (higher = more accessible for small programs)
    ranked = sorted(metrics, key=lambda x: x['access_score'], reverse=True)

    # Print results table
    print()
    print('%-55s %6s %5s %8s %8s %8s' %
           ('IC', 'Proj', 'Orgs', 'Top-3%', 'Top-5%', 'Access'))
    print('-' * 55)

    for rd in ranked[:20]:
        ic = rd['ic'][:54] if len(rd['ic']) > 54 else rd['ic']
        print('%-55s %6d %5d %7.1f%% %7.1f%% %7.2f' %
              (ic, rd['project_count'], rd['distinct_orgs'],
               rd['top3_concentration_percent'],
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
    return ranked


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 nih_accessibility_prototype.py <spending_category_code>')
        print('Example: python3 nih_accessibility_prototype.py 101')
        sys.exit(1)

    category_code = sys.argv[1]
    ranked = run_prototype(category_code)
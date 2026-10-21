#!/usr/bin/env python3
"""
NIH SBIR Sub-Segment Screen Prototype

A reversible exploratory prototype that helps small programs identify the most
accessible NIH SBIR Funding Institutes/Centers within a given spending category.

The prototype applies the sub-segment screen methodology from E206: classify grants
by Funding IC and measure accessibility via grant count, distinct organizations,
top-N concentration, and access score.

NOTE: This is a prototype, not a validated product. It is evidence-gathering work.
"""

import urllib.request
import json
import time


def fetch_grants(spending_category=None, fiscal_year=2023, max_total=2000):
    """
    Fetch grants from NIH RePORTER API.
    
    If spending_category is specified, only returns grants that include that category.
    Otherwise, returns all grants for the fiscal year.
    """
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    all_results = []
    seen_ids = set()
    offset = 0
    
    while len(all_results) < max_total:
        payload = json.dumps({
            'criteria': {
                'fiscal_years': [fiscal_year],
                'limit': 50,
            },
            'offset': offset,
        }).encode()
        
        req = urllib.request.Request(
            url, data=payload,
            headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as r:
                data = json.load(r)
                results = data.get('results', [])
                if not results:
                    break
                
                for r in results:
                    aid = r.get('appl_id')
                    if aid and aid not in seen_ids:
                        seen_ids.add(aid)
                        all_results.append(r)
                
                # Get total from meta to know when to stop
                meta = data.get('meta', {})
                total = meta.get('total', 0)
                if len(all_results) >= total:
                    break
                    
        except urllib.error.HTTPError as e:
            print('HTTP error: %s' % e.code)
            break
        
        offset += 50
        time.sleep(0.1)
    
    # Filter by spending category if specified
    if spending_category is not None:
        filtered = []
        for g in all_results:
            cats = g.get('spending_categories')
            if cats and spending_category in cats:
                filtered.append(g)
        return filtered
    
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
    """
    Compute accessibility metrics for each Funding IC sub-area.
    Returns list of dicts sorted by access_score descending.
    """
    results = []
    
    for ic, projects in ic_groups.items():
        orgs = set()
        total_amount = 0
        org_amounts = {}
        
        for p in projects:
            org_name = p.get('organization', {}).get('org_name', 'N/A')
            orgs.add(org_name)
            amount = p.get('award_amount', 0) or 0
            total_amount += amount
            
            if org_name not in org_amounts:
                org_amounts[org_name] = 0
            org_amounts[org_name] += amount
        
        # Compute top-5 concentration
        sorted_orgs = sorted(org_amounts.items(), key=lambda x: x[1], reverse=True)
        top5_sum = sum(amount for _, amount in sorted_orgs[:5])
        top5_share = (top5_sum / total_amount * 100) if total_amount else 0
        
        # Access score: grant count / (top-5 share fraction)
        # Higher = more accessible (more grants, distributed among more orgs)
        access_score = len(projects) / (top5_share / 100) if top5_share > 0 else float('inf')
        
        results.append({
            'ic': ic,
            'project_count': len(projects),
            'distinct_orgs': len(orgs),
            'top5_concentration_percent': top5_share,
            'access_score': access_score,
            'total_amount': total_amount,
        })
    
    return results


def run_screen(category_code, fiscal_year=2023, max_total=2000):
    """
    Run a sub-segment screen for NIH SBIR spending category.
    Prints ranked results and returns the ranked metrics list.
    """
    print('\nNIH SBIR Sub-Segment Screen')
    print('Spending Category: %s' % category_code)
    print('Fiscal Year: %s' % fiscal_year)
    print('=' * 55)
    
    # Fetch grants in category
    print('\nFetching grants in category %s...' % category_code)
    grants = fetch_grants(spending_category=category_code, fiscal_year=fiscal_year, max_total=max_total)
    print('Grants with category %s: %d' % (category_code, len(grants)))
    
    if len(grants) == 0:
        print('No grants found with category %s. Checking available data...' % category_code)
        # Try without filter to see what we get
        all_grants = fetch_grants(fiscal_year=fiscal_year, max_total=max_total)
        print('Total grants fetched (no filter): %d' % len(all_grants))
        # Check a few for their categories
        for g in all_grants[:3]:
            cats = g.get('spending_categories', [])
            print('  Sample cats:', cats)
        return []
    
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
    
    for ic_data in ranked[:15]:
        ic = ic_data['ic'][:54] if len(ic_data['ic']) > 54 else ic_data['ic']
        print('%-55s %6d %5d %7.1f%% %8.2f' % (ic, ic_data['project_count'],
            ic_data['distinct_orgs'], ic_data['top5_concentration_percent'],
            ic_data['access_score']))
    
    print()
    print('Top 3 most accessible:')
    for ic_data in ranked[:3]:
        ic = ic_data['ic'][:54] if len(ic_data['ic']) > 54 else ic_data['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share, access score %.2f' % (ic,
            ic_data['project_count'], ic_data['distinct_orgs'],
            ic_data['top5_concentration_percent'], ic_data['access_score']))
    
    print()
    print('Least accessible (lowest 3):')
    for ic_data in ranked[-3:]:
        ic = ic_data['ic'][:54] if len(ic_data['ic']) > 54 else ic_data['ic']
        print('  %s: %d projects, %d orgs, %.1f%% top-5 share' % (ic,
            ic_data['project_count'], ic_data['distinct_orgs'],
            ic_data['top5_concentration_percent']))
    
    print()
    return ranked


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print('Usage: python3 nih_sbir_subsegment.py <spending_category_code>')
        print('Example: python3 nih_sbir_subsegment.py 101')
        sys.exit(1)
    
    category_code = sys.argv[1]
    ranked = run_screen(category_code)

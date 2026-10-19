#!/usr/bin/env python3
import urllib.request, json

# Explore NIH grants landscape - NIDDK (Diabetes, Digestive, Kidney) R01 grants
url = 'https://api.reporter.nih.gov/v2/projects/search'
payload = json.dumps({
    'criteria': {
        'fiscal_years': [2023],
        'activity_codes': ['R01'],  # Research Project Grant
        'agency_ic_codes': ['DK'],  # NIDDK
        'limit': 500
    },
    'offset': 0,
    'include_fields': ['appl_id', 'project_title', 'award_amount', 'organization', 'principal_investigators', 'agency_ic_fundings', 'spending_categories']
}).encode()

req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    data = json.load(r)
    print(f'Total: {data.get("meta", {}).get("total")}')
    results = data.get('results', [])
    print(f'Returned: {len(results)}')
    
    # Aggregate by organization
    org_stats = {}
    for result in results:
        org = result.get('organization', {})
        org_name = org.get('org_name', 'Unknown')
        amount = result.get('award_amount', 0) or 0
        if org_name not in org_stats:
            org_stats[org_name] = {'total': 0, 'count': 0}
        org_stats[org_name]['total'] += amount
        org_stats[org_name]['count'] += 1
    
    # Sort by total amount
    sorted_orgs = sorted(org_stats.items(), key=lambda x: x[1]['total'], reverse=True)
    total_amount = sum(s['total'] for s in org_stats.values())
    total_count = sum(s['count'] for s in org_stats.values())
    
    print(f'\nTotal amount: ${total_amount:,.0f}')
    print(f'Total grants: {total_count}')
    print(f'Distinct organizations: {len(org_stats)}')
    print(f'\nTop 20 organizations by total funding:')
    for i, (name, stats) in enumerate(sorted_orgs[:20]):
        share = stats['total'] / total_amount * 100
        print(f'  {i+1}. {name}: ${stats["total"]:,.0f} ({stats["count"]} grants, {share:.1f}%)')
    
    # Top 10 share
    top10_share = sum(s['total'] for _, s in sorted_orgs[:10]) / total_amount * 100
    print(f'\nTop 10 share: {top10_share:.1f}%')
    
    # Check if fragmented (top 10 < 80%)
    if top10_share < 80:
        print('FRAGMENTED: Top 10 < 80%')
    else:
        print('CONCENTRATED: Top 10 >= 80%')
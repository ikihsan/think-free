#!/usr/bin/env python3
import urllib.request, json

# Explore NIH grants - NIDDK R01 with pagination
def fetch_page(offset, limit=50):
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    payload = json.dumps({
        'criteria': {
            'fiscal_years': [2023],
            'activity_codes': ['R01'],
            'agency_ic_codes': ['DK'],
            'limit': limit
        },
        'offset': offset
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# Fetch multiple pages
all_results = []
for offset in [0, 50, 100, 150, 200, 250, 300, 350, 400, 450]:
    data = fetch_page(offset)
    results = data.get('results', [])
    if not results:
        break
    all_results.extend(results)
    print(f'Offset {offset}: {len(results)} results')
    if len(results) < 50:
        break

print(f'\nTotal collected: {len(all_results)}')

# Aggregate by organization
org_stats = {}
for result in all_results:
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

print(f'\nTotal amount (sample): ${total_amount:,.0f}')
print(f'Total grants (sample): {total_count}')
print(f'Distinct organizations: {len(org_stats)}')
print(f'\nTop 20 organizations by total funding:')
for i, (name, stats) in enumerate(sorted_orgs[:20]):
    share = stats['total'] / total_amount * 100 if total_amount else 0
    print(f'  {i+1}. {name}: ${stats["total"]:,.0f} ({stats["count"]} grants, {share:.1f}%)')

top10_share = sum(s['total'] for _, s in sorted_orgs[:10]) / total_amount * 100 if total_amount else 0
print(f'\nTop 10 share: {top10_share:.1f}%')
if top10_share < 80:
    print('FRAGMENTED: Top 10 < 80%')
else:
    print('CONCENTRATED: Top 10 >= 80%')
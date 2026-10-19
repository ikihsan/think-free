#!/usr/bin/env python3
import urllib.request, json

# Explore NIH SBIR/STTR grants (R43/R44, R41/R42)
def fetch_page(offset, activity_codes):
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    payload = json.dumps({
        'criteria': {
            'fiscal_years': [2023],
            'activity_codes': activity_codes,
            'limit': 50
        },
        'offset': offset
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# SBIR Phase I (R43), Phase II (R44)
# STTR Phase I (R41), Phase II (R42)
sbir_codes = ['R43', 'R44', 'R41', 'R42']

all_results = []
for offset in [0, 50, 100, 150, 200]:
    data = fetch_page(offset, sbir_codes)
    results = data.get('results', [])
    if not results:
        break
    all_results.extend(results)
    print(f'Offset {offset}: {len(results)} results')

print(f'\nTotal collected: {len(all_results)}')

if not all_results:
    print("No results")
    exit()

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

# Check total from meta
data = fetch_page(0, sbir_codes)
print(f'\nTotal from meta: {data.get("meta", {}).get("total")}')
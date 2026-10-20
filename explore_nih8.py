#!/usr/bin/env python3
import urllib.request, json

# Check fiscal_year distribution in results
def fetch_page(offset):
    url = 'https://api.reporter.nih.gov/v2/projects/search'
    payload = json.dumps({
        'criteria': {
            'fiscal_years': [2023],
            'activity_codes': ['R01'],
            'agency_ic_codes': ['DK'],
            'limit': 50
        },
        'offset': offset
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as r:
        return json.load(r)

# Check first few pages
for offset in [0, 1000, 5000, 10000, 20000]:
    data = fetch_page(offset)
    results = data.get('results', [])
    if not results:
        break
    years = {}
    for r in results:
        fy = r.get('fiscal_year')
        years[fy] = years.get(fy, 0) + 1
    print(f'Offset {offset}: fiscal_year distribution: {years}')
    if offset == 0:
        print(f'  Sample award_amount: {[r.get("award_amount") for r in results[:5]]}')
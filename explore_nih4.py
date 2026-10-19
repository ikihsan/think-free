#!/usr/bin/env python3
import urllib.request, json

# Explore NIH grants - check award amount field
url = 'https://api.reporter.nih.gov/v2/projects/search'
payload = json.dumps({
    'criteria': {
        'fiscal_years': [2023],
        'activity_codes': ['R01'],
        'agency_ic_codes': ['DK'],
        'limit': 10
    },
    'offset': 0
}).encode()

req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    data = json.load(r)
    for result in data.get('results', []):
        print(f"award_amount: {result.get('award_amount')}")
        print(f"agency_ic_fundings: {result.get('agency_ic_fundings')}")
        print(f"direct_cost_amt: {result.get('direct_cost_amt')}")
        print(f"indirect_cost_amt: {result.get('indirect_cost_amt')}")
        print("---")
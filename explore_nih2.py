#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore NIH RePORTER - check raw response
url = 'https://api.reporter.nih.gov/v2/projects/search'
payload = json.dumps({
    'criteria': {
        'fiscal_years': [2023],
        'limit': 5
    },
    'offset': 0
}).encode()

req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    data = json.load(r)
    print(f'Total: {data.get("meta", {}).get("total")}')
    if data.get('results'):
        print(f'First result keys: {list(data["results"][0].keys())}')
        print(json.dumps(data['results'][0], indent=2)[:2000])
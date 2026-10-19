#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore FEC API
url = 'https://api.open.fec.gov/v1/candidates/?api_key=DEMO_KEY&per_page=10&sort=-receipts&cycle=2024'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    print(f"Total: {data.get('pagination', {}).get('count', 'N/A')}")
    for cand in data.get('results', [])[:10]:
        print(f"  {cand.get('name')}: ${cand.get('receipts', 0):,} - {cand.get('party')} - {cand.get('state')} - {cand.get('office')}")
#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore FEC API - try simpler query
url = 'https://api.open.fec.gov/v1/committees/?api_key=DEMO_KEY&per_page=10&cycle=2024'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    print(f"Total: {data.get('pagination', {}).get('count', 'N/A')}")
    for comm in data.get('results', [])[:10]:
        print(f"  {comm.get('name')}: ${comm.get('receipts', 0):,} - {comm.get('committee_type')} - {comm.get('state')}")
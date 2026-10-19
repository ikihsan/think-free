#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore ProPublica Nonprofits
url = 'https://projects.propublica.org/nonprofits/api/v2/search.json?q=technology&page=1'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    print(f"Total results: {data.get('total_results')}")
    print(f"Page: {data.get('cur_page')}/{data.get('num_pages')}")
    for org in data.get('organizations', [])[:5]:
        print(f"  {org.get('ein')}: {org.get('name')} - Revenue: ${org.get('total_revenue')} - Assets: ${org.get('total_assets')} - State: {org.get('state')}")
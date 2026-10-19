#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore ProPublica Nonprofits - try different queries
queries = ['hospital', 'university', 'foundation', 'health', 'education', 'research']
for q in queries:
    url = f'https://projects.propublica.org/nonprofits/api/v2/search.json?q={urllib.parse.quote(q)}&page=1'
    with urllib.request.urlopen(url) as r:
        data = json.load(r)
        orgs = data.get('organizations', [])
        with_revenue = [o for o in orgs if o.get('total_revenue')]
        print(f'Query "{q}": {data.get("total_results")} total, {len(with_revenue)}/5 with revenue')
        for org in with_revenue[:3]:
            print(f"  {org.get('ein')}: {org.get('name')[:50]} - Revenue: ${org.get('total_revenue'):,} - State: {org.get('state')}")
    print()
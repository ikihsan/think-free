#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore ProPublica Nonprofits - get organization detail
# First get some EINs from search
url = 'https://projects.propublica.org/nonprofits/api/v2/search.json?q=hospital&page=1'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    orgs = data.get('organizations', [])
    for org in orgs[:3]:
        ein = org.get('ein')
        print(f"Getting detail for {ein}...")
        detail_url = f'https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json'
        with urllib.request.urlopen(detail_url) as r2:
            detail = json.load(r2)
            org_detail = detail.get('organization', {})
            filings = org_detail.get('filings_with_data', [])
            if filings:
                latest = filings[0]
                print(f"  {org_detail.get('name')[:60]}")
                print(f"    Revenue: ${latest.get('total_revenue', 'N/A'):,}")
                print(f"    Expenses: ${latest.get('total_expenses', 'N/A'):,}")
                print(f"    Assets: ${latest.get('total_assets', 'N/A'):,}")
                print(f"    Year: {latest.get('tax_prd_yr', 'N/A')}")
            else:
                print(f"  {org_detail.get('name')[:60]} - No filings with data")
        print()
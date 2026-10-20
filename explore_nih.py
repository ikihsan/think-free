#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore NIH RePORTER for research grants
url = 'https://api.reporter.nih.gov/v2/projects/search'
payload = json.dumps({
    'criteria': {
        'fiscal_years': [2023],
        'org_names': ['Harvard University', 'Stanford University', 'MIT', 'University of California'],
        'limit': 10
    },
    'offset': 0,
    'include_fields': ['ApplId', 'ProjectTitle', 'ProjectNum', 'TotalCost', 'Organization', 'PrincipalInvestigator', 'FiscalYear', 'FundingICs']
}).encode()

req = urllib.request.Request(url, data=payload, headers={'User-Agent': 'think-free-research/0.1', 'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    data = json.load(r)
    print(f'Meta: {data.get("meta")}')
    for result in data.get('results', [])[:10]:
        print(f'  {result.get("ApplId")}: ${result.get("TotalCost", 0):,} - {result.get("Organization", {}).get("OrgName", "")} - {result.get("ProjectTitle", "")[:80]}')
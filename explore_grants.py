#!/usr/bin/env python3
import urllib.request, json

# Explore USAspending grants
url = 'https://api.usaspending.gov/api/v2/references/toptier_agencies/'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    agencies = data.get('results', [])
    print(f"Total agencies: {len(agencies)}")
    # Look for grant-making agencies
    for a in agencies[:20]:
        print(f"  {a.get('toptier_code')}: {a.get('abbreviation')} - {a.get('agency_name')}")

print("\n--- Grant search ---")
# Search for grants
payload = {
    "filters": {
        "time_period": [{"start_date": "2020-01-01", "end_date": "2023-12-31"}],
        "award_type_codes": ["02", "03", "04", "05"],  # Grant types
    },
    "fields": ["Award ID", "Award Amount", "Description", "Awarding Agency", "Recipient Name", "Prime Award Transaction Obligation Amount"],
    "page": 1, "limit": 10, "subawards": False,
}
req = urllib.request.Request(
    "https://api.usaspending.gov/api/v2/search/spending_by_award/",
    data=json.dumps(payload).encode(),
    headers={"User-Agent": "think-free-research/0.1", "Content-Type": "application/json", "Accept": "application/json"}
)
with urllib.request.urlopen(req) as r:
    data = json.load(r)
    print(f"Results: {len(data.get('results', []))}")
    for result in data.get('results', [])[:5]:
        print(f"  {result.get('Award ID')}: ${result.get('Award Amount')} - {result.get('Recipient Name')} - {result.get('Awarding Agency')}")
#!/usr/bin/env python3
import urllib.request, json

# Check for duplicate grants (same project_serial_num)
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

# Collect project_serial_num
serials = set()
for offset in [0, 50, 100, 150, 200, 250, 300, 350, 400, 450]:
    data = fetch_page(offset)
    results = data.get('results', [])
    for r in results:
        serial = r.get('project_num_split', {}).get('serial_num')
        if serial:
            serials.add(serial)
    print(f'Offset {offset}: unique serials so far: {len(serials)}')

print(f'\nTotal unique serial_nums in 500 grants: {len(serials)}')

# Also check award_type
types = {}
for offset in [0, 50, 100, 150, 200]:
    data = fetch_page(offset)
    for r in data.get('results', []):
        at = r.get('award_type')
        types[at] = types.get(at, 0) + 1
print(f'Award types: {types}')
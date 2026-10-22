#!/usr/bin/env python3
import json
import urllib.request

def fetch_page(os, rows=50):
    url = f"https://search.worldbank.org/api/v2/projects?format=json&rows={rows}&fl=id,mjthemecode,impagency,boardapprovaldate,totalcommamt,project_name&os={os}"
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free research'})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

# Search for 2015-2019 and 2020-2024 windows
# Offset 0 gives 2022-2024, so 2020-2024 should be near the beginning
# Let me check various offsets
offsets = list(range(0, 5000, 200)) + list(range(5000, 15000, 500))
for os in offsets:
    try:
        data = fetch_page(os)
        projects = data.get('projects', {})
        dates = []
        for pid, p in projects.items():
            date = p.get('boardapprovaldate', '')
            if date:
                dates.append(int(date[:4]))
        if dates:
            print(f"Offset {os:5d}: Year range: {min(dates)} - {max(dates)} ({len(dates)} projects)")
    except Exception as e:
        print(f"Offset {os:5d}: Error: {e}")
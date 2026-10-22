#!/usr/bin/env python3
import json
import sys
import urllib.request

def fetch_page(os, rows=20):
    url = f"https://search.worldbank.org/api/v2/projects?format=json&rows={rows}&fl=id,mjthemecode,impagency,boardapprovaldate,totalcommamt,project_name&os={os}"
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free research'})
    with urllib.request.urlopen(req) as response:
        return json.load(response)

for os in [12000, 14000, 16000, 18000, 20000, 21000, 22000]:
    print(f"=== Offset {os} ===")
    try:
        data = fetch_page(os)
        projects = data.get('projects', {})
        dates = []
        for pid, p in projects.items():
            date = p.get('boardapprovaldate', '')
            if date:
                dates.append(date[:4])
        if dates:
            print(f"  Year range: {min(dates)} - {max(dates)}")
        else:
            print("  No dates")
    except Exception as e:
        print(f"  Error: {e}")
#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore NSF Awards - try different keywords
keywords = ['computer', 'software', 'machine learning', 'cybersecurity', 'robotics']
for kw in keywords:
    url = f'https://api.nsf.gov/services/v1/awards.json?keyword={urllib.parse.quote(kw)}&printFields=id,title,amount,awardeeName,startDate,expDate&rows=3'
    with urllib.request.urlopen(url) as r:
        data = json.load(r)
        awards = data.get('response', {}).get('award', [])
        print(f'Keyword "{kw}": {len(awards)} awards')
        for award in awards:
            print(f"  {award.get('id')}: ${award.get('amount')} - {award.get('awardeeName')} - {award.get('title')[:60]}")
    print()
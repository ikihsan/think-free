#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore NSF Awards - try without rows
url = 'https://api.nsf.gov/services/v1/awards.json?keyword=computer&printFields=id,title,amount,awardeeName,startDate,expDate'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    print(json.dumps(data, indent=2)[:3000])
#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Explore NSF Awards - check raw response
url = 'https://api.nsf.gov/services/v1/awards.json?keyword=computer&printFields=id,title,amount,awardeeName,startDate,expDate&rows=5'
with urllib.request.urlopen(url) as r:
    data = json.load(r)
    print(json.dumps(data, indent=2)[:2000])
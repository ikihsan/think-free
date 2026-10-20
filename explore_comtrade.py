#!/usr/bin/env python3
import urllib.request, json, time

# Explore Comtrade more systematically
# Get all HS codes for USA imports in 2023, sorted by value

# First, let's get a broader set of HS codes for USA
# We'll try chapters (2-digit) to see what's big
chapters = []
for i in range(1, 99):
    if i in [77, 98, 99]:  # Reserved/special chapters
        continue
    hs = f"{i:02d}0000"  # Chapter level (first 2 digits)
    url = f'https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=2023&reporterCode=842&cmdCode={hs}&flowCode=M&partnerCode=0'
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
            if data.get('data'):
                d = data['data'][0]
                val = d.get('primaryValue', 0)
                if val > 0:
                    chapters.append((hs, val, d.get('cmdDesc', '')))
                    print(f"Chapter {hs}: ${val:,.0f}")
            else:
                print(f"Chapter {hs}: no data")
    except Exception as e:
        print(f"Chapter {hs}: ERROR {e}")
    time.sleep(0.3)

# Sort by value
chapters.sort(key=lambda x: x[1], reverse=True)
print("\nTop 20 chapters by import value:")
for hs, val, desc in chapters[:20]:
    print(f"  {hs}: ${val:,.0f}")
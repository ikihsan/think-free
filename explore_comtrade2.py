#!/usr/bin/env python3
import urllib.request, json, time

# Explore Comtrade - focus on specific high-value chapters
# Known high-value chapters from general knowledge
chapters = [
    ('27', 'Mineral fuels, oils'),
    ('84', 'Nuclear reactors, machinery'),
    ('85', 'Electrical machinery'),
    ('87', 'Vehicles'),
    ('90', 'Optical, medical instruments'),
    ('30', 'Pharmaceuticals'),
    ('29', 'Organic chemicals'),
    ('39', 'Plastics'),
    ('72', 'Iron and steel'),
    ('71', 'Pearls, precious metals'),
    ('88', 'Aircraft'),
    ('73', 'Articles of iron/steel'),
    ('94', 'Furniture'),
    ('62', 'Apparel'),
    ('61', 'Knit apparel'),
    ('64', 'Footwear'),
    ('44', 'Wood'),
    ('48', 'Paper'),
    ('76', 'Aluminum'),
    ('89', 'Ships'),
]

for ch, desc in chapters:
    hs = f"{ch}0000"
    url = f'https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=2023&reporterCode=842&cmdCode={hs}&flowCode=M&partnerCode=0'
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.load(r)
            if data.get('data'):
                d = data['data'][0]
                val = d.get('primaryValue', 0)
                if val > 0:
                    print(f"Chapter {ch} ({desc}): ${val:,.0f}")
                else:
                    print(f"Chapter {ch} ({desc}): $0")
            else:
                print(f"Chapter {ch} ({desc}): no data")
    except Exception as e:
        print(f"Chapter {ch} ({desc}): ERROR {e}")
    time.sleep(1)
#!/usr/bin/env python3
"""E060 probe: do static version badges in READMEs match the repo's latest release?"""
import json, re, subprocess, sys, time, urllib.request, urllib.error, base64

repos = []
for lang in ('python', 'rust', 'javascript'):
    d = json.load(open(f'/tmp/opencode/repos_{lang}.json'))
    repos += [(lang, i['full_name']) for i in d['items']]
print(len(repos), 'repos')

def get(url, raw=False):
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free probe', 'Accept': 'application/vnd.github+json'})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.read()
    except Exception as e:
        return None

def readme(full):
    b = get(f'https://api.github.com/repos/{full}/readme')
    if not b: return ''
    try:
        j = json.loads(b)
        return base64.b64decode(j['content']).decode('utf-8', 'replace')
    except Exception:
        return ''

def latest(full):
    b = get(f'https://api.github.com/repos/{full}/releases/latest')
    if not b: return None
    try: return json.loads(b)['tag_name']
    except Exception: return None

BADGE = re.compile(r'(?:img\.shields\.io|shields\.io/badge|badge/)[^"\)\s]*version[^"\)\s]*', re.I)
STATIC = re.compile(r'version-v?([^-]+?)-(?:blue|green|brightgreen|orange|red|yellow|informational)', re.I)

ok = 0; withbadge = 0; static = 0; drift = 0; rows = []
for lang, full in repos:
    rd = readme(full); time.sleep(1.0)
    rel = latest(full); time.sleep(1.0)
    row = {'repo': full, 'release': rel}
    badges = set()
    for m in re.finditer(r'(?:!\[[^\]]*\]\(|<img[^>]+src="|\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)|src=")([^"\)\s]*(?:version)[^"\)\s]*)', rd, re.I):
        for s in STATIC.findall(m.group(1)):
            badges.add(s)
    row['static_badges'] = sorted(badges)
    if badges: withbadge += 1
    for b in badges:
        static += 1
        if rel and b.lstrip('v').rstrip('.x') not in rel.lstrip('v'):
            drift += 1
    rows.append(row); ok += 1
    if ok % 15 == 0: print(ok, withbadge, static, drift)

print(f"repos={ok} with_static_version_badge={withbadge} static_badges={static} drifted={drift}")
json.dump(rows, open('raw/rows.json', 'w'), indent=1)
for r in rows:
    if r['static_badges']:
        print(r['repo'], r['release'], r['static_badges'])

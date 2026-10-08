#!/usr/bin/env python3
"""E059 probe: do top PyPI packages' import names / commands match their pip names?

Sample: stride 125 over the downloaded top-15000 list (120 rows).
For each row: fetch PyPI JSON (1 request), pick a wheel for this platform
(py3-none-any preferred, else any py3 wheel), download it (<=8 MiB), read
top-level import packages (top_level.txt + RECORD dirs) and console_scripts.

Measurements per row:
  M1: normalized pip name in normalized import names? (True/False/None=none found)
  M2: every console script normalized name == normalized pip name? (True/False/None)
Kill gate (declared): if M1-mismatch share < 0.05 AND M2-mismatch share < 0.10,
the population is not observed -> nothing to build.
"""
import json, re, sys, time, urllib.request, urllib.error, zipfile, io, collections

TOP = json.load(open('raw/top-pypi.json'))['rows']
ROWS = TOP[::125]
print(f"sample rows: {len(ROWS)}")

def norm(s): return re.sub(r'[-_.]+', '-', s.lower())

def fetch(url, tries=2):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'think-free probe (research)'})
            return urllib.request.urlopen(req, timeout=20).read()
        except Exception as e:
            if i == tries-1: raise
            time.sleep(1)

results = []
for idx, row in enumerate(ROWS):
    name = row['project']
    rec = {'project': name, 'downloads': row['download_count']}
    try:
        meta = json.loads(fetch(f'https://pypi.org/pypi/{name}/json'))
        files = meta['urls']
        wheels = [f for f in files if f['filename'].endswith('.whl') and 'py3' in f['filename']]
        wheels.sort(key=lambda f: 0 if 'none-any' in f['filename'] else 1)
        if not wheels or wheels[0]['size'] > 8*1024*1024:
            rec['status'] = 'no-wheel'
            results.append(rec); continue
        data = fetch(wheels[0]['url'])
        z = zipfile.ZipFile(io.BytesIO(data))
        names = z.namelist()
        tl_files = [n for n in names if n.endswith('top_level.txt')]
        imports = set()
        for t in tl_files:
            for line in z.read(t).decode().split():
                imports.add(line.strip())
        # fallback: first path segment of RECORD entries that are packages
        if not imports:
            recs = [n for n in names if n.endswith('RECORD')]
            if recs:
                for line in z.read(recs[0]).decode().splitlines()[1:]:
                    p = line.split(',')[0]
                    if '/' in p: imports.add(p.split('/')[0])
        imports = {i for i in imports if i and not i.endswith('.dist-info')}
        npn = norm(name)
        m1 = any(norm(i) == npn for i in imports) if imports else None
        scripts = set()
        ep = [n for n in names if n.endswith('entry_points.txt')]
        for e in ep:
            for line in z.read(e).decode().splitlines():
                m = re.match(r'\s*([\w.-]+)\s*=', line)
                if m and '[console_scripts]' in z.read(e).decode()[:z.read(e).decode().find(line)+1]:
                    scripts.add(m.group(1))
        # simpler: parse sections
        scripts = set()
        for e in ep:
            section = None
            for line in z.read(e).decode().splitlines():
                if line.strip().startswith('['): section = line.strip()
                elif section == '[console_scripts]':
                    m = re.match(r'\s*([\w.-]+)\s*=', line)
                    if m: scripts.add(m.group(1))
        m2 = (all(norm(s) == npn for s in scripts)) if scripts else None
        rec.update(status='ok', imports=sorted(imports)[:6], scripts=sorted(scripts)[:6], m1=m1, m2=m2)
    except Exception as e:
        rec.update(status=f'error:{type(e).__name__}')
    results.append(rec)
    if idx % 20 == 0: print(idx, rec['project'], rec.get('status'))

ok = [r for r in results if r['status'] == 'ok']
m1_rows = [r for r in ok if r['m1'] is not None]
m2_rows = [r for r in ok if r['m2'] is not None]
m1_bad = [r for r in m1_rows if not r['m1']]
m2_bad = [r for r in m2_rows if not r['m2']]
print(f"ok={len(ok)} m1_evaluable={len(m1_rows)} m1_mismatch={len(m1_bad)} m2_evaluable={len(m2_rows)} m2_mismatch={len(m2_bad)}")
print('M1 mismatch examples:', [(r['project'], r['imports']) for r in m1_bad][:10])
print('M2 mismatch examples:', [(r['project'], r['scripts']) for r in m2_bad][:10])
json.dump(results, open('raw/results.json','w'), indent=1)

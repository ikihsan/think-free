#!/usr/bin/env python3
"""E131 — baseline: label Java repos with base v2 classifier."""
from __future__ import print_function

import json, os, sys, re, random
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(script_dir)
elev = os.path.join(parent, '113-viewcount-matched-harvest')
sys.path.insert(0, elev)
import labeling_improved as L_base

with open(os.path.join(script_dir, "raw_pool.json"), 'r') as f:
    pool = json.load(f)

print('Pool rows: %d' % len(pool))

# Label with base v2 classifier (label_masked)
labels = []
for i, row in enumerate(pool):
    description = row.get("description")
    if description:
        label = L_base.label_masked(description)[0]
    else:
        label = "unlabelled"
    labels.append(label)
    if (i + 1) % 100 == 0:
        print("  Labeled %d/%d" % (i + 1, len(pool)))

need_count = sum(1 for l in labels if l == "need")
generic_count = sum(1 for l in labels if l == "generic")
unlabelled_count = sum(1 for l in labels if l == "unlabelled")

print()
print("Label counts (base v2 classifier):")
print("  need: %d" % need_count)
print("  generic: %d" % generic_count)
print("  unlabelled: %d" % unlabelled_count)
print("  total: %d" % len(labels))
print()

# G1 check
g1_pass = need_count >= 100 and generic_count >= 100
print("G1 (population >= 100/100): %s (need=%d, generic=%d)" %
      ('PASS' if g1_pass else 'FAIL', need_count, generic_count))

# G0 check
g0_result = L_base.g0_score()
print()
print("G0 (planted positive recovery):")
print("  planted_need_recovered: %d/%d" % (g0_result['planted_need_recovered'], g0_result['planted_need_total']))
print("  planted_generic_recovered: %d/%d" % (g0_result['planted_generic_recovered'], g0_result['planted_generic_total']))
print("  pass: %s" % ('PASS' if g0_result['pass'] else 'FAIL'))
print("  threshold: %d" % g0_result['threshold'])

# Store stars per label
stars_need = []
stars_generic = []
need_rows = []
generic_rows = []

for i, (row, label) in enumerate(zip(pool, labels)):
    stars = row['stargazers_count']
    if label == 'need':
        stars_need.append(stars)
        need_rows.append(row)
    elif label == 'generic':
        stars_generic.append(stars)
        generic_rows.append(row)

def cliffs_delta(x, y):
    if not x or not y: return 0.0
    greater = less = tied = 0
    for xi in x:
        for yi in y:
            if xi > yi: greater += 1
            elif xi < yi: less += 1
            else: tied += 1
    n_x = len(x); n_y = len(y)
    if n_x == 0 or n_y == 0: return 0.0
    return (greater - less) / (n_x * n_y)

def permutation_test(x, y, delta_observed, iters=20000):
    combined = x + y
    count_ge = 0
    for _ in range(iters):
        random.shuffle(combined)
        x_perm = combined[:len(x)]
        y_perm = combined[len(x):]
        d = cliffs_delta(x_perm, y_perm)
        if abs(d) >= abs(delta_observed):
            count_ge += 1
    return count_ge / iters

# G2
delta_stars = cliffs_delta(stars_need, stars_generic)
perm_p_stars = permutation_test(stars_need, stars_generic, delta_stars, iters=20000)
print()
print("G2 (cliffs delta on stars): %.4f, p=%.4f" % (delta_stars, perm_p_stars))

# G3 stars/year created
def years_since_created(row):
    created_str = row.get('created_at')
    if not created_str: return None
    try:
        created_at = datetime.strptime(created_str, '%Y-%m-%dT%H:%M:%SZ')
        age = (datetime.utcnow() - created_at).days / 365.25
        return max(age, 1.0)
    except: return None

need_spy = []
generic_spy = []

for row in need_rows:
    y = years_since_created(row)
    stars = row['stargazers_count']
    if y and y > 0: need_spy.append(stars / y)
for row in generic_rows:
    y = years_since_created(row)
    stars = row['stargazers_count']
    if y and y > 0: generic_spy.append(stars / y)

print()
print("G3 (stars/year, age-controlled via created_at):")
if need_spy:
    print("  need: n=%d, mean %.2f, median %.2f" % (len(need_spy), sum(need_spy)/len(need_spy), sorted(need_spy)[len(need_spy)//2]))
else:
    print("  need: no data")
if generic_spy:
    print("  generic: n=%d, mean %.2f, median %.2f" % (len(generic_spy), sum(generic_spy)/len(generic_spy), sorted(generic_spy)[len(generic_spy)//2]))
else:
    print("  generic: no data")

if need_spy and generic_spy:
    delta_spy = cliffs_delta(need_spy, generic_spy)
    perm_p_sy = permutation_test(need_spy, generic_spy, delta_spy, iters=20000)
    print("  permutation p (stars/year, iters=20000): %.4f" % perm_p_sy)

print()
print("=== SUMMARY ===")
print("Coverage (base v2): need=%d, generic=%d, unlabelled=%d out of %d total" %
      (need_count, generic_count, unlabelled_count, len(pool)))
print("G1 pass: %s" % ('YES' if g1_pass else 'NO'))
print("G0 pass: %s" % ('YES' if g0_result['pass'] else 'NO'))
print("G2 delta: %.4f, p=%.4f" % (delta_stars, perm_p_stars))
if need_spy and generic_spy:
    print("G3 delta: %.4f, p=%.4f" % (delta_spy, perm_p_sy))
else:
    print("G3: insufficient data")
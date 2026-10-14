#!/usr/bin/env python3
"""Quick test: label JavaScript repos with JS-adapted v2 classifier."""
from __future__ import print_function

import json, time, re, sys
import os

# Add the E113 directory to path for the v2 classifier base
# The script is in EXPERIMENTS/130-viewcount-js-repos-matched-harvest/
ELEVEN3_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'EXPERIMENTS', '113-viewcount-matched-harvest')
sys.path.insert(0, ELEVEN3_DIR)

import labeling_improved as L_base

# JS-specific additions
JS_NEED_INDICATORS = {'npm', 'node', 'package.json', 'express', 'react', 'cli tool'}
JS_GENERIC_TERMS = {'library', 'framework', 'starter kit', 'microservice'}

EXTENDED_NEED_INDICATORS = L_base.NEED_INDICATORS | JS_NEED_INDICATORS
EXTENDED_GENERIC_TERMS = L_base.GENERIC_TERMS | JS_GENERIC_TERMS

def _anchored_patterns(terms):
    pats = []
    for term in sorted(terms, key=len, reverse=True):
        parts = [re.escape(w) for w in term.split()]
        pats.append(re.compile(r'\b' + r'\s+'.join(parts) + r'\b'))
    return pats

EXTENDED_NEED_PATTERNS = _anchored_patterns(EXTENDED_NEED_INDICATORS)
EXTENDED_GENERIC_PATTERNS = _anchored_patterns(EXTENDED_GENERIC_TERMS)

with open('raw_pool.json', 'r') as f:
    pool = json.load(f)

print('Pool rows:', len(pool))
start = time.time()
labels = []
for i, row in enumerate(pool):
    description = row.get('description')
    if description:
        text = description.lower()
        masked = text
        need_hit = []
        for pat in EXTENDED_NEED_PATTERNS:
            masked, n = pat.subn(' ', masked)
            if n:
                need_hit.append(pat.pattern)
        generic_hit = [p.pattern for p in EXTENDED_GENERIC_PATTERNS if p.search(masked)]
        has_need, has_gen = bool(need_hit), bool(generic_hit)
        if has_need and not has_gen:
            label = 'need'
        elif has_gen and not has_need:
            label = 'generic'
        else:
            label = 'unlabelled'
    else:
        label = 'unlabelled'
    labels.append(label)
    if (i + 1) % 100 == 0:
        print('  Labeled %d/%d (%.1fs)' % (i+1, len(pool), time.time()-start))
        start = time.time()

need_count = sum(1 for l in labels if l == 'need')
generic_count = sum(1 for l in labels if l == 'generic')
unlabelled_count = sum(1 for l in labels if l == 'unlabelled')
print()
print('need:', need_count, 'generic:', generic_count, 'unlabelled:', unlabelled_count, 'total:', len(labels))
print('Coverage:', 100.0 * (need_count + generic_count) / len(labels), '%')
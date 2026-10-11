#!/usr/bin/env python3
"""E105 — View-count principle on Stack Overflow (software Q&A)."""

import urllib.request, json, time, sys
from collections import Counter
import numpy as np
from scipy import stats

# Fetch Stack Overflow questions sorted by view count
questions = []
try:
    url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=view_count&pagesize=100&site=stackoverflow'
    r = urllib.request.urlopen(url, timeout=15)
    data = json.loads(r.read().decode())
    questions = data.get('items', [])
    print('Fetched %d Stack Overflow questions sorted by view_count' % len(questions))
except Exception as e:
    print('Error fetching questions: %s' % e)
    questions = []

# Classify questions as need-related or random
need_keywords = ['error', 'bug', 'fix', 'problem', 'issue', 'how to', 'crash', 'debug']
generic_keywords = ['introduction', 'tutorial', 'overview', 'getting started']

classified = []
for q in questions:
    title = q.get('title', '').lower()
    body = q.get('body', '').lower()[:500]
    text = title + ' ' + body

    need_matches = sum(1 for kw in need_keywords if kw in text)
    generic_matches = sum(1 for kw in generic_keywords if kw in text)

    if need_matches > generic_matches and need_matches > 0:
        classification = 'need-related'
    elif generic_matches > 0 and need_matches == 0:
        classification = 'random'
    else:
        classification = 'ambiguous'

    classified.append({
        'title': q.get('title', '')[:100],
        'views': q.get('view_count', 0),
        'answers': q.get('answer_count', 0),
        'classification': classification
    })

n_need = sum(1 for c in classified if c['classification'] == 'need-related')
n_random = sum(1 for c in classified if c['classification'] == 'random')
n_ambiguous = sum(1 for c in classified if c['classification'] == 'ambiguous')

print('Classification: need-related=%d, random=%d, ambiguous=%d' % (n_need, n_random, n_ambiguous))
print('Total classified: %d' % len(classified))

# G1: Sample size
g1_pass = n_need + n_random >= 100
print('G1 (sample size >= 100 with valid classification): %s' % ('PASS' if g1_pass else 'FAIL (valid=%d)' % (n_need + n_random)))

if n_need + n_random >= 50:
    need_views = np.array([c['views'] for c in classified if c['classification'] == 'need-related'])
    random_views = np.array([c['views'] for c in classified if c['classification'] == 'random'])

    if len(need_views) > 0 and len(random_views) > 0:
        # G2: Mann-Whitney U test and Cliff's delta
        u_stat, p_value = stats.mannwhitneyu(need_views, random_views, alternative='two-sided')

        n = len(need_views)
        m = len(random_views)
        count_less = 0
        count_greater = 0
        for xi in need_views:
            for yi in random_views:
                if xi < yi:
                    count_less += 1
                elif xi > yi:
                    count_greater += 1
        total = n * m
        delta = (count_greater - count_less) / total if total > 0 else 0

        g2_pass = p_value < 0.05 and abs(delta) > 0.147
        print('G2 (Mann-Whitney p<0.05 and |Cliff\\'s delta| > 0.147): %s' % ('PASS' if g2_pass else 'FAIL'))

        # G3: median comparison (Wilson CI95 LB > 0.60 adapted)
        need_median = np.median(need_views) if len(need_views) > 0 else 0
        random_median = np.median(random_views) if len(random_views) > 0 else 0
        g3_pass = need_median > random_median
        print('G3 (need-related median view > random median view): %s (need_median=%d, random_median=%d)' % ('PASS' if g3_pass else 'FAIL', need_median, random_median))

        # G4: Both categories represented
        g4_pass = n_need > 0 and n_random > 0
        print('G4 (both categories represented): %s' % ('PASS' if g4_pass else 'FAIL'))

        print()
        all_pass = g1_pass and g2_pass and g3_pass and g4_pass
        print('Overall: %s' % ('ALL GATES PASS' if all_pass else 'GATES CLOSED'))
    else:
        print('Not enough data for statistical comparison')
else:
    print('Not enough classified items for statistical analysis (need >= 50 valid)')
PYEOF
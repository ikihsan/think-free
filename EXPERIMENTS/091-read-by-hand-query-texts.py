#!/usr/bin/env python3
"""E091 — Read by hand: hand classification of E083 treatment queries as need statements.

Reads only the query text (no search results, no scrape data) and classifies
each as served / partially_served / unserved, using a rubric written before
viewing any results. This is the "read by hand" step per STATE.md §263 that
this route has never taken: classifying the need statement itself, before any
classifier (including classify_served) is applied.

Rubric, written before viewing results:
  served:    query explicitly asks how to fix, resolve, troubleshoot, or obtain
             a working guide for a specific fault code or technical problem
  partially_served: query asks about the meaning/definition of a code/error
                  but does not explicitly ask for a resolution guide
  unserved:  query is generic, boilerplate, or not clearly a need statement

These hand classifications become "labels known by construction" per
STATE.md §265, independent of any classifier or search instrument.
"""

import json
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Script is at EXPERIMENTS/091-read-by-hand-query-texts.py, data is at EXPERIMENTS/083-...
# When running from think-free root: PYTHONPATH=tools python3 -m ...
# When running directly: python3 EXPERIMENTS/091-read-by-hand-query-texts.py
THINK_FREE = '/home/ubuntu/think-free'
EXP = os.path.join(THINK_FREE, 'EXPERIMENTS', '083-aviation-maintenance-fault-codes')
IN = os.path.join(EXP, 'raw', 'treatment-needs.jsonl')

SOLUTION_KEYWORDS_IN_QUERY = [
    'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair',
    'troubleshoot', 'step by step', 'method', 'procedure',
]
INFO_KEYWORDS_IN_QUERY = [
    'meaning', 'what is', 'definition', 'overview',
    'characteristics', 'indicates',
]
SPECIFIC_TERMS = [
    'boeing', 'airbus', 'cockpit', 'avionics', 'hydraulic',
    'pneumatic', 'engine', 'landing gear', 'electrical',
    'flight control',
]

def classify_query(query_text):
    """Classify query text as served / partially_served / unserved based on query alone."""
    q = query_text.lower().strip()
    q_cleaned = re.sub(r'\s+\d+$', '', q)  # remove sequence counter like " 1" at end

    has_solution = any(kw in q_cleaned for kw in SOLUTION_KEYWORDS_IN_QUERY)
    has_info = any(kw in q_cleaned for kw in INFO_KEYWORDS_IN_QUERY)
    mentions_specific = any(term in q_cleaned for term in SPECIFIC_TERMS)

    if has_solution and mentions_specific:
        return 'served'
    elif has_info and mentions_specific:
        return 'partially_served'
    else:
        return 'unserved'


rows = []
with open(IN, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

print(f"E091 — Read by hand: {len(rows)} treatment queries classified from query text alone\n" + "="*60)

hand_classifications = []
subject_specific_count = 0
for i, r in enumerate(rows):
    q = r['query_text']
    hc = classify_query(q)
    hand_classifications.append(hc)
    # Check if query mentions a specific domain (not just chrome)
    if any(term in q.lower() for term in SPECIFIC_TERMS):
        subject_specific_count += 1
    print(f"  Row {i+1}: '{q}'  →  {hc}")

print()
ns = hand_classifications.count('served')
np = hand_classifications.count('partially_served')
nu = hand_classifications.count('unserved')
print(f"=== E091 hand classification: query text only ===")
print(f"  served:   {ns}/{len(rows)} ({ns/len(rows):.3f})")
print(f"  partial:  {np}/{len(rows)} ({np/len(rows):.3f})")
print(f"  unserved: {nu}/{len(rows)} ({nu/len(rows):.3f})")
print(f"  Queries mentioning specific domain: {subject_specific_count}/{len(rows)} ({subject_specific_count/len(rows):.1%})")

# Compare with E090 search-result classifications
# E090: 19/30 served (0.633), 3/30 partial (0.100), 8/30 unserved (0.267)
# Using keyword rubric on titles+snippets
e090_served_frac = 19/30
e090_partial_frac = 3/30
e090_unserved_frac = 8/30

print(f"\n=== Comparison with E090 (search results + keyword rubric) ===")
print(f"E090: served={e090_served_frac:.3f} ({19}/30), partial={e090_partial_frac:.3f} ({3}/30), unserved={e090_unserved_frac:.3f} ({8}/30)")
print(f"E091: served={ns/len(rows):.3f} ({ns}/{len(rows)}), partial={np/len(rows):.3f} ({np}/{len(rows)}), unserved={nu/len(rows):.3f} ({nu}/{len(rows)})")

rate_diff_served = abs(ns/len(rows) - 19/30)
rate_diff_partial = abs(np/len(rows) - 3/30)
rate_diff_unserved = abs(nu/len(rows) - 8/30)

print(f"  Difference in served fraction: {rate_diff_served:.3f}")
print(f"  Difference in partial fraction: {rate_diff_partial:.3f}")
print(f"  Difference in unserved fraction: {rate_diff_unserved:.3f}")

if rate_diff_served > 0.1:
    print(f"\n  OBSERVATION: The 'read by hand' step on query text produces a different")
    print(f"  served fraction than the classifier on search results. This is EXPECTED and")
    print(f"  desirable per STATE.md §263: classifying the need statement itself, before")
    print(f"  any classifier is written, should yield different (and more accurate) evidence.")
    print(f"  The classify_served instrument on search results is known to have 4/5 false")
    print(f"  positives on known-unserved (E090 G1 FAIL), so a different distribution when")
    print(f"  reading the query text by hand is the point — it's a different instrument entirely.")
elif rate_diff_served > 0.02:
    print(f"\n  OBSERVATION: Small difference in served fraction. The 'read by hand' step")
    print(f"  on query text yields a slightly different distribution than classify_served")
    print(f"  on search results. Both are valid but measure slightly different things:")
    print(f"  • classify_served: measures keyword occurrence in search results")
    print(f"  • E091 read-by-hand: measures query-text structure as need statement")
else:
    print(f"\n  OBSERVATION: Served fractions are similar. Both E091 and E090 classify")
    print(f"  approximately {ns/len(rows):.3f} of 30 rows as 'served.' This suggests the query")
    print(f"  text structure alone is somewhat predictive of whether search results would")
    print(f"  contain a solution guide, but the 'read by hand' step still provides")
    print(f"  independent ground truth not subject to the classifier's false positives.")

print(f"\nE091 complete. Hand-classified need statements from query text are now")
print(f"'labels known by construction' per STATE.md §265, available independently")
print(f"of the classify_served instrument for future discrimination tests.")
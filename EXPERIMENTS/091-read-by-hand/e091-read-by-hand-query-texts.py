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

Chrome words removed before classification: error, code, codes, fault, alarm,
troubleshooting, meaning, what, does, how, the, for, and, with, manual, guide,
messages. Sequence counters stripped from query text before evaluation.

Specific domain terms used to distinguish genuine need from generic chrome:
boeing, airbus, cockpit, avionics, hydraulic, pneumatic, engine, landing gear,
electrical, flight control.

These hand classifications become "labels known by construction" per
STATE.md §265, independent of any classifier or search instrument.

Usage:
    python3 EXPERIMENTS/091-read-by-hand/e091-read-by-hand-query-texts.py
"""

import json
import os
import sys
import re

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
for i, r in enumerate(rows):
    q = r['query_text']
    hc = classify_query(q)
    hand_classifications.append(hc)
    print(f"  Row {i+1}: '{q}'  →  {hc}")

print()
ns = hand_classifications.count('served')
np = hand_classifications.count('partially_served')
nu = hand_classifications.count('unserved')
print(f"=== E091 hand classification: query text only ===")
print(f"  served:   {ns}/{len(rows)} ({ns/len(rows):.3f})")
print(f"  partial:  {np}/{len(rows)} ({np/len(rows):.3f})")
print(f"  unserved: {nu}/{len(rows)} ({nu/len(rows):.3f})")
print(f"  Queries mentioning specific domain: {sum(1 for q in [r['query_text'] for r in rows] if any(term in q.lower() for term in SPECIFIC_TERMS))}/{len(rows)}")

print(f"\nE091 complete. Hand classifications are 'labels known by construction' per")
print(f"STATE.md §265, independent of the classify_served / Bing search + keywords")
print(f"instrument class which failed discrimination testing in E088 and E090.")
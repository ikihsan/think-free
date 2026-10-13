#!/usr/bin/env python3
"""
E124 — GNOME Discourse-specific classifier with IMPROVED excluded patterns.

This classifier addresses the precision defect found in E123 (meta.discourse.org):
blog posts, case studies, announcements, and content marketing were misclassified
as "need-related" because they contain question-form patterns.

IMPROVEMENTS over classifier_discourse (declared BEFORE measurement on this domain):
1. Blog/content marketing exclusion patterns
2. Announcement/celebration exclusion patterns
3. "Getting Started" guide exclusion (when presented as published content)
4. Case study/tutorial exclusion (when not a question)
"""

import os
import json

_CACHE = {}


def _load(filename, key):
    """A moved-out data list, read once and cached.

    The list was inline here as a Python literal and pushed the file over
    the 300-line cap in `docs/policy/doc-standards.md`; it is data, so it
    now lives in a `.json` sibling, which the cap exempts.
    """
    if not _CACHE:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              filename), encoding="utf-8") as handle:
            _CACHE.update(json.load(handle))
    return _CACHE[key]


import re
from collections import Counter


# Need-related indicators for Discourse forums (same as classifier_discourse)
# Question forms + technical problem/error keywords
DISCOURSE_NEED_PATTERNS = _load('gnome_patterns.json', 'DISCOURSE_NEED_PATTERNS')


# IMPROVED Excluded patterns for Discourse (addressing E123 precision defect)
# Hard exclusion — if any matches, classify as 'random' regardless of need patterns
DISCOURSE_EXCLUDED_PATTERNS = _load('gnome_patterns.json', 'DISCOURSE_EXCLUDED_PATTERNS')


def compile_patterns(patterns):
    """Compile patterns with IGNORECASE flag."""
    return [(re.compile(p, re.IGNORECASE), p) for p in patterns]


DISCOURSE_NEED_COMPILED = compile_patterns(DISCOURSE_NEED_PATTERNS)
DISCOURSE_EXCLUDED_COMPILED = compile_patterns(DISCOURSE_EXCLUDED_PATTERNS)


def classify_gnome_item(title_body: str) -> str:
    """
    Classify a Discourse topic as 'need-related', 'random', or 'unclassified'.
    
    Strategy (declared before measurement):
    1. If any excluded pattern matches (case-insensitive) → 'random'
    2. If any need-related pattern matches (case-insensitive) → 'need-related'
    3. Otherwise → 'unclassified' (counts toward coverage deficit)
    """
    if not title_body:
        return 'unclassified'

    combined = title_body.lower()

    # Step 1: excluded patterns → random (hard exclusion)
    for pat, _ in DISCOURSE_EXCLUDED_COMPILED:
        if pat.search(combined):
            return 'random'

    # Step 2: need-related patterns → need-related
    for pat, _ in DISCOURSE_NEED_COMPILED:
        if pat.search(combined):
            return 'need-related'

    # Step 3: unclassified
    return 'unclassified'


def compute_gnome_coverage(items: list) -> dict:
    """Compute coverage statistics for a batch of Discourse topics."""
    total = len(items)
    if total == 0:
        return {
            'total': 0, 'classified': 0, 'unclassified': 0,
            'coverage': 0.0, 'need_related': 0, 'random': 0,
            'by_pattern': Counter(),
        }

    need_related = 0
    random_count = 0
    unclassified = 0
    by_pattern = Counter()

    for item in items:
        if 'combined_text' in item:
            text = item['combined_text'].lower()
        elif 'title' in item and 'body' in item:
            text = f"{item['title']} {item['body']}".lower()
        else:
            text = str(item.get('', '')).lower()

        # Check excluded patterns first
        matched_excluded = False
        for pat, pattern_str in DISCOURSE_EXCLUDED_COMPILED:
            if pat.search(text):
                random_count += 1
                by_pattern[f"EXCLUDED:{pattern_str}"] += 1
                matched_excluded = True
                break

        if matched_excluded:
            continue

        # Check need-related patterns
        matched_need = False
        for pat, pattern_str in DISCOURSE_NEED_COMPILED:
            if pat.search(text):
                need_related += 1
                matched_need = True
                by_pattern[f"NEED:{pattern_str}"] += 1
                break

        if not matched_need:
            unclassified += 1

    classified = need_related + random_count
    coverage = classified / total if total > 0 else 0.0

    return {
        'total': total,
        'classified': classified,
        'unclassified': unclassified,
        'coverage': coverage,
        'need_related': need_related,
        'random': random_count,
        'by_pattern': by_pattern,
    }


if __name__ == "__main__":
    # Quick test on meta.discourse.org blog posts that were misclassified
    test_cases = [
        # Blog posts that SHOULD be excluded (from E123)
        ("How Jennifer Aniston and Friends Cost Us 377GB and Broke ext4 Hardlinks", "random"),
        ("Getting Started with Discourse - Part 1: Discourse Setup | Blog", "random"),
        ("The Six Types of Online Communities (with Examples of Each) | Blog", "random"),
        ("Why Your Community Didn't Take Off (and How to Fix it)", "random"),
        ("Five Ways Support Communities Improve Customer Experience | Blog", "random"),
        ("How Let's Encrypt Uses Community to Provide Free Support", "random"),
        ("How Elastic Bolsters Community Support with Discourse Automation", "random"),
        ("How Katalon Increased Community engagement with Discourse hosting", "random"),
        
        # Genuine questions that SHOULD be need-related
        ("How to configure SSO with SAML?", "need-related"),
        ("Why does my GTK app crash on startup?", "need-related"),
        ("Cannot install Flatpak - permission denied", "need-related"),
        ("Help: GTK4 migration issue with deprecated API", "need-related"),
        ("Getting started with GTK4 development", "need-related"),  # This IS a question
        ("How do I create a custom widget in libadwaita?", "need-related"),
        ("Bug: Flatpak builder fails with new SDK", "need-related"),
    ]
    
    print("=== Test Classification (E124 improved classifier) ===")
    correct = 0
    for tc, expected in test_cases:
        result = classify_gnome_item(tc)
        status = "✓" if result == expected else "✗"
        if result == expected:
            correct += 1
        print(f"  [{result:12s}] {tc[:70]} (expected: {expected}) {status}")
    
    print(f"\nAccuracy: {correct}/{len(test_cases)} = {correct/len(test_cases)*100:.1f}%")
    
    print(f"\n=== Pattern counts ===")
    print(f"Need patterns: {len(DISCOURSE_NEED_PATTERNS)}")
    print(f"Excluded patterns: {len(DISCOURSE_EXCLUDED_PATTERNS)}")
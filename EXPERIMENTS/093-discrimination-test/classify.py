<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->
#!/usr/bin/env python3
"""
E093 — Classification instruments for discrimination testing.
"""

import re

# Keyword lists
SOLUTION_KEYWORDS = [
    'how to', 'tutorial', 'guide', 'solution', 'fix', 'repair',
    'tool', 'software', 'app', 'download', 'install',
    'step by step', 'method', 'procedure', 'resolution',
    'fix for', 'fixes', 'troubleshooting',
]

INFO_KEYWORDS = [
    'definition', 'what is', 'overview', 'introduction',
    'summary', 'characteristics', 'fault code',
    'meaning', 'indicates', 'refers to',
]

STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'i', 'me',
    'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'do', 'does', 'did', 'doing', 'a', 'an'
}


def classify_hand(r):
    """Hand rubric: served if solution keyword or tool title, partially_served if info, else unserved."""
    all_text = ' '.join(r['titles'] + r['snippets']).lower()
    has_solution = any(kw in all_text for kw in SOLUTION_KEYWORDS)
    has_info = any(kw in all_text for kw in INFO_KEYWORDS)
    titles = r['titles']
    has_tool_title = any(
        t and any(kw in t.lower() for kw in ['tool', 'software', 'app', 'guide', 'tutorial', 'manual'])
        for t in titles
    )
    if has_solution or has_tool_title:
        return 'served'
    elif has_info:
        return 'partially_served'
    else:
        return 'unserved'


def _extract_subject_terms(query: str) -> list:
    """Extract subject terms from query (stopword-filtered)."""
    terms = re.findall(r'[a-z0-9]+', query.lower())
    return [t for t in terms if t not in STOPWORDS and not t.isdigit()]


def classify_v1(r):
    """V1: subject mention + guide structure."""
    all_text = ' '.join(r['titles'] + r['snippets']).lower()
    subject_terms = _extract_subject_terms(r['query'])
    
    if not subject_terms:
        return classify_hand(r)
    
    blob = all_text
    subject_mentioned = any(term in blob for term in subject_terms)
    has_solution = any(kw in all_text for kw in SOLUTION_KEYWORDS)
    has_info = any(kw in all_text for kw in INFO_KEYWORDS)
    
    if subject_mentioned and has_solution:
        return 'served'
    elif subject_mentioned and has_info and not has_solution:
        return 'partially_served'
    elif has_solution and not subject_mentioned:
        return 'unserved'
    elif has_info and not subject_mentioned:
        return 'partially_served'
    else:
        return 'unserved'


def classify_v2(r):
    """V2: stricter - subject mention + step-by-step/part info."""
    all_text = ' '.join(r['titles'] + r['snippets']).lower()
    subject_terms = _extract_subject_terms(r['query'])
    
    if not subject_terms:
        return classify_hand(r)
    
    blob = all_text
    subject_mentioned = any(term in blob for term in subject_terms)
    has_solution = any(kw in all_text for kw in SOLUTION_KEYWORDS)
    has_info = any(kw in all_text for kw in INFO_KEYWORDS)
    
    step_kws = ['step by step', 'first', 'second', 'then', 'finally',
                'click', 'press', 'select', 'navigate', 'run', 'execute']
    has_step_by_step = any(kw in all_text for kw in step_kws)
    
    part_kws = ['part number', 'pn ', 'p/n', 'component', 'module', 'assembly']
    has_part_info = any(kw in all_text for kw in part_kws)
    
    if subject_mentioned and has_solution and (has_step_by_step or has_part_info):
        return 'served'
    elif subject_mentioned and has_info and not has_solution:
        return 'partially_served'
    elif subject_mentioned and has_solution and not has_step_by_step and not has_part_info:
        return 'partially_served'
    elif not subject_mentioned and has_solution:
        return 'unserved'
    elif not subject_mentioned and has_info:
        return 'partially_served'
    else:
        return 'unserved'


def classify_original(r):
    """Original classifier from outcome.py."""
    return classify_hand(r)
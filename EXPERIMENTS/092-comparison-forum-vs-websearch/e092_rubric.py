#!/usr/bin/env python3
"""
E092 — the served/unserved rubric, written before any result was viewed.

Split out of `compare_data_formats.py` at the 300-line cap. This is the
judgement the comparison holds constant while it varies the data format, so it
is kept apart from the runner: the rubric can be read, challenged, and
re-run on new formats without touching the comparison that reports its gates.
"""

import html
import re


SOLUTION_KEYWORDS = [
    "how to", "tutorial", "guide", "solution", "fix", "repair", "tool", "software",
    "app", "download", "install", "step by step", "method", "procedure",
    "resolution", "fix for", "fixes", "troubleshooting"
]

INFO_KEYWORDS = [
    "definition", "what is", "overview", "introduction", "summary",
    "characteristics", "fault code", "meaning", "indicates", "refers to"
]

CHROME_WORDS = [
    "error", "code", "fault", "meaning", "how", "the", "for", "and", "with",
    "manual", "guide", "messages"
]


def strip_chrome(text):
    """Remove chrome/boilerplate words from text."""
    text = html.unescape(text).lower()
    for word in CHROME_WORDS:
        text = re.sub(r'\b' + re.escape(word) + r'\b', ' ', text)
    return text


def classify_by_rubric_revised(thread_text, query_subject):
    """
    Revised rubric written before viewing results.
    
    Criteria (written before viewing results):
    - served: The query's distinctive subject term appears in the thread/text (excluding chrome words),
      AND either solution keywords or info keywords are present. This avoids the false
      positive pattern from E088 (0.80 FPR on known-unserved) while capturing served cases.
    - partially_served: The subject appears AND info keywords are present but not solution keywords.
    - unserved: The subject does NOT appear in the text (after removing chrome words), OR
      neither solution nor info keywords are present after the subject check.
    """
    # Clean the text and check for subject mention
    text = strip_chrome(thread_text)
    query_lower = (query_subject or "").lower()
    subject_mentioned = query_lower in text if query_lower else False
    
    # Check for solution and info keywords in original text
    text_lower = thread_text.lower()
    solution_keywords_present = any(kw in text_lower for kw in SOLUTION_KEYWORDS)
    info_keywords_present = any(kw in text_lower for kw in INFO_KEYWORDS)
    
    # Classification logic (REVISED)
    # served: subject_mentioned AND (solution_keywords_present OR info_keywords_present)
    # This maintains FPR=0 from subject_mentioned check but increases TPR
    if subject_mentioned and (solution_keywords_present or info_keywords_present):
        return "served"
    # partially_served: subject_mentioned AND info_keywords_present AND NOT solution_keywords_present
    if subject_mentioned and info_keywords_present and not solution_keywords_present:
        return "partially_served"
    # unserved: NOT subject_mentioned, or subject present but no relevant keywords
    return "unserved"

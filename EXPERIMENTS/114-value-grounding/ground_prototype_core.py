#!/usr/bin/env python3
"""
ground-prototype.py — improved mechanical value grounding checker.

Extends ground.py (E114) to address its explicit limitations:
  (1) More rendering forms for CFR/U.S.C./FR citations
  (2) Context presence check: whether surrounding words in the answer
      also appear near the value in the document
  (3) Richer verdict types: grounded, ungrounded_value, ungrounded_claim,
      ungrounded_context

This is an exploratory prototype. It is NOT claimed as a finished product
or a new algorithm validated for publication. It gathers evidence about
whether mechanical checks can do better than the v1 baseline.
"""

import html
import os
import re
import sys
from collections import defaultdict

#
# STOP words for content-word extraction
#
STOP = set("""a an the of to in for and or by with at on from as is are be been was
were this that these those it its his her their our your my we they he she i you
not no also any all each other others such same more most less least than then
so if when while under over above below after before during between within
without into onto per may must shall can could would should will do does did
done have has had""".split())


#
# MONTH and abbreviation patterns
#
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_RE = "|".join(MONTHS)

ABBR = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April",
        "May": "May", "Jun": "June", "Jul": "July", "Aug": "August",
        "Sep": "September", "Sept": "September", "Oct": "October",
        "Nov": "November", "Dec": "December"}
ABBR_RE = "|".join(sorted(ABBR, key=len, reverse=True))


#
# VALUE EXTRACTION PATTERNS
# Extended from ground.py v1 to cover more rendering forms
#
PATTERNS = [
    ("date", re.compile(
        r"(?:%s)\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}" % MONTH_RE +
        r"|\d{1,2}\s+(?:%s)\.?\s+\d{4}" % MONTH_RE +
        r"|(?:%s)\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}" % ABBR_RE +
        r"|\d{1,2}/\d{1,2}/\d{2,4}")),
    ("money", re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand))?",
                         re.I)),
    ("pct", re.compile(r"\d[\d,]*(?:\.\d+)?\s?(?:percent|%)", re.I)),
    ("code", re.compile(
        r"\d+\s+CFR\s+(?:part\s+)?[\d.]+(?:\s*(?:through|-|to)\s*[\d.]+)?"
        r"(?:\([A-Za-z0-9()]*\))*"
        r"|\d+\s+U\.?S\.?C\.?\s*(?:et seq\.|\s*\d+[A-Za-z0-9()]*|§\s*\d+)"
        r"|\d+\s*FR\s+\d+"
        r"|Docket\s+No\.?\s*[\w.()\-]+"
        r"|RIN\s+\d{4}-[A-Z]{2}\d{2}"
        r"|\b\d{2,4}-\d{3,4}\b(?=[A-Z])")
     ),
    ("qty", re.compile(
        r"\d[\d,]*(?:\.\d+)?\s?(?:lb|lbs|pound|pounds|kg|kilogram|kilograms|"
        r"mt|metric ton|metric tons|ton|tons|nautical mile|nautical miles|"
        r"\bnm\b|foot|feet|\bm\b|degree|degrees|hour|hours|day|days|year|years)",
        re.I)),
    ("num", re.compile(r"\b\d[\d,]*(?:\.\d+)?\b")),
]


#
# BOUNDARIES for extracting the enclosing sentence/row
#
BOUND = re.compile(r"[.;](?=\s)|—")


#
# UTILITIES
#

def normalize(raw):
    """Readable text: tags gone, entities decoded, hard line wraps joined."""
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt).replace(" ", " ")
    txt = re.sub(r"\s*\n\s*", " ", txt)
    return re.sub(r"[ \t]+", " ", txt).strip()


def unit(text, start, end, cap=420):
    """The enclosing sentence-or-table-row of text[start:end].
    Split on .;/ followed by whitespace but never inside a number or citation.
    """
    left = 0
    for m in BOUND.finditer(text, max(0, start - cap), start):
        left = m.end()
    right = len(text)
    for m in BOUND.finditer(text, end, min(len(text), end + cap)):
        right = m.start() + 1
        break
    return text[left:right]


SUFFIX = ("ings", "ing", "edly", "ed", "es", "s", "ly", "ment", "tion", "ions")


def stem(w):
    for suf in SUFFIX:
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[:-len(suf)]
    return w


def content_words(text):
    """Stemmed non-stop words in text."""
    return set(stem(w) for w in re.findall(r"[a-z][a-z'\-]{2,}", text.lower())
               if w not in STOP)


def date_renderings(value):
    """Every rendering a document might legitimately use for this date."""
    v = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", value, flags=re.I)
    v = v.replace(".", "")
    out = {v.lower().replace(",", ""), v.lower()}
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})$", v)
    if m:
        mon, day, yr = m.group(1), m.group(2), m.group(3)
        mon = ABBR.get(mon[:3].capitalize(), mon)
        out |= {"%s %s, %s" % (mon, day, yr), "%s %s %s" % (mon, day, yr),
                "%s %d, %s" % (mon, int(day), yr)}
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})$", v)
    if m:
        day, mon, yr = m.group(1), m.group(2), m.group(3)
        mon = ABBR.get(mon[:3].capitalize(), mon)
        out |= {"%s %s, %s" % (mon, day, yr), "%s %s %s" % (mon, day, yr)}
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})$", v)
    if m:
        a, b, yr = m.group(1), m.group(2), m.group(3)
        out |= {"%s/%s/%s" % (a, b, yr), "%s/%s/%s" % (b, a, yr)}
    return {o for o in out if o}


def renderings(value, kind):
    """The strings under which this value may legitimately occur."""
    v = value.strip()
    if kind == "date":
        return date_renderings(v)
    v = re.sub(r"^\$\s*", "", v)
    v = re.sub(r"\s+(?:million|billion|thousand)$", "", v, flags=re.I)
    cands = {v.lower()}                       # the comma form, as the document writes it
    bare = v.replace(",", "")
    cands.add(bare.lower())
    if "." in bare:
        cands.add(bare.rstrip("0").rstrip(".").lower())
    if kind == "money" and "." not in bare:
        cands.add(bare + ".00")
    return {c for c in cands if c}


#
# CORE LOGIC
#

def extract(answer):
    """Every value claim in the answer, longest match wins, no nested double-count."""
    spans = []
    for kind, pat in PATTERNS:
        for m in pat.finditer(answer):
            spans.append((m.start(), m.end(), kind, m.group(0)))
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    kept = []
    for s, e, kind, raw in spans:
        if any(k[0] <= s and e <= k[1] for k in kept):
            continue
        kept.append((s, e, kind, raw))
    return [(k, r) for _, _, k, r in kept]


def renderings_in_doc(doc_low, cand, kind, window=90):
    """Check if any rendering of cand occurs in doc_low within window.
    Returns (found:bool, matched:set of renderings actually found)."""
    found = set()
    for cand_ver in renderings(cand, kind):
        start = 0
        while True:
            i = doc_low.find(cand_ver, start)
            if i < 0:
                break
            found.add(cand_ver)
            start = i + 1
    return bool(found), found


def judge(doc, answer, threshold=0.6, window=90):
    """Judge each value claim against the document.
    
    Verdits:
      grounded          - value occurs in doc with matching context
      ungrounded_value  - value truly absent from doc
      ungrounded_claim  - value occurs in doc but not beside answer's words
      ungrounded_context - value occurs in doc but surrounding context differs
    """
    dlow = doc.lower()
    out = []
    for kind, raw in extract(answer):
        at = answer.find(raw)
        # Two granularities, applied symmetrically to both sides, best-of wins.
        ctxs = [content_words(unit(answer, at, at + len(raw))),
                content_words(answer[max(0, at - window):at + len(raw) + window])]
        ctxs = [c for c in ctxs if c]
        if not ctxs:
            continue
        best = 0.0
        found_in_doc = False
        # Check if any rendering of this value occurs in the document
        found_in_doc, matched = renderings_in_doc(dlow, raw, kind, window)
        
        if found_in_doc:
            # Value IS in document - check context match
            ctx_match_score = 0.0
            for cand_ver in matched:
                # Find all occurrences of this rendering in doc
                doc_start = 0
                while True:
                    i = dlow.find(cand_ver, doc_start)
                    if i < 0:
                        break
                    # Check context words from doc around this occurrence
                    doc_ctx = content_words(dlow[max(0, i - window):i + len(cand_ver) + window])
                    if doc_ctx:
                        for ctx in ctxs:
                            if ctx:
                                ctx_match_score = max(ctx_match_score, len(ctx & doc_ctx) / float(len(ctx)))
                    doc_start = i + 1
            best = max(best, ctx_match_score)
        else:
            # Value not found in doc at all
            best = 0.0
        
        # Determine verdict
        if not found_in_doc:
            # Value truly ungrounded - not in document
            out.append({"kind": kind, "value": raw,
                        "verdict": "ungrounded_value", "score": 0.0})
        elif best >= threshold:
            # Value found in doc AND context matches well
            out.append({"kind": kind, "value": raw,
                        "verdict": "grounded", "score": round(best, 3)})
        elif best > 0:
            # Value found in doc but context does NOT match well
            out.append({"kind": kind, "value": raw,
                        "verdict": "ungrounded_context", "score": round(best, 3)})
        else:
            # This shouldn't happen if found_in_doc is True but best is 0
            out.append({"kind": kind, "value": raw,
                        "verdict": "ungrounded_claim", "score": round(best, 3)})
    return out


#
# DOCUMENT LOADING
#

def load_doc(num, rawdir):
    with open(os.path.join(rawdir, "text", num + ".txt"), "rb") as fh:
        return normalize(fh.read().decode("utf-8", "replace"))

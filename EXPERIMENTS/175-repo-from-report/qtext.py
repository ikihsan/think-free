#!/usr/bin/env python3
"""E175: the query text, extracted from the report only.

E169 recorded a defect worth not repeating: its automated literal extractor
selected prose, which weakened the incumbent it was meant to represent. So a
candidate here must survive a filter that rejects sentences: a literal is a
**quoted span, a code line, or a line that opens with an error keyword**, 12-120
characters, at most eight words, no URL, no first-person pronoun.
"""
import re

from derive import _STOP

_QUOTED = re.compile(r'"([^"\n]{8,160})"')
_TICKED = re.compile(r"'([^'\n]{8,160})'")
_FENCE = re.compile(r"```[a-zA-Z0-9_+-]*\n(.{8,160}?)\n", re.S)
_ERRLINE = re.compile(
    r"^\s*(?:[A-Za-z_][\w.]*(?:Error|Exception|Warning|Failure|Fault)\b"
    r"|(?:error|fatal|panic|segfault|assertion)\b)[^\n]{0,160}", re.M | re.I)
_FIRSTPERSON = re.compile(r"\b(I|I'm|I've|my|we|our)\b")
_URLISH = re.compile(r"https?://|www\.")


def _ok(cand):
    if not cand:
        return False
    c = " ".join(cand.split())
    if not (12 <= len(c) <= 120):
        return False
    if len(c.split()) > 8:
        return False
    if _URLISH.search(c) or _FIRSTPERSON.search(c):
        return False
    return True


def literal(row):
    """The asker's own error string, or '' when the post has none (E170's
    `literal_type: symptom_only` rows)."""
    body = row.get("body") or ""
    for rx in (_QUOTED, _FENCE, _ERRLINE, _TICKED):
        for m in rx.finditer(body):
            cand = m.group(1).strip("`")
            if _ok(cand):
                return " ".join(cand.split())
    return ""


def keywords(row, extra=""):
    """Component + symptom words: title content words, then the derived
    artifact's name. Deterministic, no model."""
    toks = [t.strip(".,;:()[]<>`\"'").lower() for t in
            re.split(r"\s+", row.get("title") or "")]
    toks = [t for t in toks
            if len(t) >= 3 and t not in _STOP and re.search(r"[A-Za-z0-9]", t)]
    out = []
    for t in toks + [extra]:
        if t and t not in out and t not in _STOP:
            out.append(t)
        if len(out) >= 6:
            break
    return " ".join(out)
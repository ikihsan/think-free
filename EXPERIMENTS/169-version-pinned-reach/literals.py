"""Error-literal extraction from a Stack Exchange question body.

Written before any of the 61 unfetched bodies were read, and not retuned
after the run: E169's G1 is the falsification of this module, and a retuned
extractor reporting its own agreement is not a falsification.
"""
import html
import re

_BLOCK = re.compile(r"(?is)<(script|style)\b.*?</\1>")
_BR = re.compile(r"(?i)<br\s*/?>")
_P = re.compile(r"(?i)</(p|div|li|h[1-6]|pre|blockquote|tr)>")
_TAG = re.compile(r"(?s)<[^>]+>")
_ERRWORD = re.compile(r"(?i)\b(error|errors|exception|fail(?:ed|ure|s)?|"
                      r"cannot|can't|unexpected|invalid)\b")
# A span the asker delimited: quoted, or in a code span, or after a colon.
_DELIM = re.compile(r"[\"'\u201c\u201d`]([^\"'\u201c\u201d`]{15,200})[\"'\u201c\u201d`]")
_COLON = re.compile(r"(?m)^\s{0,6}(?:[A-Za-z][\w .\-]{0,40})?:\s*(\S.{14,200})$")
_HAS_DIGIT = re.compile(r"\d")
_HAS_CAPS = re.compile(r"\b[A-Z][A-Z0-9_]{3,}\b")


def to_text(raw):
    """HTML body -> plain text with block structure preserved as newlines."""
    if not raw:
        return ""
    s = _BLOCK.sub(" ", raw)
    s = _BR.sub("\n", s)
    s = _P.sub("\n", s)
    s = _TAG.sub(" ", s)
    s = html.unescape(s)
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s).strip()


def candidates(text):
    """Every span that could be pasted into a search engine verbatim."""
    out = []
    for m in _DELIM.finditer(text):
        out.append(_clean(m.group(1)))
    for m in _COLON.finditer(text):
        out.append(_clean(m.group(1)))
    for line in text.split("\n"):
        line = line.strip()
        if len(line) >= 15 and _ERRWORD.search(line):
            out.append(_clean(line))
    seen, uniq = set(), []
    for c in out:
        if c and c.lower() not in seen:
            seen.add(c.lower())
            uniq.append(c)
    return uniq


def _clean(span):
    s = span.strip().strip("*_`# ").strip()
    s = re.sub(r"\s+", " ", s)
    return s[:200]


def primary(text):
    """The literal a developer would paste: longest, tie-broken on specificity.

    Longest wins because GitHub's phrase search needs the distinctive part,
    and the tie-break keeps a code-shaped literal over an English sentence
    that happens to contain the word "error".
    """
    cands = candidates(text)
    if not cands:
        return ""
    def score(c):
        return (len(c),
                1 if _HAS_DIGIT.search(c) else 0,
                1 if _HAS_CAPS.search(c) else 0,
                -c.count(" "))
    return max(cands, key=score)


def weak_literal(text):
    """The longest quoted/error span even when short -- for the reader's check.

    E168's G3 rows include cases where the asker names the symptom in prose
    only. `primary` returns "" for those, which is the row-level label this
    experiment measures in G3; `weak_literal` reports whether the row held any
    technical span at all, so a hand reader can tell "no literal" apart from
    "literal my rules missed".
    """
    relaxed = []
    for m in re.finditer(r"[\"'\u201c\u201d`]([^\"'\u201c\u201d`]{8,200})[\"'\u201c\u201d`]", text):
        relaxed.append(_clean(m.group(1)))
    for line in text.split("\n"):
        line = line.strip()
        if len(line) >= 8 and _ERRWORD.search(line):
            relaxed.append(_clean(line))
    return max(relaxed, key=len) if relaxed else ""
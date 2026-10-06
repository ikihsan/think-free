#!/usr/bin/env python3
"""Shared constants for E031. Fixed by PROTOCOL.md; nothing here is tuned on data.

Stdlib only; Python 3.8 compatible (this VM's interpreter). No network access:
E031 reads E030's captures, which are already on disk.
"""

import hashlib
import html
import json
import math
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E030_RAW = os.path.join(os.path.dirname(HERE), "030-departure-recurrence", "raw")

SEED_SAMPLE = 3101
SEED_SHUFFLE = 3102
N_PER_ARM = 72
N_NONSENSE = 24
N_REREAD = 40
N_PERMUTATIONS = 200

# Strata declared in PROTOCOL.md, by E030's framing phrase.
SEEK_FRAMINGS = [
    "alternative to",
    "alternatives to",
    "looking for a replacement",
    "what are you using instead of",
]
MOVE_FRAMINGS = [
    "switched from",
    "migrating from",
    "moved off",
]

# The one question block, byte-identical in every view. RUBRIC.md.
QUESTION_BLOCK = [
    "q1: Does this comment state a capability that something the author relies",
    "    on cannot do? Answer 1 (yes), 0 (no), or u (unclear).",
    "q2: Only if q1 is 1. Copy the SHORTEST phrase INSIDE this comment that",
    "    states the missing capability, verbatim, original casing and",
    "    punctuation. Do not paraphrase. If q1 is 0 or u, write -.",
    "q3: Does this comment name the thing the author moved to? 1, 0, or u.",
]

Q4_BLOCK = [
    "Do these two clauses state THE SAME missing capability?",
    "Answer one of: same / different / unclear.",
]

_PUNCT = re.compile(r"[^\w\s]")
_HTML = re.compile(r"<[^>]+>")

# Stoplist for clause normalisation only. Fixed here, not derived from data.
STOPWORDS = set("""
a an the this that these those there here it its it's their his her our your my
is are was were be been being am do does did doing done have has had having
can could will would shall should may might must need needs needed want wants
wanted like likes liked use uses used using get gets got make makes made makes
much many more most less least very too also just still now then than when
where which who whom what why how all any both each few other others some such
no nor not only own same so too under until up very via with without within
one two three new old good better best bad worse worst first last next back
after before because although though while about against between during over
per out off again further once here there what why how if
""".split())

# Words that must never count as arm-identifying leakage in a view.
ARM_WORDS = ("A1", "A2", "A3", "seek", "move", "ordinary", "treatment", "control",
             "arm", "stratum", "cohort")


def clean(text):
    return _HTML.sub(" ", html.unescape(text or ""))


def wilson_ci(k, n, z=1.959963985):
    """Wilson score interval. (0.0, 0.0) when n == 0."""
    if n == 0:
        return (0.0, 0.0)
    p = k / float(n)
    d = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z / d) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centre - half), min(1.0, centre + half)


def diff_ci(k1, n1, k2, n2):
    """Newcombe CI95 for p1 - p2."""
    l1, u1 = wilson_ci(k1, n1)
    l2, u2 = wilson_ci(k2, n2)
    p1 = k1 / float(n1) if n1 else 0.0
    p2 = k2 / float(n2) if n2 else 0.0
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, max(-1.0, lo), min(1.0, hi)


def cohen_kappa(pairs):
    """Cohen's kappa over (label_a, label_b) pairs of equal length. Any label set."""
    if not pairs:
        return None, 0
    n = len(pairs)
    labels = set()
    for a, b in pairs:
        labels.add(a)
        labels.add(b)
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / float(n)
    pe = 0.0
    for lab in labels:
        ca = sum(1 for a, b in pairs if a == lab) / float(n)
        cb = sum(1 for a, b in pairs if b == lab) / float(n)
        pe += ca * cb
    if pe >= 1.0:
        return (1.0 if po == 1.0 else 0.0), n
    return (po - pe) / (1.0 - pe), n


def read_jsonl(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    return path


def sha256_bytes(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def sha256_file(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def normalise_clause(text):
    """Lowercase, strip punctuation, drop stopwords and short tokens -> set."""
    low = clean(text).lower()
    toks = [t for t in _PUNCT.sub(" ", low).split() if t]
    return set(t for t in toks if len(t) >= 4 and t not in STOPWORDS)


def clause_len(text):
    return len([t for t in _PUNCT.sub(" ", clean(text).lower()).split() if t])


# Typographic variants a copy tool may normalise silently. Only these six, and
# only on the q2 side: HN comment bodies carry curly quotes and dashes, and a
# reader copying by keyboard produces straight ones. Anything else must match.
_TYPO = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-",
}


def fold_typo(text):
    """Typographic fold plus whitespace-run collapse. See is_verbatim."""
    for a, b in _TYPO.items():
        text = text.replace(a, b)
    return re.sub(r"[ \t\r\n]+", " ", text).strip()


def is_verbatim(phrase, source):
    """True when `phrase` occurs inside `source` up to the declared fold.

    The fold (PROTOCOL-AMENDMENT-2.md) maps the four curly quotes and the en and
    em dashes to their ASCII equivalents, and collapses runs of horizontal
    whitespace to a single space, on both sides. Nothing else is folded: not
    case, not punctuation, not spelling, not word order.

    Neither fold can create or destroy a clause. It cannot introduce a word that
    is not in the source, remove one, or reorder any — it can only change which
    of two spellings of the same characters matches, and how many spaces stand
    between words. A reader who paraphrased therefore still fails this test.
    """
    return fold_typo(phrase) in fold_typo(clean(source))


def log(event, **kw):
    kw["event"] = event
    print(json.dumps(kw, sort_keys=True))
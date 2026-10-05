#!/usr/bin/env python3
"""Shared constants and helpers for E030.

Everything here is fixed by
[`PROTOCOL.md`](PROTOCOL.md) and must not be tuned on the data.
Stdlib only; Python 3.8 compatible (this VM's interpreter).
"""

import html
import json
import math
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

ALGOLIA = "https://hn.algolia.com/api/v1/search"

# The seven framing phrases fixed in the protocol's corpus table and selected in
# PROTOCOL-AMENDMENT-2.md. The two vague English phrases ("replaced", "instead
# of") and "insteadof" are deliberately absent. Queries are PHRASE-EXACT: the
# quotes go on the wire, which is what the protocol's volume table measured.
FRAMINGS = [
    "what are you using instead of",
    "looking for a replacement",
    "moved off",
    "migrating from",
    "switched from",
    "alternatives to",
    "alternative to",
]


def phrase(query):
    """Quote a query for Algolia's phrase-exact match (AMENDMENT-2)."""
    return '"%s"' % query

# Probe instruments the whole harvest is checked against (gate A2/A3).
POSITIVE_PROBES = [
    "we migrated from Jenkins to",
    "switched from Sentry to",
    "moved off from Heroku",
    "alternatives to Firebase",
    "what are you using instead of Salesforce",
    "looking for a replacement for Jira",
]
NONSENSE_PROBES = [
    "we migrated from zzqxvpn to",
    "switched from zzqxvpn to",
    "moved off from zzqxvpn",
    "alternatives to zzqxvpn",
    "what are you using instead of zzqxvpn",
    "looking for a replacement for zzqxvpn",
]

SINCE = 1704067200  # 2024-01-01T00:00:00Z, declared in the protocol
MIN_WORDS = 40

_PUNCT = re.compile(r"[^\w\s]")
_HTML = re.compile(r"<[^>]+>")


def clean(text):
    """Unescape entities, then strip tags (order fixed by AMENDMENT-2)."""
    return _HTML.sub(" ", html.unescape(text or ""))


def words(text):
    return [w for w in re.split(r"\s+", _PUNCT.sub(" ", clean(text).lower())) if len(w) >= 4]


def wilson(k, n, z=1.959963985):
    """Wilson score interval. Returns (lo, hi) or (0.0, 0.0) when n == 0."""
    if n == 0:
        return 0.0, 0.0
    p = k / float(n)
    d = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z / d) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centre - half), min(1.0, centre + half)


def diff_ci(k1, n1, k2, n2):
    """Newcombe CI95 for p1 - p2, from two Wilson intervals."""
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    p1 = k1 / float(n1) if n1 else 0.0
    p2 = k2 / float(n2) if n2 else 0.0
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return d, max(-1.0, lo), min(1.0, hi)


def fetch(url, tries=4, sleep=1.5):
    """GET with retries. Returns (status, body_text)."""
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "e030-research"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.getcode(), r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - recorded, never swallowed
            last = exc
            time.sleep(sleep * (attempt + 1))
    return None, "error: %s" % (last,)


def algolia_pages(query, tags, page, hits_per_page=100, since=SINCE):
    """One Algolia page. Returns (status, decoded_or_None, raw_text)."""
    params = {
        "query": query,
        "tags": tags,
        "hitsPerPage": str(hits_per_page),
        "page": str(page),
        "numericFilters": "created_at_i>%d" % since,
        "advancedSyntax": "true",
    }
    url = ALGOLIA + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    status, body = fetch(url)
    if status != 200:
        return status, None, body
    try:
        return status, json.loads(body), body
    except ValueError as exc:
        return status, None, "decode error: %s" % exc


def read_jsonl(name):
    path = os.path.join(RAW, name)
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(name, rows):
    path = os.path.join(RAW, name)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    return path


def log(event, **kw):
    kw["event"] = event
    print(json.dumps(kw, sort_keys=True))

#!/usr/bin/env python3
"""Finding a capture by the query that produced it.

Split from `tally.py` at the 300-line cap, by invariant. Three questions are one
question -- *which capture answers this path pattern?* -- and each has already
been answered wrongly here:

* `^\.claude/hooks/` is a **substring** of `^\.claude/hooks/README\.md$`, so a
  substring match gave the broad pattern the narrow one's count of 42. Matching is
  on the recovered term, by equality, after canonicalising the escaping, which
  differs between the file that asks and the file that fetches.
* the capture's filename **cannot** answer this. The slug is lossy, so 9 captures
  fetched before the `# query:` header existed can only be recovered by slug, and
  are marked `attributed_by: slug` rather than treated as attributed.
* the ceiling parameter differs between fetches, so the same pattern may have
  several captures. The **largest** count is the better floor.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from captureformat import read_raw  # noqa: E402


def term_of(query):
    """Recover the `file:` term from a query string, exactly.

    `select:repo` and `count:` are stripped and the leading `context:global` with
    them, so an overlapping pattern can never be confused with a longer one
    containing it.
    """
    body = query.split(" file:", 1)
    if len(body) != 2:
        return None
    tail = body[1]
    for suffix in (" select:", " count:"):
        if suffix in tail:
            tail = tail.split(suffix, 1)[0]
    return tail


def canon(pattern):
    """A path pattern reduced to what it actually constrains.

    Every pattern here is written escaped in one file and unescaped in another --
    `^\\.claude/hooks/` and `^.claude/hooks/` are the same query, and the first
    version of this lookup compared them as strings and reported five measured
    controls as `missing`. A backslash before a character that needs no escaping
    is dropped, anchors are kept, and the rest compares case-sensitively because a
    path is.
    """
    out = pattern.replace("\\", "")
    if not out.startswith("^"):
        out = "^" + out
    return out


def slug_for(pattern, name=None):
    """The filename the capture for this pattern is written under.

    Delegates to the format module's naming function. Restating the rule here is
    what produced two successive rounds of `no_origin` on every configuration:
    first because the rule was re-implemented differently, then because the query
    header changed the file's shape underneath a second copy of it.
    """
    from captureformat import capture_name

    return capture_name("context:global file:%s select:repo count:4000" % pattern, name)


def raw_by_query():
    """Every capture on disk, keyed by the query it answers."""
    out = {}
    raw = os.path.join(HERE, "raw")
    for entry in sorted(os.listdir(raw)):
        if not entry.endswith(".sse"):
            continue
        rec = read_raw(os.path.join(raw, entry))
        if rec.get("query"):
            out[rec["query"]] = rec
    return out


def headerless_captures():
    """Captures fetched before the query header existed, keyed by their slug.

    These cannot be attributed by reading the file: the query was never written
    into it. They are recovered through the slug, which IS lossy, and the loss is
    declared rather than absorbed -- the slug cannot distinguish
    `^\.claude/hooks/README\.md$` from `^\.claude/hooks/`, which is the exact
    confusion that produced defect 1 in this file. So a slug-matched capture is
    only used when the pattern sought is the ONLY one its slug could stand for,
    and the result carries `attributed_by: slug`.
    """
    raw = os.path.join(HERE, "raw")
    out = {}
    for entry in sorted(os.listdir(raw)):
        if not entry.endswith(".sse"):
            continue
        rec = read_raw(os.path.join(raw, entry))
        if rec.get("query"):
            continue
        rec["attributed_by"] = "slug"
        out[rec["name"]] = rec
    return out


def best_capture(captures, pattern):
    """The largest count any capture of this path pattern recorded.

    Keyed on the `file:` term rather than the whole query, because the ceiling
    parameter differs between fetches -- a pattern first asked at count:4000 and
    later at count:20000 has two captures, and the larger is the better floor.
    """
    best = None
    wanted = canon(pattern)
    for query, rec in captures.items():
        term = term_of(query)
        if term is None or canon(term) != wanted:
            continue
        if rec["state"] not in ("ok", "saturated"):
            continue
        if best is None or rec["count"] > best["count"]:
            best = rec
    if best is not None:
        return best
    # Fall back to the pre-header captures, by slug.
    rec = headerless_captures().get(slug_for(pattern))
    return rec

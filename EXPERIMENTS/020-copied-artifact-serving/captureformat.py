#!/usr/bin/env python3
"""The on-disk capture format: how a raw stream is named, read and re-derived.

Split from `copycount.py` at the 300-line cap, by invariant: this module decides
what a capture on disk MEANS, and the fetcher decides how to obtain one. They
were one file, and the reader who wanted to know whether a figure could be
trusted had to read past the curl invocation to find the rule.

A capture is the ground truth; `copycount.json` is an index over it. Three
properties are load-bearing and each was a defect before it was a rule:

* the file records its own query in a `# query:` first line, because the slug
  cannot distinguish `^\\.claude/hooks/README\\.md$` from `^\\.claude/hooks/`;
* a capture holding an answer is never overwritten, and a refusal is written
  beside it rather than over it;
* `--rebuild` re-derives the index from these bytes, so a lost index is a command
  rather than a re-fetch.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Saturation ceiling observed on the calibration anchors. Above this the
# repositoriesCount is a floor set by our own count: parameter, not by the world.
CEILING = 4000

# The capture's filename: a lossy slug of the query. It is NOT an identity --
# `^\\.claude/hooks/README\\.md$` and `^\\.claude/hooks/` reduce to the same shape --
# which is why every capture also records its query in a first line.


def _slug(query):
    import re

    return re.sub(r"[^A-Za-z0-9]+", "-", query).strip("-").lower()[:80]

def capture_name(query, name=None):
    """The filename a query's raw capture is written under.

    One definition, callable by the consumer. The slug was previously recomputed
    independently by forkstatus.py and the two versions disagreed once the query
    header was added to the file, which turned all twenty-two configurations into
    `no_origin`. Anything that needs to find a capture must call this.
    """
    return name or _slug(query)


# Observed on 2026-10-05: the public stream sits behind a Cloudflare challenge that
# arms after roughly 30 requests from one host and then answers every query with
# an HTTP 200 HTML challenge page. That is F036's shape exactly -- a well-formed
# response carrying nothing about the query.
CHALLENGE_MARKERS = ("__cf_chl", "cf_chl_opt", "Vercel Security Checkpoint", "Just a moment")


def detect_challenge(text):
    """Name the challenge marker if this response is one, else None.

    Kept beside the reader rather than beside the fetcher, because the reader is
    what must recognise a challenge page already on disk: a refusal written by an
    earlier run is re-read here long after the process that wrote it is gone.
    """
    for marker in CHALLENGE_MARKERS:
        if marker in text:
            return marker
    return None


INSTRUMENT_NOTES = {
    "is_a_floor": "Sourcegraph indexes a subset of GitHub. Every count is 'at least N'.",
    "default_exclusions": "forks and archived repositories are excluded unless fork:yes archived:yes",
    "unit": "the file: pattern is a path glob, so a repository counts once however "
            "many of its files match",
    "auth": "no token is sent; the public stream is the whole instrument",
}


def read_raw(path):
    """Parse one raw stream back into a record.

    The raw captures are the ground truth; copycount.json is an index over them.
    Rebuilding from raw is what makes that true rather than merely intended -- the
    clobbering defect above lost ten counts from the index while every raw file
    was still on disk, and this function is how they came back.

    The query is read from a `# query:` first line rather than recovered from the
    filename: the slug is lossy (`^\.claude/hooks/README\.md$` and
    `^\.claude/hooks/` differ only in a suffix the slug drops to the same shape),
    so a rebuild keyed on the filename cannot tell two patterns apart. Streams
    written before this header are read without one and are reported as such.
    """
    name = os.path.basename(path)[:-4]
    with open(path) as handle:
        text = handle.read()
    record = {"name": name, "raw": os.path.relpath(path, HERE), "query": "",
              "query_present": False}

    if text.startswith("# query:"):
        record["query"] = text.split("\n", 1)[0][len("# query:"):].strip()
        record["query_present"] = True
        text = text.split("\n", 1)[1] if "\n" in text else ""
    else:
        record["no_query_header"] = True

    challenge = detect_challenge(text)
    if challenge is not None:
        record.update({"state": "refused", "count": None,
                       "reason": "anti-bot challenge (%s), not an answer" % challenge})
        return record

    progress = None
    for line in text.splitlines():
        if not line.startswith("data: "):
            continue
        try:
            blob = json.loads(line[6:])
        except ValueError:
            continue
        if isinstance(blob, dict) and blob.get("done") is True:
            progress = blob
    if progress is None:
        record.update({"state": "refused", "count": None, "reason": "no terminal progress event"})
        return record

    record["repositoriesCount"] = progress.get("repositoriesCount")
    record["matchCount"] = progress.get("matchCount")
    record["skipped"] = progress.get("skipped", [])
    if progress.get("repositoriesCount") is None:
        if progress.get("matchCount") == 0:
            record.update({"state": "ok", "count": 0})
        else:
            record.update({"state": "refused", "count": None,
                           "reason": "matched files but named no repository"})
        return record
    record["count"] = progress["repositoriesCount"]
    limit_hit = any(i.get("reason") in ("shard-match-limit", "hit-limit")
                    for i in record["skipped"])
    if limit_hit or record["count"] >= CEILING:
        record["state"] = "saturated"
        record["reason"] = "at or above count:4000; a floor set by the query"
    else:
        record["state"] = "ok"
    return record


INSTRUMENT_NOTES = {
    "is_a_floor": "Sourcegraph indexes a subset of GitHub. Every count is 'at least N'.",
    "default_exclusions": "forks and archived repositories are excluded unless fork:yes archived:yes",
    "unit": "the file: pattern is a path glob, so a repository counts once however "
            "many of its files match",
    "auth": "no token is sent; the public stream is the whole instrument",
}


def rebuild_index():
    """Re-derive copycount.json from every raw stream on disk."""
    records = []
    for entry in sorted(os.listdir(RAW)):
        if not entry.endswith(".sse"):
            continue
        rec = read_raw(os.path.join(RAW, entry))
        records.append(rec)

    # The query lives in the capture's first line. Streams fetched before that
    # header existed cannot be attributed to a pattern, so they are reported as
    # unattributed rather than being matched by slug -- guessing here is what put
    # a broad pattern's count on a narrow one in the first place.
    attributed = [r for r in records if not r.get("no_query_header") and r["query"]]
    out = os.path.join(HERE, "copycount.json")
    with open(out, "w") as handle:
        json.dump({"instrument": INSTRUMENT_NOTES, "rebuilt_from": "raw/",
                   "attributed": len(attributed),
                   "unattributed": len(records) - len(attributed),
                   "records": records},
                  handle, indent=1, sort_keys=True)
        handle.write("\n")
    return records

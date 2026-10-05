#!/usr/bin/env python3
"""Fetch Sourcegraph repository-level counts for declared path patterns.

Every query writes its raw stream to raw/ before anything is parsed, so a figure
in results.json can be traced to bytes on disk.  Declared in
EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md; the instrument's three
ceilings are repeated in INSTRUMENT_NOTES because they are load-bearing.

Unauthenticated only.  A refused, truncated or errored answer is `refused` and is
never counted as a zero -- F032's defect class, which has already bitten this
repository twice.
"""

import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

STREAM_URL = "https://sourcegraph.com/.api/search/stream?q=%s&v=V3&t=literal"

# Observed on 2026-10-05: the public stream sits behind a Cloudflare challenge that
# arms after roughly 30 requests from one host and then answers every query with
# an HTTP 200 HTML challenge page. That is F036's shape exactly -- a well-formed
# response carrying nothing about the query -- and the fetcher's first job is to
# notice it. `detect_challenge` looks for the challenge's own marker.
CHALLENGE_MARKERS = ("__cf_chl", "cf_chl_opt", "Vercel Security Checkpoint", "Just a moment")

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# The instrument's declared ceilings, restated because every number depends on
# them.  See PROTOCOL.md "What was read before this file existed".
INSTRUMENT_NOTES = {
    "is_a_floor": (
        "Sourcegraph indexes a subset of GitHub. Every count is 'at least N'."
    ),
    "default_exclusions": (
        "forks and archived repositories are excluded unless fork:yes archived:yes"
    ),
    "unit": (
        "the file: pattern is a path glob, so a repository counts once however "
        "many of its files match"
    ),
    "auth": "no token is sent; the public stream is the whole instrument",
}

# Saturation ceiling observed on the calibration anchors. Above this the
# repositoriesCount is a floor set by our own count: parameter, not by the world,
# and a query at the ceiling is reported as saturated rather than as its number.
CEILING = 4000


def _quote(term):
    """Escape a query term for the URL, leaving Sourcegraph operators readable."""
    return term.replace("%", "%25").replace(":", "%3A").replace(" ", "%20")


def _slug(query):
    safe = re.sub(r"[^A-Za-z0-9]+", "-", query).strip("-").lower()
    return safe[:80]


def detect_challenge(text):
    """Name the challenge marker if this response is one, else None.

    Kept separate from fetch() so that a challenge is a *named* refusal rather
    than an unexplained zero, and so the distinction is testable.
    """
    for marker in CHALLENGE_MARKERS:
        if marker in text:
            return marker
    return None


def capture_name(query, name=None):
    """The filename a query's raw capture is written under.

    One definition, callable by the consumer. The slug was previously recomputed
    independently by forkstatus.py and the two versions disagreed once the query
    header was added to the file, which turned all twenty-two configurations into
    `no_origin`. Anything that needs to find a capture must call this.
    """
    return name or _slug(query)


def fetch(query, name=None, sleep=0.0):
    """Run one query, write the raw stream, return a parsed record.

    A record always has a `state`: ok, refused, or saturated.  `count` is None
    for anything but ok/saturated.  `skipped` carries the instrument's own
    account of what it did not return.
    """
    name = capture_name(query, name)
    url = STREAM_URL % _quote(query)
    path = os.path.join(RAW, "%s.sse" % name)
    os.makedirs(RAW, exist_ok=True)

    # A capture that already holds an answer is never overwritten by a later
    # attempt. This is not tidiness: the anti-bot challenge arms after ~30
    # requests, so a retry loop re-asks questions it has already answered and
    # every retry replaces a good capture with an HTML challenge page. That
    # destroyed five low-band captures with counts of 1, 1, 1, 1 and 2, and the
    # figures were then unrecoverable because nothing else recorded them. A
    # refusal is written beside the capture it failed to replace, never over it.
    # A run asked to reproduce a result must never be able to destroy the capture
    # it reproduces. Falsifying a test by restoring the defect it holds means
    # executing the defective code, and this guard lived only inside fetch()'s
    # cache path -- so a test called fetch() and fetch() overwrote the H1 capture
    # with an HTML challenge page. The figure survived in results.json and in this
    # session's command log; the bytes did not.
    #
    # It is checked FIRST, ahead of the cache return, because a cache return is
    # itself the safe path and would otherwise make this unreachable exactly when
    # a capture holds an answer -- which is the case it exists for.
    if os.environ.get("COPYCOUNT_PROTECT") and os.path.exists(path):
        held = read_raw(path).get("count")
        if held != os.environ["COPYCOUNT_PROTECT"]:
            raise AssertionError(
                "refusing to touch capture %s: it holds %s, not the %s this run "
                "was asked to reproduce. Set COPYCOUNT_PROTECT to the value on "
                "disk to overwrite it deliberately."
                % (name, held, os.environ["COPYCOUNT_PROTECT"])
            )

    # A capture that already holds an answer is never overwritten by a later
    # attempt. This is not tidiness: the anti-bot challenge arms after ~30
    # requests, so a retry loop re-asks questions it has already answered and
    # every retry replaces a good capture with an HTML challenge page. That
    # destroyed five low-band captures with counts of 1, 1, 1, 1 and 2, and the
    # figures were then unrecoverable because nothing else recorded them. A
    # refusal is written beside the capture it failed to replace, never over it.
    if os.path.exists(path):
        prior = read_raw(path)
        if prior["state"] in ("ok", "saturated") and prior.get("query") == query:
            prior["reused_from_cache"] = True
            return prior

    proc = subprocess.Popen(
        [
            "curl", "-s", "-N", "--max-time", "180",
            "-A", USER_AGENT,
            "-H", "Accept: text/event-stream",
            url,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    text = out.decode("utf-8", "replace")

    record = {"query": query, "name": name, "raw": os.path.relpath(path, HERE)}

    # Checked before anything is written, and before any parse: an HTML challenge
    # page contains no events at all, so without this it would fall through to
    # the generic refused branch and the reason would read "no terminal progress
    # event" -- true, and useless. It is also checked before the write, because a
    # challenge must never land on the path a real answer occupies.
    challenge = detect_challenge(text)
    if challenge is not None:
        record["state"] = "refused"
        record["count"] = None
        record["reason"] = "anti-bot challenge (%s), not an answer about the query" % challenge
        # Kept under its own name, so a refusal cannot masquerade as a later
        # reading of the same question, and so the failure is on disk at all.
        with open(path + ".refused", "w") as handle:
            handle.write("# query: %s\n" % query)
            handle.write(text)
        record["raw"] = os.path.relpath(path + ".refused", HERE)
        return record

    # The query goes into the capture itself, as its first line. A raw file that
    # records only its own slug cannot be traced back to what was asked, and this
    # repository's whole complaint about its instruments is that a figure could
    # not be tied to the request that produced it (F035's one-row count, F036's
    # well-formed irrelevant answer).
    with open(path, "w") as handle:
        handle.write("# query: %s\n" % query)
        handle.write(text)
    with open(path + ".stderr", "w") as handle:
        handle.write(err.decode("utf-8", "replace"))

    # A run asked to reproduce a result must never be able to destroy the capture
    # it reproduces. Falsifying a test by restoring the defect it holds means
    # executing the defective code, and this guard lived only inside fetch()'s
    # cache path -- so a test called fetch() and fetch() overwrote the H1 capture
    # with an HTML challenge page. The figure survived in results.json and in the
    # session's command log; the bytes did not. Checked BEFORE the write, and
    # armed by the environment rather than by a flag the caller can forget.
    if proc.returncode != 0 or not text.strip():
        record["state"] = "refused"
        record["count"] = None
        record["reason"] = "curl exit %d, %d bytes" % (proc.returncode, len(text))
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
        record["state"] = "refused"
        record["count"] = None
        record["reason"] = "no terminal progress event in %d bytes" % len(text)
        return record

    record["repositoriesCount"] = progress.get("repositoriesCount")
    record["matchCount"] = progress.get("matchCount")
    record["durationMs"] = progress.get("durationMs")
    record["skipped"] = progress.get("skipped", [])

    limit_hit = any(
        item.get("reason") in ("shard-match-limit", "hit-limit")
        for item in record["skipped"]
    )
    if progress.get("repositoriesCount") is None:
        # A query that matched nothing reports matchCount without the repo field.
        record["state"] = "ok"
        record["count"] = 0 if progress.get("matchCount") == 0 else None
        if record["count"] is None:
            record["state"] = "refused"
            record["reason"] = "terminal event matched files but named no repository"
        return record

    record["count"] = progress["repositoriesCount"]
    if limit_hit or record["count"] >= CEILING:
        record["state"] = "saturated"
        record["reason"] = "instrument returned no more than count:4000; this is a floor set by the query, not by the world"
    else:
        record["state"] = "ok"
    return record


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


def main(argv):
    if len(argv) >= 2 and argv[1] == "--rebuild":
        records = rebuild_index()
        print("rebuilt %d records from raw/" % len(records))
        return 0
    if len(argv) < 2:
        sys.stderr.write("usage: copycount.py PATTERN [PATTERN ...] | --rebuild\n")
        return 1
    results = []
    for pattern in argv[1:]:
        rec = fetch(pattern)
        results.append(rec)
        print("%-58s %-9s %s" % (pattern[:58], rec["state"], rec.get("count")))
        sys.stdout.flush()
        time.sleep(1.0)
    # Merged, not overwritten. The first version wrote the whole file each run,
    # so re-running three patterns to add a hook path silently discarded the nine
    # counts fetched before it -- and the consumer then reported "3 of 10
    # configurations have a count", which reads as a fact about the vocabulary
    # rather than as this file having been clobbered. The first run in a fresh
    # clone still creates it.
    out = os.path.join(HERE, "copycount.json")
    existing = []
    if os.path.exists(out):
        with open(out) as handle:
            existing = json.load(handle).get("records", [])
    merged = {}
    for rec in existing + results:
        merged[rec["query"]] = rec
    with open(out, "w") as handle:
        json.dump(
            {"instrument": INSTRUMENT_NOTES, "records": [merged[k] for k in sorted(merged)]},
            handle, indent=1, sort_keys=True,
        )
        handle.write("\n")
    print("wrote %s" % os.path.relpath(out, HERE))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
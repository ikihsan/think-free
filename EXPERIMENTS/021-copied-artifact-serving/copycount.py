#!/usr/bin/env python3
"""Fetch Sourcegraph repository-level counts for declared path patterns.

Every query writes its raw stream to raw/ before anything is parsed, so a figure
in results.json can be traced to bytes on disk.  Declared in
EXPERIMENTS/021-copied-artifact-serving/PROTOCOL.md.

Unauthenticated only.  A refused, truncated or errored answer is `refused` and is
never counted as a zero -- F032's defect class, which has already bitten this
repository twice.

The on-disk format lives in `captureformat.py` and is not restated here: what a
capture on disk means, how it is named, and how the index is re-derived from it
are one invariant, and this file is only how to obtain one.
"""

import json
import os
import subprocess
import sys
import time

from captureformat import (  # noqa: F401  (re-exported: callers import these here)
    CEILING,
    CHALLENGE_MARKERS,
    INSTRUMENT_NOTES,
    detect_challenge,
    read_raw,
    rebuild_index,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

STREAM_URL = "https://sourcegraph.com/.api/search/stream?q=%s&v=V3&t=literal"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def _quote(term):
    """Escape a query term for the URL, leaving Sourcegraph operators readable.

    `:` and `%` are the two that break a URL, and `:` is also the operator
    character, so it is escaped without touching the operators the query is built
    from. The slug is applied after this, never to the quoted string.
    """
    return term.replace("%", "%25").replace(":", "%3A").replace(" ", "%20")


def capture_name(query, name=None):
    """The filename a query's raw capture is written under.

    Re-exported from `captureformat`, which owns it. It lived here once and was
    re-implemented independently by forkstatus.py; the two versions disagreed once
    the query header was added to the capture, which turned all twenty-two
    configurations into `no_origin`. One definition, imported by everyone.
    """
    from captureformat import capture_name as _named

    return _named(query, name)

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


def main(argv):
    """The command line, in the file that fetches.

    `--rebuild` re-derives the index from captures already on disk, which is a
    property of the format rather than a fetch; it is routed here because this is
    where a caller looks for it.
    """
    if len(argv) >= 2 and argv[1] == "--rebuild":
        print("rebuilt %d records from raw/" % len(rebuild_index()))
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
    # rather than as this file having been clobbered.
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

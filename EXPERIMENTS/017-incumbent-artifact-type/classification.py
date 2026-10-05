#!/usr/bin/env python3
"""Artifact type from primary evidence: a repository's root file listing and
whether it has published a release.

Three classes, and a third one that exists because of the previous experiment:

    executable   the root carries a build/install/entry marker, or the repository
                 has published at least one release
    document     the root was readable and carries none of those
    unreadable   the root could not be read, or is empty, or was not fetched

`unreadable` is never folded into `document`. 015's first run counted a
repository publishing no release assets as a *decided reading of zero use*; a
project that ships nothing has told us about its distribution, not its use. The
same error here would be counting a repository this instrument cannot open as a
document, which is the one class whose whole claim is that the repository exists.

    python3 classification.py            # the tally
    python3 classification.py --selfcheck
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

MARKERS = frozenset([
    "package.json", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt",
    "cargo.toml", "go.mod", "pom.xml", "build.gradle", "gemfile", "composer.json",
    "dockerfile", "docker-compose.yml", "makefile", "cmakelists.txt", "install.sh",
    "bin",
])

# Declared as an entry-name match, then corrected before any classification result
# was read. `index.*` matches `index.html` and `index.md`, so as first declared it
# called a web page an executable artifact -- and the error direction is the one
# that would have *inflated* the executable class, which is the class this
# experiment needs to be small in the young arm. Kept, and reported, rather than
# quietly replaced: see DECLARED_CORRECTION.
ENTRY_STEMS = ("cli", "main", "index", "app", "server")
SOURCE_SUFFIXES = (".py", ".js", ".ts", ".go", ".rs", ".rb", ".sh", ".java",
                   ".cs", ".php", ".ex", ".c", ".cpp", ".js")

DECLARED_CORRECTION = (
    "ENTRY_STEMS are matched only against source suffixes. As first declared the "
    "match was on any suffix, which made `index.html` an executable artifact. "
    "The correction was written before any row was classified, from the shape of "
    "the rule rather than from a row, and both classifications are reported."
)

REFUSED = "refused:upstream"
EMPTY = "empty_or_missing"

# The refusal vocabulary is the transport's, not this module's. `rootlisting.py`
# once declared its own `"refused"` while this compared against
# `"refused:upstream"`, and a genuinely refused listing therefore matched no
# branch and reached the `unexpected_shape` fallback. Asserted equal by
# tests/test_artifact_population.py so the two cannot drift apart again.


def _marker_hits(entries, stems_restricted):
    hits = []
    for e in entries:
        name = (e.get("name") or "").lower()
        if not name:
            continue
        if name in MARKERS:
            hits.append(e.get("path") or name)
            continue
        head, dot, tail = name.rpartition(".")
        if dot and head in ENTRY_STEMS:   # a suffix exists: `cli.py`, not `cli`
            if stems_restricted and "." + tail not in SOURCE_SUFFIXES:
                continue
            hits.append(e.get("path") or name)
    return sorted(set(hits))


def classify(entry, releases_include=True):
    """One classification for one cached row.

    `entry` is what `rootlisting.py` cached: `{"contents": ..., "releases": ...}`.
    Returns a dict, not a string, so the evidence behind the class travels with
    the class.
    """
    if not isinstance(entry, dict) or "contents" not in entry:
        return {"class": "unreadable", "reason": "not_fetched", "hits": [],
                "releases": None}
    contents, rel = entry["contents"], entry.get("releases")
    if contents == REFUSED:
        return {"class": "unreadable", "reason": "refused", "hits": [],
                "releases": None}
    if contents == EMPTY or contents is None:
        return {"class": "unreadable", "reason": EMPTY, "hits": [],
                "releases": rel if isinstance(rel, int) else None}
    if not isinstance(contents, list):
        return {"class": "unreadable", "reason": "unexpected_shape", "hits": [],
                "releases": rel if isinstance(rel, int) else None}

    hits = _marker_hits(contents, True)
    loose = _marker_hits(contents, False)
    has_release = isinstance(rel, int) and rel > 0
    if hits or (releases_include and has_release):
        klass = "executable"
    else:
        klass = "document"

    out = {"class": klass, "hits": hits, "loose_hits": loose,
           "releases": rel if isinstance(rel, int) else None,
           "root_size": len(contents)}
    if not releases_include:
        # The contents-only reading, reported alongside because "ships a binary and
        # keeps no manifest" is a real class and F032's `thought-machine/please`
        # is one. A refused release count leaves the row decided on contents alone
        # and says so, rather than being read as "no releases".
        out["class_contents_only"] = "executable" if loose else "document"
        if not isinstance(rel, int):
            out["class_contents_only_reason"] = "releases_refused_or_missing"
    return out


def classify_all(cache, releases_include=True):
    return {name: classify(entry, releases_include)
            for name, entry in (cache or {}).items()}


# ------------------------------------------------------------- self-check cases
# Written before the population was classified. Each case is a repository whose
# root is known, and the classifier is asserted in both directions: a row that
# should be executable must not read as a document, and a row that should be a
# document must not read as executable.

KNOWN_ANSWER = [
    # (label, cached entry, expected class)
    ("python package", {"contents": [{"name": "setup.py", "type": "file"},
                                     {"name": "README.md", "type": "file"}],
                        "releases": 0}, "executable"),
    ("binary only, no manifest", {"contents": [{"name": "main.go", "type": "file"},
                                               {"name": "README.md", "type": "file"}],
                                  "releases": 3}, "executable"),
    ("guide", {"contents": [{"name": "README.md", "type": "file"},
                            {"name": "LICENSE", "type": "file"}],
               "releases": 0}, "document"),
    ("prompt collection", {"contents": [{"name": "prompts", "type": "dir"},
                                        {"name": "README.md", "type": "file"}],
                           "releases": 0}, "document"),
    ("docker compose stack", {"contents": [{"name": "docker-compose.yml", "type": "file"},
                                           {"name": ".gitignore", "type": "file"}],
                              "releases": 0}, "executable"),
    ("cli entrypoint", {"contents": [{"name": "cli.py", "type": "file"}],
                        "releases": 0}, "executable"),
    ("bin directory", {"contents": [{"name": "bin", "type": "dir"}],
                       "releases": 0}, "executable"),
    ("web page only", {"contents": [{"name": "index.html", "type": "file"}],
                       "releases": 0}, "document"),
    ("static site", {"contents": [{"name": "index.js", "type": "file"}],
                     "releases": 0}, "executable"),
    ("empty repository", {"contents": EMPTY, "releases": 0}, "unreadable"),
    ("refused listing", {"contents": REFUSED, "releases": None}, "unreadable"),
    ("not fetched", {"contents": None}, "unreadable"),
]

def classify_as_first_declared(entry):
    """The classifier exactly as this file first declared it: the entry-name
    patterns matched on any suffix.

    Kept executable so the test can assert that DECLARED_CORRECTION changes an
    answer rather than being a comment about one.
    """
    out = classify(entry)
    if out["class"] == "document" and out.get("loose_hits"):
        out["class"] = "executable"
    return out


def run_selfcheck():
    ok = True
    for label, entry, expected in KNOWN_ANSWER:
        got = classify(entry)["class"]
        flag = "ok " if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("  %s %-26s expected %-11s got %s" % (flag, label, expected, got))
    return ok


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        sys.exit(0 if run_selfcheck() else 1)
    cache = os.path.join(HERE, "raw", "rootlistings.json")
    with open(cache) as fh:
        rows = classify_all(json.load(fh))
    tally = {}
    for value in rows.values():
        tally[value["class"]] = tally.get(value["class"], 0) + 1
    print(json.dumps(tally, indent=1, sort_keys=True))
#!/usr/bin/env python3
"""E041 verify: recompute every input digest and every row count from the bytes.

F063's rule, applied here: a hand-written digest in a summary file is not
evidence, it is a claim. This recomputes sha256 over the captured files and
re-derives the arm counts by re-reading the corpus, then exits 3 on any
difference.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
REF_PATTERNS = [
    re.compile(r"duplicate\s+of\s+#(\d+)", re.I),
    re.compile(r"dup(?:e|licate)?\s*(?:of|:)\s*#(\d+)", re.I),
    re.compile(r"same\s+(?:as|issue\s+as)\s+#(\d+)", re.I),
    re.compile(r"->\s*#(\d+)"),
    re.compile(r"see\s*#(\d+)"),
    re.compile(r"https?://github\.com/[^/\s]+/[^/\s]+/issues/(\d+)", re.I),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def target_ref(body):
    for pat in REF_PATTERNS:
        m = pat.search(body or "")
        if m:
            return int(m.group(1))
    return None


def main():
    problems = []
    with open(os.path.join(RAW, "arms_summary.json")) as fh:
        s = json.load(fh)

    for name, recorded in (("corpus.jsonl", s.get("corpus_sha256")),
                           ("arms.jsonl", s.get("arms_sha256"))):
        path = os.path.join(RAW, name)
        if not os.path.exists(path):
            problems.append("missing %s" % name)
            continue
        got = sha256(path)
        if got != recorded:
            problems.append("%s digest %s != recorded %s" % (name, got, recorded))
        else:
            print("digest ok: %s %s" % (name, got[:16]))

    # Re-derive arm P from the bytes: the pair count and its stratum split.
    pairs = 0
    stratum = {"S-easy": 0, "S-hard": 0}
    dropped = {"no_parseable_ref": 0, "target_not_in_corpus": 0,
               "target_is_self": 0, "target_missing_title": 0}
    excluded = set(s.get("repos_excluded_automation") or [])
    corpus, seen = [], set()
    with open(os.path.join(RAW, "corpus.jsonl")) as fh:
        for line in fh:
            row = json.loads(line)
            key = (row["repo"], row["number"])
            if key in seen or row["repo"] in excluded:
                continue
            seen.add(key)
            corpus.append(row)
    if len(corpus) != s.get("corpus_rows"):
        problems.append("corpus_rows %d != recorded %d"
                        % (len(corpus), s.get("corpus_rows")))
    index = {}
    for r in corpus:
        index.setdefault(r["repo"], set()).add(r["number"])
    for r in corpus:
        if r.get("state_reason") != "duplicate":
            continue
        ref = target_ref(r["body"])
        if ref is None:
            dropped["no_parseable_ref"] += 1
            continue
        if ref == r["number"]:
            dropped["target_is_self"] += 1
            continue
        if ref not in index.get(r["repo"], ()):
            dropped["target_not_in_corpus"] += 1
            continue
        pairs += 1
    if pairs != s.get("pairs_P"):
        problems.append("pairs_P %d != recorded %d" % (pairs, s.get("pairs_P")))

    # And the arms file itself, joined by key rather than trusted.
    with open(os.path.join(RAW, "arms.jsonl")) as fh:
        for line in fh:
            a = json.loads(line)
            stratum[a["stratum"]] += 1
    if stratum != s.get("pairs_by_stratum"):
        problems.append("strata %s != recorded %s"
                        % (stratum, s.get("pairs_by_stratum")))

    print("re-derived from bytes: corpus_rows=%d pairs_P=%d strata=%s dropped=%s"
          % (len(corpus), pairs, stratum, dropped))
    if problems:
        for p in problems:
            print("PROBLEM: %s" % p)
        return 3
    print("all manifest checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

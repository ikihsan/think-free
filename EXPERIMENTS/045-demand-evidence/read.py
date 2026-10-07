#!/usr/bin/env python3
"""E045 — read the demand evidence the candidate rests on.

Extracts the 195 harvested GitHub issues from E038's cached search-API
responses, locates the four issues the record names, and classifies every
issue on the two questions the record never asked: who is making the request,
and which interface does the requester lack.

Run: python3 EXPERIMENTS/045-demand-evidence/read.py
Writes raw/issues.jsonl next to this file. Exit 0 on success, 1 on a corpus
that does not match the declared shape.

The classifier's rules live in `rules.py`, the rendering lives in `report.py`,
and the reader's own labels live in `raw/hand-labels.tsv`. This file is the
reading: corpus in, one labelled row per issue out, `raw/issues.jsonl` written.
It is the only place the rules and the reader's labels are joined, which is
what makes the reported precision and recall (D069) a measurement of the rules
rather than a statement about them.
"""

import json
import os
import re
import sys
import unicodedata

import report
from rules import (
    GAP_RULES,
    REQUESTER_RULES,
    first_match,
    has_diff_access,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CORPUS = os.path.join(
    HERE, "..", "038-staging-prior-art", "raw", "requests.jsonl"
)

# The four issues F064 names as the need, with the repository they came from.
NAMED = [
    "sublime_merge#976",
    "vim-gitgutter#446",
    "sublime_merge#465",
    "mcp-multi-root-git#3",
]


def load_corpus():
    """Return (responses, issues). Only `issue:` arms carry harvested issues."""
    responses = []
    issues = []
    with open(CORPUS) as fh:
        for line in fh:
            d = json.loads(line)
            responses.append(d)
            if not str(d.get("measure", "")).startswith("issue:"):
                continue
            if d.get("status") != 200:
                continue
            try:
                items = json.loads(d["body"])["items"]
            except Exception:
                continue  # rate-limited or malformed; counted, not used
            for it in items:
                issues.append((d["measure"], it))
    return responses, issues


def repo_of(issue):
    m = re.search(
        r"api\.github\.com/repos/([^/]+/[^/]+)/issues/", issue["url"]
    )
    return m.group(1) if m else "?"


def body_text(issue):
    return issue.get("body") or ""


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"\s+", " ", s).strip()


def first_paragraph(text, limit=400):
    """The requester's own words before any log, diff, or thanks."""
    paras = [p.strip() for p in (text or "").split("\n\n")]
    out = []
    for p in paras:
        if not p:
            continue
        if p.startswith("```") or p.startswith("    "):
            break
        out.append(p)
        if sum(len(x) for x in out) > limit:
            break
    return norm(" ".join(out))[:limit]


# --- requester class, gap class and diff access live in rules.py -----------
# They were in this file until it reached the cap. The split is by invariant,
# not by size: the rules are an instrument with its own measured precision, and
# the measurement is the reason a reader would come looking for them.


def load_hand_labels(n):
    """The reader's own labels, written before this script's output was read."""
    path = os.path.join(RAW, "hand-labels.tsv")
    labels = {}
    with open(path) as fh:
        for line in fh:
            line = line.split("#")[0].strip()
            if not line or line.startswith("idx"):
                continue
            parts = [p.strip() for p in line.split("\t")]
            if len(parts) < 6 or not parts[0].isdigit():
                continue
            if int(parts[0]) >= n:
                continue
            labels[int(parts[0])] = {
                "need": int(parts[1]),
                "requester": parts[2],
                "diff_access": parts[3],
                "operation": parts[4],
                "wants": parts[5],
            }
    return labels


def main():
    os.makedirs(RAW, exist_ok=True)
    responses, harvested = load_corpus()
    need_arms = [
        r for r in responses
        if str(r.get("measure", "")).startswith("issue:")
    ]
    ok = [r for r in need_arms if r.get("status") == 200]
    failed = [r for r in need_arms if r.get("status") != 200]

    # Denominator 1: the search universe the record's rate is a fraction of.
    universe = sum(r.get("total_count") or 0 for r in ok)
    # Denominator 2: the harvested set, deduplicated.
    seen = {}
    for arm, it in harvested:
        seen.setdefault(it["html_url"], (arm, it))
    n_unique = len(seen)

    if n_unique == 0:
        print("corpus empty", file=sys.stderr)
        return 1

    rows = []
    for url, (arm, it) in sorted(
        seen.items(), key=lambda kv: kv[1][1].get("created_at") or ""
    ):
        text = body_text(it)
        req, req_hit, req_ctx = first_match(REQUESTER_RULES, text)
        if req is None:
            req = "unclassified"
        gap, gap_hit, gap_ctx = first_match(GAP_RULES, text)
        if gap is None:
            gap = "other-or-unclear"
        repo = repo_of(it)
        ref = "%s#%s" % (repo.split("/")[-1], it["number"])
        rows.append({
            "ref": ref,
            "repo": repo,
            "number": it["number"],
            "url": url,
            "title": it["title"],
            "state": it.get("state"),
            "created_at": it.get("created_at"),
            "comments": it.get("comments"),
            "author_association": it.get("author_association"),
            "author": (it.get("user") or {}).get("login"),
            "arms": [arm],
            "named": ref in NAMED,
            "requester": req,
            "requester_evidence": req_hit,
            "requester_context": req_ctx,
            "gap": gap,
            "gap_evidence": gap_hit,
            "gap_context": gap_ctx,
            "diff_access": has_diff_access(it, text),
            "lead": first_paragraph(text),
            "body_len": len(text),
        })

    # Which of the four named issues are actually present, verbatim.
    named_rows = [r for r in rows if r["named"]]
    named_missing = [n for n in NAMED if n not in {r["ref"] for r in named_rows}]

    out = os.path.join(RAW, "issues.jsonl")
    rows.sort(key=lambda r: (r["repo"], r["number"]))
    labels = load_hand_labels(len(rows))
    if len(labels) != len(rows):
        print("hand labels cover %d of %d rows" % (len(labels), len(rows)))
        return 1
    for i, r in enumerate(rows):
        r["hand"] = labels[i]
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    # --- report ------------------------------------------------------------
    # The rendering lives in `report.py`: this file is the reading, and the
    # split is what stops a change to a printed label from changing which rows
    # are written, or the reverse.
    report.emit(rows, {
        "need_arms": need_arms,
        "ok": ok,
        "failed": failed,
        "harvested": sum(len(json.loads(r["body"])["items"]) for r in ok),
        "universe": universe,
        "named": NAMED,
        "named_missing": named_missing,
        "out": out,
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())

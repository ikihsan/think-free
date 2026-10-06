#!/usr/bin/env python3
"""E038 pools A and B: code indexes, Stack Exchange, GitHub issues, rendered search."""
import os
import urllib.parse

from harvest_core import (RAW, GH, SE, GREP, DEBIAN, NEGATIVE, NEED_SITES,
                    NEED_QUERIES, CODE_TERMS, REPO_QUERIES, DELETIONS,
                    SOURCES, do, done)


def poola():
    """Code index. The probe decides which index answers unauthenticated; both are
    recorded either way so the choice is auditable. GitHub code search answered 401
    "Requires authentication" in the probe, so the 24 code terms run on the surfaces
    that did answer, and the primary sources are fetched whole."""
    seen = done()
    with open(os.path.join(RAW, "requests.jsonl"), "a") as fh:
        for name, url in SOURCES:
            if name in seen:
                continue
            rec = do(fh, name, url, arm="source", index="primary-source")
            if rec["status"] == 200 and len(rec["body"]) > 200:
                path = os.path.join(RAW, "sources", name + ".txt")
                with open(path, "w") as out:
                    out.write(rec["body"])
        for t in REPO_QUERIES:
            m = "gh-repo:%s" % t
            if m in seen:
                continue
            do(fh, m, GH + "/search/repositories?" + urllib.parse.urlencode(
                {"q": t, "per_page": 10}), query=t, index="github-repos")
        for t in CODE_TERMS:
            m = "grep:%s" % t
            if m in seen:
                continue
            do(fh, m, GREP + "?" + urllib.parse.urlencode({"q": t}), term=t, index="grep-app")


def poolb():
    seen = done()
    with open(os.path.join(RAW, "requests.jsonl"), "a") as fh:
        for field, text in NEED_QUERIES:
            for site in NEED_SITES:
                m = "need:%s:%s:%s" % (field, site, text)
                if m in seen:
                    continue
                params = {"site": site, field: text, "pagesize": 100, "sort": "votes"}
                do(fh, m, SE + "/search/advanced?" + urllib.parse.urlencode(params),
                   arm="need", field=field, phrase=text, site=site, index="stackexchange")
        for site in NEED_SITES:
            m = "control-negative:%s" % site
            if m in seen:
                continue
            do(fh, m, SE + "/search/advanced?" + urllib.parse.urlencode(
                {"site": site, "q": NEGATIVE, "pagesize": 100}),
               arm="control-negative", field="q", phrase=NEGATIVE, site=site,
               index="stackexchange")
            m = "control-denominator:%s" % site
            if m in seen:
                continue
            do(fh, m, SE + "/search/advanced?" + urllib.parse.urlencode(
                {"site": site, "tagged": "git", "pagesize": 1}),
               arm="control-denominator", site=site, index="stackexchange")
        for field, text in DELETIONS:
            m = "control-deletion:%s:%s" % (field, text)
            if m in seen:
                continue
            do(fh, m, SE + "/search/advanced?" + urllib.parse.urlencode(
                {"site": "stackoverflow", field: text, "pagesize": 100, "sort": "votes"}),
               arm="control-deletion", field=field, phrase=text, site="stackoverflow",
               index="stackexchange")




# ---------------------------------------------------------------------------
# Pool B2: the same need phrasings on the second venue that answers unauthenticated,
# GitHub issues. A developer asking for line-addressable staging files an issue far
# more often than a question. Same phrases, same negative control, so the two venues
# are read with the same instrument shape.
# ---------------------------------------------------------------------------
ISSUE_QUERIES = [
    'in:title,body "stage specific lines"',
    'in:title,body "stage a single line"',
    'in:title,body "stage only one line"',
    'in:title,body "stage line number"',
    'in:title,body "stage by line number"',
    'in:title,body "git add -p non-interactive"',
    'in:title,body "git add -p" automation script',
    'in:title,body "partially stage" lines',
    'in:title,body "stage hunks by line"',
    'in:title,body "select lines to stage"',
]


def poolc():
    seen = done()
    with open(os.path.join(RAW, "requests.jsonl"), "a") as fh:
        for q in ISSUE_QUERIES:
            m = "issue:%s" % q
            if m in seen:
                continue
            do(fh, m, GH + "/search/issues?" + urllib.parse.urlencode(
                {"q": q, "per_page": 30, "sort": "reactions"}),
               arm="need", phrase=q, site="github-issues", index="github-issues")
        m = "issue-control-negative"
        if m not in seen:
            do(fh, m, GH + "/search/issues?" + urllib.parse.urlencode(
                {"q": 'in:title,body "%s"' % NEGATIVE, "per_page": 30}),
                arm="control-negative", phrase=NEGATIVE, site="github-issues",
                index="github-issues")
        m = "issue-control-denominator"
        if m not in seen:
            do(fh, m, GH + "/search/issues?" + urllib.parse.urlencode(
                {"q": "in:title,body %22git+add+-p%22", "per_page": 1}),
                arm="control-denominator", site="github-issues", index="github-issues")


# ---------------------------------------------------------------------------
# Pool B3: the rendered Stack Overflow search, which answers while the API quota
# window is closed. Its counts are the platform's own label, the same class of
# evidence as closed_reason: a label, not a measurement. Re-checked against the API
# when the window opens, which is the control that makes it usable.
# ---------------------------------------------------------------------------
RENDERED = "https://stackoverflow.com/search?"


def poold():
    seen = done()
    with open(os.path.join(RAW, "requests.jsonl"), "a") as fh:
        for field, text in NEED_QUERIES:
            m = "rendered:%s:%s" % (field, text)
            if m in seen:
                continue
            do(fh, m, RENDERED + urllib.parse.urlencode({"q": text}),
               arm="need", field="free-text", phrase=text, site="stackoverflow",
               index="stackexchange-rendered")
        m = "rendered-control-negative"
        if m not in seen:
            do(fh, m, RENDERED + urllib.parse.urlencode({"q": NEGATIVE}),
                arm="control-negative", phrase=NEGATIVE, site="stackoverflow",
                index="stackexchange-rendered")
        m = "rendered-control-phrasedrop"
        if m not in seen:
            do(fh, m, RENDERED + urllib.parse.urlencode({"q": "git add -p"}),
                arm="control-deletion", phrase="git add -p", site="stackoverflow",
                index="stackexchange-rendered")


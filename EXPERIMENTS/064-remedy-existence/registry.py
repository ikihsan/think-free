#!/usr/bin/env python3
"""Model-free, cross-ecosystem existence check for a named remedy.

One function, `check(ecosystem, name)`, returning exactly one of

    "exists"    the registry answered 200 / numFound>0 for the name
    "absent"    the registry answered 404 / numFound==0, i.e. no
    "unknown"   a missing observation: rate limit, 5xx, timeout,
                DNS, parse failure, no free endpoint. Per D082
                this is never a zero and never a denominator.

No search engine and no model is used anywhere in this file:
its answer is reproducible and its cost is one HTTP request.
Stdlib only. The CLI that runs it lives in `control.py`:

    python3 control.py --self-test
    python3 control.py --emit-control          # real names, for arm C
    python3 control.py raw/names.tsv raw/verdicts.json
"""
from __future__ import print_function

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = "think-free-remedy-existence/0.1 (research; no tracking)"
TIMEOUT = 25

EXISTS, ABSENT, UNKNOWN = "exists", "absent", "unknown"


def _get(url, headers=None):
    """Return (status, body). status is an int, or None on transport failure."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception:
        return None, b""


def _pypi(name):
    st, _ = _get("https://pypi.org/pypi/%s/json" % urllib.parse.quote(name))
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _npm(name):
    st, _ = _get("https://registry.npmjs.org/%s"
                 % urllib.parse.quote(name, safe="@/"))
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _crates(name):
    st, _ = _get("https://crates.io/api/v1/crates/%s" % name,
                 {"Accept": "application/json"})
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _rubygems(name):
    st, _ = _get("https://rubygems.org/api/v1/gems/%s.json"
                 % urllib.parse.quote(name))
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _sonatype(filter_expr):
    """One page of Maven Central versions, by `namespace:`/`name:` filter.

    The old `search.maven.org/solrsearch` host is retired and refuses
    the connection outright (curl reports HTTP 000), which the previous
    code turned into UNKNOWN for every Maven name. Central's own browse
    API is the replacement and returns `totalResultCount`, an explicit
    negative signal rather than an absence of one.
    """
    url = ("https://central.sonatype.com/api/internal/browse/component/versions"
           "?sortField=normalizedVersion&sortDirection=desc&page=0&size=1"
           "&filter=%s" % urllib.parse.quote(filter_expr, safe=""))
    st, body = _get(url)
    if st != 200:
        return None
    try:
        found = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return None
    if not isinstance(found, dict) or "totalResultCount" not in found:
        return None
    return found


def _maven(name):
    # Maven coordinates arrive as "group:artifact" or as the artifact.
    if ":" in name:
        group, art = name.split(":", 1)
        expr = "namespace:%s,name:%s" % (group, art)
    else:
        expr = "name:%s" % name
    found = _sonatype(expr)
    if found is None:
        return UNKNOWN
    return EXISTS if found.get("totalResultCount", 0) > 0 else ABSENT


def _nuget(name):
    url = ("https://azuresearch-usnc.nuget.org/query?q=packageid:%s&take=20"
           % urllib.parse.quote(name))
    st, body = _get(url)
    if st != 200:
        return UNKNOWN
    try:
        docs = json.loads(body.decode("utf-8", "replace"))["data"]
    except Exception:
        return UNKNOWN
    # Azure Search is case-insensitive and *does* return near matches on
    # `packageid:`; an invented `Foo.Bar.Coordination` came back as
    # `exists` because `Foo.Bar` was in the hit list. Compare exact
    # ids instead.
    for d in docs:
        if str(d.get("id", "")).lower() == name.lower():
            return EXISTS
    return ABSENT


def _packagist(name):
    url = "https://packagist.org/search.json?q=%s" % urllib.parse.quote(name)
    st, body = _get(url)
    if st != 200:
        return UNKNOWN
    try:
        results = json.loads(body.decode("utf-8", "replace"))["results"]
    except Exception:
        return UNKNOWN
    want = name.lower()
    for r in results:
        if str(r.get("name", "")).lower() == want:
            return EXISTS
    return ABSENT


def _goproxy(name):
    # Case encoding: an upper-case letter is "!" + its lower case.
    enc = "".join("!" + c.lower() if c.isupper() else c for c in name)
    st, body = _get("https://proxy.golang.org/%s/@latest" % enc)
    if st == 200:
        return EXISTS
    if st in (404, 410):
        return ABSENT
    return UNKNOWN


def _hex(name):
    st, _ = _get("https://hex.pm/api/packages/%s" % name)
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _github(name):
    st, _ = _get("https://github.com/%s" % name)
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _gitlab(name):
    st, _ = _get("https://gitlab.com/api/v4/projects/%s"
                 % urllib.parse.quote(name, safe=""))
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _brew(name):
    st, _ = _get("https://formulae.brew.sh/api/formula/%s.json" % name)
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


def _launchpad(name):
    st, body = _get("https://api.launchpad.net/1.0/%s" % name)
    return {200: EXISTS, 404: ABSENT}.get(st, UNKNOWN)


CHECKS = {
    "pypi": _pypi,
    "npm": _npm,
    "crates": _crates,
    "gem": _rubygems,
    "maven": _maven,
    "nuget": _nuget,
    "packagist": _packagist,
    "go": _goproxy,
    "hex": _hex,
    "github": _github,
    "gitlab": _gitlab,
    "brew": _brew,
    "launchpad": _launchpad,
}


def check(ecosystem, name):
    fn = CHECKS.get((ecosystem or "").lower())
    if fn is None:
        return UNKNOWN
    name = (name or "").strip()
    if not name:
        return UNKNOWN
    return fn(name)

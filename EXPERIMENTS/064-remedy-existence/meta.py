#!/usr/bin/env python3
"""Registry metadata for one (ecosystem, name), for the G6 discriminability rule.

Returns a dict with a fixed shape whatever happened:

    verdict    "exists" | "absent" | "unknown"     (from registry.py's rules)
    desc       description text, "" when the registry carries none
    n_versions int or None
    newest     ISO date of the newest release, or None
    repo       repository URL, "" when the registry carries none
    downloads  int or None

`None` means **the registry did not answer that question** and the field is not
evaluable — never a zero (D082). `downloads` is in-record for npm, crates.io,
RubyGems and Packagist, but PyPI has no such field and needs pypistats, which
rate-limits a burst at 429. A 429 therefore yields `downloads=None`, and the
scorer drops that clause from the rule for that row instead of reading the
absence as a low count.

Stdlib only. The CLI that runs it lives in `control.py`:

    python3 control.py --meta-self-test
    python3 control.py --meta raw/mutations.json raw/metadata.json
"""
from __future__ import print_function

import json
import os
import re
import sys
import time
import urllib.parse

import registry

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

EMPTY = {"verdict": registry.UNKNOWN, "desc": "", "n_versions": None,
         "newest": None, "repo": "", "downloads": None}


def _out(verdict, **kw):
    d = dict(EMPTY)
    d.update(verdict=verdict)
    d.update(kw)
    return d


def _clean_repo(url):
    if not url:
        return ""
    u = url.strip()
    if u.startswith("git+"):
        u = u[4:]
    if u.startswith("git://"):
        u = "https://" + u[6:]
    if u.endswith(".git"):
        u = u[:-4]
    return u


def pypi(name):
    st, body = registry._get("https://pypi.org/pypi/%s/json" % urllib.parse.quote(name))
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        d = json.loads(body.decode("utf-8", "replace"))
        info, rels = d["info"], d["releases"]
    except Exception:
        return _out(registry.UNKNOWN)
    ups = sorted(r["upload_time"] for v in rels.values() for r in v)
    repo = ""
    for v in (info.get("project_urls") or {}).values():
        if v and "github.com" in v:
            repo = _clean_repo(v)
            break
    if not repo:
        repo = _clean_repo(info.get("home_page") or "")
    # pypistats is the only download source for PyPI and it 429s a burst, so a
    # missing count is routine here and is recorded as not-evaluable.
    dl = None
    time.sleep(1.1)
    st2, b2 = registry._get(
        "https://pypistats.org/api/packages/%s/recent" % urllib.parse.quote(name))
    if st2 == 200:
        try:
            dl = int(json.loads(b2.decode())["data"]["last_month"]) * 12
        except Exception:
            dl = None
    return _out(registry.EXISTS, desc=(info.get("summary") or "").strip(),
                n_versions=len(rels), newest=ups[-1] if ups else None,
                repo=repo, downloads=dl)


def npm(name):
    st, body = registry._get("https://registry.npmjs.org/%s"
                             % urllib.parse.quote(name, safe="@/"))
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        d = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return _out(registry.UNKNOWN)
    if "error" in d:
        return _out(registry.ABSENT)
    times = d.get("time") or {}
    latest = (d.get("dist-tags") or {}).get("latest")
    newest = times.get(latest) if latest in times else None
    if newest is None:
        mod = times.get("modified")
        newest = mod
    dl = None
    st2, b2 = registry._get("https://api.npmjs.org/downloads/point/last-year/%s"
                            % urllib.parse.quote(name, safe="@/"))
    if st2 == 200:
        try:
            dl = int(json.loads(b2.decode())["downloads"])
        except Exception:
            dl = None
    repo_raw = d.get("repository") or ""
    repo_url = repo_raw if isinstance(repo_raw, str) else (repo_raw.get("url") or "")
    return _out(registry.EXISTS, desc=(d.get("description") or "").strip(),
                n_versions=len(d.get("versions") or {}), newest=newest,
                repo=_clean_repo(repo_url),
                downloads=dl)


def crates(name):
    st, body = registry._get("https://crates.io/api/v1/crates/%s" % name,
                             {"Accept": "application/json"})
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        d = json.loads(body.decode("utf-8", "replace"))
        if d.get("errors"):
            return _out(registry.ABSENT)
        c = d["crate"]
    except Exception:
        return _out(registry.UNKNOWN)
    newest = (c.get("updated_at") or "").replace("T", " ")
    return _out(registry.EXISTS, desc=(c.get("description") or "").strip(),
                n_versions=len(d.get("versions") or []), newest=newest or None,
                repo=_clean_repo(c.get("repository")),
                downloads=c.get("downloads"))


def gem(name):
    st, body = registry._get("https://rubygems.org/api/v1/gems/%s.json"
                             % urllib.parse.quote(name))
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        d = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return _out(registry.UNKNOWN)
    src = (_clean_repo(d.get("source_code_uri") or "")
           or _clean_repo(d.get("homepage_uri") or ""))
    return _out(registry.EXISTS, desc=(d.get("info") or "").strip(),
                n_versions=None, newest=d.get("version_created_at"),
                repo=src, downloads=d.get("downloads"))


def packagist(name):
    st, body = registry._get("https://repo.packagist.org/p2/%s.json"
                             % urllib.parse.quote(name.lower(), safe="/"))
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        packs = json.loads(body.decode("utf-8", "replace")).get("packages") or {}
    except Exception:
        return _out(registry.UNKNOWN)
    vers = packs.get(name.lower()) or packs.get(name) or []
    if not vers:
        return _out(registry.ABSENT)
    vers = sorted(vers, key=lambda v: v.get("time", ""))
    newest = vers[-1].get("time")
    repo = ""
    for v in reversed(vers):
        repo = _clean_repo((v.get("source") or {}).get("url"))
        if repo:
            break
    # Packagist's public packages/<name>.json no longer carries a download
    # count (checked 2026-10-08: the response is {"package": ...} only), so
    # downloads is not evaluable for this ecosystem. Recorded, not faked.
    return _out(registry.EXISTS,
                desc=(vers[-1].get("description") or "").strip(),
                n_versions=len({v.get("version") for v in vers}), newest=newest,
                repo=repo, downloads=None)


def nuget(name):
    # Azure Search carries downloads, description and project URL, but no
    # published date; the registration index's last page carries that.
    # Free registry metadata only, no search engine, no model.
    st, body = registry._get(
        "https://azuresearch-usnc.nuget.org/query?q=packageid:%s&take=20"
        % urllib.parse.quote(name))
    if st != 200:
        return _out(registry.UNKNOWN)
    try:
        docs = json.loads(body.decode("utf-8", "replace"))["data"]
    except Exception:
        return _out(registry.UNKNOWN)
    hit = None
    for d in docs:
        if str(d.get("id", "")).lower() == name.lower():
            hit = d
            break
    if hit is None:
        return _out(registry.ABSENT)
    newest = None
    reg = hit.get("registration") or ""
    if reg:
        idx = reg if reg.endswith("index.json") else reg.rstrip("/") + "/index.json"
        st2, b2 = registry._get(idx)
        if st2 == 200:
            try:
                pages = json.loads(b2.decode("utf-8", "replace")).get("items", [])
                last = pages[-1] if pages else None
                if isinstance(last, dict) and "@id" in last and "items" not in last:
                    st3, b3 = registry._get(last["@id"])
                    if st3 == 200:
                        last = json.loads(b3.decode("utf-8", "replace")).get("items", [])
                if isinstance(last, list) and last:
                    newest = (last[-1].get("catalogEntry", {}) or {}).get("published")
            except Exception:
                newest = None
    return _out(registry.EXISTS,
                desc=str(hit.get("description") or "").strip(),
                n_versions=len(hit.get("versions") or []), newest=newest,
                repo=_clean_repo(hit.get("projectUrl")),
                downloads=hit.get("totalDownloads"))


def brew(name):
    # formulae.brew.sh carries a description and a homepage and nothing else
    # the rule needs: no download count, no release date. Both are recorded
    # not-evaluable (not zero) exactly as packagist downloads already are.
    st, body = registry._get("https://formulae.brew.sh/api/formula/%s.json" % name)
    if st != 200:
        return _out(registry.ABSENT if st == 404 else registry.UNKNOWN)
    try:
        d = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return _out(registry.UNKNOWN)
    if not isinstance(d, dict) or "name" not in d:
        return _out(registry.UNKNOWN)
    return _out(registry.EXISTS, desc=str(d.get("desc") or "").strip(),
                n_versions=None, newest=None,
                repo=_clean_repo(d.get("homepage")), downloads=None)


FETCH = {"pypi": pypi, "npm": npm, "crates": crates, "gem": gem,
         "packagist": packagist, "nuget": nuget, "brew": brew}


def fetch(ecosystem, name):
    fn = FETCH.get((ecosystem or "").lower())
    if fn is None:
        return dict(EMPTY)
    return fn((name or "").strip())
#!/usr/bin/env python3
"""Usage measurement instrument: registry downloads over one month.

Stars are a vote; a download is an install. This module answers "was this
project used in the last 30 days" and nothing else. A project is credited with
the largest single-registry figure, and the registry that supplied it is
returned with the number so a mixed measurement is never invisible.

Three outcomes are kept apart, and keeping them apart is the whole design:

  a number    measured, and it is what it says
  None        the registry has no package of that name: not published, so
              treated as no usage — an absence, which is data
  REFUSED     the upstream declined to answer: **not** an absence

The distinction is not pedantry. Two defects in this file were found by the
pre-flight self-check rather than by a result, and both would have silently
pushed measurements towards zero, which is the direction that flatters the
hypothesis under test:

  * npm's single-package endpoint answers flat (`{"downloads": N}`) while its
    bulk endpoint keys by name (`{"vite": {"downloads": N}}`). Reading only the
    keyed shape reported four known-installed packages as unused.
  * shields.io answers a throttled request with **HTTP 200** and the body
    `{"message": "rate limited by upstream service"}`, which parses as a
    successful lookup of a package with no downloads.

Package names are guessed from repository names in `census.py`, the remaining
weak link. That guess can also only push a figure towards zero, and it is
falsified against packages whose answer is known before any result is used.
"""

import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "origin-census/1 (think-free T-0059)"
REFUSED = "refused:upstream"


def get(url, timeout=30):
    """Body text, or None for a genuine 404, or REFUSED for anything else."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return None if e.code in (404, 400) else REFUSED
    except Exception:
        return REFUSED


def jget(url, timeout=30):
    body = get(url, timeout)
    if body is REFUSED:
        return REFUSED
    if not body:
        return None
    try:
        return json.loads(body)
    except ValueError:
        return REFUSED


def parse_human(text):
    """shields.io renders '1.2G/month'; return the count, else None."""
    m = re.match(r"^([0-9.]+)([kMG]?)/month$", (text or "").strip())
    if not m:
        return None
    return int(float(m.group(1)) * {"": 1, "k": 1e3, "M": 1e6, "G": 1e9}[m.group(2)])


def npm_month(name):
    """Single-package npm downloads, accepting both response shapes."""
    data = jget("https://api.npmjs.org/downloads/point/last-month/%s" % name)
    if data is REFUSED or not isinstance(data, dict):
        return data
    inner = data.get(name)
    inner = inner if isinstance(inner, dict) else data
    val = inner.get("downloads")
    return val if isinstance(val, int) else None


def pypi_month(name, attempts=3):
    """PyPI downloads per month via shields.io, retrying a throttle."""
    for i in range(attempts):
        data = jget("https://img.shields.io/pypi/dm/%s.json" % name, timeout=25)
        if data is REFUSED:
            time.sleep(1.5 * (i + 1))
            continue
        if not isinstance(data, dict):
            return None  # no such project on PyPI: an absence
        message = data.get("message") or ""
        if "rate limited" in message:
            time.sleep(1.5 * (i + 1))
            continue
        return parse_human(message or data.get("value") or "")
    return REFUSED


def crates_month(name):
    """crates.io reports per-version per-day rows; sum them for one month."""
    data = jget("https://crates.io/api/v1/crates/%s/downloads" % name)
    if data is REFUSED or not isinstance(data, dict):
        return data
    rows = data.get("version_downloads")
    if not isinstance(rows, list):
        return None
    return sum(int(r.get("downloads") or 0) for r in rows)


REGISTRIES = (("npm", npm_month), ("pypi", pypi_month), ("crates", crates_month))


# --------------------------------------------------------------------------
# Ownership. A name match is not an identity.
#
# The first census credited 39,000,000 downloads/month to PostHog because the
# repository `PostHog/posthog` happens to be returned by a search for
# "agent session log", and 47 to `thought-machine/please` — the 2,616-star
# incumbent of the mature reproducible-build niche — because the unrelated npm
# package `please` belongs to `mrdrozdov/please`. Both attributions were wrong,
# and the second one is fatal: under-counting the leader is exactly what
# manufactures the hypothesis's result.
#
# Every registry publishes the repository a package came from, so a match is
# only counted when that repository is the GitHub project being measured.

REPO_IN_URL = re.compile(r"github\.com[:/]+([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?$")


def declared_repo(registry, name):
    """(owner, repo) the package metadata claims, or None."""
    if registry == "npm":
        data = jget("https://registry.npmjs.org/%s/latest" % name)
        url = (data or {}).get("repository") if isinstance(data, dict) else None
        url = url.get("url") if isinstance(url, dict) else url
    elif registry == "pypi":
        data = jget("https://pypi.org/pypi/%s/json" % name)
        info = (data or {}).get("info") if isinstance(data, dict) else None
        urls = (info or {}).get("project_urls") or {}
        url = (info or {}).get("home_page") or next(
            (v for v in urls.values() if "github.com" in (v or "")), None)
    else:
        data = jget("https://crates.io/api/v1/crates/%s" % name)
        url = (data or {}).get("crate", {}).get("repository") \
            if isinstance(data, dict) else None
    m = REPO_IN_URL.search((url or "").strip())
    return (m.group(1).lower(), m.group(2).lower()) if m else None


def owned_by(pair, full_name):
    """Does a package's declared repository belong to this GitHub project?

    Both sides are normalised here rather than assumed normalised: a case
    difference in a package's own metadata URL would otherwise be read as a
    different project, and the figure would be dropped for a spelling.
    `tests/test_census_stats.py` holds that case.
    """
    if not pair:
        return False
    owner, repo = full_name.split("/")[-2:]
    return (owner.lower(), repo.lower()) == (str(pair[0]).lower(),
                                             str(pair[1]).lower())


def npm_bulk(names):
    """One request per 100 packages. A name absent from the reply is unpublished."""
    out = {}
    for i in range(0, len(names), 100):
        chunk = [n for n in names[i:i + 100] if n]
        if not chunk:
            continue
        data = jget("https://api.npmjs.org/downloads/point/last-month/"
                    + ",".join(chunk))
        if data is REFUSED:
            for n in chunk:
                out[n] = REFUSED
        else:
            for n in chunk:
                got = data.get(n) if isinstance(data, dict) else None
                out[n] = got.get("downloads") if isinstance(got, dict) else None
        time.sleep(0.3)
    return out


def best_known(names, npm_cache, full_name):
    """(downloads, registry:package, refused, unverified) for one project.

    A figure counts only if the package's own metadata names this repository as
    its source. Unverified attributions are still returned, in `unverified`, so
    the record can see what was rejected rather than losing it silently.
    """
    best, where, refused, unverified = 0, "none", [], []
    for n in names:
        for reg, fn in REGISTRIES:
            val = npm_cache.get(n) if reg == "npm" else fn(n)
            if val is REFUSED:
                refused.append(reg)
            elif val and val > best:
                tag = "%s:%s" % (reg, n)
                if owned_by(declared_repo(reg, n), full_name):
                    best, where = val, tag
                else:
                    unverified.append(tag)
    return best, where, sorted(set(refused)), sorted(set(unverified))


def fill_all(rows, name_key="names"):
    """Attach usage_30d, usage_registry, usage_refused and usage_unverified."""
    npm_cache = npm_bulk(sorted({n for r in rows for n in r[name_key]}))

    def fill(r):
        value, where, refused, unverified = best_known(r[name_key], npm_cache,
                                                      r["full_name"])
        r["usage_30d"] = value
        r["usage_registry"] = where
        r["usage_refused"] = refused
        r["usage_unverified"] = unverified
        return r

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(fill, rows))
    return rows


def refusals(rows):
    """Projects with at least one registry that declined to answer."""
    return sum(1 for r in rows if r.get("usage_refused"))


def unverified_count(rows):
    """Projects where a non-zero figure was found but belonged to someone else."""
    return sum(1 for r in rows if r.get("usage_unverified"))
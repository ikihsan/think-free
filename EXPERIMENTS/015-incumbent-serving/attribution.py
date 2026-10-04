#!/usr/bin/env python3
"""Transport and attribution: the two things every channel in 015 shares.

Split out of `serving.py` at the 300-line cap, by invariant rather than by size:
`serving.py` is *what is measured*, this is *how a figure is read and whether it
belongs to the project being measured*. Every channel calls `jget` and
`declared_repo`, so a defect here is invisible as a per-channel bug.

**A refusal is never an absence.** `get` answers three ways on purpose: the body,
`None` for a genuine 404/400/422, and `REFUSED` for anything else. The hypothesis
under test predicts **low** numbers, and every instrument defect this repository
has found pushed measurements towards zero — the npm endpoint answering in two
shapes, shields.io answering HTTP 200 for a throttle, a package name matching a
repository it does not belong to (F032, three of them). So the direction that
flatters the result is the direction defects travel, and the code is built to make
that direction loud rather than quiet.

    python3 attribution.py
"""

import json
import re
import urllib.error
import urllib.request

UA = "origin-incumbent-serving/1 (think-free T-0060)"
REFUSED = "refused:upstream"


def get(url, timeout=30):
    """Body text, None for a genuine 404/400/422, REFUSED for anything else."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return None if e.code in (404, 400, 422) else REFUSED
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


REPO_IN_URL = re.compile(r"github\.com[:/]+([^/\s]+)/([^/\s#?]+?)(?:\.git)?/?$")


def declared_repo(url):
    """(owner, repo) a metadata URL claims, or None."""
    m = REPO_IN_URL.search((url or "").strip())
    return (m.group(1).lower(), m.group(2).lower()) if m else None


def owned_by(pair, full_name):
    """Is the claimed repository the project being measured? A name is not an identity.

    F032's fatal case: the npm package `please` belongs to `mrdrozdov/please`, so
    crediting its downloads to `thought-machine/please` -- the 2,616-star
    incumbent of a mature niche -- under-counts the very project that decides
    whether a niche is solved. Under-counting the leader manufactures the result.
    """
    if not pair:
        return False
    owner, repo = full_name.split("/")[-2:]
    return (owner.lower(), repo.lower()) == (str(pair[0]).lower(),
                                             str(pair[1]).lower())


def metadata_repo(registry, name):
    """The (owner, repo) a registry's own metadata claims for one package name."""
    if registry == "npm":
        data = jget("https://registry.npmjs.org/%s/latest" % name)
        url = (data or {}).get("repository") if isinstance(data, dict) else None
        url = url.get("url") if isinstance(url, dict) else url
        return declared_repo(url)
    if registry == "pypi":
        data = jget("https://pypi.org/pypi/%s/json" % name)
        info = (data or {}).get("info") if isinstance(data, dict) else None
        urls = (info or {}).get("project_urls") or {}
        url = (info or {}).get("home_page") or next(
            (v for v in urls.values() if "github.com" in (v or "")), None)
        return declared_repo(url)
    if registry == "brew":
        return brew_source_repo(name)
    data = jget("https://crates.io/api/v1/crates/%s" % name)
    url = (data or {}).get("crate", {}).get("repository") \
        if isinstance(data, dict) else None
    return declared_repo(url)


def brew_source_repo(name):
    """(owner, repo) the formula's own source tarball or homepage names.

    A Homebrew formula is attributed by the URL it downloads from, which is a
    stronger claim than a matching name: `ripgrep`'s stable URL carries
    `BurntSushi/ripgrep`, so a formula named `ripgrep` that downloads something
    else is refused rather than counted.
    """
    data = jget("https://formulae.brew.sh/api/formula/%s.json" % name, timeout=25)
    if not isinstance(data, dict):
        return None
    urls = data.get("urls") or {}
    stable = urls.get("stable") or {}
    for candidate in (stable.get("url"), (urls.get("head") or {}).get("url"),
                      data.get("homepage")):
        pair = declared_repo(candidate)
        if pair:
            return pair
    return None

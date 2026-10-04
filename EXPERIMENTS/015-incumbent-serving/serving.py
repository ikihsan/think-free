#!/usr/bin/env python3
"""Serving measurement: is the incumbent a prior-art screen names actually used?

A prior-art verdict says "a tool already serves this". The verdict has been
checked twice and neither check has read the property the verdict names:

  * F029 re-checked ten of them against a populated count -- GitHub stars, which
    T-0059 then measured to be uncorrelated with use in any niche, mature
    included (F032, `|rho| <= 0.35`);
  * T-0059 measured use through npm, PyPI and crates alone, and recorded that
    its **dead branch was never executable** because the mature arm's dominant
    incumbent, `thought-machine/please`, ships as a Bazel binary rather than a
    package. Zero measured installs was not zero users.

This module closes that branch. It adds two channels that do not need a registry
package, so a tool that ships a binary or a Homebrew bottle is visible:

  brew:<formula>     Homebrew's own analytics: installs in the last 30 days.
  ghreleases         GitHub release-asset `download_count`, summed over the
                     newest 100 releases. Same-repository, so attribution is not
                     a question. Cumulative, so it is kept in its own class.

Both channels have a cost that has to be stated where the number is read:
Homebrew counts `brew install` on macOS and Linuxbrew only, and release-asset
downloads include a project's own CI, dependabot, and Docker builds. A download
is closer to use than a star, and it is still not a user.

Three outcomes are kept apart, as in `../013-prior-art-predicts-adoption/usage.py`:
a number is measured, `None` means no channel of that name could be read, and
`REFUSED` means the upstream declined. A refusal is never zero, because the
hypothesis under test predicts low numbers and every defect in an instrument
pushes towards low.

    python3 serving.py --selfcheck
"""

import sys
import time

from attribution import REFUSED, jget, metadata_repo, owned_by


# ---------------------------------------------------------------- rate channels

def npm_month(name):
    """npm downloads in the last month. Accepts both response shapes."""
    data = jget("https://api.npmjs.org/downloads/point/last-month/%s" % name)
    if data is REFUSED or not isinstance(data, dict):
        return data
    inner = data.get(name)
    inner = inner if isinstance(inner, dict) else data
    val = inner.get("downloads")
    return val if isinstance(val, int) else None


def npm_bulk(names):
    """One request per 100 packages; a name absent from the reply is unpublished."""
    out = {}
    for i in range(0, len(names), 100):
        chunk = [n for n in names[i:i + 100] if n]
        if not chunk:
            continue
        data = jget("https://api.npmjs.org/downloads/point/last-month/" + ",".join(chunk))
        if data is REFUSED:
            for n in chunk:
                out[n] = REFUSED
        else:
            for n in chunk:
                got = data.get(n) if isinstance(data, dict) else None
                out[n] = got.get("downloads") if isinstance(got, dict) else None
        time.sleep(0.3)
    return out


def pypi_month(name, attempts=3):
    """PyPI downloads in the last month, via pypistats' own mirror of BigQuery.

    shields.io answers a throttle with HTTP 200 and a message that parses as a
    package with no downloads, so a body with a `message` and no number is a
    refusal and is retried rather than recorded as zero.
    """
    for i in range(attempts):
        data = jget("https://pypistats.org/api/packages/%s/recent" % name, timeout=25)
        if data is REFUSED:
            time.sleep(1.5 * (i + 1))
            continue
        if not isinstance(data, dict):
            return None            # no such project: an absence
        block = data.get("data")
        if not isinstance(block, dict):
            return None
        val = block.get("last_month")
        if isinstance(val, int):
            return val
        time.sleep(1.5 * (i + 1))
    return REFUSED


def crates_month(name):
    """crates.io reports per-version per-day rows; sum them."""
    data = jget("https://crates.io/api/v1/crates/%s/downloads" % name)
    if data is REFUSED or not isinstance(data, dict):
        return data
    rows = data.get("version_downloads")
    if not isinstance(rows, list):
        return None
    return sum(int(r.get("downloads") or 0) for r in rows)


def brew_30d(name):
    """Homebrew's own install analytics: installs in the last 30 days."""
    data = jget("https://formulae.brew.sh/api/formula/%s.json" % name, timeout=25)
    if data is REFUSED or not isinstance(data, dict):
        return data
    install = ((data.get("analytics") or {}).get("install") or {})
    row = install.get("30d")
    if not isinstance(row, dict):
        return None
    total = sum(v for k, v in row.items() if k == name)
    return total or None


# ---------------------------------------------------------- cumulative channels

def release_downloads(full_name, pages=1):
    """Sum of release-asset downloads over the newest releases of this repository."""
    total, releases, assets = 0, 0, 0
    for page in range(1, pages + 1):
        data = jget("https://api.github.com/repos/%s/releases?per_page=100&page=%d"
                    % (full_name, page), timeout=30)
        if data is REFUSED:
            return REFUSED
        if not isinstance(data, list):
            return total if releases else None
        if not data:
            break
        for rel in data:
            releases += 1
            for a in rel.get("assets") or []:
                assets += 1
                dc = a.get("download_count")
                if isinstance(dc, int):
                    total += dc
        if len(data) < 100:
            break
        time.sleep(0.5)
    return {"downloads": total, "releases": releases, "assets": assets}


def docker_pulls(full_name):
    """Docker Hub pull count, where the image name matches the repository name."""
    owner, repo = full_name.split("/")[-2:]
    for namespace, name in ((owner.lower(), repo.lower()), ("library", repo.lower())):
        data = jget("https://hub.docker.com/v2/repositories/%s/%s/" % (namespace, name),
                    timeout=25)
        if data is REFUSED:
            return REFUSED
        if isinstance(data, dict) and isinstance(data.get("pull_count"), int):
            return data["pull_count"]
    return None


# ------------------------------------------------------------------- name guesses

def guesses(full_name):
    """Mechanical package-name guesses from a repository name. No taste, and lossy.

    A wrong guess yields an absence, which biases the measurement towards "not
    served", so the caller records `guessed` and the README states the bias. The
    two guess-free channels (Homebrew and release assets) exist for this reason.
    """
    repo = full_name.split("/")[-1]
    out = [repo, repo.lower()]
    for suffix in ("-cli", "-rs", "-py", "-js", "-tool", "-tui", "-app", "-server"):
        if repo.endswith(suffix) and len(repo) > len(suffix) + 2:
            out.append(repo[:-len(suffix)])
    seen, uniq = set(), []
    for n in out:
        if n and n not in seen:
            seen.add(n)
            uniq.append(n)
    return uniq


RATE_CHANNELS = (("npm", npm_month), ("pypi", pypi_month), ("crates", crates_month))


def measure(full_name, npm_cache=None, releases=True):
    """Every serving figure for one project, each attribution verified.

    Returns a dict with `rate`, `cumulative`, `refused`, `unverified` and
    `guessed`, so a reader can see which figures were unverifiable attributions
    rather than only the ones that counted.
    """
    names = guesses(full_name)
    cache = npm_cache if npm_cache is not None else npm_bulk(names)
    rate, refused, unverified, checked = [], [], [], []

    for name in names:
        checked.append(name)
        for reg, fn in RATE_CHANNELS:
            val = cache.get(name) if reg == "npm" else fn(name)
            tag = "%s:%s" % (reg, name)
            if val is REFUSED:
                refused.append(tag)
            elif isinstance(val, int) and val >= 0:
                pair = declared_repo_for(reg, name)
                if owned_by(pair, full_name):
                    # A verified zero is recorded, not dropped. It is a reading of
                    # this project's use, and hiding it would turn "the registry
                    # answered zero" into "the instrument read nothing" -- which
                    # would flatter the hypothesis under test.
                    rate.append({"channel": tag, "value": val})
                else:
                    unverified.append(tag)

    brew_val = brew_30d(names[0])
    if brew_val is REFUSED:
        refused.append("brew:%s" % names[0])
    elif isinstance(brew_val, int):
        tag = "brew:%s" % names[0]
        if owned_by(metadata_repo("brew", names[0]), full_name):
            rate.append({"channel": tag, "value": brew_val})
        else:
            unverified.append(tag)

    cumulative = []
    if releases:
        rel = release_downloads(full_name)
        if rel is REFUSED:
            refused.append("ghreleases")
        elif isinstance(rel, dict) and rel.get("assets"):
            cumulative.append({"channel": "ghreleases", "value": rel["downloads"],
                               "assets": rel["assets"], "releases": rel["releases"]})
        else:
            # No release assets published: a reading, and the only one this channel
            # can give. It is recorded so the row is decided rather than undecided.
            cumulative.append({"channel": "ghreleases", "value": 0, "assets": 0,
                               "releases": 0})
    pulls = docker_pulls(full_name)
    if pulls is REFUSED:
        refused.append("dockerpulls")
    elif isinstance(pulls, int) and pulls > 0:
        cumulative.append({"channel": "dockerpulls", "value": pulls})

    return {"repo": full_name, "guessed": checked, "rate": rate, "cumulative": cumulative,
            "refused": sorted(set(refused)), "unverified": sorted(set(unverified))}


def declared_repo_for(registry, name):
    """Kept as the local name because it reads better at the call site."""
    return metadata_repo(registry, name)


if __name__ == "__main__":
    # The instrument's own known-answer cases live in `selfcheck.py`, because they
    # are a falsification of the channels above rather than another channel. The
    # floors they check against live in `verdict.py`, the file whose invariant is
    # deciding whether a figure counts.
    import selfcheck

    sys.exit(1 if selfcheck.run() else 0)

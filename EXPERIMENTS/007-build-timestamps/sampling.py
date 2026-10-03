"""Which wheels the E3 census looks at.

Sampling is separated from measurement because the two fail differently: a
selection rule that silently changed the population would invalidate the whole
result, while an inspection bug would affect one artifact. Keeping them apart
makes "what population was this?" answerable without reading the zip code.

Standard library only. Driven by `census.py`; not meant to be run directly.
"""

from __future__ import annotations

import json
import urllib.request

API = "https://pypi.org/pypi/{name}/json"
WHEELS_PER_PACKAGE = 20
TARGET_WHEELS = 200
MAX_DEPTH = 40
USER_AGENT = "think-free-e3-census/1.0 (+repository evidence experiment)"
PACKAGES = (
    "requests", "numpy", "urllib3", "setuptools", "six",
    "boto3", "click", "jinja2", "pyyaml", "cryptography",
)


def fetch(url: str, timeout: int = 60) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def recent_wheels(name: str, count: int) -> list[dict]:
    """Up to `count` wheels for a package, most recently uploaded first.

    Upload time comes from the release's own file entries, so "recent" is
    measured rather than assumed from version ordering: a patch release can
    predate a feature release. Releases are consumed newest-first, and a
    release contributing more than one wheel contributes only its smallest, so
    the sample is not dominated by platform variants of one build.

    "Smallest" is applied explicitly. Taking whichever wheel the index happens
    to list first would silently make the sample a function of JSON key order,
    and the resulting byte total would not be the bounded one the rule exists
    to produce. Ties on size break on filename so the selection is reproducible.
    """
    payload = json.loads(fetch(API.format(name=name)))
    by_version: dict[str, list[dict]] = {}
    for version, files in payload.get("releases", {}).items():
        for entry in files:
            if entry.get("packagetype") != "bdist_wheel":
                continue
            stamp = entry.get("upload_time_iso_8601") or entry.get("upload_time")
            if not stamp:
                continue
            by_version.setdefault(version, []).append({
                "package": name,
                "version": version,
                "filename": entry["filename"],
                "url": entry["url"],
                "size": entry.get("size", 0),
                "upload_time": stamp,
            })
    ranked = [
        # A release's recency is its newest upload, so a partially re-uploaded
        # release is ranked by the wheel that is actually current.
        (max(wheel["upload_time"] for wheel in wheels),
         min(wheels, key=lambda wheel: (wheel["size"], wheel["filename"])))
        for wheels in by_version.values()
    ]
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    return [meta for _, meta in ranked[:count]]


def build_sample() -> tuple[list[dict], list[dict]]:
    """Select `TARGET_WHEELS` wheels, then fill any shortfall from deeper history.

    A package that ships fewer than `WHEELS_PER_PACKAGE` recent wheel releases
    must not shrink the sample below the stated 200, so the shortfall is taken
    from the next-most-recent releases of the same packages rather than from an
    eleventh package, which would change the population mid-measurement.
    """
    per_package = {name: recent_wheels(name, WHEELS_PER_PACKAGE) for name in PACKAGES}
    failures = [
        {"package": name, "error": "index resolved but produced no wheels"}
        for name, rows in per_package.items() if not rows
    ]
    selected = [meta for name in PACKAGES for meta in per_package[name]]
    # Releases are per-project: "2.4.0" is a different release in urllib3 and in
    # cryptography, so the key carries the package.
    taken_releases = {(meta["package"], meta["version"]) for meta in selected}
    taken_urls = {meta["url"] for meta in selected}
    depth = {name: WHEELS_PER_PACKAGE for name in PACKAGES}
    while len(selected) < TARGET_WHEELS and any(
        depth[name] < MAX_DEPTH for name in PACKAGES
    ):
        added = 0
        for name in PACKAGES:
            if len(selected) >= TARGET_WHEELS:
                break
            if depth[name] >= MAX_DEPTH:
                continue
            depth[name] += 1
            # One wheel per release, enforced here too. Comparing URLs alone
            # lets a release already in the sample contribute a second platform
            # variant through the top-up path, so the sample would quietly hold
            # fewer releases than its rule claims.
            for meta in recent_wheels(name, depth[name])[-1:]:
                release = (meta["package"], meta["version"])
                if release in taken_releases or meta["url"] in taken_urls:
                    continue
                selected.append(meta)
                taken_releases.add(release)
                taken_urls.add(meta["url"])
                added += 1
        if not added:
            break
    return selected, failures



"""Sdist fetching and parsing for apidiff."""

from __future__ import annotations

import io
import json
import re
import tarfile
import urllib.request
from pathlib import Path


def pypi_json(package: str) -> dict:
    url = f"https://pypi.org/pypi/{package}/json"
    req = urllib.request.Request(url, headers={"User-Agent": "apidiff/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def sdist_url(meta: dict, version: str) -> str | None:
    files = meta.get("releases", {}).get(version) or []
    for entry in files:
        if entry.get("packagetype") == "sdist":
            return entry.get("url")
    return None


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "apidiff/0.1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def sdist_package_dirs(blob: bytes) -> list[str]:
    """Top-level import package directories inside an sdist.

    A directory counts when it holds an `__init__.py` and sits at
    depth 1 or 2 (the sdist root, or under `lib`/`src`/`lib3`).
    Test and doc trees are excluded by name.
    """
    names: set[str] = set()
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile()]
    for member in members:
        member.name = member.name.lstrip("./")
        parts = member.name.split("/")
        if len(parts) < 2:
            continue
        if parts[-1] != "__init__.py" or len(parts) not in (3, 4):
            continue
        if parts[-2].lower() in {"tests", "test", "docs", "doc", "examples"}:
            continue
        names.add("/".join(parts[1:-1]))
    return sorted(names)


def sdist_modules(blob: bytes) -> dict[str, str]:
    """{module_name: source} for every .py file under the packages.

    A file is included when it sits under one of the package
    directories `sdist_package_dirs` found, or is a top-level
    single-file module whose stem matches the distribution name
    (`six.py` in `six-1.16.0`). Test, doc and example trees are
    excluded by path component, as are build files like `setup.py`.
    """
    packages = set(sdist_package_dirs(blob))
    modules: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile() or not member.name.endswith(".py"):
                continue
            parts = member.name.lstrip("./").split("/")
            if len(parts) == 2:
                stem = parts[1][:-3]
                dist = re.sub(r"[-_]\d+\..*$", "", parts[0]).lower()
                if stem.lower() != dist:
                    continue
                module = stem
            else:
                under = "/".join(parts[1:])
                segments = under.split("/")
                if segments[0] not in packages:
                    continue
                if any(seg.lower() in {"tests", "test", "docs", "doc",
                                         "examples"} for seg in segments[1:]):
                    continue
                module = under[:-3] if not under.endswith("/__init__.py") \
                    else under.rsplit("/", 1)[0]
            data = tar.extractfile(member)
            if data is None:
                continue
            modules[module] = data.read().decode("utf-8", errors="replace")
    return modules
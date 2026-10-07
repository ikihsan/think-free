#!/usr/bin/env python3
"""E049 lockfile-format parsers, with the population rules E050
added after its first run's instrument defects.

Defects found by the first E050 run (all four "absent" hits were
artifacts, not registry facts):

1. pip-style requirements write extras in the name
   (`coverage[toml]==7.10.6`); the `[extras]` suffix is not part
   of the PyPI name.
2. A project's own uv.lock carries itself as an editable package
   (`source = { editable = "." }`, e.g. `flask 3.2.0.dev0`);
   that version was never on the registry, so it is not an
   absence.
3. poetry.lock carries workspace/git dependencies under
   `[package.source] type = "git"` (e.g. poetry's own
   `poetry-core`); same exclusion.

Population rule, per format:
- uv.lock:      only `[[package]]` blocks whose `source = {...}`
                names a registry.
- poetry.lock:  only `[[package]]` blocks with no `[package.source]`
                section (Poetry's default source is PyPI).
- requirements: `name==version` lines, `[extras]` stripped.

Each parser returns (pairs, excluded) so the excluded count is
reported, not silently dropped.
"""
import re
from pathlib import Path

NAME = re.compile(r'^\s*name\s*=\s*"([^"]+)"')
VER = re.compile(r'^\s*version\s*=\s*"([^"]+)"')
URL = re.compile(r'url\s*=\s*"([^"]+)"')


def _bare(name):
    return name.split("[", 1)[0].strip()


def entries_uvlock(text):
    """uv.lock: registry-sourced packages only."""
    pairs, excluded = set(), 0
    name = ver = None
    registry = False
    for line in text.splitlines():
        if line.startswith("[[package]]"):
            if name is not None and ver is not None:
                if registry:
                    pairs.add((_bare(name), ver))
                else:
                    excluded += 1
            name = ver = None
            registry = False
        m = NAME.match(line)
        if m:
            name = _bare(m.group(1))
        m = VER.match(line)
        if m:
            ver = m.group(1)
        if line.strip().startswith("source = {"):
            registry = "registry" in line
    if name is not None and ver is not None:
        if registry:
            pairs.add((name, ver))
        else:
            excluded += 1
    return pairs, excluded


def entries_poetrylock(text):
    """poetry.lock: packages with no [package.source] section."""
    pairs, excluded = set(), 0
    name = ver = None
    has_source = False
    for line in text.splitlines():
        if line.startswith("[[package]]"):
            if name is not None and ver is not None:
                if has_source:
                    excluded += 1
                else:
                    pairs.add((_bare(name), ver))
            name = ver = None
            has_source = False
        m = NAME.match(line)
        if m:
            name = _bare(m.group(1))
        m = VER.match(line)
        if m:
            ver = m.group(1)
        if line.strip() == "[package.source]":
            has_source = True
    if name is not None and ver is not None:
        if has_source:
            excluded += 1
        else:
            pairs.add((name, ver))
    return pairs, excluded


def entries_pipstyle(text):
    """pip requirements: name==version, extras stripped."""
    pairs = set()
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "-", "[")) and "==" in line:
            spec = line.split(" ;")[0].split("#")[0].strip()
            name, _, ver = spec.partition("==")
            pairs.add((_bare(name), ver.strip()))
    return pairs, 0


def parse_pairs(path, text):
    """Dispatch on the lockfile format the path names.

    `path` is the path inside the source repository (the
    snapshot files on disk are renamed `<repo>_old.txt`,
    so the format is not in their suffix)."""
    if path.endswith("uv.lock"):
        return entries_uvlock(text)
    if path.endswith("poetry.lock"):
        return entries_poetrylock(text)
    return entries_pipstyle(text)


def parse_urls(text):
    """Every artifact URL a lockfile recorded."""
    return set(URL.findall(text))


# (snapshot file, the repo path it was fetched from)
SNAPSHOTS = [
    ("encode_httpx_old.txt", "requirements.txt"),
    ("python-poetry_poetry_old.txt", "poetry.lock"),
    ("pallets_flask_old.txt", "uv.lock"),
    ("encode_starlette_old.txt", "uv.lock"),
    ("tornadoweb_tornado_old.txt", "requirements.txt"),
    ("urllib3_urllib3_old.txt", "uv.lock"),
    ("encode_uvicorn_old.txt", "uv.lock"),
    ("samuelcolvin_pydantic_old.txt", "uv.lock"),
    ("pallets_werkzeug_old.txt", "uv.lock"),
    ("scrapy_scrapy_old.txt", "docs/requirements.txt"),
]


def snapshot_names():
    """The ten PyPI-ecosystem old snapshots, and the six
    uv.lock files whose recorded artifact URLs Q2 checks.
    ruff's Cargo.lock is a different registry (crates.io)
    and is out of scope."""
    root = Path(__file__).resolve().parent.parent / "049-lockfile-closure" / "raw"
    pip = [(f, p) for f, p in SNAPSHOTS]
    uv = [(f, p) for f, p in SNAPSHOTS if p == "uv.lock"]
    return root, pip, uv

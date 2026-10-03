"""Fetch and pin the sdists T-0017 builds from.

Kept apart from `attribute.py` for the reason `sampling.py` exists in
`007-build-timestamps`: a selection rule that silently changes the population
invalidates the result, while an inspection bug affects one artifact. Every
input's URL, size and SHA-256 is written to `sources.json` so the sample is
checkable without re-running the build.

Standard library only. Driven by `attribute.py`; also runnable on its own.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES_JSON = os.path.join(HERE, "sources.json")
SDIST_DIR = os.path.join(HERE, "sdists")

# Selection rule, fixed before the run: pure-Python sdists with a classic
# `setup.py`, a static version (no VCS-derived version, which would need git and
# a build-time network), and a small artifact. Four is the number the kill gate
# is written against: "at least 3 of 4", so one source may fail to build without
# collapsing the gate.
SOURCES = (
    ("six", "1.16.0"),
    ("toml", "0.10.2"),
    ("idna", "3.3"),
    ("packaging", "21.3"),
    ("click", "8.1.7"),
)


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(name: str, version: str) -> dict | None:
    """Fetch one sdist with pip, or return None when it cannot be fetched.

    A source that will not download is recorded as absent rather than skipped
    silently: the gate is written over "at least 3 of 4 sources", so a missing
    input has to be visible to whoever reads the result.
    """
    os.makedirs(SDIST_DIR, exist_ok=True)
    command = [
        sys.executable, "-m", "pip", "download",
        "--no-deps", "--no-binary", ":all:", "--no-build-isolation",
        "--disable-pip-version-check", "--no-cache-dir",
        "--dest", SDIST_DIR,
        f"{name}=={version}",
    ]
    done = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if done.returncode != 0:
        return {
            "package": name,
            "version": version,
            "error": (done.stderr.strip().splitlines() or ["unknown"])[-1][:300],
        }
    expected = f"{name}-{version}.tar.gz"
    path = os.path.join(SDIST_DIR, expected)
    if not os.path.exists(path):
        return {"package": name, "version": version,
                "error": f"pip exited 0 but {expected} is absent"}
    return {
        "package": name,
        "version": version,
        "file": os.path.basename(path),
        "bytes": os.path.getsize(path),
        "sha256": sha256(path),
        "source": f"https://pypi.org/pypi/{name}/{version}/json",
    }


def main() -> int:
    rows = [download(name, version) for name, version in SOURCES]
    payload = {
        "selection_rule": (
            "Pure-Python sdists with a classic setup.py, a static version, and a "
            "small artifact. Five were named and all five are attempted; the kill "
            "gate is written over 'at least 3 of 4 sources', so one source may "
            "fail without collapsing it."
        ),
        "fetched_at": None,
        "pip": subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True,
        ).stdout.strip(),
        "sources": rows,
    }
    with open(SOURCES_JSON, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    ok = [row for row in rows if row and "sha256" in row]
    print(f"fetched {len(ok)} of {len(rows)} sources -> {SOURCES_JSON}")
    for row in rows:
        if row and "sha256" in row:
            print(f"  {row['file']:34s} {row['bytes']:>9d} bytes  {row['sha256'][:16]}")
        else:
            print(f"  {row.get('package')}: {row.get('error')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
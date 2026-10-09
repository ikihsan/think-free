#!/usr/bin/env python3
"""E069 paths, environment and target-interpreter constants.

Split out of `harness.py` on 2026-10-09 when that file passed the 300-line cap.
The install machinery (`venvinstall.py`) needs these values and `harness.py`
needs its functions; putting the shared constants here is what keeps that
relationship a one-way import instead of a cycle.

Stdlib only. Python 3.8+.
"""

import os
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent.parent
E068 = REPO_ROOT / "EXPERIMENTS" / "068-arxiv-spec-generator"
REPOS = E068 / "repos"
GEN_SPECS = E068 / "cache" / "generated_specs"
EXTRACTED = E068 / "cache" / "extracted.json"
MANIFEST = BASE / "repos" / "MANIFEST.json"
VENV_PARENT = Path(os.environ.get("E069_VENV_ROOT", "/tmp/opencode/e069-venvs"))
GETPIP = VENV_PARENT / "get-pip-3.8.py"
GETPIP_URL = "https://bootstrap.pypa.io/pip/3.8/get-pip.py"

# E069's target interpreter, and the one E068 resolved its pins against. Recorded
# in results.json; the VM's own 3.8.10 is deliberately not the arms' interpreter.
BASE_PYTHON_VERSION = "3.10.19"
# Resolved at import time. E068 resolved every pin against 3.10, so testing its
# output on any other interpreter would measure the mismatch rather than the
# mechanism. Prefer an interpreter already present at that version, otherwise
# fetch a standalone CPython with `uv python install`. Override with E069_PYTHON.


def _find_base_python():
    """Absolute path of a CPython at BASE_PYTHON_VERSION, fetched if needed."""
    import glob
    import shutil as _shutil
    import subprocess as _subprocess

    def _at_version(exe):
        try:
            out = _subprocess.run([exe, "-c", "import sys;print(sys.version.split()[0])"],
                                  capture_output=True, text=True, timeout=60).stdout.strip()
        except (OSError, _subprocess.SubprocessError):
            return False
        return out == BASE_PYTHON_VERSION

    if BASE_PYTHON_VERSION:
        found = _shutil.which("python%s" % BASE_PYTHON_VERSION)
        if found and _at_version(found):
            return found
        for pattern in ("~/.local/share/uv/python/cpython-%s-*/bin/python%s"
                        % (BASE_PYTHON_VERSION, BASE_PYTHON_VERSION),
                        "~/.local/share/uv/python/cpython-%s-*/bin/python3"
                        % BASE_PYTHON_VERSION):
            for path in sorted(glob.glob(os.path.expanduser(pattern))):
                if _at_version(path):
                    return path
    if _shutil.which("uv"):
        try:
            _subprocess.run(["uv", "python", "install", BASE_PYTHON_VERSION],
                            capture_output=True, text=True, timeout=900, check=False)
        except (OSError, _subprocess.SubprocessError):
            pass
        for pattern in ("~/.local/share/uv/python/cpython-%s-*/bin/python%s"
                        % (BASE_PYTHON_VERSION, BASE_PYTHON_VERSION),
                        "~/.local/share/uv/python/cpython-%s-*/bin/python3"
                        % BASE_PYTHON_VERSION):
            for path in sorted(glob.glob(os.path.expanduser(pattern))):
                if _at_version(path):
                    return path
    fallback = _shutil.which("python3") or sys.executable
    return fallback


BASE_PYTHON = os.environ.get("E069_PYTHON") or _find_base_python()

# pip's own wall-clock ceiling for one arm. Exceeding it returns exit `None`,
# which is a missing observation and never a failed install — see analyze.py.
PIP_TIMEOUT = int(os.environ.get("E069_PIP_TIMEOUT", "1800"))
REPO_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
#!/usr/bin/env python3
"""E047 — what actually ran, read from disk rather than remembered.

Split out of `harness.py` at the 300-line cap, by invariant: this is the
provenance of the result, and it is read from the files `setup.sh` wrote and from
the binaries themselves, so a result can be tied to the artifacts that produced
it rather than to the operator's account of them.

Two entries here exist because the first draft of this file got them wrong:

- `git_used` and `git_on_path` are both recorded, and they differ. The arms ran on
  a git built from source; the VM's own git is older than the minimum two of the
  runners enforce, so recording only the one on `PATH` read as though lefthook and
  lint-staged had been measured on a version they refuse to start on.
- the sha256 of every fetched tarball is recorded, so a number in
  `raw/results.json` traces to specific bytes.
"""

import os
import subprocess

from gitenv import ROOT, git_bin


def read_versions():
    versions = {}
    for name, path in (
        ("lefthook", "logs/lefthook.version"),
        ("pre-commit", "logs/pre-commit.version"),
        ("node", "logs/node.version"),
        ("lint-staged", "logs/lint-staged.version"),
        ("husky", "logs/husky.version"),
        ("prettier", "logs/prettier.version"),
    ):
        full = os.path.join(ROOT, path)
        versions[name] = open(full).read().strip() if os.path.exists(full) else None
    for name, path in (("lefthook.sha256", "logs/lefthook.sha256"),
                       ("node.sha256", "logs/node.sha256"),
                       ("python.sha256", "logs/python.sha256"),
                       ("git.sha256", "logs/git.sha256")):
        full = os.path.join(ROOT, path)
        versions[name] = open(full).read().split()[0] if os.path.exists(full) else None
    # The git that actually ran every arm, not the one on this VM's PATH. The
    # first draft recorded the system git here, which read as though lefthook
    # and lint-staged had been measured on 2.25.1 — the version both refuse to
    # start on.
    try:
        versions["git_used"] = subprocess.run(
            [git_bin(), "--version"], capture_output=True, text=True).stdout.strip()
    except Exception:
        versions["git_used"] = None
    try:
        versions["git_on_path"] = subprocess.run(
            ["git", "--version"], capture_output=True, text=True).stdout.strip()
    except Exception:
        versions["git_on_path"] = None
    versions["python_used"] = read_version_file("python.version")
    return versions


def read_version_file(name):
    full = os.path.join(ROOT, "logs", name)
    if os.path.exists(full):
        return open(full).read().strip()
    try:
        return subprocess.run([os.path.join(ROOT, "py", "bin", "python3"),
                               "--version"], capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return None

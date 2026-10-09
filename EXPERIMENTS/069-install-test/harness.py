#!/usr/bin/env python3
"""E069 install-test harness.

Three arms per repository, one fresh virtualenv each:
  GEN   E068's generated pinned requirements.txt, as committed
  DECL  the repository's own declared spec, as shipped
  NONE  no install, repository source tree only

The oracle has two parts, both recorded: pip's exit code, and whether every
top-level module the repository imports (that is neither stdlib, nor
first-party, nor named in the arm's spec) actually imports afterwards.

Stdlib only. Python 3.8+.
"""

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Paths, environment and the target interpreter live in config.py; the install
# machinery (virtualenvs, pip, the import oracle) lives in venvinstall.py. Both
# were split out of this file on 2026-10-09 at the 300-line cap.
from config import (BASE, REPO_ROOT, E068, REPOS, GEN_SPECS, EXTRACTED,
                     MANIFEST, VENV_PARENT, GETPIP, GETPIP_URL,
                     BASE_PYTHON, BASE_PYTHON_VERSION, PIP_TIMEOUT, REPO_SLUG_RE)


# ---------------------------------------------------------------- stdlib module set

def stdlib_names():
    """Top-level module names the running interpreter provides."""
    names = set(getattr(sys, "stdlib_module_names", ()))  # 3.10+
    if not names:
        # 3.8: derive from the stdlib directory listing plus a fixed floor.
        stdlib_dir = Path(sys.base_prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}"
        for path in stdlib_dir.glob("*.py"):
            names.add(path.stem)
        for path in stdlib_dir.iterdir():
            if path.is_dir() and not path.name.startswith(("__", "site-packages", "lib-dynload", "dist-packages")):
                names.add(path.name)
        names.update(sys.builtin_module_names)
    return names


# ---------------------------------------------------------------- repo facts

def load_manifest():
    data = json.loads(MANIFEST.read_text())
    out = []
    for row in data["repos"]:
        key = "%s/%s" % (row["owner"], row["repo"])
        out.append((key, row))
    return out


def extracted_index():
    data = json.loads(EXTRACTED.read_text())
    idx = {}
    for row in data["a1_repos"] + data["test_repos"]:
        idx["%s/%s" % (row["owner"], row["repo"])] = row
    return idx


def gen_spec_path(key, arm):
    owner, repo = key.split("/")
    return GEN_SPECS / ("%s_%s_%s.txt" % (arm, owner, repo))


def first_existing(repo_dir, *names):
    for name in names:
        for hit in sorted(repo_dir.glob(name)):
            if hit.is_file():
                return hit
    return None


def decl_spec(repo_dir):
    """The repository's own dependency declaration, installed the way a person would.

    `requirements*.txt` is installed with `-r`. A `pyproject.toml` or `setup.py`
    is a build file, not a requirement list: pip reads it when asked to install
    the directory, and that is the command a person actually types. Declaring
    DECL as "skip repos with a pyproject" would weaken the incumbent arm on
    exactly the repos where it is strongest.
    """
    req = first_existing(repo_dir, "requirements*.txt", "requirement*.txt")
    if req is not None:
        return {"mode": "requirements", "path": str(req)}, "requirements"
    pyproject = repo_dir / "pyproject.toml"
    if pyproject.is_file():
        return {"mode": "install_dir", "path": str(repo_dir)}, "pyproject"
    setup = repo_dir / "setup.py"
    if setup.is_file():
        return {"mode": "install_dir", "path": str(repo_dir)}, "setup.py"
    return None, None


def first_party(repo_dir):
    """Top-level directories in the repo that shadow an import name."""
    out = set()
    for child in repo_dir.iterdir():
        if child.is_dir() and not child.name.startswith(".") and child.name not in ("__pycache__",):
            out.add(child.name)
        elif child.is_file() and child.suffix == ".py":
            out.add(child.stem)
    return out


# The install machinery (virtualenvs, pip, the import oracle) lives in
# venvinstall.py, split out on 2026-10-09 at the 300-line cap. Re-exported
# here so every existing `harness.<name>` call site keeps working.
from venvinstall import (  # noqa: E402,F401
    classify_failure, ensure_getpip, install, make_venv, needed_modules,
    probe_imports, run, spec_names, venv_root,
)

# ---------------------------------------------------------------- arms

def _on_rmtree_error(func, path, exc):
    """Make a read-only file writable and retry; pip writes some that way.

    `shutil.rmtree(ignore_errors=True)` hid this: it swallowed the failure and
    the venv stayed. 17 GB of torch wheels accumulated across 14 repositories
    and the run had to be stopped at 88% disk, with 6 of 20 repositories
    unmeasured. The removal now reports, and a removal that fails aborts the
    arm rather than quietly costing the next one its disk.
    """
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
        func(path)
    except Exception:
        raise


def discard_venv(bin_path):
    """Remove a venv after its arm is measured, and report whether it went.

    18 of 20 specs carry torch, and one measured venv reaches 7 GB. Leaving
    every venv on disk exhausts this VM partway through the population, and a
    run that dies at repository 14 is a run with no denominator.
    """
    path = Path(bin_path).parent
    shutil.rmtree(path, onerror=_on_rmtree_error)
    removed = not path.exists()
    if not removed:
        raise RuntimeError("venv %s survived removal; refusing to measure the next arm "
                           "without disk for it" % path)
    return True


def run_arm(key, row, arm, repo_dir, stdlib):
    firstparty = first_party(repo_dir)
    record = {"arm": arm, "repo": key}
    venv_name = "%s__%s" % (key.replace("/", "_"), arm)

    if arm == "GEN":
        path = gen_spec_path(key, row["arm"])
        if not path.is_file():
            record["skipped"] = "no generated spec on disk"
            return record
        spec = {"mode": "requirements", "path": str(path)}
    elif arm == "DECL":
        spec, kind = decl_spec(repo_dir)
        if spec is None:
            record["skipped"] = "no declared spec in repository"
            return record
        record["decl_kind"] = kind
    else:
        spec = None

    bin_path = make_venv(venv_root() / venv_name)
    record["venv_python"] = str(bin_path)
    needed = needed_modules(row, stdlib, firstparty, spec_names(spec))
    record["needed"] = needed

    if spec is None:
        record["install"] = {"spec": None, "exit": 0, "detail": "no spec installed (NONE arm)"}
    else:
        record["install"] = install(bin_path, spec, repo_dir)
        if record["install"]["exit"] != 0:
            record["imports"] = {"__skipped__": "install failed"}
            record["working"] = False
            record["venv_removed"] = discard_venv(bin_path)
            return record

    if not needed:
        record["imports"] = {}
        record["working"] = None
        record["note"] = "no third-party import to probe; install result only"
        record["venv_removed"] = discard_venv(bin_path)
        return record
    record["needed"] = needed
    record["imports"] = probe_imports(bin_path, repo_dir, needed)
    record["working"] = all(v == "ok" for v in record["imports"].values())
    record["venv_removed"] = discard_venv(bin_path)
    return record


# ---------------------------------------------------------------- main

def interpreter_record():
    proc = subprocess.run([BASE_PYTHON, "-c",
                           "import sys,platform;print(sys.version.split()[0], platform.machine())"],
                          capture_output=True, text=True)
    version, machine = (proc.stdout.split() + ["?", "?"])[:2]
    getpip_sha = ""
    if GETPIP.exists():
        import hashlib
        getpip_sha = hashlib.sha256(GETPIP.read_bytes()).hexdigest()
    return {
        "path": BASE_PYTHON,
        "expected": BASE_PYTHON_VERSION,
        "observed_version": version,
        "machine": machine,
        "getpip_url": GETPIP_URL,
        "getpip_sha256": getpip_sha,
    }


def main():
    VENV_PARENT.mkdir(parents=True, exist_ok=True)
    ensure_getpip()
    stdlib = stdlib_names()
    rows = extracted_index()
    manifest = load_manifest()
    arms = os.environ.get("E069_ARMS", "GEN,DECL,NONE").split(",")
    only = os.environ.get("E069_ONLY", "").strip()
    # A per-repository raw file is written as each repository finishes, so an
    # interrupted run resumes at the next repository instead of re-downloading
    # every torch wheel it already measured. Set E069_FRESH=1 to measure again.
    fresh = os.environ.get("E069_FRESH", "") not in ("", "0", "no", "false")
    (BASE / "raw").mkdir(exist_ok=True)
    out = []
    for key, mrow in manifest:
        row = rows.get(key)
        if row is None:
            continue
        if only and only not in key:
            continue
        repo_dir = REPO_ROOT / mrow["path"]
        if not repo_dir.is_dir():
            out.append({"repo": key, "error": "missing checkout at %s" % mrow["path"]})
            continue
        done_file = BASE / "raw" / ("%s.json" % key.replace("/", "_"))
        if done_file.is_file() and not fresh:
            cached = json.loads(done_file.read_text())
            if {r.get("arm") for r in cached} >= set(arms):
                out.extend(cached)
                print("=== %s (%s)  cached, %d arms reused" % (key, row["arm"], len(cached)),
                      flush=True)
                continue
        print("=== %s (%s)" % (key, row["arm"]), flush=True)
        for arm in arms:
            if arm == "NONE":
                rec = run_arm(key, row, "NONE", repo_dir, stdlib)
            else:
                rec = run_arm(key, row, arm, repo_dir, stdlib)
            print("    %-5s %s" % (arm, rec.get("skipped") or (
                "install_exit=%s working=%s" % (rec.get("install", {}).get("exit"), rec.get("working"))
            )), flush=True)
            out.append(rec)
        # One file per repository, holding only that repository's arms, so a
        # resumed run reuses it and a partially measured repository is redone.
        done_file.write_text(json.dumps(out[len(out) - len(arms):], indent=1))
        free = shutil.disk_usage(VENV_PARENT).free / 1e9
        print("    (%.1f GB free)" % free, flush=True)
    (BASE / "raw_results.json").write_text(json.dumps({
        "interpreter": interpreter_record(),
        "arms": arms,
        "records": out,
    }, indent=1))
    print("\nwrote %s" % (BASE / "raw_results.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

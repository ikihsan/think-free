#!/usr/bin/env python3
"""E069 install machinery: virtualenvs, pip, and the import oracle.

Split out of `harness.py` on 2026-10-09 when that file passed the 300-line cap.
Everything here is reachable as `harness.<name>`; `harness.py` imports this
module and re-exports, so no call site and no committed raw record moves.

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

from config import (BASE, REPO_ROOT, VENV_PARENT, GETPIP, GETPIP_URL,
                     BASE_PYTHON_VERSION, PIP_TIMEOUT)





# ---------------------------------------------------------------- venv

def ensure_getpip():
    if GETPIP.exists():
        return
    VENV_PARENT.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(GETPIP_URL, timeout=120) as response:
        GETPIP.write_bytes(response.read())


BASE_PYTHON = os.environ.get(
    "E069_PYTHON",
    "/home/ubuntu/.local/share/uv/python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10",
)


RUN_ID = os.environ.get("E069_RUN_ID") or ("run%s" % int(time.time()))


def venv_root():
    """A per-run virtualenv directory.

    Never reused across runs: a venv left over from an interrupted run can be
    mid-write while shutil.rmtree walks it, which is what a `Directory not
    empty` failure is. A new directory per run costs a venv and buys the
    guarantee that every arm of a run is measured on bytes nothing else is
    writing.
    """
    path = VENV_PARENT / RUN_ID
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_venv(path):
    """Fresh virtualenv for one arm. Python 3.10, pip from the recorded bootstrap."""
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
        if path.exists():
            shutil.rmtree(path)
    proc = subprocess.run(
        [BASE_PYTHON, "-m", "venv", str(path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        # 3.10 from python-build-standalone ships ensurepip; fall back if it does not.
        proc = subprocess.run(
            [BASE_PYTHON, "-m", "venv", "--without-pip", str(path)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError("venv failed: %s" % proc.stderr[-2000:])
        proc = subprocess.run(
            [str(path / "bin" / "python"), str(GETPIP), "--no-warn-script-location"],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError("get-pip failed: %s" % proc.stderr[-2000:])
    return path / "bin" / "python"


def run(cmd, timeout=PIP_TIMEOUT, cwd=None):
    started = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return proc.returncode, proc.stdout, proc.stderr, time.time() - started
    except subprocess.TimeoutExpired:
        return None, "", "TIMEOUT after %ss" % timeout, time.time() - started


# ---------------------------------------------------------------- install

RESOLUTION_PATTERNS = (
    "no matching distribution",
    "requires a different python version",
    "requires-python",
    "resolutionimpossible",
    "conflict",
    "not find a version that satisfies",
    "could not find a version",
    "no such file or directory",
    "invalid requirement",
)


def classify_failure(stderr, stdout):
    """Distinguish a version-resolution failure from a missing dependency.

    A pin that exists but is incompatible with the target interpreter is a
    different defect from an import the spec never covered, and pooling them
    hides which one is present.
    """
    blob = (stderr + "\n" + stdout).lower()
    resolution = [p for p in RESOLUTION_PATTERNS if p in blob]
    kinds = set()
    if "requires a different python version" in blob or "requires-python" in blob:
        kinds.add("interpreter_incompatible_pin")
    if "no matching distribution" in blob or "could not find a version" in blob \
            or "not find a version that satisfies" in blob:
        kinds.add("pin_absent_for_interpreter")
    if "resolutionimpossible" in blob or "conflict" in blob:
        kinds.add("pin_conflict")
    if "no such file or directory" in blob:
        kinds.add("missing_spec_file")
    if "invalid requirement" in blob:
        kinds.add("malformed_spec")
    if "error" in blob and not kinds:
        kinds.add("other_pip_error")
    if not kinds:
        kinds.add("install_succeeded" if "error" not in blob else "unclassified_failure")
    return sorted(kinds), resolution


def install(python_bin, spec, repo_dir):
    """pip install the arm's spec into a fresh venv. Returns a record."""
    if spec["mode"] == "requirements":
        rel = spec["path"]
        try:
            rel = str(Path(spec["path"]).relative_to(REPO_ROOT))
        except ValueError:
            pass
        record = {"mode": "requirements", "spec": rel}
        target = ["-r", spec["path"]]
    else:
        record = {"mode": "install_dir", "spec": spec["path"]}
        target = [spec["path"]]
    record.update({"exit": None, "first_failure": None, "seconds": None,
                   "failure_kinds": None, "download_mb": 0, "detail": None})
    cmd = [python_bin, "-m", "pip", "install", "--no-input", "--disable-pip-version-check",
           "--no-cache-dir"] + target
    code, out, err, secs = run(cmd, cwd=repo_dir)
    record["exit"] = code
    record["seconds"] = round(secs, 1)
    combined = out + "\n" + err
    units = {"kB": 1e-3, "MB": 1.0, "GB": 1e3}
    record["download_mb"] = round(
        sum(float(m) * units.get(u, 1.0)
            for m, u in re.findall(r"([\d.]+)\s*(kB|MB|GB)", combined)), 2)
    if code != 0:
        kinds, _ = classify_failure(err, out)
        record["failure_kinds"] = kinds
        for line in (err + "\n" + out).splitlines():
            low = line.lower()
            if low.startswith("error"):
                record["first_failure"] = line.strip()[:400]
                break
        if record["first_failure"] is None:
            record["first_failure"] = ((err or out).strip().splitlines() or ["(no output)"])[-1][:400]
    else:
        kinds, _ = classify_failure(err, out)
        record["failure_kinds"] = kinds
        line = [l for l in combined.splitlines() if l.startswith("Successfully installed")]
        record["detail"] = line[0][:400] if line else None
    return record


# ---------------------------------------------------------------- import oracle

PROBE_SOURCE = '''\
import importlib, json, sys
sys.path.insert(0, sys.argv[1])
out = {}
for name in json.loads(sys.argv[2]):
    try:
        importlib.import_module(name)
        out[name] = "ok"
    except BaseException as exc:
        out[name] = "{0}: {1}".format(type(exc).__name__, str(exc)[:120])
print(json.dumps(out))
'''


def probe_imports(bin_path, repo_dir, needed):
    """Import every needed top-level module in one child process."""
    proc = subprocess.run(
        [str(bin_path), "-c", PROBE_SOURCE, str(repo_dir), json.dumps(needed)],
        capture_output=True, text=True, timeout=900, cwd=str(repo_dir),
    )
    out, err, code = proc.stdout, proc.stderr, proc.returncode
    if code != 0:
        return {"__harness__": err.strip()[-300:]}
    for line in reversed(out.splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            return json.loads(line)
    return {"__harness__": "no json: %s" % (out.strip()[-200:] + err.strip()[-200:])}


def needed_modules(extracted_row, stdlib, firstparty, spec_names):
    """Third-party top-level modules the repo imports that the arm's spec names.

    This is the set that answers "did the spec work". It was previously the
    complement — the modules the spec did **not** name — which made "working"
    unsatisfiable by construction: no spec can supply an import it never
    mentions. P1 caught it: both A1 repositories installed cleanly (exit 0) and
    were still reported not working, because every module checked was one their
    own pinned spec had never claimed to provide.
    """
    needed = []
    for name in sorted(extracted_row.get("imports", [])):
        top = name.split(".")[0]
        if not top or top in stdlib or top in firstparty:
            continue
        if top in spec_names:
            needed.append(top)
    return needed


def spec_names(spec, repo_dir=None):
    """Package names an arm's spec supplies, normalised to import-name form."""
    if spec is None:
        return set()
    if isinstance(spec, dict) and spec.get("mode") == "install_dir":
        # A build file declares its runtime deps only after a build; read the
        # names pip would need by asking pip itself, and fall back to the union
        # of the obvious declarations inside the directory.
        names = set()
        target = Path(spec["path"])
        for child in sorted(target.glob("*.txt")) + sorted(target.glob("*.cfg")):
            names |= _names_from_requirements(child)
        for child in sorted(target.glob("*.toml")):
            names |= _names_from_toml(child)
        setup = target / "setup.py"
        if setup.is_file():
            names |= _names_from_setup(setup)
        return names
    return _names_from_requirements(Path(spec["path"]))


def _names_from_requirements(path):
    names = set()
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "-")):
            continue
        name = re.split(r"[=<>!~;\[ ]", line, 1)[0].strip()
        if name:
            names.add(name.replace("-", "_").lower())
    return names


def _names_from_toml(path):
    names = set()
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if "=" not in line or line.startswith(("#", "[")):
            continue
        key = line.split("=", 1)[0].strip().strip('"\'')
        if not key or key in ("version", "name", "description", "python"):
            continue
        names.add(key.replace("-", "_").lower())
    return names


def _names_from_setup(path):
    names = set()
    text = path.read_text(errors="replace")
    for match in re.finditer(r"install_requires\s*=\s*\[(.*?)\]", text, re.S):
        for item in re.findall(r"[\"']([^\"']+)[\"']", match.group(1)):
            names.add(re.split(r"[=<>!~;\[ ]", item, 1)[0].strip().replace("-", "_").lower())
    return names


def normalise(name):
    return name.replace("-", "_").lower()


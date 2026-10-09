#!/usr/bin/env python3
"""E070 arm M - the mechanism, on bytes.

For each pre-declared name: create a fresh virtualenv, run
`pip install <name>` with pip's defaults, capture stdout+stderr
verbatim and the exit code, then probe what the installed
distribution actually provides. Nothing is inferred from the
package's own claims: the import probe is the artifact test.

Writes raw/arm_m.json. Stdlib only.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# The system python3.8 lacks ensurepip (no python3.8-venv on
# this host), so arm M uses the uv-managed 3.10.19 interpreter
# E069 also used; record which one every row ran on.
BASE = os.environ.get(
    "E070_PY",
    "/home/ubuntu/.local/share/uv/python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10",
)

# name -> (declared class, the project the user intended, top-level
# module the intended project provides, for the import probe)
NAMES = [
    ("sklearn", "B", "scikit-learn", "sklearn"),
    ("telegram", "B", "python-telegram-bot", "telegram"),
    ("beautifulsoup", "B", "beautifulsoup4", "bs4"),
    ("color", "B", "colour", "color"),
    ("reqests", "A", "requests", "requests"),
]


def run(cmd, cwd=None, timeout=600):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    return {"exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def probe_import(venv_py, module):
    code = "import %s; print('IMPORT_OK', %s.__file__)" % (module, module)
    return run([venv_py, "-c", code], timeout=120)


def main():
    os.makedirs(RAW, exist_ok=True)
    results = [{"interpreter": BASE, "interpreter_version": run(
        [BASE, "--version"])["stdout"].strip()}]
    for name, klass, intended, module in NAMES:
        tmp = tempfile.mkdtemp(prefix="e070-armm-")
        venv = os.path.join(tmp, "venv")
        row = {"name": name, "declared_class": klass,
               "intended_project": intended}
        mk = run([BASE, "-m", "venv", venv])
        if mk["exit"] != 0:
            row["venv_create"] = mk
            results.append(row)
            continue
        venv_py = os.path.join(venv, "bin", "python")
        row["pip_version"] = run([venv_py, "-m", "pip", "--version"])
        row["install"] = run([venv_py, "-m", "pip", "install", name])
        row["import_probe"] = probe_import(venv_py, module)
        # What did pip think it installed? pip show is a second read.
        row["pip_show"] = run([venv_py, "-m", "pip", "show", name])
        results.append(row)
        shutil.rmtree(tmp, ignore_errors=True)
        print("done", name, "install exit", row["install"]["exit"],
              file=sys.stderr)
    out = os.path.join(RAW, "arm_m.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out, file=sys.stderr)


if __name__ == "__main__":
    main()

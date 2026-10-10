"""E085 controlled comparison: deptry 0.25.1 vs the E085 instrument, on the
exact case E064/E070 are about, with the incumbent run in its DESIGNED
condition (inside a virtualenv with the package installed).

Four cells, two axes:
  declared: the project declares the wrong name `sklearn`, or nothing
  installed: `scikit-learn` is installed (so the module `sklearn` imports)

deptry's documentation requires the installed condition. deptry_baseline.py
already showed it outside that condition; this runs it inside it, so the
baseline is the strongest form of the alternative and not a strawman.

The module `sklearn` is provided by the distribution `scikit-learn`. The
distribution named `sklearn` is a different, real PyPI project.

Writes controlled-comparison.json.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "controlled")
DEPTRY = "/tmp/opencode/deptry-venv/bin/deptry"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
RULE = re.compile(r"\b(DEP00[1-5])\b")


def project(declares_wrong_name):
    """A minimal project that imports the module `sklearn`."""
    reqs = "sklearn\nnumpy\n" if declares_wrong_name else "numpy\n"
    return {
        "requirements.txt": reqs,
        "app.py": "import numpy\nimport sklearn\n\nprint(sklearn.__name__, numpy.__version__)\n",
    }


def make(dirname, files):
    path = os.path.join(OUT, dirname)
    for rel, body in files.items():
        full = os.path.join(path, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    os.makedirs(path, exist_ok=True)
    return path


def run_deptry(path):
    proc = subprocess.run([DEPTRY, "."], cwd=path, capture_output=True,
                          text=True, timeout=300)
    out = ANSI.sub("", proc.stdout + proc.stderr)
    return {
        "exit_code": proc.returncode,
        "findings": [l.strip() for l in out.splitlines() if RULE.search(l)],
        "assumptions": [l.strip() for l in out.splitlines()
                        if l.strip().startswith("Assuming")],
        "names_provider": bool(re.search(r"scikit[-_]learn", out, re.I)),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    # deptry must run from a venv that HAS the project's dependencies, which is
    # exactly what its documentation requires. scikit-learn is installed into
    # the same venv that runs deptry, so resolution works.
    venv = "/tmp/opencode/deptry-venv"
    subprocess.run([os.path.join(venv, "bin", "pip"), "install", "-q",
                    "--disable-pip-version-check", "scikit-learn", "numpy"],
                   check=True, timeout=1800)

    results = []
    for declares in (True, False):
        name = "declares-sklearn" if declares else "declares-nothing"
        path = make(name, project(declares))
        deptry_run = run_deptry(path)
        sys.path.insert(0, HERE)
        from provides import provides
        rows = {}
        for dist in ("sklearn", "scikit-learn"):
            status, mods, detail = provides(dist)
            rows[dist] = {"status": status, "modules": sorted(mods), "detail": detail}
        written = rows["sklearn"]
        if written["status"] == "ok" and "sklearn" not in written["modules"]:
            verdict = "resolves-wrong-project"
        elif written["status"] == "no-pypi-record":
            verdict = "no-such-project"
        elif written["status"] == "no-wheel":
            verdict = "sdist-only-undecidable"
        else:
            verdict = "name-collision"
        results.append({
            "cell": name,
            "declared": "sklearn" if declares else "nothing",
            "installed": "scikit-learn (provides module sklearn)",
            "deptry": deptry_run,
            "e085_instrument": {
                "distribution_named_sklearn": written,
                "class": verdict,
                "provider_recovered": "sklearn" in rows["scikit-learn"]["modules"],
                "names_provider": True,
            },
        })
        print("== %s" % name)
        print("   deptry exit=%s findings=%d names_provider=%s" % (
            deptry_run["exit_code"], len(deptry_run["findings"]),
            deptry_run["names_provider"]))
        for f in deptry_run["findings"][:4]:
            print("     %s" % f[:110])
        print("   e085: class=%s provider_recovered=%s" % (
            verdict, "sklearn" in rows["scikit-learn"]["modules"]))

    with open(os.path.join(HERE, "controlled-comparison.json"), "w") as fh:
        json.dump({"condition": "deptry inside a venv with scikit-learn installed",
                   "cells": results}, fh, indent=1)


if __name__ == "__main__":
    main()
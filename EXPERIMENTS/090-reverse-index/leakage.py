#!/usr/bin/env python3
"""How much of E090's population is the repositories' own private code?

Declared 2026-10-10, before the run, because it decides what G2's number means.

The protocol says the population is "top-level module names imported by real
Python repositories", with the repository's own packages excluded. `harvest.py`
implements that exclusion as *top-level* packages, `src/` and `lib/` layouts,
and the repo basename. It does not ask the sharper question this file asks:
**does the repository itself provide this name?** A repo that vendors a package,
keeps a namespace directory at the root, or has a `tests/` directory without
`__init__.py` contributes names that no PyPI project can be expected to provide.
Those rows sit in G2's denominator, so a leak share of C puts a ceiling of
roughly `1 - C` on any coverage this index can report, and a gate at 0.70 can be
made unreachable by the harvest alone.

**This file changes no gate and no population.** It is read alongside G2. The
protocol's "the denominator is printed next to every figure and both readings
are given" is honoured by reporting coverage over the harvested population and
over the population with the leak removed, side by side.

**Why the names are classified, not just counted.** A name found as a nested
`pkg/helpers.py` is not provided by the repository at its top level, and a name
found as `<root>/X.py` is. Those are different claims, and the first pass of
this file conflated them into one number that was therefore only an upper bound.
Every hit is now recorded with the path that produced it and a class:

  | class | meaning | provides X at top level? |
  |---|---|---|
  | `root-file` | `<root>/X.py` | yes |
  | `root-package` | `<root>/X/__init__.py` | yes |
  | `root-namespace` | `<root>/X/` with no `__init__.py` | yes, as a namespace package |
  | `src-layout` | `<root>/{src,lib}/X/...` | yes |
  | `nested-vendored` | `X/` or `X.py` only at depth > 1 | only if that directory is itself a sys.path root |

`nested-vendored` is the only class that does not by itself make the name
un-provideable by a PyPI project, so the **strict** leak share counts the first
four classes and the **broad** share counts all five. Both are reported; the
strict one bounds G2's ceiling and the broad one is recorded as an upper bound.

**Reuse control.** The 60 repositories are the exact names harvest.py recorded,
re-read from `population.json` and never re-selected: the harvest sorted GitHub
search by `updated`, so a second harvest chooses different repositories and the
two figures are not comparable.

**Declared gates.**

  L1  Strict leak share and broad leak share, each with its denominator. No
      pass/fail. A strict share above 0.20 puts G2's 0.70 gate within reach of
      the harvest alone and would be reported as an instrument limitation.
  L2  `git clone` reaches fewer than 60 repositories -> `not_evaluated`, never a
      partial figure presented as the whole.

status: draft. Run: python3 leakage.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
POP = os.path.join(HERE, "population.json")
OUT = os.path.join(HERE, "leakage.json")
SKIP = {".git"}

STRICT = ("root-file", "root-package", "root-namespace", "src-layout")


def clone(full_name, root):
    dest = os.path.join(root, full_name.replace("/", "__"))
    if os.path.isdir(dest):
        return dest
    subprocess.run(["git", "clone", "--depth", "1", "--quiet",
                    "https://github.com/%s.git" % full_name, dest],
                   check=False, capture_output=True, timeout=600)
    return dest if os.path.isdir(dest) else None


def classify(root, name):
    """The strongest class that makes `root` provide top-level `name`."""
    p = os.path.join(root, name)
    if os.path.isfile(p + ".py"):
        return "root-file", p + ".py"
    if os.path.isdir(p):
        if os.path.isfile(os.path.join(p, "__init__.py")):
            return "root-package", p
        return "root-namespace", p
    for layout in ("src", "lib"):
        q = os.path.join(root, layout, name)
        if os.path.isdir(q):
            return "src-layout", q
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if name in dirnames:
            return "nested-vendored", os.path.join(dirpath, name)
        if depth == 0:
            continue
        if name + ".py" in filenames:
            return "nested-vendored", os.path.join(dirpath, name + ".py")
    return None, None


def check(entry):
    root, name = entry
    dest = clone(name, root)
    if not dest:
        return {"repo": name, "status": "clone-failed", "internal": {}}
    hits = {}
    for mod in LOCAL.get(name, []):
        cls, path = classify(dest, mod)
        if cls:
            hits[mod] = {"class": cls,
                         "path": os.path.relpath(path, dest)}
    shutil.rmtree(dest, ignore_errors=True)
    return {"repo": name, "status": "ok", "n_modules": len(LOCAL.get(name, [])),
            "internal": hits}


LOCAL = {}


def main():
    with open(POP) as fh:
        doc = json.load(fh)
    population = doc["population"]
    for r in doc["per_repo"]:
        LOCAL[r["repo"]] = r.get("modules") or []

    root = tempfile.mkdtemp(prefix="e090-leak-", dir="/tmp/opencode")
    started = time.time()
    names = sorted(LOCAL)
    with ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(lambda n: check((root, n)), names))
    shutil.rmtree(root, ignore_errors=True)

    ok = [r for r in rows if r["status"] == "ok"]
    failed = [r["repo"] for r in rows if r["status"] != "ok"]

    internal = {}
    for r in ok:
        for mod, info in r["internal"].items():
            internal.setdefault(mod, []).append(dict(info, repo=r["repo"]))

    # A name leaked only when the repository that imports it also provides it.
    # A name a second repository imports has independent evidence of being a
    # real distribution, so it is kept in the population and reported apart.
    solo = {m: v for m, v in internal.items() if len(v) == 1}
    shared = {m: v for m, v in internal.items() if len(v) > 1}
    strict = sorted(m for m, v in solo.items() if v[0]["class"] in STRICT)
    broad = sorted(solo)

    n = len(population)
    out = {
        "schema": "e090.leakage/2",
        "declared_gates": {
            "L1": "report strict and broad leak share with denominators; no "
                  "pass/fail. strict > 0.20 puts G2's 0.70 within reach of the "
                  "harvest alone",
            "L2": "fewer than 60 repositories cloned -> not_evaluated",
        },
        "population": n,
        "repositories_in_population": len(LOCAL),
        "repositories_cloned": len(ok),
        "repositories_failed": failed,
        "l2_verdict": "not_evaluated" if failed else "ok",
        "seconds": round(time.time() - started, 1),
        "internal_names": len(internal),
        "strict_leak": len(strict),
        "strict_share": round(len(strict) / n, 4),
        "broad_leak": len(broad),
        "broad_share": round(len(broad) / n, 4),
        "g2_coverage_ceiling_strict": round(1 - len(strict) / n, 4),
        "g2_coverage_ceiling_broad": round(1 - len(broad) / n, 4),
        "by_class": {},
        "shared_internal_elsewhere": {m: [x["repo"] for x in v]
                                     for m, v in sorted(shared.items())},
        "leaked": {m: solo[m][0] for m in sorted(solo)},
        "population_minus_strict_leak": sorted(
            m for m in population if m not in set(strict)),
        "per_repo": [{"repo": r["repo"], "status": r["status"],
                      "n_modules": r.get("n_modules"),
                      "n_repo_internal": len(r.get("internal") or {})}
                     for r in rows],
    }
    for m, v in solo.items():
        out["by_class"][v[0]["class"]] = out["by_class"].get(v[0]["class"], 0) + 1
    out["by_class"] = dict(sorted(out["by_class"].items()))

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("repositories cloned: %d of %d (failed: %s)"
          % (len(ok), len(LOCAL), failed or "none"))
    print("population: %d distinct names" % n)
    print("classes (single-repo hits):", out["by_class"])
    print("strict leak %d (%.4f)  broad leak %d (%.4f)"
          % (len(strict), out["strict_share"], len(broad), out["broad_share"]))
    print("G2 coverage ceiling: strict %.4f  broad %.4f"
          % (out["g2_coverage_ceiling_strict"],
             out["g2_coverage_ceiling_broad"]))
    print("sample strict leaked:", strict[:20])
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Harvest the top-level module names real Python repositories import.

The population is a distinct top-level module name. Nothing here is curated,
filtered by whether it is a known cross-name case, or chosen because it is
interesting: every `import X` / `from X import ...` in the cloned sources
contributes, minus three declared exclusions.

Selection rule, fixed before the run so it cannot be tuned to the result:

  Two popularity strata, both `language:python`, both sorted by `updated`, both
  filtered to pushed within the last 12 months:
      A  stars >= 1000      (30 repositories)
      B  5 <= stars <= 100  (30 repositories)
  The first repository page of each query, in API order, cloned at `--depth 1`.

  Stratum B exists because stratum A is biased *towards* popular modules, which
  is exactly the bias that would make a coverage number read high. Reporting
  both strata is the control; dropping B because it reads worse is not allowed.

Exclusions, each counted and printed:
  - the running interpreter's own standard library, from the interpreter, not
    from a hard-coded list, so the figure is this machine's truth
  - the repository's own top-level directories and packages
  - relative imports (`from . import x`, `from .mod import y`)

status: draft. Run: python3 harvest.py
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
CLONES = os.path.join(HERE, "clones")
POP = os.path.join(HERE, "population.json")

STRATA = [
    {"name": "A-popular", "q": "language:python stars:>=1000 pushed:>2025-10-01",
     "n": 30},
    {"name": "B-longtail", "q": "language:python stars:5..100 pushed:>2025-10-01",
     "n": 30},
]

IMPORT_RE = re.compile(
    r"^[ \t]*(?:import[ \t]+([A-Za-z_][\w.]*)"
    r"|from[ \t]+([A-Za-z_][\w.]*)[ \t]+import\b)", re.M)
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".tox",
             ".venv", "venv", "build", "dist", ".eggs", "site-packages",
             ".mypy_cache", ".pytest_cache"}


def api(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "e090-harvest",
                      "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def stdlib_names():
    """This interpreter's standard library, from the interpreter.

    `sys.stdlib_module_names` is the interpreter's own answer and is used when it
    exists (3.10+). Before 3.10 it does not, and the first version of this
    function fell back to listing top-level `.py` files without a leading
    underscore. That fallback missed every C extension module and every
    underscore-prefixed stdlib module: 20 names reached the population on
    Python 3.8 (`math`, `array`, `gc`, `itertools`, `_thread`, `__future__`,
    ...), 1.02% of it. Too small to move a verdict, and still wrong, because
    `sys.builtin_module_names` is the interpreter's own list of built-ins and
    needs no hard-coded table. The platform lib-dynload directory covers the
    remaining extensions.
    """
    import sysconfig
    names = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") \
        else set()
    names |= set(sys.builtin_module_names)
    paths = sysconfig.get_paths()
    dirs = {paths.get("stdlib"), paths.get("platstdlib")}
    for lib in dirs:
        if not lib or not os.path.isdir(lib):
            continue
        for entry in os.listdir(lib):
            stem, ext = os.path.splitext(entry)
            if stem:
                names.add(stem)
            for sub in ("lib-dynload", "lib64"):
                d = os.path.join(lib, sub)
                if os.path.isdir(d):
                    for e2 in os.listdir(d):
                        s2, _x = os.path.splitext(e2)
                        if s2:
                            names.add(s2)
    return names


def search_repos(query, n):
    out, page = [], 1
    while len(out) < n and page <= 3:
        items = api("https://api.github.com/search/repositories?q=%s"
                    "&sort=updated&order=desc&per_page=50&page=%d"
                    % (urllib.request.quote(query), page)).get("items", [])
        if not items:
            break
        for it in items:
            if it.get("fork") or it.get("size", 0) > 120000:
                continue
            out.append({"full_name": it["full_name"],
                        "clone_url": it["clone_url"],
                        "stars": it["stargazers_count"],
                        "pushed_at": it["pushed_at"]})
            if len(out) >= n:
                break
        page += 1
    return out[:n]


def clone(repo, root):
    dest = os.path.join(root, repo["full_name"].replace("/", "__"))
    if os.path.isdir(dest):
        return dest
    subprocess.run(["git", "clone", "--depth", "1", "--quiet",
                    repo["clone_url"], dest],
                   check=False, capture_output=True, timeout=300)
    return dest if os.path.isdir(dest) else None


def local_names(root):
    """The repository's own importable top-level names."""
    names = set()
    try:
        for entry in os.listdir(root):
            if entry in SKIP_DIRS:
                continue
            p = os.path.join(root, entry)
            if os.path.isdir(p) and os.path.isfile(os.path.join(p, "__init__.py")):
                names.add(entry)
            elif entry.endswith(".py"):
                names.add(os.path.splitext(entry)[0])
    except OSError:
        pass
    # A `src/` layout puts the package one level down.
    for layout in ("src", "lib"):
        d = os.path.join(root, layout)
        if os.path.isdir(d):
            try:
                for entry in os.listdir(d):
                    p = os.path.join(d, entry)
                    if os.path.isdir(p) and os.path.isfile(
                            os.path.join(p, "__init__.py")):
                        names.add(entry)
            except OSError:
                pass
    names.add(os.path.basename(root).split("__")[-1])
    return {n for n in names if n}


def harvest_one(repo, root, stdlib):
    dest = clone(repo, root)
    if not dest:
        return {"repo": repo["full_name"], "stars": repo["stars"],
                "stratum": repo["stratum"],
                "status": "clone-failed", "modules": [], "files": 0}
    local = local_names(dest)
    found, files = set(), 0
    for dirpath, dirnames, filenames in os.walk(dest):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            files += 1
            try:
                with open(os.path.join(dirpath, fn), encoding="utf-8",
                          errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            if len(text) > 400000:
                continue
            for m in IMPORT_RE.finditer(text):
                mod = m.group(1) or m.group(2)
                if not mod or mod.startswith("."):
                    continue
                top = mod.split(".")[0]
                if not top or top in stdlib or top in local:
                    continue
                found.add(top)
    return {"repo": repo["full_name"], "stars": repo["stars"],
            "stratum": repo["stratum"],
            "status": "ok", "modules": sorted(found), "files": files}


def main():
    stdlib = stdlib_names()
    root = tempfile.mkdtemp(prefix="e090-clones-", dir="/tmp/opencode")
    selected = []
    for s in STRATA:
        rows = search_repos(s["q"], s["n"])
        for r in rows:
            r["stratum"] = s["name"]
        selected.extend(rows)
    print("selected %d repositories (%s)"
          % (len(selected), ", ".join("%s=%d" % (s["name"], s["n"])
                                      for s in STRATA)), flush=True)

    started = time.time()
    with ThreadPoolExecutor(8) as ex:
        harvested = list(ex.map(
            lambda r: harvest_one(r, root, stdlib), selected))
    shutil.rmtree(root, ignore_errors=True)

    ok = [h for h in harvested if h["status"] == "ok"]
    per_stratum = {}
    for h in ok:
        per_stratum.setdefault(h["stratum"], set()).update(h["modules"])
    population = sorted({m for h in ok for m in h["modules"]})

    out = {
        "schema": "e090.population/1",
        "harvest_seconds": round(time.time() - started, 1),
        "stdlib_names": len(stdlib),
        "repositories_selected": len(selected),
        "repositories_ok": len(ok),
        "repositories_failed": len(harvested) - len(ok),
        "python_files_read": sum(h["files"] for h in ok),
        "distinct_modules": len(population),
        "per_stratum_modules": {k: len(v) for k, v in per_stratum.items()},
        "population": population,
        "per_repo": [{"repo": h["repo"], "stratum": h["stratum"],
                      "stars": h["stars"], "n_modules": len(h["modules"]),
                      "files": h["files"],
                      # The per-repository control in PROTOCOL.md ("coverage
                      # is also reported per repository, so a reader can see
                      # whether one well-known repository is deciding the
                      # pooled figure") is only computable with this list.
                      "modules": h["modules"]} for h in harvested],
    }
    with open(POP, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("population", "per_repo")}, indent=1,
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
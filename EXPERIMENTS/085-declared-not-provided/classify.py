"""E085 arm A classification: for every (declared D, imported M) pair, ask PyPI
whether D provides M, and whether some other real distribution does.

Reads repo-scan.json, resolves every declared distribution once through the
cache, and writes classified-pairs.json plus results.json (the gate verdicts).

Every denominator is over computable pairs. A distribution with no PyPI record,
no wheel, or an unreadable central directory is a missing observation and is
counted separately (D082). Read PROTOCOL.md, AMENDMENT-1/2/3.md first.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from provides import provides  # noqa: E402
from scan_repos import SKIP_DIRS, stdlib_modules  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")


def resolve(name):
    key = name.replace("/", "_")
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        try:
            with open(path) as fh:
                return json.load(fh)
        except ValueError:
            pass
    for attempt in range(3):
        try:
            status, mods, detail = provides(name)
            break
        except Exception as exc:                      # network, 5xx, malformed
            if attempt == 2:
                status, mods, detail = "unreadable", set(), {"why": repr(exc)[:120]}
            else:
                time.sleep(2 * (attempt + 1))
    row = {"distribution": name, "status": status, "modules": sorted(mods), "detail": detail}
    with open(path, "w") as fh:
        json.dump(row, fh, indent=1, sort_keys=True)
    time.sleep(0.12)
    return row


def project_local_modules(repo_path):
    """Top-level names the repository itself defines, which are not dependencies.

    Two shapes count. A directory holding `__init__.py` is a package. A
    directory holding any source file is also local: a first version required
    `__init__.py`, so LPMP_BDD's own compiled extension directory `BDD/`
    (a C extension with no `__init__.py`) was scored as a third-party import
    and, because a PyPI project called `BDD` exists, as a silent wrong-project
    finding. That is instrumentation defect 3 in README.md.
    """
    tops = set()
    for dirpath, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for d in list(dirnames):
            inner = os.listdir(os.path.join(dirpath, d)) if os.path.isdir(os.path.join(dirpath, d)) else []
            if any(f.endswith((".py", ".pyx", ".c", ".cpp", ".so", ".pyd")) for f in inner):
                tops.add(d)
        for fn in filenames:
            if fn.endswith(".py"):
                tops.add(fn[:-3])
    return tops


def classify(pairs, index, stdlib):
    """index: distribution -> resolved row, for the corpus-wide reverse lookup."""
    # For each module, which corpus distributions provide it.
    provider_of = {}
    for dist, row in index.items():
        if row["status"] != "ok":
            continue
        for mod in row["modules"]:
            provider_of.setdefault(mod, set()).add(dist)
    out = []
    for repo, dist, module, sites in pairs:
        row = index.get(dist)
        if row is None or row["status"] != "ok":
            out.append({"repo": repo, "declared": dist, "module": module,
                        "sites": sites, "class": "missing-observation",
                        "declared_status": (row or {}).get("status", "unknown")})
            continue
        if module in stdlib:
            out.append({"repo": repo, "declared": dist, "module": module,
                        "sites": sites, "class": "stdlib-declared"})
            continue
        provided = module in row["modules"]
        others = {d for d in provider_of.get(module, set()) if d != dist}
        if provided:
            cls = "correct"
        elif others:
            cls = "wrong-distribution"
        else:
            cls = "unprovided"
        rec = {"repo": repo, "declared": dist, "module": module, "sites": sites,
               "class": cls, "declared_status": "ok"}
        if cls == "wrong-distribution":
            rec["providers"] = sorted(others)
        out.append(rec)
    return out


def covered_by_other_declared(pairs, index):
    """Pairs where a DIFFERENT declared distribution provides the module."""
    provider_of = {}
    for dist, row in index.items():
        if row["status"] == "ok":
            for mod in row["modules"]:
                provider_of.setdefault(mod, set()).add(dist)
    excluded = []
    for repo, dist, module, sites in pairs:
        if module in provider_of and provider_of[module] - {dist}:
            excluded.append({"repo": repo, "declared": dist, "module": module,
                             "sites": sites, "class": "covered-by-other-declared",
                             "providers": sorted(provider_of[module] - {dist})})
    return excluded


def classify_modules(repos, index, stdlib):
    """AMENDMENT-4: the unit of analysis is the imported module.

    For each non-stdlib, non-project-local imported top-level module M in each
    repository: is M provided by some distribution this repository declares? If
    not, what does the name M itself resolve to on PyPI? Only the last case is
    the silent wrong-project class.

    The module name is resolved as a distribution IN ITS OWN RIGHT. A first
    version looked it up in the index of declared distributions only, which
    meant a module that was not also a declared dependency - that is, exactly
    the modules most likely to be unprovided - was never resolved and was
    scored as a missing observation. That defect suppressed the target class
    by construction; it is recorded in README.md as instrumentation defect 1.
    """
    corpus_path = repos["corpus"]
    rows = []
    for r in repos["repos"]:
        declared = set(r["declared"])
        provided_by_declared = {}
        for dist in declared:
            row = index.get(dist)
            if row and row["status"] == "ok":
                for mod in row["modules"]:
                    provided_by_declared.setdefault(mod, set()).add(dist)
        if not declared:
            # No declarations to check against: missing observation, not a zero.
            for module, sites in sorted(r["imports"].items()):
                rows.append({"repo": r["repo"], "module": module, "sites": sites,
                             "class": "missing-observation", "reason": "repo declares nothing"})
            continue
        local = project_local_modules(os.path.join(corpus_path, r["path"]))
        for module, sites in sorted(r["imports"].items()):
            if module in stdlib or module in local:
                continue
            providers = provided_by_declared.get(module)
            if providers:
                rows.append({"repo": r["repo"], "module": module, "sites": sites,
                             "class": "covered", "providers": sorted(providers)})
                continue
            written = resolve(module)
            status = written["status"]
            if status == "ok" and module in written["modules"]:
                cls = "name-collision"
            elif status == "ok":
                cls = "silent-wrong-project"
            elif status == "no-pypi-record":
                cls = "loud-no-such-project"
            elif status == "no-wheel":
                cls = "undecidable-sdist-only"
            else:
                cls = "missing-observation"
            rec = {"repo": r["repo"], "module": module, "sites": sites, "class": cls,
                   "name_status": status}
            if cls == "silent-wrong-project":
                rec["shadow_provides"] = written["modules"]
            rows.append(rec)
    return rows


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def main():
    scan = json.load(open(os.path.join(HERE, "repo-scan.json")))
    stdlib = stdlib_modules()
    index = {}
    names = sorted({d for r in scan["repos"] for d in r["declared"]})
    print("resolving %d declared distributions" % len(names))
    for i, name in enumerate(names):
        index[name] = resolve(name)
        if (i + 1) % 50 == 0:
            print("  %d/%d" % (i + 1, len(names)), flush=True)

    corpus_provider_of = {}
    for dist, row in index.items():
        if row["status"] == "ok":
            for mod in row["modules"]:
                corpus_provider_of.setdefault(mod, set()).add(dist)

    module_rows = classify_modules(scan, index, stdlib)
    for rec in module_rows:
        if rec.get("class") == "silent-wrong-project":
            rec["corpus_providers"] = sorted(
                corpus_provider_of.get(rec["module"], set()))

    # Secondary, retained from the first declaration (AMENDMENT-4): the
    # declared x imported cross-product view, reported but not gated.
    pairs, live = [], []
    for r in scan["repos"]:
        local = project_local_modules(os.path.join(scan["corpus"], r["path"]))
        declared = set(r["declared"])
        for module, sites in sorted(r["imports"].items()):
            if module in local or module in stdlib:
                continue
            for dist in sorted(declared):
                pairs.append((r["repo"], dist, module, sites))
    excluded = covered_by_other_declared(pairs, index)
    excluded_keys = {(e["repo"], e["declared"], e["module"]) for e in excluded}
    live = [p for p in pairs if (p[0], p[1], p[2]) not in excluded_keys]
    cross_rows = classify(live, index, stdlib)

    counts = {}
    for rec in module_rows:
        counts[rec["class"]] = counts.get(rec["class"], 0) + 1
    cross_counts = {}
    for rec in cross_rows:
        cross_counts[rec["class"]] = cross_counts.get(rec["class"], 0) + 1

    scored = len(module_rows) - counts.get("missing-observation", 0)
    silent = counts.get("silent-wrong-project", 0)
    findings = [r for r in module_rows
                if r["class"] in ("silent-wrong-project", "loud-no-such-project",
                                  "undecidable-sdist-only")]
    with_provider = sum(1 for r in module_rows
                        if r["class"] == "silent-wrong-project" and r.get("corpus_providers"))
    cross_computable = len(live) - cross_counts.get("missing-observation", 0)
    results = {
        "counts": counts,
        "cross_counts": cross_counts,
        "repos_total": scan["n_repos"],
        "repos_with_both": len([r for r in scan["repos"] if r["declared"] and r["imports"]]),
        "declared_distributions": len(names),
        "declared_resolved_ok": sum(1 for v in index.values() if v["status"] == "ok"),
        "declared_missing": sum(1 for v in index.values() if v["status"] != "ok"),
        "modules_scored": scored,
        "modules_unprovided": len(findings),
        "s_modules": silent / scored if scored else None,
        "s_findings": silent / len(findings) if findings else None,
        "s_cross": (cross_counts.get("wrong-distribution", 0) / cross_computable
                    if cross_computable else None),
        "silent_with_corpus_provider": with_provider,
        "wilson_modules": wilson(silent, scored),
        "wilson_findings": wilson(silent, len(findings)),
    }
    results["gates"] = {
        "g1_ceiling": results["declared_resolved_ok"] / float(len(names) or 1),
        "g3_rate_s_modules": results["s_modules"],
        "g3_verdict": (
            "KILL" if results["s_modules"] is not None and results["s_modules"] < 0.005
            else "BUILD" if results["s_modules"] is not None and results["s_modules"] >= 0.02
            else "HOLD"),
    }
    with open(os.path.join(HERE, "classified-pairs.json"), "w") as fh:
        json.dump({"module_rows": module_rows, "cross_rows": cross_rows,
                   "excluded_covered": excluded}, fh, indent=1)
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
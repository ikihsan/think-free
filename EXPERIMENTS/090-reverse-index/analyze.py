#!/usr/bin/env python3
"""E090 analysis: does the reverse index reach real code, and is it worth more
than `pip install <module>`?

Everything the verdict rests on is computed here from two committed files --
population.json and raw-projects.jsonl -- so the numbers regenerate without a
network. The one thing that cannot be computed offline is the incumbent: whether
`pip install M` would have worked. That is measured once, cached under
baseline-cache/, and its cost reported.

Read the gates in PROTOCOL.md before reading this. G2 is coverage with the
baseline fallback DISABLED, so the number is the index's own. G3 is the share of
the population the index resolves and the incumbent does not.

status: draft. Run: python3 analyze.py
"""

import json
import os
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, os.pardir, "pyprovides"))
import report                                         # noqa: E402
from pyprovides import pypi, _pick_wheel, _central_directory, \
    entry_names, top_level_modules      # noqa: E402

POP = os.path.join(HERE, "population.json")
LEAK = os.path.join(HERE, "leakage.json")
RAW = os.path.join(HERE, "raw-projects.jsonl")
RANKED = os.path.join(HERE, "top-pypi-packages.min.json")
CACHE = os.path.join(HERE, "baseline-cache")
KS = [500, 1000, 2500, 5000, 10000, 15000]


def normalize(name):
    """PEP 503, the rule pip applies before it installs anything."""
    return re.sub(r"[-_.]+", "-", name).lower()


def load_rows():
    best = {}
    with open(RAW) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            best.setdefault(row["project"], row)
    return best


def index_at(rows, order, k):
    """module -> [projects], from the k most-downloaded projects read so far."""
    idx = {}
    for i, name in enumerate(order[:k]):
        row = rows.get(name)
        if not row or row.get("status") != "ok":
            continue
        for m in row["modules"]:
            idx.setdefault(m, []).append(name)
    return idx


def baseline_for(module):
    """Does `pip install <module>` leave the import working?

    That is: a project of the normalized name exists, and its wheel ships a
    module by that name. Cached, because this is the only network work here.
    """
    os.makedirs(CACHE, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in module)
    path = os.path.join(CACHE, safe + ".json")
    if os.path.exists(path):
        try:
            with open(path) as fh:
                return json.load(fh)
        except ValueError:
            pass
    project = normalize(module)
    rec = {"module": module, "project": project, "exists": False,
           "ships": False, "status": "unknown"}
    try:
        ok, payload = pypi(project)
        if not ok:
            rec["status"] = "no-such-project"
        else:
            rec["exists"] = True
            wheel = _pick_wheel(payload)
            if wheel is None:
                rec["status"] = "no-wheel"
            else:
                mods = top_level_modules(
                    entry_names(_central_directory(wheel["url"],
                                                   wheel.get("size"))[1]))
                rec["ships"] = module in mods
                rec["status"] = "ok"
                rec["shipped_modules"] = sorted(mods)[:12]
    except Exception as exc:                            # noqa: BLE001
        rec["status"] = "read-error:%s" % type(exc).__name__
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    return rec


def main():
    with open(POP) as fh:
        pop_doc = json.load(fh)
    population = pop_doc["population"]
    rows = load_rows()
    with open(RANKED) as fh:
        order = [r["project"] for r in json.load(fh)["rows"]]

    # leakage.py measures how much of the population the repositories provide
    # themselves. Those rows cannot be answered by any PyPI project, so they are
    # a ceiling on coverage rather than a failure of the index. G2 keeps its
    # declared denominator; the de-contaminated reading is reported beside it,
    # because PROTOCOL.md requires both readings and a denominator.
    leak = {}
    clean = population
    if os.path.exists(LEAK):
        with open(LEAK) as fh:
            leak = json.load(fh)
        clean = leak.get("population_minus_strict_leak") or population
    n_proj_ok = sum(1 for r in rows.values() if r.get("status") == "ok")
    status_counts = Counter(r.get("status") for r in rows.values())

    print("population: %d distinct module names from %d repositories"
          % (len(population), pop_doc["repositories_ok"]))
    if leak:
        print("leakage: strict %d of %d (%.4f) -> de-contaminated population %d"
              % (leak["strict_leak"], leak["population"], leak["strict_share"],
                 len(clean)), flush=True)
    print("projects read: %d (%d ok) of %d ranked"
          % (len(rows), n_proj_ok, len(order)))
    print("status mix:", status_counts.most_common(8), flush=True)

    curve = []
    for k in KS:
        idx = index_at(rows, order, k)
        hit = [m for m in population if m in idx]
        hit_c = [m for m in clean if m in idx]
        curve.append({"k": k, "modules_indexed": len(idx),
                      "covered": len(hit),
                      "coverage": round(len(hit) / len(population), 4),
                      "covered_decontaminated": len(hit_c),
                      "coverage_decontaminated":
                          round(len(hit_c) / len(clean), 4) if clean else None})
        print("  K=%-6d index=%-7d covered=%-5d coverage=%.4f  "
              "decontaminated=%-5d %.4f"
              % (k, len(idx), len(hit), len(hit) / len(population),
                 len(hit_c), (len(hit_c) / len(clean)) if clean else 0.0),
              flush=True)

    full = index_at(rows, order, len(order))
    covered = [m for m in population if m in full]
    uncovered = [m for m in population if m not in full]
    covered_c = [m for m in clean if m in full]

    print("baseline: %d modules, one PyPI lookup each" % len(population),
          flush=True)
    with ThreadPoolExecutor(12) as ex:
        base = list(ex.map(baseline_for, population))

    b_rec = {b["module"]: b for b in base}
    baseline_ok = {m for m, b in b_rec.items() if b["exists"] and b["ships"]}
    added = [m for m in covered if m not in baseline_ok]
    added_c = [m for m in covered_c if m not in baseline_ok]

    # Per-stratum and per-repository, so one repository cannot decide the
    # pooled figure. Requires harvest.py's per-repo module lists.
    per_stratum = {}
    for r in pop_doc["per_repo"]:
        mods = set(r.get("modules") or [])
        if not mods:
            continue
        s = per_stratum.setdefault(
            r["stratum"], {"repos": 0, "modules": set(), "hit_repos": 0})
        s["repos"] += 1
        s["modules"].update(mods)
        if any(m in full for m in mods):
            s["hit_repos"] += 1
    per_repo = []
    for r in pop_doc["per_repo"]:
        mods = r.get("modules") or []
        if not mods:
            per_repo.append({"repo": r["repo"], "stratum": r["stratum"],
                             "n_modules": 0, "n_covered": 0, "coverage": None})
            continue
        hit = sum(1 for m in mods if m in full)
        per_repo.append({"repo": r["repo"], "stratum": r["stratum"],
                         "n_modules": len(mods), "n_covered": hit,
                         "coverage": round(hit / len(mods), 4)})

    # Reuse stratification. PROTOCOL.md fixes the sampling unit at "a distinct
    # top-level module name", which pools a name ten repositories depend on
    # with a name one repository depends on. The second kind is where repo-local
    # leakage lives, and leakage can only lower coverage, so a single pooled
    # figure understates what the index reaches. Declared gate G2 keeps its
    # pooled denominator; this is the stratified reading beside it, not a
    # replacement, and every level prints its own denominator.
    reuse = Counter()
    for r in pop_doc["per_repo"]:
        for m in r.get("modules") or []:
            reuse[m] += 1
    by_reuse = []
    for k in (1, 2, 3, 5, 10):
        sub = [m for m in population if reuse[m] >= k]
        if not sub:
            continue
        hit = [m for m in sub if m in full]
        add = [m for m in hit if m not in baseline_ok]
        by_reuse.append({
            "min_repositories": k, "denominator": len(sub),
            "covered": len(hit), "coverage": round(len(hit) / len(sub), 4),
            "pip_install_works": sum(1 for m in sub if m in baseline_ok),
            "added_over_pip_install": len(add),
            "added_share": round(len(add) / len(sub), 4)})

    result = report.build({
        "population": population, "clean": clean, "leak": leak,
        "pop_doc": pop_doc, "rows": rows, "order": order, "full": full,
        "n_proj_ok": n_proj_ok, "status_counts": status_counts,
        "curve": curve, "covered": covered, "uncovered": uncovered,
        "covered_c": covered_c, "baseline_ok": baseline_ok, "added": added,
        "added_c": added_c, "per_stratum": per_stratum,
        "per_repo": per_repo, "by_reuse": by_reuse, "base": base,
        "reuse": reuse})
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in result.items()
                      if k in ("g2", "g2_decontaminated", "g3",
                                "union")},
                     indent=1, sort_keys=True)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
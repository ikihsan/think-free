#!/usr/bin/env python3
"""E090 results document: assemble results.json from what analyze.py measured.

Split out of `analyze.py` at the 300-line cap, by invariant: this file is the
serialisation of a verdict, and it owns the shape of results.json. analyze.py
owns the measurement. Nothing is computed here that is not computed there, and
every denominator a gate is judged on is written next to the figure it belongs
to, because PROTOCOL.md requires it.

status: draft. Imported by analyze.py; not run directly.
"""

from collections import Counter


def build(ctx):
    """Assemble results.json from the measurements analyze.py passes in."""
    population = ctx["population"]
    clean = ctx["clean"]
    leak = ctx["leak"]
    pop_doc = ctx["pop_doc"]
    rows = ctx["rows"]
    order = ctx["order"]
    full = ctx["full"]
    n_proj_ok = ctx["n_proj_ok"]
    status_counts = ctx["status_counts"]
    curve = ctx["curve"]
    covered = ctx["covered"]
    uncovered = ctx["uncovered"]
    covered_c = ctx["covered_c"]
    baseline_ok = ctx["baseline_ok"]
    added = ctx["added"]
    added_c = ctx["added_c"]
    per_stratum = ctx["per_stratum"]
    per_repo = ctx["per_repo"]
    by_reuse = ctx["by_reuse"]
    base = ctx["base"]
    result = {
        "schema": "e090.results/1",
        "population": {
            "distinct_modules": len(population),
            "repositories_ok": pop_doc["repositories_ok"],
            "python_files_read": pop_doc["python_files_read"],
            "per_stratum_modules": pop_doc["per_stratum_modules"],
        },
        "index": {
            "projects_read": len(rows),
            "projects_ok": n_proj_ok,
            "status_counts": dict(status_counts),
            "modules_indexed": len(full),
            "k_curve": curve,
        },
        "g2": {
            "gate": "coverage >= 0.70 with baseline fallback disabled",
            "covered": len(covered),
            "denominator": len(population),
            "coverage": round(len(covered) / len(population), 4),
            "verdict": "PASS" if len(covered) / len(population) >= 0.70
                       else "FAIL",
            "uncovered_examples": uncovered[:60],
        },
        "g2_decontaminated": {
            "note": "same index, population minus the names the importing "
                    "repository provides itself; read beside g2, never "
                    "instead of it",
            "covered": len(covered_c),
            "denominator": len(clean),
            "coverage": round(len(covered_c) / len(clean), 4) if clean else None,
            "verdict": "PASS" if clean and len(covered_c) / len(clean) >= 0.70
                       else "FAIL",
            "uncovered_examples": [m for m in clean if m not in full][:60],
        },
        "leakage": ({k: leak[k] for k in
                     ("schema", "population", "repositories_cloned",
                      "l2_verdict", "by_class", "internal_names", "strict_leak",
                      "strict_share", "broad_leak", "broad_share",
                      "g2_coverage_ceiling_strict",
                      "g2_coverage_ceiling_broad")} if leak else None),
        "g3": {
            "gate": "share resolved by the index and not by pip install >= 0.02",
            "resolved_by_index": len(covered),
            "baseline_works": len(baseline_ok),
            "added_over_baseline": len(added),
            "denominator": len(population),
            "share": round(len(added) / len(population), 4),
            "verdict": "PASS" if len(added) / len(population) >= 0.02
                       else "FAIL",
            "added_examples": sorted(added)[:80],
            "added_decontaminated": len(added_c),
            "share_decontaminated":
                round(len(added_c) / len(clean), 4) if clean else None,
        },
        "per_stratum_coverage": {
            k: {"repos": v["repos"], "repos_with_any_covered": v["hit_repos"],
                "distinct_modules": len(v["modules"]),
                "covered": sum(1 for m in v["modules"] if m in full),
                "coverage": round(
                    sum(1 for m in v["modules"] if m in full)
                    / len(v["modules"]), 4) if v["modules"] else None}
            for k, v in sorted(per_stratum.items())},
        "coverage_by_repository_reuse": by_reuse,
        "union": {
            "note": "index and `pip install <module>` together, over the pooled "
                    "population. This is the share of imported names for which "
                    "one of the two free mechanisms names a provider at all.",
            "index_only": len(added),
            "pip_install_only": len(baseline_ok - set(covered)),
            "both": len(set(covered) & baseline_ok),
            "neither": len(population) - len(set(covered) | baseline_ok),
            "union_share": round(
                len(set(covered) | baseline_ok) / len(population), 4),
            "conditional_value": {
                "note": "among the names the index covers, the share "
                        "`pip install <module>` does not resolve",
                "covered": len(covered),
                "pip_install_misses": len(added),
                "share": round(len(added) / len(covered), 4) if covered
                          else None}},
        "per_repo_coverage": per_repo,
        "baseline": {
            "status_counts": dict(Counter(b["status"] for b in base)),
            "exists_but_does_not_ship": sorted(
                b["module"] for b in base
                if b["exists"] and not b["ships"] and b["status"] == "ok")[:40],
        },
        "cost": {
            "seconds": _dist([r.get("seconds", 0) for r in rows.values()]),
            "wheel_bytes": _dist([r.get("wheel_bytes", 0) for r in rows.values()]),
            "total_wheel_bytes": sum(r.get("wheel_bytes", 0)
                                     for r in rows.values()),
        },
    }
    return result


def _dist(values):
    """A distribution, not a mean: a build costs its tail."""
    vals = sorted(v for v in values if isinstance(v, (int, float)))
    if not vals:
        return {}
    def q(p):
        return vals[min(len(vals) - 1, int(p * len(vals)))]
    return {"n": len(vals), "p50": q(0.50), "p90": q(0.90), "p99": q(0.99),
            "max": vals[-1], "mean": round(sum(vals) / len(vals), 3)}

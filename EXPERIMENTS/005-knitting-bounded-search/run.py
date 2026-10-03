#!/usr/bin/env python3
"""Run the T-0011 bounded-neighbourhood comparison.  SYNTHETIC.

Headline: does the bounded planner from `planner.py` reproduce the exhaustive
minimum-cost repair of `EXPERIMENTS/004-knitting-stage-a/planner.py`, and is its
search space actually smaller?  The kill gate is in `README.md` and was fixed
before this ran.  Says nothing about physical feasibility.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import fixtures
from planner import MODEL, bounded_plan

HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"

HEADLINE = {"cap": None, "beam": 1}
SETTINGS = [
    {"cap": None, "beam": 1},
    {"cap": None, "beam": 2},
    {"cap": None, "beam": 4},
    {"cap": 3, "beam": 1},
    {"cap": 2, "beam": 1},
    {"cap": 2, "beam": 4},
    {"cap": 1, "beam": 1},
    {"cap": 1, "beam": 2},
    {"cap": 1, "beam": 4},
]
PATCH_COSTS = [1, 2, 3, 5, 8]
WORK_KEYS = ("subsets_enumerated", "combinations_evaluated", "combinations_required",
             "budget_applied", "separable", "oracle_subsets")


def key_of(setting):
    return f"cap={setting['cap']},beam={setting['beam']}"


def plan_row(plan, opt_cost=None, detail=True, work=True):
    row = {
        "cost": plan["cost"],
        "valid": plan["valid"],
        "checkable": plan["checkable"],
    }
    if detail:
        # Cell-level plans are kept for the hand-built fixtures, where they can
        # be read against the README's table. The random fixtures are
        # regenerable from the recorded seeds, so their cells are not repeated
        # nine times per case.
        row["patched"] = sorted(map(list, plan["patched"]))
        row["released"] = sorted(map(list, plan["released"]))
    if work:
        row["work"] = plan["work"]
    else:
        # Enough counters for the aggregates and the printed table; the rest
        # (group sizes, chunk counts) only matters where cells are recorded.
        row["work"] = {k: plan["work"].get(k) for k in WORK_KEYS}
    if opt_cost is None:
        # The oracle could not run here: optimality is not claimed for this row.
        row["oracle_skipped"] = True
    else:
        row["optimal"] = plan["cost"] == opt_cost
        row["suboptimality"] = plan["cost"] - opt_cost
    return row


def evaluate(name, patch, compared):
    """Oracle, 004's local rule, and the bounded planner on one case."""
    row = {"case": name, "family": fixtures.family(name), "errors": len(patch.errors)}
    if patch.unsupported:
        plan = bounded_plan(patch, **HEADLINE)
        row.update(
            {
                "unsupported": patch.unsupported,
                "required_behavior": "refuse",
                "refused": True,
                "refused_by_planner": bool(plan.get("refused")),
                "emitted_plan": plan["plan"] is not None,
            }
        )
        return row
    opt = patch.exhaustive_best() if compared else None
    if compared and opt is None:
        row.update({"unsupported": "no valid repair exists", "required_behavior": "refuse",
                    "refused": True})
        return row
    opt_cost = opt[0] if compared else None
    detail = row["family"] in ("from_004", "constructed", "large_oracle_skipped",
                               "large_with_oracle")
    loc_patched, loc_released = patch.local_plan()
    loc_cost = patch.cost(loc_patched, loc_released)
    row.update(
        {
            "oracle_available": compared,
            "exhaustive_cost": opt_cost,
            "local_cost": loc_cost,
            "local_valid": patch.errors <= (loc_released | loc_patched),
            "local_optimal": loc_cost == opt_cost,
            "settings": {
                key_of(s): plan_row(bounded_plan(patch, **s),
                                    opt_cost if compared else None,
                                    detail, s == HEADLINE or detail)
                for s in SETTINGS
            },
        }
    )
    return row


def aggregate(rows, setting):
    key = key_of(setting)
    solved = [r for r in rows if not r.get("refused") and r.get("oracle_available")]
    pairs = [(r, r["settings"][key]) for r in solved if key in r["settings"]]
    return {
        "cases": len(pairs),
        "all_valid": all(e.get("valid") for _, e in pairs),
        "all_optimal": all(e.get("optimal") for _, e in pairs),
        "suboptimal_cases": sorted(r["case"] for r, e in pairs if e.get("suboptimality", 0) > 0),
        "total_suboptimality": sum(e.get("suboptimality", 0) for _, e in pairs),
        "non_separable_cases": sorted(r["case"] for r, e in pairs
                                      if not e["work"].get("separable", True)),
        "subsets_enumerated": sum(e["work"]["subsets_enumerated"] for _, e in pairs),
        "combinations_evaluated": sum(e["work"]["combinations_evaluated"] for _, e in pairs),
        "budget_applied_cases": sorted(r["case"] for r, e in pairs
                                       if e["work"].get("budget_applied")),
        "oracle_subsets": sum(e["work"]["oracle_subsets"] for _, e in pairs),
    }


def by_family(rows, setting):
    key = key_of(setting)
    out = {}
    for row in rows:
        fam = row["family"]
        if key not in row.get("settings", {}) or not row.get("oracle_available"):
            continue
        entry = out.setdefault(fam, {"cases": 0, "all_optimal": True, "subsets": 0,
                                     "combinations": 0, "oracle_subsets": 0,
                                     "local_optimal": 0, "suboptimality": 0})
        e = row["settings"][key]
        entry["cases"] += 1
        entry["all_optimal"] &= bool(e.get("optimal"))
        entry["subsets"] += e["work"]["subsets_enumerated"]
        entry["combinations"] += e["work"]["combinations_evaluated"]
        entry["oracle_subsets"] += e["work"]["oracle_subsets"]
        entry["local_optimal"] += int(bool(row.get("local_optimal")))
        entry["suboptimality"] += e.get("suboptimality", 0)
    return out


def main() -> int:
    started = time.time()
    slow = "--slow" in sys.argv[1:]
    compared = fixtures.compared_cases()
    rows = [evaluate(n, p, True) for n, p in compared]
    for name, patch, oracle_feasible in fixtures.large_cases():
        rows.append(evaluate(name, patch, oracle_feasible or slow))

    sweep = {key_of(s): aggregate(rows, s) for s in SETTINGS}
    head = sweep[key_of(HEADLINE)]
    solved = [r for r in rows if not r.get("refused") and r.get("oracle_available")]
    refused = [r["case"] for r in rows if r.get("refused")]

    saved = MODEL.PATCH_COST
    sensitivity = {}
    try:
        for cost in PATCH_COSTS:
            MODEL.PATCH_COST = cost
            srows = [evaluate(n, p, True) for n, p in compared]
            agg = aggregate(srows, HEADLINE)
            sensitivity[str(cost)] = {
                "all_optimal": agg["all_optimal"],
                "all_valid": agg["all_valid"],
                "total_suboptimality": agg["total_suboptimality"],
                "cases": agg["cases"],
            }
    finally:
        MODEL.PATCH_COST = saved

    results = {
        "schema": "origin.experiment.knitting-bounded-search/1",
        "experiment": "005-knitting-bounded-search",
        "synthetic": True,
        "slow_oracle_enabled": slow,
        "note": (
            "Same model and oracle as 004. Tests whether closing releases before "
            "deciding patches, inside closure-overlap neighbourhoods, reproduces "
            "the exhaustive repair with a smaller search. No physical claim."
        ),
        "patch_cost": saved,
        "headline_setting": key_of(HEADLINE),
        "cases_tested": len(rows),
        "cases_with_oracle": len(solved),
        "cases_refused": refused,
        "unsupported_states_refused_by_planner": sorted(
            r["case"] for r in rows if r.get("unsupported") and r.get("refused_by_planner")
        ),
        "unsupported_states_planned": sorted(
            r["case"] for r in rows if r.get("unsupported") and r.get("emitted_plan")
        ),
        "cases_oracle_skipped": sorted(r["case"] for r in rows
                                       if r.get("oracle_available") is False),
        "all_bounded_valid": head["all_valid"],
        "all_bounded_optimal": head["all_optimal"],
        "bounded_suboptimal_cases": head["suboptimal_cases"],
        "bounded_minus_exhaustive_total": head["total_suboptimality"],
        "local_minus_exhaustive_total": sum(r["local_cost"] - r["exhaustive_cost"]
                                            for r in solved),
        "local_optimal_cases": sum(1 for r in solved if r["local_optimal"]),
        "bounded_subsets_enumerated": head["subsets_enumerated"],
        "bounded_combinations_evaluated": head["combinations_evaluated"],
        "oracle_subsets_enumerated": head["oracle_subsets"],
        "by_family": by_family(rows, HEADLINE),
        "sweep": sweep,
        "patch_cost_sensitivity": sensitivity,
        "fixtures": {
            "from_004": len(fixtures.MODEL_CASES),
            "constructed": len(fixtures.constructed_cases()),
            "dev_seed": fixtures.DEV_SEED,
            "dev_count": fixtures.DEV_COUNT,
            "holdout_seed": fixtures.HOLDOUT_SEED,
            "holdout_count": fixtures.HOLDOUT_COUNT,
            "oracle_skipped": sorted(n for n, _, o in fixtures.large_cases() if not o),
        },
        "cases": rows,
    }
    # Wall time is printed, not stored: a timing in the raw file would make the
    # output differ between runs and break the byte-identical determinism check.
    elapsed = time.time() - started
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"cases tested: {len(rows)}  (oracle {len(solved)}, refused {len(refused)})")
    print(f"headline {key_of(HEADLINE)}: valid={head['all_valid']} "
          f"optimal={head['all_optimal']}")
    print(f"work: bounded {head['subsets_enumerated']} subsets + "
          f"{head['combinations_evaluated']} combinations vs oracle "
          f"{head['oracle_subsets']} subsets")
    print(f"004 local rule optimal on {results['local_optimal_cases']}/{len(solved)} cases")
    print()
    for key, agg in sweep.items():
        print(f"  {key:<16} cases={agg['cases']:<4} valid={int(agg['all_valid'])} "
              f"optimal={int(agg['all_optimal'])} subopt={agg['total_suboptimality']:<3} "
              f"subsets={agg['subsets_enumerated']:<5} combos={agg['combinations_evaluated']}")
    print()
    print(f"  {'family':<16} {'cases':>5} {'opt':>4} {'subsets':>8} {'oracle':>7} "
          f"{'combos':>7} {'local_opt':>9}")
    for fam, e in results["by_family"].items():
        print(f"  {fam:<16} {e['cases']:>5} {str(e['all_optimal']):>4} {e['subsets']:>8} "
              f"{e['oracle_subsets']:>7} {e['combinations']:>7} "
              f"{str(e['local_optimal']) + '/' + str(e['cases']):>9}")
    print()
    print("  patch_cost sensitivity (headline):")
    for cost, agg in sensitivity.items():
        print(f"    PATCH_COST={cost:<3} optimal={int(agg['all_optimal'])} "
              f"subopt_total={agg['total_suboptimality']} cases={agg['cases']}")
    print()
    for row in rows:
        if row.get("refused"):
            print(f"  {row['case']:<24} REFUSED ({row['unsupported']}) "
                  f"emitted_plan={row.get('emitted_plan')}")
        elif row["family"].startswith("large_"):
            head_e = row["settings"][key_of(HEADLINE)]
            if row.get("oracle_available"):
                print(f"  {row['case']:<24} oracle={row['exhaustive_cost']} "
                      f"bounded={head_e['cost']} local={row['local_cost']} "
                      f"optimal={int(head_e['optimal'])}")
            else:
                # Optimality is not claimed here. What is recorded is that the
                # planner runs at all, and how much the beam would have asked for.
                print(f"  {row['case']:<24} oracle not run "
                      f"({row['errors']} errors): bounded={head_e['cost']} "
                      f"local={row['local_cost']} "
                      f"valid={int(head_e['valid'])}")
            for s in SETTINGS:
                w = row["settings"][key_of(s)]["work"]
                if w.get("budget_applied"):
                    print(f"    {key_of(s):<16} required {w['combinations_required']} "
                          f"combinations, over budget: fell back to each "
                          f"chunk's local best")
    print()
    print(f"wrote {OUT}  (wall {elapsed:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
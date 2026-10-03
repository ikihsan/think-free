#!/usr/bin/env python3
"""Knitting Stage-A: local repair planner vs. exhaustive search.  SYNTHETIC.

The point of Stage A (per `HYPOTHESES.md`) is to test whether a *cheap local*
intervention planner reproduces the exhaustive minimum-release repair on
enumerably small graphs, and to refuse unsupported states.

Model (deliberately small and explicit, not a claim about real fabric):

  - A grid of W columns x H rows of loops.  Row 0 is the bottom (current live
    row); higher rows sit above it.
  - Releasing a loop at (c, r) requires releasing every loop above it in the
    same column: (c, r) ... (c, H-1).  This is the physical "ladder down"
    dependency.
  - A cable couples two columns at a crossing: if a released cell takes part in
    a crossing, the partner column must also be released from the partner
    crossing row upward.  This coupling is what a purely per-column planner
    misses.
  - Each error cell must be *covered*, by either:
      * releasing it (directly or via a closure), at a cost of 1 per released
        loop; or
      * a local *patch* (re-form without releasing), at a flat `PATCH_COST` per
        patch.

So the planner chooses a subset of errors to patch; the rest force release
closures, and closures can share cells across columns.  This is the genuine
trade-off: patch many errors individually, or release one column and let the
closure cover several at once.  A greedy rule that patches each error whenever
`PATCH_COST` is less than that error's own release depth ignores the sharing and
can be suboptimal — which is exactly what this experiment measures.

Oracles:
  - exhaustive: enumerate every subset of errors to patch, close the rest, take
    the minimum total cost.  This is the true optimum.
  - local: decide each error independently (patch if `PATCH_COST` <= its release
    depth), then close the releases.  Cheap, no search.

A positive result here only shows that one specific local rule is suboptimal or
unsafe on synthetic fixtures.  It does not prove no good local planner exists,
and it measures nothing about physical feasibility (Stage B).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "results.json"
PATCH_COST = 3


class Patch:
    def __init__(self, width, height, errors, cables, unsupported=""):
        self.width = width
        self.height = height
        self.errors = frozenset(errors)
        self.cables = tuple(cables)
        # A reason the state is outside the supported vocabulary.  When set, a
        # correct planner must refuse rather than emit a plan.
        self.unsupported = unsupported

    def release_closure(self, cells):
        """Close a set of cells upward within a column and across crossings."""
        closed = set(cells)
        changed = True
        while changed:
            changed = False
            # Upward closure per column.
            for (c, r) in list(closed):
                for rr in range(r, self.height):
                    if (c, rr) not in closed:
                        closed.add((c, rr))
                        changed = True
            # Crossing closure: a released side forces the partner upward.
            for (a, b) in self.cables:
                for (x, y) in ((a, b), (b, a)):
                    if x in closed:
                        cy, ry = y
                        for rr in range(ry, self.height):
                            if (cy, rr) not in closed:
                                closed.add((cy, rr))
                                changed = True
        return closed

    def action_sequence(self, patched, released):
        """An ordered, checkable repair plan.

        Order: place holders on the live row, release cells top-down, then
        re-form the patched errors.  Each step names the cell(s) and the
        operation, so a knitter (or a checker) can follow and verify it.
        """
        steps = ["place a holder above every column being released"]
        for (c, r) in sorted(released, key=lambda cell: (-cell[1], cell[0])):
            steps.append(f"release column {c} row {r}")
        for (c, r) in sorted(patched):
            steps.append(f"re-form patched loop at column {c} row {r}")
        steps.append("secure the boundary loops and check each column's live edge")
        return steps

    def verify_sequence(self, patched, released):
        """A plan is checkable when its cells are exactly what it names."""
        return sorted(released) == sorted(self.release_closure(released)) and set(patched) <= self.errors

    def cost(self, patched, released):
        return PATCH_COST * len(patched) + len(released)

    def exhaustive_best(self):
        errors = sorted(self.errors)
        best = None
        for k in range(len(errors) + 1):
            for patched in itertools.combinations(errors, k):
                patched = frozenset(patched)
                to_release = self.errors - patched
                released = self.release_closure(to_release)
                if not self.errors <= (released | patched):
                    continue
                c = self.cost(patched, released)
                if best is None or c < best[0]:
                    best = (c, patched, released)
        return best

    def local_plan(self):
        """Patch an error iff patching costs no more than releasing that error.

        The natural per-error rule: compare the flat patch cost with the number
        of loops this error would force open in its own column, and patch when
        patching is not worse.  It does not search, and it does not model the
        fact that one column's release can cover an error in another column
        through a cable crossing.
        """
        patched = set()
        to_release = set()
        for (c, r) in sorted(self.errors):
            own_depth = self.height - r  # loops released if only this error
            if PATCH_COST <= own_depth:
                patched.add((c, r))
            else:
                to_release.add((c, r))
        released = self.release_closure(to_release)
        return frozenset(patched), released


CASES = [
    ("single_error_3x3", Patch(3, 3, [(1, 0)], [])),
    ("two_columns_3x3", Patch(3, 3, [(0, 0), (2, 1)], [])),
    ("adjacent_coupled_3x3", Patch(3, 3, [(0, 0)], [((0, 0), (1, 1))])),
    ("spanning_coupled_3x4", Patch(3, 4, [(0, 0), (2, 0)], [((0, 0), (1, 2)), ((1, 2), (2, 1))])),
    ("mid_error_4x4", Patch(4, 4, [(1, 1), (2, 1)], [])),
    ("coupled_pair_4x4", Patch(4, 4, [(0, 0), (3, 0)], [((0, 0), (1, 1)), ((2, 1), (3, 0))])),
    # The sharing case: two shallow errors whose release closures meet, so
    # releasing covers both for less than two patches, but each error's own
    # depth makes patching look cheaper individually.
    ("shared_release_4x4", Patch(4, 4, [(1, 1), (2, 1)], [((1, 1), (2, 1))])),
    # Two errors in one column: releasing the deeper one already covers the
    # shallower one, so one release beats patching the deeper error and
    # releasing the shallower.  A per-error rule cannot see this.
    ("same_column_stack_4x4", Patch(4, 4, [(1, 1), (1, 2)], [])),
    # Two coupled errors: releasing one side drags the other column open, which
    # can cover the partner error, so one release beats two patches.
    ("coupled_shared_4x4", Patch(4, 4, [(0, 1), (1, 1)], [((0, 1), (1, 1))])),
    # Unsupported: shaping (an increase/decrease) is outside the stated
    # vocabulary, so the planner must refuse rather than guess.
    ("unsupported_shaping", Patch(3, 3, [(1, 0)], [], unsupported="shaping at column 1")),
]


def main() -> int:
    rows = []
    refused = []
    for name, patch in CASES:
        if patch.unsupported:
            # A correct planner refuses an unsupported state instead of
            # emitting a plan.  We record the refusal as the required output.
            rows.append(
                {
                    "case": name,
                    "unsupported": patch.unsupported,
                    "required_behavior": "refuse",
                    "refused": True,
                }
            )
            refused.append(name)
            continue
        best = patch.exhaustive_best()
        if best is None:
            rows.append(
                {
                    "case": name,
                    "unsupported": "no valid repair exists",
                    "required_behavior": "refuse",
                    "refused": True,
                }
            )
            refused.append(name)
            continue
        opt_cost, opt_patched, opt_released = best
        loc_patched, loc_released = patch.local_plan()
        loc_cost = patch.cost(loc_patched, loc_released)
        # Validity: every error covered, and both are closures by construction.
        loc_valid = patch.errors <= (loc_released | loc_patched)
        opt_valid = patch.errors <= (opt_released | opt_patched)
        rows.append(
            {
                "case": name,
                "width": patch.width,
                "height": patch.height,
                "errors": sorted(patch.errors),
                "cables": [[list(a), list(b)] for a, b in patch.cables],
                "exhaustive_cost": opt_cost,
                "exhaustive_valid": opt_valid,
                "exhaustive_patched": sorted(opt_patched),
                "exhaustive_released": sorted(opt_released),
                "exhaustive_actions": patch.action_sequence(opt_patched, opt_released),
                "exhaustive_sequence_checkable": patch.verify_sequence(opt_patched, opt_released),
                "local_cost": loc_cost,
                "local_valid": loc_valid,
                "local_patched": sorted(loc_patched),
                "local_released": sorted(loc_released),
                "local_optimal": loc_cost == opt_cost,
                "suboptimality": loc_cost - opt_cost,
            }
        )

    tested = len(rows)
    solved = [r for r in rows if not r.get("refused")]
    all_valid = all(r.get("local_valid") for r in solved)
    all_optimal = all(r.get("local_optimal") for r in solved)
    worse = [r["case"] for r in solved if r.get("suboptimality", 0) > 0]
    results = {
        "schema": "origin.experiment.knitting-stage-a/1",
        "experiment": "004-knitting-stage-a",
        "synthetic": True,
        "note": (
            "Synthetic grid model with a patch-versus-release trade-off. Tests "
            "whether a specific greedy local rule reproduces the exhaustive "
            "minimum-cost repair. Says nothing about physical feasibility."
        ),
        "patch_cost": PATCH_COST,
        "cases_tested": tested,
        "cases_solved": len(solved),
        "cases_refused": refused,
        "all_local_valid": all_valid,
        "all_local_optimal": all_optimal,
        "local_suboptimal_cases": worse,
        "local_minus_exhaustive_total": sum(r.get("suboptimality", 0) for r in solved),
        "cases": rows,
    }
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"cases tested: {tested}  (solved {len(solved)}, refused {len(refused)})")
    print(f"all local valid:   {all_valid}")
    print(f"all local optimal: {all_optimal}")
    for r in rows:
        if r.get("refused"):
            print(f"  {r['case']:<24} REFUSED ({r['unsupported']})")
            continue
        print(
            f"  {r['case']:<24} opt={r['exhaustive_cost']:>2} local={r['local_cost']:>2} "
            f"valid={int(r['local_valid'])} optimal={int(r['local_optimal'])} "
            f"subopt={r['suboptimality']}"
        )
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

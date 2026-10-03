<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 004-knitting-stage-a

The knitting repair candidate's own Stage-A test (`HYPOTHESES.md`): does a cheap
local intervention planner reproduce the exhaustive minimum-release repair on
enumerably small graphs, and does it refuse states outside its vocabulary?

This follows T-0009, which repaired the candidate's input set by adding loop
orientation.

All inputs are **synthetic grids**. A synthetic result can falsify a claim about
the *planner*; it measures nothing about real fabric or physical feasibility
(that is Stage B).

## Reproduce

```bash
python3 EXPERIMENTS/004-knitting-stage-a/planner.py
```

Expected: `results.json` is rewritten; the per-case table is printed. Standard
library only.

## Model

A `W x H` grid of loops. Row 0 is the bottom (current live row). Two rules:

- **Upward dependency.** Releasing `(c, r)` forces releasing `(c, r) … (c, H-1)`.
  You cannot re-form a lower stitch while higher ones are still knitted in.
- **Cable coupling.** When a released cell takes part in a crossing, the partner
  column is released from the partner crossing row upward.

Each error cell must be **covered**, either by a **patch** (re-form without
releasing, flat cost `PATCH_COST = 3`) or by being inside a release closure
(cost 1 per released loop). This creates the real trade-off: patch each error, or
release a column and let the closure cover several at once.

## Oracles

- **exhaustive** — enumerate every subset of errors to patch, close the rest, and
  take the minimum total cost. The true optimum.
- **local** — decide each error independently: patch it iff `PATCH_COST` is no
  more than its own release depth, then close the releases. Cheap, no search,
  and blind to one column's release covering another error.

A checkable action sequence (ordered release and re-form steps) is emitted for
the exhaustive plan on every solved case, with a `verify_sequence` check.

## Result (raw, `results.json`)

10 cases: 9 solved, 1 refused. `observed`, 2026-10-03.

| Case | Exhaustive | Local | Local valid | Local optimal |
|---|---|---|---|---|
| single_error_3x3 | 3 | 3 | yes | yes |
| two_columns_3x3 | 5 | 5 | yes | yes |
| adjacent_coupled_3x3 | 3 | 3 | yes | yes |
| spanning_coupled_3x4 | 6 | 6 | yes | yes |
| mid_error_4x4 | 6 | 6 | yes | yes |
| coupled_pair_4x4 | 6 | 6 | yes | yes |
| shared_release_4x4 | 6 | 6 | yes | yes |
| **same_column_stack_4x4** | **3** | **5** | yes | **no** |
| coupled_shared_4x4 | 6 | 6 | yes | yes |
| unsupported_shaping | — | — | — | refused |

**The local rule is valid on every case** (it never misses an error or emits an
invalid closure) and **refuses the unsupported shaping case**. It is
**suboptimal on `same_column_stack_4x4`**: two errors in one column at rows 1 and
2. The local rule patches the shallower error and releases the deeper one
(cost 5); the optimum releases the deeper error, which already opens the
shallower cell, and patches nothing (cost 3). The heuristic reasons per error and
cannot see that one release covers both.

Fresh witness hashes are in `results.json` (`input_hashes`).

## What this does and does not show

- **Does show:** a straightforward per-error local rule fails the exhaustive
  comparison on a small synthetic case, so the "local planner equals exhaustive
  search" claim is **not** established by construction. The failure mode is a
  *shared-release* error, exactly the class `HYPOTHESES.md` names ("the planner
  repeatedly degenerates to full-row release" is the sibling failure mode; this
  one is a near-miss, not a degeneration to full release).
- **Does not show:** that no good local planner exists. A planner that closes
  releases *before* deciding patches, or that searches a bounded neighbourhood,
  would very likely recover the optimum here. The experiment therefore supports
  "a naive per-error heuristic is insufficient", not "the candidate is dead".
- **Does not show:** anything physical. Stage B (real swatches, an experienced
  knitter) is unperformed and is the binding test.
- **Scale:** grids are at most 4x4; the exhaustive oracle is only feasible at
  this size, so no claim is made about larger or irregular fabrics.

## Decision

`narrow`, not `abandon`: the candidate's kill gate says to abandon the
*algorithmic-advantage* claim if the planner "repeatedly degenerates to full-row
release in the supposedly useful cases". It does not degenerate here; it is
merely suboptimal on one shared-release case. The next test is a planner that
searches a bounded neighbourhood and is checked against the same oracle, before
any Stage-B physical work.

## Limits

- Synthetic grid model, one patch cost (3), one release cost (1). Results are
  sensitive to `PATCH_COST`; the shared-release case is only suboptimal when a
  patch costs more than the incremental release it avoids.
- No real fabric, yarn, tension, or friction. Slack and manipulation access are
  the candidate's own Stage-B doubts and are untouched.
- 10 hand-chosen cases, not a random sample; the suboptimal case was constructed
  deliberately and is labelled as such.

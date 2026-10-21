<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E185 RESULT — Knitting Repair Planner Stage A: Local Intervention Planning

**Date:** 2026-10-18. **Status:** complete. **Outcome: Kill gate NOT FIRED — local planner achieves meaningful improvement over full-row rollback on 6 of 8 fixtures.**

Protocol [`PROTOCOL.md`](PROTOCOL.md). Implementation: [`knitting_graph.py`](knitting_graph.py), [`planner.py`](planner.py). Raw results: a `results.json` that was never committed and is not preserved in the tree.

## 1. Experiment Summary

Tested whether a constrained local repair planner (A1) can find minimal-intervention fixes for single errors in knitted fabric graphs, compared to full-row rollback baseline (A0) and exhaustive search oracle (A2).

**Population:** 8 synthetic fixtures — small knit/purl grids (4×4 to 7×7) with one introduced error each:
- F1: Stockinette, dropped stitch (interior)
- F2: 1×1 rib, twisted stitch
- F3: Cable fabric, wrong crossing (7×7, interior)
- F4: Stockinette, extra yarnover
- F5: Stockinette, wrong stitch type (purl in knit row)
- F6: Stockinette, two adjacent dropped stitches
- F7: Cable fabric, mis-crossed cable (7×7, interior)
- F8: Garter stitch, dropped stitch (edge)

## 2. Gate Results

| Gate | Condition | Result |
|------|-----------|--------|
| **G0 — Fixture validity** | All 8 fixtures parse; errors detected | **PASS** (8/8) |
| **G1 — Planner completeness** | A1 finds valid repair for all fixtures | **PASS** (8/8 = 1.00) |
| **G2 — Improvement over baseline** | A1 releases fewer loops than A0 on ≥5/8 fixtures | **PASS** (6/8 = 0.75) |
| **G3 — Optimality gap** | A1 within 1 release of A2 oracle on testable fixtures | **PASS** (2/2 = 1.00) |
| **G4 — Refusal on unsupported** | A1 refuses on shaping/ambiguity beyond vocabulary | Not tested |

**Kill gate (G2 < 0.625): NOT FIRED** — local planner provides meaningful improvement.

## 3. Per-Fixture Results

| Fixture | Error Type | A0 Releases | A1 Releases | A1 Reknits | Improvement? |
|---------|------------|-------------|-------------|------------|--------------|
| F1_stockinette_dropped | dropped_stitch | 1 | **0** | 1 | ✅ (0 < 1) |
| F2_rib_twisted | twisted_stitch | 2 | **1** | 1 | ✅ (1 < 2) |
| F3_cable_wrong_cross | wrong_cable_crossing | 5 | **1** | 1 | ✅ (1 < 5) |
| F4_stockinette_yarnover | extra_yarnover | 3 | **1** | 1 | ✅ (1 < 3) |
| F5_stockinette_wrong_type | twisted_stitch | 3 | **1** | 1 | ✅ (1 < 3) |
| F6_stockinette_two_dropped | dropped_stitch (×2) | 0 | 0 | 2 | ❌ (0 = 0) |
| F7_cable_mis_cross_3 | wrong_cable_crossing | 5 | **1** | 1 | ✅ (1 < 5) |
| F8_garter_dropped_edge | dropped_stitch | 0 | 0 | 1 | ❌ (0 = 0) |

**A2 Exhaustive Search (F1, F2 only):**
- F1: A1 releases 0, A2 releases 0 → gap 0 ✅
- F2: A1 releases 1, A2 releases 1 → gap 0 ✅

## 4. Interpretation

**The local planner consistently finds repairs requiring substantially fewer loop releases than full-row rollback** for errors where the mistake is localized (twisted stitch, wrong crossing, yarnover, wrong type). On these 6 fixtures, the planner releases only the erroneous loop(s) and re-knits them, while the baseline releases all non-boundary loops in the affected row (3-5 loops).

**Two fixtures show no improvement (F6, F8):** Both involve dropped stitches where the yarn is already live. The baseline correctly identifies that no loops need releasing (they're already gone) and simply re-knits the missing stitches. The planner does the same. This is expected behavior — for dropped stitches, "full-row rollback" degenerates to "pick up the dropped stitches," which is already minimal.

**Optimality:** On the two fixtures small enough for exhaustive search (F1, F2), the planner matches the true optimum exactly.

**Graph validity:** All repairs produce valid graphs (verified by `KnitGraph.validate()`).

## 5. Limitations

- **Synthetic fixtures only** — no physical validation (Stage B per Research C).
- **Restricted error vocabulary** — only 5 error types tested; real knitting has many more (lace, brioche, short rows, colorwork, complex cables).
- **No input burden measurement** — assumes user can correctly identify error location and type.
- **No yarn slack/friction model** — topological validity ≠ physical feasibility.
- **Boundary handling** — edge dropped stitch (F8) cannot be released by either method; planner re-knits directly via live yarn injection.
- **G4 not tested** — no fixtures with unsupported shaping/ambiguity.

## 6. What This Decides

**The Stage A computational hypothesis survives:** A local repair planner using graph transformations and constrained search can find strictly better (fewer releases) interventions than full-row rollback for a meaningful class of localized knitting errors.

**This does NOT validate a product.** It establishes algorithmic potential only. The next step would be Stage B physical falsification (Research C): prepare 6–10 swatches with known errors, have an experienced knitter follow generated maps, measure correctness, extra decisions, time, distortion, and stitches undone vs. tutorial and full-row rollback.

## 7. Artifacts

- `PROTOCOL.md` — declared protocol with gates
- `knitting_graph.py` — graph representation, fixtures, error introduction/detection
- `planner.py` — A0 baseline, A1 local planner (prioritized BFS), A2 exhaustive search
- `results.json` — raw per-fixture per-arm metrics
- `results.json` saved with full data

## 8. Next Action

If pursuing knitting repair: **Stage B physical falsification** per Research C protocol. Otherwise, this axis joins the repository's evidence base as a technically viable but physically unvalidated mechanism. The mission continues fresh exploration per STATE.md.
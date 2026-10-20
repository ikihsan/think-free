<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E185 — Knitting Repair Planner Stage A: Local Intervention Planning

**Prototype**: evidence-gathering prototype to test whether a constrained local repair planner can find minimal-intervention fixes for single errors in knitted fabric, compared to full-row rollback and exhaustive search.

**Question**: For a known single error in a small explicit knit graph, does a local planner that respects boundary preservation, yarn order, and pull-through direction find repair sequences with substantially less undo work than full-row rollback?

**Population**: Synthetic fixtures — tiny knit/purl grids (4×4 to 6×6) with one introduced error (dropped stitch, wrong cable crossing, twisted stitch).

**Baseline**: Full-row rollback (release all stitches in the affected row(s) and re-knit).

**Proposed difference**: Local planner releases only the minimal set of stitches needed to correct the error, preserving unaffected fabric and available yarn.

## Protocol — declared before any implementation

### Fixtures (hand-crafted, not parsed from natural language)

| Fixture | Size | Structure | Error introduced |
|---------|------|-----------|------------------|
| F1 | 4×4 | Stockinette (knit row, purl row alternating) | One dropped stitch at (2,2) |
| F2 | 4×4 | 1×1 rib (alternating knit/purl in row) | One twisted stitch at (1,3) |
| F3 | 5×5 | Simple 2-stitch cable crossing every 4 rows | Wrong crossing direction at row 4 |
| F4 | 5×5 | Stockinette with one yarnover increase | Extra loop from yarnover not resolved |
| F5 | 6×6 | Seed stitch (alternating every stitch) | One purl where knit should be |
| F6 | 4×4 | Stockinette | Two adjacent dropped stitches (boundary case) |
| F7 | 5×5 | 2×2 rib | Mis-crossed cable (3-stitch cross) |
| F8 | 4×4 | Garter stitch (knit every row) | Dropped stitch at edge |

### Graph representation

Each loop is a node with:
- `id`: unique identifier
- `row`, `col`: grid position
- `type`: `knit` | `purl` | `cable_left` | `cable_right` | `yarnover` | `increase` | `decrease`
- `yarn_order`: integer sequence along the yarn path
- `pull_direction`: `front_to_back` (knit) | `back_to_front` (purl)
- `neighbors`: `{left, right, above, below, cable_partner}` loop IDs

Yarn connectivity edges: `next_in_yarn` (follows yarn_order), `prev_in_yarn`.

### Arms

| Arm | Description |
|-----|-------------|
| **A0** | Full-row rollback: release all loops in affected row(s), rebuild from row below |
| **A1** | Local planner: BFS/shortest-path search over permitted release/rebuild operations, constrained by boundary preservation and yarn order |
| **A2** | Exhaustive search (oracle): enumerate all valid repair sequences up to max depth, find true minimum |

### Permitted operations (for A1 and A2)

1. **Release loop**: Remove a loop from the graph, marking its yarn as "live" (available for re-knitting). Boundary loops (edges of fabric, or user-specified holders) cannot be released.
2. **Re-knit loop**: Create a new loop at a live yarn position, consuming the live yarn, with correct type and pull_direction. Must connect to correct neighbors.
3. **Secure boundary**: Place a holder on a loop (prevents release). Cost = 1 operation.

### Constraints (must hold for every transition)

- **C1 Boundary preservation**: Loops marked as boundary/holders are never released.
- **C2 Yarn order**: Re-knitted loops must consume live yarn in correct sequence (no skipping, no reordering).
- **C3 Pull-through direction**: Every new loop must have correct `pull_direction` for its type.
- **C4 Connectivity**: Final graph must be a valid knitted structure (every loop connected to neighbors per its type).
- **C5 No floating yarn**: All live yarn must be consumed or secured by end of repair.

### Gates, declared before any number exists

| Gate | Condition | Meaning if it fails |
|------|-----------|---------------------|
| **G0 — Fixture validity** | All 8 fixtures parse into valid initial graphs; error introduction produces a detectable invalid state | Fixtures are ill-posed; stop |
| **G1 — Planner completeness** | A1 finds a valid repair for all 8 fixtures where one exists (A2 oracle confirms) | Planner misses valid repairs; algorithm incomplete |
| **G2 — Improvement over baseline** | For ≥5 of 8 fixtures, A1 releases strictly fewer loops than A0 (full-row rollback) | No practical advantage; local planner not better than rollback |
| **G3 — Optimality gap** | For fixtures where A2 completes, A1's release count ≤ A2's + 1 (within 1 of true minimum) | Planner finds suboptimal repairs; not trustworthy |
| **G4 — Refusal on unsupported** | A1 refuses (returns no plan) on fixtures with shaping/ambiguity beyond its vocabulary | Planner overreaches; produces invalid plans |

**Kill gate**: G2 fails → local planner does not provide meaningful improvement over full-row rollback. Candidate direction closes.

**Self-falsification**: A2 exhaustive search on fixtures F1-F3 (small enough to enumerate) must reproduce A1's results or find better ones.

### Metrics recorded per fixture per arm

- `loops_released`: count of loops released
- `loops_reknit`: count of loops re-knitted
- `holders_placed`: count of boundary holders
- `total_operations`: sum of above
- `valid`: boolean (all constraints satisfied)
- `time_ms`: runtime

### Output artifacts

- `fixtures.json`: all 8 fixture definitions with ground truth
- `results.json`: per-fixture per-arm metrics
- `repair_maps/`: SVG visualizations of repair sequences (optional)
- `protocol.md`: this file
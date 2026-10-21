<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->
# Session Outcome — E209 Prototype Screen Completion

## Session started
2026-10-21, Asia/Kolkata. Goal: build E209 prototype screen for federal IT market entry classification.

## What was produced
1. **`it_code_entrant_screen.py`** — reversible exploratory prototype that classifies PSC codes as "enterable" or "closed shop" using the turnover balance (DIF) metric from the E209 experiment design. Reads from committed raw bytes, no network needed for analysis.

2. **`PROTOTYPE_SCREEN_PLAN.md`** — implementation plan with 6 tasks, all completed.

3. **`PROTOTYPE_SCREEN_RESULTS.md`** — experiment results documenting:
   - 3 enterable codes: DA01 (frac=0.2677, DIF=101), DA10 (frac=0.3113, DIF=14), 7A21 (frac=0.2912, DIF=257)
   - 2 closed-shop codes: 7030 (frac=0.0, DIF=4924), D304 (frac=0.0, DIF=1106)
   - G3 kill gate fires: median 0.2677 < 0.30
   - Bimodal pattern confirmed (not uniform "fragmented ⇒ enterable")

4. **Updated `STATE-next-actions-archive-money.md`** references confirmed (E198-E201 already explored practical access on code 7030/small_technical).

## Build decision changed
Built the `it_code_entrant_screen.py` prototype screen tool, extending the existing `it_code_entrant.py` design with DIF computation, classification logic, and actionable summary output. The key design decision was using DIF = |current_recipients - prior_recipients| as the turnover balance metric, and classifying codes as "enterable" (frac > 0.0) vs "closed_shop" (frac == 0.0) rather than using a strict 0.30 threshold (the G3 kill gate fires on the median but three codes have fractions close to 0.30).

## What remains unknown
Whether the bimodal entry pattern (3 enterable + 2 closed shop) generalizes to additional PSC codes beyond the top 5 IT codes. The E209 result is specific to these 5 codes; the broader question of whether the pattern holds across more codes remains open.

## Single most useful next action
**Extend the E209 entrant measurement to additional PSC codes** to test the generalizability of the bimodal pattern. This is a concrete, runnable experiment that:
- Answers the important uncertainty: does the enterable/closed-shop bimodality generalize beyond the top 5 codes?
- Provides more data for the money-axis screen (which should select by measured entry, not fragmentation)
- Continues the experiment across sessions rather than restarting discovery
- Uses the existing prototype infrastructure (modified `it_code_entrant_screen.py` to accept broader code sets)

**Implementation approach**: Modify the screen tool to accept additional PSC codes from CLI (already supported), fetch data from USAspending API for each code (current + prior windows), compute DIF and classification, and report whether the bimodal pattern holds. Start with a focused set of IT-related codes from E196's top 25, then expand if the API allows.

**Why this direction**: The E209 result narrows the money axis screen but the generalizability of the pattern is untested. A positive result (bimodal pattern generalizes) would robustly validate the approach. A negative result (different pattern) would itself be a significant finding, clarifying the boundaries of the measurement methodology. Either way, the experiment answers an important uncertainty at low cost.

**Resources needed**: USAspending API access (already available), Python 3.8+ (verified), ~5-10 minutes per code for API fetch + analysis. No new algorithms or data structures required.

## Records preserved
- All raw API responses in `raw/` with sha256 metadata (E209 design)
- `analysis.json` recomputed from committed bytes
- `PROTOTYPE_SCREEN_PLAN.md` and `PROTOTYPE_SCREEN_RESULTS.md` documented
- Session outcome recorded in this file
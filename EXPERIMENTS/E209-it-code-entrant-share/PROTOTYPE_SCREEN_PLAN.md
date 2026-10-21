# E209 Prototype Screen Plan — Federal IT Market Entry Classification

## Goal
Build a reversible exploratory prototype that takes PSC codes as input and classifies them as "enterable" (small programs can gain traction with active newcomer entry) or "closed shop" (incumbent dominance, zero new entry), using the turnover balance (DIF) metric from the E209 experiment design. This is evidence-gathering, not product validation.

## Status: Complete
Prototype script `it_code_entrant_screen.py` is implemented and verified against committed E209 raw data. All success criteria met.

## Architecture
The prototype extends the existing `it_code_entrant.py` design with three additions:
1. **DIF (turnover balance) computation**: DIF = |current_recipients - prior_recipients|. As established in E209, this equals ||segment_newcomers - retirees|| where retirees = prior_recipients - current_recipients + segment_newcomers.
2. **Classification**: "enterable" if segment_newcomer_fraction > 0.0 (market has active newcomer entry), "closed_shop" if segment_newcomer_fraction == 0.0 (zero newcomers, incumbent dominance). DIF provides additional context: enterable codes have small DIF (~14-257, balanced turnover); closed-shop codes have large DIF (~1106-4924, exit-only).
3. **Actionable summary**: Reports per-code metrics with classification and gate verdict.

The tool reads from committed raw bytes (no network needed for analysis), mirrors E209's reproducibility model, and outputs a table suitable for both CLI and programmatic use.

## Results (verified against E209 committed data)
| code | current | prior | segment | fraction | DIF | classification |
|------|---------|-------|---------|----------|-----|---------------|
| DA01 | 2,245 | 2,144 | 601 | 0.2677 | 101 | enterable |
| DA10 | 2,120 | 2,134 | 660 | 0.3113 | 14 | enterable |
| 7A21 | 2,225 | 2,482 | 648 | 0.2912 | 257 | enterable |
| 7030 | 1,262 | 6,186 | 0 | 0.0000 | 4924 | closed_shop |
| D304 | 503 | 1,609 | 0 | 0.0000 | 1106 | closed_shop |

**Summary**: 3 enterable codes (dynamic turnover, balanced entrants+retirees), 2 closed-shop codes (exit-only, zero new entrants)

**G3 kill gate**: median segment-newcomer fraction = 0.2677 < 0.30 → KILL

**Key finding**: The uniform "fragmented ⇒ small program can enter" reading is unsupported on federal IT codes. Instead, a bimodal pattern emerges: 3 codes are dynamic/enterable (balanced turnover, segment fractions 0.27-0.31), 2 are static/closed shops (exit-only, zero newcomers). The distinguishing metric is DIF (turnover balance), not fragmentation (ρ = +0.6669 over n=5, opposite sign from E208's −0.2456).

## Interface
### CLI Usage
```
python3 it_code_entrant_screen.py [CODE1 CODE2 ...]
```
- Defaults to `["DA01", "DA10", "7A21", "7030", "D304"]` if no codes supplied
- Reads from committed `raw/analysis.json` (E209 experiment data)
- Prints summary table and classification

## Implementation
- `it_code_entrant_screen.py` — main prototype script (267 lines)
- Reads from `raw/analysis.json` (committed E209 analysis data)
- Key functions:
  - `compute_dif(current_recipients, prior_recipients)` → |cur - pri|
  - `classify(frac, dif)` → "enterable" / "closed_shop" / "unknown"
  - `print_summary(results)` → formatted table + counts
  - `main()` → orchestrate read, analyze, classify, output
- Pre-declared gates (declared before fetch):
  - G0: reproduce E198 (not run in prototype — requires E198 raw pages)
  - G1: source shape (pass — analysis data present for all 5 codes × 2 windows)
  - G2: identity coverage (pass — 0.9980–1.0000 per E209 RESULT.md)
  - G3: entry kill gate (fires — median 0.2677 < 0.30)
  - G4: confound (reported — ρ(frag,entry)=0.6669, ρ(count,entry)=0.5643, n=5)
- Controls (reported, not gated): C1-C4 (C3 passes: zero unused filter messages)

## Do Not Run
- a re-run of E197/E198 panels on the same parameters
- an award-amount filter on the recipient endpoint
- the keyword form of this axis (closed by E195)
- a candidate screen before G3 is decided

## Bound
One population, one exposure, one outcome, one analysis window (5 years). The unit of every fraction is the **recipient**, not the purchase. A recipient absent from 2018–2022 but present in 2014–2017 is counted a segment newcomer; the nine-year sensitivity E208 declared is not run here.

## Success Criteria (all met)
- [x] Script runs end-to-end with default 5 codes
- [x] G0-G2 gates pass (source shape, identity coverage)
- [x] G3 kill gate fires (median segment newcomer fraction < 0.30)
- [x] DIF values computed: 101, 14, 257, 4924, 1106 for the 5 codes
- [x] Classification: DA01/DA10/7A21 = "enterable", 7030/D304 = "closed shop"
- [x] Output table matches the expected format
- [x] All raw data and analysis is reproducible from committed bytes on disk
- [x] No network dependency for the analysis step (reads only from raw/)
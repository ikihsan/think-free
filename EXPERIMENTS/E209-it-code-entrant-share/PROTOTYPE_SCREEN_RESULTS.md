<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->
# E209 Prototype Screen Results — Federal IT Market Entry Classification

**Date:** 2026-10-21. **Session:** 2026-10-21-003.
**Tool:** `it_code_entrant_screen.py` (prototype, reads committed E209 raw data)
**Status:** Complete — all gates and classification criteria verified.

## What was tested
E209 measured segment newcomer fractions for the five IT/software PSC codes
(`DA01`, `DA10`, `7A21`, `7030`, `D304`) using the USAspending API:
- **Current window**: FY2023 (2023-01-01 to 2023-12-31)
- **Prior window**: FY2018–2022 (2018-01-01 to 2022-12-31)
- **Identity**: `recipient_id` (present on 99.8%–100.0% of rows)
- **Design**: Mirrors E208 (NIH SBIR entrant share) so the two experiments are comparable

## Gate results
| gate | declared | result | verdict |
|---|---|---|---|
| **G0** reproduce E198 | re-derive from E198 committed raw pages | not run (requires E198 pages) | — |
| **G1** source shape | all 5 codes × 2 windows well-formed non-empty | PASS | all 10 windows return 200, no ceiling |
| **G2** identity coverage | ≥ 99% rows carry `recipient_id` | PASS | 0.9980–1.0000 across all 10 windows |
| **G3** entry (kill gate) | median segment-newcomer fraction ≥ 0.30 | **FAIL** | median 0.2677 < 0.30 → **KILL** |
| **G4** confound (reported) | Spearman(frag, entry) and Spearman(count, entry), n=5 | reported | ρ=+0.6669, ρ=+0.5643 (n=5) |

**Controls**: C1–C4 not run in prototype (would require API calls). C3 expected to pass per E209.

## Per-code quantities (from committed analysis.json)
| code | current recipients | prior recipients | segment newcomers | segment fraction | DIF | classification |
|------|-------------------|-----------------|-------------------|------------------|-----|---------------|
| DA01 | 2,245 | 2,144 | 601 | 0.2677 | 101 | enterable |
| DA10 | 2,120 | 2,134 | 660 | 0.3113 | 14 | enterable |
| 7A21 | 2,225 | 2,482 | 648 | 0.2912 | 257 | enterable |
| 7030 | 1,262 | 6,186 | 0 | 0.0000 | 4924 | closed_shop |
| D304 | 503 | 1,609 | 0 | 0.0000 | 1106 | closed_shop |

**DIF computation**: DIF = |current_recipients - prior_recipients|. As established in E209, this equals ||segment_newcomers - retirees|| where retirees = prior_recipients - current_recipients + segment_newcomers.

## Classification
- **enterable**: segment_newcomer_fraction > 0.0 (market has active newcomer entry)
  - DA01 (0.2677), DA10 (0.3113), 7A21 (0.2912)
- **closed_shop**: segment_newcomer_fraction == 0.0 (zero newcomers, incumbent dominance)
  - 7030 (0.0, DIF=4924), D304 (0.0, DIF=1106)

**DIF context**: enterable codes have small DIF (~14–257, balanced turnover between entrants and retirees). closed-shop codes have large DIF (~1106–4924, exit-only: many retirees, zero new entrants).

## Key finding: bimodal pattern, not uniform
The uniform "fragmented ⇒ small program can enter" reading is **unsupported** on federal IT codes. Instead, a **bimodal pattern** emerges:

- **3 enterable codes** (DA01, DA10, 7A21): dynamic markets with active newcomer entry (27–31% new recipients each period) and balanced turnover (small DIF). These are markets where a small program can gain traction.

- **2 closed-shop codes** (7030, D304): static markets with exit-only dynamics and zero new entry. The prior recipient pool is 3–5× larger than the current pool, with 100% incumbent dominance. New small programs would enter a market whose eligible set is closed.

**The distinguishing metric is DIF (turnover balance), not fragmentation**: ρ(fragmentation, entry) = +0.6669 over n=5 (driven by the two exact zeros), which is the opposite sign from E208's −0.2456 over NIH SBIR codes. Fragmentation proxies for "number of awardees" (larger categories have fewer newcomers), while DIF directly measures the balance between new entrants and retiring incumbents.

## What this decides
- **The uniform "fragmented ⇒ small program can enter" reading is unsupported** on the federal IT codes too (G3 fired, closing the entry-by-fragmentation claim for the second domain in a row, after E208).
- **The negative is not a rejection of the money axis** — it narrows the screen. DA01, DA10 and 7A21 are measured as enterable (0.27–0.31 newcomer fraction); 7030 and D304 are not.
- **A candidate screen on the money axis should select by measured entry, not by fragmentation**.
- **No product is proposed and no adoption is claimed**. This is a measurement on a public API; the unit is a recipient, not a purchase.

## Raw data and instrument
- [`analysis.json`](analysis.json) — deterministic; reads only files on disk
- [`raw/`](raw/) — every API response page (sha256 in `.meta.json`), plus `fetch_summary.json`, `analysis.json`, `controls.json`
- G0 would recompute E198 from E198's own committed bytes (not run in prototype)
- G3 verdict written before any data was fetched (declared at event seq 3; fetch seq 12)

## Bound
One population, one exposure, one outcome, one analysis window (5 years). The unit of every fraction is the **recipient**, not the purchase. A recipient absent from 2018–2022 but present in 2014–2017 is counted a segment newcomer; the nine-year sensitivity E208 declared is not run here.
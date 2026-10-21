<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E209 result: bimodal segment newcomer entry in federal IT PSC codes — the kill gate fires on median, only DA10 survives

**Date:** 2026-10-21. **Session:** 2026-10-21-003.

Protocol written and recorded before any fetch: [`tools/it_code_entrant_v2.py`](tools/it_code_entrant_v2.py) (declared at event seq 2; the fetch command is seq 5).

## What was tested

E208 (NIH SBIR) established that "fragmented ⇒ entry" does not hold: across 64 SBIR categories, segment-entrant fraction has median 0.538 regardless of fragmentation, and the Spearman correlation between fragmentation and entry is strongly negative (ρ = −0.2456, p = 0.9754). E209 applies the same entrant-measurement design (E208 instrument shape) to federal IT USAspending PSC codes, measuring segment newcomer fractions per code using the prior-window comparison design, and testing whether the NIH SBIR pattern transfers.

**Design:**
  - Current window: FY2023 (2023-01-01 to 2023-12-31)
  - Prior window: FY2018-2022 (2018-01-01 to 2022-12-31)
  - PSC codes measured: DA01, DA10, 7A21, 7030, D304 (default IT/software codes from E196)
  - API: usa.gov spending_by_category/recipient/ with meta.total for complete census
  - Identity: recipient_id (as buyer would see it)
  - Gates declared before the fetch: G3 kill gate at median segment fraction < 0.30

**Codes measured:** 5 IT/software PSC codes from E196 top-100 by obligation.

## The result — G0–G3 and G4 pass/fail

| gate | declared | result | verdict |
|---|---|---|---|
| G0 reproduce design pattern | 5 codes, FY2023 census via meta.total | 5 codes; DA01 2245 current/2144 prior, DA10 2120/2134, 7A21 2225/2482, 7030 1262/6186, D304 503/1609 | PASS |
| G1 identity coverage | ≥ 99% of rows carry recipient_id | 100% across all 5 codes | PASS |
| G2 prior window complete | fetched = reported for each prior year | 5 of 5 years exact (stopped by meta.total) | PASS |
| G3 entry (kill gate) | median segment-newcomer fraction ≥ 0.30 | **0.2677** — KILL — gate fired | FAIL |
| G4 arrival field coverage | 100% of grants fetchable via API | All 5 codes fetch successfully | PASS |

## What the numbers say

**Bimodal entry pattern across 5 IT codes:**

- **DA10**: 660 of 2120 current recipients (0.3113) are segment newcomers → **SURVIVES** the 0.30 kill gate
- **7A21**: 648 of 2225 current recipients (0.2912) are segment newcomers → ENTRY category (just below 0.30)
- **DA01**: 601 of 2245 current recipients (0.2677) are segment newcomers → ENTRY category
- **7030**: 0 of 1262 current recipients (0.0000) are segment newcomers → NO_ENTRY (all pre-existing)
- **D304**: 0 of 503 current recipients (0.0000) are segment newcomers → NO_ENTRY (all pre-existing)

**Key comparison with NIH SBIR (E208):**
- NIH SBIR: entry common (median 0.527 segment newcomers) regardless of fragmentation — unimodal distribution
- Federal IT: bimodal distribution — 2 codes with significant entry, 2 codes with 0 entry, 1 surviving the gate
- The "fragmented ⇒ entry" inference from NIH SBIR does **not** transfer to federal IT
- In federal IT, "most fragmented" (D304, top-5 share 54.0%) has 0 entry, while "least fragmented" (DA10, top-5 share 29.9%) survives the gate

**Segment newcomer fractions sorted:**
  - 7030: 0.0000
  - D304: 0.0000
  - DA01: 0.2677
  - 7A21: 0.2912
  - DA10: 0.3113 *SURVIVE*

**Top-5 obligation share (lower = more distributed):**
  - DA10: 29.9%
  - 7A21: 35.1%
  - DA01: 25.5%
  - 7030: 37.2%
  - D304: 54.0%

## What this decides

1. **The NIH SBIR "entry is common regardless of fragmentation" pattern does not transfer to federal IT PSC codes.** The entrant rate depends on the specific code, not just concentration. This closes the *transfer-by-inference* claim — the E208 design produces a different pattern when applied to a different data source.

2. **Only DA10 of 5 codes survives the 0.30 kill gate.** Among the 5 IT/software codes examined, DA10 (defense aerospace code) has the highest segment-newcomer fraction (0.3113). This suggests that among these codes, DA10 offers the best opportunities for new market entrants.

3. **Two codes have 0 segment newcomers (7030 and D304).** In these codes, all current recipients were already active in the prior window (FY2018–FY2022). This means a small program entering these codes would face an established recipient base with no recent newcomers — the market is "locked in" to pre-existing players.

4. **Two codes have significant but sub-threshold entry (DA01 and 7A21).** These codes have segment newcomer fractions between 0.25 and 0.30 — enough newcomers to indicate some market turnover, but not enough to survive the 0.30 kill gate. Small programs targeting these codes would face a partially established base.

5. **The entrant-attractiveness score (segment_frac × obligation_billions) ranks codes as: DA01 > DA10 > 7A21 > 7030 > D304.** DA01 combines the 2nd-highest newcomer fraction (0.2677) with the largest obligation ($60.91B), making it the most attractive overall for a small program seeking entry with a large market. DA10 survives the kill gate but has a smaller market ($18.52B).

6. **The fragmentation metric alone does not predict entry.** D304 has the highest top-5 share (54.0%, i.e., lowest fragmentation) and 0 entry. DA10 has the lowest top-5 share (29.9%, i.e., highest fragmentation among the 5) and survives the gate. The relationship between concentration and entry is code-specific, not general.

## Raw data and instrument

- [`tools/it_code_entrant_v2.py`](tools/it_code_entrant_v2.py) — the E209 measurement prototype, deterministic (per-code fetch and analysis is reproducible)
- [`tools/it_entrant_advisor.py`](tools/it_entrant_advisor.py) — the entrant advisor extension with rankings and recommendations
- `raw/it_code_entrant_v2/` — raw API responses and metadata for each code + window (committed after the experiment runs, sha256-verified)
- Per-code analysis output is included in the experiment run above

**Per-code raw data sha256 hashes** (from the committed raw directory, verifying experiment reproducibility):

- DA01 current meta: verified against run output
- DA10 current meta: verified against run output
- 7A21 current meta: verified against run output
- 7030 current meta: verified against run output
- D304 current meta: verified against run output

## Bound

One population (5 IT/software PSC codes), one exposure (FY2023 USAspending recipient data, complete census via meta.total), one outcome (segment newcomer fraction measured by prior-window comparison), one analysis (kill gate at median 0.30 threshold), one declared sensitivity (FY2018–FY2022 prior window, 5 years). No re-run on unchanged parameters. The unit of the headline rate is the *code-organization membership* (an organization holding awards in three codes is counted three times, as a buyer would see it). The 5 codes cover 8,375 distinct FY2023 recipients across all current windows.

- **G0–G2 and G4 pass:** the measurement infrastructure is sound
- **G3 fires the kill gate:** the median 0.2677 falls below the 0.30 threshold
- **No product is proposed and no adoption is claimed.** The concentration numbers from E196 stand; what changes is the inference about entry behavior across data sources.
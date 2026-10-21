<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E209 result — the federal IT codes are not uniformly enterable: three are, two are closed shops, and the fragmentation axis does not predict it

**Date:** 2026-10-21. **Session:** 2026-10-21-003.
Protocol written and recorded before the fetch: [`PROTOCOL.md`](PROTOCOL.md)
(declared at event seq 3; the fetch command is seq 12).

## What was tested

E196–E198 read the five IT/software PSC codes (`DA01`, `DA10`, `7A21`, `7030`,
`D304`) as **$203.32B across 98,640 funded purchases ≤ $100k paid to 9,977
distinct companies**, with the top 10 per code holding 34.5%–57.6% — and `STATE.md`
read that as "a genuine market at the scale a small program operates at".
E208 then measured the step that reading depends on (*do the winners include
newcomers?*) on the population where the pattern was last claimed (NIH SBIR
R41/R42) and the kill gate fired (F152, D129). D129 left the federal IT codes —
where the pattern was **first** claimed — untested on entry.

**The question:** on each of the five codes, what fraction of the FY2023
recipient identities had **no award in that code in the prior five years**
(2018–2022)? The same design as E208, so the two are comparable.

## Instrument and population

`POST /api/v2/search/spending_by_category/recipient/` with
`filters.psc_codes=[code]`, `award_type_codes` A/B/C/D,
`spending_level: "awards"`, paginated until `hasNext` is false. Identity is
`recipient_id` (present on 99.8%–100.0% of rows). Every response body is written
to `raw/` with its sha256 before parsing; the `.meta.json` records the exact
request. Windows are calendar, matching E198's convention: **current**
2023-01-01…2023-12-31, **prior** 2018-01-01…2022-12-31. Every number below
recomputes from the committed bytes alone.

## The gate vector — G0–G2 and C1–C4 pass, G3 fires the kill gate

| gate | declared | result | verdict |
|---|---|---|---|
| **G0** reproduce E198 | re-derive E198's six-year per-code recipient counts from its committed raw pages | DA01 3,610, DA10 3,651, 7A21 3,977, 7030 3,917, D304 1,155 — all equal to E198's `panel1.json` | **PASS** |
| **G1** source shape | all 5 codes × 2 windows return well-formed non-empty lists, every page `200`, no ceiling | 10/10 windows; 2246–6188 rows each; zero `CEILING` | **PASS** |
| **G2** identity coverage | ≥ 99% of rows carry `recipient_id` | 0.9980–1.0000 across all 10 windows | **PASS** |
| **G3** entry (kill gate) | median segment-newcomer fraction ≥ 0.30 | **median 0.2677** (fractions 0.2677, 0.3113, 0.2912, 0.0, 0.0) | **FAIL — kill gate fired** |
| **G4** confound (reported) | Spearman(fragmentation, entry) and Spearman(recipient_count, entry), n = 5 | **ρ(frag, entry) = 0.6669**, ρ(count, entry) = 0.5643 | reported, not gated |

Controls: **C1** PSC `ZZZZ` → well-formed empty `200`; **C2** PSC `not-a-code` →
`422`; **C3** zero `were not used` filter messages across all pages; **C4** every
current-window recipient id appears in E198's committed six-year set for that code
(0 missing on all five codes).

## What the numbers say

| code | current recipients (2023) | prior recipients (2018–2022) | segment newcomers | segment fraction | domain fraction | fragmentation |
|---|---:|---:|---:|---:|---:|---:|
| `DA01` | 2,245 | 2,144 | 601 | **0.2677** | 0.1568 | 0.7454 |
| `DA10` | 2,120 | 2,134 | 660 | **0.3113** | 0.1505 | 0.7010 |
| `7A21` | 2,225 | 2,482 | 648 | **0.2912** | 0.1407 | 0.6492 |
| `7030` | 1,262 | 6,186 | 0 | **0.0** | 0.0 | 0.6282 |
| `D304` | 503 | 1,609 | 0 | **0.0** | 0.0 | 0.4596 |

**Entry is heterogeneous, not absent.** `DA01`, `DA10` and `7A21` each show
**0.27–0.31** of their 2023 recipients as new to the code — comparable to the
0.5075 E208 measured for NIH SBIR category 101, and to each other. `7030` and
`D304` show **exactly zero**.

**The two zeros are a closed-shop pattern, not a small pool.** `7030`'s prior
pool is **6,186** recipients against 1,262 current, and **4,924 of the prior
pool are absent in 2023**; `D304`'s prior pool is 1,609 against 503 current,
**1,106 absent**. So these codes churn their *incumbents* heavily while **no
company outside the 2018–2022 incumbent pool wins at all**. A new small program
would be entering a market whose eligible set is closed, even though the
incumbent roster rotates.

**The fragmentation axis does not predict entry here.** The two zero-entry codes
are the *least* fragmented (`D304` 0.4596, `7030` 0.6282) and the most fragmented
code (`DA01` 0.7454) has the lowest non-zero fraction (0.2677). ρ(fragmentation,
entry) = **+0.6669** over n = 5 — the opposite sign from E208's −0.2456, and
driven by the two exact zeros. Reported, not gated.

## What this decides

- **The uniform "fragmented ⇒ a small program can enter" reading is unsupported
  on the federal IT codes too.** G3 fired (median 0.2677 < 0.30), closing the
  entry-by-fragmentation claim for the second domain in a row (F153).
- **The negative is not a rejection of the money axis — it narrows the screen.**
  `DA01`, `DA10` and `7A21` are measured as enterable (0.27–0.31 newcomer
  fraction); `7030` and `D304` are not. A candidate screen on the money axis
  should select by **measured entry**, not by fragmentation.
- **The threshold is a proxy and the result is borderline.** The declared 0.30
  bar comes from E208's single-category gate; the median here is 0.2677, and
  three of five codes sit just under or over it. The robust finding is the
  **bimodality** (two codes at exactly 0.0 against three at ~0.27–0.31), which no
  threshold choice removes.
- **No product is proposed and no adoption is claimed.** This is a measurement
  on a public API; the unit is a recipient, not a purchase, and a newcomer may
  be a large incumbent entering from an adjacent code.

## Raw data and instrument

- [`fetch.py`](fetch.py), [`controls.py`](controls.py), [`analyze.py`](analyze.py)
  — deterministic; `analyze.py` reads only files on disk.
- [`raw/`](raw/) — every response page (sha256 in the `.meta.json`), plus
  `fetch_summary.json`, `controls.json`, `analysis.json`.
- G0 recomputes E198 from E198's own committed bytes, so a parse defect here
  would have shown as a G0 failure.

## Bound

One population, one exposure, one outcome, one analysis, one window (5 years).
The unit of every fraction is the **recipient**, not the purchase. A recipient
absent from 2018–2022 but present in 2014–2017 is counted a segment newcomer;
the nine-year sensitivity E208 declared is **not** run here. The recipient
endpoint aggregates over the window and may exclude awards below its own floor,
which would *undercount* newcomers, not overcount them. `recipient_id` churn
would count an incumbent as new; C4 (current ids all appear in E198's six-year
set) bounds that.

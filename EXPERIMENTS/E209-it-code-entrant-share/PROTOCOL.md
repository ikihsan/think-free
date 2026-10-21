<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E209 PROTOCOL — are the federal IT PSC codes enterable?

**Date:** 2026-10-21. **Predecessor:** E196, E197, E198 (`../196-federal-spend-metered/`,
`../197-funded-award-count/`, `../198-recipient-read/`); the entry design mirrors
E208 (`../E208-sbir-entrant-share/`).
**Status:** gates declared before `fetch.py` was written. The only fetch before
this protocol is `probe.py`, one page, reconnaissance, captured at
`raw_probe.json`.

## 1. The question, and the decision its answer changes

E196–E198 found **$203.32B across 98,640 funded purchases ≤ $100k in five
IT/software PSC codes**, paid to **9,977 distinct companies**, with the top 10
per code holding **34.5%–57.6%** of each code's obligation. `STATE.md` read that
as "a genuine market at the scale a small program operates at".

E208 then measured the step that reading depends on — *do the winners include
newcomers?* — on the population where the pattern was last claimed (NIH SBIR
R41/R42) and **the kill gate fired**: fragmentation was not associated with
segment-newcomer fraction (ρ = −0.2456), and fragmentation turned out to be a
size proxy (ρ with category size = 0.9711). D129 recorded that the federal IT
codes — where the pattern was **first** claimed — stay untested on entry.

**The decision this experiment makes.** Whether the small-program entry reading
survives on the federal IT codes. Two branches, both pre-declared:

- **G3 survives** (median segment-newcomer fraction across the five codes
  ≥ 0.30) → the entry reading holds where it was first claimed; the money axis
  supports an enterable-market screen, and the next step is a candidate screen.
- **G3 fires kill** (median < 0.30) → the entry reading is unsupported in both
  domains measured; the accessibility pattern cannot carry a "small program can
  enter" claim, and the money axis needs a different basis for choosing a
  candidate (or none).

**Not declared here:** any product, candidate, or adoption claim. The unit is a
recipient, not a purchase; see the bound in §6.

## 2. Population

The five IT/software PSC codes from E197/E198: **`DA01`, `DA10`, `7A21`,
`7030`, `D304`**. Same award types and spending level as E198:
`award_type_codes` A/B/C/D, `spending_level: "awards"`.

**Windows** (calendar, matching E198's convention):
- **current** — `2023-01-01` … `2023-12-31` (the "FY2023" of this record);
- **prior** — `2018-01-01` … `2022-12-31` (five years).

**Identity:** `recipient_id` (a stable hash on the recipient object; present
100/100 in the probe). `code` (DUNS) is present 98/100 and is **not** used as
identity; `uei` is a cross-check.

## 3. Instrument

`POST /api/v2/search/spending_by_category/recipient/` with
`filters.time_period`, `filters.award_type_codes`, `filters.psc_codes=[code]`,
`limit: 100`, `page`, `spending_level: "awards"`; paginate until
`page_metadata.hasNext` is false. Every response body is written to `raw/` with
its sha256 **before** parsing, and a `.meta.json` records the exact request, so
the analysis is reproducible from bytes on disk and a parse defect is
distinguishable from a source defect. Responses are reused only when the stored
request key matches exactly.

**Ceiling:** E198 paginated the same endpoint fully for these five codes over a
six-year window (166 pages, no ceiling). The same is expected here.

## 4. Per-code quantities

For each code, over the current window:
- `recipient_ids` — set of `recipient_id` values, with their summed obligation;
- `fragmentation` = 1 − (top-5 obligation share);
- `recipient_count` = |recipient_ids|.

Against the prior window:
- `segment_newcomer_ids` = current ids absent from that code's prior ids;
- `segment_newcomer_fraction` = |segment_newcomer_ids| / |current ids|;
- `domain_newcomer_ids` = current ids absent from the **union** of the five
  codes' prior ids;
- `domain_newcomer_fraction` = |domain_newcomer_ids| / |current ids|.

The unit of every fraction is the **recipient**, not the purchase. An
organization holding awards in two codes is counted once per code.

## 5. Gates

| gate | question | fires when |
|---|---|---|
| **G0** reproduce E198 | re-deriving E198's six-year (2020–2025) per-code recipient counts from E198's **committed** raw pages equals its committed `analysis.json` | equal → pass |
| **G1** source shape | all 5 codes × 2 windows return well-formed non-empty recipient lists, every page `200`, pagination runs to `hasNext: false` | all pass → pass |
| **G2** identity coverage | ≥ 99% of rows in both windows carry `recipient_id` | ≥ 99% → pass |
| **G3** entry (kill gate) | median segment-newcomer fraction across the five codes | ≥ 0.30 → survives; < 0.30 → **kill** |
| **G4** confound (reported, not gated) | Spearman(fragmentation, segment-newcomer fraction) and Spearman(recipient_count, segment-newcomer fraction) over the five codes | reported with n = 5 |

G3 is the decisive gate and uses the same 0.30 threshold E208 declared for its
headline category, so the two experiments are comparable. G4 is reported
because E208's lesson (D129) is that a screen axis is a candidate explanation
only after its correlation with the obvious confound is measured; here the
confound is code size.

## 6. Controls

| id | control | what a failure means |
|---|---|---|
| **C1** | PSC `ZZZZ` returns a well-formed empty `200` | a confident wrong answer passes a threshold |
| **C2** | PSC `not-a-code` returns `422` or empty, never populated | the same |
| **C3** | no response carries a `were not used` filter message | a filter was silently ignored and every number is about the wrong population |
| **C4** | every current-window recipient id for a code appears in E198's committed six-year (2020–2025) recipient set for that code | identity is not stable across windows, or a window filter is wrong |

## 7. Bound

One population, one exposure, one outcome, one analysis, one window. No
re-run on unchanged parameters. The nine-year sensitivity window E208 declared
is **not** run here; a recipient absent from 2018–2022 but present in 2014–2017
would be counted a segment newcomer. This bounds the result to the five-year
window.

## 8. Do not run

- a re-run of E197/E198 panels on the same parameters;
- an award-amount filter on the recipient endpoint (E197 `probe.py` finding 2);
- the keyword form of this axis (closed by E195);
- a candidate screen before G3 is decided.

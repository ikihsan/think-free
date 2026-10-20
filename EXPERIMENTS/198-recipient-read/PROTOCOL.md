<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E198 PROTOCOL — who is paid for the 98,640 small IT purchases?

**Date:** 2026-10-19. **Predecessor:** E197 (`../197-funded-award-count/`).
**Status:** gates declared before `panel1.py` was written.

## 1. The question, and the decision its answer changes

E197 established that five IT/software PSC codes (`DA01`, `DA10`, `7A21`, `7030`, `D304`)
carry **$203.32B across 98,640 funded purchases at or under $100,000** — real
purchases, not empty records. The money axis now has:

1. **Buyer** — US federal agencies (DoD, VA, GSA, HHS, DHS, …)
2. **Unit** — 98,640 funded awards ≤ $100k in five codes
3. **Budget** — $203.32B across those cells

**What is not yet known:** who is paid for those purchases. The recipient read
(`spending_by_category/recipient/` under the same `psc_codes` filter — verified
reachable from this host in E196's reconnaissance) names the companies.

**The decision this experiment makes.** Whether the vendor landscape for these
five cells is concentrated enough that a small program could not compete, or
fragmented enough that it is a genuine market. Two branches, both pre-declared:

- **G2 fires as survives** (≥ 20 distinct recipients across the five codes, with
  the top 10 per code holding ≤ 80% of the code's obligation) → the vendor
  landscape is fragmented; the next step is a candidate screen on the money
  axis.
- **G2 fires as kill** (< 20 distinct recipients total, or top 10 per code hold
  > 80% of obligation) → the money is concentrated in a few primes; a small
  program cannot enter without being a subcontractor, and the money axis does
  not support a direct-entry candidate.

**Not declared here:** anything about products, candidates, or adoption. There
is no candidate yet.

## 2. Population

The five IT/software PSC codes from E197's committed `THRESHOLDS.IT_CODES`:
`DA01`, `DA10`, `7A21`, `7030`, `D304`. Same window and award types as E196/E197:
FY2020–FY2025, `award_type_codes` A/B/C/D, `spending_level: awards`.

## 3. Instrument

Query `spending_by_category/recipient/` with `filters.psc_codes=[code]`,
`spending_level: "awards"`, paginated until `hasNext` is false. The endpoint
returns aggregated obligation per recipient within the filter.

**Ceiling:** The endpoint paginates with `limit` (max 100) and `page`. No
documented ceiling, but a recipient list for a $20B cell could be thousands of
rows. We will paginate fully.

## 4. Panels

- **A — the recipient list, all five codes.** Full pagination for each code.
  Output: for each code, an array of recipient objects with `name`, `amount`,
  `recipient_id`, `code` (DUNS/UEI), `uei`, `total_outlays`.

## 5. Controls

| id | control | what a failure means |
|---|---|---|
| **C1** | PSC `ZZZZ` (well-formed, non-existent) returns a well-formed empty `200`, zero results | a confident wrong answer passes a concentration threshold |
| **C2** | PSC `not-a-code` returns `422` or empty and never a populated `results` | the same |
| **C3** | The sum of recipient amounts for a code is within 5% of the cell total from `spending_by_category/psc/` (E196's head100) | the recipient aggregation is missing money or double-counting |
| **C4** | Every response is checked for a `not used` filter message | a filter was ignored and every number below it is about the wrong population |

## 6. Gates

| gate | question | fires when |
|---|---|---|
| **G1** source shape | all five codes return a well-formed, non-empty recipient list with `hasNext` pagination working | all five pass → pass; any fails → fail |
| **G2** vendor concentration | **total distinct recipients across five codes ≥ 20, AND for each code, top 10 recipients hold ≤ 80% of that code's obligation** | both hold → survives; either fails → kill |

**G2 is the decisive gate.** The concentration threshold (top 10 ≤ 80%) is a
pre-declared proxy for "a small program could plausibly win work here." If the
top 10 primes soak up >80% of the money, the remaining <20% is subcontract
territory, not a direct-entry market.

## 7. Do not run

- the keyword form of this axis (closed by E195);
- an award-amount filter on the recipient endpoint (E197 probe.py finding 2);
- a re-run of E197 panels on the same parameters.
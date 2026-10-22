<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-21
-->

# E209 Protocol — IT PSC code entrant share measurement

**Date:** 2026-10-21. **Session:** 2026-10-21-019.

## Question

`STATE.md` reads the five federal IT/software PSC codes (`DA01`, `DA10`, `7A21`, `7030`, `D304`) as "a genuine market at the scale a small program operates at" (E198: 9,977 distinct vendors, top-10 per code hold 34.5%–57.6%, $203.32B across 98,640 funded purchases ≤ $100k). Between *fragmented* and *enterable* sits one unmeasured step: **do the winners include newcomers?** No experiment in this record has computed an entrant rate for these codes.

E208 asked the same question for NIH SBIR spending categories and found: fragmentation does **not** predict newcomer entry (Spearman ρ = −0.2456, kill gate fired); entry is common everywhere (median segment-entrant fraction 0.538 across 64 categories). This protocol mirrors E208's design for the five IT PSC codes.

## Population and windows

| window | fiscal years | USAspending `time_period` |
|---|---|---|
| **Current** | FY2023 | `[{"start_date": "2023-01-01", "end_date": "2023-12-31"}]` |
| **Prior** | FY2018–FY2022 | `[{"start_date": "2018-01-01", "end_date": "2022-12-31"}]` |

Codes: `DA01`, `DA10`, `7A21`, `7030`, `D304` (the five IT/software codes from E196/E198).
Award types: `A`, `B`, `C`, `D` (contracts, definitive contracts, purchase orders, delivery orders).
Spending level: `awards` (consistent with E196–E198).
Endpoint: `spending_by_category/recipient/` with `psc_codes` filter.

## Identity

`recipient_id` field from the API response (format: UUID + suffix, e.g. `9232b26d-789d-bdd2-5a6d-28714f1dfa2c-C`). This is the stable recipient identifier used by USAspending. Coverage target: ≥ 99% of rows carry a non-empty `recipient_id`.

## Metrics (per code)

- **Fragmentation** = 1 − (top-5 obligation share in current window).
- **Segment newcomer fraction** = |current IDs absent from prior IDs **in the same code**| / |current IDs|.
- **Domain newcomer fraction** = |current IDs absent from prior IDs **in any of the 5 codes**| / |current IDs|.
- **Obligation** = sum of `amount` in current window (for context).

## Gates (declared before any fetch)

| gate | declared question | threshold |
|---|---|---|
| **G0** reproduce E198 | FY2023 current-window recipient counts and top-5 shares match E198 within 5% | current recipients per code within 5%; top-5 share within 5 pp |
| **G1** identity coverage | ≥ 99% of current-window rows carry a non-empty `recipient_id` | ≥ 0.99 |
| **G2** prior window fetched | all 5 prior years return 200 with non-empty results for all 5 codes | 5 × 5 = 25 successful year-code combinations |
| **G3** fragmentation → entry | Spearman ρ(fragmentation, segment-newcomer fraction) ≥ +0.40 **and** one-sided permutation p < 0.05 over the 5 codes | ρ ≥ 0.40, p < 0.05 |
| **G4** code-level entry | segment-newcomer fraction ≥ 0.30 for at least 1 of the 5 codes | ≥ 1 code ≥ 0.30 |

G3 is the **kill gate**: if fragmentation does not positively predict entry, the "fragmented ⇒ enterable" reading fails for this population.

## Permutation test

10,000 permutations, seed `20261021`. One-sided: proportion of permutations where ρ_perm ≥ ρ_observed.

## Sensitivity window

Nine-year prior window (FY2014–FY2022) as a post-hoc check; declared but not gated.

## Analysis population

All 5 codes. No minimum-recipient filter (E208 filtered at ≥ 10 orgs; here all 5 codes have hundreds).

## Raw data commitment

Every API response written to `raw/` with SHA-256. `fetch.py` writes one file per page per code per window. `analyze.py` reads only committed raw files.

## Do not run

- A re-fetch without a new protocol version.
- Any gate threshold adjustment after seeing data.
- A different identity field (DUNS/UEI) without a new protocol.
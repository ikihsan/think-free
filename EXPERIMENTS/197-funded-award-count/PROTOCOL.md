<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E197 PROTOCOL — are E196's federal "purchases" purchases?

**Date:** 2026-10-19. **Predecessor:** E196 (`../196-federal-spend-metered/`).
**Status:** gates declared before `panel1.py` was written. Written after
`probe.py`, which is an *instrument capability* probe and is reported in §2
because it changed the instrument.

## 1. The question, and the decision its answer changes

E196 §2 reports five IT/software cells (`DA01`, `DA10`, `7A21`, `7030`, `D304`)
carrying **$203.32B "bought in tens of thousands of separate sub-$40k
purchases"**, and F143/D123 record that nine of the 25 cells clearing E196's
addressability gate clear it only because their 10,000th-smallest award **carries
no money** — `R499` $9.98, `6515` $0.00, `1560` $0.00, and at the endpoint's
50,000-award ceiling `R499`'s 50,000th award is **$51.93**. **Every count in
E196 is an award count, and an award record is not always a purchase.**

**The decision this experiment makes.** Whether the word *purchase* survives in
E196's headline. Two branches, both pre-declared:

- **G4 fires as survives** (≥ 10 of the 25) → the money is in small funded
  purchases, and the next experiment is the **recipient** read
  (`spending_by_category/recipient/` under the same `psc_codes` filter), which
  names who is paid for those purchases.
- **G4 fires as kill** (≤ 5) → the sentence "$203.32B bought in tens of
  thousands of separate sub-$40k purchases" is **withdrawn and replaced by a
  statement about records**, and the money axis needs an instrument that
  distinguishes funded awards from unfunded records — a different question from
  the one E196 posed, and not one this protocol can answer.

**Not declared here:** anything about products, candidates, or adoption. There
is no candidate yet.

## 2. What `probe.py` found before the protocol was written

`probe.py` exists to answer one question: *can this API count funded awards
directly, or must the count be found by reading the ascending order?* Three
findings, all recorded from raw bodies:

1. **`filters.award_amounts` is rejected**, `400`, with the API's own message:
   `"{'from': 1.0} is not a valid type (array)"`.
2. **`filters.amount_requirement` is silently ignored by
   `spending_by_award_count/`** — `200`, the identical count to the unfiltered
   request, and **no `not used` message** — and **explicitly reported as not
   used by `spending_by_award/`**: `"The following filters from the request were
   not used: {'amount_requirement'}"`. **The same ignored filter produces a
   confident, well-formed, wrong answer on one endpoint and an honest refusal on
   the other.** A count endpoint that ignores an amount filter is a machine for
   manufacturing the exact number this experiment is trying to measure.
3. **The ascending head of both probed cells is entirely non-positive.** `DA01`'s
   first 100 smallest awards run from **−$105,898.16 to $0.00**; `R499`'s from
   **−$437,863.29 to $0.00**.

**Therefore the instrument is the one E196 named** — bisect the ascending award
order — and it is the *only* instrument the API offers. Finding 2 is also why
control **C5** exists: `spending_by_award_count` is the **only** endpoint in the
run that can silently ignore a filter without saying so.

## 3. Population

The 100 PSC base codes in E196's committed `raw/head100.json`, **not** a fresh
selection: FY2020–FY2025, `award_type_codes` A/B/C/D, `spending_level: awards`,
same window and award types as E196 (`client.base_filters`). `N_code` — the total
award count — is **re-captured in this run** from `spending_by_award_count/`,
because E196 read totals from `spending_by_category/psc/` and the two disagree
by small amounts (E196 recorded `DA01` at 27,425 awards; the count endpoint
returned 27,424 on 2026-10-19). Any disagreement between this run's count and
E196's is reported as a data-vintage observation, not repaired.

**E196's 25 G4-clearing codes** are named in E196's RESULT §3 and are the
`G4_CODEBOOK` list in `thresholds.py`, copied from E196's committed bytes and
checked against them at run time (control **C6**).

## 4. Instrument

For a threshold `t`, define **`n_below(t)`** = the exact number of a cell's
awards whose `Award Amount` is **< t**. The ascending order is monotone, so
`n_below(t)` is found by reading ascending 100-row blocks until the first block
whose **minimum** is `>= t` (or whose maximum is `>= t`), and counting the rows
below `t` in every block read. The count is **exact, not an interpolation**,
because every row it counts was read.

**Thresholds, declared now:** `t ∈ {0, 1, 100, 1000, 10000, 100000}` dollars.
`t=0` separates deobligations; **`t=1` is the mission-critical one** — amounts
are cents, so `amount >= $1` is the cheapest expression of *carries money* that
the data supports; `t=100000` is E196's own addressability cutoff.

**Derived, for every code:**

| name | definition |
|---|---|
| `funded_ge_1` | `N − n_below(1)` — **awards carrying money** |
| `funded_fraction` | `funded_ge_1 / N` |
| `purchases_1_100k` | `n_below(100001) − n_below(1)` — funded awards at or under $100,000 |
| `censored` | true when the turning page exceeded 500, so `n_below(t)` is a **lower bound** |

**Ceiling, carried forward from F143 and not re-measured here:** the endpoint
answers `200` for page 500 and `422` for page 501, so **the 50,000th award is
the deepest any cell can be read to**. A censored code is reported as censored
with its bound, never as a count.

## 5. Panels

- **A — the funded count, all 100 codes.** One geometric scan of ascending
  blocks (ranks 100, 200, 400, … 50,000) then a bounded binary search inside the
  bracket each threshold's scan established. Exact `n_below(t)` for all six
  thresholds, or a declared censored bound.
- **B — the independent instrument, on E196's 25 G4 codes only.** Read the same
  statistic from the **descending** end: the largest rank whose descending amount
  is `>= 1` must equal `funded_ge_1`. Two orderings, one identity. Declared in
  advance because a bisection off by one page would otherwise produce a clean,
  confident number with nothing to contradict it.
- **C — controls**, in §6.
- **D — exploratory, no gate.** For the five IT/software codes, take the top five
  awarding agencies by obligation inside that code and run the `t=1` count
  inside each. Reports whether small-purchase metering is spread across buyers
  or concentrated in a few offices. Declared exploratory because the agency list
  is not fixed in advance and no gate names it.

## 6. Controls

| id | control | what a failure means |
|---|---|---|
| **C1** | PSC `ZZZZ` (well-formed, non-existent) returns a well-formed empty `200`, zero rows at pages 1 and 500 | a confident wrong answer passes a numeric threshold |
| **C2** | PSC `not-a-code` returns `422` or empty and never a populated `results` | the same |
| **C3** | `order: "asc"` really is ascending and `order: "desc"` really is descending, checked as `max(block p) <= min(block p+1)` on a code with a wide spread | E196 defect #1, which would have measured the largest awards when the gate asks about the smallest |
| **C4** | every response in panels A and B is checked for a `not used` filter message | a filter was ignored and every number below it is about the wrong population |
| **C5** | **`spending_by_award_count/` is the only endpoint that can ignore a filter silently**, so its `n_below`-adjacent role is confined to reading `N_code`; every code's `N_code` must be `> 0` and `<=` its deepest reachable rank's existence, and a code whose count exceeds 50,000 while the run reports an uncensored `funded_ge_1` above 50,000 is a defect, not a result | the count that this experiment divides by is itself unreliable |
| **C6** | the `G4_CODEBOOK` list matches E196's committed RESULT/rows exactly | the population was re-selected by this session rather than inherited |
| **C7** | `funded_ge_1 + n_below(1) == N_code` for every code | the count is not a partition of the cell |

## 7. Gates, and the third answer each one carries

`not_evaluated` is declared **before** the run, for a gate whose population was
not measured (E017 `H2`, E195 D7, E196 G5 — the same defect three times).

| gate | question | fires when |
|---|---|---|
| **G1** source shape | ≥ 98 of 100 codes give an exact integer `n_below(1)` and an uncensored, monotone, filter-clean `funded_ge_1` | `>= 98` → pass; `< 98` → fail |
| **G2** zero control | C1 and C2 both hold | both hold → pass |
| **G3** funded fraction | **median over the 100 codes of `funded_fraction`** — over half of a cell's award records carry money? | **`>= 0.50` → the record's headline survives as purchases; `< 0.50` → it is a statement about records.** Two-sided, direction declared. `not_evaluated` if < 50 codes are measurable |
| **G4** strict addressability | **how many of E196's 25 G4 codes hold `purchases_1_100k >= 10,000`** | **`>= 10` survives; `<= 5` fires the kill; 6–9 is `unresolved`** |
| **G5** arms agree | C3/C4/C7 hold, and panel B's descending-derived `funded_ge_1` equals panel A's on ≥ 23 of the 25 codes | `>= 23` → pass; `< 23` → fail, and **no absolute number in panels A or B may be reported as a measurement** until the disagreement is explained |
| **G6** no vocabulary confound | for each of the five IT/software codes, the `t=1` funded band carries the code's own description tokens at `>= 2x` the same tokens' rate among the cell's non-funded head — E195's `TurboScan` defect, applied to the funded sub-population rather than to a keyword | **`>= 2x` for all five → pass.** **Emptiness clause, declared now:** if a code's arm has **fewer than 20 funded rows sampled**, that code is `not evaluated` and the gate is `not_evaluated` unless the other four pass |

**G3 is the decisive one.** G4 restates E196's own gate with the zero-record
population removed; G6 guards the funded sub-population against E195's defect.

## 7a. What would make this a gate on the mission rather than on the data

Nothing here can kill the money axis, because G3's `not_evaluated` and G4's
`unresolved` band both exist. What this experiment can do is settle **one
sentence of one prior result** — whether E196's $203.32B was bought in purchases
or recorded in records — and that sentence is what the next candidate decision
rests on. If it falls, the money axis does not close; it moves to the instrument
question E196 could not ask.

## 8. Do not run

- the keyword form of this axis (closed by E195);
- any longer or shallower rank walk (F143's 50,000 ceiling is carried, not
  re-measured);
- a re-run of panels A/B/D on the same parameters — `client.call` reuses any
  capture whose stored request key matches, so it is free and returns the same
  bytes;
- an amount **filter** on any USAspending search endpoint (`probe.py` finding 2).
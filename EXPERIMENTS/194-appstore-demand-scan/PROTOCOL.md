<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-19
-->

# E194 PROTOCOL — does anyone pay, and where is the supply thin?

**Date declared:** 2026-10-19, before any iTunes request was sent.
**Instrument:** `scan.py` (stdlib only). **Raw:** `raw/scan.json`.
**Question:** for a set of concrete practical difficulties, how much paid
supply exists, at what price, and how much demand is visible — and is there a
row where demand is large and paid supply is thin?

## Why this question, and what decision it changes

**187 experiments in this record measured whether a *need* is served, by
harvesting public Q&A corpora.** Not one measured whether anyone **pays** for a
solution. Every candidate so far was selected by a *question being asked in
public*, and the repeated result of that instrument is that the need was
already served — six service closures in a row ended that way (F075, F081–F083,
F096, F104). E193 established that the marketplaces carrying price data
(Etsy, eBay) are hard-blocked from this host, and that the **iTunes Search API
is reachable and carries list prices, rating counts and genre** for consumer
software.

**The decision this changes:** which practical difficulty the mission attempts
next. `STATE-next-actions.md` currently says "return to fresh exploration",
and 2026-10-18 spent seventeen hours producing four unevidenced repair-planner
prototypes without a measured buyer. This scan is a **selection instrument**,
not a candidate screen: it cannot validate a candidate, and it cannot bound
prevalence. It can only say, for fifteen pre-declared terms, what the one
reachable price-bearing source says.

## Population — declared before the run

Fifteen exact search terms, `entity=software`, `country=us`, `limit=200`,
relevance order as returned (never sorted afterwards).

**Positive controls (the instrument must recover paid supply here):**
`todo`, `password manager`

**Negative control (the instrument must return nothing here):**
`zzqxqv glorb tapestry`

**Twelve declared practical difficulties:**

| # | Term | The job a person is paying to have done |
|---|---|---|
| 1 | `shift schedule` | build and swap a rotating work roster |
| 2 | `receipt scanner` | capture paper receipts into a searchable record |
| 3 | `warranty tracker` | remember what is under warranty and until when |
| 4 | `home inventory` | catalogue what is in the house, for a claim |
| 5 | `meal plan` | turn a household's food into a week's plan and list |
| 6 | `pet medication` | dose several animals on a correct schedule |
| 7 | `chore chart` | assign and settle recurring household work |
| 8 | `moving checklist` | run a relocation from packed to unpacked |
| 9 | `plant watering` | keep houseplants alive on a schedule |
| 10 | `reading list` | hold a queue of things to read |
| 11 | `sourdough` | schedule a starter-fed bake |
| 12 | `pool care` | run a seasonal maintenance schedule for a pool |

**How this list was chosen, stated plainly:** it is a hand-declared hypothesis
about the space, not a sample of it. Twelve terms chosen by one agent do not
represent consumer software, and the scan is **not** a prevalence estimate for
any difficulty outside this list.

## Metrics — fixed before the run

Per term, over the returned set and over the **top 50** (window declared
before the run):

- `paid` — apps with `price > 0`; `free` — apps with `price == 0`
- `median_paid_price` — median list price of paid apps in the window
- `ratings_paid` — **sum of `userRatingCount` over paid apps in the window**.
  Rating count is the only demand proxy this API exposes; revenue is not
  observable, and a paid app with 2 ratings contributes 2.
- `ratings_top1_paid` — the same, for the highest-rated paid app
- `median_ratings_paid` — median `userRatingCount` across paid apps in window

## Gates — declared before the run

- **G1 positive controls.** Each of `todo` and `password manager` returns ≥1
  app with `price ≥ 0.99` in the window. **Fails → every difficulty row is
  `not_evaluated`** and the scan reports the instrument failure only.
- **G2 negative control.** `zzqxqv glorb tapestry` returns `resultCount == 0`.
  **Fails → the false-positive rate of the instrument is unknown, every row is
  `not_evaluated`.**
- **G3 money exists in this population.** ≥4 of 12 difficulties have
  `paid ≥ 5` in the window. **Fails → the list describes jobs nobody pays for
  by app, which is a finding about the list, not about the jobs.**
- **G4 thin supply against large demand.** ≥1 difficulty with
  `ratings_paid ≥ 100000` **and** `paid ≤ 10` in the window. **Fails → the
  axis produced no candidate signal and is recorded as having produced none.**
- **G5 fetch reproducibility.** Two terms are fetched twice; identical
  `resultCount` and identical first-five track ids. **Fails → the instrument is
  not stable within the run and no row is reported.**

## Kill

**G4 not fired kills the *selection signal*, not the difficulties.** A thin
paid supply with large visible demand is the only row shape this scan can
produce that changes the next build decision; absent it, the mission returns to
fresh exploration by a declared rule, not by this scan's silence.

## Limits declared now, before the run

1. One country (US), one channel (mobile app stores), one language (English).
2. Relevance order, not sales order; the window is the top 50, not the catalog.
3. Ratings are not purchases, and are not evenly distributed by app age.
4. An open-source tool competes with these apps in the *job*, not in the
   storefront. Supply counts here are **not** an adoption forecast.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/194-appstore-demand-scan/scan.py
```
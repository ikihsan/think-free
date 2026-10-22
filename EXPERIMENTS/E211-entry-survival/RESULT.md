<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-21
-->

# E211 — Entry survival: small-award recipients come back, and DA10 beats 7030 by ~20 pp

Date: 2026-10-21. Session 2026-10-21-003. Gates frozen beforehand in
[`PROTOCOL.md`](PROTOCOL.md). All commands through `tools/x`; raw pages in
[`raw/`](raw/).

## Question

If a small software team wins one ≤$100k federal contract in a PSC code,
does it come back? E200/E201 had reported "100% of 7030 recipients have
exactly one award" (FY20–25), which reads as churn; E206 recommends 7030 on
accessibility metrics only. This is the sustainability axis that DECISIONS-NEXT
named as the biggest unknown, and the E208 field test for it needs humans this
VM may not contact — so it was measured from data instead.

## Design (as frozen)

Cohort per code in {7030, DA10, DA01}: recipients of funded awards
$0 < amount ≤ $100k, FY2020-10-01 → 2021-09-30, award types A–D, award-level
endpoint, ascending amount, ≤ 50 pages. Return window: recipient aggregates,
all sizes, FY2022-10-01 → 2025-09-30 (FY2022 deliberately excluded), same
code. Identity matched on **UEI**. Negative control: the same cohort against
PSC 6810 (chemical products).

## Instrument gates

| Gate | Declared | Result |
|---|---|---|
| I1 UEI coverage | ≥ 90% of cohort rows | **PASS — 100.0%** (4,847/4,847; 2,737/2,737; 1,102/1,102). The first run printed 0.311 for this metric; that was a **formula bug** (distinct-UEIs ÷ rows, i.e. 3.2 awards per vendor inverted), not a coverage failure. Fixed before interpretation. |
| I2 UEI vs name estimate | within 5 pp | **PASS — within 0.8 pp** (53.3/54.1, 72.6/73.1, 69.6/70.2) |
| I3 audit of matched pairs | ≥ 8 of 10 plausible same-entity | **PASS — 10/10** identical recipient names, UEI, plausible amounts (audit.py, seed 211) |
| False-negative check (added) | — | 27 UEI-unmatched rows are name-matched; **all major incumbents** (Northrop, Oracle, GDIT, Rockwell Collins) whose UEI changed across windows. UEI matching therefore errs **conservative**. |

Cohort censoring: 7030's first run censored at page 50 ($92k band); the band
was completed afterwards (53 pages, +218 rows, 4,847 total, now walks past
$100k). All three return windows and the control are **complete**
(`hasNext=false`, uncensored).

## Measurements (declared populations)

| Metric | 7030 | DA10 | DA01 |
|---|---|---|---|
| Cohort awards / distinct UEIs | 4,847 / 1,496 | 2,737 / 899 | 1,102 / 563 |
| Return-window recipients (complete) | 1,303 | 3,127 | 3,215 |
| **Survival (UEI)** | **53.3%** | **72.6%** | **69.6%** |
| Survival, net-positive obligation | 26.9% | 68.3% | 63.2% |
| Graduation (return-window aggregate > $100k) | 13.8% | 41.2% | 44.9% |
| Median returner aggregate, FY23–25 | **$2,000** | $176,030 | $361,559 |
| Negative control: same cohort vs PSC 6810 | **0.7%** (10/1,496) | — | — |
| Cross-market: 7030 cohort returning via DA10 / DA01 | 470 (31.4%) / 355 (23.7%) | | |

## Gate outcomes

- **G1 (churn): not met — C1 supported.** 53.3% ≥ 15% for 7030: small-award
  recipients *do* return. E200/E201's "100% single-award" baseline is
  **refuted at award level**: 33.5% of cohort UEIs already hold >1 award in
  the entry window alone (mean 3.2 awards/UEI); the earlier reading came from
  the recipient-endpoint row semantics, not from award reality.
- **G2 (ordering): FIRED.** DA10 − 7030 = **19.3 pp** > 5 pp with both
  cohorts ≥ 300 UEIs. **The "7030 best overall" recommendation is revised:
  DA10 is the code where small recipients build sustained business.**
- **G3 (negative control): PASS.** 0.7% vs 53.3% — survival is
  code-specific, not "still a federal vendor".

## Robustness (post-hoc, labeled as such — not gate values)

The cohort includes incumbents who happened to win a small award (Northrop
won a $36k 7030 award in FY21). Reclassifying any cohort UEI whose
window-A total in the code exceeds $100k as an incumbent and removing it:

| Cleaned (all-small only) | 7030 | DA10 | DA01 |
|---|---|---|---|
| Incumbents removed | 333 of 1,496 | 252 of 899 | 197 of 563 |
| Survival | **39.4–43.1%** | **63.8–64.1%** | 56.4–56.6% |
| Net-positive return | 18.7% | 59.8% | 49.2% |
| Graduation | **1.2%** | 23.7% | 24.2% |

(The range is the sensitivity bound over 261 of 1,496 7030 cohort UEIs that
the category endpoint omits from its window-A aggregate list while the
award-level endpoint includes — an endpoint disagreement whose worst case
still leaves DA10 ahead by 20.7 pp.)

**The G2 conclusion survives and strengthens under cleaning** (gap
20.7–24.7 pp: min = DA10 63.8 − 7030 43.1, max = DA10 64.1 − 7030 39.4): it is not an incumbent artifact. Among genuinely all-small
7030 recipients, 1.2% later hold >$100k in the code versus ~24% in DA10 and
DA01, and the median 7030 returner aggregates $2,000 over three years.

## What this changes

1. The E199/E206 recommendation is now **two-axis**: 7030 is the easiest
   door (accessibility, direct sales) but weak economics after entry;
   **DA10 is the sustainability winner** and also carries the vehicle
   pathway (E207/E210) and diversifying trend (E204). For a small team
   betting 6–12 months of business development, **DA10 is the better
   default recommendation**; 7030's "abundant entry points" framing is
   qualified by a $2,000 median return.
2. E200/E201's "100% single-award" claim is closed as a **measurement
   artifact of the recipient-endpoint row semantics** (D-recorded below).
3. The screen score (recipient count × concentration) measures
   accessibility only, and the axes pick **different codes** — the screen
   must not be quoted alone.

## Limitations (observed, not inferred)

- Cohort = recipients of small awards, not verified newcomers: same-window
  incumbency is cleaned, but no pre-FY2020 history was checked.
- Return-window aggregates are net of deobligations; bare survival counts
  appearances (separated as net-positive in the table).
- One control code (6810); control CIs are not computed (n = 1,496 / 713).
- ~283 API requests (page arithmetic over raw/), ceiling was 400. One
  intermediate run exited 1 on a dict-clobber bug (preserved in session
  log); the fix and the coverage-metric fix are both in `run.py` history.

## Reproduction

```bash
cd EXPERIMENTS/E211-entry-survival
python3 run.py        # serves from raw/ if present; refetches if absent
python3 audit.py      # I3 pairs, false-negative check, awards-per-UEI
python3 complete_band.py   # completed 7030's band; idempotent
python3 incumbent_check.py # post-hoc cleaning + sensitivity inputs
```

## Single most useful next action

Add a `survival` module to the E206 CLI so the assessment tool reports both
axes (accessibility + sustainability) and reproduces this file's numbers from
`raw/` offline — the current tool would have recommended 7030 alone, which
E211 shows is only half the answer.

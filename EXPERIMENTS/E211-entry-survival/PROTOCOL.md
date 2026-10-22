<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-21
-->

# E211 — Entry survival: do small-award entrants come back?

Frozen before measurement: 2026-10-21, session 2026-10-21-003.

## Practical difficulty

A small software team (1–10 people) deciding whether to invest 6–12 months of
business development in the federal market needs to know: if I win one small
contract, is a second one realistic? The E199–E206 line recommends PSC code
7030 ("IT software") on *entry accessibility* metrics (small awards, low
concentration, 3,916 recipients), and E200/E201 reported that **100% of 7030
recipients have exactly one award** over FY2020–2025. Taken literally that
reads as churn, not a pathway. Nobody in this repository has tested whether
small entrants *return*.

## Claim under test

C1 (survival): Among recipients whose funded awards in code X during
FY2020–21 were all ≤ $100k ("small entrants"), a non-trivial fraction win
another award in code X during FY2023–25.

C2 (ordering): 7030's survival rate is at least comparable to DA10's, so the
E206 recommendation "7030 best overall for small teams" survives a
sustainability test, not just an accessibility test.

## Strongest baseline

E200/E201's own finding — 3,915 of 3,916 7030 recipients have exactly one
award across FY2020–25 — predicts survival ≈ 0%. This experiment can
contradict it (the recipient-endpoint's "award count" semantics may differ
from award-level reality) or corroborate it. Either outcome is informative;
the baseline is not a strawman because it is this repository's own prior
measurement.

## Design

Per PSC code in {7030, DA10, DA01}:

- **Cohort (window A):** `spending_by_award/` award-level query,
  FY2020-10-01 → 2021-09-30, award types A–D, sorted by amount ascending,
  ≤ 50 pages × 100 rows. Keep rows with $0 < amount ≤ $100k and a UEI.
  Cohort unit: **distinct UEI**. Cohort declared censored if the page ceiling
  is hit before the amount exceeds $100k.
- **Return window (B):** `spending_by_category/recipient/` recipient-level
  query, FY2022-10-01 → 2025-09-30, same code, ≤ 50 pages × 100 rows,
  collecting UEI → (name, aggregate amount). Declared censored if
  `hasNext` remains true at the ceiling.
- **Survival** = |cohort ∩ B| / |cohort|. **Graduation** = cohort members
  whose B aggregate obligation > $100k, over |cohort|.
- **Cross-market return:** the 7030 cohort is also intersected with the
  DA10 and DA01 B lists (reported separately, not part of any gate).

Identity is matched on **UEI**, not name. A normalized-name match (uppercase,
punctuation stripped, suffixes INC/LLC/LTD/CORP/CO/THE removed) is computed
alongside as a robustness estimate, never as the gate value.

**Negative control (must fail):** B list for PSC 6810 (chemical products,
unrelated to software). The 7030 cohort's survival in 6810 must be
substantially lower than its within-7030 survival; otherwise "survival"
measures "still a federal vendor at all", not return to this market.

Note on the gap: window A ends 2021-09-30 and window B starts 2022-10-01;
FY2022 is deliberately excluded so that a "return" is separated in time from
the entry award.

## Gates (frozen before measurement)

Instrument validity — any failure makes the run **inconclusive**, not negative:

- I1: ≥ 90% of cohort award rows carry a UEI.
- I2: UEI-matched and name-matched survival estimates agree within 5 pp.
- I3: manual audit of 10 random UEI-matched pairs (name + agency + amount in
  both windows) shows ≥ 8 plausible same-entity pairs.

Result gates:

- G1 (churn): survival ≤ 5% in 7030 → the "viable sustained-business
  pathway" reading of 7030 fails; the assessment must report entry-without-
  return. Survival ≥ 15% → C1 supported for that code. In between → weak.
- G2 (ordering): DA10 survival − 7030 survival > 5 pp with both cohorts
  ≥ 300 UEIs → revise the recommendation toward DA10 for sustained business.
  7030 ≥ DA10 − 5 pp → recommendation stands.
- G3 (negative control): 7030-cohort survival in 6810 < within-7030
  survival. If not, the code-specific survival claim is unsupported and only
  the generic "still in the federal market" claim can be made.

## Resource limits

≤ 400 HTTP requests, ≤ 15 minutes wall time, standard library only. Raw JSON
pages saved under `raw/` with the query recorded. All commands through
`tools/x`.

## What would make this experiment fail honestly

- API page ceilings censor either window (declared, biases survival down).
- UEI coverage below 90% (I1) — many small awards may lack a recipient UEI.
- Cohort in window A contains many one-shot procurement anomalies ($0 rows
  already excluded; residual anomalies remain a known limitation).

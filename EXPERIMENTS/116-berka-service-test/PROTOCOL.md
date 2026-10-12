<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-12
-->

# E116 — Does a free general assistant find the recurring payments in a real bank extract?

Predeclared **before any extract was read**. The question D107's
standing constraint asks of every candidate line: *is the answer
already decidable — and decided — by the incumbent?* Here the
incumbent is the free general assistant, the data is a real bank
extract, and the answer is "which of these transactions are part
of a recurring payment".

## Question

A person reviews their bank export and asks: **which of my
payments are recurring?** E066 validated a deterministic detector
(interval+amount core, F1 0.8194, permutation control 0.0022) on
this data, but never tested the discriminating question: can a
free general assistant, handed the same extract, do the same job?
If it can, the line closes like E062/E091/E092/E114/E115. If it
cannot, the detector has an unserved population.

## Data

Berka (PKDD'99), real anonymized Czech retail-bank transactions
1993–1998, already provenance-recorded in
[`../066-berka-real-validation/raw/SOURCES.md`](../066-berka-real-validation/raw/SOURCES.md)
(sha256 verified on retrieval). Ground truth is the dataset's own
`k_symbol` standing-order categories — bank-coded, not
inferred by this mission.

**Declared limitation:** the extract's counterparty field is
`bank`+`account` (two codes), not a merchant name. A real modern
export is *easier* than this; the test is conservative. The
1990s standing-order population is not the subscription economy.

## Predeclared sample

E066's deterministic samples, truncated: the **first 60** of its
positive-bearing stride sample (R) and the **first 20** of its
control sample (C). Same accounts for every reader. Expected
positive groups ≈ 75 (300 R accounts carried 377 in E066).

## Presentation (what the assistant sees)

Per account, the **debit** transactions only (the detector's own
filter), chronological, one row each:

```
2019-03-05 | -2450.00 | Ceska sporitelna / 123456789
```

**No `k_symbol`** — it is the label. The assistant must find and
group the recurring counterparties itself.

## The assistant's answer

Per account: the list of counterparties (`bank / account`, copied
verbatim) the assistant judges to be recurring payments, plus the
number of occurrences it saw. Answers are committed
(`answers.jsonl`) **before any scoring runs**.

## Ground truth (the key)

A counterparty group is a **positive** iff its `k_symbol` ∈
{`POJISTNE`, `SIPO`, `LEASING`, `UVER`} and it carries ≥ 3
debits (E066's positive definition, unchanged). `SLUZBY` groups
are the excluded zone, scored neither way. Key committed as
`key.jsonl` before any answer exists.

## Readers (all on the same accounts, same key)

1. **Assistant** — a free general assistant (this session's
   model), blind to `k_symbol`, reading the committed extracts.
2. **Detector** — E066's `detect.py`, imported **unmodified**,
   fed the same normalized transactions.
3. **Naive baseline** — any counterparty with ≥ 3 debits.

## Predeclared gates

- **G0 (reader validity):** on R accounts the assistant's
  micro-recall ≥ 0.50, and on C accounts its micro-precision
  ≥ 0.80. A reader that cannot find the obvious standing orders
  or that hallucinates them is not performing the task; the run
  is **void**, not "not served".
- **K1 (service):** assistant micro-recall on positive groups ≥
  0.95.
- **K2 (separation):** assistant micro-F1 ≥ detector micro-F1 −
  0.05, same accounts.

**Served** iff G0, K1 and K2 all pass → the line closes and the
detector has no unserved population. **Not served** if K1 or K2
fails with G0 passing → the population is real and the detector
is the better reader; candidate opens with E066's evidence.

## Scoring

Group level, pooled (micro) across accounts, exactly E066's
evaluation. An assistant answer matches a group iff the
`bank/account` identity matches a group's counterparty; a match
against a positive group is a TP, against a non-positive group
an FP. Positives not matched are FN. The scorer is deterministic,
reads only the committed key and answers, and is pinned by
`test_score.py` (key-locked, falsifiable).

## Integrity constraints

- Sample, key, extracts, scorer and its tests are committed
  **before** the assistant reads any extract.
- Answers are committed before the scorer is run.
- The assistant knows only the sample design (R accounts carry
  ≥ 1 positive by construction); the C accounts control the
  resulting hallucination bias via G0's precision arm.
- All code stdlib-only, Python 3.8.

## What this does not establish

- Merchant-name robustness (real modern exports carry noisy
  merchant strings; no population-scale public dataset of real
  modern exports exists — recorded as a finding, F120).
- The subscription economy; 1990s standing orders only.
- Multiple assistant readers; one reader is the mission's
  established instrument (E091/E092/E114/E115 used the same).

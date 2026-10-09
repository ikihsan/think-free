<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# E072 — E066's recurring-expense detector on real modern bank exports

**Date:** 2026-10-09 · **Status: complete — G1 and G2 did not fire. No
candidate, no prototype.**

Protocol (predeclared before any detector ran): [`PROTOCOL.md`](PROTOCOL.md).
Corpus provenance and hashes: [`raw/SOURCES.json`](raw/SOURCES.json),
[`raw/CORPUS.json`](raw/CORPUS.json). Measurements:
[`results.json`](results.json). Gates: [`verdict.json`](verdict.json).

## The one-line result

**E065's detector does not survive real modern subscription data, and the
reason is not the one E066 named as its open question.**

## What was asked

E066 passed all four of its gates on 1,056,320 real Berka transactions and
named its own untested axis: *Berka carries no merchant text, so grouping here
is cleaner than any real bank-export string.* E072 ran the detector
**unmodified** on 36 real bank exports with merchant text — 34,231
transactions, 29 public repositories, 2021–2026, 18 hand-verified
subscription merchants — against an incumbent that actually ships this
feature.

## Results (observed)

| arm | precision | recall | F1 | TP | FP | FN | groups |
|---|---|---|---|---|---|---|---|
| `e065_raw` (E065 on raw descriptors) | 0.100 | **0.394** | **0.160** | 13 | 117 | 20 | 130 |
| `actual_raw` (Actual Budget `findSchedules`) | 0.091 | 0.424 | 0.150 | 14 | 140 | 19 | 154 |
| `e065_normalized` | 0.088 | 0.364 | 0.141 | 12 | 125 | 21 | 137 |
| `actual_shared` (both on E065's merchant axis) | 0.088 | 0.424 | 0.146 | 14 | 145 | 19 | 159 |
| `naive` (≥3 debits to a merchant) | 0.018 | 0.697 | 0.035 | 23 | 1263 | 10 | 1286 |

| gate | needs | saw | fired |
|---|---|---|---|
| **G4** population | ≥8 accounts, ≥3000 txns, ≥12 merchants | 36 / 34231 / 18 | ✅ |
| **G1** survives merchant strings | P ≥ 0.60 **and** R ≥ 0.50 | P 0.100, **R 0.394** | ❌ |
| **G2** beats the incumbent | F1 margin ≥ +0.05 | **+0.0098** | ❌ |
| **G3** instrument can say no | permutation ≤ 0.10 | **0.0000** (0 of 99) | ✅ |
| **G5** no single account decides it | direction stable | stable, none flip | ✅ |

## What the gates did not predict

The protocol expected the merchant-name axis to be the failure. It is a real
and measurable failure — but it is the **smaller** one.

**Failure 1 — under-grouping (the axis E066 named). 6 of 20 misses.**
`normalize.py` strips a trailing run of **≥4 digits**. Card processors emit
references of 3 characters or mixed alphanumeric, so a fixed-price monthly
subscription shatters into singletons and every fragment falls under the
`n ≥ 3` floor:

| account | family | rows | distinct raw strings → normalized names |
|---|---|---|---|
| a03 | Amazon Prime, $16.04, cv 0.000, gap 30 d | 13 | **13 → 13** |
| a03 | Spectrum, $115.00, cv 0.020 | 12 | **12 → 12** |
| a03 | Google One, $9.99, cv 0.000 | 13 | **13 → 13** |
| a05 | Amazon Prime, $14.99, cv 0.038 | 21 | **21 → 21** |
| a31 | Peacock, $4.99, cv 0.000 | 6 | **6 → 6** |
| a02 | Spectrum, $44.99, cv 0.082 | 18 | 4 → 4 |

Read `AMAZON PRIME*111 …` against `AMAZON PRIME*7U1 …`: three digits and one
letter, so the strip pattern never fires and both survive verbatim. A month of
$16.04, twelve times over, with an amount coefficient of variation of exactly
zero, is invisible.

**Failure 2 — the amount-consistency gate (not predicted, and larger). 14 of
20 misses.** `detect.py` rejects any group whose amount CV exceeds **0.15**,
and its score falls below 0.5 well before that. Real subscriptions change
price. Five accounts here pay for the same service — Spotify, monthly, on the
same day of the month, ten to fourteen charges each:

| account | amounts | CV | interval regularity | detected |
|---|---|---|---|---|
| a34 | $9.99 ×8, then $10.99 ×4 | 0.048 | 0.868 | **yes** |
| a36 | $5.99 ×1, then $11.99 ×11 | 0.151 | 0.868 | **no** |
| a35 | $10.99 ×1, then $5.99 ×11 | 0.225 | 0.899 | **no** |
| a11 | $9.99 ×3, then $4.99 ×11 | 0.318 | 0.784 | **no** |
| a28 | $9.99 ×3, then $4.99 ×10 | 0.352 | 0.744 | **no** |

**One price change, and the detector stops seeing the subscription.** a35 and
a36 have *higher* interval regularity than a34, which is detected. The only
thing separating them is whether the amount ever moved.

This is why E066 could not see it. E066's own README reports the false
positives as *"all 159 monthly, amount CV ≈ 0.000"* — in 1990s Czech retail
banking a standing order's amount does not drift. The gate E066 passed four
times was never exposed to a price change.

The same gate takes the rest: Comcast $39.99 × 24 monthly, CV **0.395**, not
detected. Hulu, CV 0.231, not detected. Vodafone, CV 0.263. Brightwheel,
CV 0.681. Planet Fitness, CV 0.505 across five raw spellings.

## Why precision reads 0.100 and what it really is

The 0.100 is a **lower bound with a known flaw, not a precision estimate.** The
watchlist exists to answer a question about *positives*; it holds 33 families.
Scoring every other reported group as a false positive counts a mortgage
auto-pay and a school meal plan as errors.

A stratified hand-read sample of 13 unclaimed groups (`precision_labels.json`),
stratified by detected interval:

| label | n | examples |
|---|---|---|
| recurring | 10 | `WF HOME MTG AUTO PAY` (129 charges over 5 years), `LOUDOUN COUNTY PUBLIC SCHOOLS` (32 × $35.00), `VANGUARD` (25 × $500.00) |
| not recurring | 1 | `SEVEN HILLS TECH DIRECT DEP` — an employer's payroll deposit |
| ambiguous | 1 | `FEE` — three identical $12.00 rows, descriptor says nothing |

**Stratified precision ≈ 0.91, watchlist-scored 0.100.** Both are in
`results.json`. The gap is the size of the labelling asymmetry, not a property
of the detector, and reporting only one of them would have been the wrong
claim in either direction. With n = 13 the sample is not a census and no
interval is computed.

## Against the incumbent

Actual Budget ships `findSchedules()` — a full automatic recurring detector in
a personal finance app. E072 ported it (stdlib only, 285 lines, published
here) and ran it on the same rows.

- **`actual_raw` F1 0.150 vs `e065_raw` F1 0.160: margin +0.0098**, against a
  +0.05 gate. **G2 does not fire.**
- This is *not* evidence that E065 is competitive. `actual_raw` is a **lower
  bound on the incumbent**: in production Actual matches on a payee its
  importer has already cleaned, and this arm hands it the same dirty strings
  E065 gets. A margin of +0.01 between two weak detectors says only that
  neither works here.
- `actual_shared` (both given E065's merchant axis) is F1 0.146 vs 0.141 —
  the interval/amount engines are within noise of each other once the merchant
  axis is held fixed. **The engine is not the differentiator.** The merchant
  axis is.

## What this closes, and what it does not

**Closed, on this population:** E065's detector as shipped. The E066 result
does not transfer to real modern subscription data, and the reason is a gate
E065 inherited from its synthetic corpus — a fixed 0.15 amount-CV ceiling that
treats a price change as evidence of non-recurrence.

**Closed with it:** the idea that the *merchant-name axis* is the thing left to
solve. It is worth 6 of 20 misses. The amount axis is worth 14.

**Not closed, and this is where the next experiment goes:** whether a
detector that models **piecewise-constant price** instead of rejecting on CV
recovers the recall. The evidence that this is a real repair and not a
retune: a24's ChatGPT, 9 × $20.00, CV **0.000**, regularity 0.922, score 0.915
— is detected. The machinery finds a fixed-price monthly subscription
immediately. The five Spotify accounts are the same mechanism with one price
step, and they are missed. That is a specification defect with a bounded,
testable repair, and it is a different mechanism from E065's.

**Not claimed:** anything about usefulness, adoption, or a market. `naive`
scores F1 0.035 and the incumbent scores 0.150, so on this population the
floor is higher than both.

## Honest limitations

- **The corpus is 36 real exports committed to public repositories because
  their owners were building something else.** It is not a random sample of
  bank exports and no claim of representativeness is made.
- **17 of the 38 candidate accounts were dropped at selection**, recorded with
  reasons in `raw/CORPUS.json`. The largest loss is `a04`, whose merchant
  column is ambiguous (a budget app's `Payee` beside a raw Chase `Payee`),
  which cost the corpus its longest-verified subscription: 49 Spotify charges
  over 1461 days.
- **The brand proxy is a proxy.** A detection is scored by leading brand token,
  not by an adjudicated merchant identity.
- **The Actual port is mine.** Its fidelity notes are in
  `actual_find_schedules.py`; a reader who judges it unfaithful voids G2.
- **Two accounts are excluded from precision scoring** because their
  descriptors carry a personal legal name. Two privacy screens were written and
  both were withdrawn — the reasons are in `finalize.py` and are the clearest
  thing in this experiment about what a rule needs before it is trusted.

## Reproduction

```bash
cd EXPERIMENTS/072-merchant-noise-raw
python3 finalize.py        # re-select accounts, re-hash, record exclusions
python3 relabel.py         # print candidate families for hand reading
python3 eval_arms.py       # run all five arms, write results.json
python3 fire_gates.py      # compare to PROTOCOL.md, write verdict.json
python3 inspect_errors.py  # print misses with their raw strings
```

Environment: Python 3.8.10, stdlib only, no network after retrieval.
Runtime ≈ 6 min on this VM (2 CPUs). The CSVs are **not committed**: url,
sha256, byte count and row count are in `raw/SOURCES.json`.
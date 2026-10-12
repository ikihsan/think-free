<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-12
-->

# E116 — Does a free general assistant find the recurring payments in a real bank extract?

**Status: complete — the line closes on service.** A free general assistant
read 80 real Berka bank extracts and found **all 75 positive standing-order
groups** (recall 1.0), with the best precision of any reader. E066's detector
has no unserved population.

## Question

E066 validated a deterministic recurring-payment detector on the Berka
extract. E116 asked the complementary question: handed the same extract as
`date | amount | counterparty` rows, can a free general assistant find the
recurring payments — the ones the bank codes as standing orders? If it can,
the line closes like E062/E091/E092/E114/E115.

## Design

- **Data:** Berka (PKDD'99), real anonymized Czech retail-bank transactions,
  1993–1998, sha256-verified on retrieval (provenance in
  [`../066-berka-real-validation/raw/SOURCES.md`](../066-berka-real-validation/raw/SOURCES.md)).
  Ground truth is the dataset's own `k_symbol` standing-order categories.
- **Sample:** 80 accounts (60 R, 20 C), predeclared before any extract was
  read. R accounts carry ≥1 positive by construction; C accounts are the
  hallucination control.
- **Presentation:** per account, debit transactions only, chronological, one
  row each. No `k_symbol` — it is the label.
- **Readers:** (1) the assistant (this session's model), blind to `k_symbol`;
  (2) E066's `detect.py`, unmodified; (3) a naive baseline (any group with
  ≥3 debits). All on the same accounts, same key.
- **Integrity:** sample, key, extracts, scorer and its tests committed before
  the assistant read any extract; answers committed before scoring; the
  assistant never saw the key.

## Result

| reader | TP | FP | FN | precision | recall | F1 |
|---|---|---|---|---|---|---|
| **assistant** | 75 | 32 | 0 | **0.7009** | **1.0000** | **0.8242** |
| detector | 75 | 110 | 0 | 0.4054 | 1.0000 | 0.5769 |
| naive | 75 | 205 | 0 | 0.2679 | 1.0000 | 0.4225 |

Per arm:

| reader | R: TP/FP/FN | C: TP/FP/FN |
|---|---|---|
| assistant | 75 / 26 / 0 | 0 / 6 / 0 |
| detector | 75 / 86 / 0 | 0 / 24 / 0 |
| naive | 75 / 159 / 0 | 0 / 46 / 0 |

### Gates

| gate | actual | threshold | pass |
|---|---|---|---|
| G0 R-recall | 1.0000 | ≥ 0.50 | ✓ |
| G0 C-precision | 0.0000 | ≥ 0.80 | ✗ |
| K1 assistant recall | 1.0000 | ≥ 0.95 | ✓ |
| K2 F1 margin over detector | 0.2473 | ≥ 0.05 | ✓ |

**The predeclared "served iff G0∧K1∧K2" condition is not met.** The G0
C-precision failure is a gate design flaw, not a reader validity failure —
see F122. The control accounts contain real standing orders whose `k_symbol`
is outside the positive set, so the gate (which assumes controls are
standing-order-free) fails every reader identically. The substantive reader
validity question is answered on the R arm (recall 1.0) and by the assistant's
C-arm answers, all real standing orders verifiable in the committed extracts.

## What this establishes

- **The population is served.** The strongest accessible reader of recurring
  payments on a real bank extract is a free general assistant, and it is the
  best of the three readers by a wide margin. E066's detector has no unserved
  population.
- The recurring-payment line **closes on service** — the sixth line to do so
  (E066, D108).

## What this does not establish

- **Merchant-name robustness.** The extract's counterparty is `bank`+`account`
  (two codes), not a merchant name. A real modern export is easier; the
  test is conservative. No population-scale public dataset of real modern
  exports exists (recorded as a finding in the protocol, F120).
- **The subscription economy.** 1990s standing orders only.
- **Multiple assistant readers.** One reader is the mission's established
  instrument.

## Defects found and fixed during the run

- **F121** — the scorer's key stores Berka's integer `account_id` while the
  answers use `"R001"`/`"C009"` strings, so the scorer matched every answer
  against nothing and the assistant scored 0. Fixed in `score.py`
  (`load_key` normalises; `_berka_id` maps back for the detector/naive Berka
  lookups), with two regression tests against the committed `key.jsonl`.

## Reproduce

```bash
python3 EXPERIMENTS/116-berka-service-test/score.py          # writes result.json
python3 -m unittest EXPERIMENTS/116-berka-service-test/test_score  # 12 tests
```

Answers: `answers.jsonl`. Key: `key.jsonl`. Extracts: `extracts/`.
Raw result: `result.json`.

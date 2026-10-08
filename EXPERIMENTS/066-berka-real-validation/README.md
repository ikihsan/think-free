<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-08
-->

# E066 — E065's recurring-expense detector on real bank data (Berka PKDD'99)

**Date:** 2026-10-08 · **Status:** complete — **all four predeclared gates PASS**

Protocol (predeclared before any run): [`PROTOCOL.md`](PROTOCOL.md).
Data provenance: [`raw/SOURCES.md`](raw/SOURCES.md).

## What was asked

E065's detector passed its kill gates on synthetic CSVs from its own
generator — exactly the "synthetic near-copies" case the owner brief warns
cannot validate an instrument. E066 ran the detector **unmodified** on real
anonymized Czech retail-bank transactions (1993–1998, 1,056,320 rows, 4,500
accounts), against labels built from the dataset's own `k_symbol`
standing-order categories, on a predeclared deterministic sample (300
positive-bearing accounts, stride-sampled from 3,501; 100 controls).

## Results (observed)

| metric | detector | naive baseline (≥3 debits) |
|---|---|---|
| precision | **0.7006** | 0.3601 |
| recall | **0.9867** | 1.0000 |
| F1 | **0.8194** | 0.5295 |
| FPR | 0.2284 | 0.9626 |
| TP / FP / FN / TN | 372 / 159 / 5 / 537 | 377 / 670 / 0 / 26 |

| gate | threshold | actual | verdict |
|---|---|---|---|
| G1 recall (real positive recovery) | ≥ 0.50 | 0.9867 | ✅ |
| G2 precision (real data) | ≥ 0.60 | 0.7006 | ✅ |
| G3 F1 margin over baseline | ≥ 0.05 | +0.2899 | ✅ |
| G4 permutation control (instrument can say no) | ≤ 0.10 | **0.0022** (2 of 921 detections survive date-shuffling) | ✅ |

Sensitivity row (predeclared; `SLUZBY` bank-fee groups counted as positive
instead of excluded): precision 0.8274, recall 0.9909, F1 0.9018 — gates pass
under that reading too.

## The false positives are mostly label gaps (observed, then inferred)

All 159 FP groups are uncategorized (`k_symbol` empty) transfers. Post-hoc
inspection (command below): **152 of 159 have ≥ 12 transactions, all 159
monthly, amount CV ≈ 0.000, medians 292–3,274 CZK** — e.g. 45–64 fixed-amount
monthly transfers to one counterpart. `observed`: those are the bytes.
`inferred`: in 1990s Czech retail banking such groups are overwhelmingly
real recurring payments (rent, standing transfers, external loans) the bank
never coded with a `k_symbol` — i.e. the detector found genuine recurring
payments the labels do not cover, so **0.7006 is a floor on semantic
precision, not the value**. Only 7 of 159 groups have fewer than 12
transactions.

Recall on real data (0.9867) *exceeds* the synthetic recall (0.8386): real
standing orders are more regular than E065's generator made them.

## What this establishes — and what it does not

- `observed`: the interval+amount core of E065's mechanism recovers real,
  independently-shaped recurring payments, beats its own baseline by 29 F1
  points on real data, and the instrument is decisively non-vacuous
  (permutation control 0.0022). The mechanism is no longer synthetic-only.
- Not established: the merchant-name axis. Berka has no merchant text, so
  grouping here is cleaner than real bank-export strings; robustness to
  merchant-string noise is tested only by E065's own generator so far.
- Not established: modern subscription-economy data (this population is
  1990s standing orders), real CSV format coverage, and the entire
  usefulness / differentiation / adoption stack above mechanism. A passing
  gate is evidence about a mechanism, not about a product.

## Single most useful next action

Test the second mechanism axis — merchant-name noise — on real modern bank
exports (open fixtures from self-hosted finance tools such as Firefly III /
Actual Budget / beancount test suites, or OFX samples), unmodified detector,
predeclared gates; and in parallel read those projects' import workflows for
whether recurring-transaction detection is already served there (D077:
read the population out of the evidence before building).

## Reproduction

```bash
cd EXPERIMENTS/066-berka-real-validation
python3 run.py            # writes results.json, prints pooled metrics + gates
```

FP-group inspection (post-hoc):

```bash
python3 - <<'EOF'
import sys; sys.path.insert(0, '.'); sys.path.insert(0, '../065-recurring-expense-detection')
import berka, detect as det
accounts = berka.load_accounts('raw/trans.csv')
r, c, _ = berka.sample_accounts(accounts)
fp = [(aid, d) for aid in r + c
      for d in det.detect_recurring_expenses(accounts[aid])
      if d['merchant'] in berka.label_groups(accounts[aid])[2]]
print(len(fp), sum(1 for _, d in fp if d['transaction_count'] >= 12))
EOF
```

Environment: Python 3.8.10, stdlib only, no network after `raw/` retrieval.
Runtime ≈ 41 s on this VM. E065's synthetic gates re-verified identical to
its README on the same day (P 1.0000, R 0.8386, FPR 0.0000).

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# E066 — Does E065's recurring-expense detector recover real recurring payments?

Predeclared before any run on Berka data. E065 passed its kill gates on a
synthetic corpus produced by its own generator
([`../065-recurring-expense-detection/README.md`](../065-recurring-expense-detection/README.md)).
The owner brief's standing warning applies: an instrument that passes only on
synthetic near-copies of its generator's assumptions has shown nothing about
the world. E066 runs the detector, **unmodified**, on data shaped by
independent reality: real anonymized Czech retail-bank transactions, 1993–1998.

## Question

Does the deterministic interval+amount machinery of E065's `detect.py`
recover real recurring payments (standing orders) in real bank data, at
precision a person reviewing their spending could tolerate?

## Data

Berka dataset (PKDD'99 Discovery Challenge), real anonymized transactions of
~4,500 accounts of a Czech bank, 1993–1998, ~1.06M rows. Retrieved
2026-10-08 as `raw/trans.csv` (sha256 recorded in `raw/SOURCES.md`) from a
GitHub mirror of the original `.asc` release. Nothing about the data was
shaped by this mission, its generator, or its vocabulary.

## Predeclared mapping (Berka row → E065 normalized transaction)

- `date`: `YYMMDD` → `datetime.date`.
- `amount`: `type` ∈ {`VYDAJ`, `VYBER`} (debits) → negative; `PRIJEM`
  (credit) → positive. The detector reads only debits.
- `merchant`: `"{k_symbol}|{bank}|{account}"` — counterpart identity
  (empty fields → `NA`). Berka has no merchant text; this is the closest
  honest key and it is *cleaner* than real CSV merchant strings, which is a
  declared limitation, not a hidden one.

Unit of evaluation: one account (mirrors E065's one-CSV-file unit).

## Predeclared labels

- **Positive (labeled recurring group):** a (account, merchant-key) group
  whose `k_symbol` ∈ {`POJISTNE` insurance, `SIPO` household, `LEASING`,
  `UVER` loan payment} — the standing-order categories — with ≥ 3 debit
  transactions. The detector requires ≥ 3 occurrences, so the label does too.
- **Excluded zone:** `SLUZBY` (bank statement-fee) groups are scored neither
  as positives nor as false positives. They are bank-side monthly fees:
  semantically recurring, but the label source cannot separate them from the
  customer-initiated standing orders the candidate claims to find. A
  secondary sensitivity row reports all metrics with `SLUZBY` counted as
  positive, so the effect of this judgment call is visible.
- **Negative:** every other merchant group.

## Predeclared sample

Deterministic, from `account_id` ascending:

- **R (positive-bearing):** every account with ≥ 1 positive group, stride
  `max(1, len(R_all) // 300)`, capped at 300 accounts.
- **C (controls):** the first 100 accounts by id with zero positive groups
  and ≥ 20 transactions (precision/FPR come from real transaction noise,
  not only from accounts known to carry standing orders).

## Predeclared gates

- **G1 (real positive recovery):** micro-recall over positive groups ≥ 0.50.
  Below that, the mechanism only works on its own generator's assumptions.
- **G2 (real-world precision):** micro-precision ≥ 0.60 (excluded zone not
  counted either way). Synthetic precision was 1.00; real data is allowed to
  cost more, not unlimited.
- **G3 (baseline dominance):** detector micro-F1 − naive micro-F1 ≥ 0.05,
  where naive = E065's own baseline ("merchant group has ≥ 3 debits"). If
  the machinery cannot beat the trivial rule on real data, it carries nothing.
- **G4 (the instrument can say no):** permutation control — within each
  sampled account, permute dates across that account's transactions
  (seed 42), destroying interval structure while preserving every marginal.
  Detected recurring groups on the permuted data must be ≤ 10% of the
  unshuffled count. If the detector fires anyway, the instrument is vacuous
  on this data and every other gate is void.

## Predeclared constraints

- `detect.py` and `scoring.py` from `../065-recurring-expense-detection/`
  are imported **unmodified**. If real data forces a code change, the change
  and its reason are recorded and the affected results are marked post-hoc.
- All code stdlib-only (per D082). Every number recomputed from
  `raw/trans.csv` by `run.py`; no hand-picked rows.

## Reading of outcomes (predeclared)

- All gates pass: the interval+amount core survives real data. What remains
  untested is the axis Berka cannot carry — merchant-name noise in real CSV
  exports — and the whole usefulness/adoption stack above mechanism.
- G1 fails: the detector is tuned to its generator. Record the finding,
  narrow or close the recurring-detection line.
- G2 fails: inspect the false-positive classes before deciding; real
  recurring-but-unlabeled groups are a label-quality question, not
  automatically a detector defect (that is what the excluded zone is for).
- G3 fails: the mechanism adds nothing over a three-line rule on real data.
- G4 fails: results void regardless of the other gates.

## Declared limitations

- No merchant text: grouping is by category+counterpart, cleaner than real
  bank-export strings. A pass does **not** clear the merchant-normalization
  risk; that is a separate axis E065's synthetic corpus already covered only
  under its own generator.
- 1990s Czech retail banking predates the subscription economy; `SIPO`
  household payments and insurance standing orders are the recurring
  population that exists here.
- k_symbol labels are coarse; the sensitivity row bounds the one ambiguous
  category.

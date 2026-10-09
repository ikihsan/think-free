<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E072 protocol — predeclared before any detector was run

**Ordering, stated exactly.** Written 2026-10-09, **before E065's detector was
run on a single row of this corpus** and before any metric in it was computed.
No gate, threshold, arm, or label definition below was changed after the first
detector run; git history is the proof.

**What had already been seen when this was written, so the ordering claim is
not overstated.** The corpus had been selected by a mechanical filter over 411
publicly committed CSVs, and during that selection the column headers and
roughly four sample rows per candidate were read. So the *layout* of these
files and a handful of example descriptors were known. What was **not** known:
any detector output, any recurring-payment rate, any normalization failure
rate, and which merchants recur.

**One claim withdrawn rather than kept.** An earlier sentence here said the
protocol preceded *any* reading of a descriptor string. That was false, per the
paragraph above.

## The uncertainty

E065 built a recurring-payment detector and passed its gates on a synthetic
corpus. E066 ran it **unmodified** on 1,056,320 real transactions from Berka
and it passed all four gates (P 0.7006 / R 0.9867 / F1 0.8194, permutation
control 0.0022). E066 names its own untested axis in its README:

> Berka carries no merchant text, so grouping here is cleaner than real
> bank-export strings.

So the mechanism E066 confirmed — **interval + amount regularity** — was
confirmed on a population where merchants never vary. Real exports vary the
merchant string on every row. Grouping is load-bearing: if one real
subscription splits into three groups of one row, recall collapses; if two
different merchants merge, precision collapses. **E066 cannot distinguish
these two failures because it never had merchant strings.**

## The question, stated so it can fail

> On real modern bank exports that do carry merchant text, does E065's
> detector still identify real recurring payments — and does it beat the
> strongest alternative a user could actually install today?

## Population

Real personal bank / credit-card CSV exports committed to public GitHub
repositories, each with ≥ 180 days of span and ≥ 250 rows, taken before any
payee-cleaning or categorization. The sampling unit is the **account-file**.
Files whose bytes duplicate another's are dropped by sha256; near-duplicate
accounts are collapsed on the (date, amount) multiset at Jaccard ≥ 0.5.

**D077's population rule was applied first**, before anything was built:
Actual Budget ships `findSchedules()`, an automatic recurring-payment
detector, at
`packages/loot-core/src/server/schedules/find-schedules.ts`. Firefly III ships
a first-class `Recurring` resource with a `CalculateXOccurrences` trait.
beancount has four mentions of "recurring" in its entire repository. The
*user-facing recurring-transaction feature is served in two of the three*; what
is open is detection **from imported history without the user declaring it**.

## What is measured, and against what

**Instrument.** `EXPERIMENTS/065-recurring-expense-detection/detect.py`
**unmodified**. Format adapters map columns only; **no adapter alters a
merchant string**, because the merchant axis is the thing under test. One
adapter is declared separately, in `arm_sign.py`: an account's debits are
resolved to the negative side from the file's own sign shape, because 11 of 38
accounts record debits as positive and E065 keeps expenses as `amount < 0`.
Both arms are reported so the format effect is visible rather than absorbed.

**Baselines.**

1. **Actual Budget `findSchedules()`** — shipping code, MIT, ported to Python
   with stdlib only and ported line-by-line: the six patterns, the ±2-day
   window, `getApproxNumberThreshold` (7.5%), the ≥3-occurrence requirement,
   `Array.find` payee semantics, and dedupe-by-payee. **Stated handicap:** in
   production Actual matches on a payee its importer has already cleaned, so
   every `actual_raw` number is a **lower bound on the incumbent**.
2. **E065's own naive baseline** (≥3 debits to a merchant), for continuity.

**Arms.** `e065_raw` and `actual_raw` both receive the raw descriptor —
*who copes better with the strings a bank actually sends?* `e065_normalized`
and `actual_shared` both receive E065's normalized name — *holding merchant
quality fixed isolates the interval/amount engine, which is what E066
actually confirmed.*

**Labels.** Positives are a hand-read watchlist of real recurring-payment
families, built from raw rows by reading and frozen (`watchlist.json`) before
any arm ran; `eval_arms.py` cannot write it. Negatives are every other
transaction in the same account. Precision is additionally checked on a
**hand-read stratified sample** of reported groups (`precision_labels.json`),
because the watchlist exists to answer a question about positives and counting
every unclaimed detection as a false positive understates precision by an
unknown and large amount.

## Predeclared gates

| gate | statement | threshold | fires when |
|---|---|---|---|
| **G1** | the mechanism survives merchant strings | precision ≥ 0.60 **and** recall ≥ 0.50 | below either, the merchant axis destroyed E066's result and **the line closes** |
| **G2** | it beats the incumbent on its own ground | F1 margin over Actual `findSchedules` on the same raw strings ≥ +0.05 | not met → no differentiation → **nothing is built** |
| **G3** | the instrument can say no | permutation control ≤ 0.10 | above, every result above is an artifact |
| **G4** | the population is real and big enough | ≥ 8 accounts, ≥ 3,000 transactions, ≥ 12 hand-verified merchants | not met, the verdict is **`untested`**, never `pass` |
| **G5** | no single account decides it | the G1 direction is unchanged when the largest account is removed | flips, the result is one person's spending |

## Falsifiers held in reserve

- The corpus is mostly one person's re-uploads. G4 catches it by content-hash
  and near-duplicate collapse; G5 by leave-one-out.
- Watchlist recall is circular. It is not: the watchlist is built from **raw
  strings read by hand** and frozen before any arm ran.
- Actual's port is a strawman. The port is published next to the TypeScript
  path and its deviations are listed in its docstring; if a reader judges it
  unfaithful, G2 is void and the verdict is `untested` on that arm.
- E065 was tuned on this corpus. It is not: it is frozen at its 2026-10-08
  bytes and is not modified anywhere in this directory.

## What a pass would and would not have licensed

A pass is evidence about **one mechanism** on **one population** of real
exports that happen to be public because their owners were building something
else. It is not evidence of usefulness, differentiation from a
*fully-featured* incumbent, or adoption. None of those was started by a pass.

## What actually happened

Recorded here because a protocol that is not read against its result is a
protocol that cannot fail: **G1 and G2 did not fire**, and the failure is not
the one this protocol was written to expect. G1's precision arm was written as
"precision ≥ 0.60", assuming the watchlist would cover the accounts' recurring
payments. It does not, and cannot: 33 hand-read families against 36 accounts
whose readers hold mortgages, gym plans, school meal plans and brokerage
contributions. See [`README.md`](README.md) §What the gates did not predict.
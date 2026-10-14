<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E134 AMENDMENT-1 — two more recomputation checks, declared before the run

Written 2026-10-14 at 00:36 UTC, after the protocol was committed
(`f187edb1`) and **before** `lm_eval` was installed and before one row of its
output existed. The install log in this directory is the evidence of order.

## Why

The protocol declares R1 — recompute the headline rate from the shipped per-row
verdicts. Reading the harness's *own documentation* of what it writes (its
README's "Logging" section, which is documentation rather than output) shows
that a run emits two things: a `results.json` carrying the aggregate, and a
samples file carrying per-row records. Two further questions are answerable on
those bytes with no extra input, and both are silent-failure shapes rather than
quality questions:

- **R2 — row count.** Does the aggregate's own `n-samples` equal the number of
  per-row records actually shipped? A harness that scores N rows and ships M
  has published a number that describes rows the reader cannot see. Nothing
  raises.
- **R3 — metric presence.** Does every metric the aggregate reports have a
  per-row column behind it? A metric computed only in the aggregate is not
  recomputable, so the aggregate is unfalsifiable — which is the same defect
  class F121 was, read from the other side.

Neither needs gold labels, a model, or the harness's cooperation, which is what
makes them the checks that transfer to a third party.

## What this changes

Nothing in the gates. R1–R3 are measurements recorded beside the gates; a
disagreement is a finding to be hand-verified, and agreement is a result. The
declared failure condition is unchanged: **if Arm A's run is clean under C1 and
the recomputations agree, `preflight` has no observed external value and the
release question closes.**

## What this does not do

It does not widen the population, and it does not make `preflight` into a
recomputation tool. If the recomputations disagree on a real run, the finding
belongs to whoever published that run, and the tool that follows from it would
be a *new* tool with its own pre-declared protocol — not an extension decided
after seeing the result.

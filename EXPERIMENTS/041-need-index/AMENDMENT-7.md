<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — AMENDMENT-7: a ratio with no denominator is a third state, and here it
## would have printed a positive result as red

**Written after the instrument's first complete readout and before the gates were
re-evaluated.** The numbers it governs were already on disk; nothing was re-collected
and no similarity was recomputed.

## What the first readout printed

At the frozen `tau` of **0.05** on both text units, arm **N0's recall is exactly
0.0** — not one of the 77 matched cross-repository controls reached 0.05 cosine
against anything. So `recall@tau(P) / recall@tau(N0)` is `0.74 / 0.0`.

**My first implementation evaluated G1's ratio condition as
`rec_n0 > 0 and (rec_p / rec_n0) >= RATIO_BAR`,** which turns "the control arm has
no instances" into "the ratio condition failed", and the gate printed:

```
G1 met = False   conditions = {ratio: False, diff: False, ci: True}
paired_diff = 0.74026   ci95 = [0.636, 0.831]
```

**A paired difference of +0.74 with a CI95 of [0.64, 0.83] printed as a failure,
and the condition that failed was the one that could not be computed.** The
absolute-difference condition was false only because it was written with the same
`rec_n0 > 0 and ...` guard.

## Why this is F067 and not a new finding

F067 is recorded in this repository as *"a zero-denominator control arm scored as a
failed bar, so a strongly positive result printed `not met`"* — a defect of E040's own
instrument, listed as the third of E040's three self-inflicted errors. **The same
defect, in the same family, made it into the code written specifically to avoid
repeating E040's mistakes.** E041's protocol exists because E040's G2 could not fire;
the fix for that line introduced the identical error shape on a different gate.

**The generalisation, which is the part worth keeping:** a defect does not stop
reproducing just because the run that found it has been diagnosed. What stops it is a
**rule the implementation is obliged to satisfy**, not a lesson the implementer has
to remember. `docs/policy/gate-falsification.md` already carries that rule for gates;
this is the case where **the gate evaluation itself** needed one, and the way to get it
is the same as everywhere else here — declare it in an amendment, write the third state
into the code, and check that the code produces it.

## The correction

- A ratio with a zero denominator is **`not_evaluated`**, never `False`.
- The **absolute-difference condition no longer carries a `rec_n0 > 0` guard.** It is
  a subtraction of two measured rates and is defined whenever both rates exist, which
  they do. It was false here only because the guard suppressed it.
- A gate is reported with `met_on_evaluated_conditions` alongside `met`, so a reader
  sees which conditions were computed and which were not, rather than a single boolean
  that conflates "failed" with "could not be evaluated".
- **The bars are untouched**: 1.5, 0.20, 0.50, 0.50, exactly as declared.

## What this amendment does not decide

It does not make G1 pass, and it does not rescue anything. Read correctly, G1 on this
population is **"the instrument separates judged repeats from matched controls by
+0.74 [+0.64, +0.83] at the operating point where the control is silent; the ratio
form of the same statement is not evaluable"** — which is a *positive* result about the
loose control, sitting alongside **G2's failure** (`beats_impostor` 0.40 on titles,
0.14 on title+body, against a bar of 0.50), which is the gate that carries the weight.
The verdict is still **`failed G2`**, and it is still a negative result about the
instrument. **This amendment changes a label on one sub-condition and nothing about the
outcome.**

## The reproduction command, which `--reuse` does not change

```
python3 EXPERIMENTS/041-need-index/instrument.py            # both units, both gates
python3 EXPERIMENTS/041-need-index/instrument.py --reuse    # gates from raw/unit_*.json
```

`--reuse` exists because the unit steps cost **20 s and 552 s** on this host, and
re-evaluating a gate must not re-pay either. It reads the same files the full run reads
and **refuses to run if either is missing**, so it cannot report on absent work.

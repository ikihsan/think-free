<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# E073 protocol — predeclared before any pwc detector was run

**Ordering, stated exactly.** Written 2026-10-09, before the
piecewise-constant detector ran on a single row of E072's corpus.
No gate, threshold, arm, or label definition below was changed after
the first `e073_pwc` run; git history is the proof. The corpus, the
watchlist, the frozen `detect.py`, the `actual_find_schedules.py`
port and the scoring functions are E072's bytes, unmodified.

## The uncertainty

E072 closed E065's detector on real modern exports and attributed
its 20 misses: 6 to the merchant-name axis it went in to measure,
**14 to an amount-consistency gate nobody had questioned** — a fixed
0.15 amount-CV ceiling that treats a price change as evidence of
non-recurrence. Five accounts pay the same subscription monthly on
the same day; the detected one (a34, CV 0.048) and the missed ones
(a36 0.151, a35 0.225, a11 0.318, a28 0.352) differ only in
whether the price ever moved. The missed ones have *higher* interval
regularity than the detected one.

That diagnosis is a claim, and it makes a prediction: if the amount
gate is replaced by a model that admits exactly one price change,
those subscriptions reappear, and nothing else does.

## The model, stated so it can fail

A group's amounts, in date order, quantized to integer cents, are
**piecewise-constant with at most one step**: the run-length
encoding of consecutive equal cent values has **at most 2 runs**.
One run is the fixed-price case E065 already catches; two runs is
one price change, in either direction. Any other amount shape —
drift, oscillation, a second step — is rejected, exactly as the CV
ceiling rejected it.

The utility-keyword escape hatch is **withdrawn**. It existed only
to relax the CV ceiling, and the pwc gate subsumes it on stricter
terms: a utility with drifting amounts has more than 2 runs and is
still rejected; a utility with one price change is accepted on the
same terms as any other merchant.

**Score.** An accepted group's amounts are fully explained by the
model (≤ 2 parameters), so `compute_recurring_score` is called with
`amount_cv = 0.0`, which is its own `amount_factor = 1.0` branch —
the frozen scoring function supplies the mapping, this experiment
does not invent one. Everything else is E065's, unchanged: `n ≥ 3`,
`interval_regularity ≥ 0.45`, `score ≥ 0.5`.

This is a **different mechanism from both baselines**, and the
difference is stated so it can be checked: E065's gate is a
distribution-shape test (CV over the whole series); Actual
`findSchedules`' gate is a per-occurrence ±7.5% amount window
(`getApproxNumberThreshold`), which a price change beyond 7.5% also
breaks. The pwc model admits the transition instead of penalizing it.

## The question

> On E072's frozen corpus and frozen watchlist, does the piecewise-
> constant amount gate recover the recall the CV ceiling lost, without
> a precision cost, and does it differentiate against the incumbent?

## Arms

| arm | what it is |
|---|---|
| `e065_raw` | frozen E065 `detect.py`, raw strings. **Fidelity gate G0**: must reproduce E072's `e065_raw` row exactly (P 0.100 / R 0.394 / F1 0.160, TP 13 / FP 117 / FN 20). If it does not, the comparison is void. |
| `e073_pwc_raw` | the pwc arm on the **same raw strings** — the only difference from `e065_raw` is the amount gate. This is the primary arm. |
| `e073_pwc_norm` | the pwc arm on E065's normalized names — the axis E072 used to isolate the engine. |
| `actual_raw` | the incumbent, re-run on the same rows, same port. |
| `naive` | E065's naive baseline (≥ 3 debits to a merchant), continuity. |

## Predeclared gates

| gate | statement | threshold | fires when |
|---|---|---|---|
| **G0** | the baseline is the same baseline | `e065_raw` reproduces E072's row exactly | any mismatch → void, the harness differs from E072's |
| **G1** | the repair recovers recall | pooled recall of `e073_pwc_raw` ≥ **0.50** on the same watchlist (33 families) and corpus | below, the price model does not recover the CV-gate misses and the diagnosis is wrong |
| **G2** | it beats the incumbent | F1 margin of `e073_pwc_raw` over `actual_raw` ≥ **+0.05** (unchanged from E072) | not met → no differentiation → nothing is built |
| **G3** | the instrument can say no | permutation control (3 date-shuffles per account, seed 20261009, E072's procedure) ≤ **0.10** | above, every number above is an artifact |
| **G4** | the population is real | the frozen corpus and watchlist, unchanged — already met (36 accounts / 34,231 transactions / 33 families) | — |
| **G5** | no single account decides it | leave-one-out recall direction unchanged when the largest account is dropped | flips, the recovery is one person's spending |
| **P1a** | no precision collapse | pooled watchlist-scored precision of `e073_pwc_raw` ≥ `e065_raw`'s − **0.02** | below, the recall was bought with false positives |
| **P1b** | the added groups are real | **census** hand-read of every group `e073_pwc_raw` adds over `e065_raw` on the raw axis, precision ≥ **0.80** recurring (if the census exceeds 40 groups, a stratified sample of 40, seed 20261010, is read instead) | below, the repair is a CV-ceiling relaxation, not a price model |

P1b is the falsifier that separates *mechanism* from *retune*: a
loosened CV ceiling would also add groups; a price model adds
groups whose amounts take exactly two constant values.

## Falsifiers held in reserve

- **The recovery is the watchlist's own arithmetic.** G1's ceiling is
  bounded: 0.394 + 14/33 = 0.816 if every CV-gate miss returns. A
  number at the ceiling would mean the merchant-axis misses never
  stood a chance, which is expected and is not a defect.
- **The added groups are one account's spending.** G5.
- **The corpus's amounts were quantized by the exporter** (every
  amount ends in a fixed cent pattern), inflating exact-cent runs.
  Checked by reporting the single-segment share of accepted groups.
- **The pwc arm also drops groups** the utility escape hatch used to
  accept (variable merchants, CV 0.15–0.40). Reported as `dropped`,
  never absorbed.

## What a pass would and would not license

A pass is evidence that E072's *diagnosis* was right — the amount
gate, not the merchant axis, was the binding constraint for a
measurable set of real subscriptions — and that a one-step price
model is the repair that fits this population. It is **not**
evidence of usefulness, of adoption, or of differentiation from a
fully-featured incumbent running on cleaned payees: `actual_raw` is
a lower bound on Actual (D090), and per D090/F185 the detector line
is closed. The next question after a pass is whether a person pays
for this, and that question is not started by any gate here.

## What actually happened

Filled in by `README.md` after the run; the numbers land in
`results.json` and `verdict.json`, and the hand-read labels in
`added_labels.json`.

# E113 — matched-harvest control for the view-count principle

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

Classifier follow-up: [`IMPROVEMENT-SUMMARY.md`](IMPROVEMENT-SUMMARY.md)
records the v2 labeler built against this experiment's ~30% coverage
constraint (the G1 gate failure F116/D106 named).

## Verdict: the principle does not survive a matched harvest

**`observed`, session `2026-10-12-001`, VM `instance-20260717-0947`.**
The effect the view-count line rests on is a **harvest artifact**. E107's
`Cliff's δ = 0.826` is reproduced exactly by its own code on its own committed
data, and it disappears — to δ = +0.075, p = 0.183 — when both arms are drawn
from one pool under one selection.

Two separate defects, each sufficient on its own to produce the published
number:

1. **Asymmetric harvest.** E107 drew its need arm from `topic:web-framework`
   and its random arm from `topic:utils`, both sorted by stars. Re-derived from
   `raw_data.json`: **80 of 80** need rows carry `web-framework`, **80 of 80**
   random rows carry `utils`, before any classifier runs. The published gap
   compares the most-starred web frameworks to the most-starred utility
   libraries. That is true, and it is a tautology.
2. **String-label matching.** E107 matched vocabulary by unanchored substring,
   so `ai` fired inside `email`, `ml` inside `html`, `base` inside `database`,
   `learning` inside `machine learning`, `cli` inside `client`. On E113's pool
   that rule assigns `unlabelled` to **504 of 700 rows (72%)**.

## What the numbers are

| quantity | value | source |
|---|---|---|
| E107 published δ, recomputed | **+0.826010** | exact match to `results.json` |
| E113 pooled δ, matched harvest | +0.2048, p = 0.0146 | `analyze.py` |
| **E113 within-stratum δ** | **+0.0746** | `stratified.py` |
| **E113 stratified permutation** | **p = 0.1835**, 20 000 iters | `stratified.py` |
| need-label coverage of the pool | **196 / 700 = 28.0%** | `analyze.py` |

The pooled effect is carried by the need label **sitting in higher star
strata**, not by need labels winning at equal fame. Five of seven strata are
negative or zero; the two positive ones are the two middle strata.

## Reading it correctly

This does **not** say "need-related repositories get no arrivals." It says the
**screen** cannot tell you that, and its published confidence was bought with a
sampling design that made the answer inevitable. A negative here closes the
**claim and population actually tested** — this platform, this classifier, this
pool — and says nothing about PyPI, Hex.pm, or the rest. What it does say is
that the same two defects are present in the shared scaffolding of the registry
sweeps (E090, E095, E102, E103, E108 all import or copy this classifier and
sort their "random" arm by the outcome metric), so **those results cannot be
read as independent confirmations** until re-run on a matched harvest.

## The gates, and one honest disagreement with myself

G0 fired twice before passing and **AMENDMENT-3** records a one-word edit to a
probe after seeing it fail. That edit is the weakest link in this experiment and
is flagged as such rather than buried: it changes no need term, no threshold and
no statistic, and the sensitivity arm re-runs the whole comparison under E107's
unanchored rule so the verdict is checkable without it.

`analyze.py` on its own printed **verdict: survives** — G2 and G3 both passed.
That verdict is **wrong**, and `stratified.py` is why: it pooled across star
strata, which is the same class of error as E107's, one level down. The correct
verdict is the stratified one, and both files are committed so a reader can see
the stronger claim and its refutation in the same directory.

## What this does not decide

- Whether a better classifier would find a real effect. The test here is of a
  screen, not of the world.
- Whether the line is worth re-running properly. That needs a classifier that
  covers its population first — see the coverage result below.

## The coverage result, which is independent of the above

The need/generic vocabulary labels **196 of 700 rows (28.0%)**. Of the 504
unlabelled, **458 match neither vocabulary** — they describe themselves in words
the list does not contain. E107 reported 100% coverage implicitly, by reporting
only rows it labelled.

A screen that discards 72% of a representative population cannot be said to
have measured that population, and no effect size computed on the surviving
28% transfers to the whole. This is a larger obstacle to the line than the
effect-size collapse, and it is a fixable engineering problem rather than a
dead end — but it must be fixed *before* any further domain sweep, or the next
sweep inherits both defects.

## Files

| file | what it is |
|---|---|
| `PROTOCOL.md` | gates and failure condition, declared before the first fetch |
| `AMENDMENT-1.md` | first pool was truncated on the outcome variable; stratified repair |
| `AMENDMENT-2.md` | G0 fired; substring matching, and the 28% coverage cost |
| `AMENDMENT-3.md` | G0 fired again; need/generic vocabulary nesting, and the probe edit |
| `harvest.py` | one pool, 7 disjoint star strata, no need vocabulary in the query |
| `labeling.py` | the three label rules (unanchored / anchored / masked) + G0 probes |
| `raw_pool.json` | 700 rows as fetched, with the stratum that produced each |
| `analyze.py` | G0–G4, coverage, pooled comparison, sensitivity arm |
| `stratified.py` | within-stratum delta and stratified permutation test |
| `results.json`, `stratified.json` | machine-readable outcomes |

## Reproducing

```sh
cd EXPERIMENTS/113-viewcount-matched-harvest
python3 harvest.py     # refetches the pool (GitHub search API; rows shift over time)
python3 analyze.py     # ~6 min: permutation test
python3 stratified.py  # ~4 min: MERGES into results.json — run it last
```

**Order matters.** `analyze.py` writes `results.json`; `stratified.py` then adds
the decisive stratified figures to the same file. Running `analyze.py` alone
leaves a `results.json` without them, and `tools/origin doc lint` will correctly
report that this record restates numbers the artifact does not contain. Run
both, `stratified.py` last.

`cliffs_delta` is a merge-based exact implementation, verified equal to the
naive double loop on 600 randomised pairs with heavy ties, and verified to
reproduce E107's published +0.826010 exactly — so the difference reported here
is the harvest design, not arithmetic.
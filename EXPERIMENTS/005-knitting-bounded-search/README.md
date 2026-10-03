<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 005-knitting-bounded-search

Follow-up to `EXPERIMENTS/004-knitting-stage-a` (T-0010), testing the repair
that experiment named: a planner that closes releases *before* deciding patches
and searches only inside bounded neighbourhoods, checked against the same
exhaustive oracle. All inputs are **synthetic grids**; nothing here measures
physical feasibility (that is Stage B, still unperformed).

## Claim under test

On the 004 grid model, a planner that groups errors whose release closures
intersect, takes each group's minimum-cost local plan, and charges the union of
the releases once, returns a minimum-cost valid repair on every solvable case
and agrees with the exhaustive oracle exactly — and does so with a search space
smaller than the oracle's.

## Kill gate (predeclared, 2026-10-03, before any run)

1. **Abandon the candidate** if, at full neighbourhoods (no chunk cap, beam 1),
   the bounded planner is invalid or cost-suboptimal on *any* solvable case, or
   ever emits a plan for an unsupported state. That would mean closing releases
   before deciding patches does not repair the planner.
2. **Narrow, not abandon** if the full-neighbourhood planner matches the oracle
   but any cheaper setting (chunk cap 1, or beam 1 with a smaller cap) is still
   suboptimal on shared-release cases. The planner then works, but only by
   searching whole neighbourhoods, and that is where its cost comes from.
3. **Reject "bounded" as a claim** if the enumerated patch subsets plus
   combinations are not materially fewer than the oracle's on any case family.
   Then "bounded neighbourhood" is a misnomer for exhaustive search with extra
   steps.

## Baseline (strongest available)

The exhaustive minimum-cost oracle from 004, unmodified, plus 004's per-error
local rule so the result is comparable with T-0010. A deliberately weak baseline
is not used anywhere here.

## Negative controls

- **Unsupported states** (shaping, tension change) must be refused, not planned.
- **Refusal is not a fallback for search failure**: for every supported case the
  planner must return a plan, so an invalid plan cannot hide behind a refusal.
- **Held-out fixtures.** Random grids from one seed are never inspected while
  the code is written; the holdout seed is declared here and run once.
- **Cost-sensitivity sweep.** `PATCH_COST = 3` is a choice, not a fact. The
  headline setting is re-run at several patch costs; a result that only holds at
  one cost is not a result.

## Method

- Fixtures: 004's 10 cases unchanged, 5 constructed cases for this experiment
  (fragmenting, one deep stack, mixed groups, a cable chain, one extra
  unsupported state), 40 seeded random cases for development, 60 seeded
  holdout cases, and 3 larger fabrics.
- Settings swept: chunk cap 1, 2, 3, none x beam 1, 2, 4. Chunking is what
  bounds the work when one neighbourhood is large, so its cost/quality trade-off
  is measured rather than asserted.
- Reported per case: oracle cost, bounded cost, validity, optimality, released
  and patched cells, neighbourhood sizes, subsets enumerated, and whether the
  per-chunk costs were separable. Cell-level plans are recorded for the
  hand-built fixtures; the random ones are regenerable from the recorded seeds.

## Reproduce

```bash
python3 EXPERIMENTS/005-knitting-bounded-search/run.py              # ~2 s
python3 EXPERIMENTS/005-knitting-bounded-search/run.py --slow       # ~335 s
```

Standard library only. `results.json` is rewritten. Deterministic apart from the
printed wall time: no clock, no randomness outside the seeded fixtures.

## Result

`observed`, 2026-10-03, from `results.json`. 118 cases: 115 with the oracle, 2
refused as unsupported, 1 the oracle is not run for by default (24 errors,
`2**24` subsets; `--slow` runs it and took 334.8 s against 2.3 s). Consecutive
default runs produced byte-identical `results.json`.

**Headline setting, whole neighbourhoods, beam 1:** valid on 115/115, cost
identical to the exhaustive optimum on 115/115, total suboptimality 0. The
per-chunk costs were *separable* on 115/115 cases, which is the mechanism the
design predicts: errors whose release closures cannot intersect are genuinely
independent problems, so the union costs what the parts charged and no
combination search is needed. 004's per-error rule, on the same cases, is
optimal on 85/115.

### The chunk cap is the failure boundary

The bound is not free. Splitting a neighbourhood, or keeping only one candidate
per chunk, is what breaks exactness:

| Setting | Optimal | Total suboptimality | Combinations evaluated |
|---|---|---|---|
| `cap=None, beam=1` | yes | 0 | 115 |
| `cap=None, beam=4` | yes | 0 | 976 |
| `cap=3, beam=1` | no | 2 | 115 |
| `cap=2, beam=1` | no | 8 | 115 |
| `cap=1, beam=1` | no | 42 | 115 |
| `cap=1, beam=2` | yes | 0 | 1080 |
| `cap=2, beam=4` | yes | 0 | 1080 |

Two readings matter. First, `cap=1, beam=1` is a per-error rule again and it
fails on 20 of 115 cases — including T-0010's own `same_column_stack_4x4`, the
constructed deep stack, and 14 holdout cases never seen while the code was
written. The gain comes from searching whole closure-overlap neighbourhoods,
not from the "bounded" framing.
Second, **the two settings that look best are not bounded at all**: on all 115
checked cases `cap=1, beam=2` and `cap=2, beam=4` evaluate exactly `2**|errors|`
combinations — the oracle's own search space — so they are exhaustive search with
extra steps and must not be counted as a bounded-planner result.

### Is "bounded" worth anything?

Work is counted as patch subsets enumerated plus combinations evaluated, since
each needs one closure computation.

| Family | Cases | Bounded work | Oracle work | Ratio |
|---|---|---|---|---|
| from 004 | 9 | 41 | 32 | **1.28** |
| constructed (fragmenting) | 4 | 48 | 104 | 0.46 |
| development random | 40 | 220 | 240 | 0.92 |
| holdout random | 60 | 394 | 440 | 0.90 |
| larger fabrics | 2 | 26 | 264 | 0.10 |

Honest reading: on T-0010's own cases and on small random grids the bounded
planner does **not** save work — on the 004 family it does slightly *more*. The
saving appears only where closures fragment: 48 subsets and one combination on
the 24-error fixture against `2**24 = 16,777,216` for the oracle. So the
defensible claim is that the decomposition is *exact* and collapses the
combination phase, not that it is cheap.

### Refusal, sensitivity, and the larger fabrics

- Both unsupported states are refused inside the planner, with no plan emitted.
- The headline setting is optimal at `PATCH_COST` 1, 2, 3, 5, and 8, so the
  result does not depend on the cost constant.
- The beam is not a bound either: on the 24-error fixture, `beam=2` asks for
  `2**24` combinations, trips the planner's declared 20,000-combination budget,
  falls back to each chunk's local best, and records that it did.
- On the two larger fabrics that the oracle can check, the planner is optimal on
  both and beats 004's local rule on one (6 against 8 on the column stack). With
  `--slow` the 24-error fabric is checked too and the planner is optimal there
  (24 against 24), so **all 116 solvable fixtures are oracle-checked across the
  two run modes**.

### Kill-gate verdict

1. **Not met** — the candidate is not abandoned. Whole-neighbourhood search is
   valid and optimal on every case where the oracle could check it (116 of 116
   solvable fixtures across both run modes), at every patch cost, on both the
   development and the holdout seed.
2. **Met — narrow.** The planner works only when it may search whole
   neighbourhoods. Any cheaper setting is either suboptimal (cap 1, 2, 3) or no
   longer bounded (beam 2 at cap 1).
3. **Partially met.** "Bounded neighbourhood" is not an efficiency claim at this
   scale. See the ratio table.

## What this does and does not show

- **Does show:** the planner question T-0010 left open is now answered at the
  mechanism level. Closing releases before deciding patches, inside
  closure-overlap neighbourhoods, reproduces the exhaustive minimum-cost repair
  on 115/115 cases in the default run and 116/116 with `--slow`; the per-error
  rule does not (85/115).
- **Does not show:** that this is useful. It is a search over a synthetic
  closure system; the same decomposition is textbook separable optimisation over
  a closure operator, so **no novelty is claimed or implied**.
- **Does not show:** anything physical. Stage B (real swatches, an experienced
  knitter) is unperformed and remains the binding test.
- **Does not settle** the knitting kill gate's other condition, whether existing
  graph tooling already supplies equivalent intervention sequences. That is a
  prior-art question and is untouched by this experiment.

## Limits

- Synthetic grid model, one patch cost in the headline run (swept separately),
  one release cost. Cables are the only cross-column coupling modelled.
- The optimality result is *expected* from the model's structure, so it is a
  check that the implementation matches its design, not a discovery. The
  informative results are the cap/beam failure boundary and the work accounting.
- Random grids are 3x3 to 6x6 with at most four errors; the exhaustive oracle is
  only practical at that size, so most of the evidence about larger fabrics rests
  on three hand-built fixtures.
- `cap=1, beam=2` and `cap=2, beam=4` are exhaustive search in disguise; they are
  reported for the curve, not as evidence for the bounded planner.
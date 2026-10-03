<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 006-ventilation-measurement-design

`RESEARCH/C.md` hypothesis 2, run as its own predeclared kill gate (T-0014).
The question: when two explanations of a room's CO2 trace are almost
indistinguishable from passive data, does **choosing the next measurement**
separate them better than a fixed door-open protocol at the same budget?

All inputs are **synthetic**. Nothing here measures a real room, a real sensor,
or a real person. It can falsify the claim; it cannot establish usefulness.

## Claim under test

Given a two-room mass-balance system and a pair of parameter sets whose passive
traces in the measured room are nearly identical, an adaptive protocol that
picks its next action from a small menu separates the pair more often than a
fixed door-open/door-closed protocol at the same number of observations and
interventions.

## Kill gate (predeclared, 2026-10-03, before any run)

1. **Stop this formulation** if, on the correctly specified paired cases, the
   adaptive protocol's pairwise discrimination accuracy is not greater than the
   fixed protocol's.
2. **Stop this formulation** if the adaptive protocol's rate of *false precise*
   answers on the violating holdouts (changing weather, poor mixing) is not lower
   than the fixed protocol's. A design that wins on specified cases and then
   reports confident wrong answers has failed the gate as written in
   `RESEARCH/C.md`.
3. **Narrow** if adaptive wins on discrimination but neither protocol's parameter
   estimates are useful on their own, i.e. the gain is confined to picking
   between two named stories and does not extend to estimating a rate.

Passing any single comparison establishes only that the separation is possible
in this model. `RESEARCH/C.md` states the ceiling itself: the right outcome on a
pass is an extension to NIST CONTAM or QICO2 or NVAPF, not a new repository, and
independent room measurements are required before any practical claim.

## Method

- **Simulator.** Two zones with outdoor exchange to each and inter-room exchange,
  occupancy-generated CO2, per-sensor offset and Gaussian noise. A weather
  multiplier and a stratified-mixing switch provide the two violations the
  estimator does not model.
- **Estimator.** One grid maximum-likelihood fitter shared by every protocol, so
  the only thing that differs between protocols is *which measurements were
  taken*. Parameter intervals are profile-likelihood intervals at the 90% level.
- **Protocols, equal budget.** Same number of samples and same number of
  interventions for all three: passive fitting; a fixed door-open/door-closed
  sequence; adaptive selection from the action menu.
- **Metrics.** Pairwise discrimination accuracy, ventilation-rate error, 90%
  interval coverage, and the rate of false precise answers.
- **Controls.** Paired sets whose room-A traces must actually be nearly
  identical (the tolerance is stated and checked, not assumed); a condition in
  which all three protocols are given the *same* trace, so no protocol can win by
  luck; and holdout cases the estimator cannot represent.

## Reproduce

```bash
python3 EXPERIMENTS/006-ventilation-measurement-design/run.py
```

Standard library only. `results.json` is rewritten. Deterministic: every
randomness is seeded.

## Result

`observed`, 2026-10-03, from `results.json`. 144 cases: 6 pair families x 3
conditions x 8 noise seeds, one shared fitter, one budget (12 slots, one
decision). Wall time about 140 s.

**The kill gate was not met, so this formulation is stopped.** Both halves:

| Gate | Required | adaptive | fixed | Met |
|---|---|---|---|---|
| 1. discrimination on specified cases | adaptive > fixed | **0.792** | **0.833** | **no** |
| 2. false precise answers on violations | adaptive < fixed | 0.000 | 0.021 | yes, but see below |

Gate 2 was met almost vacuously: the false-precise rate is 0.000 for adaptive,
0.042 for fixed under poor mixing, and 0.000 for both under changing weather.
Neither protocol produces confident wrong answers at the 0.4 ACH threshold, so
this is not evidence that adaptivity buys safety.

| Protocol | Condition | Discrimination | Median abs error (ACH) | Coverage 90% | False precise |
|---|---|---|---|---|---|
| passive | specified | 0.333 | 0.0 | 1.000 | 0.000 |
| passive | changing weather | 0.333 | 0.0 | 1.000 | 0.000 |
| passive | poor mixing | 0.292 | 0.0 | 1.000 | 0.000 |
| fixed (door open) | specified | 0.833 | 0.0 | 1.000 | 0.000 |
| fixed (door open) | changing weather | 0.833 | 0.0 | 1.000 | 0.000 |
| fixed (door open) | poor mixing | 0.542 | 0.1 | 0.958 | 0.042 |
| adaptive | specified | 0.792 | 0.0 | 1.000 | 0.000 |
| adaptive | changing weather | 0.833 | 0.0 | 1.000 | 0.000 |
| adaptive | poor mixing | **0.708** | 0.0 | 1.000 | 0.000 |

Discrimination on the specified cases, per pair family:

| Pair family | passive | fixed | adaptive |
|---|---|---|---|
| coupled_vs_outdoor | 1.00 | 1.00 | 1.00 |
| near_degenerate | 1.00 | 1.00 | 1.00 |
| deep_seal | 0.00 | 1.00 | 1.00 |
| neighbour_stuffy | 0.00 | 1.00 | 1.00 |
| neighbour_mild | 0.00 | 1.00 | 0.75 |
| **offset_only** (unidentifiable control) | 0.00 | 0.00 | 0.00 |

Actions the adaptive rule chose: `co_locate_b` 72 times, `door_open` 64, `noop`
8 (all eight on the unidentifiable control, which is the correct response).

### What the numbers actually say

1. **The ambiguity is real and the door resolves it.** Passive fitting picks the
   true story 33% of the time, which is chance. Prescribing a door-open window
   takes it to 83%.
2. **Choosing the action does not beat prescribing it.** The adaptive rule is
   *given* the surviving pair and still scores slightly below the fixed
   protocol, losing on `neighbour_mild`. Maximising a predicted, noiseless
   separation is not the same as maximising realised discrimination, and here the
   loss outweighs the occasional better choice.
3. **The one real adaptive advantage is robustness, not accuracy.** Under poor
   mixing the fixed protocol drops to 0.542 while adaptive holds 0.708, because
   reading the neighbour does not depend on room A being well mixed. That is
   consistent with gate 2 and worth recording, but it is not what the gate asked
   for, and on specified cases — the condition the gate names — it is absent.
4. **Neither protocol estimates the rate usefully.** Median absolute error is
   0.0-0.1 ACH but the 90% interval is never narrower than one grid step, and
   coverage is 1.000 everywhere, so the estimates are coarse-but-honest rather
   than sharp. The third narrowing condition in the kill gate would also fail:
   the gain, where there is one, is confined to picking between two named
   stories.
5. **The changing-weather holdout did not bite.** It inflates the residual sum of
   squares but leaves discrimination unchanged, because the paired hypotheses
   differ in room B's exchange and the weather multiplier scales both
   hypotheses' outdoor flows equally. It is reported as run, not as informative.
6. **The unidentifiable control failed for everyone**, as it must. Where two
   hypotheses differ only in a sensor offset and the offsets are fitted, no
   protocol can separate them, and the honest output is a refusal rather than a
   number.

### One design correction made mid-experiment

The first build put sensors in both rooms and paired hypotheses with equal total
exchange but different splits between outdoor and inter-room flow. Measured, the
room-A traces of such pairs differed by 32 ppm RMS against a 6 ppm sensor noise,
so the pair was separable from passive data and the comparison was vacuous. That
build was rejected before any result was recorded. The pairs used above hold
`q_ext_a + q_ab` fixed *and* keep room A's exposure constant, which makes the
passive room-A trace identical (0.0 ppm RMS by construction for four of the six
families; 3.8 and 32.4 for the two where room A's own outdoor flow differs).

## What this does and does not show

- **Does show:** the strongest available baseline in this experiment — one
  prescribed intervention — matches or beats adaptive selection at equal budget
  on correctly specified cases, so the measurement-design advantage the candidate
  proposed is **not** demonstrated. Recorded as `FAILURES.md` F008.
- **Does show:** a modest, real robustness advantage for reading a second sensor
  under poor mixing. That is a narrower claim than the candidate's, and it is
  the kind of thing an existing package could add.
- **Does not show:** that no experimental-design method could help. The adaptive
  rule here maximises a noiseless predicted separation, and was given the
  surviving pair for free. A rule that also had to generate the pair, or that
  optimised an expected information criterion rather than a predicted separation,
  was not tested.
- **Does not show:** anything about a real room. Synthetic two-node mass balance,
  30 m3 and 25 m3, one occupant source constant, no drafts, no infiltration
  modelling, no real sensor behaviour.
- **Does not touch novelty.** `RESEARCH/C.md` already records QICO2, CONTAM,
  NVAPF and PopED as prior art, and nothing here changes that.

## Limits

- Grid fitter: 0.2 ACH resolution on the reported parameter, 0.4 on the
  nuisance, 3 points for room B's outdoor flow. A finer grid would sharpen the
  intervals but not change which protocol discriminates better, because the
  discrimination statistic is a comparison of two fixed-hypothesis residuals and
  does not use the grid at all.
- The adaptive rule knows the surviving pair. The information cost of producing
  that pair is excluded, which favours adaptive and still did not save it.
- Eight seeds per cell: discrimination differences of a few percent are within
  noise and are not claimed as differences.
- `offset_only` is a synthetic impossibility, not a measured prevalence.
- Metric 4 (`false precise`) uses an engineering threshold of 0.4 ACH declared
  before the run. Both protocols are near zero at it, so the metric has little
  power here.
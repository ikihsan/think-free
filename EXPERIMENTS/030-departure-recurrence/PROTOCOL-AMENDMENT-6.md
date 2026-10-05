# E030 — Amendment 6

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after one run of `recurrence.py` and before the second.** The
first run produced a control-arm statistic that is zero *by construction*. That is
a defect in the declared rule, it is corrected here, and the correction can only
make the result worse for the hypothesis.

## 1. The defect, exactly

The protocol's primary statistic is *"accounts in a **multi-artifact** cluster ÷
|arm|)"*, and it defines a multi-artifact cluster as one with **≥ 2 distinct
departing artifacts and ≥ 2 distinct authors**.

**The control arm has no departing-artifact field.** Its accounts were selected
precisely for *not* containing a framing phrase, so `artifact` is `null` on every
row and never resolved. Every control cluster therefore has **0** artifacts, every
control cluster fails the multi-artifact test, and `R_c = 0.0000` — not because
ordinary comments never share a clause, but because the criterion is unsatisfiable
for them.

The first run's own log shows how obviously this is an artefact and not a finding:
the control arm produced **165 clusters of size ≥ 2** and **0** qualifying ones.
**That run's `R_c`, its difference and its CI are withdrawn.**

## 2. The correction, and the direction it can move the result

Two criteria are computed for every cluster, and both are reported:

| criterion | definition | arms it is defined for |
|---|---|---|
| **shared** | ≥ 2 distinct **authors** | **both** — identical rule, no asymmetry |
| **multi-artifact** | ≥ 2 distinct authors **and** ≥ 2 distinct departing artifacts | treatment only; control reports `not_defined` rather than 0 |

`R_shared` is the statistic the B gates are read on, because it is the only one
defined for both arms. `R_multi` is reported for the treatment arm as the
protocol's stricter version, **with the control side marked `not_defined`** and no
difference computed against it.

**Direction, stated because it decides whether the correction is convenient.** The
shared criterion is **weaker** than the one the protocol declared for the treatment
arm (it drops the artifact condition) and **stronger** than the condition the
control arm was accidentally given (which was unsatisfiable). So the correction
**raises `R_t`, raises `R_c`, and shrinks the difference.** It is the correction
that most reduces the measured effect, and it is the one made.

## 3. The B gates, restated onto the corrected statistic

Unchanged in substance, applied to `R_shared`:

- **B1 fires** if `R_shared(treatment) − R_shared(control)` ≥ **0.10**, its CI95
  excludes **0**, and the treatment arm has **≥ 3** multi-artifact clusters.
- **B2 fires** if the two arms' `R_shared` CI95 intervals **overlap**, **or** the
  treatment arm has **fewer than 2** multi-artifact clusters.
- **B3** otherwise.

## 4. A diagnostic added, feeding no gate: stories per cluster

`AMENDMENT-4` §2 showed that the artifact field does not reliably name what the
account is about, and the signature rule removes the story **title's** tokens but
not the rest of a story's vocabulary. A cluster of accounts from one story may
therefore share rare tokens because they are **in one conversation**, not because
two strangers failed at the same task. That is the same confound W-A named, one
level down.

So every cluster now also records **`n_stories`**, and two further statistics are
computed and reported **feeding no gate**:

- `R_cross_story` = accounts in clusters spanning **≥ 2 stories** ÷ |arm|, both
  arms, identical rule;
- the top clusters are printed with their accounts' stories, authors and artifacts
  so a reader can see whether the linkage is a shared clause or a shared thread.

**Declared here, after the first run's numbers were in hand, and for that reason
the cross-story figure is not a substitute for the declared statistic.** It is the
diagnostic that says whether the declared statistic means what it says.

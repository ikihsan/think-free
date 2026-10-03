---
name: falsification-design
description: Design the experiment that could disprove a claim before implementing it, including kill gate, strongest baseline, controls, and honest acceptance criteria. Use BEFORE writing code for any claim that could be wrong, before prototyping a hypothesis, or when an existing prototype has not been given a real chance to fail. Triggers - "how do I test this?", "what would prove this wrong?", "design the experiment", "set up an ablation", "is this worth building?", or before any prototype.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: mission-record
  enforcement: evidence-record
---

# Falsification design

A prototype that cannot fail teaches nothing. This skill front-loads the way a
claim could be wrong, so the cheapest possible thing can be built to find out.

Protocol: [`docs/process/experiment-protocol.md`](../../../docs/process/experiment-protocol.md).
Adversarial checklist: `RESEARCH/D.md` in this repository.

## Before implementation, write down

1. **The claim, in one sentence, with its scope.** "Useful" and "novel" are not
   test assertions. "Given commodity sensor CSV, adaptive selection of the next
   ventilation measurement separates exchange-rate hypotheses better than a
   fixed protocol" is a test assertion.
2. **The strongest baseline**, named specifically. Not a strawman. If it cannot
   be executed here, label the comparison **unperformed** and say why.
3. **The kill gate**: the exact result that ends this line of work, with a
   number. "If it does not feel useful" is not a gate. "If adaptive selection
   fails to beat the fixed protocol on more than 60% of paired parameter sets" is.
4. **Inputs, oracle, thresholds, and resource limits**, all fixed before
   observing results.
5. **Negative controls** that must fail. An experiment where every variant wins
   is measuring the wrong thing.

A gate written after seeing results is a rationalisation. Write it first.

## The information-sufficiency test

The single most productive falsification step, before any implementation:

Construct **two underlying realities that produce identical inputs but require
different outputs**. If they cannot be distinguished from the permitted inputs,
the design is wrong. Your options are to narrow the claim, to request one more
observation, or to permit abstention.

This is cheap, it needs no code, and it eliminates proposals that no amount of
implementation could rescue. Build it as a tiny numerical witness first — two
arrays, one print statement, an assertion. If the ambiguity is provable in ten
lines, prove it in ten lines.

## Choosing the smallest honest experiment

The experiment must be able to **reject** the claim. Size it accordingly:

- If the claim is universal, one counterexample is enough, and a small one is
  better than a large one.
- If the claim is a mechanism, the oracle must check the mechanism, not a proxy.
  A final row count does not verify a repair plan.
- If the claim is a performance improvement, the baseline must be the strongest
  available and the measurement must include everything the user pays: setup,
  calibration, review, correction time.
- If the claim is about usefulness, no local experiment can settle it. Say so
  early and plan for real observation instead.

## What to measure

| Measure | Why |
|---|---|
| Correctness against an independent oracle | The claim itself |
| **Abstention rate and coverage** | A tool that answers when it should refuse is worse than useless |
| Human review and correction time | Belongs in total cost; usually dominates |
| Setup steps and calibration burden | Determines adoption, and is usually ignored |
| Failure severity distribution | Average error hides the catastrophic cases |

Report distributions, not just means. Include the cases where it failed.

## Beating yourself up front

Run the experiment against your own implementation first, on purpose:

- a trivial or random variant,
- a deliberately broken variant,
- an ablation with one component removed.

If the broken variant performs as well as the real one, the experiment cannot
distinguish them and its positive result would mean nothing. This is cheap and it
catches the most common self-deception in this kind of work.

## Synthetic data rules

- Label synthetic fixtures as synthetic, always.
- Synthetic data can **falsify** a universal claim. It cannot establish
  prevalence, distribution shape, or real-world demand.
- Never report a planted defect as a discovered one.
- Fixtures must be licensed or synthetic, and their origin recorded.

## After the run

- Record commands, versions, seeds, hashes, exit codes, environment.
- Keep failures. A failed run with a preserved log is evidence; a deleted one is
  a gap.
- Have a separate reviewer check the oracle and the baseline's fairness before
  believing a positive result. Ask specifically: did the baseline get a fair
  shot, and does this oracle actually test the claim?
- Update the hypothesis record with the result, the uncertainty that remains, and
  the decision. Distinguish a failed implementation from a failed idea.

## Abandonment

Abandon when the kill gate is met, when gains disappear under modest changes to
assumptions, when the advantage exists only for deliberately weakened baselines,
or when the useful output cannot be defined without arbitrary inputs.

Abandoning on evidence is success. Defending a candidate because effort was
spent is the failure mode this repository exists to avoid.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Hypothesis lifecycle

How a candidate becomes a decision. The aim is that no candidate is ever
believed because it was written down persuasively.

Prior art: [`prior-art-check` skill](../../.agents/skills/prior-art-check/SKILL.md).
Falsification: [`falsification-design` skill](../../.agents/skills/falsification-design/SKILL.md).
Records: [`evidence-record` skill](../../.agents/skills/evidence-record/SKILL.md).

## Stages

```
observation
    │
    ▼
hypothesis ── prior art check ──▶ killed (clone / no meaningful difference)
    │
    ▼
kill gate written ── experiment designed
    │
    ▼
experiment run ──▶ mechanism survives?  ── no ──▶ FAILURES.md
    │
   yes
    │
    ▼
useful to a real person? ── unobserved ──▶ hold, seek observation
    │
   yes
    ▼
differentiated? ── no ──▶ narrow, or contribute upstream
    │
   yes
    ▼
committed
```

Each stage has an entry condition and an exit condition. A stage may be
repeated; it may not be skipped.

## Entry and exit conditions

| Stage | Enter when | Leave when |
|---|---|---|
| Observation | Something was seen or read | A specific unexplained gap is named |
| Hypothesis | A gap is named | Mechanism, assumptions, and kill gate are written |
| Prior art | A mechanism is proposed | Difference stated in one sentence, or killed |
| Experiment | A gate and baseline exist | Result recorded with raw artifacts |
| Useful | Mechanism survives | A real person is observed using it, or it is held |
| Differentiated | Usefulness is plausible | The strongest alternative is beaten on a stated metric |
| Committed | All of the above | Engineering starts with tests |

"Unobserved" is a legitimate long-term state. Most mechanisms never pass it, and
recording that honestly is more valuable than simulating it.

## What may not be skipped

- **Prior art before novelty.** Not after. The cost of checking is an afternoon;
  the cost of skipping is the whole project.
- **Kill gate before implementation.** A gate written afterwards is a
  rationalisation.
- **Baseline before comparison.** The strongest available one, actually run.
- **Negative results before commitment.** A candidate never adopted without at
  least one attempt to kill it.

## The information-sufficiency check

Run this before implementing anything, because it needs no code:

Construct two underlying realities that give the proposed system identical inputs
but that require different outputs. If such a pair exists, the design is wrong
regardless of implementation quality. Narrow the claim, ask for one more
observation, or permit abstention.

Proposals already killed by this test in this repository, recorded in
`RESEARCH/D.md`: appliance disaggregation from aggregate power only, ventilation
rate from a single CO2 decay curve, and universal accessibility certification from
static DOM analysis.

## Deciding

Prefer to abandon. A repository that accumulates undefended candidates is
collecting sunk cost, not evidence. Before committing, be able to answer:

- What single result would prove this wrong?
- What is the strongest existing approach, and have we actually run it?
- Would an independent engineer reproduce every claim?
- Is this better as a contribution to something that already exists?
- What does adoption cost the user, in steps and in understanding?

Any "no" or "cannot answer" is a reason to hold or narrow, not to proceed faster.

## Reconsidering

A held candidate reopens when something changes: new evidence about the prior
art, a technical development that removes a constraint, or observation of a real
person struggling with exactly this. Reopening requires new evidence, not
new enthusiasm.

An abandoned candidate stays abandoned unless the specific evidence that killed
it is invalidated. Record that evidence in `FAILURES.md` so the next session can
find it in one grep.
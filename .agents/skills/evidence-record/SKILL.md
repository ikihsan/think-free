---
name: evidence-record
description: Write and update hypothesis, experiment, decision, and failure records using this repository's evidence labels and templates. Use when creating or updating anything in HYPOTHESES.md, DECISIONS.md, FAILURES.md, STATE.md, RESEARCH.md, or an EXPERIMENTS/ directory. Triggers - "new hypothesis", "record the decision", "log this failure", "update STATE.md", "write up the experiment", "what did we learn", or before committing any result.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: mission-record
  enforcement: tools/origin session finish
---

# Evidence record

The mission's durable memory is `MISSION.md`, `STATE.md`, `DECISIONS.md`,
`HYPOTHESES.md`, `FAILURES.md`, `ROADMAP.md`, `RESEARCH.md`, `RESEARCH/`, and
`EXPERIMENTS/`. This skill defines how to write into them.

Labels: [`docs/policy/evidence-labels.md`](../../../docs/policy/evidence-labels.md).
Experiment design: [`docs/process/experiment-protocol.md`](../../../docs/process/experiment-protocol.md).

## Label every claim

`observed`, `source-supported`, `inferred`, `speculative`, `untested`. An
unlabelled claim is treated as `untested` however confident it sounds. If the
label is uncomfortable, that is information: either gather evidence or downgrade
the claim.

## Hypothesis record

Required fields. A hypothesis missing one of these is not ready to test.

```
### H-nn — short falsifiable claim

Observation:     what was seen or read, with a source or a command
Mechanism:       the proposed cause or approach, in one paragraph
Assumptions:     each thing that must be true, listed separately
Prior art:       nearest existing work, and the precise claimed difference
Strongest        why this might be worthless even if it works
  objection:
Kill gate:       the exact result that ends this line of work
Baseline:        the strongest existing approach, and how it is run here
Experiment:      smallest runnable test, with its reproduction command
Result:          observed facts, or `untested`
Uncertainty:     what the result does not settle
Decision:        advance / narrow / hold / abandon, with the reason
Reconsider when: the new observation that would reopen it
```

The **kill gate** is written before the implementation. A gate written
afterwards is a rationalisation, not a criterion.

## Experiment directory

Every experiment is self-contained and runnable:

```
EXPERIMENTS/0nn-slug/
  README.md      hypothesis, kill gate, baseline, controls, limits
  run.py|.sh     the implementation
  results.json   raw output, machine-readable
  failure.json   written only when a run failed, and kept
```

Requirements:

- One reproduction command, from the experiment directory.
- Pinned versions, seeds, input hashes, and the source revision.
- Negative controls and, where relevant, an adversarial case.
- Synthetic data labelled as synthetic.
- Failures retained. A failed run is evidence.

## Decision record

Decision-log entries: identifier, date, what was decided, the evidence, the
alternatives rejected, and the reason. Record a decision when a choice was
genuinely open and the choice constrains later work — not every edit.

Which file it goes in is decided by invariant, not by size. `DECISIONS.md` is
the index; `DECISIONS-FOUNDATION.md` holds what the mission is, what the
workspace is, and what counts as evidence; `DECISIONS-PRACTICE.md` holds how
work is recorded, moved, and published; `DECISIONS-GATING.md` holds how work
is verified, screened, and judged.

```bash
tools/origin session decision "…" --refs <files>
```

`session finish` fails with a documentation gap if a `decision` event exists and
no decision record changed. Any one of the three clears it. That check is the
point.

## Failure record

`FAILURES.md` requires the distinction that matters most:

| Statement | Means |
|---|---|
| "The implementation was wrong" | The approach may still work; the code did not |
| "The approach does not work" | The idea is disproved; do not rebuild it |
| "The measurement was inadequate" | Unknown; fix the experiment and re-run |
| "Access or resources blocked it" | Unknown; record the blocker precisely |

Record the reason it was killed, not just the fact. A future session that
revisits the same idea needs to know what evidence stopped it, or it will
re-spend the same effort.

## Updating STATE.md

`STATE.md` is the reload point. Keep it short enough to read entirely, and make
it current rather than comprehensive.

Required sections: verified status by area, resume procedure, current next
actions, and the capability evidence with its date. Update it in the same commit
as the work it describes. A stale `STATE.md` costs more than a missing one,
because it is trusted.

## Rules

1. A claim without a reachable artifact is `untested`.
2. One local timing is not a benchmark; record repetitions or label it `observed`.
3. A search that finds nothing is not evidence of originality.
4. Preserve negative results. A disproved option is progress.
5. Never describe planned work as completed, in any document.
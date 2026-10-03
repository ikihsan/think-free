<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures and negative results

Disproved ideas, failed implementations, and the lessons worth keeping. An
abandoned option is progress; a silently dropped one is a repeat.

Distinguishing the kind of failure matters, because it determines the next step:

| Statement | Consequence |
|---|---|
| The implementation was wrong | The approach may still work |
| The approach does not work | Do not rebuild it |
| The measurement was inadequate | Unknown; fix the experiment |
| Access or resources blocked it | Unknown; record the blocker precisely |

## F001 — Photo-migration auditor: the motivating example is not evidence

Source: `RESEARCH/B.md`, `EXPERIMENTS/001-photo-baseline/`.

**Observation.** Investigation B found a published bug report
(`immich-go` issue 1422) in which an importer reported `Errors: 0` while two
images were missing from the destination, and proposed a source-relative
migration verifier as a candidate invention.

**Experiment.** `EXPERIMENTS/001-photo-baseline/run.py` reconstructs the
accepted-operation model from the published API trace and compares the
destination's content set against the source fixture's, using a plain checksum
set difference — the cheapest baseline available, with no relationship inference.

**Result.** `observed`. The baseline recovered exactly the two missing filenames
(`REPRO_eaaed6cd_A-edited.jpg`, `REPRO_eaaed6cd_B.jpg`) from a
`4 → 3 created − 1 deleted` trace, with all four controls passing.

**Conclusion.** The motivating failure is fully explained by source-relative
checksum comparison. It demonstrates a defect in **importer reporting**, not a
gap that requires a relationship-aware auditor. The checksum baseline is
structurally blind to relationship-only loss, but that blindness was not
demonstrated to occur in a real case.

**Classification.** The candidate's *chosen motivating example* is disproved. The
idea is not disproved; it is unevidenced.

**Decision.** Do not build the verifier on this basis. A standalone tool is
premature while the motivating example needs no novel mechanism. Per `RESEARCH/B.md`,
a fixture or audit contribution to an existing project may be the better outcome,
and real destination observation remains a genuine untested opportunity.

**Limits.** The fixture and trace are published artifacts, not an independent live
reproduction. An accepted deletion may complete asynchronously, so the model is not
a measured final server state. No conclusion about whether the bug is still present.
Nothing measured about prevalence, usefulness, novelty, or adoption.

## F002 — E001 first run: implementation failure, not hypothesis failure

**What happened.** The first execution of `run.py` raised `AssertionError` with
`accepted_operations_match_reported_missing_contents: false` and
`expected_trace_operation_counts: false`. Preserved in
`EXPERIMENTS/001-photo-baseline/first-failure.json`.

**Diagnosis.** The runner expected four asset creations and one deletion; the
published trace excerpt contains three creations and one deletion. The fixture's
reported missing pair requires accounting for operations outside the excerpt.

**Classification.** Implementation failure. The baseline's adequacy as an
explanation of the case was not tested by this run and was tested by the later
successful run (F001).

**Lesson kept.** A failure record distinguishes the two classifications
explicitly, so a later reader does not read a parser bug as a refutation. The
original `first-failure.json` was left in place rather than deleted.

## Open, not yet disproved

These remain live questions, not settled negatives:

- **Knitting repair planning** (`RESEARCH/C.md`): graph representation is prior
  art; whether an *intervention* planner is differentiated and physically
  feasible is untested.
- **Adaptive ventilation measurement selection** (`RESEARCH/C.md`): NVAPF and NIST
  tools occupy uncertainty-aware estimation; identifiability-focused selection may
  be an extension rather than an invention.
- **Sidewalk survey prioritisation** (`RESEARCH/A.md`): strong value story,
  substantial prior art; the decision-value advantage is untested.

## Reopening

A failed idea returns when the specific evidence that killed it is invalidated —
not because effort was previously spent on it. Record that evidence here so the
next session finds it in one search.
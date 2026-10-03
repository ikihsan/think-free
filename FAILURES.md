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

## F003 — Session 002 under-declared its artifacts; reconciliation caught it

**What happened.** The first full working session (`2026-10-03-002-build-durable-session-infrastructure-ven`)
finished with 57 declared artifacts and 55 further files that had been created and
committed without ever being declared. `session finish` reported all 55 as
`UNLOGGED` and exited `4`.

**Classification.** A process failure in the agent's own bookkeeping, not a tooling
failure and not a hypothesis failure. The tooling behaved exactly as designed: it
compared the working tree against the record and reported the difference.

**Root cause.** Artifacts were declared in one batch at the end of the session, from
a hand-written list. With 57 items that list was inevitably incomplete, and there was
no way to sweep a directory without enumerating it by hand.

**Not remediated by backfill.** The event stream is append-only by contract and the
session was closed, so writing artifact events afterwards would have broken the
invariant that `session_end` is the last event. The omission stands in the record.
This entry is the remedy.

**Fix applied.** `origin session artifact` now accepts several paths and a repeatable
`--dir`, so a directory of authored files can be declared in one command. Each file
still gets its own hash, because a hash of a directory says nothing about its contents.
Covered by five tests in `tests/test_session.py` (`ArtifactBatchTest`).

**Lesson.** Declare artifacts as they are created, not in a batch at the end. A
reconciliation report that fires on a correct piece of work is still a correct report:
the work was complete and the record was not.

## F004 — The new directory sweep declared 13 build-output files

**What happened.** Immediately after F003 was fixed, a `--dir tools` sweep
declared every file beneath `tools/`, including 13 `__pycache__/*.pyc` artefacts.
They appeared in session 003's generated report as if they were deliverables.

**Classification.** Tooling defect, found by reading the report rather than by a
gate. `session verify` cannot detect it: the files were genuinely declared, with
genuine hashes, and the event stream is valid.

**Root cause.** The sweep expanded a directory to all of its files without asking
git which of them are tracked. A directory sweep is exactly the operation that
walks into build output.

**Fix.** `gitutil.is_ignored` now backs both paths: an explicitly named ignored
file is refused with an explanation, and a directory sweep skips ignored files and
prints what it skipped. Three tests in `tests/test_session.py` (`IgnoredArtifactTest`).

**Lesson.** A sweep that trusts the filesystem will eventually sweep the build
directory. Anything derived from a source file is noise in an evidence record.
This is the same reasoning that makes vendored content hash-verified rather than
declared, and it should have been applied when `--dir` was added, minutes earlier.

**Not remediated in session 003.** Its events stay as they are. Editing a closed
session's append-only stream to remove them would be worse than the noise.

## F005 — Claims were local-only, so two VMs could both own one task

**What happened.** `docs/process/task-lifecycle.md` claimed that "a second agent
claiming a held task fails with exit 1 and names the holder. This is the only
concurrency control, and it is enough for a fleet that respects claims." That was
false for the actual fleet. `origin task claim` read and wrote the *local* task
file only. Two VMs whose working trees were both at `status: open` both claimed
successfully, each in its own private copy of the file. The second push to the base
branch would be the one that survived, and the loser's task file still said
`claimed` locally.

**Classification.** Design gap in the tooling, not an agent mistake, and not a
hypothesis failure. Nothing detected it: there was no test with two clones and no
command that consulted the remote.

**Root cause.** Exclusivity was asserted in prose while the implementation used
per-machine state. A claim is only mutual exclusion if the loser finds out, which
requires a shared arbiter. Git already provides one: the remote ref update is an
atomic compare-and-swap, and a rejected push *is* the loser signal.

**Fix.** `tools/originlib/taskremote.py`: claims are committed **and** pushed to
the shared base branch, the claim commit must be the only thing between the branch
and the base, a rejected push discards the claim commit and reports the winner, and
`--takeover "reason"` is the only way to take a dead VM's task. Task listings
default to the remote's view. Tests in `tests/test_fleet.py` drive two clones of a
local bare remote.

**Lesson.** "This is the only concurrency control" was a claim about behaviour
written in a document, not a measurement. Any statement about what happens when
two machines act at once has to be exercised by a test with two machines in it,
otherwise it is a hope with a docstring.

## F006 — Decision-directed advantage does not transfer to a fieldwork-cost budget

Source: `EXPERIMENTS/002-a1-masking/distance.py`, `distance.json`, T-0007.

**Observation.** T-0006 showed DD's advantage holds under a *count* budget
(150 of 955 crossings) even at the K~budget corner. The open question was
whether it survives the realistic cost metric: walking distance.

**Experiment.** The same masks, priors, and policies as `masking.py`, but a
policy's observations are whatever it can visit on a walk from the
southwest corner that stays under D meters (D ∈ {40, 80, 160} km; the full
nearest-neighbour tour of the neighbourhood takes ~190 km). 30 seeds, both
mask modes, K=20, same regret definition.

**Result.** `observed`. Median regret: centrality 16.3 (D=40 km) and 0
(D ≥ 80 km); decision-directed 85.2 at every D; dd-walk (DD value per
metre) 134.6 at D=40 km and 85.2 at D ≥ 80 km. The gate (DD within 25% of
the strongest baseline in every config) failed in 6 of 6 configurations for
both DD and dd-walk.

**Conclusion.** The mechanism worked because of *what it observed*, not the
budget: under a count budget DD fills 150 slots in 150 steps; under a walk
budget its scattered marginal-value picks consume the distance cap after
~17–60 hops, while space-filling baselines (centrality, tour) cover the
neighbourhood. The DD-advantage hypothesis is **not confirmed** in the
fieldwork-cost regime that motivated A1. This does not kill DD as a policy,
but it kills "budget-limited implies DD wins".

**Lesson.** A budget has a unit, and the unit is part of the hypothesis.

## F007 — Knitting repair planner: the stated input set is information-insufficient

Source: `EXPERIMENTS/003-information-sufficiency/`, witness W2, T-0008.

**Observation.** `RESEARCH/C.md` proposes a local repair planner whose inputs are
"the intended chart, the actual local error, the current live stitches, and the
side facing the user". The information-sufficiency witness asks whether two
underlying realities can share exactly those inputs yet need different repairs.

**Experiment.** Witness W2 in `EXPERIMENTS/003-information-sufficiency/witnesses.py`.
Reality A: the dropped loops are mounted normally, so the repair is to re-form
them in place. Reality B: the same loops are mounted twisted, so the repair is to
re-form them *and* untwist. Both present the same chart symbols, connectivity,
live stitches, and facing side; physical mount is not in the input.

**Result.** `observed`. The two realities share identical permitted inputs and
require different repairs, and nothing in the stated input set can represent the
difference.

**Conclusion.** The candidate's *input specification* is information-insufficient:
as described, no implementation can choose between the two repairs. This is a
failed claim about the input set, **not** a failed mechanism — a knitter can see
orientation, so adding mount (or refusing ambiguous states) repairs the
specification. The design as written must be narrowed before any planner is
built.

**Classification.** The stated input set is disproved as sufficient. The
intervention-planning idea is not disproved; it is under-specified.

**Limits.** A four-loop synthetic patch with one error class. It does not measure
how often real errors are ambiguous, nor whether physical slack or friction
dominates repair success (the candidate's own Stage-B doubt). It cannot show that
*no* fix exists — only that the present one does not.

**Lesson.** "What are the inputs?" is a falsifiable claim. Test it before writing
the algorithm, because the algorithm cannot recover a fact its inputs omit.

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
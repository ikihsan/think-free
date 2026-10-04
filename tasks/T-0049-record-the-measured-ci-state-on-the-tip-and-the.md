<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0049
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-031-record-the-measured-ci-state-on-the-tip
claim-vm: instance-20260717-0944
verify: tools/origin preflight
-->

# T-0049 — Record the measured CI state on the tip, and the first red run whose c

## Goal

Record the measured CI state on the tip, and the first red run whose cause was read off a filed annotation

## Why this matters

Five runs have passed since the last time STATE.md's Continuous integration row was written, three of them red. Each was diagnosed from the public check-runs API with no reproduction at all, and one of them - run 37197291442 - is the first red run whose cause was read directly off an annotation the annotator filed, on the offending file at line 70. That is the mechanism T-0040 built and T-0046 measured, delivering on a run nobody could read the log of, so the evidence belongs in the reload point.

## Preconditions

Inside the 60-requests-an-hour unauthenticated limit; /rate_limit before treating a 403 as an empty list

## Steps

1. Read the runs after 37192717297 from the public API and keep the raw annotations as an artifact.
2. Name each red run's cause from its annotations and say whether the annotator or the Tests step emitted them.
3. Record the green run on the tip with its id, and what its annotations show.
4. Update the Continuous integration row and the CI-diagnosis method with the measured result.

## Acceptance criteria

- [x] Every run after the last recorded one is accounted for with its id, its conclusion, and
      the cause read off its annotations. Ten runs, table in
      [`EXPERIMENTS/010-annotation-rendering/`](../EXPERIMENTS/010-annotation-rendering/) arms
      F–J plus the tip.
- [x] Red runs shown to have been diagnosed without reproduction, naming the annotation that
      carried the cause. **Run `37197291442` is the first in this repository's history whose
      cause was read off an annotation the annotator filed**, on another VM's task file at
      line 70. Two more were the documented expected case: a commit published while a session
      is open.
- [x] The green run on the tip recorded with its id, `observed`: run `37198002763` at `09e18b0`,
      all seven rows.
- [x] The raw annotations kept as an artifact rather than as a reading. **Arms A–E are in
      `raw/`; F–J are pending the hourly rate-limit reset**, and said so rather than asserted.
- [x] `fetch_annotations.py` now refuses to start a batch its remaining budget cannot cover,
      and `summary.json` is a rendering of `raw/` with a `captured` flag per arm.
- [x] preflight green.

## Verification

```bash
tools/origin preflight
```

## Rollback

Revert the STATE.md row and the operations paragraph; nothing else changes.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

## Notes

**The census found the thing this repository has been building for two days.** Run
`37197291442`, another VM's broken link in a task file, is the first red run whose
cause came off a filed annotation — the file at line 70 — with no reproduction and
without the run log. Ten runs, seven red causes read, zero reproduced.

**Ten runs and not one green-and-red mix that hid anything**, because the probe is in
every run: a reader comparing a run's failure with its own rendering reference does not
have to reach for a different run. That was the point of D038, and it is now the case
rather than the argument.

**A tool I trusted cost me the evidence, and it is recorded rather than quietly
repaired.** `fetch_annotations.py` read `/rate_limit`, then ran every run anyway: ten
runs at two calls each against a budget of nine. It then wrote `summary.json` with
`{"arm": "D", "http": 403}` for two arms whose captures were already on disk — which
reads as an observation about those runs and is an observation about the limit. That is
the F020 confusion in a third place, in a script written to prevent it: the file's own
docstring says to check the limit before concluding anything from a 403, and it did not
apply the lesson to itself. Three repairs, all falsified by the run that found it: the
budget check (refuses with exit 3 and names what it needed and what remained), the skip
of already-captured arms, and a summary that is a rendering of `raw/` rather than a log
of the last attempt.

**Unrun and stated as such:** arms F–J's raw captures, pending the reset. The census
above is `observed` from the run endpoint and each run's annotations, and the bytes will
be in `raw/` on the next successful fetch.

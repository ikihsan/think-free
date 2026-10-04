<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0046
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-029-measure-how-github-files-an-annotation-o
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin preflight
-->

# T-0046 — Measure how GitHub files an annotation on the file= property, and repa

## Goal

Measure how GitHub files an annotation on the file= property, and repair the false record and the gate step that never ran

## Why this matters

docs/operations/ci-diagnosis.md says the annotator's rendering is unmeasured and that run 37189825232 carried '::error file=tools/originlib/identifiers.py::' in an annotation whose path was .github. Both are false and both were read off the public API. The string is a unittest assertion diff from the Tests step, not an emitted annotation: that row's Tests step failed, so every later step with an if: expression was skipped by GitHub's implicit success(). Run 37191658964, where Tests passed and only Documentation lint failed, carries an annotation with path=DECISIONS-RECORDS.md. So the renderer files the annotation and the mechanism has run once.

## Preconditions

The annotations endpoint is public and this VM is inside the 60-requests-an-hour unauthenticated limit; /rate_limit must be read before treating a 403 as an empty list

## Steps

1. Read the annotations of the three red runs of 2026-10-04 from the public check-runs API and keep the raw JSON as an artifact.
2. Establish which of the emitter and GitHub's renderer is responsible for the annotation's path, from the run whose gate step actually ran, and name the false reading it replaces.
3. Falsify the repair: a step whose only job is to emit diagnostics is skipped when an earlier step fails, because an if: expression gets an implicit success(). Confirm against the two runs whose Tests step failed.
4. Give every diagnostic step a status function, and hold the workflow to it with a test whose failure is the unmodified workflow.
5. Add a probe that emits one annotation per rendering shape on every run, so the same run that reports a failure also says how GitHub renders each shape, and hold its shapes with a test.
6. Correct docs/operations/ci-diagnosis.md, ROADMAP.md, STATE.md and STATE-next-actions.md; record the finding, the defect, and the gating decision T-0040 owed.

## Acceptance criteria

- [x] The runs' annotations are captured raw and kept as an artifact, with the
      commit and check-run ids each came from. Four runs, not the three named on
      creation: a green run is the control that makes `.github` readable as "no
      path was given" rather than "a path was discarded".
      `EXPERIMENTS/010-annotation-rendering/raw/`, fetched by a script that reads
      `/rate_limit` first and refuses to proceed without a verified limit.
- [x] `docs/operations/ci-diagnosis.md` says what the annotations actually say: run
      `37191658964`'s `Documentation lint` annotation carries
      `path=DECISIONS-RECORDS.md`, so GitHub files an annotation on the `file=`
      property, and the `37189825232` reading is named as the false one it was.
- [x] ROADMAP.md's claim that no pushed commit has exercised the annotator is
      corrected, since one has, with the run id.
- [x] Every workflow step whose purpose is to emit a diagnostic names a status
      function, and a test fails on the workflow as it is today. Falsified: with
      `always() &&` reverted to the bare matrix guard the assertion fails and names
      the step and its expression.
- [x] A probe emits one annotation per rendering shape on the run that reports a
      failure, always exits 0, and a test asserts each shape it claims to measure.
      Falsified: deleting one shape from the table fails the test that holds the
      list literally, so the code, the test and the document cannot drift apart.
- [x] The finding, the defect and the gating decision T-0040 owed are recorded,
      each with the label its evidence carries. `FAILURES.md` F021, defect 18, and
      D037/D038 in `DECISIONS-GATING.md` — which had room again only because T-0042
      split it, so the entry the record said was waiting for that split is written.
- [x] The suite and all four preflight gates are green. 485 tests in 227s and
      `preflight: OK`, `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin preflight
```

## Rollback

Revert the workflow's if: lines, the probe command and its test, and the document edits. Nothing else reads the probe.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The measurement settled the question the task was created to ask, in one call,
against the one run of four whose annotating step had run.** Run `37191658964`:
`Tests` green on the 3.12 row, `Documentation lint` alone red, and an annotation
with `path: DECISIONS-RECORDS.md`, `start_line: 0`, and the annotator's message
verbatim. GitHub files it. `docs/operations/ci-diagnosis.md` had said the rendering
was `unmeasured` and told the next reader to read `file=` as "the reader is told
which file", not "the annotation is filed on it" — so the record understated a
mechanism that had already worked.

**The wrong run was wrong in a way the endpoint could not show.** `37189825232`'s
`Tests` step failed, and every later step carried an `if:` naming no status
function, so GitHub's implicit `success()` skipped all five gate steps. The
annotator emitted nothing on that run. Its `::error file=…` string was the first
line of a unittest assertion diff — `AssertionError: Lists differ: ['::error
file=…'] != []` — re-emitted by the same awk. Two readings stacked: a test's
expected text read as an emitted command, and `.github` (what a *fileless* command
gets, as the green run shows three of) read as a verdict on one that carried
`file=`. Confounded by construction: a renderer that honours `file=` and one that
ignores it both produce `.github` on a run where nothing carried a `file=`.

**The repair's second half is the general one, and the suite found its first
false positive.** `always() &&` on each diagnostic step, held by
`tests/test_ci_annotations.py`. But `tests/test_ci_matrix.py` read a step's guard
with `if:\s*matrix\.python-version`, so `if: always() && matrix…` read as an
*unguarded* step — and the test concluded a gate would run on seven rows when it
runs on one. That is D025's shape in a fourth place: a parser anchored on the one
form it had seen. The suite said so rather than the change being landed and
discovered later, which is the whole argument for `preflight` running the suite
(T-0045).

**The probe emits no `::error`, and that is a decision rather than a style.** No
run in this repository's history has an error-level annotation on a green job, so
whether one would change the conclusion is unmeasured — and putting that
assumption into every push is the record asserting what it has not measured. The
`::error` + `file=` shape is the one the gates emit and arm A already observed it.

**Line caps were the other cost, and two of them were real splits.**
`STATE-defects.md` and `STATE.md` were both at 300 of 300. The defect entry landed
by removing a trailing section that restated a rule its own preamble already gave;
`STATE.md` landed by moving five older session entries to `STATE-history-2.md`,
which is where T-0045 had already moved one. `FAILURES-findings-4.md` reached 300
with F021 and is now at 297. The next entry in any of them needs a split, and
`STATE-defects.md` cannot be split inside its own numbered list without
`defectlist.py` reading more than one file — that is a task, not an edit.

**Unrun and stated as such:** the probe has not executed on a pushed run, so what
GitHub does with its `line=`, its escaped message and its `warning` level is
`unmeasured` until the next green run. Read them off
`EXPERIMENTS/010-annotation-rendering/`'s shapes list rather than assumed.

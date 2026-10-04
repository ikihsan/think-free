<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0046
status: claimed
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

- [ ] The three red runs' annotations are captured raw and kept as an artifact, with the commit and check-run ids each came from.
- [ ] docs/operations/ci-diagnosis.md says what the annotations actually say: run 37191658964's Documentation lint annotation carries path=DECISIONS-RECORDS.md, so GitHub files an annotation on the file= property, and the 37189825232 reading is named as the false one it was.
- [ ] ROADMAP.md's claim that no pushed commit has exercised the annotator is corrected, since one has.
- [ ] Every workflow step whose purpose is to emit a diagnostic names a status function, and a test fails on the workflow as it is today.
- [ ] A probe emits one annotation per rendering shape on the run that reports a failure, always exits 0, and a test asserts each shape it claims to measure.
- [ ] The finding, the defect and the gating decision T-0040 owed are recorded, each with the label its evidence carries.
- [ ] The suite and all four preflight gates are green.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin preflight
```

## Rollback

Revert the workflow's if: lines, the probe command and its test, and the document edits. Nothing else reads the probe.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

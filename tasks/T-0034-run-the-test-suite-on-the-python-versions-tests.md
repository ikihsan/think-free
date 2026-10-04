<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0034
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check
-->

# T-0034 — Run the test suite on the Python versions tests/python-versions.json n

## Goal

Run the test suite on the Python versions tests/python-versions.json names as never exercised, and make CI keep running them

## Why this matters

The record's own not_exercised clause says a regression that only appears on an intermediate version 'would not be caught until a VM or a CI matrix row runs it'. The suite has run on 3.8.10 and 3.12 and nothing between, so the 3.8-or-newer floor is a claim about two points with a gap in it, and no gate closes the gap.

## Preconditions

Network reachable for portable CPython tarballs and the public Actions API. This VM runs Python 3.8.10, so it is one of the two versions already on record.

## Steps

1. Falsify the premise against the old workflow: introduce a temporary 3.9-only behaviour and show the suite green on the pinned 3.8/3.12 evidence while red on 3.9, so the gap is demonstrable rather than asserted. 2. Measure the full suite on 3.9, 3.10, 3.11, 3.13 and 3.14 locally (portable CPython), captured through tools/x. 3. Add a python-version matrix to .github/workflows/ci.yml, with the non-version-dependent gates guarded to the authoritative row. 4. Add a test that the matrix and tests/python-versions.json agree, so a row cannot be added without a recorded scope and a version cannot be recorded as unexercised while a row runs it. Falsify that test against the unmodified workflow first. 5. Update the record, docs/operations/ci.md, vm-execution.md, ROADMAP.md, STATE.md, and record the decision. 6. Push, read the pushed runs from the public API, and record what actually ran.

## Acceptance criteria

- [ ] The full suite has been observed green or red on every CPython minor from 3.8 to 3.14, with each run's scope recorded.
- [ ] CI runs a matrix row per minor version, and the non-version-dependent gates run once.
- [ ] A test fails if a matrix version has no recorded scope, or a version is listed as never exercised while a row runs it.
- [ ] The new test was observed failing against the unmodified workflow before the repair.
- [ ] The pushed CI run for the change was read from the public API and its result recorded.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin release check
```

## Rollback

Revert the workflow matrix and the record entries. The tarballs live outside the repository.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

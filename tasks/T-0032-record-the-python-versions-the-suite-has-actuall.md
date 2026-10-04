<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0032
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0032 — Record the Python versions the suite has actually run on, the way git-

## Goal

Record the Python versions the suite has actually run on, the way git-versions.json does for git

## Why this matters

Defect 6 in STATE-defects.md is open and names this as the remaining half: tests/git-versions.json records how much of the suite each git version has run, and docs/operations/vm-execution.md says plainly that 'no gate pins a Python range' and that closing that gap is unclaimed work. This VM runs Python 3.8.10 while CI pins 3.12, and the mission record once demanded a 3.11+ floor invented from one machine (T-0023) - so the range that is actually exercised is exactly the kind of claim this repository refuses to make from memory.

## Preconditions

The git record and its test are the pattern: tests/git-versions.json (schema origin.git-versions/1) and tests/test_gitversions.py, which validates the schema and that the docs point at it. docs/operations/ci.md and docs/operations/vm-execution.md are the two documents that state the gap.

## Steps

1. Establish the real exercised versions rather than assuming: which Python versions CI actually runs, and what this VM runs. 2. Write tests/python-versions.json with the same schema shape and honest scope per entry. 3. Write tests/test_pythonversions.py validating the schema and that the docs point at it, so the record cannot rot silently. 4. Update vm-execution.md and ci.md to state the exercised range and what remains unverified. 5. Falsify the new test: it must fail against a seeded defect in the record, since a test that only ever passes is not a test.

## Acceptance criteria

- [ ] tests/python-versions.json names every Python version the suite has actually run, each entry saying how much of the suite it has run - [ ] The record is validated by a test that can fail - [ ] docs/operations/vm-execution.md no longer describes the Python record as unclaimed work, and states what is exercised against what - [ ] docs/operations/ci.md names the CI Python version and points at the record - [ ] Nothing claims a floor or a range the record does not support - [ ] doc lint and the full suite are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete tests/python-versions.json and tests/test_pythonversions.py and revert the two operations documents; no tooling behaviour changes, so there is nothing else to undo.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

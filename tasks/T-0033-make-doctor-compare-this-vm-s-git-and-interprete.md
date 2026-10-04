<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0033
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0033 — Make doctor compare this VM's git and interpreter against the records 

## Goal

Make doctor compare this VM's git and interpreter against the records the suite is verified on

## Why this matters

Defect 6 in STATE-defects.md is the last open item whose halves are both now recorded and neither read: tests/git-versions.json (T-0018) and tests/python-versions.json (T-0032) say what has run, and doctor prints 'tool python3 3.8.10' and a git version without ever comparing either against those files. A VM on 3.9 is therefore undocumented rather than warned, which is the difference between a record that is true and a machine that knows it is unverified.

## Preconditions

Both records exist and are schema-checked. tools/originlib/doctor.py collects versions in collect() and renders them in summarize(); docs/operations/doctor.md states the gap in its own words and will need updating.

## Steps

1. Read both records and decide the comparison: a version is 'exercised' if the record has an entry whose version it matches, and the summary must say which record was consulted rather than a bare verdict. 2. Add the comparison to doctor, distinguishing exercised / unrecorded / record unreadable - three states, not two, so an unreadable record cannot read as an unexercised VM. 3. Test it against real records: the versions both VMs actually run must come out exercised, and a version nobody recorded must not. 4. Falsify: a comparison that always says exercised, or that reports a missing record as a failing VM, must fail the tests.

## Acceptance criteria

- [ ] doctor names, for this VM's git and interpreter, whether the suite has been exercised on that version and which record says so - [ ] Three states are distinguished: exercised, not in any record, and record unreadable - [ ] doctor on both this VM and a fleet harness reports the real versions as exercised - [ ] The tests fail against a comparison that cannot distinguish the three states - [ ] docs/operations/doctor.md states the contract and the ceiling rather than describing the gap as open - [ ] doc lint and the full suite are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete the comparison from tools/originlib/doctor.py and tests/test_doctor_versions.py and revert docs/operations/doctor.md; nothing else reads the records, so there is nothing else to undo.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

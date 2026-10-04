<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0033
status: done
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

## Outcome

`observed`. `tools/originlib/versions.py` compares each probed tool against the
record that covers it, and `doctor` prints the comparison:

```
versions python3   3.8.10     exercised (tests/python-versions.json: 3.8.10); full suite green (373 tests at T-0033)
versions git       2.25.1     exercised (tests/git-versions.json: 2.25.1); full suite green (373 tests at T-0033)
versions rustc     (none)     no record - no record covers this tool
```

**Four states, not two.** `exercised` (with the entry's own `scope` attached),
`NOT exercised`, `record unreadable`, and `no record` for the three probed tools
no record covers. The third is the load-bearing one: a comparison that cannot
tell "we looked and it is not there" from "we could not look" reports a confident
answer in both cases, which is the failure T-0025 found in this same report.

**Falsified four ways before it was trusted**, all in the session command log: a
comparison that always said `exercised` (3 failures), a missing record read as
`unexercised` (5), a summary that dropped the record name (2), and `doctor` not
reporting the comparison at all (1). The last one is worth naming: removing the
single line in `summarize` left every unit test of the comparison passing, which
is the shape of a gate that tests a module rather than the report a reader sees.

**Two defects in the first implementation, found by the tests.**

- Entries were matched in file order, so a VM on `3.12.15` got CI's `3.12`
  entry's scope instead of its own. The longest matching entry now wins.
- The real-record tests initially ran against the `RepoTest` fixture, which ships
  neither record — making every assertion about `exercised` vacuous, and the
  whole file failed for that reason. They now point `ORIGIN_ROOT` at the working
  repository, and a test asserts the files it reads exist.

**Matching is by dotted prefix, longest entry first.** The records mix
patch-level entries (`3.8.10`) with a minor-level one (`3.12`, CI's pin), so a
VM on `3.12.7` must find the `3.12` entry or the record under-reports. Dotted, so
`2.25` cannot match `2.250.1`.

**Ceiling.** `exercised` means a run happened, not that the version is
supported, and no interpreter between 3.8 and 3.12 has ever run this suite. Both
records' scopes were updated to name the 373 tests they have now run, because a
stale scope is the same defect in the opposite direction.

373 tests green; `doc lint` and `release check` exit 0.

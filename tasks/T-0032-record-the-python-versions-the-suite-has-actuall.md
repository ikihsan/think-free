<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0032
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-006-t-0032-record-the-python-versions-the-su
claim-vm: instance-20260717-0944
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

## Outcome

`observed`. `tests/python-versions.json` (schema `origin.python-versions/1`)
names every interpreter the suite has actually run, each entry carrying the scope
it ran: 3.8.10 with all 335 tests on this VM, CI's pinned 3.12 with the whole
suite on every push, and the standalone 3.12.15 from T-0016 with the 173 tests
that existed then. `not_exercised` names 3.9–3.11, 3.13 and newer, and any
non-CPython or non-Linux target.

**CI is recorded as the minor version only.** `actions/setup-python` pins
`'3.12'`; the public API does not report the patch and the run log returns 403
without admin rights, so a patch version there would be a number nobody could
check. The test enforces that.

**Falsified four ways before it was trusted**, all in the session command log: a
floor claiming `3.10`, an entry with no `scope`, CI credited with the unreadable
patch `3.12.7`, and an emptied `not_exercised` list each fail the test; the
restored record passes. The floor clause compares minor versions, so `3.8 or
newer` is supported by 3.8.10 while a record that had never run 3.8 fails — the
distinction T-0023's invented 3.11 floor needed.

**One defect in the test, caught by its first run:** the floor clause compared
version strings exactly, so it rejected the honest form of the claim. Fixed by
comparing minor versions, with the reasoning in the test.

**Defect 6 is twice-partly closed, not closed.** The claim exists and is checked;
nothing *reads* it at run time. `doctor` reports the interpreter and git it found
and stops, so a VM on 3.9 is undocumented rather than warned. That is the
reading half and it is a separate change.

335 tests green; `doc lint`, `release check` and `preflight` all exit 0.

## Two collisions, resolved in the act of this session

**A D-number collision.** `instance-20260717-0947` published its own D032 (the
collision detector, T-0030) while this session was rebasing, and this session
had already used D032 for the Python-versions record. Two different decisions,
one number. Resolved the way the repository's own rule says — renumber on the
side that has not been pushed — so this side moved to **D033**, and the entry
says so in its own text. `origin id next D` against the remote base returned
D033 before the renumber, which is the allocator doing its job one commit too
late to prevent this particular one and correctly enough to fix it.

**A conflict-marker block committed to the ledger.** The same rebase resolved
`tasks/CLAIMS.jsonl` by leaving `<<<<<<<`/`=======`/`>>>>>>>` in the file, and
`tests/test_conflicts.py` failed on it — the T-0021 rule catching a recurrence of
F013 in a new place. Repaired by keeping both ledger lines and dropping the three
marker lines: the ledger is a sequence of events, so the union is correct and
only the order was in question. 100 entries, all parsing as JSON, no duplicate
`(task, action, ts)`.

The second one is now documented in
[`docs/process/multi-vm-coordination.md`](../../docs/process/multi-vm-coordination.md)
under *Append-only conflicts*, because the resolution rule was previously
written down nowhere and this session had to derive it.

**On `sync land`'s auto-resolution.** It regenerates the three generated indexes
and stops for everything else, which is the right default — but it means a ledger
conflict reaches a human, and this session resolved one under time pressure with
a gate to catch the mistake afterwards. That ordering is a choice worth keeping:
the gate caught it, so nothing was lost.

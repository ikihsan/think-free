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
claim-session: 2026-10-04-012-measure-the-test-suite-on-every-cpython
claim-vm: instance-20260717-0947
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

### What the measurement found, before anything was repaired

The premise was falsified by measurement rather than by a synthetic instrument,
and it was worse than the record suggested. Running the full suite on 3.9.23,
3.10.18, 3.11.13, 3.13.7 and 3.14.2 — portable CPython builds from
python-build-standalone, unpacked under `/tmp`, no installation step — failed on
**all five**, with exactly one failure and no errors each time:

```
FAIL: test_the_reported_scope_names_this_suites_size (test_doctor_versions.RealRecordTest)
AssertionError: Regex didn't match: '\\d+ tests' not found in ''
```

The failing test was written hours earlier in T-0033 and asserts that the
interpreter running it appears in `tests/python-versions.json`. So the suite was
red on precisely the versions it had never been run on. Recorded as F018 and
defect 8; `FAILURES.md` holds the write-up.

The near-miss is worth naming: a sibling test asserts the same claim from a
different source — `doctor` probes `python3` on `PATH` — and the two agreed only
because this VM's `PATH` interpreter is 3.8.10, the one recorded version
available locally. Running the suite under a downloaded interpreter is what
separated `sys.executable` from `PATH`.

### Falsification of the new gate, in four directions

`tests/test_ci_matrix.py` was written before the workflow was changed, and run
against the unmodified workflow: 8 of its 11 tests failed, naming the missing
matrix and the five unrecorded rows. After the repair, four mutations were tried
with the restored file as the control (`sessions/…-012/commands.log`):

| Mutation | Result |
|---|---|
| Guard naming `3.7`, which is not a row | fails — the five file-reading gates would never run |
| `fail-fast: true`, the default | fails — a cancelled row is not a version anything ran on |
| A row `3.15` the record has never heard of | fails on both the missing-scope and the still-unexercised clause |
| Unmutated file | green |

**One mutation was my error and is recorded because the log would show it:** the
first draft of the guard mutation rewrote `'3.12'` to `'3.13'`, which *is* a
row, so it passed. The mutation was wrong, not the gate.

**One non-detection is recorded rather than hidden:** moving every guard to a
different real row passes. Which row carries the file-reading gates is a decision
in `docs/operations/ci.md`, not a property a gate can read without duplicating
that decision.

Two of the gate's own parsers were corrected because the controls they failed
were the parsers, not the code: a step at the wrong indent was silently skipped,
and a `not_exercised` range naming no version was reported as unreadable when it
constrains nothing and is a real answer.

### Measured result

392 tests, green on 3.8.10 (this VM), on all five portable builds, and on
git 2.55.0 — the version the CI runner image ships, unpacked from conda-forge
outside the repository. Captured in `commands.log`.

`tests/python-versions.json` now carries an entry per environment — a
patch-level one for each portable build and the VM, a minor-level one per CI
row — because `versions.compare` picks the longest match and a patch-level entry
can otherwise shadow the CI entry for its own minor. `doctor` now prints the
matched entry's `where`, so `exercised` cannot be read as a claim about the
reader's own machine. `tests/git-versions.json` gained a 2.55.0 entry, a `where`
on every entry, and a `not_exercised` list (2.26–2.54, 2.57+), with test
clauses for all three.

### Ceilings

- A matrix row is evidence about that row. Nothing checks the `floor` claim
  itself; widening the range is a decision somebody has to read.
- Nothing from 3.15 upwards has run, and no gate widens that. Git 2.26–2.54 and
  2.57+ have not run either, and now say so.
- The local measurements are CPython on Linux x86_64 only, and the git 2.55.0 run
  is a conda-forge build on this VM rather than GitHub's runner: the *version*
  matches what the runner ships (`source-supported`, `actions/runner-images`
  readme) but the machine does not.
- The definitive confirmation of the matrix is the pushed CI run, read from the
  public API; the run log needs repository admin rights, so each CI entry claims
  the minor version only — and the `::error::` annotations the docs used to rely
  on are **not** returned to an unauthenticated caller, so a red run names a
  version and a step, not a test.

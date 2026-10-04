<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Tests

Standard-library `unittest` suite. No third-party runner, so it works on a
fresh VM with nothing installed.

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

Each test builds a throwaway git repository in a temporary directory, copies the
tooling into it, and points `ORIGIN_ROOT` at it. Tests therefore exercise the
same code path as the CLI, including real `git` reconciliation, and cannot
interfere with the working repository.

| File | Covers |
|---|---|
| `harness.py` | Repository fixture and in-process CLI runner |
| `test_events.py` | Event ordering, schema validation, malformed-line handling |
| `test_secrets.py` | Secret detection, redaction, artifact refusal |
| `test_session.py` | Lifecycle, reconciliation, command capture, reports |
| `test_report_freshness.py` | The generated session report equals its render after every append — capture, redaction, artifact, milestone — because a stale one is a red CI run (`STATE-defects.md`, run 37180487906) |
| `test_doc_gaps.py` | Documentation-gap implications: `any` and `all` record groups |
| `test_tasks.py` | Task creation, claim conflicts, verification, index, and the flags a writer repeats: three `--acceptance` values must reach the file as three lines, which the unmodified parser reduced to one (defect 11) |
| `test_doclint.py` | Line cap, metadata, links, orphans, stale generated files |
| `test_conflicts.py` | Unresolved merge-conflict markers: every shape git writes, the shapes that must stay silent, the declared waiver |
| `test_release.py` | `RELEASE-MANIFEST.md` enforcement: one seeded defect per clause, and a fixture that passes |
| `test_skillsync.py` | Skill naming, cross-agent mirrors, vendored integrity |
| `test_fleet.py` | Two-clone fleet: remote-truth claims, takeovers, worktrees |
| `test_sync.py` | Pull, push, land, rebase, divergence reporting; the rebase continue must stay non-interactive |
| `test_session_flow.py` | Session start and finish across two clones: stale trees, uncommitted work |
| `test_cli.py` | Exit codes, index generation, doctor, preflight, in-flight tolerance |
| `test_inflight_session.py` | In-flight versus abandoned: one falsifiable clause per rule of `inflight.classify`, plus the `--strict` and `--lease-hours` gate |
| `test_landed_work.py` | Attribution when another VM's commits land mid-session: replayed against session 029's nine false reports, with the negative controls that must keep reporting |
| `test_task_index_freshness.py` | A created task is linked by the generated indexes: `task new` then `doc lint` must pass with no manual regeneration, and a file nobody created must still be an orphan |
| `test_idalloc.py` | Identifier allocation reads the shared base: a clone whose tree is behind it, a withdrawn number, an unreachable base, and the three states the source line distinguishes |
| `test_gitversions.py` | Schema of `git-versions.json`, that the docs point at it, and the honesty clauses added after F019: every entry has a scope with a count and a machine, and the unexercised ranges are named |
| `test_identifiers.py` | The identifier rule: the two definitions of F010 as commit `e6eb992` wrote them, index rows with and without a body, task numbers, and the paraphrased rows that must stay silent |
| `test_identifier_enforcement.py` | Where that rule is read: this repository's own record, its decision index in both directions, `doc lint`, and `land`'s refusal to push a colliding tree — for both sources of definitions |
| `test_defectlist.py` | The defect list as an identifier record: the two entries both numbered 7 as `e53ca23` and `e701ad8` wrote them, a sweep over every commit that touches the file, and the four shapes that must stay silent (prose, a plain numbered list, an indented nested item, out-of-order numbering) |
| `pushcred_fixture.py` | Throwaway HOME, git config, App directory, and **cleared credential-token environment** for the push-credential tests. It clears `GH_TOKEN`/`GITHUB_TOKEN` because `pushprobe` counts an environment token as a mechanism, so inheriting the runner's token made a test asserting `unavailable` read `broken` — green on both VMs, red on any runner that exports one (CI runs `37174050724`, `37174316639`, `37174309822`). A fixture must build the machine it claims to build |
| `test_pushcred.py` | Push-credential report: helper classification, volatile dependencies, and the `configured`/`broken`/`unavailable` verdicts against real helper scripts and a real `git credential fill` |
| `test_pushcred_safety.py` | No credential value reaches the report, the summary, `doctor.json`, or stdout; a test sandbox cannot write to the real `~/.gitconfig` (`FAILURES.md` F014) |
| `test_doctor_versions.py` | `doctor`'s comparison of this VM's git and interpreter against the exercised-version records: the four states, dotted-prefix matching with the longest entry first, and a real-record class that reads this repository rather than the fixture |
| `test_pythonversions.py` | `python-versions.json`: every entry has a scope, the floor is supported by an entry that ran it, the unexercised versions are named, and CI is not credited with a patch version the public API cannot report — with the allowed set read from the workflow, so a new matrix row cannot slip past that clause |
| `test_ci_matrix.py` | The CI `python-version` matrix and the exercised-version record held to each other: every row recorded, nothing a row runs still called unexercised, `fail-fast` off, the file-reading gates guarded to one row that exists, and every shape the parsers do not understand a failure rather than a pass |
| `git-versions.json` | Machine-readable record of the git versions the suite and the sync flow are verified against (schema `origin.git-versions/1`) |
| `python-versions.json` | The same record for interpreters, with the versions nobody has run named rather than implied (schema `origin.python-versions/1`) |

Exit codes are part of the contract and are tested: `0` success, `1` usage,
`2` lint, `3` verification failed, `4` integrity.

**A test that cannot fail is worse than no test.** Every clause of the in-flight
predicate was checked by deleting the clause and re-running: each produced a
failing test. Do the same before believing a new gate is covered — F011, F013,
F014 and F015 all sat in code paths whose tests could only have passed.

**Falsifying a new gate.** A gate added for a defect is run against that
defect's own bytes before it is trusted. `test_conflicts.py` carries the three
committed regions of `fd7b4a1` as literal text with the line numbers the rule
must report, which is how its first implementation was caught reporting only
malformed blocks and missing three of four committed defects.
`test_release.py` seeds one defect per clause of `release check` into a
throwaway repository, plus a fixture that passes — because a check that only
ever fails is not a check either.
`test_landed_work.py` was written before the fix it covers and run against the
unfixed code first: 4 failures and 1 error naming session 029's mis-attributed
paths. Reverting the exclusion failed 3 of its 6 tests while the 3 negative
controls stayed green, which is the shape a falsifiable control should have.

`test_idalloc.py` was run against the unfixed allocator before the repair: the
stale-clone test reported `T-0002` where the base already defined `T-0002`, which
is the collision itself rather than a proxy for it, and a deleted task file
recycled its number. That first run also failed three tests for the wrong reason
— two were defects in the implementation under test (a configured-but-unreadable
base reported as current, and a test placed in the fleet class when it belonged
in the no-remote one), which is the useful outcome of falsifying early: the test
found its author's mistakes before the code found anyone else's.

`test_pushcred.py` does the same thing for a diagnostic rather than a gate: three
environments that must be distinguishable — a working credential, the recorded
`instance-20260717-0947` failure, and no credential at all — built from real
helper scripts and a real `git credential fill`. The pre-fix `doctor` reported
one identical line for all three, which is recorded in the session command log
rather than here. **A fixture must build its paths inside its own sandbox**:
the first version named `/tmp/github-app-jwt.sh`, which exists on one VM and not
another, so it passed for the wrong reason where it happened to exist.

**A control that cannot fail is not a control.** `test_identifiers.py` carries the
two rows `FAILURES.md` shortens on purpose, and an earlier version of the rule
compared index rows to their headings as strings — which flagged 83 of 174
commits, including the tip, for being paraphrased. The control is what found it.
It is also what caught a decision-index regex that matched no row in any commit:
a check that has never fired looks exactly like a check with nothing to report,
so the suite asserts each mechanism notices its own removal. Run against the real
history the rule reports one commit of 174 (`e6eb992`, the collision that
reached the base) and the hand repair one minute later is clean.

**The interpreter is part of it too.**
[`python-versions.json`](python-versions.json) says the same thing for Python,
and its test is stricter than `test_gitversions.py` on purpose. A schema check
passes just as happily on a record that lies, so four clauses are about honesty
rather than shape: every entry must say how much of the suite it ran, the floor
must be a minor version some entry actually ran (the claim `3.8` is supported by
3.8.10, and a record that had never run 3.8 fails), the unexercised list must not
be empty, and an entry located on CI may claim the minor version only — the run
log needs repository admin rights, so a patch version there would be a number
nobody could check. All four were falsified against the record before it was
trusted.

**A test that asserts something about a record is green only where the record
points.** Running the suite on the five interpreters the record had never heard
of (T-0034) failed on all five, on an assertion that had nothing to do with the
code (`FAILURES.md` F018). Two tests in `test_doctor_versions.py` claimed *this
interpreter* is recorded, from two different sources — `platform.python_version`
and the `python3` on `PATH` — that agreed only because this VM's `PATH`
interpreter is one of the two recorded ones. A third, one function away, claimed
*this machine's git* is recorded, and had CI's seven matrix rows red for two hours
because the runner ships git 2.55.0 and the record named 2.25.1 and 2.56.0
(F019). The repairs state the disjunction each situation supports, and
`test_ci_matrix.py` holds the CI matrix to the record so that coupling is
checked on the two artefacts instead of being discovered by running a download.

The general form, which is what both findings are instances of: **a gate that
reads its own environment is only as portable as the record of that
environment.** Assert about the artefacts, state the environment's gaps as data
— `not_exercised` in both records, each with a test that the list is non-empty —
and keep "this machine is not covered" a warning `doctor` prints rather than an
assertion the suite makes. `test_gitversions.py` grew the honesty clauses for
this after F019: every entry names a scope with a count and a machine, and the
unexercised list may not be empty.

**A test can exercise a module and miss the report a reader sees.** Falsifying
`doctor`'s version comparison, removing the single line that renders it left
every unit test of the comparison green — the tests read `versions.compare`, and
nothing asserted that `doctor.summarize` printed it. The fourth falsification
caught it, and `RealRecordTest` now renders the whole report rather than calling
the comparator. The same class of gap: the "real record" tests were originally
written against the `RepoTest` fixture, which ships neither record, so every
assertion about `exercised` was vacuous and the whole file failed for that
reason instead of the one it was written for.

**A gate wired into one reader is not read by the other.** The defect list was a
second source of definitions, and `test_defectlist.py` could have been entirely
green while `doc lint` and `sync land` went on reading only the first — which is
what happened, for real, to two VMs that each took defect 7 in an hour. Both gates
now call `idcheck.report`, and the wiring is tested where it is read: `doc lint`
fails and `land` refuses on a tree that repeats a defect number. **Two of the new
controls failed on first run**, and the failure was worth more than the fix: a
`STATE-defects.md` whose only numbered list is unbolded is both "no item here is a
definition" and "nothing could be read at all", and the second reading has to win,
because a parser that quietly stops matching is indistinguishable from a clean
tree.

**The git version is part of the suite's environment.** The land tests failed on
git 2.56 and passed on git 2.25 until `FAILURES.md` F011 was fixed, because
`git rebase --continue` opens an editor from git 2.26. The machine-readable
authority is [`git-versions.json`](git-versions.json): every version there has
carried the full suite green. This repository's VMs disagree
(`EXPERIMENTS/000-capabilities/` recorded 2.55.0, one VM has 2.25.1), so run
the suite against the git your fleet actually uses — and when a new version
goes green, record it in `git-versions.json` rather than in prose alone.

**A generated file is a function of its inputs, and every append is an input.**
The session report is rendered from the event stream, so appending an event
invalidates it — and `doc lint` fails on a generated file that differs from its
generator's output. Only `session start` and `finish` regenerated it, so a commit
made after a `tools/x` capture and before the next write published a stale report:
run 37180487906, seven green `Tests` jobs and a red `Documentation lint`. The two
earlier repairs of this family (T-0026, T-0027) made the *task* commands rebuild
the *task* and *docs* indexes and so did not reach it, because the appender here
is not a task command. The fix is in the appenders, and
`test_report_freshness.py` calls the **module** API rather than the CLI precisely
because the first attempt put the repair in the CLI, where a module caller could
still break it. Two rules earned here: find the appender rather than the command
that happened to be running when someone noticed, and put a generated-file
invariant below the layer that changes the input.

## Running a subset

The full suite takes about four minutes on two cores, the fleet harness and the
doc-lint suites being the slow parts. One file is much faster and is the right way
to iterate:

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_report_freshness -v
```


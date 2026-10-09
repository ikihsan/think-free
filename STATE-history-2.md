<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Session history behind the verified state (part 2)

Older session detail moved from `STATE-history.md` on 2026-10-06 to keep the
main history file under the 300-line cap.

# Session history, part 2

Older per-session detail behind [`STATE.md`](STATE.md), and the thematic
sections that came off [`STATE-history.md`](STATE-history.md). `STATE.md` is the
reload point; `STATE-history.md` holds the newest sessions; this file holds
what is behind them. Identifiers are the same ones `STATE.md` uses.

**Split on 2026-10-09** when E069's record pushed `STATE-history.md` past 300
lines and its oldest sections moved here. Nothing was edited in the move.

| Sibling | Holds |
|---|---|
| [`STATE-history.md`](STATE-history.md) | the newest sessions, and the invariant behind these splits |
| [`STATE-history-3.md`](STATE-history-3.md) | the sessions that moved out of this file in the 2026-10-09 split |

## What changed in sessions 001-003, VM 0947 (T-0025, T-0026, T-0027)

Moved out of `STATE.md` on 2026-10-04, where three per-session bullets had
drifted into the *Honest limitations* section and two of them had run together on
one line. They are session detail, which is what this file is for.

- **Session 003 (T-0027).** T-0026's verification passed while its defect was
  still live: a lint on the author's own tree cannot see what a claim commit
  published, and the claim staged only the task file and the ledger. Four more
  red runs followed; `task claim` now stages the rebuilt indexes, and the new
  test lints a *fetched* tree on a second clone. **Lesson worth more than the
  fix:** a gate that reads the tree the author is standing in cannot see the
  commit the author is about to publish.
- **Session 002 (T-0026).** `task new` now rebuilds the generated indexes,
  because two CI runs failed on 2026-10-03 for exactly that: a task file was
  pushed before `tasks/INDEX.md` was rebuilt and the orphan rule rejected the
  file the VM had just created. The rule is unchanged - a file no command wrote
  is still an orphan, which the new tests assert. **The task file for this work
  guessed the wrong index:** the stale one was `docs/INDEX.md`, which lists task
  files by path. 274 tests green.
- **Session 001 (T-0025).** The pushed CI run for T-0024 is read and recorded:
  all six steps green on `9e865a4`, including the session-integrity step that
  had been red on every push while a VM was working. The two failures from ten
  minutes earlier were **not** the date defect this session's predecessor
  assumed: their failing step was Documentation lint, and the cause was a task
  file pushed without regenerating `tasks/INDEX.md`. **Reading the run rather
  than the expectation is what caught it.**

## What changed in session 012, VM 0947 (T-0034)

The exercised-Python record named 3.9 to 3.11 as versions nobody had run, and its
own `why` clause gave the reason: *"CI pins a single version"*. The 3.8-or-newer
floor was two points with a gap between them. So the gap was measured instead of
described — portable CPython builds (python-build-standalone, unpacked outside the
repository, no installation step) for 3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2,
each running the full suite.

**The gap was not hypothetical, and it was not a version incompatibility.** All
five runs failed, with exactly one failure each and no errors, on
`RealRecordTest.test_the_reported_scope_names_this_suites_size` — a test written
hours earlier in T-0033 that asserts *this* interpreter appears in
`tests/python-versions.json`. 3.14.2, an interpreter newer than anything this
repository has ever named, failed exactly as 3.9.23 did. `FAILURES.md` F018,
defect 8 in [`STATE-defects.md`](STATE-defects.md).

- **The half that was nearly missed.** A sibling test asserts the same
  "this interpreter is recorded" claim from a different source: `doctor` probes
  `python3` on `PATH`. One question, two sources, agreeing only because this VM's
  `PATH` interpreter is 3.8.10 — the one recorded version available locally.
- **Why adding the matrix without the repair would have been worse than not
  adding it.** Five of seven rows red for a reason about the record invites two
  responses, weaken the assertion or drop the rows, and both reduce measurement.
- **The second machine-fact gate, one function away, and this one was invisible
  from outside.** T-0033 had also added an assertion that *this machine's* git is
  in `tests/git-versions.json`. The matrix's seven rows were all red at the
  `Tests` step, including rows whose interpreter had just been measured green on a
  VM; the run log needs admin rights and the public check-runs API returned
  `annotation_count: None` for every failing check, so the annotation route
  `docs/operations/ci.md` relies on does not work unauthenticated. Found by
  elimination (every row's minor version was green locally, so not the
  interpreter) and then by reading the runner image's own readme, which lists
  **Git 2.55.0** — a version the git record did not name. A conda-forge 2.55.0
  was unpacked outside the repository and reproduced the failure exactly.
  `FAILURES.md` F019, defect 9.
- **What was actually repaired.** Not the missing entry — the assertion. It is
  now the module's contract (four states reachable, an `exercised` verdict
  carrying its entry's scope and machine), with a control that emptying the
  record moves every version off `exercised`. Adding the 2.55.0 entry alone would
  have made CI green and left the assumption in place. The git record gained a
  2.55.0 entry, a `where` on every entry, and a `not_exercised` list — 2.26–2.54
  and 2.57+ — with test clauses, so the gap is named rather than inferred from
  two points.
- **`docs/operations/ci.md` no longer claims the annotation route works.** It
  says what is readable without rights — step conclusions and check names, which
  with a matrix is enough to localise a failure to a version — and names the fix
  that would make it enough to localise it to a test: one check per test file.
- **The other VM found the same assertion from the other end, an hour later.**
  Its CI run was red on the same test for the mirror-image reason: on a CI row the
  matched entry is `3.12`, whose scope names a run id rather than a test count.
  Its fix asserted the reported scope is the matched entry's own text unchanged —
  a different property from the one it replaced. The rebase resolved the conflict
  by keeping both clauses, because neither catches the other's failure, and the
  record's `3.12` CI entry was given a count as well as its run id.
- **Repair.** The test states the disjunction it can support: every entry's
  `scope` names a test count, the comparison returns that entry's text
  unaltered, and this interpreter either matches an entry or is reported
  `unrecorded` with its version named. The coupling is enforced on the two
  artefacts instead: `tests/test_ci_matrix.py` holds the workflow's row list and
  the record to each other in both directions, and
  `test_pythonversions.py`'s "minor version only" clause now reads its allowed
  set from the workflow so a new row cannot slip past it.
- **Falsified in four directions** — a row with no recorded scope, a guard naming
  a version that is not a row, `fail-fast` returned to its default, and the
  unmodified workflow — with the restored file green as the control. One
  non-detection is recorded rather than hidden: moving every guard to a
  *different real row* passes, because which row carries the file-reading gates is
  a decision in `docs/operations/ci.md`, not a property a gate can read without
  duplicating it. Two of the parsers were corrected first because the controls
  they failed were the parsers, not the code.
- **`doctor` now names the machine.** One record covers two environments per
  minor version — a portable build on a VM and a CI row — so a patch-level entry
  can shadow the minor-level one, and `exercised` alone would describe a runner
  the reader has never seen. The matched entry's own `where` travels with the
  verdict.
- **Session 012 closed with two reconciliation reports, and neither could be
  logged.** `session finish` recorded 24 `unlogged_change` events and one
  `documentation_gaps` entry. The events split in two: this session's own
  documentation edits, which were recorded as `doc_update` but never declared as
  artifacts, and the other VM's T-0035 files, which arrived through **two
  hand-run `git rebase --continue`** calls. D028 attributes a path only from a
  base move the tooling performed, and a hand-run continuation is not one — the
  same ceiling session 040 hit through seven hand-run rebases, now the second
  time it has been reached. The gap entry is the more interesting half: this
  session logged an `experiment_result` for work that was not an experiment on a
  candidate, and the tooling obliged by requiring `HYPOTHESES.md` to change. That
  is the rule working — it will not let a result-shaped event go unrecorded — but
  it has no way to tell a fleet measurement from a candidate experiment, so the
  file now says so in one paragraph. **A closed event stream accepts neither
  report**, which is the point of closing it: the honest remedy is a later
  session that records what the reconciliation said, not an edit to history.
  Session 014 did that.
- 392 tests green on 3.8.10, on all five portable builds, and on git 2.55.0 —
  the runner's own git. D035 in
  [`DECISIONS-GATING.md`](DECISIONS-GATING.md).

## What changed in session 005, VM 0947 (T-0030)

A collision between two VMs is created by the *merge*: each branch is internally
consistent, and each VM's own `doc lint` sees nothing wrong with its own tree. So
that is where the property is now read. `tools/originlib/identifiers.py` reports an
identifier defined twice, an index row with no definition behind it, a defined
finding with no row, and a decision its own index row does not list.
`sync land` refuses to publish a tree the rule would refuse; doc lint rule 7 is
the backstop for any other route. D032 in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).

**Falsified in both directions.** Run over all 174 commits on the shared base the
rule reports **one** — `e6eb992`, which carries two different findings both headed
`## F010` to the base — and the hand repair one minute later is clean. Removing
each of the three mechanisms in turn makes the covering test fail while the
controls stay green; both runs are in this session's `commands.log`.

**The control earned its place.** A draft that compared an index row to its heading
as strings flagged 83 of 174 commits including the tip, because two rows in
`FAILURES.md` are shortened paraphrases on purpose. A second half, fixed next,
allowed no Markdown link in its filename pattern and so matched no row in any
commit — a sweep that passed while the rule did nothing. The rule also found a
real desync on its first run: **D030 was missing from its row in `DECISIONS.md`.**

## What changed in session 040, VM 0944 (T-0029)

`doctor` reported a property it never read, and the check that repaired it found a
live defect on the VM that wrote it. Contract in
[`docs/operations/doctor.md`](docs/operations/doctor.md); the rule is D027.

- **`doctor` could not see the credential this fleet uses.** It read four
  environment variables and printed `credentials     none present` — on a machine
  whose pushes are made by a GitHub App key reached through git's
  `credential.helper`, on one whose helper pointed at a file `/tmp` had taken, and
  one with no credential at all. One line, three realities: D025's failure mode
  in a diagnostic rather than a gate.
- **The falsification ran before the fix, as D025 requires.** Three environments
  built from real helper scripts, each with its own `HOME`: a working credential,
  the recorded `instance-20260717-0947` failure, and no credential. `git
  credential fill` told them apart (exit 0 vs 128, two distinct git complaints);
  `doctor` produced **one** distinct report for all three. Both runs are in the
  session command log, as is the rejected `git ls-remote` probe, which cannot fail
  because this remote is public.
- **The verdict is three-valued and the difference is load-bearing.** The first
  implementation reported a fresh VM with no credential as `broken`, the same
  verdict as the machine that lost a day of pushes; the harness caught it.
- **A live defect, on this VM.** `~/.config/github-app/git-credential-helper.sh`
  was intact, mode `0700`, and working — and invoked `/tmp/github-app-jwt.sh`,
  one `/tmp` clear from failing. Repaired: the generator moved to
  `~/.config/github-app/jwt.sh`, the helper was repointed, and
  `/tmp/github-app-jwt.sh` was then **deleted**. `git credential fill` still exits
  0 and the warning is gone, so the dependency disappeared because the helper
  changed and not because the check stopped looking.
- **`F014`: this session's own harness overwrote this VM's `~/.gitconfig`,**
  destroying the git identity and `credential.helper` that 125 commits are
  authored with, because two of its three sandboxes were `Path.home()`. Repaired
  and verified in the same session; the harness now refuses any HOME outside its
  own directory.

## What changed in session 039, VM 0944 (T-0023)
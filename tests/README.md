<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
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
| `test_link_escape.py` | That a link's verdict is a function of the repository and not of the checkout's neighbours: one probe document at two checkout locations, where the old rule reported `broken link` in one and nothing in the other (defect 19). The previous rule is written out as a witness, the escape is published as a check-run annotation with its file and line, and `NoRegressionTest` counts the 577 tracked links it read so "none leaves the repository" cannot pass by reading almost nothing |
| `test_table_rows.py` | That a hand-authored document says each thing once, against `eff1126`'s own bytes: `STATE.md` carried a byte-identical second copy of its `Implemented (2)` dashboard row, one per VM, and every gate passed (defect 20). The committed-defect tests read both lines out of git and assert they are byte-identical; a generated report repeating an artifact row is silent, as is a code fence, a separator line, and the same row in two different tables. Falsified by removing the rule *and* by removing only the generated-document exemption, which reports 47 findings on a clean tree |
| `test_conflicts.py` | Unresolved merge-conflict markers: every shape git writes, the shapes that must stay silent, the declared waiver |
| `test_release.py` | `RELEASE-MANIFEST.md` enforcement: one seeded defect per clause, and a fixture that passes |
| `test_skillsync.py` | Skill naming, cross-agent mirrors, vendored integrity |
| `test_fleet.py` | Two-clone fleet: remote-truth claims, takeovers, worktrees |
| `test_sync.py` | Status, pull and push: divergence reporting, fast-forward, the refusals on a dirty tree and on local commits that would be lost, and that a push never forces |
| `test_land.py` | `sync land`, split out at the line cap by operation: publishes the branch, regenerates a *conflicted* generated file, rebuilds one that merged **cleanly** and was therefore stale (defect 13), never lets `rebase --continue` open an editor, and stops for a human on a real conflict with the work intact |
| `test_session_flow.py` | Session start and finish across two clones: stale trees, uncommitted work |
| `test_cli.py` | Exit codes, index generation, doctor, preflight, in-flight tolerance |
| `test_preflight_gates.py` | That `preflight` runs every gate a change here can break, not three of four: an unclassified root document must make it fail, a classified one must leave it silent, and the gate's line must be printed before the verdict it decides |
| `test_inflight_session.py` | In-flight versus abandoned: one falsifiable clause per rule of `inflight.classify`, plus the `--strict` and `--lease-hours` gate, and **the two clocks the fixture can date a claim from** — a fixed `NOW` for the tests that pass `now=` and the real one for the three that drive the CLI, because dating the CLI's claim from `NOW` made one assertion expire 24 hours later and never pass again (defect 15) |
| `test_landed_work.py` | Attribution when another VM's commits land mid-session: replayed against session 029's nine false reports, with the negative controls that must keep reporting |
| `test_task_index_freshness.py` | A created task is linked by the generated indexes: `task new` then `doc lint` must pass with no manual regeneration, and a file nobody created must still be an orphan |
| `test_idalloc.py` | Identifier allocation reads the shared base: a clone whose tree is behind it, a withdrawn number, an unreachable base, and the three states the source line distinguishes |
| `test_gitversions.py` | Schema of `git-versions.json`, that the docs point at it, and the honesty clauses added after F019: every entry has a scope with a count and a machine, and the unexercised ranges are named |
| `test_identifiers.py` | The identifier rule: the two definitions of F010 as commit `e6eb992` wrote them, index rows with and without a body, task numbers, and the paraphrased rows that must stay silent |
| `test_identifier_enforcement.py` | Where that rule is read: this repository's own record, its decision index in both directions, `doc lint`, and `land`'s refusal to push a colliding tree — for both sources of definitions |
| `test_task_rewrite.py` | Whose change is a task file `task complete` just rewrote: the command's own write is declared with the **bytes** it wrote, so an agent's later edit to the same file — body or meta block — is reported again, and a file changed with no command run at all is still reported. Falsified by mutation in both directions. Counts name the ledger too, since T-0050 gave `tasks/CLAIMS.jsonl` the same treatment and a task command writes both files (defect 12) |
| `test_task_rewrite_recorded.py` | The same defect on the bytes the fleet published: session 2026-10-04-019 declared seven artifacts and closed `worked` with `unlogged_changes: 1` naming its own task file, and its stream declares no `task_rewrite` at all — for the task file or for the ledger — so the rule reads it as declaring nothing rather than as silent by default. Split from `test_task_rewrite.py` at the line cap; also that a whole-file digest cannot stand in for a task file's two-part one (defect 12) |
| `test_unlogged_data.py` | A file's extension must not decide whether a session declared it: a `.json`, `.jsonl` and `.log` changed without declaring is reported, all three because a rule that fixed only `.json` would leave the ledger and the session streams. The controls that must still hold — a declared data file, a generated file, a declared exempt glob, and the cap's own exemption of a 400-line JSON — plus the ledger's declaration by its bytes and the four experiment captures session `2026-10-04-030` changed and never declared (defect 12's stated false negative, F022) |
| `test_defectlist.py` | The defect list as an identifier record: the two entries both numbered 7 as `e53ca23` and `e701ad8` wrote them, a sweep over every commit that touches the file, and the four shapes that must stay silent (prose, a plain numbered list, an indented nested item, out-of-order numbering) |
| `test_decision_header.py` | The third source of a decision identifier: a record's own `Decisions **…**` header, held to the decisions that file defines in both directions. Falsified against `d451169`'s own bytes, which carried two false headers while every gate passed, and silent on the repair (defect 14) |
| `test_decision_files.py` | The two hand-maintained lists of decision records — `paths.MISSION_RECORDS` and `reconcile.IMPLICATIONS` — held to the files on disk, because the log was split five times and each split added a file to both by hand |
| `test_land_hand_completed_rebase.py` | `landrebase.recover`: a rebase a reader *finished with raw git* is read back from `ORIG_HEAD` and the reflog's `rebase …: checkout` entry, recorded once, excluded from `changed since start` at finish, and refused for a merge, a fast-forward, or an arrival already recorded |
| `test_land_resume.py` | `sync land` finishing a rebase **it** stopped on, once the conflict is resolved: the tool's own instruction has to be followable by the tool that gave it, or the only way out is `git rebase --continue` by hand and every path the base brought is attributed to the session that resolved the conflict (defect 2's ceiling, reached through a refusal message). Both halves falsified against the unmodified code — without the resume nothing lands at all and the unresolved case degrades to the wrong message; without reading git's own `orig-head` the arrival is empty, because mid-rebase `HEAD` has already moved onto the base. Plus the still-unresolved refusal, the unstaged-work refusal, and a sentinel editor proving the continuation is non-interactive |
| `test_claim_in_session.py` | A claim published from inside the session that made it, and the control that keeps the repair from becoming a blank cheque: with a session open the dirty tree is the session's own record and the claim still reaches the remote, while uncommitted work that is *not* that record is refused by name, before anything is written, leaving no line in `tasks/CLAIMS.jsonl` and no commit ahead of the base (defect 21). The failure it replaces was silent about the part that mattered — the claim commit stayed local, so no other VM could see it |
| `pushcred_fixture.py` | Throwaway HOME, git config, App directory, and **cleared credential-token environment** for the push-credential tests. It clears `GH_TOKEN`/`GITHUB_TOKEN` because `pushprobe` counts an environment token as a mechanism, so inheriting the runner's token made a test asserting `unavailable` read `broken` — green on both VMs, red on any runner that exports one (CI runs `37174050724`, `37174316639`, `37174309822`). A fixture must build the machine it claims to build |
| `test_pushcred.py` | Push-credential report: helper classification, volatile dependencies, and the `configured`/`broken`/`unavailable` verdicts against real helper scripts and a real `git credential fill` |
| `test_pushcred_safety.py` | No credential value reaches the report, the summary, `doctor.json`, or stdout; a test sandbox cannot write to the real `~/.gitconfig` (`FAILURES.md` F014) |
| `test_doctor_versions.py` | `doctor`'s comparison of this VM's git and interpreter against the exercised-version records: the four states, dotted-prefix matching with the longest entry first, and a real-record class that reads this repository rather than the fixture |
| `test_pythonversions.py` | `python-versions.json`: every entry has a scope, the floor is supported by an entry that ran it, the unexercised versions are named, and CI is not credited with a patch version the public API cannot report — with the allowed set read from the workflow, so a new matrix row cannot slip past that clause |
| `test_ci_matrix.py` | The CI `python-version` matrix and the exercised-version record held to each other: every row recorded, nothing a row runs still called unexercised, `fail-fast` off, the file-reading gates guarded to one row that exists, and every shape the parsers do not understand a failure rather than a pass |
| `test_annotate.py` | A violation becomes one workflow command naming the file: the structured path wins over the message, a directory or absent path and a line past the end of a file are dropped rather than guessed, `%` is `%25`, a newline cannot inject a second command, the cap is announced, a clean tree emits nothing, and the wrapper keeps each gate's own exit code and refuses a gate or flag it cannot read |
| `test_ci_annotations.py` | The two things the annotator exists for: `e53ca23`'s real bytes produce an annotation naming `STATE-defects.md` where the previous wiring produced none and this tip produces none, and every gate step in the workflow runs through it |
| `test_probe.py` | The rendering probe: one annotation per shape, each with the file, line, level and message its table declares; the shape list held literally, so a shape cannot be dropped from the code, this file and the operations document together; the paths and lines it names are real files, or the probe would measure `finding.location`'s drop rather than the rendering; a newline cannot inject a second command; and it never emits `::error`, the control that keeps a measurement from being able to redden a run (defect 18) |
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

`test_ci_annotations.py` is the same discipline against a real commit rather than a
fixture: `e53ca23`'s `STATE-defects.md` is read out of git with `git show`, and both
directions are asserted — that tree yields an annotation naming the file, and this tip
yields none. The first run of the mechanism also failed its own kill gate, because
`check_identifiers` wrapped the collision's location away when it added its prefix; the
gate is what caught it, and the fix is in the code the gate reads.

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

**A test that reads a clock is a gate on the calendar, and it fails on a
schedule rather than intermittently.** Three tests in `test_inflight_session.py`
drive `origin session verify`, which reaches `inflight.classify`'s `now=None`
default and reads `datetime.now(timezone.utc)`. They aged the ledger entry to
`NOW − 13h` against the fixture's fixed `NOW = 2026-10-03T22:00Z`, so the
assertion that a 13-hour claim is in flight under a 24-hour lease held for exactly
24 hours from that instant and then failed forever, growing. Run `37190842104`
showed it, `observed` 2026-10-04 at 09:00Z. It is F018 and F019 with the
environment being **time** rather than a tool version: the general rule is that a
test's correctness depends on every clock the code under it reads, and the fixture
has to hand over the one the code uses. Two methods rather than a flag on one,
because the clocks differ by however long ago the suite was written, and the fix
added the negative control the expired assertion lacked — a claim older than the
*widest* lease is still abandoned, so a longer lease moves the threshold rather
than removing it.

**A gate belongs in the one command the protocol tells you to run.** T-0042 added
`DECISIONS-RECORDS.md` at the top level, declared nothing about it in
`RELEASE-MANIFEST.md`, and its own `verify` passed — the command ran the suite,
`doc lint` and `preflight`, and `preflight` was lint, skills and sessions. Run
`37191658964` is red with the violation named, and the fix was not "remember to
run `release check`": `release check` now runs from `preflight`, so a change that
adds a document, a session, a skill or an identifier cannot pass verification
without meeting the gate that reads it. `test_preflight_gates.py` falsifies it in
the direction that matters — with `release check` out, `preflight`'s output has no
`release check:` line at all, so the test cannot pass for the wrong reason. The
same statement as the generated-file rule, about a different layer: put the
invariant below the thing that changes its input.

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

**Three sources, three modules, one entry point — and the split by record was not
a size decision.** `identifiers` keeps what a definition is and whether one number
means two things; `findingindex` holds `FAILURES.md`'s table to the findings;
`decisionindex` holds `DECISIONS.md`'s rows to the decisions; `decisionheader`
holds each record's own header to what it defines; `defectlist` reads the numbered
defect list. T-0043 split `identifiers` after T-0042 and T-0040 each added to it
from a different VM — each under the cap alone, the merge at 307 of 300, and run
`37189825232` red on all seven rows. The line drawn was one module per **record**,
because two records with the same shape and different tables are two rules, and
one file holding both grows by half each time a check is added to either. The
refactor's own falsification was an equivalence, not a mutation: the report on a
fixture tree carrying 28 findings is byte-identical before and after the move,
which is the only claim a relocation can honestly make.

**A third source was the same story again, and it was found by reading the record
rather than by a red run.** T-0036 added the defect list to the entry point and
said so; T-0042 found that a decision number is written in three places that must
agree — the `## Dnnn` heading, the index row in `DECISIONS.md`, and the
`Decisions **…**` header under each file's title — and that the third had no
reader at all. Two of the five records were false: `DECISIONS-GATING.md` named D013,
which lives in another file, and omitted three of its own entries, and
`DECISIONS-PRACTICE.md` named a `D011–D018` range covering three entries that had
moved out when T-0030's split was reversed. Both were correct in `DECISIONS.md`,
which is what a reader checking one source concludes. `test_decision_header.py`
reads the two files out of `d451169` on every run, so the rule is falsified
against the defect's own bytes rather than a fixture written after it, and its
second direction matters as much: it asserts the repaired record is silent, which
is the half a rule can fail without anyone noticing.

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

**A mutation that cannot be applied cannot falsify anything, and it looks
exactly like a control that held.** Removing the clause that honours a
`task_rewrite` event should fail `test_task_rewrite.py` — the defect's own shape.
The first attempt at that mutation left all 14 tests green, because the patch
script's `str.replace` pattern did not match the file's real indentation: nothing
was mutated, and the green run was read as "the clause is not load-bearing". The
same pattern removed only the digest bound *did* fail 3, so the two mutations were
distinguishable only because one of them was applied twice by hand. **Assert that
the patch landed before trusting the run**, and treat a mutation that needed no
repair as the suspicious result rather than the reassuring one. **It happened again
in the same file's subject on 2026-10-04 (T-0050):** the first mutation of
`reconcile`'s exemption clause left all 16 tests of `test_unlogged_data.py` green
for exactly the same reason, and the second attempt failed 10.

**A borrowed predicate carries its own question, so a repair can be green and
still wrong.** The defect here was one line: `reconcile` asked `doclint.is_exempt`,
the *cap's* question, and read "yes" as "exempt from the undeclared-change report".
The fix is to ask the question actually meant, which means the two questions have
to be named separately in the first place. Price that class of change **before**
making it — `tools/sweep_unlogged_data.py` answers "how many reports would appear"
from git and the committed streams, and the answer (72 pairs over 17 paths) is what
told this repair its residual had to be written down rather than discovered.

## Running a subset

The full suite takes about four minutes on two cores, the fleet harness and the
doc-lint suites being the slow parts. One file is much faster and is the right way
to iterate:

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_report_freshness -v
```


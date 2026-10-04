<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Known defects

Every defect this repository's own tooling and records have shown, whether or not
it is fixed. Split out of [`STATE.md`](STATE.md) on 2026-10-04 when that file reached
293 of the 300 permitted lines. **The rule:** a defect is *solved* only when a gate
fails on its own bytes and passes on the repair; a repair not falsified against its
defect is open. The method is in
[`docs/policy/gate-falsification.md`](docs/policy/gate-falsification.md) and the
mechanism in [`tests/README.md`](tests/README.md), beside the tests.

1. **An in-flight session reddened every other VM's CI** (solved in T-0020). Two
   correct rules met — `task claim` needs HEAD on the remote base, so a claiming VM
   must publish its `session_start` first, and D013 then failed every push — and the
   live record corrected its own predicate once already: clause 1 required the session
   to name a task, the other VM started one without `--task`, and the gate called a
   working session abandoned. `inflight.py` now separates in flight from abandoned
   from the tree alone (D027; F014, F015), counting a claim in the ledger.

2. **Reconciliation compared trees, not authorship** (solved in T-0024, D028). A VM
   that landed another VM's work inherited its `unlogged_change` and
   `documentation_gaps` reports — session 029 emitted nine of the first, none of
   them its own. `sync pull`/`sync land` now record a `base_advance` naming the
   commits that arrived, and reconciliation attributes a path by the newest thing
   that touched it. **Ceiling:** attribution knows only about base moves the
   tooling performed, so a rebase run by hand still reports — reached by sessions
   012 and 040, both through hand-run `git rebase --continue`. That is the intended
   direction of failure, and why a session has to record such a gap where a *closed*
   stream cannot accept it: `session finish` will not take the events, and editing
   the stream afterwards would be worse.

3. **Every generated file stamped `last-verified` with the render date** (solved
   in T-0024, D029), so `doc lint` failed on 42 committed session reports and all
   three indexes on 2026-10-04 — the day after they were written. Each generator now
   stamps from the content it renders. The CI consequence is `inferred` from that local
   reproduction: no pushed run has failed this way, the two red runs at 23:58 on
   2026-10-03 having a different and verified cause (defect 5).

4. **A pushed task file without `doc index` reddens CI** (solved in T-0026 and
   T-0027). Runs `37163434868` and `37163438950` failed on Documentation lint: this VM
   created a task, committed it and pushed it without rebuilding the generated indexes,
   so the orphan rule rejected the file the VM had just created. `task new`, `claim`,
   `complete` and `release` now rebuild both indexes, and a *published claim* also
   stages them, because that commit is the first thing every other VM reads (four more
   red runs, `37165502352`–`37165807196`, were the same defect one step later). **The
   rule is unchanged** — a file no command wrote is still an orphan, which the new
   tests assert — because the omission was the defect, not the strictness. **Residual:**
   the create commit is the agent's own, so `task new` prints the command that stages
   the indexes; nothing can enforce that step.

5. **`doctor` did not compare this VM's interpreter or git against what the suite
   has been exercised on** (solved in T-0033). Both records existed and were
   schema-checked — `tests/git-versions.json` and `tests/python-versions.json` — and
   nothing read either at run time, so a VM on Python 3.9 was indistinguishable in the
   report from one on 3.8.10. `tools/originlib/versions.py` now reports `exercised` with
   the entry's own `scope`, `NOT exercised`, `record unreadable`, and `no record`, and
   **the third is the load-bearing one**: a comparison that cannot tell "we looked and
   it is not there" from "we could not look" reports a confident answer in both.
   Falsified four ways, and its first implementation matched record entries in file
   order, so a VM on 3.12.15 got CI's `3.12` scope; the longest entry wins and a test
   says so. **Ceiling:** `exercised` means a run happened, not that the version is
   supported. Contract: [`docs/operations/doctor.md`](docs/operations/doctor.md).

7. **A test fixture inherited the runner's environment** (solved in T-0035).
   `tests/pushcred_fixture.py` built a sandbox with a fresh `HOME`, git config
   and `GIT_CONFIG_SYSTEM=/dev/null`, and left `GH_TOKEN`/`GITHUB_TOKEN` alone;
   `pushprobe` counts an environment token as a credential mechanism — correctly,
   it is one — so a test asserted `unavailable` on a machine that had one. Three
   CI runs failed while both VMs were green on the same commits. **A defect that
   only reproduces where the author does not work.** Its third falsification was
   found *by* falsifying: a fixture that clears the tokens but never restores
   them leaves every test green, because unittest shares one process.
   **Ceiling:** the fixture builds the machine its own tests need.

10. **The identifier rule did not read the defect list, so two VMs took defect 7
    in the same hour** (solved in T-0036). Rule 7 read findings definitions,
    findings index rows, decision spans and task file names. `STATE-defects.md` is
    an ordered list of bold headings with no `F`, `D` or `T` identifier in it, so it
    was the one document here whose identifiers were checked by reading them — and
    reading them found T-0034's and T-0035's **defect 7** side by side. Both copies
    reached the shared base (`e53ca23`, `e701ad8`), each VM's own tree internally
    consistent; the unpushed side renumbered in `157e463`, which is the standing rule
    and the cheapest available repair.
    **Repair:** `tools/originlib/defectlist.py` reads a bold-subject list item as a
    definition of its number and reports one defined twice, reached through
    `idcheck.py` — the single entry point both publishing gates call, because a module
    added to `doc lint` is not thereby read by `sync land`, which is the operation that
    creates the collision. Falsified against the defect's own bytes: the previous
    wiring reports **nothing** on either commit and the new rule names defect 7 with
    both lines, and reports nothing on the repair or the tip either.
    **Second obligation, and it came from the first control failing:** a rule that
    cannot read its input must say so, because a parser that quietly stops matching
    looks exactly like a clean tree — D025's shape from a new direction.
    **Ceiling:** a gap in the numbering is not reported, since a dropped entry and a
    withdrawn defect produce the same bytes; nothing is checked about what a reference
    points at; and there is no allocator here, so this is the detection half of a race
    it cannot prevent. The full account is in [`tests/README.md`](tests/README.md).

## Open

Numbering is continuous and never reused, so a solved defect keeps its number and this
section is not in numeric order: an entry lands under whichever heading fits it when it
is closed.

11. **`task new` silently keeps one `--acceptance` line and drops the rest** (solved
    in T-0039). Five criteria were passed on the command line and the task file
    recorded one, with no warning: `--acceptance` and `--steps` were declared with
    `default=""` and no `action="append"`, so argparse kept the last occurrence.
    **The cost is a task that reads as complete against a truncated definition of
    complete** — F010's near-vacuous gate: the field is filled in, and nobody can tell
    that most of it is missing. Found by using the documented workflow, which is the
    only way this class of defect shows up.
    **Repair:** both flags accumulate, one line per occurrence, joined in
    `cli_task.py` so `taskops.create` keeps taking a string. Falsified first: three
    flags wrote one line, and three `--steps` wrote only `3. third`. A fourth control
    came from the same run — `taskops.create` defaults `acceptance` to a bare
    `- [ ] `, which the CLI made unreachable; the test now pins the empty section,
    because a checkbox nobody wrote is worse than an empty heading.
    **Ceiling:** only the two flags a writer repeats are changed. Every other `--`
    flag in `cli_args.py` is still last-wins, and the general rule — *a flag that
    collects more than one thing must say so* — is not enforced anywhere.

12. **A task file is changed by the commands that manage it and declared by
    neither** (solved in T-0047, D040; its false negative in T-0050, D042). `task
    claim`, `task complete` and `task release` rewrite the task file, and
    reconciliation reports any changed-but-undeclared path as an `unlogged_change`, so
    each of them closed its session with exit 4 on the tooling's own write. **The
    count was an undercount twice over:** the entry said "three such events in two
    sessions" because it had been read from two sessions, and a sweep of every closed
    session's stream finds **37 reports naming a task file across 21 sessions**
    (`observed` 2026-10-04). Session `2026-10-04-019` is the clean instance — seven
    declared artifacts, `unlogged_changes: 1` naming `tasks/T-0039-*.md`; that stream
    is now in the suite rather than in a session log.
    **Repair:** `_set_meta`, the only function that writes the meta block, appends a
    `task_rewrite` event carrying the path, the task, the status and **two digests** —
    the meta block and everything outside it — and reconciliation honours it only
    while both still match. So the command's write is not reported and the agent's
    next edit to the same file is. The appender, not the four commands that call it:
    a rule attached to the command that happened to run is a rule the next one
    misses. `session finish` names what it excluded, for D028's reason.
    **The trade-off the entry above refused is answered, not assumed away:** a
    declaration naming the *file* would silence every later edit to it, so the
    declaration names the *bytes*. Falsified both ways — removing the clause in
    `reconcile` fails 4 of 14 new tests, removing only the digest bound fails 3 —
    and the first attempt at the first mutation **passed all 14**, because the patch
    pattern did not match.
    **The false negative this entry never measured is closed (T-0050, D042, F022).**
    `reconcile` asked `doclint.is_exempt` — the *cap's* question, true for every
    `.json`, `.jsonl` and `.log` — so a data-file edit was excluded from `unlogged`
    and `tests/python-versions.json` could change with nothing said. Reconciliation
    asks the declared question only now, and the ledger and `vendor/hashes.json` are
    declared by the bytes their writers wrote. Priced **before** the change by
    `tools/sweep_unlogged_data.py`: 72 (session, path) pairs over 17 paths across 77
    closed sessions, 50 the ledger — so 50 closed sessions now report a file they
    cannot declare, and F022 records that rather than leaving it a surprise.
    **Ceiling:** a command run with no session open records nothing.

15. **The lease tests dated a claim from a fixed date while the gate read the
    real clock, so one expired on a schedule and can never pass again** (solved in
    T-0044). `tests/test_inflight_session.py` fixes `NOW = 2026-10-03T22:00Z` and
    `inflight.classify` takes `now=` so the classification tests can be dated
    against it — correct, because they pass the clock in. Three tests in
    `VerifyGateTest` drive the CLI instead, which cannot: `session verify` reaches
    `classify`'s `now=None` default and reads `datetime.now(timezone.utc)`. Those
    three aged the ledger entry to `NOW − 13h`, so the claim's age under the real
    clock grew by an hour every hour, and `test_the_lease_is_a_flag_not_a_constant`
    began failing at **2026-10-04T09:00Z exactly** — 24 hours after the fixed
    instant — with `AssertionError: 4 != 0`. Run `37190842104` at `f566ff0` is red
    on it and its annotations name the test and the line. Nothing about it is
    intermittent: the failure is permanent and grows. **This is F018 and F019 with
    the environment being time rather than a tool version** — a test that reads a
    clock is a gate whose correctness depends on a record that is not in it.
    **Repair:** the fixture gained `backdate_claim_now`, which dates the entry from
    `datetime.now`, and the three CLI tests use it, so a claim is N hours old, which
    is what a lease assertion is about. `backdate_claim` keeps the fixed clock for
    the unit tests, which do pass it. Two methods rather than a flag, because the
    clocks differ by however long ago the suite was written and a flag lets a test
    pick the wrong one silently. The negative control the expired assertion lacked
    was added too: a claim older than the *widest* lease is still abandoned — falsified
    by moving its age under the threshold, which fails it with `0 != 4`.
    **Ceiling:** the fix dates the fixture rather than injecting a clock into the CLI,
    so those three tests still depend on the wall clock agreeing with itself within a
    test's runtime. Any other test that dates a record against a fixed instant and then
    lets production code read the real clock has the same defect, and nothing scans for
    the pairing. General form in [`tests/README.md`](tests/README.md).

14. **A decision record's own header was false in two of five files, and the
    identifier rule read every other source** (solved in T-0042). A decision number
    is written in three places that must agree: the `## Dnnn — …` heading that
    defines it, the index row in [`DECISIONS.md`](DECISIONS.md), and the
    `Decisions **…**` line under each record's title — the first thing a reader
    sees. T-0030 held the second to the first and T-0036 added the numbered defect
    list; neither read the third. `DECISIONS-GATING.md` said
    `Decisions **D013, D024–D029**` while defining D024, D025, D026, D029, D030,
    D032 and D035 — naming D013, which lives in another file, and omitting three of
    its own; `DECISIONS-PRACTICE.md` said `D011–D018, D027–D028` while defining
    D011, D012, D014–D018, D031, D033 and D034, so its range covered exactly the
    three entries that moved out when T-0030's split was reversed. **Both index rows
    were correct throughout**, which is what a reader checking one source concludes.
    The range is the general form: it claims a contiguous block, and a split moves
    entries out of the middle without changing either end.
    **Repair:** `tools/originlib/decisionheader.py` reads the header as the third
    source and reports both directions, through `idcheck` — the one entry point both
    publishing gates call. A header it cannot read is itself reported, which is
    D025's second obligation and the failure defect 10's control found. Falsified
    against the defect's own bytes: `d451169` carried both false headers,
    `idcheck.report` on the real tree returned **nothing** before the repair and
    twelve findings after it, and the repaired tip is silent.
    **Ceiling:** the header is compared as a set of identifiers and not as wording,
    it reads one line per record and nothing outside `DECISIONS*.md`, and a
    document defining decisions elsewhere would not be asked for a header. The full
    account is in [`tests/README.md`](tests/README.md) beside the tests.

13. **`sync land` regenerated only the generated files git reported as conflicted,
    so a cleanly merged one was published stale** (solved in T-0041). The three
    generated files are functions of the whole tree, so two VMs adding one session
    each produce two *different* renders of the same file. When git merges them
    without a conflict — different lines, no overlapping hunk — the merged file is
    stale, and `_resolve_generated_conflicts` asks git what conflicted and correctly
    hears nothing. Commit `e942225` was published that way. **This is the fourth
    arrival of one defect family and the third repair that did not generalise**:
    T-0026/T-0027 fixed the *task* commands, session 015 fixed the *appenders*, and this
    layer is neither — it is the one that *merges* trees. **Repair:** after every
    rebase, `land` asks the question
    `doc lint` asks — is each generated file equal to its renderer — and commits
    the answer before the push, which refuses a dirty tree anyway; a missing file is
    rebuilt too. Falsified first: with the call removed the new test fails
    (`'sessions/INDEX.md' not found in []`) and its control stays green.
    **Ceiling:** the rebuild is a commit nobody claimed, on a tree that was just
    rebased, so an operator reading the log sees a commit between the work and the
    session that recorded it. `land` prints what it rebuilt and the commit says so
    in its own message, which is the only attribution available.

6. **Identifier allocation collides by construction** (both halves solved: allocation in
   T-0031, detection in T-0030). Identifiers were allocated by reading the local tree,
   so two VMs in an hour took the same number — **twelve times in two days, and a
   thirteenth at T-0047**. **The cost, measured:** a rebase restored one file's index
   row to the renumbered form while reverting its body, so a document and its own table
   disagreed; and `e6eb992` carried two findings both numbered F010. `idalloc.py` now
   reads `origin/<base>` — task files, claim ledger, findings definitions and index
   rows, decision definitions and spans — plus this working tree, and every command that
   hands out a number prints the record it read; falsified first, since with the old
   allocator a clone behind the base allocated `T-0002` where the base already defined
   it. `idcheck.report` then refuses a colliding tree in `sync land` and reports it in
   `doc lint` rule 7; over all 174 commits it flags exactly one (`e6eb992`), and it
   found a live desync on its first run — D030 missing from `DECISIONS.md`. **Residual,
   stated:** two VMs allocating between their own fetches still collide and an unpushed
   number reserves nothing; the push rejection and the detector catch it, nothing
   prevents it, and **this cost one collision in the act of fixing it** — both VMs
   published a D032 and this side renumbered to D033; every collision is in
   [`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md).

8. **The suite was red on every interpreter it had never run on** (solved in
   T-0034, F018). `tests/python-versions.json` named 3.9 to 3.11 as versions nobody
   had run, and `test_doctor_versions.py` — written hours earlier — asserted that
   the interpreter running it was in that record: a fact about the record, not the
   code. On 3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2 the suite failed on
   exactly that assertion and nothing else. **Repair:** the test states the
   disjunction it can support, and `tests/test_ci_matrix.py` holds the workflow's
   matrix to the record in both directions. **Ceiling:** the record is
   hand-maintained, and CI covers only what `actions/setup-python` publishes, so a
   matrix row is evidence about that row and nothing beyond it. 
9. **The suite asserted that this machine's git is in the record** (solved in
   T-0034, F019). The same class as 8, one function away: every CI row was red from
   T-0033 onward while the runner image ships **git 2.55.0** and the record named
   2.25.1 and 2.56.0, the run log needs admin rights so the cause was invisible from
   outside, and the stated reason at the time — that the public check-runs API returns
   no annotations — was false for this very run (F020). **Repair:** the assertion is
   the comparator's contract — four reachable states, an `exercised` verdict carrying
   its entry's scope and machine — with a control that emptying the record moves every
   version off `exercised`; adding the 2.55.0 entry alone would have made CI green and
   left the assumption in place. **The general form of 8, 9, 15 and 19: a gate that
   reads its own environment is only as portable as the record of that environment.**

18. **Every step whose only job is to emit a diagnostic was skipped when an earlier
    step failed** (solved in T-0046). Each of the five file-reading gate steps carried
    `if: matrix.python-version == '3.12'` and no status function, so an implicit
    `success()` skipped all five on a red `Tests` step: runs `37189825232` and
    `37190842104`, 2026-10-04. It is also what made the record wrong twice (F021); the
    evidence and ceiling are in
    [`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md).

17. **A gate's report named a step and nothing else** (solved in T-0040, two faults in the
    same path; method and ceiling in
    [`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md)).

19. **A link's verdict was a function of the checkout's neighbours rather than of the
    repository** (solved in T-0051, D041). Rule 3 tested its candidates for existence
    *wherever they landed*, so `../../docs/x.md` from `tasks/` was decided by what the
    checkout's parent held — T-0047's `doc lint` passing in a worktree and failing in
    the main checkout on identical bytes. Containment is now decided lexically, so the
    existence check is the only read, and removing that filter brings the parent-
    dependence back. Instance of the form named in 9, the environment being the
    filesystem *outside* the repository; method in
    [`docs/policy/gate-falsification.md`](docs/policy/gate-falsification.md).

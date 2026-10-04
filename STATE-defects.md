<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Known defects

Every defect this repository's own tooling and records have shown, whether or not
it is fixed. Split out of [`STATE.md`](STATE.md) on 2026-10-04 when that file
reached 293 of the 300 permitted lines, so the reload point stays a reload point.

The rule for this list: a defect is *solved* only when a gate fails on its own
bytes and passes on the repair. A repair that has not been falsified against the
defect is listed as open.

1. **An in-flight session reddened every other VM's CI** (solved in T-0020). Two
   correct rules met — `task claim` needs HEAD on the remote base, so a claiming
   VM must publish its `session_start` first, and D013 then failed every push.
   `tools/originlib/inflight.py` separates in flight from abandoned from the tree
   alone (D027; findings F014 and F015). The live record corrected that predicate
   once already: clause 1 required the session to name a task, the other VM
   started one without `--task`, so the gate called a working session abandoned. A
   claim in the ledger naming the session now counts.

2. **Reconciliation compared trees, not authorship** (solved in T-0024, D028). A VM
   that landed another VM's work inherited its `unlogged_change` and
   `documentation_gaps` reports — session 029 emitted nine of the first, none of
   them its own. `sync pull`/`sync land` now record a `base_advance` naming the
   commits that arrived, and reconciliation attributes a path by the newest thing
   that touched it. **Ceiling:** attribution knows only about base moves the
   tooling performed, so a rebase run by hand still reports; that is the intended
   direction of failure.

3. **Every generated file stamped `last-verified` with the render date** (solved
   in T-0024, D029), so `doc lint` failed on 42 committed session reports and all
   three indexes on 2026-10-04 — the day after they were written. Each generator
   now stamps from the content it renders. The CI consequence is `inferred` from
   that local reproduction: no pushed run has failed this way, because the two
   red runs at 23:58 on 2026-10-03 had a different and verified cause (defect 5).

4. **A pushed task file without `doc index` reddens CI** (solved in T-0026 and
   T-0027). Runs `37163434868` and `37163438950` failed on Documentation lint:
   this VM created a task, committed it and pushed it without rebuilding the
   generated indexes, so the orphan rule rejected the file the VM had just
   created. `task new`, `claim`, `complete` and `release` now rebuild
   `tasks/INDEX.md` and `docs/INDEX.md`; a *published claim* also stages them,
   because that commit is the first thing every other VM reads (four more red
   runs, `37165502352`–`37165807196`, were the same defect one step later).
   **The rule is unchanged** — a file no command wrote is still an orphan, which
   the new tests assert — because the omission was the defect, not the strictness.
   **Residual:** the create commit is the agent's own, so `task new` prints the
   command that stages the indexes; nothing can enforce that step.

5. **`doctor` did not compare this VM's interpreter or git against what the suite
   has been exercised on** (solved in T-0033). Both records existed and were
   schema-checked — `tests/git-versions.json` (T-0018) and
   `tests/python-versions.json` (T-0032) — and nothing read either at run time,
   so a VM on Python 3.9 was indistinguishable in the report from one on 3.8.10.
   `tools/originlib/versions.py` now compares each probed tool against the record
   covering it and reports four states: `exercised` with the entry's own `scope`
   attached, `NOT exercised`, `record unreadable`, and `no record` for the three
   tools no record covers. **The third state is the load-bearing one** — a
   comparison that cannot tell "we looked and it is not there" from "we could not
   look" reports a confident answer in both, which is the failure T-0025 found in
   this same report. Falsified four ways before it was trusted: a comparison that
   always said `exercised` (3 failures), a missing record read as `unexercised`
   (5), a summary dropping the record name (2), and `doctor` not reporting the
   comparison at all (1). Its first implementation also matched entries in file
   order, so a VM on 3.12.15 got CI's `3.12` entry's scope instead of its own;
   the longest entry now wins, and a test says so.
   **Ceiling:** `exercised` means a run happened, not that the version is
   supported, and no interpreter between 3.8 and 3.12 has ever run this suite.

7. **A test fixture inherited the runner's environment** (solved in T-0035).
   `tests/pushcred_fixture.py` built a sandbox with a fresh `HOME`,
   `XDG_CONFIG_HOME`, git config and `GIT_CONFIG_SYSTEM=/dev/null`, and left
   `GH_TOKEN`/`GITHUB_TOKEN` alone. `pushprobe` counts an environment token as a
   credential mechanism — correctly, it is one — so
   `test_no_mechanism_is_unavailable_not_broken` built a machine with a mechanism
   and asserted `unavailable`. Three CI runs failed (`37174050724`,
   `37174316639`, `37174309822`) while both VMs were green on the same commits,
   and the cause predates T-0033: it arrived with the fixture in T-0025.
   **This is the shape worth naming — a defect that only reproduces where the
   author does not work.** Falsified three ways, and the third was found *by*
   falsifying: a fixture that clears the tokens but never restores them leaves
   every test green, because unittest shares one process and nothing asserted
   the restore. A control now asserts the opposite verdict, so the original
   test says *which* absence it is about rather than that some absence is
   reported. **Ceiling:** the fixture builds the machine its own tests need and
   says nothing about the runners those tests never model.

10. **The identifier rule did not read the defect list, so two VMs took defect 7
    in the same hour** (solved in T-0036). Rule 7 read findings definitions,
    findings index rows, decision spans and task file names. `STATE-defects.md` is
    an ordered list of bold headings with no `F`, `D` or `T` identifier in it, so
    it was the one document here whose identifiers were checked by reading them —
    and reading them found T-0034's and T-0035's **defect 7** side by side. Both
    copies reached the shared base (`e53ca23`, `e701ad8`), each VM's own tree
    internally consistent; the unpushed side renumbered 7 and 8 to 8 and 9 in
    `157e463`, which is the standing rule and the cheapest available repair.
    **Repair:** `tools/originlib/defectlist.py` reads a numbered list item whose
    subject is bold as a definition of that number, and reports a number defined
    twice. It is reached through `tools/originlib/idcheck.py`, the single entry
    point both publishing gates call — the wiring lesson being that a module added
    to `doc lint` is not thereby read by `sync land`, which is the operation that
    creates the collision. Falsified against the defect's own bytes: each commit's
    real tree extracted from git, the previous wiring reports **nothing** on
    `e53ca23` and `e701ad8` where the new rule names defect 7 with both lines, and
    reports nothing on `157e463` or the tip either — so the rule reports nothing on
    a correct tree, which is the half of a falsification that is easy to leave out.
    **Second obligation, and it came from the first control failing:** a rule that
    cannot read its input must say so. A `STATE-defects.md` from which no entry can
    be read is itself reported, because a parser that quietly stops matching looks
    exactly like a clean tree — D025's shape, reached from a new direction.
    **Ceiling:** a gap in the numbering is not reported, since a dropped entry and
    a withdrawn defect produce the same bytes and the record does not distinguish
    them; nothing is checked about what a reference points at; and there is no
    allocator here, so this is the detection half of a race it cannot prevent.

## Open

Numbering is continuous and never reused, so a solved defect keeps its
number and this section is not in numeric order: entries land under whichever
heading they belong in when they are closed.

11. **`task new` silently keeps one `--acceptance` line and drops the rest** (solved
    in T-0039). Five criteria were passed on the command line and the task file
    recorded one, with no warning: `--acceptance` and `--steps` were declared with
    `default=""` and no `action="append"`, so argparse kept the last occurrence.
    **The cost is a task that reads as complete against a truncated definition of
    complete** — the same shape as F010's near-vacuous gate: the field is filled in,
    and nobody can tell that most of it is missing. Found by using the documented
    workflow, which is the only way this class of defect shows up.
    **Repair:** both flags accumulate, one line per occurrence, joined in
    `cli_task.py` so `taskops.create` keeps taking a string and its other callers
    are unaffected. Falsified first: three flags wrote one line, and three `--steps`
    wrote only `3. third`. A fourth control came from the same run —
    `taskops.create` defaults `acceptance` to a bare `- [ ] `, which the CLI made
    unreachable by always passing a value; the test now pins the empty section
    instead, because a checkbox nobody wrote is worse than an empty heading.
    **Ceiling:** only the two flags a writer repeats are changed. Every other `--`
    flag in `cli_args.py` is still last-wins, and the general rule — *a flag that
    collects more than one thing must say so* — is not enforced anywhere.

12. **A task file is changed by the commands that manage it and declared by
    neither** (open, found 2026-10-04 across sessions 017 and 018). `task claim` and
    `task complete` rewrite the task file, and reconciliation reports any
    changed-but-undeclared path as an `unlogged_change`. Three such events in two
    sessions, every one of them the task file, on tasks that were otherwise
    complete. The protocol's answer is to declare it, and an agent that has just
    run `task complete` is at the least alert state for remembering one more
    command. **The fix has a real trade-off and is not made here:** the task
    commands could declare the file they change, which removes the gap and also
    removes a place where the agent could have declared something *else* on purpose.
    **Ceiling:** the tooling cannot tell an intentional declaration from an
    automatic one, so an automatic declaration weakens the signal it repairs.

14. **A decision record's own header was false in two of five files, and the
    identifier rule read every other source** (solved in T-0042). A decision
    number is written in three places that must agree: the `## Dnnn — …` heading
    that defines it, the index row in [`DECISIONS.md`](DECISIONS.md) that says
    which file holds it, and the `Decisions **…**` line under each record's
    title — the first thing a reader sees. T-0030 held the second to the first in
    both directions and T-0036 added the numbered defect list; neither read the
    third. `DECISIONS-GATING.md` said `Decisions **D013, D024–D029**` while
    defining D024, D025, D026, D029, D030, D032 and D035 — naming D013, which
    lives in `DECISIONS-SESSIONS.md`, and omitting three of its own entries.
    `DECISIONS-PRACTICE.md` said `Decisions **D011–D018, D027–D028**` while
    defining D011, D012, D014–D018, D031, D033 and D034, so its range covered
    exactly the three entries that moved to `DECISIONS-SESSIONS.md` when T-0030's
    split was reversed, and it omitted three of its own. **Both index rows in
    `DECISIONS.md` were correct throughout**, which is what a reader checking one
    source concludes. The `D011–D018` range is the general form: a range is a
    claim about a contiguous block, and a split moves entries out of the middle
    of one without changing either end.
    **Repair:** `tools/originlib/decisionheader.py` reads the header as the
    third source and reports, in both directions, an identifier the file defines
    and its header does not name and one its header names and the file does not
    define; reached through `idcheck`, the single entry point both publishing
    gates call. A decision record whose header cannot be read is itself reported,
    which is D025's second obligation and the failure defect 10's control found.
    Falsified against the defect's own bytes: `d451169` carried both false
    headers, `idcheck.report` on the real tree returned **nothing** before the
    repair and twelve findings after it, and the repaired tip is silent.
    **Ceiling:** the header is compared as a set of identifiers and not as
    wording; it reads one line per decision record and nothing outside
    `DECISIONS*.md`; and a document that defined decisions without living there
    would not be asked for a header.

13. **`sync land` regenerated only the generated files git reported as conflicted,
    so a cleanly merged one was published stale** (solved in T-0041). The three
    generated files are functions of the whole tree, so two VMs adding one session
    each produce two *different* renders of the same file. When git merges them
    without a conflict — different lines, no overlapping hunk — the merged file is
    stale, and `_resolve_generated_conflicts` asks git what conflicted and
    correctly hears nothing. Commit `e942225` was published that way and `doc
    lint` on it says `sessions/INDEX.md: generated file is stale`; the next commit
    rebuilt it. **This is the fourth arrival of one defect family and the third
    repair that did not generalise** — T-0026/T-0027 fixed the *task* commands,
    session 015 fixed the *appenders*, and this layer is neither: it is the one
    that *merges* trees. **Repair:** after every rebase, `land` asks the question
    `doc lint` asks — is each generated file equal to its renderer — and commits
    the answer before the push, which refuses a dirty tree anyway. A missing file
    is rebuilt too, since `doc lint` calls that a violation as well. Falsified
    first: with the call removed the new test fails
    (`'sessions/INDEX.md' not found in []`) and its control stays green.
    **Ceiling:** the rebuild is a commit nobody claimed, on a tree that was just
    rebased, so an operator reading the log sees a commit between the work and the
    session that recorded it. `land` prints what it rebuilt and the commit says so
    in its own message, which is the only attribution available.

6. **Identifier allocation collides by construction** (both halves solved:
   allocation in T-0031, detection in T-0030). Identifiers were allocated by
   reading the local tree, so two VMs in an hour took the same numbers. Six times
   on 2026-10-03: T-0016 and F009/F010/D022; session 029's F012 against session
   026's F010; session 030's F012 for E3's attribution against VM 0947's F012 for
   the worktree defect; D024 issued twice for unrelated decisions; then F013,
   `FAILURES-findings-3.md`, D025 and D026 all taken on 0944 while 0947 held the
   same numbers. VM 0947's two findings became F014 and F015 and its session-gate
   decision D027, and six more collisions followed in a single hour on 2026-10-04
   (T-0024 through T-0028, F014, F015, D027, D028). **The cost was measured:** a
   rebase resolution restored one file's index row to the renumbered form while
   reverting its body, so a findings file and its own table disagreed about the
   same entries; and commit `e6eb992` carries two findings both numbered F010 to
   the shared base, which no gate reported.
   **Allocation solved in T-0031, `observed`:** `tools/originlib/idalloc.py`
   allocates F, D and T numbers from `origin/<base>` — task files, claim ledger,
   findings definitions and index rows, decision definitions and spans — plus this
   working tree, and every command that hands out a number prints the record it
   read. Falsified first: with the old allocator, a clone whose tree is behind
   the base allocated `T-0002` where the base already defined it; after the
   repair it allocates `T-0003`. A withdrawn task's number is no longer recycled,
   because the ledger still names it.
   **Detection solved in T-0030, D032:** `tools/originlib/identifiers.py` reports
   an identifier defined twice, an index row with no body, and a decision its own
   index row does not list; `sync land` refuses to publish such a tree and `doc
   lint` rule 7 reports it. Falsified in both directions: one commit of 174 is
   flagged, and each of the three mechanisms notices its own removal. It found a
   live desync on its first run — D030 missing from `DECISIONS.md`.
   **Residual, stated:** two VMs allocating between their own fetches still
   collide, and an unpushed number reserves nothing. The push rejection and the
   detector catch it; nothing prevents it. **This cost one collision in the act of
   fixing it:** VM 0947's D032 and this VM's D032 were both published, and this
   side renumbered to D033 during the rebase.

8. **The suite was red on every interpreter it had never run on** (solved in
   T-0034, F018). `tests/python-versions.json` named 3.9 to 3.11 as versions
   nobody had run, and `test_doctor_versions.py` — written hours earlier in
   T-0033 — asserted that the interpreter running it was in that record. On
   3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2 the suite failed on exactly that
   assertion and nothing else; on 3.8.10 and CI's 3.12 it is green. The gate was
   reading the record, not the code. A sibling test asserted the same claim from
   a different source (`doctor` probes `python3` on `PATH`), and the two agreed
   only because this VM's `PATH` interpreter is one of the two recorded ones.
   **Repair:** the test states the disjunction it can support, and
   `tests/test_ci_matrix.py` now holds the workflow's matrix and the record to
   each other in both directions. Falsified first: the new gate fails on the
   unmodified workflow, names the five unrecorded rows, and fails again on the
   unmodified record; two of its parsers were corrected because the controls
   they failed were the parsers, not the code. **Ceiling:** the record is
   hand-maintained, and CI can only cover what `actions/setup-python` publishes,
   so a matrix row is evidence about that row and nothing beyond it.

9. **The suite asserted that this machine's git is in the record** (solved in
   T-0034, F019). Every CI row was red at the `Tests` step from T-0033 onward,
   including rows whose interpreter had just been measured green on a VM, and the
   run log needs admin rights while the public check-runs API returned no
   annotations — so the cause was invisible from outside. Reproduced: the runner
   image ships **git 2.55.0** (`actions/runner-images` readme, `source-supported`)
   and `tests/git-versions.json` named 2.25.1 and 2.56.0. A conda-forge 2.55.0
   unpacked outside the repository reproduced the failure exactly. Same class as
   defect 8 and one function away from it: **a gate that reads its own environment
   is only as portable as the record of that environment.**
   **Repair:** the assertion is now the module's contract — four states reachable,
   an `exercised` verdict carrying its entry's scope and machine — with a negative
   control that emptying the record's list moves every version off `exercised`.
   Adding the 2.55.0 entry alone would have made CI green and left the assumption
   in place. **Also:** the git record gained a `not_exercised` list and a
   `where` on every entry, with test clauses, so the gap is nameable rather than
   inferred from two points.

**Reconciliation cannot see a hand-run rebase continuation, and that ceiling was
reached twice.** Session 012 closed with 24 `unlogged_change` events and session
040 with its own, both times including the other VM's files, which arrived
through hand-run `git rebase --continue` calls. D028 attributes a path only from
a base move the tooling performed, so those paths stay reported — the intended
direction of failure, and the reason a session has to record here what a
*closed* stream cannot accept: `session finish` will not take the events, and
editing the stream afterwards would be worse than leaving the gap visible.

## What a fix costs to believe

The method every entry above is held to — falsify against the defect's own bytes,
in both directions, and say so when the input cannot be read — is in
[`docs/policy/gate-falsification.md`](docs/policy/gate-falsification.md), split
out of this file on 2026-10-04 (T-0042) when a new entry took it past the
300-line cap. The mechanism and the lessons from five falsifications that failed
are in [`tests/README.md`](tests/README.md), next to the tests they describe.
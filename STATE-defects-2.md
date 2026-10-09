<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Known defects, part 2 — the solved entries before the `## Open` section

Split out of [`STATE-defects.md`](STATE-defects.md) on 2026-10-04 (T-0056) when
that file reached the 300-line cap and defect 22 had nowhere to go. **The rule is
unchanged and lives in the parent file:** a defect is *solved* only when a gate
fails on its own bytes and passes on the repair; a repair not falsified against
its defect is open. Method:
[`gate-falsification.md`](docs/policy/gate-falsification.md).

**Why the split falls here rather than anywhere else.** The parent file's own
record said this split "cannot be done inside its own numbered list without
`defectlist.py` reading more than one file — so that split is a task, not an
edit", and it is done here rather than by trimming. The cut is at the `## Open`
heading, which is a boundary the document already states: entries above it are
the ones solved before the open section was written, and entries below it are the
later ones. So a reader of either file knows which half it holds, and a reader of
the pair still reads every number in order.

**What had to change with it.** `defectlist.py` reads a *set* of files rather than
one, and `STATE-defects.md`'s preamble says so, because a reader that checks one
list and not the other is the exact defect the rule exists to catch — the reason
it reads the defect list at all is defect 10, where two VMs took defect 7 in the
same hour and nothing reported it. A rule that read only the parent would be
blind to every entry below.

Entries moved verbatim. Numbering is continuous and never reused, so a reference
to defect 3 still resolves here and defect 15 still resolves in the parent.

1. **An in-flight session reddened every other VM's CI** (solved in T-0020). Two
   correct rules met — `task claim` needs HEAD on the remote base, so a claiming VM
   must publish its `session_start` first, and D013 then failed every push — and the
   live record corrected its own predicate once already: clause 1 required the session
   to name a task, the other VM started one without `--task`, and the gate called a
   working session abandoned. `inflight.py` now separates the two from the tree alone
   (D027; F014, F015), counting a claim in the ledger.

2. **Reconciliation compared trees, not authorship** (solved in T-0024, D028). A VM
   that landed another VM's work inherited its `unlogged_change` and
   `documentation_gaps` reports — session 029 emitted nine of the first, none of
   them its own. `sync pull`/`sync land` now record a `base_advance` naming the
   commits that arrived, and reconciliation attributes a path by the newest thing
   that touched it. **Ceiling:** attribution knows only about base moves it can prove —
   reached by sessions 012 and 040 through hand-run `git rebase --continue`. T-0053
   recovers that one from `ORIG_HEAD` and the reflog; a hand-run pull, cherry-pick or
   reset remains unrecorded. That is the intended direction of failure.

3. **Every generated file stamped `last-verified` with the render date** (solved
   in T-0024, D029), so `doc lint` failed on 42 committed session reports and all
   three indexes on 2026-10-04 — the day after they were written. Each generator now
   stamps from the content it renders. The CI consequence is `inferred` from that local
   reproduction, and no pushed run has failed this way.

4. **A pushed task file without `doc index` reddens CI** (solved in T-0026 and
   T-0027). Runs `37163434868` and `37163438950` failed on Documentation lint: this VM
   created a task, committed it and pushed it without rebuilding the generated indexes,
   so the orphan rule rejected the file the VM had just created. `task new`, `claim`,
   `complete` and `release` now rebuild both indexes, and a *published claim* also
   stages them, because that commit is the first thing every other VM reads (four more
   red runs, `37165502352`–`37165807196`, were the same defect one step later). **The
   rule is unchanged** — a file no command wrote is still an orphan, which the new tests
   assert — because the omission was the defect, not the strictness. **Residual:** the
   create commit is the agent's own, so `task new` prints the command that stages the
   indexes; nothing can enforce that step.

5. **`doctor` did not compare this VM's interpreter or git against what the suite
   has been exercised on** (solved in T-0033). Both records existed and were
   schema-checked — `tests/git-versions.json` and `tests/python-versions.json` — and
   nothing read either at run time, so a VM on Python 3.9 was indistinguishable in the
   report from one on 3.8.10. `tools/originlib/versions.py` now reports `exercised` with
   the entry's own `scope`, `NOT exercised`, `record unreadable`, and `no record`, and
   **the third is the load-bearing one**: a comparison that cannot tell "we looked and
   it is not there" from "we could not look" reports a confident answer in both. Falsified
   four ways, and its first implementation matched entries in file order, so a VM on
   3.12.15 got CI's `3.12` scope; the longest entry wins and a test says so.
   **Ceiling:** `exercised` means a run happened, not that the version is supported.

7. **A test fixture inherited the runner's environment** (solved in T-0035).
   `tests/pushcred_fixture.py` built a sandbox with a fresh `HOME`, git config
   and `GIT_CONFIG_SYSTEM=/dev/null`, and left `GH_TOKEN`/`GITHUB_TOKEN` alone;
   `pushprobe` counts an environment token as a credential mechanism — correctly,
   it is one — so a test asserted `unavailable` on a machine that had one. Three
   CI runs failed while both VMs were green on the same commits. **A defect that
   only reproduces where the author does not work.** Its third falsification was
   found *by* falsifying: a fixture that clears the tokens but never restores them
   leaves every test green, because unittest shares one process.
   **Ceiling:** the fixture builds the machine its own tests need.

10. **The identifier rule did not read the defect list, so two VMs took defect 7
     in the same hour** (solved in T-0036). Rule 7 read findings definitions,
     findings index rows, decision spans and task file names. `STATE-defects.md` is an
     ordered list of bold headings with no `F`, `D` or `T` identifier in it, so it
     was the one document here whose identifiers were checked by reading them — and
     reading them found T-0034's and T-0035's **defect 7** side by side. Both copies
     reached the shared base (`e53ca23`, `e701ad8`), each VM's own tree internally
     consistent; the unpushed side renumbered in `157e463`, the standing rule.
     **Repair:** `tools/originlib/defectlist.py` reads a bold-subject list item as a
     definition of its number and reports one defined twice, reached through `idcheck.py`
     — the single entry point both publishing gates call, because a module wired into
     one gate is not thereby read by the other. Falsified against the defect's own
     bytes: the previous wiring reports **nothing** on either commit and the new rule
     names defect 7 with both lines, and nothing on the repair or the tip either.
     **Second obligation, and it came from the first control failing:** a rule that
     cannot read its input must say so, because a parser that quietly stops matching
     looks exactly like a clean tree — D025's shape from a new direction.
     **Ceiling:** a gap in the numbering is not reported, since a dropped entry and a
     withdrawn defect produce the same bytes; and there is no allocator here, so this
     is the detection half of a race it cannot prevent. See
     [`tests/README.md`](tests/README.md).

25. **Two concurrent writers of one session's event stream each
     appended the same seq** (solved in session 2026-10-08-010).
     `events.append` computed `next_seq` and wrote in two steps, so
     two processes on one session file — a live session and a
     reconcile pass — each computed the same seq and both appended
     it. Observed as 19 duplicated seqs in the finished stream of
     `2026-10-08-008`, which `session verify` — and CI's
     `session verify --strict` step — read as a non-contiguous
     stream and exited 4 on. **Repair:** `events.locked` holds an
     exclusive `flock` across the seq assignment and the append, and
     `recorder.record_command` holds the same lock across the
     commands.log header seq and the event append, so those two
     numbers cannot drift apart either. The corrupted stream was
     renumbered in file order (all 181 events preserved, the
     session's generated report regenerated). Falsified three ways:
     the gate failed on the corrupted bytes and passes on the
     repair; the same two-process append produced duplicate seqs in
     8 of 8 rounds on the pre-fix code and 0 of 8 on the repair;
     and a regression test runs two processes against one stream and
     asserts exactly 1..60 (`tests/test_events.py`). **Ceiling:**
     the lock serializes writers; a reader that never takes it can
     still observe a half-written line, which `read` already
     tolerates as malformed.

26. **The identifier allocator read a quoted string as an allocation** (solved
    in session 2026-10-09-002). `NUMBERED_CELL` matched `F(\d{3})` with no
    word boundary, and F097's own findings row quotes the bike serial
    `SNACEOSF18391`. The serial's `F183` counted as a defined finding, so
    `origin id next F` reported the highest as 183 and handed out **F184**,
    skipping 83 numbers. The record's own prose names the trigger twice: the
    module docstring says a citation must not count as an allocation, and the
    gate next to it (`identifiers.py`, whose `DEFINITION` pattern *does* anchor
    with `^`) was reading a different, stricter pattern than the allocator —
    so a rule written for the problem existed and was not applied here.
    **Repair:** both boundaries added to `NUMBERED_CELL`, with the comment
    naming this serial as the reason they are load-bearing. **Falsified against
    its own bytes:** two new tests in `tests/test_idalloc.py` (one quoting
    `SNACEOSF18391`, one quoting `SNACEOSF1839A` for the trailing side) both
    fail on the pre-fix pattern — `F184 != F098`, `F184 != F005` — and pass on
    the repair; the full suite is 832 tests green. `origin id next F` now
    returns **F101**. **Ceiling:** the boundary fixes quoted strings, not a
    *cell* that is genuinely an allocation and should be counted — the pattern
    still cannot tell `| F010 |` the allocation from `| see F010 |` the
    citation, because both are table cells. Numbering is also only ever read,
    never reserved, so two VMs allocating from a shared base can still collide;
    that race is unchanged.

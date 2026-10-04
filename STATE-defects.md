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

## Open

Numbering is continuous and never reused, so a solved defect keeps its
number and this section is not in numeric order: entries land under whichever
heading they belong in when they are closed.

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

7. **The suite was red on every interpreter it had never run on** (solved in
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

## What a fix costs to believe

Every entry above marked solved was falsified against its own defect first: the
new tests were run against the unfixed code and had to fail. One of those
falsifications (T-0024's second attempt) mutated a code path the callers never
reach and passed anyway — the failure of the falsification, not of the gate — so
it was redone by reverting the generators instead. See D025 in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).

**A gate that has never fired looks exactly like a gate with nothing to report.**
T-0030's first decision-index check matched no row in any commit, because the
regex did not allow a Markdown link around the filename, so the sweep of all 174
commits passed while that half of the rule did nothing. The control test — the two
`FAILURES.md` rows this repository deliberately paraphrases — was what caught it,
and it had already caught the other half of the same draft, which compared index
rows to headings as strings and flagged 83 of 174 commits. Both are in the
session's `commands.log`.
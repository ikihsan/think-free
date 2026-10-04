<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Evidence-driven roadmap

Stages are ordered by dependency, not by date. Evidence can send work back to an
earlier stage; there is no calendar here and none is promised.

Status legend: **done**, **partial**, **not started**, **blocked**.

## A — Independent exploration

**Status: partial.** All six roles sealed; the consolidation below is partial.

- [x] Verify the environment and record actual limits (`EXPERIMENTS/000-capabilities`)
- [x] Preserve the mission and boundaries (`MISSION.md`)
- [x] Sealed reports A–D (`RESEARCH/A.md`–`D.md`)
- [x] Investigation E: experimental engineer — three cheap falsifiable
      mechanisms. Sealed 2026-10-03 (T-0002). E1 and E2 remain `untested`; E3's
      census ran (T-0013) and its declared gate turned out not to be able to fail
      (`FAILURES.md` F010), so E3's load-bearing claim is still `untested`.
- [x] Investigation F: adoption researcher — six pre-release checkable criteria.
      Sealed 2026-10-03 (T-0003); the criteria become a gate at stage D, not a
      candidate screen.
- [ ] Consolidate the reports into competing hypotheses, preserving
      disagreements. Partly done in `HYPOTHESES.md`; the cross-report screen is
      `RESEARCH/SYNTHESIS.md` (T-0012).

## B — Experimental discovery

**Status: partial.** Ten experiments have run; four invention claims are
disproved, one declared gate could not fail, one mechanism was confirmed while
its candidate died of it, and no candidate is validated.

- [x] Write the experiment protocol (`docs/process/experiment-protocol.md`)
- [x] Run E001 as a baseline check; kill gate met, candidate's motivating example
      disproved (`FAILURES.md` F001)
- [x] Write kill gates for the three held candidates in `HYPOTHESES.md` (T-0001, 2026-10-03)
- [x] Apply the information-sufficiency test to the three held candidates (`003-information-sufficiency`, T-0008: W1/W3 survive, W2 spec insufficient, F007)
- [x] Run the A1 masking experiment on the PPNA sidewalk extract (`002-a1-masking`, T-0005/T-0006/T-0007: count-budget gate met, fieldwork-cost gate fails, F006)
- [x] Test the knitting candidate's Stage-A planner twice: per-error rule
      suboptimal (`004-knitting-stage-a`, T-0010), whole-neighbourhood search
      exact (`005-knitting-bounded-search`, T-0011)
- [x] Search the knitting candidate's last kill-gate condition in three
      vocabularies (`RESEARCH/PRIOR-ART-KNITTING.md`, T-0015): the algorithmic
      advantage is prior art (`FAILURES.md` F009), no tool supplies an
      intervention sequence for an existing hand-knit
- [x] Run the ventilation candidate's measurement-design kill gate
      (`006-ventilation-measurement-design`, T-0014): gate not met, formulation
      stopped (`FAILURES.md` F008)
- [x] Run E3's build-timestamp census over 200 PyPI wheels (`007-build-timestamps`,
      T-0013): declared 5% gate met at 0.965, but the metric measures DOS-epoch
      pinning rather than reproducibility (`FAILURES.md` F010)
- [x] Attribute the byte difference (`008-build-timestamp-attribution`, T-0017):
      398 of 398 differing bytes are timestamp fields, and `SOURCE_DATE_EPOCH`
      makes builds bit-identical, so E3's mechanism is supported and its
      candidate abandoned — the remedy is one environment variable the builder
      already honours (`FAILURES.md` F012)
- [x] Measure the premise behind the dominant kill reason rather than a proxy for
      it (`015-incumbent-serving`, T-0060): "prior art exists" was checked against
      stars twice and registry installs once, and T-0059's own dead branch meant the
      mature arm was never read. Two new channels close it, and the premise
      **holds in mature vocabularies (4 of 4 served) and fails in young ones
      (1 of 4)** — `FAILURES.md` F034
- [ ] Run at least two materially different falsification experiments before any
      commitment decision. Only the knitting line has had two, both producing no
      product claim; with C2 stopped (F008) and the knitting algorithmic claim
      abandoned (F009), no candidate has two.
- [ ] Independently reproduce each result, checking oracle and baseline fairness

## C — Commitment

**Status: not started. Nothing may be selected yet.** Select only when evidence
demonstrates technical possibility, meaningful differentiation against the
strongest existing approach, practical value, and a plausible adoption path;
otherwise continue or pivot. Criteria in `docs/process/hypothesis-lifecycle.md`.

## D — Engineering

**Status: not started. No product exists.**

- [ ] Build the smallest independently usable implementation
- [ ] Behavioural tests that can fail on a meaningful defect
- [ ] Honest limits documented alongside capabilities
- [ ] Reproducible build and installation, security review
- [ ] Real examples, minimal learning curve

## E — Public release

**Status: not started. Blocked on C, D and the user's push authorization.**

- [ ] Licence, install path, demo, comparison, contributor guide
- [x] `origin release check` implemented against `RELEASE-MANIFEST.md` (T-0022)
- [ ] Push with explicit user authorization
- [ ] No unreleased behaviour described as shipped — the front-door state
      directive now makes this an agreement the machine checks, not a promise

## F — Real-world validation

**Status: not started.** No fabricated feedback, no unsolicited outreach.

- [ ] Observe actual use and adoption friction

## G — Expansion

**Status: not started.** Improve reliability, capability, accessibility and
interoperability in response to observed problems.

## H — Sustained reassessment

**Status: ongoing.** Reassess whether continuing is justified. Reopen a rejected
candidate only when the evidence that killed it is invalidated.

## Infrastructure track

Separate from the invention stages, because the mission cannot be run without it.

- [x] Session logging with append-only events and git reconciliation, including
      attribution by recorded evidence: a base move the tooling performed (D028), and a
      command's own write, honoured only while the file holds those bytes (T-0047, D040)
- [x] Command capture with exit codes and secret redaction; task dispatch with an
      append-only claim ledger
- [x] Documentation lint: line cap, metadata, links, table rows, orphans, generated
      freshness. A link resolves *inside* the repository without asking the filesystem,
      and a hand-authored document says each table row once (T-0051/52, D041/D043)
- [x] Generated indexes for documents, sessions, and tasks; 21 skills vendored in-repo and
      mirrored for every supported agent
- [x] Unresolved merge conflicts fail `doc lint` (T-0021, `FAILURES.md` F013),
      because three mission records had reached the shared base with markers in
      them while every gate read those files for a different property
- [x] Machine-readable exercised-git-versions record (`tests/git-versions.json`, T-0018)
- [x] Identifier allocation from the shared base for F, D and T, with the record
      it was read from printed by every command that hands out a number
      (`tools/originlib/idalloc.py`, `origin id next`, T-0031). Twelve
      collisions between two VMs in two days were the cost of allocating from a
      working tree instead
- [x] Decision log split by invariant a second time (`DECISIONS-GATING.md`, T-0018)
- [x] Environment doctor with presence-only credential checks
- [x] Continuous integration running lint, tests, release manifest, and session
      verification.
      Six gates, Python pinned with `setup-python`, failing tests re-emitted as
      public annotations. **Measured green on all six steps** on a pushed commit
      (run `37165413909`, `9e865a4`, T-0025); it had failed on **all 60** earlier
      runs because of a git-version defect in `sync land`
      (`FAILURES.md` F011, fixed in T-0016), and twice more on 2026-10-03 because a
      task file was pushed before `tasks/INDEX.md` was rebuilt.
- [x] Session gate that tells an in-flight session from an abandoned one
      (`tools/originlib/inflight.py`, T-0020). `session verify --strict` failed
      on every push of every VM whenever the fleet was working, because `task
      claim` requires the session's start to be on the base branch first. Now
      five clauses read off the tree, plus a 12-hour claim lease (D027).
- [x] The documented VM sequence is executable end to end: `worktree add` no
      longer refuses the claiming VM's own claim, and every flow refusal exits 1
      with one line instead of a traceback (`FAILURES.md` F014). The remaining red step is
      `session verify --strict` while any VM has a session in flight on the
      shared branch, which is D013 meeting fleet practice rather than a defect.
      T-0022 adds a sixth step, `release check`, which has not yet run on CI.
- [x] `origin release check` implemented against `RELEASE-MANIFEST.md` (T-0022):
      no wildcards, every tracked top-level entry classified exactly once,
      declared paths present unless `(pending)`, no path inside a directory of
      the other audience, no credential-shaped text in a classified path, and
      the front door's declared release state equal to the manifest's. It
      enforces agreement, not truth — **and `preflight` runs it** (T-0045), because
      a gate nobody runs from the command the protocol points at is a gate the
      next agent repeats the omission against: T-0042 added a root document,
      classified nothing, and its own `verify` passed
- [x] Reconciliation attributes a landed base move to the VM that wrote it (T-0024, D028). A
      session that merged a colleague's work closed with nine false `unlogged_change` events,
      four false `doc_update` events and an inherited `documentation_gaps` report; `sync` now
      records what arrived. A hand-run rebase is still reported, which is the intended direction
      of failure.
- [x] Generated files are functions of the tree, not of the clock (T-0024, D029). Every
      generator stamped `last-verified` with the render date, so `doc lint` failed on 42
      committed reports and three indexes the day after they were written.
- [x] `task new` leaves no orphan behind (T-0026 and T-0027, `observed` in runs
      `37163434868`, `37163438950` and four more on 2026-10-04): `new`, `claim`,
      `complete` and `release` rebuild the generated indexes, and a published
      claim stages them, so the commit every other VM reads first is lintable
- [x] Operations documents agree with what the fleet has actually run (T-0023 repaired the
      Python floor and the GitHub App status; T-0029 closed the `doctor` gap). The App's real
      permissions still need a human with its settings page — nothing here can read them
- [x] `doctor` reports the push credential mechanism (T-0029): the configured
      `credential.helper`, whether each named helper exists and is executable,
      App key files by path and mode, whether the helper depends on anything outside
      `~/.config`, and whether `git credential fill` obtains a credential. Three-valued verdict
      (`configured`/`broken`/`unavailable`), no value ever recorded, and `configured` explicitly
      does not mean the credential can push (`docs/operations/doctor.md`)
- [x] A machine-readable record of the Python versions the suite is verified on, the way
      `tests/git-versions.json` records git versions (`tests/python-versions.json`, T-0032)
- [x] `doctor` compares this VM's git and interpreter against both records
      (T-0033), reporting `exercised` / `NOT exercised` / `record unreadable` /
      `no record` with the matched entry's own scope attached, so an unexercised
      VM is warned rather than undocumented and an unreadable record cannot read
      as a failing machine
- [x] CI runs one row per CPython minor from 3.8 to 3.14, and the matrix is held
      to the exercised-version record (`tests/test_ci_matrix.py`, T-0034, D035,
      `FAILURES.md` F018). The gap was real rather than theoretical: running the
      suite on the five unrecorded interpreters failed on all five, on a test
      that asserted a fact about the record instead of about the code. The five
      gates that read files stay on one row, guarded explicitly
- [x] The identifier rule reads every source of definitions, through one entry
      point both publishing gates call (`tools/originlib/idcheck.py`, T-0036,
      defect 10). Rule 7 did not read the numbered list in `STATE-defects.md`, so
      two VMs took defect 7 in an hour and both copies reached the base with each
      VM's own tree internally consistent. It also reports a list it cannot read,
      because a parser that stops matching looks like a clean tree
- [x] The same rule reads the third source of a decision identifier — the
      `Decisions **…**` header under each record's title (T-0042, defect 14,
      D036). Two of the five records were false while every gate passed, with
      both index rows in `DECISIONS.md` correct throughout, and one record named a
      `D011–D018` range covering exactly the entries that had moved out of it. The
      rule is compared as identifier sets, and a header it cannot read is reported
- [x] The two index checks live one per record — `findingindex` for `FAILURES.md`,
      `decisionindex` for `DECISIONS.md` — with `identifiers` keeping what a
      definition is and whether one number means two things (T-0043). Two VMs each
      added to `identifiers.py` from a different hour, each stayed under the cap
      alone, and the merge concatenated them to 307 of 300: run `37189825232` red on
      all seven rows, and `observed` from the public annotations
- [x] An experiment number a mission record restates is held to the artifact it names
      (`tools/originlib/resultnumbers.py`, T-0056, D047, defect 22, F024).
      `docs/process/experiment-protocol.md` claimed `113/113` checked cases for an artifact
      whose `cases_with_oracle` is 115 — wrong in the commit that published the artifact, with
      every gate green. **The obvious rule is blind to it**: "does this number occur anywhere in
      the artifact?" answers *yes*, since `113` also sits at `patch_cost_sensitivity/*/cases`. So
      the rule decides the property from the number's *shape*, and
      `tests/test_result_numbers_falsified.py` asserts that blindness.
- [ ] Seed tasks from `STATE.md` next actions
- [ ] Headless task-runner script for VMs, once a VM exists
- [ ] Scheduling or supervision, once unattended execution is authorised

## Sequencing note

The infrastructure track finished ahead of stage B because stage B is blocked on judgement
rather than tooling. Kill gates exist for the three held candidates, ten experiments have
run, and none has validated a claim. Stage B is blocked on what no experiment here can
answer: whether a knitter follows a generated repair plan, and whether E3's builder-level
finding generalises beyond the one builder this machine has. E2's time-gated drift
comparison is scheduled (side A banked, T-0019).

What remains in tooling is *fleet* work, not invention work: the exercised-version
records exist and `doctor` reads them (T-0033), and every
CPython minor from 3.8 to 3.14 has now run the suite (T-0034, D035). The floor claim is
still two things it is not: it says nothing about 3.15 onwards, and a green row is
evidence about that row and not the version below it. Git is weaker in kind, a git
version being a property of a machine rather than of a workflow step: T-0034 added the runner's own 2.55.0 to the record by running the suite on it, and
`git-versions.json` names what it does **not** run against (2.26-2.54 and 2.57+). A suite that only passes where its author works is not a suite, and that is a
recorded pattern rather than a coincidence: the interpreter assertion failed on every version the
record lacked (F018), the git assertion on every runner whose git nobody recorded (F019), and the
credential fixture on every runner exporting `GITHUB_TOKEN` (T-0035). Each was green where it
was written.
Identifiers are allocated from the shared base and the record is printed (T-0031), so a
stale tree no longer collides — but two VMs allocating between their own fetches still do, and
T-0030's detector catches that. A red CI run is diagnosable without admin rights, the check-run
annotations naming the failing test and public all along (F020, T-0038); what is left is that
the endpoint answers "nothing" in three different ways, one a 403 from the unauthenticated rate
limit. T-0020 is the pattern for the rest: run the documented sequence, and fix what it does.
- [x] A red gate step names the file it rejected (`tools/origin annotate`, T-0040,
      defect 17). The five file-reading steps ran a gate, printed a report and exited, so
      the check run's only annotation was "Process completed with exit code 2" and the log
      that says which rule failed needs admin rights. A violation now carries the file and
      line its own rule knows; falsified against `e53ca23`'s own bytes in both directions,
      and `observed` on run `37196459285` filing all seven. The same session found the
      workflow's awk escaping `%` wrongly, and four CLI handlers raising a `Usage` they had
      never imported — all in [`STATE-defects.md`](STATE-defects.md).
- [x] A diagnostic step runs whenever the job runs, and a probe measures it on the same run
      (T-0046, defect 18, F021, D038). An `if:` naming no status function gets an implicit
      `success()`, so a red `Tests` step skipped all five gate steps on two runs. `always() &&`
      on each, plus `tools/origin probe`: one annotation per rendering shape on every push
- [x] A refusal is followable by the tool that gave it (T-0048, D039,
      `tools/originlib/landrebase.py`). `sync land` stopped on a real conflict and said *resolve
      it and land again*; the second `land` refused on the dirty tree that resolving leaves, so
      the only way out was a hand-run `git rebase --continue`, which records no `base_advance` —
      defect 2's ceiling reached through a message rather than a mistake. `land` now completes
      the rebase and reads the pre-rebase tip from git's own `orig-head` rather than a `HEAD`
      already moved onto the base. Falsified both ways
- [x] A command's own write is declared by the bytes it wrote, whatever its suffix (T-0050, D042,
      F022). `reconcile` asked the *line cap's* exemption predicate, true for every `.json`,
      `.jsonl` and `.log`, so the undeclared-change report skipped every data-file edit — including
      the version records that decide whether a VM can run the work. The two questions are named
      separately now and reconciliation asks its own; the claim ledger and `vendor/hashes.json` are
      declared by their writers' bytes. Priced **before** the repair by
      `tools/sweep_unlogged_data.py`: 72 (session, path) pairs over 17 paths, 50 the ledger. The
      general form: an exemption is a claim about what another check covers, and the cheap way to
      write one is to borrow a predicate.
- [x] A claim is publishable from inside the session that made it (T-0055, D044, defect 21,
      F023). `task claim` committed the claim then called `push`, which refuses a dirty tree —
      and an open session guarantees one, so the refusal named the session's own record and told
      the agent to commit or revert it. The claim stayed local and unpushed, so **no other VM
      could see it**: the exclusivity the command exists to provide was not in force, and each
      retry added another `claim` line to the ledger (three identical ones for T-0053). Falsified
      both ways, and on a clone of this repository's own history
- [x] Standard-library test suite (575 tests on git 2.25.1), with
      [`tests/git-versions.json`](tests/git-versions.json) recording how much of the suite
      each git version has actually run. A test's correctness depends on every clock the code
      under it reads: three tests behind the in-flight gate read one the fixture never handed
      over, so one assertion expired on a schedule and could never pass again (T-0044, defect 15)

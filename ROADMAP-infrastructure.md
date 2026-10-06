# Infrastructure track

<!-- origin-meta
owner: ROADMAP.md
status: active
last-verified: 2026-10-06
-->

Split out of [`ROADMAP.md`](ROADMAP.md) on 2026-10-06 at its 300-line cap, **by
invariant**: this is everything the mission needs before an invention stage can
run at all, and it is tracked separately from the invention stages for exactly
that reason. The stages live in [`ROADMAP.md`](ROADMAP.md).

Separate from the invention stages: the mission cannot be run without it.


- [x] Session logging with append-only events and git reconciliation, with attribution
      by recorded evidence: a base move the tooling performed (D028), and a command's own
      write, honoured only while the file holds those bytes (T-0047, D040)
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
- [x] Identifier allocation from the shared base for F, D and T, with the record it was
      read from printed by every command that hands out a number
      (`tools/originlib/idalloc.py`, `origin id next`, T-0031); twelve collisions between
      two VMs in two days were the cost of allocating from a working tree instead
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
- [x] `doctor` reports the push credential mechanism (T-0029): the configured helper, whether
      each named helper exists and runs, App key files by path and mode, whether the helper
      depends on anything outside `~/.config`, and whether `git credential fill` obtains a
      credential. Three-valued, no value ever recorded, and `configured` does not mean it can push
      (`docs/operations/doctor.md`)
- [x] A machine-readable record of the Python versions the suite is verified on, the way
      `tests/git-versions.json` records git versions (`tests/python-versions.json`, T-0032)
- [x] `doctor` compares this VM's git and interpreter against both records
      (T-0033), reporting `exercised` / `NOT exercised` / `record unreadable` /
      `no record` with the matched entry's own scope attached, so an unexercised
      VM is warned rather than undocumented
- [x] CI runs one row per CPython minor from 3.8 to 3.14, and the matrix is held
      to the exercised-version record (`tests/test_ci_matrix.py`, T-0034, D035,
      `FAILURES.md` F018). Running the suite on the five unrecorded interpreters
      failed on all five, on a test that asserted a fact about the record instead
      of about the code
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
- [ ] Seed tasks from `STATE.md` next actions; a headless task-runner once a VM exists

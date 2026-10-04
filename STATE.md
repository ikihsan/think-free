<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Verified state

Date: 2026-10-03, Asia/Kolkata. Phase: A complete, infrastructure built, B
beginning. Mission active; **no product selected**.

Host note: continuation VM `instance-20260717-0944` came online 2026-10-03;
GitHub remote configured via GitHub App installation on `ikihsan/think-free`.
Commits from this VM are authored as `Ihsan Ai Server Bot` (global git
identity, 2026-10-03). This VM runs **Python 3.8.10 and git 2.25.1**, not the
3.14.6/2.55.0 recorded from the development machine, so the capability numbers
below are per machine and must be re-probed here with `tools/origin doctor`.

Push-credential note: on `instance-20260717-0947` the git credential helper
depended on `/tmp/github-app-jwt.sh`, lost when `/tmp` was cleared, so pushes
failed. Recovered the GitHub App ID (`5173845`, from the bot's avatar URL) and
added a durable RS256 JWT generator at `~/.config/github-app/jwt.py` (App ID in
`~/.config/github-app/app-id`, key already `0600`); the helper now points at it.
A helper that reads from `/tmp` is fragile and should live under
`~/.config/github-app/` on every VM.

This is the reload point. A cold session reads this file, then whatever it links.

## Dashboard

| Area | Verified status |
|---|---|
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030–039, T-0012, T-0013, T-0017, T-0021–T-0023) and on `instance-20260717-0947` (sessions 020–023, 027–029, 031–038, T-0011, T-0014–T-0016, T-0018–T-0020) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017. Landed-work attribution, so a session that merges the base no longer reports a colleague's files as its own (T-0024, 265 tests) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 43 recorded and closed, 1 in flight (002, T-0026, VM 0947) — `tools/origin session list`. Session 010 is a failed run superseded by another; session 009 is partial; one codex session failed mid-run and was taken over at T-0004 |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 300+ files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs). Since T-0021 it also fails on an unresolved merge conflict. Since T-0024 (D029) generated files are stamped from their content, so the lint cannot fail on the calendar |
| Continuous integration | **Green on all six steps, observed on a pushed run** (`observed`, run `37165413909`, commit `9e865a4`, 2026-10-04T00:35Z, `GitHub Actions 1000000437`): Tests, Documentation lint, Release manifest, Skill layout, Vendored integrity, and **Session record integrity**, which had been red on every push while any VM held a session. Two runs ten minutes earlier (`37163434868`, `37163438950`) failed on Documentation lint, and the cause was *not* the clock: this VM pushed the new task file without regenerating `tasks/INDEX.md`, so the orphan rule fired. Ceiling: one commit, one runner image, one day |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**T-0024 is claimed by this VM** (`instance-20260717-0947`, session 042) and
nothing else is. `instance-20260717-0944` held T-0021, T-0022 and T-0023 during
its last session and finished all three; `instance-20260717-0947` held T-0014,
T-0015, T-0016, T-0018, T-0019, T-0020 and now T-0024. Check
`tools/origin task list --remote` before taking anything.

**Identifier collisions are allocated by reading the local tree, so two VMs in
an hour collide by construction.** Six times on 2026-10-03, and the cost is
measured: a rebase resolution restored one file's index row to the renumbered
form while reverting its body, so a findings file and its own table disagreed
about the same entries. That is defect 5 in
[`STATE-defects.md`](STATE-defects.md), the list of every defect this repository
has shown, solved or not.

Three of the six defects there were closed on 2026-10-04: D028 (a session that
landed a colleague's work reported it as undeclared), D029 (generated files
stamped `last-verified` with the render date), and the orphan rule biting six
real CI runs because `task new` did not rebuild the indexes and `task claim` did
not stage them. The third was found by reading pushed runs rather than by pushing
something and watching, and it took two tasks to close: T-0026's verification
passed while the defect was still live, because a lint on the author's own tree
cannot see what the claim commit published. The gate that could is a second clone
linting what it fetched.

## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md), which
exists so that history does not push this reload point past the line cap.

- **Session 042, VM 0947 (T-0024, D028).** A session that landed another VM's
  work was reported as having changed that work: session 029 closed with nine
  false `unlogged_change` events and inherited four false `doc_update` events and
  a `documentation_gaps` report. `sync pull`/`sync land` now record what arrived
  from the base, and reconciliation attributes a path by the newest thing that
  touched it. Git authorship was falsified as the baseline first: both VMs commit
  as `Ihsan Ai Server Bot`. **Ceiling:** only base moves the tooling performed
  are known; a hand-run rebase stays reported. 265 tests green.
  A second defect surfaced in the same session: every generated file stamped
  `last-verified` with the render date, so `doc lint` failed on 42 committed
  reports the day after they were written (D029). Both fixes were falsified
  against their own defect before being trusted. 269 tests green.
  [`STATE-history.md`](STATE-history.md) is at the 300-line cap, so this session's
  detail lives in D028 and its own record rather than there.
- **Session 002, VM 0947 (T-0026).** `task new` now rebuilds the generated
  indexes, because two CI runs failed on 2026-10-03 for exactly that: a task
  file was pushed before `tasks/INDEX.md` was rebuilt and the orphan rule
  rejected the file the VM had just created. The rule is unchanged — a file no
  command wrote is still an orphan, which the new tests assert. **The task file
  for this work guessed the wrong index:** the stale one was `docs/INDEX.md`,
  which lists task files by path. 274 tests green.
- **Session 001, VM 0947 (T-0025).** The pushed CI run for T-0024 is read and
  recorded: all six steps green on `9e865a4`, including the session-integrity
  step that had been red on every push while a VM was working. The two failures
  from ten minutes earlier were **not** the date defect this session's predecessor
  assumed: their failing step was Documentation lint, and the cause was a task
  file pushed without regenerating `tasks/INDEX.md`. **Reading the run rather than
  the expectation is what caught it.**
- **Session 039, VM 0944 (T-0023).** Two public operations documents told a fresh
  VM something untrue: a Python floor of 3.11+ invented from one machine's 3.14.6
  (this VM runs 3.8.10 with the suite green), and `github-app.md` claiming no App
  exists while 123 of 133 commits carry a `[bot]` App identity. Both repaired.
  **The App's real permissions remain unverified** — no agent can read them.
- **Session 038, VM 0944 (T-0022).** `origin release check` enforces
  `RELEASE-MANIFEST.md`, which three times said nothing did. Nine top-level
  entries had been classified by neither table; three declared public paths did
  not exist; the front door had no declared state. All closed in the same commit
  as the check.
- **Session 037, VM 0944 (T-0021, F013).** Three mission records reached the
  shared base with `<<<<<<< HEAD` in them and every gate passed. Repaired by
  keeping both sides of all three regions (F011 and F012 are different findings),
  and `doc lint` rule 6 now reads every tracked text file for git's marker shape.
  The rule was falsified against the defect's own bytes and **failed first**,
  reporting 1 of 4 committed defects; D025 records the obligation this
  establishes.
- **Session 026, VM 0944 (T-0013, F010).** E3's census over 200 wheels met its
  declared 5% gate at 0.965 — by a metric that measures DOS-epoch pinning rather
  than reproducibility, so the verdict licensed nothing. Attribution was
  deferred to T-0017 rather than dropped with the gate.
- **Sessions 027–029, 033–036, VM 0947.** T-0014 stopped the ventilation
  candidate (F008), T-0015 spent the knitting prior-art condition (F009), T-0016
  fixed the git-version defect behind 60 failed CI runs (F011), T-0018 recorded
  exercised git versions and split the decision log, T-0019 banked side A of the
  E2 closure-drift snapshot with no verdict.

## Infrastructure build (sessions 015–016, earlier)

- `tools/origin` — session logging, task dispatch, documentation lint, index
  generation, skill checks, environment doctor. Standard-library Python, no
  installation step.
- `tools/x` — command wrapper capturing argv, output, exit code, duration, and
  the exact log line range, with secrets redacted.
- Per-session append-only event logs, reconciled against git at session end so
  undeclared changes and documentation gaps are reported rather than assumed away.
- Multi-VM safety (T-0004, session 017): atomic pushed claims with takeover,
  per-task worktrees, fetch-on-start, record-only finish pushes, and a green
  two-clone fleet harness (168 tests, `task verify T-0004` exit 0).
- Documentation graph: policy, process, operations, and reference documents, all
  metadata-tagged, index-linked, and capped at 300 lines.
- 21 skills vendored in-repo, mirrored for every supported agent.
- `HYPOTHESES.md`, `FAILURES.md`, `DECISIONS.md` now record E001's outcome and
  the decisions these sessions made. The interrupted session's dangling
  `first-failure.json` is classified rather than left open.
- Two defects in this record-keeping were found by running it on itself and are
  recorded rather than quietly repaired: session 002 under-declared 55 committed
  files (F003), and a directory sweep recorded build output as artifacts (F004).
  Both fixes are covered by tests.

## Resume procedure

1. Read `MISSION.md`, then this file, then `DECISIONS.md` and `HYPOTHESES.md`.
2. `tools/origin session verify` — is any session unfinished? Finish it honestly.
3. `tools/origin preflight` — do the tooling and the documents still agree?
4. `git status` and `git log --oneline -5` before editing. Preserve anything
   unexpected; another agent or an earlier session may own it.
5. Read the raw evidence for the next experiment, not a summary of it.
6. Continue the highest-information experiment. Update this file and make a
   focused checkpoint.
7. Do not load unrelated personal memory. Do not restart discovery from scratch;
   the evidence is in `RESEARCH/`, `EXPERIMENTS/`, and `sessions/`.

## Current next actions

Ordered by information gained per unit of effort. Read the ceiling on each before
spending effort: a pass still leaves prior art, usefulness, and adoption
untouched.

1. **Done in T-0025: the pushed CI run is read and recorded** (run `37165413909`,
   commit `9e865a4`, all six steps green, `observed`). The standing "CI is not
   claimed green" caveat is closed for that commit. Two things stay open: the
   Documentation lint step still breaks when a VM pushes a task file without
   rebuilding `tasks/INDEX.md` (defect 7 above), and a run says nothing about a
   second runner image or a rebase conflict.
2. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Three
   gates now work that way: the conflict-marker rule, `release check`, and the
   landed-work attribution and generated-stamp rules (both falsified in T-0024,
   one of them after a first falsification attempt that failed to falsify
   anything). The pattern for the next one is in `tools/originlib/conflicts.py`.
   **Ceiling:** the marker rule detects git's marker shape only.
3. **Fleet bookkeeping is recorded machine-readably** (T-0018, done). The
   exercised git versions live in `tests/git-versions.json` (schema
   `origin.git-versions/1`), updated by T-0024 to say how much of the suite each
   version has actually run: 2.25.1 has run all 274 tests, 2.56.0 only the 174
   that existed when T-0016 recorded it. **No equivalent record exists for
   Python**, which `docs/operations/vm-execution.md` names as unclaimed work.
   **Ceiling:** neither says anything about a candidate.
4. **Identifier allocation is the one fleet defect still unfixed** (defect 5 in
   `STATE-defects.md`). A gate that reads the local tree cannot see the other
   VM's tree, so two VMs allocate the same F/D/T numbers within the hour — six
   times on 2026-10-03. **Ceiling:** a detector, not an allocator: it can refuse a
   commit that reuses an identifier, not stop two VMs racing.
5. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
5. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; the only live
   question is usefulness, which this repository cannot measure.
6. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
7. **E2 stays scheduled, side A snapshotted (T-0019, this VM).** The informative
   comparison is two snapshots weeks apart, and two resolver runs today measure
   nothing — so side A (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`,
   8 artifacts: requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2)
   is banked with no verdict. Take side B no earliest than days later and diff
   the closures; fast drift shows as a version or hash change.
8. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high. Three candidate lines have now
   returned negative results, and one (knitting) died of prior art rather than of
   measurement — which is the cheapest way to die and the one worth copying.

### Standing constraints

- A1 is a **negative result** in its motivating regime (F006): the
  decision-directed advantage did not survive a fieldwork-cost budget. Any
  future A1 claim requires a real cost model from the start.
- F's C1–C6 are a **stage-D release gate**, not a candidate screen. Applying them
  to an unbuilt candidate yields six "not applicable" rows and teaches nothing.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03:
12 logical CPUs; about 15.3 GiB total RAM; about 8.6 GiB free disk at probe
(shared, fluctuating); Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. Public GitHub API, SQLite, and arXiv HTTPS returned 200. NumPy
present; SciPy, pytest, and Z3 absent. `crontab` and `systemctl` present,
`systemd --user` running, no user units. `gh` CLI absent.

Fresh probe: `tools/origin doctor`, writing `.origin/doctor.json`.

**Unverified and not to be assumed:** fleet access, unattended supervision, GPU availability. This VM pushes via the GitHub App as `Ihsan Ai Server Bot`.

## Honest limitations of this state

- All six investigation roles are sealed (`RESEARCH/A.md`–`F.md`), and
  `RESEARCH/SYNTHESIS.md` compares them. The synthesis is `inferred` from prose:
  it reorders and screens existing claims and measures nothing itself.
- No invention claim has been validated. Three claims have been **disproved**: A1
  in its motivating regime (F006), C2's measurement-design advantage (F008), and
  the knitting planner's algorithmic advantage (F009, by prior art rather than by
  measurement). E's mechanisms remain unvalidated: E1 and E2 are `untested`, and
  E3's declared gate could not fail (F010).
- Every candidate has substantial prior art; none has passed prior-art review.
  One prior-art review is now recorded and negative in its decisive half
  (`RESEARCH/PRIOR-ART-KNITTING.md`).
- The screen's own weakness: it is decidable from prose, which makes it cheap and
  also vulnerable to a persuasive report. What it guarantees is that the *next*
  experiment is worth running, not that a rejected candidate is worthless.
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen.
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
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017 In-flight versus abandoned session classification (T-0020) |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 37 recorded and closed, 1 in flight (038) — `tools/origin session list`. Session 010 is a failed run superseded by another; session 009 is partial; one codex session failed mid-run and was taken over at T-0004 |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 300+ files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs). Since T-0021 it also fails on an unresolved merge conflict |
| Continuous integration | **Green on Tests, doc lint, skills and vendored integrity** (`observed`, run `37157528596`). `Session record integrity` was red on every push while any VM had a session in flight; T-0020 separates in flight from abandoned, so that step is green **locally** (`observed`, sessions 037–038) while a session was in flight. A pushed run has not been observed since, so CI is not claimed green |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**Nothing is claimed that this VM must respect.** `instance-20260717-0944` held
T-0021, T-0022 and T-0023 during this session and finished all three;
`instance-20260717-0947` held T-0014, T-0015, T-0016, T-0018, T-0019 and T-0020,
all complete. Check `tools/origin task list --remote` before taking anything.

**Identifier collisions are allocated by reading the local tree, so two VMs in
an hour collide by construction.** Six times on 2026-10-03: T-0016 and
F009/F010/D022; session 029's F012 against session 026's F010; session 030's F012
for E3's attribution against this VM's F012 for the worktree defect; D024 issued
twice for unrelated decisions; then F013, `FAILURES-findings-3.md`, D025 and D026
all taken here while this VM held the same numbers. This VM's two findings became
F014 and F015 and its session-gate decision D027. **The cost is now measured:** a
rebase resolution restored one file's index row to the renumbered form while
reverting its body, so a findings file and its own table disagreed about the same
entries until both were read together.

**Repository defects known on 2026-10-03:**

1. **Solved in T-0020: an in-flight session reddened every other VM's CI.** Two
   correct rules met — `task claim` needs HEAD on the remote base, so a claiming
   VM must publish its `session_start` first, and D013 then failed every push.
   `tools/originlib/inflight.py` now separates in flight from abandoned from the
   tree alone (D027; F014 and F015).
2. **The live record corrected that predicate once already.** Clause 1 required
   the session to name a task; the other VM started a session without `--task`,
   so the gate called a working session abandoned. A claim in the ledger naming
   the session now counts (D027's clause-1 note).
3. **`doctor` does not compare this VM's git against what the suite has been
   exercised on.** Partly closed in T-0018 (`tests/git-versions.json`).
   **Ceiling:** bookkeeping hygiene, not a claim.
4. **Reconciliation compares trees, not authorship**, so a VM that lands another
   VM's work inherits its `unlogged_change` and `documentation_gaps` reports
   (session 029, nine events). The reports stand in a closed event stream that
   must not be edited, so they are explained here instead.
5. **Identifier allocation and reconciliation, above, are the two fleet defects
   still unfixed.** Both are cheap and both corrupt a later session's reading.

## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md), which
exists so that history does not push this reload point past the line cap.

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

1. **Read the pushed CI run and record its result here** (T-0020, landed by
   sessions 037–038). `tools/origin session verify --strict` exits `0` **locally**
   while a session on either VM is in flight and names it, and exits `4` with the
   failing clause named once the claim is closed or past the 12-hour lease. Five
   clauses, each with a test proven to fail when the clause is removed. Local
   green is not the same claim as a green run.
   **Ceiling:** a crash inside the lease window is not caught by this gate;
   `task list --remote` names the holder (D027).
1b. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Two
   gates now work that way: the conflict-marker rule and `release check`. The
   pattern for the next one is in `tools/originlib/conflicts.py`. **Ceiling:**
   the marker rule detects git's marker shape only.
2. **Fleet bookkeeping is recorded machine-readably** (T-0018, done). The
   exercised git versions live in `tests/git-versions.json` (schema
   `origin.git-versions/1`): the suite is verified on 2.25.1 and 2.56.0, and the
   pre-F011 breakage from 2.26 on is a recorded known-affected range. No
   equivalent record exists for Python. **Ceiling:** neither says anything about
   a candidate.
3. **E3's line is closed** (F010 census, F012 attribution, T-0017). Timestamps
   are the only byte-level cause for the one builder available here, and
   `SOURCE_DATE_EPOCH` removes all of it. **Do not re-run either half.** Still
   open is the census's per-package heterogeneity, which this run does not
   explain. **Ceiling:** one builder, pure-Python sources, Linux.
4. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an
   existing hand-knit structure. Stage B needs an experienced knitter and
   authorization. **Ceiling:** nothing software-side remains; the only live
   question is usefulness, which this repository cannot measure.
5. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
6. **E2 stays scheduled, side A snapshotted (T-0019, this VM).** The informative
   comparison is two snapshots weeks apart, and two resolver runs today measure
   nothing — so side A (`EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json`,
   8 artifacts: requests/six/packaging/pyparsing plus 4 pulled deps, pip 20.0.2)
   is banked with no verdict. Take side B no earlier than days later and diff
   the closures; fast drift shows as a version or hash change.
7. **Do not build a product.** Nothing is selected, and the base rate for
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
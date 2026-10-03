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
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, 030, 037, 038, T-0012, T-0013, T-0017, T-0021, T-0022) and on `instance-20260717-0947` (sessions 020–023, 027–029, 033–036, T-0011, T-0014, T-0015, T-0016, T-0018, T-0019, T-0020) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010); `008-build-timestamp-attribution` complete (398 of 398 differing bytes are timestamp fields, `SOURCE_DATE_EPOCH` gives bit-identical builds — mechanism supported, candidate abandoned, F012) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous; F011 `sync land` broke on git >= 2.26, so every CI run failed; F012 E3's ordering claim holds and that is why there is nothing to build; F013 three mission records were committed with conflict markers and every gate passed. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), one declared gate shown not to be able to fail (F010), and one mechanism confirmed whose candidate died of the confirmation (F012). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F012 in `FAILURES-findings-2.md`, F013+ in `FAILURES-findings-3.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, release-manifest enforcement, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017 |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door and `origin release check` now enforces it (T-0022); nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 37 recorded and closed, 1 in flight (038) — `tools/origin session list`. Session 010 is a failed run superseded by another; session 009 is partial; one codex session failed mid-run and was taken over at T-0004 |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 300+ files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs). Since T-0021 it also fails on an unresolved merge conflict |
| Continuous integration | **Green on Tests, doc lint, skills and vendored integrity** (`observed`, run `37157528596`). The `Session record integrity` step is red while any VM has a session in flight on the shared branch. A sixth step, `release check`, is added by T-0022 and **has not yet run on CI** |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**T-0022 is claimed by opencode on `instance-20260717-0944`** — implementing
`origin release check`, so `RELEASE-MANIFEST.md` is enforced by a machine rather
than by review. Its session `2026-10-03-038-implement-origin-release-check-so-releas`
is in flight, so the CI strict-session gate is red while it runs. **T-0020 is
claimed by opencode on `instance-20260717-0947`** — telling an in-flight session
apart from an abandoned one, which is what that red gate needs. Do not start
either. T-0021 is complete: three corrupted mission records repaired, and the
gate that detects them added (F013).

Note for whoever picks up T-0020: its declared `verify` command includes
`session verify --strict`, which cannot pass while its own session is open
(D026). T-0022 hit the same wall and corrected its own task file before running
it.

Nothing else is claimed. T-0012 and T-0013 and T-0017 are `instance-20260717-0944`'s;
T-0014, T-0015, T-0016, T-0018 and T-0019 are `instance-20260717-0947`'s and
complete.

**Identifier collisions are being allocated by reading the local tree, so two
VMs in the same hour collide by construction.** Twice on 2026-10-03: T-0016 and
F009/F010/D022 all went to two different sessions, and both renumbered before
pushing (D023, and this session's F011). The renumbering is manual and happens
*after* the fact, which is how a finding ends up described in the wrong place.

**Repository defects known on 2026-10-03**, none of them claimed:

1. **CI's own gates are green** (`observed`, run `37157528596`): Tests,
   Documentation lint, Skill layout, and Vendored integrity all pass on commit
   `b9991bde`. The one red step is `Session record integrity` (exit 4) while
   `instance-20260717-0944` has a session in flight on the shared branch. The
   underlying defect — `git rebase --continue` being interactive from git 2.26,
   which broke `origin sync land` on any modern-git VM — is fixed and recorded as
   `FAILURES.md` F011.
2. **An in-flight session on the shared branch reddens every other VM's CI.**
   D013 wants CI strict, and the fleet practice of committing a session's start
   makes an unfinished session visible on the base branch. Open question, not a
   defect: see next action 1.
3. **Nothing compares a VM's git version against what this repository has been
   exercised on.** `tools/origin doctor` does record it (`git --version`, in
   `.origin/doctor.json` and in its printed summary), so the gap is not
   recording. The gap is that `EXPERIMENTS/000-capabilities/` and this file's
   capability paragraph were copied between VMs without being re-probed, and no
   gate states which git versions the sync flow has actually run against — which
   is how F011 went unnoticed for a session on a repository that was printing
   the answer. **Ceiling:** this is bookkeeping hygiene, not a claim.
4. **Nothing detected a committed merge conflict** (F013, fixed in T-0021, so
   this is a closed entry kept for the record): every gate read those files for a
   different property and none read the markers. `doc lint` rule 6 does now.
5. **Nine top-level entries were published or withheld by accident** (fixed in
   T-0022): `RELEASE-MANIFEST.md` had no row for `.agents/`, `.github/`,
   `.gitignore`, `RELEASE-MANIFEST.md`, `STATE-history.md`,
   `HYPOTHESES-results.md` or the three `FAILURES-findings*.md`, and no way to
   declare an absent path on purpose. `origin release check` now fails on both.
   **Ceiling:** it enforces agreement between the manifest and `README.md`, not
   the truth of either.
5. **Session 029 closed with nine `unlogged_change` events that are not its
   own.** `tools/origin sync land` rebased that session's branch onto
   `instance-20260717-0944`'s pushed work, so `EXPERIMENTS/007-build-timestamps/`,
   `HYPOTHESES.md`, `HYPOTHESES-results.md`, `RESEARCH.md`,
   `DECISIONS-PRACTICE.md`, `tasks/T-0013-…` and `tasks/T-0017-…` appeared in its
   working tree. Their own sessions declare those files, and a closed event
   stream must not be edited to say so, so the report stands unexplained in the
   log and is explained here instead. The same mechanism recorded those files as
   session 029's `doc_update`s: **reconciliation compares trees, not
   authorship**, so a VM that lands another VM's work inherits its
   `documentation_gaps` and `unlogged_change` reports.
6. **`DECISIONS-PRACTICE.md` was within a few lines of the cap** — resolved in
   T-0018 by splitting it by invariant: mechanics (D011–D012, D014–D018) stay,
   verification and judgement (D013, D019–D026) live in
   `DECISIONS-GATING.md`.

T-0008 (`003-information-sufficiency`, session 020 on VM 0947) completed the
information-sufficiency gate for the three held candidates. Witness W1 (sidewalk
survey) and W3 (ventilation) survive; W2 (knitting) found the stated input set
information-insufficient (F007). T-0010 (session 022, VM 0947) then ran the
knitting Stage-A comparison, T-0011 (session 023, VM 0947) closed it, T-0014
(session 027, VM 0947) stopped the ventilation candidate (F008), T-0015
(session 028, VM 0947) spent the knitting prior-art condition (F009), and
session 026 on VM 0944 spent E3's declared census gate (F010). T-0004 (multi-VM
safety, session 017) is green: fleet/sync suite passing, flow documented across
process/operations/reference docs, AGENTS.md, and the two skills — with the git
version exception recorded in F011.

## What changed recently

Full detail per session is in [`STATE-history.md`](STATE-history.md), which
exists so that history does not push this reload point past the line cap.

- **Session 038, VM 0944 (T-0022).** `origin release check` now enforces
  `RELEASE-MANIFEST.md`, which three times said nothing enforced it. Seven
  top-level tracked entries had been classified by neither table; three paths
  declared public did not exist; the public front door had no declared state.
  All three gaps are closed in the same commit that added the check, and the
  check found a credential-shaped fixture in its own new test file, which is
  how D012's waiver mechanism earns its second use.
- **Session 037, VM 0944 (T-0021, F013).** The shared base carried three
  corrupted mission records — `FAILURES.md`, `FAILURES-findings-2.md`, and
  `DECISIONS-GATING.md` — with `<<<<<<< HEAD` in them from commit `fd7b4a1`, and
  every gate passed. Repaired by keeping both sides of all three regions (F011
  and F012 are different findings), and `doc lint` rule 6 now reads every
  tracked text file for git's conflict-marker shape. The rule was falsified
  against the defect's own bytes and **failed first**, reporting 1 of 4 committed
  defects; D025 records the obligation this establishes.
- **Session 026, VM 0944 (T-0013, F010).** E3's census over 200 wheels met its
  declared 5% gate at 0.965 — by a metric that measures DOS-epoch pinning rather
  than reproducibility, so the verdict licensed nothing. Attribution was
  deferred to T-0017 rather than dropped with the gate.
- **Sessions 027–029, 033–036, VM 0947.** T-0014 stopped the ventilation
  candidate (F008), T-0015 spent the knitting prior-art condition (F009), T-0016
  fixed the git-version defect behind 60 failed CI runs (F011), T-0018 recorded
  exercised git versions and split the decision log (D025's file), T-0019 banked
  side A of the E2 closure-drift snapshot with no verdict.

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

1. **CI is green on every gate a commit controls; one gate is red by design —
   and T-0020, claimed by `instance-20260717-0947`, owns the fix.**
   `observed`, run `37157528596` on commit `b9991bde`: Tests **success**,
   Documentation lint **success**, Skill layout and mirrors **success**,
   Vendored content integrity **success**, Session record integrity **failure**
   (exit 4) — because a session is in flight on the shared branch. That is the
   whole of the remaining red, and it is the D013 rule meeting the fleet's
   practice, not a defect in the change under test. Read as a *warning* it keeps
   D013's intent (a crashed run must not look successful) while stopping one
   VM's in-flight work from reddening everyone else's push. Do not start this
   while T-0020 holds it.
1b. **A gate must read the property it claims to check, and must be falsified
   against the defect's own bytes before it is trusted** (D025, from F013). Two
   gates now work that way: the conflict-marker rule and `release check`. The
   pattern for the next one is in `tools/originlib/conflicts.py`. **Ceiling:**
   the marker rule detects git's marker shape only.
2. **Fleet bookkeeping is recorded machine-readably** (T-0018, done). The
   exercised git versions live in `tests/git-versions.json` (schema
   `origin.git-versions/1`): the suite is verified on 2.25.1 and 2.56.0, and the
   pre-F011 breakage from 2.26 on is a recorded known-affected range.
   **Ceiling:** none of this says anything about a candidate.
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
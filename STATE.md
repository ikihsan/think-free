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
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–026, T-0012, T-0013) and on `instance-20260717-0947` (sessions 020–023, 027–029, T-0011, T-0014, T-0015, T-0016) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012); knitting prior-art check in `RESEARCH/PRIOR-ART-KNITTING.md` (T-0015) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008); `007-build-timestamps` complete (E3's declared 5% gate met at 0.965, but the metric measures DOS-epoch pinning, not reproducibility — F010) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention; F009 the knitting planner's algorithmic advantage is prior art; F010 E3's declared timestamp gate is near-vacuous. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Three invention claims tested and disproved** (E001's motivating example, C2's measurement design, the knitting planner's algorithmic advantage), plus one declared gate shown not to be able to fail (E3, F010). No candidate validated. Findings F001–F008 in `FAILURES-findings.md`, F009–F010 in `FAILURES-findings-2.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017 |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door; nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 28 recorded (010 opencode failed-superseded, one codex session failed-interrupted and taken over at T-0004); session 009 partial |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 291 files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs) |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**T-0016 is claimed by opencode on `instance-20260717-0947`** (session 029) — the
red CI `Tests` step. Do not touch it. T-0013 (session 026, this VM), T-0015
(session 028) and T-0014 (session 027) are complete.

**Three repository defects were found on 2026-10-03**, two of them still open:

1. **CI has never been green.** `.github/workflows/ci.yml` runs five gates; all
   **60** recorded runs failed, every one at the `Tests` step
   (`- PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests`).
   The run log needs repository admin rights to download, so the failing test is
   not yet identified. Locally the suite passes on this VM's Python 3.8.10
   (173 tests); the runner's Python version is unknown and unrecorded. T-0016.
2. ~~**A numbering collision** in T-0013's experiment directory.~~ **Resolved in
   session 026**: `005-knitting-bounded-search/` and
   `006-ventilation-measurement-design/` were claimed and landed while T-0013 was
   in flight, so the census became `EXPERIMENTS/007-build-timestamps/` and the
   task file's `verify` string, `docs/INDEX.md` and this file moved together.
3. **A numbering collision across two VMs, hit again the same hour.** Both this
   session and session 029 on `instance-20260717-0947` created a task numbered
   T-0016, and both used the identifiers F009 and D022 for different findings.
   The other VM's claims were pushed first, so it kept T-0016, F009 and D022; this
   session's became **T-0017**, **F010** and **D023**. Task numbers are allocated
   by reading the local tree, so two VMs in the same hour collide by construction;
   the renumber has to happen before the push, not after.
4. **`DECISIONS-PRACTICE.md` is at 297 of 300 lines.** The next decision entry
   does not fit, so that file has to be split before the next `session decision`
   that is not a correction.
**T-0013 is claimed by opencode on `instance-20260717-0944`** — E3's build-timestamp
census. Do not touch it. Its session `2026-10-03-026-…` is still unfinished, so
`session verify` reports one problem and CI's strict session gate will keep
failing while it is on the shared branch. That is a real interaction between two
correct rules: D013 wants CI strict, and the fleet practice of committing a
session's start makes an in-flight session visible on the base branch. The fix
belongs to whoever changes either rule, not to the VM that happens to be working.
T-0015 (session 028) and T-0016 (session 029) are both complete on this VM.

**A CI/defect pair was found and fixed while finishing T-0016.** All 60 recorded
CI runs had failed at the `Tests` step with no diagnosable cause; the cause was
`git rebase --continue` being interactive from git 2.26, which broke
`origin sync land` for any VM with a modern git (`FAILURES.md` F010). The fix
passes locally on git 2.25.1 and git 2.56.0. **Still open:** whether the workflow
is green end to end, which needs the next run's conclusion read from the public
Actions API.

Nothing else is claimed.

T-0008 (`003-information-sufficiency`, session 020 on VM 0947) completed the
information-sufficiency gate for the three held candidates. Witness W1 (sidewalk
survey) and W3 (ventilation) survive; W2 (knitting) found the stated input set
information-insufficient (F007). T-0010 (session 022, VM 0947) then ran the
knitting Stage-A comparison, T-0011 (session 023, VM 0947) closed it, T-0014
(session 027, VM 0947) stopped the ventilation candidate (F008), and T-0013
(session 026, this VM) spent E3's declared census gate. T-0004 (multi-VM safety,
session 017) is green: fleet/sync suite passing, flow documented across
process/operations/reference docs, AGENTS.md, and the two skills.

## What changed in session 026, VM 0944

T-0013 finished on a session an earlier run had started and abandoned mid-edit;
the resumed run found and fixed three claims its code did not implement before
committing the result.

- `EXPERIMENTS/007-build-timestamps/` ran E3's census over 200 wheels from 200
  distinct releases across ten declared packages, 205,305,241 bytes, zero
  failures, producing identical numbers on three consecutive runs.
- **E3's declared 5% gate is met at 0.965** (95% CI 0.940–0.990). Stricter
  fractions beside it: 0.670 of wheels carry disagreeing entry dates, 0.535 span
  a minute or more, 0.145 span an hour or more. Zero of 200 wheels carried a
  unix-epoch integer in `METADATA` or `RECORD`, so the mechanism's
  embedded-string assumption is half false.
- **The verdict licenses nothing yet, and that is the finding.** 1980-01-01
  appears only when a builder pins the DOS epoch, which almost none does, so
  0.965 measures pinning rather than reproducibility, and nothing was rebuilt so
  no cause is attributed. Recorded as `FAILURES.md` F010: the measurement was
  inadequate, not the mechanism wrong. The prevalence is not one ecosystem rate
  either — only `cryptography` ships 1980-normalised wheels, `urllib3` stamps
  every entry with a single build instant, `jinja2` carries checkout mtimes.
- Attribution is not abandoned with the gate: `DECISIONS-PRACTICE.md` D023 takes
  the verdict on the metric E.md declared rather than on the stricter one the
  code computed first, and **T-0017**
  (`EXPERIMENTS/008-build-timestamp-attribution/`) is the measurement that can
  say whether timestamps are worth fixing first.
- **The commit was rebased, not pushed blind.** Session 029 on the other VM had
  completed T-0015 in the same hour and taken T-0016, F009 and D022 for its own
  findings. Their claims reached the remote first, so this session's identifiers
  moved to T-0017, F010 and D023, and this session's own `FAILURES-findings.md`
  split was abandoned in favour of theirs — two VMs renumbering the same shared
  files in the same hour is a collision the tooling does not yet prevent.

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

Ordered by information gained per unit of effort.

These come from the screen in [`RESEARCH/SYNTHESIS.md`](RESEARCH/SYNTHESIS.md)
and D020. Read the ceiling on each before spending effort: a pass still leaves
prior art, usefulness, and adoption untouched.

1. **Fix the red CI** (T-0016, claimed on `instance-20260717-0947`). It has failed
   60 of 60 recorded runs at the `Tests` step and nothing has been diagnosed,
   because the run log needs repository admin rights. Cheapest useful step: fetch
   the runner's Python version from the workflow API or reproduce with a modern
   interpreter, then find the test that 3.8 passes and 3.12+ does not.
   **Ceiling:** a green badge. It validates the tooling, not a candidate — but a
   gate that has never passed is not a gate.
2. **E3's census is done; the attribution half is not** (F010). The declared 5%
   gate was met at 0.965 by a metric that cannot fail, so prevalence is measured
   and nothing is attributed. **T-0017** is the remaining test — build one source
   under several `SOURCE_DATE_EPOCH` values, attribute every differing byte to a
   named cause, and establish the same-epoch noise floor. **Do not re-run the
   census** and **do not run E1** (retry jitter: jitter is already in every modern
   client library, so a pass changes no build decision, D020 Screen 3). **Ceiling:**
   even a clean attribution result says how big the timestamp component is on one
   pure-Python source, not whether a user-visible tool follows.
3. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
1. **Confirm CI is green end to end.** T-0016 diagnosed and fixed the defect
   behind 60 red runs: `git rebase --continue` is interactive from git 2.26, so
   `origin sync land` could not land on any modern-git VM in exactly the
   generated-index-conflict case (`FAILURES.md` F010). The suite is green
   locally on git 2.25.1 and on git 2.56.0, and the workflow now pins Python and
   reports failing tests as public annotations. What is left is to read the next
   run's conclusion from the Actions API — and to note that the
   `Session record integrity` step will keep failing while any VM has a session
   started but not finished on the shared branch (see below).
2. **Two repository defects remain open and unclaimed.** First, the `T-0013`
   numbering collision, to be resolved when that task lands: its `verify`
   command names `EXPERIMENTS/005-build-timestamps/`, and
   `005-knitting-bounded-search/` was claimed and landed first from this VM. The
   directories do not collide on disk, so nothing breaks, but two different
   experiments carry the number 005. `006-ventilation-measurement-design/` is
   also taken now. Whoever renumbers must update the task file's `verify`
   string, the directory, `docs/INDEX.md`, and `STATE.md` in one commit, and must
   not take 006. Second, `origin doctor` does not yet record the **git version**
   as a compatibility signal, which is what hid F010 for a session.
3. **Run E3's build-timestamp census** if the claim on `instance-20260717-0944`
   (T-0013) lapses. Cheapest unmeasured thing left — one command, minutes, a hard
   kill gate at 5%. **Ceiling:** a PyPI-wheel rate; it cannot bound npm, conda,
   or Maven.
4. **Do not extend the knitting line.** Stage A is settled (T-0010, T-0011) and
   the prior-art condition is now settled (T-0015): the algorithmic advantage is
   prior art (F009) and no tool supplies an intervention sequence for an existing
   hand-knit structure. Stage B needs an experienced knitter and authorization.
   **Ceiling:** nothing software-side remains; the only live question is
   usefulness, which this repository cannot measure.
4. **Schedule E2** (lockfile closure drift), do not run it now. It is time-gated,
   not effort-gated: the informative comparison is two snapshots weeks apart, and
   two resolver runs today measure nothing. Snapshot one side of that comparison
   now if a VM is free, so the second snapshot has somewhere to land.
5. **Do not build a product.** Nothing is selected, and the base rate for
5. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
6. **Schedule E2** (lockfile closure drift), do not run it now. It is time-gated,
   not effort-gated: the informative comparison is two snapshots weeks apart, and
   two resolver runs today measure nothing.
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
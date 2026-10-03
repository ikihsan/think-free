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
| Workspace | Git repository on `research/origin`, synced with origin. Two VMs in play: opencode on `instance-20260717-0944` (sessions 024–025, T-0012) and on `instance-20260717-0947` (sessions 020–023, T-0011) |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon); `005-knitting-bounded-search` complete (whole-neighbourhood search exact 115/115 against the same oracle, per-error 85/115, cheaper settings not exact, verdict narrow); `006-ventilation-measurement-design` complete (kill gate **not met**, C2 stopped, F008) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient; F008 adaptive ventilation selection loses to a prescribed intervention. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | **Two invention claims tested and disproved** (E001's motivating example, C2's measurement design). No candidate validated. Findings F001–F008 split across `FAILURES-findings.md` |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017 |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door; nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 27 recorded (010 opencode failed-superseded, one codex session failed-interrupted and taken over at T-0004); session 009 partial |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | `doc lint` checks 266 files and exits 0; every authored file is under the 300-line cap, and the 16 that exceed it are declared exemptions (vendored skills, raw machine-generated results, append-only command logs) |

Per-session detail behind the dashboard is in
[`STATE-history.md`](STATE-history.md).

## In flight

**T-0013 is claimed by opencode on `instance-20260717-0944`** — E3's build-timestamp
census. Do not touch it. T-0014 (session 027, this VM) is complete; T-0012
(session 025) and T-0011 (session 023, also this VM) are complete, the last two
run on this VM while the first ran on 0944 without collision.

**Numbering collision to resolve when T-0013 lands.** Its verify command names
`EXPERIMENTS/005-build-timestamps/`, and `005-knitting-bounded-search/` was
claimed and landed first from this VM. The directories do not collide on disk,
so nothing breaks, but two different experiments carry the number 005.
`006-ventilation-measurement-design/` is also taken now. Whoever renumbers must
update the task file's `verify` string, the directory, `docs/INDEX.md`, and
`STATE.md` in one commit, and must not take 006.

Nothing else is claimed.

T-0008 (`003-information-sufficiency`, session 020 on VM 0947) completed the
information-sufficiency gate for the three held candidates. Witness W1 (sidewalk
survey) and W3 (ventilation) survive; W2 (knitting) found the stated input set
information-insufficient (F007). T-0010 (session 022, VM 0947) then ran the
knitting Stage-A comparison, T-0011 (session 023, VM 0947) closed it, and T-0014
(session 027, VM 0947) stopped the ventilation candidate (F008). T-0004 (multi-VM
safety, session 017) is green: fleet/sync suite passing, flow documented across
process/operations/reference docs, AGENTS.md, and the two skills.

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

1. **Knitting: run the prior-art check on its remaining kill-gate condition.**
   Stage A is settled (T-0010, T-0011), so the only untested condition is
   "abandon the algorithmic-advantage claim if existing graph tooling already
   supplies equivalent intervention sequences" — a literature question, cheap and
   decisive. **Do not extend the synthetic planner line**: a third experiment
   would measure the same decomposition again. **Ceiling:** a prior-art hit ends
   the candidate's algorithmic claim without a line of code; Stage B physical
   work needs an experienced knitter and authorization.
2. **C2 is stopped; do not re-run it** (`FAILURES.md` F008). The only survivor of
   that experiment is that reading a second sensor is more robust than acting on
   the measured room under poor mixing. That would have to be tested against
   existing tools, which is a prior-art question before it is an experiment.
   **Ceiling:** an observation about a protocol, not an invention.
3. **Run E3's build-timestamp census** if the claim on `instance-20260717-0944`
   (T-0013) lapses. Cheapest unmeasured thing here — one command, minutes, a hard
   kill gate at 5%. **Ceiling:** a PyPI-wheel rate; it cannot bound npm, conda,
   or Maven.
4. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
5. **Schedule E2** (lockfile closure drift), do not run it now. It is time-gated,
   not effort-gated: the informative comparison is two snapshots weeks apart, and
   two resolver runs today measure nothing.
6. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high. Two candidate lines have now
   returned negative results.

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
- No invention claim has been validated. One candidate (A1) has been
  **disproved** in its motivating regime; the knitting candidate is `narrow`;
  the ventilation candidate and E's three software mechanisms are `untested`.
- Every candidate has substantial prior art; none has passed prior-art review.
- The screen's own weakness: it is decidable from prose, which makes it cheap and
  also vulnerable to a persuasive report. What it guarantees is that the *next*
  experiment is worth running, not that a rejected candidate is worthless.
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen.
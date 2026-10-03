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
| Workspace | Git repository on `research/origin`, synced with origin. Agent: opencode on instance-20260717-0944 |
| Investigations | A, B, C, D, E, F all sealed; cross-report screen in `RESEARCH/SYNTHESIS.md` (T-0012) |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met; `002-a1-masking` gate met with caveats; `003-information-sufficiency` complete (W1/W3 survive, W2 spec insufficient); `004-knitting-stage-a` complete (local planner valid 9/9, suboptimal on 1 shared-release case, verdict narrow-not-abandon) |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping; F005 local-only claims; F006 DD advantage does not transfer to fieldwork cost; F007 knitting planner input set information-insufficient. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | One invention claim tested and **disproved**. No candidate validated |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, doctor. Multi-VM sync, worktree isolation, and remote-truth claims completed and verified green in session 017 |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door; nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 20 recorded (010 opencode failed-superseded, one codex session failed-interrupted and taken over at T-0004); session 009 partial |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | 260 tracked files; every authored file is under the 300-line cap, and the 13 that exceed it are declared exemptions (vendored, raw results, append-only logs). `doc lint` exits 0 |

## In flight

**T-0011 is claimed by opencode on `instance-20260717-0947`** — the
bounded-neighbourhood knitting planner. Do not touch it. T-0012 completed in
session 025 (this VM).

Nothing else is claimed.

T-0008 (`003-information-sufficiency`, session 020 on VM 0947) completed the
information-sufficiency gate for the three held candidates. Witness W1 (sidewalk
survey) and W3 (ventilation) survive; W2 (knitting) found the stated input set
information-insufficient (F007). T-0010 (session 022, VM 0947) then ran the
knitting Stage-A comparison. T-0004 (multi-VM safety, session 017) is green:
fleet/sync suite passing, flow documented across process/operations/reference
docs, AGENTS.md, and the two skills.

## What changed in session 025, VM 0944

The screen `STATE.md` had been carrying as next action 3, run and recorded.

- `RESEARCH/SYNTHESIS.md` — all sixteen candidates from A–F in one table, three
  screens, and a ranked shortlist. Applying F's C1–C6 literally yields six
  "not applicable": they describe a built repository and cannot discriminate six
  unimplemented candidates. A third question does the work — *if the gate
  passes, what gets built* — and it is what rules out E1, the cheapest
  experiment in the repository, because jitter is already in every client
  library and a pass would confirm a 2015 blog post.
- Finding no single report contains: **every promoted candidate in A, B and C
  needs a person or a room this repository cannot reach** — a planner, an
  experienced knitter's hands, sensors in a room. Three tasks (T-0005/6/0007)
  bought A1 a falsification, not a decision. Only D, E and F proposed things
  testable on this machine, and D proposed nothing.
- `DECISIONS.md` reached the 300-line cap and was split by invariant into
  `DECISIONS-FOUNDATION.md` (mission, workspace, evidence) and
  `DECISIONS-PRACTICE.md` (recording, verifying, publishing, gating). Entries
  moved verbatim; numbering unchanged.
- D020 records the screen as a gate and keeps C1–C6 as a stage-D release check
  rather than a candidate screen that cannot fail.
- `reconcile.IMPLICATIONS` gained an explicit `any`/`all` mode per event kind, so
  the decision gate survives the split without weakening the `experiment_result`
  gate, which still demands both `HYPOTHESES.md` and `FAILURES.md`. Five new
  tests in `tests/test_doc_gaps.py`; 173 tests pass.
- Repaired two tracked documents that were false: `RESEARCH.md` and `ROADMAP.md`
  both described investigations E and F as "not run" although both are sealed
  and their tasks are done.

## What changed in session 020, VM 0947

- `EXPERIMENTS/003-information-sufficiency/` — one synthetic witness per held
  candidate, each stating two realities with identical permitted inputs and the
  required divergent output. W1 and W3 survive (an askable observation separates
  them); W2 is information-insufficient as specified. `task verify T-0008`
  exit 0.
- `HYPOTHESES.md` records the E002 gate and its per-candidate outcome;
  `FAILURES.md` F007 records the knitting input-set finding.
- Push credentialing repaired: App ID recovered, durable JWT generator added
  under `~/.config/github-app/`.

## What changed in the last session (session 022, VM 0947)

T-0010 completed: `EXPERIMENTS/004-knitting-stage-a/` runs the knitting
candidate's own Stage A. A cheap per-error local heuristic was compared
against an exhaustive minimum-cost oracle on 10 synthetic cases (9 solved, 1
refused). The heuristic is valid on all 9 solved cases (never misses an
error, never emits an illegal closure), refuses unsupported shaping, and is
suboptimal on exactly one constructed shared-release case (local 5 vs.
optimum 3) — the same_column_stack case a per-error rule cannot see. No
full-row-release degeneration. Verdict `narrow`, not `abandon`; next test is
a bounded-neighbourhood planner against the same oracle before Stage-B
physical work. `task verify T-0010` exit 0. Push credentials on this VM are
the durable `~/.config/github-app/` JWT helper from session 020.

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

1. **Run the ventilation measurement kill gate** (`RESEARCH/C.md`, "Smallest
   runnable falsification experiment"). Unclaimed and locally runnable: a
   two-room mass-balance simulator in stdlib Python, three protocols at one
   observation budget, paired parameter sets with near-identical passive traces,
   and held-out weather and mixing violations that break the estimator model.
   W3 already showed the mechanism is information-sufficient, so a result is
   possible at all — that is the only reason it is first. **Ceiling:** a pass
   means "mathematically possible on correctly specified synthetic models".
   E's rule 2 and C's own conclusion both say the right outcome on a pass is an
   extension to NIST or NVAPF, not a new repository.
2. **Run E3's build-timestamp census**, because it is the cheapest thing here —
   one command, minutes, a hard kill gate at 5% — not because it is promising.
   It closes the one E-mechanism whose experiment is both runnable today and
   genuinely unmeasured. **Ceiling:** a PyPI-wheel rate; it cannot bound npm,
   conda, or Maven.
3. **Do not run E1** (retry jitter). It is the cheapest experiment in the
   repository and the least informative: jitter is already in every modern
   client library, so a pass changes no build decision. D020, Screen 3.
4. **Schedule E2** (lockfile closure drift), do not run it now. It is time-gated,
   not effort-gated: the informative comparison is two snapshots weeks apart, and
   two resolver runs today measure nothing.
5. **Let T-0011 finish** — bounded-neighbourhood knitting planner, claimed on VM
   0947. Do not duplicate it.
6. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high.

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
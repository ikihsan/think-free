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
identity, 2026-10-03).

This is the reload point. A cold session reads this file, then whatever it links.

## Dashboard

| Area | Verified status |
|---|---|
| Workspace | Git repository on `research/origin`, 3 commits. No remote configured |
| Investigations | A, B, C, D sealed. E and F never ran |
| Experiments | `000-capabilities` complete; `001-photo-baseline` complete with its kill gate met |
| Disproved | F001 photo-auditor motivating example; F002 E001 parser failure (implementation, not hypothesis); F003 and F004, both defects in this session's own record-keeping. Six candidate areas rejected in `RESEARCH/D.md` and `RESEARCH/B.md` |
| Experimental validation | One invention claim tested and **disproved**. No candidate validated |
| Implemented | Session logging, task dispatch, documentation lint, index generation, secret scanning, doctor. 133 stdlib tests, all passing |
| Users and adoption | None. No product, no release, no claims |
| External release | None. `RELEASE-MANIFEST.md` defines the public front door; nothing published |
| Skills | 21 total: 14 vendored (Superpowers v6.2.0, MIT, hash-verified), 7 authored |
| Sessions | 4 recorded, 3 worked, 1 deliberately abandoned mid-way and kept in the log |
| Supervision | Interactive execution only. Unattended persistence **not verified** |
| Documentation | 183 tracked files; every authored file is under the 300-line cap, and the 7 that exceed it are declared vendored exemptions. `doc lint` exits 0 |

## What changed in the last session

Built the infrastructure the mission was missing, and folded the interrupted
session's findings into the record:

- `tools/origin` — session logging, task dispatch, documentation lint, index
  generation, skill checks, environment doctor. Standard-library Python, no
  installation step.
- `tools/x` — command wrapper capturing argv, output, exit code, duration, and
  the exact log line range, with secrets redacted.
- Per-session append-only event logs, reconciled against git at session end so
  undeclared changes and documentation gaps are reported rather than assumed away.
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

1. **Write kill gates for the three held candidates** in `HYPOTHESES.md`. No
   candidate may be tested before its gate exists. Highest priority: the
   decision-directed sidewalk survey, which `RESEARCH/A.md` recommends advancing.
2. **Run the A1 masking experiment.** Pin a commit of
   `OpenSidewalks/PLoS-cities-complex-systems`, extract one neighbourhood, hide
   curb and incline facts at random and in contiguous blocks, and compare
   decision-directed observation selection against centrality, missingness, and
   random heuristics at equal budget. Kill gate and acceptance threshold are
   written in `RESEARCH/A.md` step 5. Record whether a usable extract exists
   before investing in the comparison.
3. **Run investigations E and F.** The experimental-engineering and
   adoption-researcher roles have no sealed report, so the current candidate set
   comes from four perspectives and is missing two.
4. **Apply the information-sufficiency test** to the three held candidates. Ten
   lines of code each; it has already killed two proposals cheaply.
5. **Do not build a product.** Nothing is selected, and the base rate for
   agent-generated ideas with prior art is high.

## Capability evidence

`EXPERIMENTS/000-capabilities/results.json`, probed 2026-10-03:
12 logical CPUs; about 15.3 GiB total RAM; about 8.6 GiB free disk at probe
(shared, fluctuating); Python 3.14.6; Node 22.23.1; Rust 1.96.0; GCC 16.1.1;
`git` 2.55.0. Public GitHub API, SQLite, and arXiv HTTPS returned 200. NumPy
present; SciPy, pytest, and Z3 absent. `crontab` and `systemctl` present,
`systemd --user` running, no user units. `gh` CLI absent.

Fresh probe: `tools/origin doctor`, writing `.origin/doctor.json`.

**Unverified and not to be assumed:** authenticated GitHub writes, remote VM
fleet access, unattended supervision, GPU availability. No git remote is
configured; pushing requires the user's authorization per
`docs/policy/permissions-and-safety.md`.

## Honest limitations of this state

- One of two planned initial investigations is missing (E, F), so the candidate
  set rests on four perspectives.
- The one experiment that ran was a baseline check, not a candidate test. No
  invention claim has been validated.
- Every candidate has substantial prior art; none has passed prior-art review.
- The tooling's own coverage is demonstrated by its tests, not by independent
  reproduction. `tests/README.md` lists what is and is not covered.
- Unattended execution is not implemented. What exists is the record that makes an
  interrupted run recoverable, plus detection that reveals when it did not happen.
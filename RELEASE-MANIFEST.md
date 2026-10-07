<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Release manifest — what is public

This repository holds two different things: the **product** the mission is
trying to earn adoption for, and the **process record** that proves how it was
reached. Only the first belongs on a public front door. This file is the
authority on that split.

**Enforced by `tools/origin release check`** (T-0022), which parses the two
tables below. A path is one backticked token in the first cell of a row; a row
may hold several. Mark a declared path `(pending)` when it is expected to be
absent, and the check fails the moment it appears.

<!-- origin-release-state: no-public-product -->

## Public by default

| Path | Why |
|---|---|
| `README.md` | The front door. What it is, why it exists, how to run it. |
| `AGENTS.md` `CLAUDE.md` `GEMINI.md` | Agent entry points; part of the contribution story. |
| `LICENSE` (pending) | Required for a credible open-source release. Absent until a product is chosen. |
| `CONTRIBUTING.md` (pending) | Same; `AGENTS.md` is its foundation for now. |
| `CODE_OF_CONDUCT.md` (pending) | Same. |
| `docs/` | Policy, process, operations, reference. Shows the method is real. |
| `tools/` `tests/` | The infrastructure that makes claims reproducible. |
| `stage-lines/` | The first candidate artifact. Public because the experiment record cites it and its own tests are the correctness argument; its header says `status: draft`, so it is not presented as released. |
| `.agents/` `.claude/` `vendor/` | Canonical skills, their mirrors, and the licences they keep. |
| `.github/` | The CI gates that enforce those tests, and the agent entry point. |
| `.gitignore` | A credible repository ships its ignore rules. |
| `RELEASE-MANIFEST.md` | This file. Publishing the promise is part of keeping it. |

## Internal by default

| Path | Why it stays out |
|---|---|
| `sessions/` | Raw operational history of agent runs. Interesting to auditors, noise to users. |
| `tasks/` | Dispatch state for the VM fleet. Meaningless outside the mission. |
| `EXPERIMENTS/` `RESEARCH/` | Working notes, sealed reports, and raw experiment outputs. Cited, not published. |
| `MISSION.md` `STATE.md` `STATE-defects.md` `STATE-defects-2.md` `STATE-history.md` `STATE-history-2.md` `STATE-history-3.md` `STATE-next-actions.md` `STATE-next-actions-closed.md` `STATE-next-actions-closed-2.md` `STATE-selection.md` `STATE-in-flight.md` `STATE-in-flight-2.md` `STATE-in-flight-3.md` `STATE-in-flight-4.md` `STATE-constraints.md` `ROADMAP.md` `ROADMAP-infrastructure.md` | Mission control records. Honest to keep, distracting as a front door. |
| `DECISIONS.md` `DECISIONS-FOUNDATION.md` `DECISIONS-PRACTICE.md` `DECISIONS-SCREENING.md` `DECISIONS-SCREENING-2.md` `DECISIONS-SCREENING-3.md` `DECISIONS-SCREENING-4.md` `DECISIONS-SCREENING-5.md` `DECISIONS-SCREENING-6.md` `DECISIONS-SCREENING-7.md` `DECISIONS-SCREENING-8.md` `DECISIONS-SCREENING-9.md` `DECISIONS-SCREENING-10.md` `DECISIONS-SCREENING-11.md` `DECISIONS-SCREENING-12.md` `DECISIONS-GATING.md` `DECISIONS-SESSIONS.md` `DECISIONS-PUBLISHING.md` `DECISIONS-RECORDS.md` | The decision log, split by invariant. |
| `HYPOTHESES.md` `HYPOTHESES-results.md` `HYPOTHESES-results-2.md` `HYPOTHESES-results-3.md` `HYPOTHESES-candidates.md` `FAILURES.md` `FAILURES-findings.md` `FAILURES-findings-2.md` `FAILURES-findings-3.md` `FAILURES-findings-4.md` `FAILURES-findings-5.md` `FAILURES-findings-6.md` `FAILURES-findings-8.md` `FAILURES-findings-9.md` `FAILURES-findings-10.md` `FAILURES-findings-11.md` `FAILURES-findings-12.md` `FAILURES-findings-13.md` `FAILURES-findings-14.md`, `FAILURES-findings-15.md`, `FAILURES-findings-16.md`, `FAILURES-findings-17.md`, `FAILURES-findings-18.md`, `FAILURES-findings-19.md`, `FAILURES-findings-20.md`, `FAILURES-findings-21.md`, `FAILURES-findings-22.md`, `FAILURES-findings-23.md`, `FAILURES-findings-24.md`, `FAILURES-findings-25.md`, `FAILURES-findings-26.md`, `FAILURES-findings-27.md`, `FAILURES-findings-28.md`, `FAILURES-findings-30.md` | Candidate and failure records, split at the line cap. |
| `MISSION.md` `STATE.md` `STATE-defects.md` `STATE-defects-2.md` `STATE-history.md` `STATE-history-2.md` `STATE-history-3.md` `STATE-next-actions.md` `STATE-next-actions-closed.md` `STATE-next-actions-closed-2.md` `STATE-selection.md` `STATE-in-flight.md` `STATE-in-flight-2.md` `STATE-in-flight-3.md` `STATE-in-flight-4.md` `STATE-in-flight-5.md` `STATE-in-flight-6.md` `STATE-constraints.md` `ROADMAP.md` `ROADMAP-infrastructure.md` | Mission control records. Honest to keep, distracting as a front door. |
| `DECISIONS.md` `DECISIONS-FOUNDATION.md` `DECISIONS-PRACTICE.md` `DECISIONS-SCREENING.md` `DECISIONS-SCREENING-2.md` `DECISIONS-SCREENING-3.md` `DECISIONS-SCREENING-4.md` `DECISIONS-SCREENING-5.md` `DECISIONS-SCREENING-6.md` `DECISIONS-SCREENING-7.md` `DECISIONS-SCREENING-8.md` `DECISIONS-SCREENING-9.md` `DECISIONS-SCREENING-10.md` `DECISIONS-SCREENING-11.md` `DECISIONS-GATING.md` `DECISIONS-SESSIONS.md` `DECISIONS-PUBLISHING.md` `DECISIONS-RECORDS.md` | The decision log, split by invariant. |
| `HYPOTHESES.md` `HYPOTHESES-results.md` `HYPOTHESES-results-2.md` `HYPOTHESES-results-3.md` `HYPOTHESES-candidates.md` `FAILURES.md` `FAILURES-findings.md` `FAILURES-findings-2.md` `FAILURES-findings-3.md` `FAILURES-findings-4.md` `FAILURES-findings-5.md` `FAILURES-findings-6.md` `FAILURES-findings-8.md` `FAILURES-findings-9.md` `FAILURES-findings-10.md` `FAILURES-findings-11.md` `FAILURES-findings-12.md` `FAILURES-findings-13.md` `FAILURES-findings-14.md`, `FAILURES-findings-15.md`, `FAILURES-findings-16.md`, `FAILURES-findings-17.md`, `FAILURES-findings-18.md`, `FAILURES-findings-19.md`, `FAILURES-findings-20.md`, `FAILURES-findings-21.md`, `FAILURES-findings-22.md`, `FAILURES-findings-23.md`, `FAILURES-findings-24.md`, `FAILURES-findings-25.md`, `FAILURES-findings-26.md`, `FAILURES-findings-27.md`, `FAILURES-findings-28.md`, `FAILURES-findings-29.md` | Candidate and failure records, split at the line cap. |
| `RESEARCH.md` | Index for the sealed investigations. |

## Rules

1. A path not listed as public is **not** published. There is no wildcard, and
   `release check` fails one.
2. Promoting a path requires moving it here in the same commit that changes its
   audience. Nothing enforces that; review is the only gate.
3. Nothing internal may contain a secret, a private URL, or an unpublished
   third-party dataset path. `release check` scans every classified path for
   credential shapes; the rest is still review.
4. The public `README.md` must never describe unreleased behaviour as if it
   shipped. The decidable part of that is agreement: the
   `origin-release-state` directive above and the same directive in `README.md`
   must match, so publishing a product means changing both in one commit.

## What `release check` decides, and what it does not

It checks six properties: no wildcards; every tracked top-level entry classified
by exactly one table; a declared path exists unless marked `pending`, and a
`pending` one does not; no path sits inside a directory of the other audience; no
classified path holds credential-shaped text; and the two release states agree.

It does **not** decide whether the declared state is true, whether prose is
accurate, or whether a path deserves its classification. A manifest and a README
that agree on a false claim pass. That is agreement enforced, not truth.

It reads the same tracked set `doc lint` reads, which skips `.claude/` because
its entries are symlinks into `.agents/skills/`; `.claude/` is listed above
anyway, and its coverage is not machine-checked.

## Current state

**No public product exists.** The repository is a research and infrastructure
record only. `README.md` describes the mission and the tooling, and says plainly
that no product has been selected. Do not imply otherwise. Both files declare
`no-public-product`; the check fails if they ever disagree.

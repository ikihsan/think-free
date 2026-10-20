<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
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

<!-- origin-release-state: public-product -->

## Public by default

| Path | Why |
|---|---|
| `README.md` | The front door. What it is, why it exists, how to run it. |
| `AGENTS.md` `CLAUDE.md` `GEMINI.md` | Agent entry points; part of the contribution story. |
| `LICENSE` | Required for a credible open-source release. |
| `CONTRIBUTING.md` (pending) | Same; `AGENTS.md` is its foundation for now. |
| `CODE_OF_CONDUCT.md` (pending) | Same. |
| `docs/` | Policy, process, operations, reference. Shows the method is real. |
| `tools/` `tests/` | The infrastructure that makes claims reproducible. |
| `pyprovides/` | The pyprovides package, a prototype resolver for which PyPI distribution provides a given Python module; published on PyPI with MIT licence; source+docs tutorial in `README.md` |
| `pyfix.fish` `pyfix.zsh` | Shell integrations for pyprovides (zsh/fish); part of the pyprovides prototype. |
| `preflight/` | The preflight package, three checks on evaluation harness instruments; MIT-licensed prototype; built-in adapters for JSONL/CSV/YAML/XML; source+docs in `README.md` |
| `.agents/` `.claude/` `vendor/` | Canonical skills, their mirrors, and the licences they keep. |
| `.github/` | The CI gates that enforce those tests, and the agent entry point. |
| `.gitignore` | A credible repository ships its ignore rules. |
| `RELEASE-MANIFEST.md` | This file. Publishing the promise is part of keeping it. |

## Internal by default

| Path | Why it stays out |
|---|---|
| `sessions/` | Raw operational history of agent runs. Interesting to auditors, noise to users. |
| `tasks/` | Dispatch state for the VM fleet. Meaningless outside the mission. |
| `SESSION_OUTCOME.json` | A single session's outcome summary, written at the repository root on 2026-10-15 and tracked by that session's commit. Same class as `sessions/`: operational history, and its content is already in `sessions/` and `EXPERIMENTS/`. Classified here rather than left as the one path `release check` could not account for. |
| `EXPERIMENTS/` `RESEARCH/` `stage-lines/` | Working notes, sealed reports, and raw experiment outputs. Cited, not published. |
| `MISSION.md` `STATE.md` `STATE-defects.md` `STATE-defects-2.md` `STATE-history.md` `STATE-history-2.md` `STATE-history-3.md` `STATE-next-actions.md` `STATE-next-actions-closed.md` `STATE-next-actions-closed-2.md` `STATE-next-actions-closed-3.md` `STATE-next-actions-sweep-history.md` `STATE-selection.md` `STATE-in-flight.md` `STATE-in-flight-2.md` `STATE-in-flight-3.md` `STATE-in-flight-4.md` `STATE-in-flight-5.md` `STATE-in-flight-6.md` `STATE-in-flight-7.md` `STATE-in-flight-8.md` `STATE-in-flight-9.md` `STATE-dashboard.md` `STATE-constraints.md` `ROADMAP.md` `ROADMAP-infrastructure.md` | Mission control records. Honest to keep, distracting as a front door. |
| `DECISIONS.md` `DECISIONS-FOUNDATION.md` `DECISIONS-PRACTICE.md` `DECISIONS-SCREENING.md` `DECISIONS-SCREENING-2.md` `DECISIONS-SCREENING-3.md` `DECISIONS-SCREENING-4.md` `DECISIONS-SCREENING-5.md` `DECISIONS-SCREENING-6.md` `DECISIONS-SCREENING-7.md` `DECISIONS-SCREENING-8.md` `DECISIONS-SCREENING-9.md` `DECISIONS-SCREENING-10.md` `DECISIONS-SCREENING-11.md` `DECISIONS-SCREENING-12.md` `DECISIONS-SCREENING-13.md` `DECISIONS-SCREENING-14.md` `DECISIONS-SCREENING-15.md` `DECISIONS-SCREENING-16.md` `DECISIONS-SCREENING-17.md` `DECISIONS-SCREENING-18.md` `DECISIONS-SCREENING-19.md` `DECISIONS-SCREENING-20.md` `DECISIONS-GATING.md` `DECISIONS-SESSIONS.md` `DECISIONS-PUBLISHING.md` `DECISIONS-RECORDS.md` `DECISIONS-RECORDS-2.md` `DECISIONS-PYTESTIVE-SUMMARY.md` | The decision log, split by invariant. |
| `HYPOTHESES.md` `HYPOTHESES-results.md` `HYPOTHESES-results-2.md` `HYPOTHESES-results-3.md` `HYPOTHESES-candidates.md` `HYPOTHESES-candidates-2.md` `HYPOTHESES-experiments.md` `FAILURES.md` `FAILURES-findings.md` `FAILURES-findings-2.md` `FAILURES-findings-3.md` `FAILURES-findings-4.md` `FAILURES-findings-5.md` `FAILURES-findings-6.md` `FAILURES-findings-8.md` `FAILURES-findings-9.md` `FAILURES-findings-10.md` `FAILURES-findings-11.md` `FAILURES-findings-12.md` `FAILURES-findings-13.md` `FAILURES-findings-14.md`, `FAILURES-findings-15.md`, `FAILURES-findings-16.md`, `FAILURES-findings-17.md`, `FAILURES-findings-18.md`, `FAILURES-findings-19.md`, `FAILURES-findings-20.md`, `FAILURES-findings-21.md`, `FAILURES-findings-22.md`, `FAILURES-findings-23.md`, `FAILURES-findings-24.md`, `FAILURES-findings-25.md`, `FAILURES-findings-26.md`, `FAILURES-findings-27.md`, `FAILURES-findings-28.md`, `FAILURES-findings-29.md` `FAILURES-findings-30.md` `FAILURES-findings-31.md` `FAILURES-findings-32.md` `FAILURES-findings-33.md` `FAILURES-findings-34.md` `FAILURES-findings-35.md` `FAILURES-findings-36.md` `FAILURES-findings-37.md` `FAILURES-findings-38.md` `FAILURES-findings-39.md` `FAILURES-findings-40.md` `FAILURES-findings-41.md` `FAILURES-findings-42.md` `FAILURES-other-vm.md` `FAILURES-reopening.md` | Candidate and failure records, split at the line cap. |
| `DECISIONS-RECORDS-3.md` `DECISIONS-RECORDS-4.md` `DECISIONS-RECORDS-5.md` `DECISIONS-RECORDS-6.md` `DECISIONS-SCREENING-21.md` `DECISIONS-SCREENING-22.md` `HYPOTHESES-candidates-3.md` `FAILURES-findings-43.md` `FAILURES-findings-44.md` `FAILURES-findings-45.md` `FAILURES-findings-46.md` `FAILURES-findings-47.md` `STATE-in-flight-10.md` `STATE-next-actions-d083-sweep.md` `STATE-next-actions-sessions.md` | Later splits of the same records; same class as the rows above, added as the files appeared. |
| `CLASSIFICATION-PROTOTYPE.md` `E197_RECIPIENT_READ_SUMMARY.md` `EXTENSIONS` `PROTOCOL-E172.md` `SESSION_OUTCOME.jsonl` `SESSION_OUTCOME_SUMMARY.json` `SESSION_SUMMARY.md` `session-outcome-summary.md` `session-record-E142.json` `checked-output.jsonl` `experiment_t0094_results.json` `github-screen-minimal-results.json` `hackage-viewcount-library-100.jsonl` `hackage-viewcount-library-30.jsonl` `hackage-viewcount-library-50.jsonl` `analyze_models.py` `explore_comtrade.py` `explore_comtrade2.py` `explore_fec.py` `explore_fec2.py` `explore_grants.py` `explore_grants2.py` `explore_nih.py` `explore_nih10.py` `explore_nih2.py` `explore_nih3.py` `explore_nih4.py` `explore_nih5.py` `explore_nih6.py` `explore_nih7.py` `explore_nih8.py` `explore_nih9.py` `explore_nsf.py` `explore_nsf2.py` `explore_nsf3.py` `explore_nsf_sbir.py` `explore_propublica.py` `explore_propublica2.py` `explore_propublica3.py` `improved_procedure.py` `regcheck.py` `test_prototype.py` `raw_recipient` | Scratch scripts, harvested API payloads and session-outcome drafts that landed at the repository root during uncommitted runs; internal working state cited by experiment records, never a front door. |
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
5. The `origin-release-state` directive must be `public-product` when any
   public product path is promoted, and `no-public-product` when no public
   product exists.

## What `release check` decides, and what it does not

It checks six properties: no wildcards; every tracked top-level entry classified
by exactly one table; a declared path exists unless marked `pending`, and a
`pending` one does not; no path sits inside a directory of the other audience;
no classified path holds credential-shaped text; and the two release states agree.

It does **not** decide whether the declared state is true, whether prose is
accurate, or whether a path deserves its classification. A manifest and a README
that agree on a false claim pass. That is agreement enforced, not truth.

It reads the same tracked set `doc lint` reads, which skips `.claude/` because
its entries are symlinks into `.agents/skills/`; `.claude/` is listed above
anyway, and its coverage is not machine-checked.

## Current state

**preflight is a public product candidate.** The `preflight/` package exists at the root with a working stdlib-only implementation, 16 passing tests, built-in adapters for JSONL/CSV/YAML/XML, and a validated adapter pattern across 6 harness formats. The `pyprovides/` package is also a public prototype. Both are MIT-licensed with source and documentation. The repository still describes the mission and tooling honestly: neither has a user base or adoption claims. The `origin-release-state` directive in both this file and `README.md` is `public-product`; the check fails if they ever disagree.

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

No tool validates it yet: `origin` has no `release` command, so these tables are
maintained by hand and reviewed, not enforced. Until a `release check` exists,
a path listed as public here is a human claim rather than a machine guarantee.

## Public by default

| Path | Why |
|---|---|
| `README.md` | The front door. What it is, why it exists, how to run it. |
| `AGENTS.md` `CLAUDE.md` `GEMINI.md` `.github/copilot-instructions.md` | Agent entry points; part of the contribution story. |
| `LICENSE` `CONTRIBUTING.md` `CODE_OF_CONDUCT.md` | Required for a credible open-source release. |
| `docs/` | Policy, process, reference. Shows the method is real. |
| `tools/` `tests/` | The infrastructure that makes claims reproducible. |
| `.agents/skills/` `.claude/skills/` `vendor/` | Skills other agents can reuse, with licences intact. |
| Product source and its tests | Not created yet. Added here when it exists. |

## Internal by default

| Path | Why it stays out |
|---|---|
| `sessions/` | Raw operational history of agent runs. Interesting to auditors, noise to users. |
| `tasks/` | Dispatch state for the VM fleet. Meaningless outside the mission. |
| `RESEARCH/` `EXPERIMENTS/` | Working notes, sealed reports, and raw experiment outputs. Cited, not published. |
| `MISSION.md` `STATE.md` `DECISIONS.md` `DECISIONS-FOUNDATION.md` `DECISIONS-PRACTICE.md` `DECISIONS-GATING.md` `HYPOTHESES.md` `FAILURES.md` `ROADMAP.md` `RESEARCH.md` | Mission control records. Honest to keep, distracting as a front door. |

## Rules

1. A path not listed as public is **not** published. There is no wildcard.
2. Promoting a path requires moving it here in the same commit that changes its
   audience. Nothing enforces this yet; review is the only gate.
3. Nothing internal may contain a secret, a private URL, or an unpublished
   third-party dataset path. `tools/origin session artifact` refuses known
   secret shapes and the session log redacts them, but no release-time scan
   exists.
4. The public `README.md` must never describe unreleased behaviour as if it
   shipped. If the product does not exist yet, the README says so.

## Current state

**No public product exists.** The repository is a research and infrastructure
record only. `README.md` currently describes the mission and the tooling, and
says plainly that no product has been selected. Do not imply otherwise.
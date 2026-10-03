<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Repository map

What lives where and why. `docs/INDEX.md` lists every document; this file
explains the shape of the tree.

## Zones

| Path | Contents | Mutability | Public |
|---|---|---|---|
| Root records | Mission, state, decisions, hypotheses, failures, roadmap | Hand-edited, one writer | Per `RELEASE-MANIFEST.md` |
| `AGENTS.md` | Canonical agent contract | Rarely edited | yes |
| `CLAUDE.md` `GEMINI.md` `.github/copilot-instructions.md` | Pointers to `AGENTS.md` | Rarely edited | yes |
| `docs/` | Policy, process, operations, reference | Hand-edited | yes |
| `sessions/` | Append-only event log, generated reports, raw command logs | Never hand-edited | no |
| `tasks/` | Task definitions and the append-only claim ledger | Task files hand-edited | no |
| `RESEARCH/` | Sealed independent investigation reports | Sealed once written | no |
| `EXPERIMENTS/` | Runnable experiments with raw results | Append-only per experiment | no |
| `tools/` | `origin` CLI, `x` wrapper, `originlib` package | Hand-edited and tested | yes |
| `tests/` | Standard-library test suite | Hand-edited with the code | yes |
| `.agents/skills/` | Canonical skills, authored and vendored | Vendored part is frozen | yes |
| `.claude/skills/` | Per-skill symlinks into `.agents/skills/` | Generated | yes |
| `vendor/` | Licences, provenance, vendored hashes | Rarely edited | yes |
| `.github/workflows/` | CI | Rarely edited | yes |

## Why the root records stay at the root

The mission contract names `MISSION.md`, `STATE.md`, `DECISIONS.md`,
`HYPOTHESES.md`, `FAILURES.md`, `ROADMAP.md`, and `RESEARCH.md` as the durable
memory, and `STATE.md` is the reload point for a cold session. Keeping them at
the root means the recovery instruction is one path, in every document that
mentions it. Moving them would buy tidiness at the cost of every reference.

## Naming conventions

| Kind | Pattern | Example |
|---|---|---|
| Session directory | `YYYY-MM-DD-NNN-slug` | `2026-10-03-002-build-infrastructure` |
| Experiment | `0NN-slug` | `001-photo-baseline` |
| Task | `T-NNNN-slug.md` | `T-0001-close-e001-decision.md` |
| Skill | `kebab-case` matching frontmatter `name` | `session-lifecycle` |
| Research report | single letter | `RESEARCH/A.md` |

## The generated files

Exactly four kinds of file are generated. All carry
`<!-- generated-by: origin … -->`, and `doc lint` fails if the committed content
differs from a fresh render.

| File | Produced by |
|---|---|
| `docs/INDEX.md` | `origin doc index` |
| `sessions/INDEX.md` | `origin doc index` |
| `tasks/INDEX.md` | `origin doc index` |
| `sessions/<id>/README.md` | `origin session finish` |

Edit the source, never the output.

## Two sources of truth, kept separate

**The event stream** is authoritative for what happened:
`sessions/<id>/events.jsonl`, append-only.

**The documents** are authoritative for conclusions: `HYPOTHESES.md`,
`DECISIONS.md` (with its four split siblings `DECISIONS-FOUNDATION.md`,
`DECISIONS-PRACTICE.md`, `DECISIONS-SCREENING.md`, and
`DECISIONS-GATING.md`), `FAILURES.md`, `STATE.md`.

They are cross-checked rather than merged. `session finish` reports a gap when a
decision was recorded but no decision record changed. A mismatch means one of
the two is stale, and the fix is to correct whichever is wrong, not to soften the
check.

## Where to add what

| Adding | Goes in | Must be linked from |
|---|---|---|
| A rule about how work is done | `docs/policy/` or a skill | `docs/INDEX.md` |
| A procedure | `docs/process/` | `docs/INDEX.md` |
| Something about running this repository or another machine | `docs/operations/` | `docs/INDEX.md` |
| A schema, table, or command reference | `docs/reference/` | `docs/INDEX.md` |
| An independent investigation | `RESEARCH/` | `RESEARCH.md` |
| An experiment | `EXPERIMENTS/0NN-slug/` | `EXPERIMENTS/PLAN.md` |
| A unit of work | `tasks/` via `origin task new` | `tasks/INDEX.md` (generated) |
| A reusable behaviour | `.agents/skills/` | `docs/reference/skill-inventory.md` |
| A finding | `HYPOTHESES.md` or `FAILURES.md` | root record set |

## What is not here yet

No product source code. The mission has not selected a product, and nothing in
this tree implies otherwise. `RELEASE-MANIFEST.md` reserves the paths a product
will occupy, and `README.md` says plainly that none exists.

No `vendor/` directory beyond the one vendored skill set. Adding material means
adding provenance, a licence, and a hash manifest in the same commit.
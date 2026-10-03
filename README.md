# think-free

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

An independent invention mission, and the infrastructure that keeps its reasoning
honest and recoverable.

**No product exists yet.** Nothing here has been released, and no user has used
anything in this repository. What exists is a research record and the tooling
that makes it checkable: four sealed investigations, one completed baseline
experiment, and a session/documentation system designed so that a claim cannot
outlive the evidence behind it.

Read [`STATE.md`](STATE.md) for the verified current state.
[`MISSION.md`](MISSION.md) states the objective, the boundaries, and the
stopping rules.

## What this repository is for

Discover, invent, implement, and grow an unusually useful open-source project,
with evidence that survives outside the agent that produced it. The
authoritative record is files in git, not conversation context.

Three properties are enforced mechanically rather than promised:

- **Nothing is fabricated.** Every claim is labelled `observed`,
  `source-supported`, `inferred`, `speculative`, or `untested`. See
  [`docs/policy/evidence-labels.md`](docs/policy/evidence-labels.md).
- **Every session is recorded.** An append-only event log, reconciled against
  git at the end of each session so that undeclared changes become visible. See
  [`docs/process/session-protocol.md`](docs/process/session-protocol.md).
- **Every document is bounded and connected.** No file over 300 lines, every
  document linked from an index, broken links and stale generated files fail the
  linter. See [`docs/policy/doc-standards.md`](docs/policy/doc-standards.md).

## Documentation

Start at [`docs/INDEX.md`](docs/INDEX.md): every document, grouped, with its
owning index and what it is for.

| I want to | Read |
|---|---|
| Know where things stand | [`STATE.md`](STATE.md) |
| Work on this repository as an agent | [`AGENTS.md`](AGENTS.md) |
| Understand the rules | [`AGENTS.md`](AGENTS.md), then [`docs/INDEX.md`](docs/INDEX.md) |
| See what was investigated | [`RESEARCH.md`](RESEARCH.md), [`RESEARCH/`](RESEARCH/) |
| Reproduce an experiment | [`EXPERIMENTS/PLAN.md`](EXPERIMENTS/PLAN.md) |
| Reconstruct a session | [`sessions/`](sessions/) |
| Pick up a unit of work | [`tasks/INDEX.md`](tasks/INDEX.md) |
| Run this on another machine | [`docs/operations/bootstrap.md`](docs/operations/bootstrap.md) |
| Understand what will be public | [`RELEASE-MANIFEST.md`](RELEASE-MANIFEST.md) |

## Tooling

Standard-library Python and bash. No installation step, no dependencies.

```bash
tools/origin doctor                      # what can this machine do?
tools/origin preflight                   # lint, skills, session integrity
tools/origin session start --goal "…"    # begin a recorded session
tools/x -- python3 -m unittest discover -s tests -t tests
tools/origin doc lint                    # documentation gates
```

Full reference: [`docs/reference/cli-reference.md`](docs/reference/cli-reference.md).
Tests: [`tests/README.md`](tests/README.md).

## Skills

Twenty-one skills are vendored in-repo so no agent needs to install anything.
They work in Claude Code, Codex, Gemini, Cursor, and OpenCode from a fresh clone.

Seven are authored to encode this repository's rules; fourteen are
[Superpowers](https://github.com/obra/superpowers) v6.2.0 by Jesse Vincent (MIT),
byte-identical to upstream. See
[`docs/reference/skill-inventory.md`](docs/reference/skill-inventory.md) and
[`vendor/MANIFEST.md`](vendor/MANIFEST.md).

## Status

| Area | State |
|---|---|
| Investigations | Four of six roles sealed (`RESEARCH/A.md`–`D.md`) |
| Experiments | Two complete: environment probe, and a baseline that disproved its own motivating example |
| Hypotheses | Candidates recorded, none selected |
| Product | None. Not started. |
| Users, adoption, stars | None. No claims. |
| Unattended execution | Not verified; see [`docs/operations/scheduling-and-supervision.md`](docs/operations/scheduling-and-supervision.md) |

## Licence

To be chosen when a product exists. The vendored skills keep their own licence;
see [`vendor/superpowers/LICENSE`](vendor/superpowers/LICENSE).

## Contributing

Not yet open. The agent contract in [`AGENTS.md`](AGENTS.md) describes how work is
done here, and will serve as the contributor guide's foundation once there is a
product to contribute to.
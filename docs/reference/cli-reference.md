<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# CLI reference

Every command the repository's tooling provides. Stdlib Python only, so no
installation step is needed on a fresh machine.

Wrapper scripts: `tools/origin` and `tools/x`. Both resolve the repository root
from their own location and work from any directory inside it.

## Exit codes

Part of the contract; CI and VM scripts branch on them.

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Usage error: bad arguments, no active session, unknown task |
| `2` | Lint violation, or a stale generated file |
| `3` | Verification ran and did not pass |
| `4` | Integrity violation: session record or vendored content is inconsistent |

## `session`

Records what a working session did. Protocol:
[`../process/session-protocol.md`](../process/session-protocol.md).

| Command | Effect |
|---|---|
| `session start --goal TEXT [--task ID] [--agent NAME]` | Fetches and fast-forwards onto the base, refuses a stale or dirty tree, then opens the single active session; records goal, agent, host, branch, starting commit, files already dirty |
| `session step TEXT` | Records a milestone |
| `session note TEXT` | Records an observation |
| `session decision TEXT [--refs ...]` | Records a decision; implies at least one of `DECISIONS.md`, `DECISIONS-FOUNDATION.md`, `DECISIONS-PRACTICE.md`, `DECISIONS-GATING.md` must change |
| `session experiment-result ID TEXT [--refs ...]` | Records an experiment outcome; implies `HYPOTHESES.md` and `FAILURES.md` must change |
| `session block REASON` | Records a blocker; implies `STATE.md` must change |
| `session artifact PATH... [--dir DIR]... [--note TEXT]` | Records files with their SHA-256 and size; `--dir` declares every file beneath a directory; refuses files containing credentials |
| `session finish --outcome O --summary S --next N [--push]` | Reconciles against git, checks documentation obligations, closes the stream, regenerates reports, commits the session record; `--push` also publishes the branch |
| `session status` | Active session, elapsed time, staleness, event count |
| `session resume [ID]` | Compressed brief: goal, outcome, decisions, last events |
| `session list` | Every session and its outcome |
| `session verify [--strict]` | Integrity across every session. Exit `4` on a problem. The session in flight is reported as in progress rather than failed; `--strict` fails for it too, which is what CI uses |

`--outcome` is one of `worked`, `partial`, `failed`, `no-change`.

## `task`

Dispatchable work. Protocol:
[`../process/task-lifecycle.md`](../process/task-lifecycle.md).

| Command | Effect |
|---|---|
| `task new --goal TEXT --verify CMD [...]` | Creates a task file from the template |
| `task list [--status S]` | Tasks with status and current holder |
| `task claim ID --agent NAME [--vm NAME] [--takeover R] [--push \| --no-push]` | Claims a task and publishes the claim; fails if another agent holds it. `--takeover` replaces a dead holder's claim with a recorded reason |
| `task release ID --agent NAME [--vm NAME]` | Returns a held task to the pool with a recorded reason |
| `task verify ID` | Runs the task's declared verification command; exit `3` on failure |
| `task complete ID --summary S [--evidence ...]` | Marks done and appends to the claim ledger |
| `task cancel ID --reason R` | Marks cancelled with a reason |

## `sync`

| Command | Effect |
|---|---|
| `sync status` | Branch, divergence from the remote base, dirty paths, rebase state |
| `sync pull` | Fetch and fast-forward onto the base; refuses a dirty tree or a diverged one |
| `sync push` | Publish the current branch; never forces |
| `sync land` | Rebase this branch onto the base, regenerate conflicted indexes, push |

## `worktree`

| Command | Effect |
|---|---|
| `worktree add T-0001 [--branch NAME]` | Create an isolated worktree and branch for one task |
| `worktree list` | List worktrees and the tasks they hold |
| `worktree remove T-0001` | Remove the worktree; the branch is kept |

## `doc`

| Command | Effect |
|---|---|
| `doc lint [--quiet]` | Line caps, `origin-meta`, links, orphans, stale generated files, unresolved merge conflicts. Exit `2` on a violation |
| `doc index` | Regenerates `docs/INDEX.md`, `sessions/INDEX.md`, `tasks/INDEX.md` |
| `doc index --check` | Exit `2` if anything would change; does not write |

## `skills`

| Command | Effect |
|---|---|
| `skills check` | Naming rules, frontmatter, spec compliance, `.claude/skills` mirrors |
| `skills sync [--copy]` | Creates missing mirrors; symlinks by default, copies with `--copy` |
| `skills hash` | Records per-file hashes of declared vendored skills |
| `skills verify` | Detects local modification of vendored skills. Exit `4` on a mismatch |

## `doctor` and `preflight`

| Command | Effect |
|---|---|
| `doctor [--offline] [--json]` | Environment probe; writes `.origin/doctor.json` (gitignored) |
| `preflight [--strict]` | `doc lint` + `skills check` + `session verify`, for a VM before it claims a task and for CI |

`doctor` reports only whether credential environment variables are **present**.
It never reads, prints, or stores a value.

## `tools/x`

```bash
tools/x -- <command> [args...]
```

Runs a command, captures stdout and stderr separately into
`sessions/<id>/commands.log`, records argv, cwd, exit code, duration, and the
exact log line range, then exits with the command's own exit code. Transparent
inside pipelines and under `set -e`.

Secrets in captured output are redacted before they reach disk, and the
redaction is recorded as an event. Terminal output is not redacted.

With no active session the command still runs and nothing is recorded, with a
warning on stderr.

## Tests

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

See [`../../tests/README.md`](../../tests/README.md).
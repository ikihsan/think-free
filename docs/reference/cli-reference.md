<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
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
| `session decision TEXT [--refs ...]` | Records a decision; implies at least one of `DECISIONS.md`, `DECISIONS-FOUNDATION.md`, `DECISIONS-PRACTICE.md`, `DECISIONS-SCREENING.md`, `DECISIONS-GATING.md` must change |
| `session experiment-result ID TEXT [--refs ...]` | Records an experiment outcome; implies `HYPOTHESES.md` and `FAILURES.md` must change |
| `session block REASON` | Records a blocker; implies `STATE.md` must change |
| `session artifact PATH... [--dir DIR]... [--note TEXT]` | Records files with their SHA-256 and size; `--dir` declares every file beneath a directory; refuses files containing credentials |
| `session finish --outcome O --summary S --next N [--push]` | Reconciles against git, checks documentation obligations, closes the stream, regenerates reports, commits the session record; `--push` also publishes the branch |
| `session status` | Active session, elapsed time, staleness, event count |
| `session resume [ID]` | Compressed brief: goal, outcome, decisions, last events |
| `session list` | Every session and its outcome |
| `session verify [--strict] [--lease-hours H]` | Integrity across every session. Exit `4` on a problem. A session running in this tree is "in progress" locally and a failure under `--strict`; a session on another VM is "in flight" while its task claim is in force and younger than `--lease-hours` (default 12), and "abandoned" otherwise |

`--outcome` is one of `worked`, `partial`, `failed`, `no-change`.

## `task`

Dispatchable work. Protocol:
[`../process/task-lifecycle.md`](../process/task-lifecycle.md).

| Command | Effect |
|---|---|
| `task new --goal TEXT --verify CMD [...]` | Creates a task file from the template, allocating the next number from the shared base and printing which record it was read from, then rebuilds `tasks/INDEX.md` and `docs/INDEX.md` so the new document is linked rather than an orphan. `--steps` and `--acceptance` **accumulate**: repeat the flag once per line, and omitting both leaves those sections empty rather than inventing a criterion |
| `task list [--status S]` | Tasks with status and current holder |
| `task claim ID --agent NAME [--vm NAME] [--takeover R] [--push \| --no-push]` | Claims a task and publishes the claim; fails if another agent holds it. `--takeover` replaces a dead holder's claim with a recorded reason |
| `task release ID --agent NAME [--vm NAME]` | Returns a held task to the pool with a recorded reason |
| `task verify ID` | Runs the task's declared verification command; exit `3` on failure |
| `task complete ID --summary S [--evidence ...]` | Marks done and appends to the claim ledger |
| `task cancel ID --reason R` | Marks cancelled with a reason |

## `id`

Fetches the shared base and prints the next free identifier, with the record it
was read from. Rule and ceiling:
[`identifier-allocation.md`](identifier-allocation.md).

| Command | Effect |
|---|---|
| `id next T\|F\|D [--json]` | The next free number of that kind, read from `origin/<base>` and this working tree. `--json` adds every number read, `local_highest`, `remote_highest` and `fetched` |

## `sync`

| Command | Effect |
|---|---|
| `sync status` | Branch, divergence from the remote base, dirty paths, rebase state |
| `sync pull` | Fetch and fast-forward onto the base; refuses a dirty tree or a diverged one |
| `sync push` | Publish the current branch; never forces |
| `sync land` | Rebase this branch onto the base, regenerate conflicted indexes, push. On a tree whose rebase a previous `land` stopped on, it first completes that rebase once no path is still conflicted — reporting `resumed: true` — so its own "resolve it and land again" instruction is followable by the tool that gave it. A path dirty and not staged is refused rather than swept into the rebase's commit |

## `worktree`

| Command | Effect |
|---|---|
| `worktree add T-0001 [--branch NAME]` | Create an isolated worktree and branch for one task; refuses when the task is claimed on another VM, not on this one |
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

## `release`

Enforces `RELEASE-MANIFEST.md`, which decides what is public. Protocol: the
manifest's own *What `release check` decides* section.

| Command | Effect |
|---|---|
| `release check` | Six properties of the manifest against this tree: no wildcards; every tracked top-level entry classified by exactly one table; a declared path exists unless marked `(pending)`, and a `pending` one does not; no path sits inside a directory of the other audience; no classified path holds credential-shaped text; and the release state declared here matches the one in `README.md`. Exit `2` on a violation |

It enforces **agreement, not truth**. A manifest and a `README.md` that agree on
a false claim still pass, and it does not read a path's meaning.

## `annotate`

| Command | Effect |
|---|---|
| `annotate -- doc lint` | Runs the gate, prints its report, and re-emits each violation as a `::error` naming the file; exits with the gate's own code |
| `annotate -- release check` | As above |
| `annotate -- skills check` | As above, exit `2` |
| `annotate -- skills verify` | As above, exit `4` |
| `annotate -- session verify [--strict] [--lease-hours H]` | As above, exit `4`; the session gate's own flags are read here |

This is what CI runs for the five file-reading gates, and the same string
reproduces a run you cannot read. It publishes `file=` and `line=` only when the
rule that found the violation knows them: a path that is a directory or absent,
and a line past the end of a file, are dropped rather than guessed, and a clean
tree emits no command at all. An unknown gate or an unread flag is refused with
exit `1` rather than quietly running something else. Method and escaping:
[`../operations/ci-diagnosis.md`](../operations/ci-diagnosis.md).

## `probe`

| Command | Effect |
|---|---|
| `probe` | Emits one workflow command per rendering shape, `title`d `annotation-probe/<shape>`, and exits `0` whatever the tree says |

Not a gate and not a wrapper for one. CI runs it on every push so that the run
reporting a failure also carries the reference for reading it: a mechanism's
rendering measured on a green run cannot be compared with what it did on a red
one, and F021 is what reading a red run without that reference cost. It emits
only `notice` and `warning` — levels a green run already publishes — so it cannot
redden the run it measures, and it takes no flags and refuses nothing. The seven
shapes and what each settles are in
[`../operations/ci-diagnosis.md`](../operations/ci-diagnosis.md).

## `doctor` and `preflight`

| Command | Effect |
|---|---|
| `doctor [--offline] [--json]` | Environment probe; writes `.origin/doctor.json` (gitignored) |
| `preflight [--strict] [--lease-hours H]` | `doc lint` + `skills check` + `session verify` + `release check`, for a VM before it claims a task and for CI |

`doctor` reports the push credential **mechanism** as well as the presence of
four environment variables: which `credential.helper` is configured, whether each
named helper exists and is executable, which App key files are present and at
what mode, whether the helper depends on anything outside `~/.config`, and
whether `git credential fill` obtained a credential. The verdict is
`configured`, `broken`, or `unavailable`, and **`configured` does not mean the
credential can push**. It never reads, prints, or stores a value; the contract
and its ceilings are in [`../operations/doctor.md`](../operations/doctor.md).

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
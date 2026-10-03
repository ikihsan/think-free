<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Bootstrap

Getting a fresh machine able to work on this repository. The design goal is that
a new VM needs no installation step: the tooling is standard-library Python plus
a shell.

## Requirements

| Requirement | Version | Verified |
|---|---|---|
| Python | 3.11 or newer | 3.14.6 on the development machine |
| `git` | any recent | 2.55.0 |
| bash | 4 or newer | yes |
| Disk | enough for the experiment | 8.6 GiB free at the last probe |
| Memory | 1 GiB per concurrent experiment | 15.3 GiB total, shared |

Not needed: `pip`, `virtualenv`, `pytest`, `docker`, `gh`, `uv`, or a GPU. Their
absence is not an error.

## Fresh-machine setup

```bash
git clone <repo-url> think-free
cd think-free

tools/origin doctor              # environment probe; writes .origin/doctor.json
tools/origin preflight           # lint + skills + session integrity
python3 -m unittest discover -s tests -t tests   # needs PYTHONPATH, see below
```

Run the test suite the way CI does:

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

## How the entry points resolve the repository

`tools/origin` and `tools/x` locate the repository root from their own location
via `git rev-parse --show-toplevel`, export it as `ORIGIN_ROOT`, put
`<root>/tools` on `PYTHONPATH`, and hand off to `python3 -m originlib`.

Consequences worth knowing:

- They work from any working directory inside the repository.
- `ORIGIN_ROOT` can be set explicitly, which is what the test suite does to
  isolate each test in a throwaway repository.
- A worktree works without further configuration.
- If `git` is unavailable, the shims fall back to their parent directory and
  will fail loudly rather than writing into the wrong tree.

## Windows and filesystems without symlinks

`.claude/skills/<name>` entries are symlinks so that Claude Code finds the same
files as Codex, Gemini, Cursor, and OpenCode. On a filesystem that cannot create
symlinks, use copy mode:

```bash
tools/origin skills sync --copy
```

Copies are second-class: editing the copy does not change the canonical skill.
Prefer a developer mode or WSL over copy mode, because a stale copy produces
exactly the bug this layout exists to prevent.

## What a machine must not have

- A GitHub App private key, until `docs/operations/github-app.md` is implemented
  and its key-handling checklist has passed.
- Repository secrets in the environment of an agent process, beyond what that one
  task needs.
- An `ORIGIN_AGENT` value that lies about which agent is running. It is the only
  thing distinguishing one runner's record from another's.

## Checking a machine before it takes a task

```bash
tools/origin doctor --json | python3 -m json.tool | less
```

Look at: tool versions present, free disk, free memory, network probe status,
git cleanliness. An environment limitation discovered before claiming a task is
a recorded fact; the same limitation discovered halfway through is a lost
session.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Logging standard

What must be recorded, in what form, and what is deliberately exempt. The
session protocol describes the workflow; this file defines the record itself.

## Two layers

| Layer | File | Mutability | Authority |
|---|---|---|---|
| Machine | `sessions/<id>/events.jsonl` | Append-only, never rewritten | Authoritative |
| Human | `sessions/<id>/README.md` | Regenerated | Derived, disposable |

Derived reports can be deleted and rebuilt at any time. The event stream cannot
be edited without detection, which is the point: an agent that improves its own
narrative after the fact has to leave a trace.

## Event kinds

| Kind | Emitted when | Carries |
|---|---|---|
| `session_start` | A session opens | goal, agent, task, files already dirty |
| `milestone` | A step finishes | summary |
| `decision` | A choice is made | summary, refs |
| `experiment_result` | An experiment concludes | experiment, summary, refs |
| `artifact` | A file is produced | path, sha256, bytes, tracked |
| `command` | `tools/x` runs something | argv, cwd, exit, duration, log lines |
| `note` | An observation worth keeping | summary |
| `block` | Progress stops | reason |
| `base_advance` | `sync pull`/`sync land` moved the base under an open session | reason, from, to, commits that arrived |
| `unlogged_change` | Reconciliation finds one | path |
| `doc_update` | A mission record changed | path |
| `task_claim` / `task_status` | Task state moves | task, action |
| `redaction` | A secret was masked | patterns, argv |
| `integrity_error` | A rule was broken | what, action |
| `session_end` | A session closes | outcome, summary, next, counts |

Unknown kinds are rejected at write time. A typo becomes an error rather than an
event nothing else understands.

## Required event fields

Every event carries `schema`, `seq`, `ts`, `session`, `kind`, and `data`.
`seq` starts at 1 and increments by exactly 1 within a session. `ts` is local
ISO 8601 with an offset. `actor` and `host` are recorded when known; `git.head`
and `git.branch` on the opening event.

`schema` is `origin.session.event/1`. A future incompatible shape bumps it, and
`verify` rejects a mismatch rather than guessing.

## What is exempt from the line cap

- `*.json`, `*.jsonl`, `*.log` — machine data and raw captured output.
- Paths declared `exempt:` in `vendor/MANIFEST.md` — vendored upstream content,
  kept byte-identical so it can be diffed and updated.

Exempt files are still **reported** by `origin doc lint` as `info` with their
line counts. Exemption means "not a failure", never "invisible".

## Secrets

Two policies, because the risks differ.

**Artifacts are refused.** A file matching a credential pattern is not recorded
and the command fails with exit `1`. The file would become the exposure, and a
redacted artifact would be a corrupted artifact. Patterns cover GitHub tokens
and App private keys, AWS keys, OpenAI and Anthropic keys, Slack tokens, Google
API keys, PEM private-key blocks, and generic `key = value` assignments.

Overlapping matches collapse to the most specific pattern, so `TOKEN=ghp_...`
is reported once as `github-token`, not twice. Values are never included in a
finding, a log line, or an event: only the pattern name.

**Command output is redacted.** Losing evidence is worse than masking a token,
so captured output is written with matches replaced by
`<REDACTED:pattern>` and a `redaction` event naming the patterns. Terminal
output is not redacted, because suppressing it would hide command failures.

**Deliberate fixtures may declare themselves.** A test for a credential scanner
has to contain a credential that looks real. A file can say so, by naming the
patterns it contains:

```python
# origin-allow-secret-patterns: github-token, aws-access-key-id
```

The directive applies to that file only, must appear within its first 40 lines,
and suppresses exactly the patterns named. Suppressing a specific pattern also
silences the generic rule that re-reported the same span, so one name is enough.
Every use is recorded as a `note` event when the file is declared as an artifact,
so a suppression is visible in the session log and reviewable in a diff. It is not
a way to declare a real credential harmless.

Before committing anything containing a credential, rotate it. Removing the
string from the file does not undo a leak.

## What reconciliation exempts, and why

Three categories of change are not reported as undeclared work, each for a
concrete reason:

1. **Session bookkeeping.** `sessions/active.json` and the active session's own
   directory, which change by design while a session runs.
2. **Generated files.** Anything carrying `generated-by: origin`. Regenerating an
   index is the tooling's job, not a work product to declare.
3. **Vendored content.** Paths declared in `vendor/MANIFEST.md`. These are
   verified by digest against `vendor/hashes.json` by `origin skills verify`,
   which is a stronger check than an artifact event; declaring every vendored file
   on each update would be noise.

Everything else must be declared as an artifact. If reconciliation is too noisy
to be useful, the fix is to narrow what the tooling exempts deliberately, never
to ignore the report.

## Retention

Keep everything. `sessions/` is small: an event is a few hundred bytes and
command output is capped by what you chose to capture. Deleting a session
record removes the only evidence that a piece of work happened; the generated
report can always be rebuilt, so it is the thing to regenerate rather than keep.

`commands.log` is the one file that can grow large. If a session's log becomes
unwieldy, the fix is to capture less, not to delete history.

## What the record deliberately does not contain

- Secrets, in any form, anywhere.
- Model weights, prompts, or raw conversation transcripts. The claim is about
  what was done and what was observed, not about the agent's internals.
- Anything the agent did not actually do. Every entry traces to a command, a
  file, or an explicit statement that something was not done.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Session protocol

Every working session follows these steps. The goal is that a session's record
is complete and checkable without trusting the agent that produced it.

## The short version

```bash
tools/origin session start --goal "one sentence" [--task T-0001] [--agent name]
tools/origin session step "milestone reached"
tools/origin session artifact path/to/file
tools/x -- <command>
tools/origin session finish --outcome worked --summary "…" --next "…"
```

## 1. Start before you touch anything

`session start` records the goal, the agent, the host, the branch, the commit
you started from, and which files were already dirty. Starting afterwards is
the one unrecoverable mistake: reconciliation needs the starting commit to tell
your changes from the ones that were already there.

Only one session may be open per working tree. `tools/origin session status`
tells you which. A leftover pointer means a session ended without `finish`;
finish it or delete `sessions/active.json` deliberately, having checked
`session verify` first.

On a shared repository, `session start` also fetches the remote and
fast-forwards onto the shared base before recording anything. A tree that
diverged, or a tree with uncommitted changes while the remote moved, is
refused — the session never starts from a state nobody else has seen, and
never merges. The starting event records the remote commit the work branched
from.

## 2. Declare artifacts, do not just write files

`tools/origin session artifact <path>` records a file you produced together with
its SHA-256 and size. Use it for anything a reader would want to verify:
reports, experiment results, task files, decisions.

Artifacts are refused when they contain something matching a credential
pattern, because the file itself is the exposure. Redacting an artifact would
corrupt it, so the correct response is to fix the file.

## 3. Route evidence-producing commands through `tools/x`

```bash
tools/x -- python3 EXPERIMENTS/001-foo/run.py
```

`tools/x` runs the command, captures stdout and stderr separately into
`sessions/<id>/commands.log`, records argv, exit code, duration, and the exact
log lines, then exits with the command's own exit code. It is transparent
inside pipelines.

Commands run outside `tools/x` are not captured. That is acceptable for
throwaway inspection, but anything a conclusion depends on must be captured.

Secrets in captured output are redacted before they reach disk, and the
redaction is itself recorded. Terminal output is not redacted, so do not print
a credential in the first place.

## 4. Record decisions as you make them

```bash
tools/origin session decision "chose X over Y because Z" --refs docs/...
tools/origin session experiment-result E001 "baseline was sufficient" --refs EXPERIMENTS/001-...
tools/origin session block "needs a VM with GPU"
```

These are not decoration. On `finish`, a `decision` event that is not matched by
a change to any decision record becomes an `integrity_error`. The log is split
by invariant across `DECISIONS.md` (index), `DECISIONS-FOUNDATION.md`,
`DECISIONS-PRACTICE.md`, and `DECISIONS-GATING.md`, so *any one* of them
satisfies the check — demanding all
four would report a gap on every correct session. The same applies to
`experiment_result` and `HYPOTHESES.md`, `FAILURES.md`, and `block` and
`STATE.md`. The tooling enforces that the record and the documents agree.

## 5. Finish: reconcile, then close

`session finish` does five things in order:

1. **Reconciles.** Compares the working tree against declared artifacts. Anything
   changed but undeclared becomes an `unlogged_change` event.
2. **Checks declarations still exist.** A declared artifact that has since been
   deleted becomes an `integrity_error`.
3. **Checks documentation obligations.** Mission records implied by this
   session's events that did not change become `integrity_error`.
4. **Records `doc_update` events** for mission records that did change.
5. **Closes the stream**, removes `sessions/active.json`, and regenerates the
   session report and `sessions/INDEX.md`.

It exits `4` when reconciliation found something unlogged or missing. Read the
output. Either declare the files or revert them. Do not paper over the report.

## What "logged perfectly" means here, honestly

Logging is cooperative. An agent can forget. What this design guarantees is that
forgetting is **visible**:

- undeclared changes are detected by comparing git against the record;
- missing or duplicated session lifecycle events fail `session verify`;
- command events point at log line ranges that must exist;
- committed generated reports must match what the generator produces now;
- documentation obligations are cross-checked against event kinds.

The honest claim is "gaps are detected", not "nothing is ever missed".

## Verify

```bash
tools/origin session verify     # every session, every event
tools/origin preflight          # lint + skills + sessions, for CI and VM start
```

`verify` checks: contiguous sequences, exactly one `session_start` and at most
one `session_end`, the last event is `session_end` (or the session is reported
unfinished), valid session ids, a report for every session, and that every
command event's log lines exist.

## Recovery after an interruption

```bash
tools/origin session status
tools/origin session resume            # goal, outcome, decisions, last events
tools/origin session finish --outcome partial --summary "…" --next "…"
```

An unfinished session is not an error. It is a session whose `session_end` is
missing, and `verify` says so. Finish it honestly rather than deleting it.

## Multi-machine note

Each session writes its own `events.jsonl` under its own directory, so two
sessions on different branches never conflict. `sessions/INDEX.md` is generated
and may need regenerating after a merge; that is expected, not corruption.

With `--push`, `session finish` commits only the session's own files and pushes
the branch. Uncommitted work of your own is refused, not auto-committed, so the
record and the work travel together. See
[`multi-vm-coordination.md`](multi-vm-coordination.md) for the full contract.
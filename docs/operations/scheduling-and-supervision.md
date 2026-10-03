<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Scheduling and supervision

Whether agent work can run unattended, and what has actually been verified. The
distinction between the two matters: a scheduler that exists is not a system
that works.

## Verified on the development machine

Observed 2026-10-03, Fedora, systemd user session active:

| Capability | Status |
|---|---|
| `crontab` present | yes, no crontab installed |
| `systemctl` present | yes |
| `systemd --user is-system-running` | `running` |
| User units | none defined |

Source: `.origin/doctor.json` produced by `tools/origin doctor`, and
`EXPERIMENTS/000-capabilities/results.json`.

## Not verified

| Capability | Why it matters | State |
|---|---|---|
| Unattended agent execution | The whole premise of fleet operation | untested |
| A scheduler that survives logout | Long runs must not die with a session | untested |
| Remote VM fleet access | The VMs do not exist yet | untested |
| Authenticated GitHub writes | Needed for PR creation | untested; no credentials present |
| GPU availability | Some experiments may need one | not probed |

Nothing in this repository may assume any of these. `tools/origin doctor` is
the check to run before depending on one.

## Persistence is a property of the harness, not of the agent

An agent process that ends takes its reasoning with it. The only durable
continuity is what reached disk. That is why this repository requires a session
record before the first edit and a reconciliation at the end: a session that dies
mid-run leaves an unfinished session with a start event, a goal, and a record of
what was captured so far.

`origin session verify` reports any session whose last event is not
`session_end`. That report **is** the recovery mechanism. It does not require
the agent to have survived.

## Local scheduling, if used

A periodic check that does no work, only reports:

```bash
*/15 * * * * cd /path/to/repo && tools/origin preflight >> /tmp/origin-preflight.log 2>&1
```

or, under systemd, a user timer calling the same command. Two rules:

- The scheduled job **reports**; it does not edit. A job that can change the
  repository unattended can corrupt the record it is supposed to be protecting.
- Every invocation is short, bounded, and idempotent. `preflight` and
  `session verify` are both read-only.

Running an agent unattended is a different decision with a different risk
profile, and it needs the App's key on the machine. See
[`github-app.md`](github-app.md).

## Recovery procedure after any interruption

```bash
tools/origin session status               # is a session open?
tools/origin session verify               # which sessions never finished?
tools/origin session resume <id>          # goal, decisions, last events
tools/origin session finish --outcome partial --summary "…" --next "…"
```

Then reconcile the repository against the record:

```bash
git status --short
tools/origin session finish ...           # reports undeclared changes
```

Never delete an unfinished session to make the report clean. The gap is the
information.

## Supervision requirements for a real fleet

Not implemented. When it is built, it must provide:

1. **A liveness signal.** A session open longer than 24 hours is flagged by
   `session status` (`stale: true`).
2. **Failure visibility.** Any session without `session_end` is a failure to
   investigate, surfaced by `session verify`.
3. **Bounded retries.** Not implemented. An automatic retry can loop forever on
   a task whose verification always fails.
4. **A resource ceiling.** Not implemented. Without it, a fleet can exhaust disk
   or CPU before anything reports a problem.
5. **A single writer per working tree.** Enforced by
   `session start`, which refuses to open a second session.

## Honest statement

The mission brief assumes continuous execution across days or weeks. What
exists here is the **record** that makes such execution recoverable, plus the
detection that reveals when it did not happen. Continuous execution itself is a
property of the agent harness and its scheduler, neither of which is under this
repository's control, and neither of which has been verified.
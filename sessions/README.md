<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Sessions

The append-only record of every working session in this repository.

Format: [`../docs/policy/logging-standard.md`](../docs/policy/logging-standard.md).
Protocol: [`../docs/process/session-protocol.md`](../docs/process/session-protocol.md).

## What a session directory contains

| File | Mutability | Contents |
|---|---|---|
| `events.jsonl` | **Append-only. Never hand-edited.** | The authoritative record: one JSON object per line |
| `commands.log` | Append-only | Raw captured stdout and stderr, with argv, exit code, duration |
| `README.md` | Generated; never hand-edited | Human-readable summary, regenerated from the events |

One directory per session, rather than one global log, so two sessions running on
separate branches never produce a merge conflict. `INDEX.md` is generated and may
need rebuilding after a merge; that is expected.

## Reading a session

```bash
tools/origin session list                  # every session and its outcome
tools/origin session resume 2026-10-03-002-build-infrastructure
cat sessions/<id>/events.jsonl | python3 -m json.tool --json-lines
```

## Working in this directory

```bash
tools/origin session status                # is a session open right now?
tools/origin session start --goal "…"      # before the first edit
tools/origin session finish --outcome worked --summary "…" --next "…"
```

One active session per working tree. `active.json` is the pointer; an
interrupted session leaves it behind, which is how an unfinished run becomes
visible instead of disappearing.

## Integrity

```bash
tools/origin session verify                     # local
tools/origin session verify --strict            # CI
tools/origin session verify --lease-hours 6     # tighten the in-flight lease
```

Checks contiguous sequence numbers, exactly one `session_start` and at most one
`session_end`, that the last event is `session_end` (or the session is reported
unfinished), valid session ids, a generated report per session, and that every
command event's recorded log line range still exists. Exit `4` on a problem.

Unfinished is not the same as abandoned. A session in *this* working tree is
"in progress" locally and a failure under `--strict`. A session on another VM is
"in flight" while its task claim is in force and younger than `--lease-hours`
(12), and abandoned otherwise — on a shared base branch an unfinished session is
expected while the fleet works, so only an abandoned one fails. See
[`../docs/operations/ci.md`](../docs/operations/ci.md).

## Reading outcomes honestly

`INDEX.md` records the outcome each session declared, including `failed`. A
`failed` or `partial` outcome is a legitimate record, not a defect to be tidied
away: an experiment that disproved its own motivating example
(`FAILURES.md` F001) and a session closed deliberately in order to fix a defect
before continuing are both more useful in the log than absent from it.

Session `2026-10-03-001` in this repository is the second case. It was closed
mid-way to add agent-runtime detection, which then identified the runtime
correctly for session 002 onward. Its record was kept because the log is
append-only and a discarded attempt is still an attempt that happened.

## Honest limitation

Recording is cooperative. The design makes omissions **detectable** — git is
reconciled against the record, and documentation obligations are cross-checked
against event kinds — but it cannot prevent an agent from forgetting to record
something in the first place. The claim is "gaps are found", not "nothing is ever
missed".

## Retention

Keep everything. Events are a few hundred bytes each. If a `commands.log` becomes
unwieldy, capture less in future sessions rather than deleting history: the log
is the only evidence of what a command actually printed.
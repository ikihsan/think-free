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
tools/origin session verify            # local: the session in flight is "in progress"
tools/origin session verify --strict   # CI: nothing in flight, so unfinished is a failure
```

Checks contiguous sequence numbers, exactly one `session_start` and at most one
`session_end`, that the last event is `session_end` (or the session is reported
unfinished), valid session ids, a generated report per session, and that every
command event's recorded log line range still exists. Exit `4` on a problem.

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
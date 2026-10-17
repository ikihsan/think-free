<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-16
-->

<!-- task-meta
id: T-0095
status: open
created: 2026-10-16
claim-agent:
claim-session:
claim-vm:
verify: tools/origin doc lint
-->

# T-0095 — E172: fresh observation — view-count principle and need-shape on a lar

## Goal

E172: fresh observation — view-count principle and need-shape on a large public Discourse community (community.home-assistant.io)

## Why this matters

STATE.md named next action: fresh observation in an untouched domain chosen by a stated rule; needs no Stack Exchange quota; runs in parallel with E171.

## Preconditions

E171 session owns the main tree — work in an isolated worktree.

## Steps

Write predeclared PROTOCOL.md (arms, gates, kill condition) before any fetch; commit it; fetch sample via Discourse no-key API; classify by platform-published category metadata; measure Cliff's delta on views; record RESULT.md; update FAILURES/STATE.

## Acceptance criteria

Protocol committed before first fetch; raw captures hashed; kill gate applied as declared; result recorded in RESULT.md and STATE.md.

## Verification

```bash
tools/origin doc lint
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

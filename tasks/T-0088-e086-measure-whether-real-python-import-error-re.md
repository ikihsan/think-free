<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- task-meta
id: T-0088
status: claimed
created: 2026-10-10
claim-agent: opencode
claim-session: 2026-10-10-003-e086-measure-demand-for-a-module-to-dist
claim-vm: instance-20260717-0947
verify: test -f EXPERIMENTS/086-import-error-demand/VERDICT.md
-->

# T-0088 — E086: measure whether real Python import-error reports name a module a

## Goal

E086: measure whether real Python import-error reports name a module and no distribution, testing whether pyprovides' resolver has a use

## Why this matters

STATE-next-actions.md names this the single most useful next action after E085: the resolver instrument is built and correct, but the linter is closed at 0.6%; only measured demand for 'which distribution provides this module' can justify carrying it forward. Kill line predeclared: under 1% closes the package-name line.

## Preconditions



## Steps



## Acceptance criteria

PROTOCOL.md declares gates, reachable sets, and kill conditions before the run; VERDICT.md reports the measured rate with Wilson CI, precision hand-read, and the decision

## Verification

```bash
test -f EXPERIMENTS/086-import-error-demand/VERDICT.md
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

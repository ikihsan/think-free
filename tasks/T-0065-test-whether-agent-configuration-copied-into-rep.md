<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0065
status: claimed
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-003-test-whether-agent-configuration-copied
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0065 — Test whether agent-configuration copied into repositories goes stale, 

## Goal

Test whether agent-configuration copied into repositories goes stale, which is the one external consequence F037's copy-not-install finding opens

## Why this matters

F037 found the young-vocabulary populations are 14/18 executable code and that the artifact in use is a copied .claude/ directory rather than a package, so every serving channel this repository owns counts installations and reads near-zero. STATE-next-actions item 0 names the untaken third reading: if the artifact is copied, it can silently drift from the upstream it was copied from. That is a consequence in the world, not a measurement of our own instruments, so it is the first line in four experiments that is not about the mission's machinery. Either drift is common and is invisible, or copied configuration tracks upstream and the concern is unfounded.

## Preconditions

Unauthenticated raw.githubusercontent.com serves 200 for a present path and 404 for an absent one, verified 2026-10-05 before design. Repository search API reachable unauthenticated. No auth token, no rate-limit dependency: 404 is an answer, not a refusal.

## Steps

Declare the population rule, the upstream-attribution rule, both arms and both gates in EXPERIMENTS/019-copied-config-drift/README.md before the first population fetch. Sample repositories that contain a copied agent-config directory by a stated rule. For each, attribute the copy to an upstream by a stated rule and compare the copy against upstream HEAD over the fields both expose. Run the negative control arm on repositories whose config is first-party, where drift must be near zero by construction. Falsify the comparator against a deliberately stale synthetic copy. Write results.json with the unmeasured count beside every measured one.

## Acceptance criteria

Arm 1 and Arm 2 separated by a declared margin else the arm reports inconclusive. Both the drift gate and the no-drift gate declared before the first fetch. Every rate-limited or undecidable row counted as undecidable, never as absent.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

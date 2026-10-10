<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- task-meta
id: T-0090
status: open
created: 2026-10-10
claim-agent:
claim-session:
claim-vm:
verify: test -f EXPERIMENTS/091-anova-answerability/VERDICT.md
-->

# T-0090 — E091: hand-replicate E062's answerability sub-test on Anova cooking Di

## Goal

E091: hand-replicate E062's answerability sub-test on Anova cooking Discourse to test whether unanswered-means-unserved generalizes beyond Stack Exchange

## Why this matters

E062 found 17/20 top-arrival unremedied SE needs resolved by a free general assistant (F096), but flagged a venue confound: SE members skew technical. No hand replication in a second, non-technical venue exists; the classifier-based generalization route failed discrimination (E088/F109). A 20-row hand replication with pre-declared calibration gates tests whether F096 generalizes or was a venue quirk, without any classifier.

## Preconditions



## Steps



## Acceptance criteria

PROTOCOL.md declares calibration gates, reachable sets, and kill conditions before any population row is read; VERDICT.md reports served share with Wilson CI alongside denominators; raw Q/A rows committed for re-judgment

## Verification

```bash
test -f EXPERIMENTS/091-anova-answerability/VERDICT.md
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

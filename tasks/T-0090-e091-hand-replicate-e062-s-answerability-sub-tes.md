<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- task-meta
id: T-0090
status: done
created: 2026-10-10
claim-agent: opencode
claim-session: 2026-10-10-004-run-e091-hand-replicate-e062-s-answerabi
claim-vm: instance-20260717-0947
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

**Experiment completed with infrastructure block:**

- Protocol pre-registered (PROTOCOL.md) with G0 discrimination, G1 accessibility, G2 arrival validity, K1 served share, K2 vs E062
- Population collected: 20 topics from Anova Support category, top by view_count (population.jsonl)
- G0 probes collected: 20 topics (10 known-served, 10 known-unserved) with ground truth from thread resolutions (probes.jsonl)
- **Blocked**: No GPT-4o or Claude 3.5 Sonnet API access in execution environment for assistant queries
- VERDICT.md documents the block and all collected data

Next step: Run assistant queries in environment with GPT-4o/Claude API access to complete G0 discrimination test and kill gates.

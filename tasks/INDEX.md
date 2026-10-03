# Tasks index

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

12 task(s). Every task file declares a runnable verification command;
`tools/origin task verify <id>` executes it and records the exit code.

| Task | Status | Claimed by | Verify | Created |
|---|---|---|---|---|
| [`T-0001-write-falsification-kill-gates-for-the-three-hel.md`](T-0001-write-falsification-kill-gates-for-the-three-hel.md) | done |  | PYTHONPATH=tools python3 -c "import pathlib,sys; | 2026-10-03 |
| [`T-0002-run-investigation-e-the-experimental-engineer-ro.md`](T-0002-run-investigation-e-the-experimental-engineer-ro.md) | done |  | test -f RESEARCH/E.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0003-run-investigation-f-the-adoption-researcher-role.md`](T-0003-run-investigation-f-the-adoption-researcher-role.md) | done |  | test -f RESEARCH/F.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md`](T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md`](T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md) | done |  | test -f EXPERIMENTS/002-a1-masking/results.json  | 2026-10-03 |
| [`T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md`](T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md) | done |  | test -f EXPERIMENTS/002-a1-masking/sensitivity.j | 2026-10-03 |
| [`T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md`](T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md) | done |  | test -f EXPERIMENTS/002-a1-masking/distance.json | 2026-10-03 |
| [`T-0008-apply-the-information-sufficiency-witness-to-the.md`](T-0008-apply-the-information-sufficiency-witness-to-the.md) | done |  | test -f EXPERIMENTS/003-information-sufficiency/ | 2026-10-03 |
| [`T-0009-repair-the-knitting-witness-input-set-by-adding.md`](T-0009-repair-the-knitting-witness-input-set-by-adding.md) | done |  | python3 EXPERIMENTS/003-information-sufficiency/ | 2026-10-03 |
| [`T-0010-run-the-knitting-stage-a-planner-comparison-loca.md`](T-0010-run-the-knitting-stage-a-planner-comparison-loca.md) | done |  | test -f EXPERIMENTS/004-knitting-stage-a/results | 2026-10-03 |
| [`T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md`](T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md) | claimed | opencode | test -f EXPERIMENTS/005-knitting-bounded-search/ | 2026-10-03 |
| [`T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md`](T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md) | done |  | test -f RESEARCH/SYNTHESIS.md && grep -q 'origin | 2026-10-03 |

## How tasks run on another machine

```bash
tools/origin doctor                       # verify the VM can do the work
tools/origin session start --goal "$TASK" --task T-0001
tools/origin task claim T-0001 --agent "$AGENT" --vm "$HOSTNAME"
tools/origin task verify T-0001
tools/origin task complete T-0001 --summary "…"
tools/origin session finish --outcome worked --summary "…" --next "…"
```

Protocol: [`../docs/process/task-lifecycle.md`](../docs/process/task-lifecycle.md).

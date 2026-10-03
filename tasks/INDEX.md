# Tasks index

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

5 task(s). Every task file declares a runnable verification command;
`tools/origin task verify <id>` executes it and records the exit code.

| Task | Status | Claimed by | Verify | Created |
|---|---|---|---|---|
| [`T-0001-write-falsification-kill-gates-for-the-three-hel.md`](T-0001-write-falsification-kill-gates-for-the-three-hel.md) | done |  | PYTHONPATH=tools python3 -c "import pathlib,sys; | 2026-10-03 |
| [`T-0002-run-investigation-e-the-experimental-engineer-ro.md`](T-0002-run-investigation-e-the-experimental-engineer-ro.md) | done |  | test -f RESEARCH/E.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0003-run-investigation-f-the-adoption-researcher-role.md`](T-0003-run-investigation-f-the-adoption-researcher-role.md) | done |  | test -f RESEARCH/F.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md`](T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md) | claimed | codex-multivm-20261003 | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md`](T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md) | claimed | opencode | test -f EXPERIMENTS/002-a1-masking/results.json  | 2026-10-03 |

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

# Tasks index

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

3 task(s). Every task file declares a runnable verification command;
`tools/origin task verify <id>` executes it and records the exit code.

| Task | Status | Claimed by | Verify | Created |
|---|---|---|---|---|
| [`T-0001-write-falsification-kill-gates-for-the-three-hel.md`](T-0001-write-falsification-kill-gates-for-the-three-hel.md) | done |  | PYTHONPATH=tools python3 -c "import pathlib,sys; | 2026-10-03 |
| [`T-0002-run-investigation-e-the-experimental-engineer-ro.md`](T-0002-run-investigation-e-the-experimental-engineer-ro.md) | open |  | test -f RESEARCH/E.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0003-run-investigation-f-the-adoption-researcher-role.md`](T-0003-run-investigation-f-the-adoption-researcher-role.md) | open |  | test -f RESEARCH/F.md && grep -q 'origin-meta' R | 2026-10-03 |

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

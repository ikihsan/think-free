# Tasks index

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

23 task(s). Every task file declares a runnable verification command;
`tools/origin task verify <id>` executes it and records the exit code.

| Task | Status | Claimed by | Verify | Created |
|---|---|---|---|---|
| [`T-0001-write-falsification-kill-gates-for-the-three-hel.md`](T-0001-write-falsification-kill-gates-for-the-three-hel.md) | done |  | PYTHONPATH=tools python3 -c "import pathlib,sys; | 2026-10-03 |
| [`T-0002-run-investigation-e-the-experimental-engineer-ro.md`](T-0002-run-investigation-e-the-experimental-engineer-ro.md) | done |  | test -f RESEARCH/E.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0003-run-investigation-f-the-adoption-researcher-role.md`](T-0003-run-investigation-f-the-adoption-researcher-role.md) | done |  | test -f RESEARCH/F.md && grep -q 'origin-meta' R | 2026-10-03 |
| [`T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md`](T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md) | done | codex-multivm-20261003 | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md`](T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md) | done |  | test -f EXPERIMENTS/002-a1-masking/results.json  | 2026-10-03 |
| [`T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md`](T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md) | done |  | test -f EXPERIMENTS/002-a1-masking/sensitivity.j | 2026-10-03 |
| [`T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md`](T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md) | done |  | test -f EXPERIMENTS/002-a1-masking/distance.json | 2026-10-03 |
| [`T-0008-apply-the-information-sufficiency-witness-to-the.md`](T-0008-apply-the-information-sufficiency-witness-to-the.md) | done |  | test -f EXPERIMENTS/003-information-sufficiency/ | 2026-10-03 |
| [`T-0009-repair-the-knitting-witness-input-set-by-adding.md`](T-0009-repair-the-knitting-witness-input-set-by-adding.md) | done |  | python3 EXPERIMENTS/003-information-sufficiency/ | 2026-10-03 |
| [`T-0010-run-the-knitting-stage-a-planner-comparison-loca.md`](T-0010-run-the-knitting-stage-a-planner-comparison-loca.md) | done |  | test -f EXPERIMENTS/004-knitting-stage-a/results | 2026-10-03 |
| [`T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md`](T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md) | done |  | test -f EXPERIMENTS/005-knitting-bounded-search/ | 2026-10-03 |
| [`T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md`](T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md) | done |  | test -f RESEARCH/SYNTHESIS.md && grep -q 'origin | 2026-10-03 |
| [`T-0013-run-e3-s-build-timestamp-census-over-200-recent.md`](T-0013-run-e3-s-build-timestamp-census-over-200-recent.md) | done |  | test -f EXPERIMENTS/007-build-timestamps/results | 2026-10-03 |
| [`T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md`](T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md) | done |  | test -f EXPERIMENTS/006-ventilation-measurement- | 2026-10-03 |
| [`T-0015-run-the-knitting-candidate-s-remaining-kill-gate.md`](T-0015-run-the-knitting-candidate-s-remaining-kill-gate.md) | done |  | test -f RESEARCH/PRIOR-ART-KNITTING.md && for f  | 2026-10-03 |
| [`T-0016-make-the-test-suite-pass-on-the-ci-runner-s-pyth.md`](T-0016-make-the-test-suite-pass-on-the-ci-runner-s-pyth.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0017-build-one-source-twice-under-different-source-da.md`](T-0017-build-one-source-twice-under-different-source-da.md) | done | opencode | test -d EXPERIMENTS/008-build-timestamp-attribut | 2026-10-03 |
| [`T-0018-record-exercised-git-versions-machine-readably-a.md`](T-0018-record-exercised-git-versions-machine-readably-a.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0019-snapshot-side-a-of-the-e2-dependency-closure-dri.md`](T-0019-snapshot-side-a-of-the-e2-dependency-closure-dri.md) | done |  | test -f EXPERIMENTS/009-lockfile-drift-snapshot/ | 2026-10-03 |
| [`T-0020-tell-an-in-flight-session-apart-from-an-abandone.md`](T-0020-tell-an-in-flight-session-apart-from-an-abandone.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0021-resolve-the-merge-conflict-markers-committed-to.md`](T-0021-resolve-the-merge-conflict-markers-committed-to.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0022-implement-origin-release-check-so-release-manife.md`](T-0022-implement-origin-release-check-so-release-manife.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |
| [`T-0023-repair-the-two-operations-documents-whose-stated.md`](T-0023-repair-the-two-operations-documents-whose-stated.md) | done |  | PYTHONPATH=tools:tests python3 -m unittest disco | 2026-10-03 |

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

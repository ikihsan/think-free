# Session 2026-10-04-029-measure-how-github-files-an-annotation-o

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T10:07:57+00:00
- **Duration:** 2370.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure how GitHub files an annotation on the file= property, and repair the false record and the gate step that never ran (T-0046)

## Summary

Measured how GitHub files a check-run annotation: it files it on the emitted file=, observed on run 37191658964. The record had called the rendering unmeasured on run 37189825232, whose Tests step failed and so skipped all five annotating steps - the ::error file=... string there was a unittest assertion diff (F021, defect 18). Repaired with always() on every diagnostic step, added origin probe so every rendering shape is measured on the run that needs it, wrote the gating decision T-0040 owed (D037, D038), and moved STATE.md's oldest session entries to STATE-history-2.md to make room. 485 tests green, preflight OK. Hit defect 2's hand-run-rebase ceiling landing, which also exposed that sync land's own conflict instruction cannot be followed.

## Next

Teach sync land to complete a paused rebase whose conflicts are already resolved, so 'resolve it and land again' is executable and the base_advance is recorded. Filed as a task.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/010-annotation-rendering/README.md | 2d6908d6b073 | 7199 |
| EXPERIMENTS/010-annotation-rendering/fetch_annotations.py | 561b28d7441e | 5326 |
| EXPERIMENTS/010-annotation-rendering/raw/summary.json | 3e94a1d54dd9 | 2288 |
| tools/originlib/probe.py | e404d044e66a | 4637 |
| tests/test_probe.py | 956ee2bc4f31 | 7401 |
| tests/test_ci_matrix.py | 830eea8cefeb | 13556 |
| .github/workflows/ci.yml | 3b7f9ddb5452 | 6624 |
| STATE-defects.md | 297bf0eb4972 | 21146 |
| FAILURES-findings-4.md | b9870ec359dc | 18539 |
| DECISIONS-GATING.md | 51c88af8bcc1 | 18229 |

## Commands

7 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/010-annotation-rendering/fetch_annotations.py'] | 0 | 6036 |
| 4 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -q'] | 1 | 230022 |
| 5 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -q 2>&1 \| tail -6'] | 0 | 227991 |
| 6 | ['tools/origin', 'preflight'] | 0 | 8320 |
| 23 | ['git', '-c', 'core.editor=true', 'rebase', '--continue'] | 0 | 293 |
| 24 | ['tools/origin', 'sync', 'land'] | 1 | 489 |
| 25 | ['tools/origin', 'sync', 'land'] | 0 | 5076 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 15 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS.md |
|   undeclared | FAILURES.md |
|   undeclared | ROADMAP.md |
|   undeclared | STATE-history-2.md |
|   undeclared | STATE-next-actions.md |
|   undeclared | STATE.md |
|   undeclared | docs/operations/ci-diagnosis.md |
|   undeclared | docs/operations/ci.md |
|   undeclared | docs/reference/cli-reference.md |
|   undeclared | tasks/T-0046-measure-how-github-files-an-annotation-on-the-fi.md |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:07:57 | session_start | Measure how GitHub files an annotation on the file= property, and repair the false record and the gate step that never ran (T-0046) |
| 2 | 10:09:49 | command | $ python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py |
| 3 | 10:23:40 | milestone | captured four runs' annotations raw: GitHub files the annotation on file=, and two red runs never reached the annotator (F021, defect 18) |
| 4 | 10:33:30 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -q |
| 5 | 10:37:56 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -q 2>&1 \| tail -6 |
| 6 | 10:38:12 | command | $ tools/origin preflight |
| 7 | 10:42:30 | artifact | wrote EXPERIMENTS/010-annotation-rendering/README.md |
| 8 | 10:42:31 | artifact | wrote EXPERIMENTS/010-annotation-rendering/fetch_annotations.py |
| 9 | 10:42:31 | artifact | wrote EXPERIMENTS/010-annotation-rendering/raw/summary.json |
| 10 | 10:42:32 | artifact | wrote tools/originlib/probe.py |
| 11 | 10:42:32 | artifact | wrote tests/test_probe.py |
| 12 | 10:42:33 | artifact | wrote tests/test_ci_matrix.py |
| 13 | 10:42:33 | artifact | wrote .github/workflows/ci.yml |
| 14 | 10:42:34 | artifact | wrote STATE-defects.md |
| 15 | 10:42:34 | artifact | wrote FAILURES-findings-4.md |
| 16 | 10:42:35 | artifact | wrote DECISIONS-GATING.md |
| 17 | 10:42:36 | decision | A step whose only job is to emit a diagnostic says always() &&, and a diagnostic mechanism is measured by a probe on the same run that needs it, not i |
| 18 | 10:42:36 | decision | A violation carries the location its own rule knows and the workflow publishes it - the decision T-0040 owed, whose prose sat in an operations documen |
| 19 | 10:42:37 | milestone | probe shipped, both gates falsified against the unmodified workflow and the unmodified shape table, 485 tests green |
| 20 | 10:42:47 | milestone | suite green 485 tests and all four preflight gates; task verify exit 0 |
| 21 | 10:43:02 | experiment_result | GitHub files a check-run annotation on the workflow command's file=, observed on run 37191658964; the run the record had quoted for that question (371 |
| 22 | 10:43:03 | milestone | suite green 485 tests and all four preflight gates; task verify exit 0 |
| 23 | 10:46:09 | command | $ git -c core.editor=true rebase --continue |
| 24 | 10:46:15 | command | $ tools/origin sync land |
| 25 | 10:46:28 | command | $ tools/origin sync land |
| 26 | 10:47:18 | note | Three paths in the finish report will be reported as unlogged and are the other VM's, not mine: tasks/T-0047-attribute-a-task-file-that-a-task-command |
| 27 | 10:47:27 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 28 | 10:47:27 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 29 | 10:47:27 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 30 | 10:47:27 | unlogged_change | changed but never declared as an artifact: STATE-history-2.md |
| 31 | 10:47:27 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 32 | 10:47:27 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 33 | 10:47:27 | unlogged_change | changed but never declared as an artifact: docs/operations/ci-diagnosis.md |
| 34 | 10:47:27 | unlogged_change | changed but never declared as an artifact: docs/operations/ci.md |
| 35 | 10:47:27 | unlogged_change | changed but never declared as an artifact: docs/reference/cli-reference.md |
| 36 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tasks/T-0046-measure-how-github-files-an-annotation-on-the-fi.md |
| 37 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tasks/T-0047-attribute-a-task-file-that-a-task-command-rewrot.md |
| 38 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tests/README.md |
| 39 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tests/test_ci_annotations.py |
| 40 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli.py |
| 41 | 10:47:27 | unlogged_change | changed but never declared as an artifact: tools/originlib/cli_args.py |
| 42 | 10:47:27 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 43 | 10:47:27 | doc_update | updated DECISIONS-GATING.md |
| 44 | 10:47:27 | doc_update | updated DECISIONS.md |
| 45 | 10:47:27 | doc_update | updated FAILURES.md |
| 46 | 10:47:27 | doc_update | updated ROADMAP.md |
| 47 | 10:47:27 | doc_update | updated STATE.md |
| 48 | 10:47:27 | session_end | Measured how GitHub files a check-run annotation: it files it on the emitted file=, observed on run 37191658964. The record had called the rendering u |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-029-measure-how-github-files-an-annotation-o/events.jsonl
```

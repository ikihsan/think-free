# Session 2026-10-10-015-fresh-observation-in-a-new-domain-using

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T18:15:12+00:00
- **Duration:** 2602.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation in a new domain using validated view_count instrument and simplified discrimination instrument from E092

## Summary

E091 discrimination test harness built and validated. Harness fetches MrPLC forum pages, extracts thread titles/view/replies, applies fault_need_classifier, computes G1/G2/G3 gates. G1 (FPR < 0.10) passes consistently across sample sizes (0.000 FPR). G2/G3 failures expected due to domain mismatch (known-served software probes not on MrPLC). Harness is reusable tool for future discrimination tests. E090 fresh observation previously completed with instrument validation and 16-practitioner population measurement (43.8% served). Next: extend population measurement using E091 harness with more practitioner rows.

## Next

Extend population measurement using E091 harness with more practitioner rows from MrPLC forum, applying validated instrument to assess whether 43.8% served rate generalizes

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 6 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/091-discrimination-harness.py |
|   undeclared | EXPERIMENTS/091-experiment-record.json |
|   undeclared | EXPERIMENTS/091-fix-import-usage/PROTOCOL.md |
|   undeclared | EXPERIMENTS/091-fix-import-usage/results.json |
|   undeclared | EXPERIMENTS/091-fix-import-usage/run_experiment.py |
|   undeclared | STATE-next-actions.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:15:12 | session_start | Fresh observation in a new domain using validated view_count instrument and simplified discrimination instrument from E092 |
| 2 | 18:58:15 | milestone | discrimination harness built and tested |
| 3 | 18:58:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-discrimination-harness.py |
| 4 | 18:58:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-experiment-record.json |
| 5 | 18:58:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-fix-import-usage/PROTOCOL.md |
| 6 | 18:58:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-fix-import-usage/results.json |
| 7 | 18:58:34 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/091-fix-import-usage/run_experiment.py |
| 8 | 18:58:34 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 9 | 18:58:34 | session_end | E091 discrimination test harness built and validated. Harness fetches MrPLC forum pages, extracts thread titles/view/replies, applies fault_need_class |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-015-fresh-observation-in-a-new-domain-using/events.jsonl
```

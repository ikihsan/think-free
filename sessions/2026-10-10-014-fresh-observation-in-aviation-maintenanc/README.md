# Session 2026-10-10-014-fresh-observation-in-aviation-maintenanc

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T16:49:19+00:00
- **Duration:** 48.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation in aviation maintenance fault codes — discrimination test and population measurement complete

## Summary

E098 completed: Fresh observation in aviation maintenance fault codes domain on Aviation Stack Exchange. Discrimination test PASSED (G1 FPR=0.000, G2 TPR=0.800, G3 FNR=0.000) on 30 probes with labels known by construction. Population measurement on 77 fault-related topics: 94.8% served, 5.2% unserved. View-count instrument validated at 100% availability on Stack Exchange. No candidate emerges — domain exceptionally well-served.

## Next

Continue fresh observation in remaining structured fault domains (industrial PLC/SCADA, medical device alarm codes via FDA MAUDE, laboratory instrument error codes) or reassess candidate generation approach given 6 domains tested with no viable unserved population found.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/098-aviation-discrimination-test/PROTOCOL.md | b5ae8da9721f | 7364 |
| EXPERIMENTS/098-aviation-discrimination-test/discrimination_test.py | 804444280930 | 11941 |
| EXPERIMENTS/098-aviation-discrimination-test/results.json | d0c77e329e79 | 8496 |
| EXPERIMENTS/098-aviation-discrimination-test/measure_population.py | 974a3615500d | 4605 |
| EXPERIMENTS/098-aviation-discrimination-test/population_results.json | e9bdbd80e4b0 | 20001 |
| EXPERIMENTS/098-aviation-discrimination-test/VERDICT.md | cb97b5fff6ec | 4708 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/096-aviation-view-count/outcome.py |
|   undeclared | sessions/2026-10-10-013-prototype-query-time-reverse-lookup-give/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 16:49:19 | session_start | Fresh observation in aviation maintenance fault codes — discrimination test and population measurement complete |
| 2 | 16:49:48 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/PROTOCOL.md |
| 3 | 16:49:49 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/discrimination_test.py |
| 4 | 16:49:50 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/results.json |
| 5 | 16:49:51 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/measure_population.py |
| 6 | 16:49:53 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/population_results.json |
| 7 | 16:49:54 | artifact | wrote EXPERIMENTS/098-aviation-discrimination-test/VERDICT.md |
| 8 | 16:50:08 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/096-aviation-view-count/outcome.py |
| 9 | 16:50:08 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-013-prototype-query-time-reverse-lookup-give/events.jsonl |
| 10 | 16:50:08 | session_end | E098 completed: Fresh observation in aviation maintenance fault codes domain on Aviation Stack Exchange. Discrimination test PASSED (G1 FPR=0.000, G2  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-014-fresh-observation-in-aviation-maintenanc/events.jsonl
```

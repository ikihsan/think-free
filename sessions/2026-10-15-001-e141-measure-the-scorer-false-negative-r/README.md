# Session 2026-10-15-001-e141-measure-the-scorer-false-negative-r

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T00:26:38+00:00
- **Duration:** 7659.7s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E141: measure the scorer false-negative rate on the already-fetched HELM lite v1.0.0 math rows -- how many rows the harness scores wrong are mathematically equal to the reference -- under declared controls and kill gate, and let that decide whether preflight's missing positive exists

## Summary

E141: scorer false-negative rate 6/2874 rows (0.377% of scored-wrong); P1 4/246=1.626% vs 2.0% and 5-row gate -- kill gate FIRED, preflight line closed

## Next

E140 GitHub Actions CI-failure fresh observation (only live protocol)

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/141-scorer-false-negatives/PROTOCOL.md | d902e317bab3 | 8949 |
| EXPERIMENTS/141-scorer-false-negatives/RESULT.md | 2625251a2397 | 9217 |
| EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py | 09dc5a1740b2 | 4181 |
| EXPERIMENTS/141-scorer-false-negatives/nobox_candidates.json | eb7a04354448 | 225 |
| EXPERIMENTS/141-scorer-false-negatives/population_verification.json | ce8b0c64da71 | 491 |
| EXPERIMENTS/141-scorer-false-negatives/recall_audit.py | 7adbc01aa05f | 3225 |
| EXPERIMENTS/141-scorer-false-negatives/recall_audit_sample.json | 6ae41cb211d1 | 8071 |
| EXPERIMENTS/141-scorer-false-negatives/recover.py | 3c4c58786b3f | 10205 |
| EXPERIMENTS/141-scorer-false-negatives/recovered_rows.json | f482234cd633 | 1524 |
| EXPERIMENTS/141-scorer-false-negatives/relations.py | 849fcc7b7a70 | 9523 |
| EXPERIMENTS/141-scorer-false-negatives/verify_population.py | 8d58ee96eafe | 6328 |
| tests/test_e141_relations.py | 838fdd7cd4a4 | 4284 |
| STATE.md | a43a1ade6007 | 28160 |
| STATE-next-actions.md | f6080fd30ae2 | 12035 |
| vendor/MANIFEST.md | eaaf0000f295 | 11399 |
| EXPERIMENTS/141-scorer-false-negatives/RESULT.md | 2625251a2397 | 9217 |
| EXPERIMENTS/141-scorer-false-negatives/PROTOCOL.md | d902e317bab3 | 8949 |
| EXPERIMENTS/141-scorer-false-negatives/recovered_rows.json | f482234cd633 | 1524 |
| EXPERIMENTS/141-scorer-false-negatives/recall_audit_sample.json | 6ae41cb211d1 | 8071 |
| tests/test_e141_relations.py | 838fdd7cd4a4 | 4284 |
| EXPERIMENTS/141-scorer-false-negatives/RESULT.md | 2625251a2397 | 9217 |
| EXPERIMENTS/141-scorer-false-negatives/RESULT.md | 2625251a2397 | 9217 |
| EXPERIMENTS/141-scorer-false-negatives/PROTOCOL.md | d902e317bab3 | 8949 |
| EXPERIMENTS/141-scorer-false-negatives/recovered_rows.json | f482234cd633 | 1524 |
| EXPERIMENTS/141-scorer-false-negatives/recall_audit_sample.json | 6ae41cb211d1 | 8071 |
| EXPERIMENTS/141-scorer-false-negatives/nobox_candidates.json | eb7a04354448 | 225 |
| EXPERIMENTS/141-scorer-false-negatives/population_verification.json | ce8b0c64da71 | 491 |
| tests/test_e141_relations.py | 838fdd7cd4a4 | 4284 |
| EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py | 09dc5a1740b2 | 4181 |
| EXPERIMENTS/141-scorer-false-negatives/recall_audit.py | 7adbc01aa05f | 3225 |
| EXPERIMENTS/141-scorer-false-negatives/recover.py | 3c4c58786b3f | 10205 |
| EXPERIMENTS/141-scorer-false-negatives/verify_population.py | 8d58ee96eafe | 6328 |

## Commands

20 captured, 6 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/verify_population.py'] | 1 | 905 |
| 3 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/verify_population.py'] | 3 | 223 |
| 4 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/verify_population.py'] | 0 | 2705 |
| 5 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 1 | 610 |
| 6 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 1 | 1482 |
| 7 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 1 | 1216 |
| 8 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 2718 |
| 9 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 5416 |
| 10 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 5620 |
| 11 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 3925 |
| 12 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recall_audit.py'] | 0 | 283 |
| 13 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py'] | 0 | 276 |
| 14 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 3439 |
| 15 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recover.py'] | 0 | 3611 |
| 16 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/recall_audit.py'] | 0 | 218 |
| 17 | ['python3', 'EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py'] | 0 | 193 |
| 34 | ['tools/origin', 'doc', 'lint'] | 2 | 142715 |
| 35 | ['tools/origin', 'doc', 'lint'] | 0 | 2895105 |
| 41 | ['tools/origin', 'doc', 'lint'] | 0 | 4624801 |
| 42 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_e141_relations.py', '-v'] | 0 | 2004 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:26:38 | session_start | E141: measure the scorer false-negative rate on the already-fetched HELM lite v1.0.0 math rows -- how many rows the harness scores wrong are mathemati |
| 2 | 00:29:53 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/verify_population.py |
| 3 | 00:30:05 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/verify_population.py |
| 4 | 00:30:38 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/verify_population.py |
| 5 | 00:31:07 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 6 | 00:31:19 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 7 | 00:32:17 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 8 | 00:32:37 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 9 | 00:33:05 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 10 | 00:33:37 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 11 | 00:34:03 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 12 | 00:34:19 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recall_audit.py |
| 13 | 00:34:36 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py |
| 14 | 00:36:15 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 15 | 00:37:14 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 16 | 00:37:16 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/recall_audit.py |
| 17 | 00:37:17 | command | $ python3 EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py |
| 18 | 00:37:54 | milestone | E141 measured: 6 of 2874 HELM rows scored wrong are mathematically correct; kill gate fired (4/246 = 1.63% vs declared 2.0% and 5 rows); recall audit  |
| 19 | 00:37:55 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/PROTOCOL.md |
| 20 | 00:37:56 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/RESULT.md |
| 21 | 00:37:57 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py |
| 22 | 00:37:58 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/nobox_candidates.json |
| 23 | 00:37:59 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/population_verification.json |
| 24 | 00:38:00 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recall_audit.py |
| 25 | 00:38:02 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recall_audit_sample.json |
| 26 | 00:38:03 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 27 | 00:38:04 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recovered_rows.json |
| 28 | 00:38:05 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/relations.py |
| 29 | 00:38:06 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/verify_population.py |
| 30 | 00:38:07 | artifact | wrote tests/test_e141_relations.py |
| 31 | 00:38:08 | artifact | wrote STATE.md |
| 32 | 00:38:09 | artifact | wrote STATE-next-actions.md |
| 33 | 00:38:10 | artifact | wrote vendor/MANIFEST.md |
| 34 | 00:40:38 | command | $ tools/origin doc lint |
| 35 | 01:29:12 | command | $ tools/origin doc lint |
| 36 | 01:54:58 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/RESULT.md |
| 37 | 01:55:09 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/PROTOCOL.md |
| 38 | 01:55:22 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recovered_rows.json |
| 39 | 01:55:31 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recall_audit_sample.json |
| 40 | 01:55:44 | artifact | wrote tests/test_e141_relations.py |
| 48 | 02:26:44 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/nobox_candidates.json |
| 49 | 02:26:50 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/population_verification.json |
| 50 | 02:27:00 | artifact | wrote tests/test_e141_relations.py |
| 51 | 02:29:02 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/nobox_audit.py |
| 52 | 02:29:22 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recall_audit.py |
| 53 | 02:29:38 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/recover.py |
| 54 | 02:29:49 | artifact | wrote EXPERIMENTS/141-scorer-false-negatives/verify_population.py |
| 55 | 02:32:10 | milestone | E141 artifacts logged; kill gate fired, RESULT committed to record |
| 56 | 02:34:17 | doc_update | updated STATE.md |
| 57 | 02:34:17 | session_end | E141: scorer false-negative rate 6/2874 rows (0.377% of scored-wrong); P1 4/246=1.626% vs 2.0% and 5-row gate -- kill gate FIRED, preflight line close |

_7 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-001-e141-measure-the-scorer-false-negative-r/events.jsonl
```

# Session 2026-10-10-004-falsify-the-e081-e087-view-count-general

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `partial`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-10T00:57:18+00:00
- **Duration:** 2043.2s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Falsify the E081-E087 view-count generalisation line: test whether its instrument discriminates a known-served set from a known-unserved set

## Summary

Ran E088: froze 40 probes with labels known by construction and ran E087's unchanged bing_search/classify_served over them. G1 FAIL - 8 of 20 nonexistent products classified served (0.40) vs 11 of 20 genuinely-served (0.55); difference +0.150, Newcombe CI95 [-0.148, +0.414] spanning 0. All 8 false positives off-topic; substring 'app' in a 19-word keyword list fired on clipart vectors, Windows tutorials and spam. F109, D095 recorded; synthesis withdrawn in place; E081-E087 raw JSONL committed.

## Next

Next session starts from a fresh observation, not an eighth classify_served domain; per D083/D095.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/088-instrument-discrimination/PROTOCOL.md | efae17eb55ea | 5836 |
| EXPERIMENTS/088-instrument-discrimination/probes.jsonl | 14506fdf9e00 | 4521 |
| EXPERIMENTS/088-instrument-discrimination/README.md | 6d7a799c03fb | 5988 |
| EXPERIMENTS/088-instrument-discrimination/analyze.py | cd1ff7888744 | 11018 |
| EXPERIMENTS/088-instrument-discrimination/harvest_probes.py | c8546d6d72ff | 2167 |

## Commands

7 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-'] | 0 | 3596 |
| 6 | ['python3', 'EXPERIMENTS/088-instrument-discrimination/analyze.py'] | 1 | 3797 |
| 7 | ['python3', 'EXPERIMENTS/088-instrument-discrimination/analyze.py'] | 1 | 4489 |
| 8 | ['python3', 'EXPERIMENTS/088-instrument-discrimination/analyze.py'] | 1 | 3897 |
| 9 | ['python3', 'EXPERIMENTS/088-instrument-discrimination/analyze.py'] | 0 | 715 |
| 10 | ['python3', '-'] | 0 | 468 |
| 11 | ['python3', '-'] | 0 | 389 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 36 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-14.md |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/raw/control-needs.jsonl |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/raw/treatment-needs.jsonl |
|   undeclared | EXPERIMENTS/081-lab-instrument-error-codes/raw/treatment-results.jsonl |
|   undeclared | EXPERIMENTS/082-mcu-fault-diagnostics/raw/topics_all.jsonl |
|   undeclared | EXPERIMENTS/082-mcu-fault-diagnostics/raw/topics_embedded_forum_placeholder.jsonl |
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/raw/control-needs.jsonl |
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/082-medical-device-alarm-codes/raw/treatment-needs.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:57:18 | session_start | Falsify the E081-E087 view-count generalisation line: test whether its instrument discriminates a known-served set from a known-unserved set |
| 2 | 00:57:51 | command | $ python3 - |
| 3 | 01:02:36 | artifact | wrote EXPERIMENTS/088-instrument-discrimination/PROTOCOL.md |
| 4 | 01:02:46 | artifact | wrote EXPERIMENTS/088-instrument-discrimination/probes.jsonl |
| 5 | 01:02:57 | milestone | E088 protocol and frozen probe sets written before any harvest ran |
| 6 | 01:05:22 | command | $ python3 EXPERIMENTS/088-instrument-discrimination/analyze.py |
| 7 | 01:05:53 | command | $ python3 EXPERIMENTS/088-instrument-discrimination/analyze.py |
| 8 | 01:07:07 | command | $ python3 EXPERIMENTS/088-instrument-discrimination/analyze.py |
| 9 | 01:07:29 | command | $ python3 EXPERIMENTS/088-instrument-discrimination/analyze.py |
| 10 | 01:07:48 | command | $ python3 - |
| 11 | 01:08:02 | command | $ python3 - |
| 12 | 01:11:31 | artifact | wrote EXPERIMENTS/088-instrument-discrimination/README.md |
| 13 | 01:11:40 | artifact | wrote EXPERIMENTS/088-instrument-discrimination/analyze.py |
| 14 | 01:11:43 | artifact | wrote EXPERIMENTS/088-instrument-discrimination/harvest_probes.py |
| 15 | 01:11:47 | milestone | E088 run complete: G1 FAIL (8/20 nonexistent products called served), predeclared kill gate closes the E081-E087 line |
| 16 | 01:31:21 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-14.md |
| 17 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/raw/control-needs.jsonl |
| 18 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/raw/control-results.jsonl |
| 19 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/raw/treatment-needs.jsonl |
| 20 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/081-lab-instrument-error-codes/raw/treatment-results.jsonl |
| 21 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/topics_all.jsonl |
| 22 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-mcu-fault-diagnostics/raw/topics_embedded_forum_placeholder.jsonl |
| 23 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/raw/control-needs.jsonl |
| 24 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/raw/control-results.jsonl |
| 25 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/raw/treatment-needs.jsonl |
| 26 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/082-medical-device-alarm-codes/raw/treatment-results.jsonl |
| 27 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/raw/control-needs.jsonl |
| 28 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/raw/control-results.jsonl |
| 29 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/raw/treatment-needs.jsonl |
| 30 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/083-aviation-maintenance-fault-codes/raw/treatment-results.jsonl |
| 31 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/raw/control-needs.jsonl |
| 32 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/raw/control-results.jsonl |
| 33 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/raw/treatment-needs.jsonl |
| 34 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/084-industrial-equipment-fault-codes/raw/treatment-results.jsonl |
| 35 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/raw/control-needs.jsonl |
| 36 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/raw/control-results.jsonl |
| 37 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/raw/treatment-needs.jsonl |
| 38 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/085-building-automation-hvac/raw/treatment-results.jsonl |
| 39 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-building-code-compliance/raw/control-needs.jsonl |
| 40 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/086-building-code-compliance/raw/control-results.jsonl |
| 46 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/087-environmental-monitoring/raw/treatment-results.jsonl |
| 47 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/088-instrument-discrimination/raw/probe-results.jsonl |
| 48 | 01:31:21 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/synthesis-view-count-principle.md |
| 49 | 01:31:21 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-35.md |
| 50 | 01:31:21 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 51 | 01:31:21 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 52 | 01:31:21 | doc_update | updated DECISIONS-SCREENING-14.md |
| 53 | 01:31:21 | doc_update | updated FAILURES.md |
| 54 | 01:31:21 | doc_update | updated STATE.md |
| 55 | 01:31:21 | session_end | Ran E088: froze 40 probes with labels known by construction and ran E087's unchanged bing_search/classify_served over them. G1 FAIL - 8 of 20 nonexist |

_5 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-10-004-falsify-the-e081-e087-view-count-general/events.jsonl
```

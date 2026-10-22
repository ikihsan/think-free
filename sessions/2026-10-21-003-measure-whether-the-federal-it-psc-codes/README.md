# Session 2026-10-21-003-measure-whether-the-federal-it-psc-codes

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T08:25:51+00:00
- **Duration:** 3617.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Measure whether the federal IT PSC codes (DA01, DA10, 7A21, 7030, D304) are enterable: what fraction of each code's FY2023 recipients had no award in that code in the prior window, with gates declared before any fetch

## Summary

E209 completed: federal IT codes not uniformly enterable; three codes enterable (0.27-0.31), two closed shops (0.0); fragmentation does not predict entry. G3 kill gate fired (median 0.2677 < 0.30). Three codes (DA01, DA10, 7A21) show 0.27-0.31 newcomer fractions; two codes (7030, D304) show exactly zero - closed shops. Fragmentation axis positively correlates with entry (ρ=+0.6669) opposite sign from E208's -0.2456. The negative is not a rejection of the money axis - enterable codes are not necessarily the most fragmented. A candidate screen on the money axis should select by measured entry, not by fragmentation. Threshold 0.30 is borderline - median 0.2677 with bimodal distribution. No product proposed or adoption claimed.

## Next

Record D128 fix and determine next action

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md | f536183a9f79 | 6521 |
| EXPERIMENTS/E209-it-code-entrant-share/fetch.py | eaff645e2581 | 5914 |
| EXPERIMENTS/E209-it-code-entrant-share/analyze.py | e39a2de013c9 | 9781 |
| EXPERIMENTS/E209-it-code-entrant-share/controls.py | 518f3ff17ea2 | 1347 |
| EXPERIMENTS/E209-it-code-entrant-share/probe.py | 477ee585d492 | 2721 |
| EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json | 186a09db2257 | 1050 |

## Commands

4 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/probe.py'] | 0 | 5372 |
| 9 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/fetch.py'] | 0 | 548979 |
| 10 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/controls.py'] | 0 | 5878 |
| 11 | ['python3', 'EXPERIMENTS/E209-it-code-entrant-share/analyze.py'] | 0 | 1420 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 480 |
| declared artifacts now missing | 0 |
| integrity errors | 3 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.json |
|   error | FAILURES.md was not updated although the session recorded experiment_result |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |
|   error | DECISIONS.md was not updated although the session recorded decision |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:25:51 | session_start | Measure whether the federal IT PSC codes (DA01, DA10, 7A21, 7030, D304) are enterable: what fraction of each code's FY2023 recipients had no award in  |
| 2 | 08:26:56 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 3 | 08:36:04 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/PROTOCOL.md |
| 4 | 08:36:06 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 5 | 08:36:08 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 6 | 08:36:10 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 7 | 08:36:11 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/probe.py |
| 8 | 08:36:13 | artifact | wrote EXPERIMENTS/E209-it-code-entrant-share/raw_probe.json |
| 9 | 08:40:00 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/fetch.py |
| 10 | 08:40:35 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/controls.py |
| 11 | 08:40:53 | command | $ python3 EXPERIMENTS/E209-it-code-entrant-share/analyze.py |
| 12 | 08:55:06 | experiment_result | federal IT PSC codes are not uniformly enterable: median segment-newcomer fraction 0.2677 < declared 0.30 kill gate; DA01/DA10/7A21 enterable at 0.27- |
| 13 | 08:55:09 | decision | The uniform 'fragmented => a small program can enter' reading is unsupported in both domains measured (NIH SBIR E208, federal IT E209); a money-axis s |
| 14 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/RESULT.md |
| 15 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 16 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 17 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 18 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 19 | 09:26:01 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 20 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 21 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.json |
| 22 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.meta.json |
| 23 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.json |
| 24 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.meta.json |
| 25 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p11.json |
| 26 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p11.meta.json |
| 27 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p12.json |
| 28 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p12.meta.json |
| 29 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p13.json |
| 30 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p13.meta.json |
| 31 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p2.json |
| 32 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p2.meta.json |
| 33 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p3.json |
| 34 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p3.meta.json |
| 35 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p4.json |
| 36 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p4.meta.json |
| 37 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p5.json |
| 38 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p5.meta.json |
| 39 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p6.json |
| 40 | 09:26:02 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p6.meta.json |
| 488 | 09:26:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p8.json |
| 489 | 09:26:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p8.meta.json |
| 490 | 09:26:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p9.json |
| 491 | 09:26:07 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p9.meta.json |
| 492 | 09:26:07 | unlogged_change | changed but never declared as an artifact: tools/nih_accessibility_prototype.py |
| 493 | 09:26:07 | unlogged_change | changed but never declared as an artifact: tools/nih_sbir_metrics.py |
| 494 | 09:26:08 | integrity_error | FAILURES.md was not updated although the session recorded experiment_result |
| 495 | 09:26:08 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 496 | 09:26:08 | integrity_error | DECISIONS.md was not updated although the session recorded decision |
| 497 | 09:26:08 | session_end | E209 completed: federal IT codes not uniformly enterable; three codes enterable (0.27-0.31), two closed shops (0.0); fragmentation does not predict en |

_447 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl
```

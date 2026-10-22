# Session 2026-10-21-004-explore-small-program-accessibility-in-3

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-21
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-21T09:27:49+00:00
- **Duration:** 26.0s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

Explore small-program accessibility in 3rd NIH SBIR spending category using fixed prototype methodology

## Summary

D128 NIH SBIR prototype provenance fix verified and committed. Key changes: (1) tools/nih_accessibility_prototype.py fetch_grants() now accepts activity_codes parameter and uses meta.total stopping condition instead of arbitrary 2000-row cap; (2) tools/nih_sbir_metrics.py same fix applied. E209 completed: federal IT codes not uniformly enterable (median 0.2677 < 0.30), three codes enterable (DA01/DA10/7A21 at 0.27-0.31), two closed shops (7030/D304 at 0.0); fragmentation does not predict entry (ρ=+0.6669). Analysis logic verified against E207 census data: category 101 reproduces E204 (147 grants, 134 orgs, top5 11.6%). Single most useful next action: explore small-program accessibility pattern in 3rd NIH SBIR spending category (category 176) using fixed prototype methodology with activity_codes filtering and meta.total census, extending pattern from 2 to 3 domains and actualizing the D128 fix.

## Next

Record decision and continuation plan for 3rd domain small-program accessibility screen

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 479 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.meta.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.json |
|   undeclared | EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.meta.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 09:27:49 | session_start | Explore small-program accessibility in 3rd NIH SBIR spending category using fixed prototype methodology |
| 2 | 09:28:09 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/analysis.json |
| 3 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/controls.json |
| 4 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.json |
| 5 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_notacode.meta.json |
| 6 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.json |
| 7 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/ctl_zzzz.meta.json |
| 8 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.json |
| 9 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p1.meta.json |
| 10 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.json |
| 11 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p10.meta.json |
| 12 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p11.json |
| 13 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p11.meta.json |
| 14 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p12.json |
| 15 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p12.meta.json |
| 16 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p13.json |
| 17 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p13.meta.json |
| 18 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p2.json |
| 19 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p2.meta.json |
| 20 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p3.json |
| 21 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p3.meta.json |
| 22 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p4.json |
| 23 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p4.meta.json |
| 24 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p5.json |
| 25 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p5.meta.json |
| 26 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p6.json |
| 27 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p6.meta.json |
| 28 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p7.json |
| 29 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p7.meta.json |
| 30 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p8.json |
| 31 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p8.meta.json |
| 32 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p9.json |
| 33 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7030_p9.meta.json |
| 34 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p1.json |
| 35 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p1.meta.json |
| 36 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p10.json |
| 37 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p10.meta.json |
| 38 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p11.json |
| 39 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p11.meta.json |
| 40 | 09:28:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/current_7A21_p12.json |
| 472 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p6.meta.json |
| 473 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p7.json |
| 474 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p7.meta.json |
| 475 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p8.json |
| 476 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p8.meta.json |
| 477 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p9.json |
| 478 | 09:28:14 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E209-it-code-entrant-share/raw/prior_DA10_p9.meta.json |
| 479 | 09:28:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/commands.log |
| 480 | 09:28:15 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-21-003-measure-whether-the-federal-it-psc-codes/events.jsonl |
| 481 | 09:28:15 | session_end | D128 NIH SBIR prototype provenance fix verified and committed. Key changes: (1) tools/nih_accessibility_prototype.py fetch_grants() now accepts activi |

_431 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-21-004-explore-small-program-accessibility-in-3/events.jsonl
```

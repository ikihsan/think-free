# Session 2026-10-09-004-observe-whether-the-silent-wrong-project

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T08:19:26+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Observe whether the silent wrong-project install (E064's false-accept class: a near-miss name that resolves to a real different project, invisible to installer guards) occurs among real users, and decide whether a deterministic did-you-mean-a-different-project check has a population worth prototyping

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md | 1ffdd41a28c3 | 7329 |
| EXPERIMENTS/070-silent-wrong-project/README.md | 42066b793cc9 | 5627 |

## Commands

9 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'arm_m.py'] | 2 | 30 |
| 4 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/arm_m.py'] | 0 | 1105 |
| 5 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/arm_m.py'] | 0 | 97213 |
| 6 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/fetch_reports.py'] | 0 | 139906 |
| 7 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 313 |
| 8 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 319 |
| 9 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/fetch_reports.py'] | 0 | 177651 |
| 10 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 304 |
| 11 | ['python3', 'EXPERIMENTS/070-silent-wrong-project/sample.py'] | 0 | 398 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:19:26 | session_start | Observe whether the silent wrong-project install (E064's false-accept class: a near-miss name that resolves to a real different project, invisible to  |
| 2 | 08:20:30 | artifact | wrote EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md |
| 3 | 08:21:19 | command | $ python3 arm_m.py |
| 4 | 08:21:27 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/arm_m.py |
| 5 | 08:25:56 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/arm_m.py |
| 6 | 08:30:38 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
| 7 | 08:34:13 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 8 | 08:43:16 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 9 | 08:53:20 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/fetch_reports.py |
| 10 | 08:54:37 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 11 | 08:58:20 | command | $ python3 EXPERIMENTS/070-silent-wrong-project/sample.py |
| 12 | 09:15:53 | milestone | arm_m complete: only telegram installs silently (exit 0); sklearn, beautifulsoup, color all fail loudly. PC classification 194/233 done. G and PL clas |
| 13 | 09:37:41 | milestone | G classification complete: 3 B rows in 105 G rows. K2 primary = 3/4 = 0.75 >= 0.10. K1a met. README written. |
| 14 | 09:37:41 | artifact | wrote EXPERIMENTS/070-silent-wrong-project/README.md |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-004-observe-whether-the-silent-wrong-project/events.jsonl
```

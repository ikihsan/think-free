# Session 2026-10-07-001-e043-run-real-coding-agents-on-real-stag

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T00:07:36+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E043: run real coding agents on real staging tasks, with and without stg, to replace E042's simulated agent-usability claim with an observed one

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

38 captured, 11 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/043-real-agent-staging/build.py', '/tmp/opencode/e043'] | 0 | 417 |
| 3 | ['python3', 'EXPERIMENTS/043-real-agent-staging/build.py', '/tmp/opencode/e043'] | 1 | 1004 |
| 4 | ['python3', 'EXPERIMENTS/043-real-agent-staging/build.py', '/tmp/opencode/e043'] | 0 | 803 |
| 5 | ['python3', 'EXPERIMENTS/043-real-agent-staging/check_oracle.py', '/tmp/opencode/e043'] | 0 | 902 |
| 6 | ['python3', 'EXPERIMENTS/043-real-agent-staging/check_oracle.py', '/tmp/opencode/e043'] | 1 | 701 |
| 7 | ['python3', 'EXPERIMENTS/043-real-agent-staging/check_oracle.py', '/tmp/opencode/e043'] | 0 | 884 |
| 8 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'nostg'] | 1 | 691 |
| 9 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'stg'] | 1 | 601 |
| 10 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'nostg'] | 1 | 606 |
| 11 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'stg'] | 1 | 595 |
| 12 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'nostg'] | 1 | 587 |
| 13 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'stg'] | 1 | 589 |
| 14 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'nostg'] | 0 | 118 |
| 15 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'stg'] | 0 | 176 |
| 16 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'nostg'] | 0 | 111 |
| 17 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'stg'] | 0 | 119 |
| 18 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'nostg'] | 0 | 144 |
| 19 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'stg'] | 0 | 120 |
| 20 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043/adjacent-modifications-nostg-trial', '/tmp/opencode/e043/two-line-inser | 0 | 182 |
| 21 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'nostg'] | 0 | 194 |
| 22 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'stg'] | 0 | 127 |
| 23 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'nostg'] | 0 | 107 |
| 24 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'stg'] | 0 | 410 |
| 25 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'nostg'] | 0 | 282 |
| 26 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'stg'] | 0 | 182 |
| 27 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043'] | 0 | 492 |
| 28 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043'] | 0 | 311 |
| 29 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043'] | 0 | 395 |
| 30 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'stg'] | 1 | 771 |
| 31 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'stg'] | 1 | 673 |
| 32 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'stg'] | 1 | 697 |
| 33 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'adjacent-modifications', 'stg'] | 0 | 220 |
| 34 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'two-line-insertion', 'stg'] | 0 | 220 |
| 35 | ['python3', 'EXPERIMENTS/043-real-agent-staging/prepare.py', '/tmp/opencode/e043', 'one-edit-among-three', 'stg'] | 0 | 210 |
| 36 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043'] | 0 | 309 |
| 37 | ['sh', '-c', 'ls /tmp/opencode/e043/*-trial/ \| sort -u; echo "=== leaks checked ==="; find /tmp/opencode/e043 -name ".expected_index" -path "*-trial/ | 0 | 107 |
| 38 | ['python3', 'EXPERIMENTS/043-real-agent-staging/check_oracle.py', '/tmp/opencode/e043'] | 0 | 1887 |
| 39 | ['python3', 'EXPERIMENTS/043-real-agent-staging/score.py', '/tmp/opencode/e043'] | 0 | 287 |

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
| 1 | 00:07:36 | session_start | E043: run real coding agents on real staging tasks, with and without stg, to replace E042's simulated agent-usability claim with an observed one |
| 2 | 00:08:03 | command | $ python3 EXPERIMENTS/043-real-agent-staging/build.py /tmp/opencode/e043 |
| 3 | 00:08:30 | command | $ python3 EXPERIMENTS/043-real-agent-staging/build.py /tmp/opencode/e043 |
| 4 | 00:08:52 | command | $ python3 EXPERIMENTS/043-real-agent-staging/build.py /tmp/opencode/e043 |
| 5 | 00:09:04 | command | $ python3 EXPERIMENTS/043-real-agent-staging/check_oracle.py /tmp/opencode/e043 |
| 6 | 00:10:04 | command | $ python3 EXPERIMENTS/043-real-agent-staging/check_oracle.py /tmp/opencode/e043 |
| 7 | 00:10:12 | command | $ python3 EXPERIMENTS/043-real-agent-staging/check_oracle.py /tmp/opencode/e043 |
| 8 | 00:10:29 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications nostg |
| 9 | 00:10:30 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications stg |
| 10 | 00:10:31 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion nostg |
| 11 | 00:10:32 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion stg |
| 12 | 00:10:33 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three nostg |
| 13 | 00:10:34 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three stg |
| 14 | 00:10:41 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications nostg |
| 15 | 00:10:42 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications stg |
| 16 | 00:10:43 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion nostg |
| 17 | 00:10:43 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion stg |
| 18 | 00:10:44 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three nostg |
| 19 | 00:10:44 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three stg |
| 20 | 00:11:32 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043/adjacent-modifications-nostg-trial /tmp/opencode/e043/two-line-insert |
| 21 | 00:11:59 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications nostg |
| 22 | 00:12:00 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications stg |
| 23 | 00:12:00 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion nostg |
| 24 | 00:12:02 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion stg |
| 25 | 00:12:03 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three nostg |
| 26 | 00:12:04 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three stg |
| 27 | 00:13:07 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043 |
| 28 | 00:13:28 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043 |
| 29 | 00:14:21 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043 |
| 30 | 00:14:40 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications stg |
| 31 | 00:14:42 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion stg |
| 32 | 00:14:43 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three stg |
| 33 | 00:14:53 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 adjacent-modifications stg |
| 34 | 00:14:53 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 two-line-insertion stg |
| 35 | 00:14:54 | command | $ python3 EXPERIMENTS/043-real-agent-staging/prepare.py /tmp/opencode/e043 one-edit-among-three stg |
| 36 | 00:15:51 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043 |
| 37 | 00:15:55 | command | $ sh -c ls /tmp/opencode/e043/*-trial/ \| sort -u; echo "=== leaks checked ==="; find /tmp/opencode/e043 -name ".expected_index" -path "*-trial |
| 38 | 00:16:24 | command | $ python3 EXPERIMENTS/043-real-agent-staging/check_oracle.py /tmp/opencode/e043 |
| 39 | 00:16:25 | command | $ python3 EXPERIMENTS/043-real-agent-staging/score.py /tmp/opencode/e043 |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-001-e043-run-real-coding-agents-on-real-stag/events.jsonl
```

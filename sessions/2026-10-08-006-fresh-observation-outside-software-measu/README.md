# Session 2026-10-08-006-fresh-observation-outside-software-measu

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T03:56:34+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Fresh observation outside software: measure what happens to publicly stated unmet needs in a non-software domain, where the platform records the outcome

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| STATE.md | dc0c1d10541b | 32476 |
| STATE-next-actions.md | 02e07c31aa7e | 21257 |
| STATE-history.md | f6a935550218 | 21654 |
| DECISIONS-SCREENING-13.md | bc18cb40dba3 | 9902 |
| EXPERIMENTS/058-nonsw-need-shape/PROTOCOL.md | 1dd8b17268c9 | 6438 |
| STATE.md | e1515e5b6a7c | 36165 |
| FAILURES.md | 016a2f7e04fc | 52874 |
| docs/INDEX.md | 80c75fc45d90 | 33306 |
| FAILURES-findings-33.md | 1e0ad06c86f0 | 7697 |
| EXPERIMENTS/058-nonsw-need-shape/README.md | 1d1eac259eb5 | 6752 |
| EXPERIMENTS/058-nonsw-need-shape/AMENDMENT-1.md | 21e70666bb2b | 3616 |
| EXPERIMENTS/058-nonsw-need-shape/AMENDMENT-2.md | e72497be7e55 | 6478 |
| EXPERIMENTS/058-nonsw-need-shape/harvest.py | fa6510dafe14 | 4372 |
| EXPERIMENTS/058-nonsw-need-shape/harvest2.py | 5bffd22315fc | 4058 |
| EXPERIMENTS/058-nonsw-need-shape/sample.py | 3887436acb69 | 5383 |
| EXPERIMENTS/058-nonsw-need-shape/outcome.py | 61875ea82c89 | 10822 |
| EXPERIMENTS/058-nonsw-need-shape/raw/arm1.jsonl | bb2880e28197 | 1738912 |
| EXPERIMENTS/058-nonsw-need-shape/raw/arm2.jsonl | 030e0f91767e | 204405 |
| EXPERIMENTS/058-nonsw-need-shape/raw/requests.jsonl | 0811b2d6d8d5 | 4580 |
| EXPERIMENTS/058-nonsw-need-shape/raw/requests-arm2.jsonl | 1d4963dd805c | 5421 |
| EXPERIMENTS/058-nonsw-need-shape/raw/attempt1-requests.jsonl | a55a54a6f9d9 | 4316 |
| EXPERIMENTS/058-nonsw-need-shape/raw/attempt1-arm1-nobody.jsonl | abe18a1bda5d | 935955 |
| EXPERIMENTS/058-nonsw-need-shape/raw/sample-arm1.tsv | 22039e4830e1 | 5708 |
| EXPERIMENTS/058-nonsw-need-shape/raw/sample-arm2.tsv | 1581fae37071 | 5512 |
| EXPERIMENTS/058-nonsw-need-shape/raw/noremedy-classified.tsv | 94fd21299859 | 10533 |
| EXPERIMENTS/058-nonsw-need-shape/raw/answerability-top20.tsv | 87d298d07b9d | 5407 |
| EXPERIMENTS/058-nonsw-need-shape/raw/g2a-positive.tsv | d7ff79d74d28 | 703 |
| EXPERIMENTS/058-nonsw-need-shape/raw/g2b-negative.tsv | 3c6f4222263a | 489 |
| EXPERIMENTS/058-nonsw-need-shape/raw/outcome.json | 97e85d405d16 | 3073 |
| EXPERIMENTS/058-nonsw-need-shape/raw/steam-probe.json | cb09e947beb9 | 1178 |

## Commands

8 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 7 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/harvest.py'] | 0 | 22327 |
| 8 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/harvest.py'] | 0 | 21699 |
| 9 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/harvest2.py'] | 0 | 12879 |
| 10 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/harvest2.py'] | 0 | 194165 |
| 11 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/sample.py'] | 0 | 288 |
| 13 | ['python3', '-c', "print('ok')"] | 0 | 95 |
| 14 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/outcome.py'] | 0 | 196 |
| 15 | ['python3', 'EXPERIMENTS/058-nonsw-need-shape/outcome.py'] | 0 | 197 |

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
| 1 | 03:56:34 | session_start | Fresh observation outside software: measure what happens to publicly stated unmet needs in a non-software domain, where the platform records the outco |
| 2 | 04:10:33 | artifact | wrote STATE.md |
| 3 | 04:10:35 | artifact | wrote STATE-next-actions.md |
| 4 | 04:10:36 | artifact | wrote STATE-history.md |
| 5 | 04:10:36 | artifact | wrote DECISIONS-SCREENING-13.md |
| 6 | 04:11:33 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/PROTOCOL.md |
| 7 | 04:13:18 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/harvest.py |
| 8 | 04:15:10 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/harvest.py |
| 9 | 04:16:01 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/harvest2.py |
| 10 | 04:19:45 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/harvest2.py |
| 11 | 04:20:45 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/sample.py |
| 12 | 04:23:21 | milestone | resumed session 006 on VM 0944 after an interruption: E058 declared, Steam venue retired (AMENDMENT-1), arm 1 harvested 1200 rows with bodies, arm 2 m |
| 13 | 04:30:50 | command | $ python3 -c print('ok') |
| 14 | 04:31:32 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/outcome.py |
| 15 | 04:36:07 | command | $ python3 EXPERIMENTS/058-nonsw-need-shape/outcome.py |
| 16 | 04:43:40 | artifact | wrote STATE.md |
| 17 | 04:43:43 | artifact | wrote FAILURES.md |
| 18 | 04:43:45 | artifact | wrote docs/INDEX.md |
| 19 | 04:43:47 | artifact | wrote FAILURES-findings-33.md |
| 20 | 04:43:49 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/README.md |
| 21 | 04:43:51 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/AMENDMENT-1.md |
| 22 | 04:43:53 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/AMENDMENT-2.md |
| 23 | 04:43:55 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/harvest.py |
| 24 | 04:43:57 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/harvest2.py |
| 25 | 04:43:59 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/sample.py |
| 26 | 04:44:01 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/outcome.py |
| 27 | 04:44:06 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/arm1.jsonl |
| 28 | 04:44:11 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/arm2.jsonl |
| 29 | 04:44:13 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/requests.jsonl |
| 30 | 04:44:15 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/requests-arm2.jsonl |
| 31 | 04:44:22 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/attempt1-requests.jsonl |
| 32 | 04:44:30 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/attempt1-arm1-nobody.jsonl |
| 33 | 04:44:33 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/sample-arm1.tsv |
| 34 | 04:44:34 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/sample-arm2.tsv |
| 35 | 04:44:35 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/noremedy-classified.tsv |
| 36 | 04:44:37 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/answerability-top20.tsv |
| 37 | 04:44:38 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/g2a-positive.tsv |
| 38 | 04:44:40 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/g2b-negative.tsv |
| 39 | 04:44:42 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/outcome.json |
| 40 | 04:44:47 | artifact | wrote EXPERIMENTS/058-nonsw-need-shape/raw/steam-probe.json |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-006-fresh-observation-outside-software-measu/events.jsonl
```

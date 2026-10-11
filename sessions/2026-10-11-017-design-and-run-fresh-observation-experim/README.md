# Session 2026-10-11-017-design-and-run-fresh-observation-experim

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T10:28:13+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run fresh observation experiment on crates.io (Rust package registry) to test view-count principle on a new package registry domain

## Summary

_(none recorded)_

## Artifacts

_none_

## Commands

6 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', 'https://crates.io/api/v1/crates?page=1&per_page=5'] | 0 | 276 |
| 3 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect.py'] | 0 | 477044 |
| 4 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect_v2.py'] | 0 | 340625 |
| 5 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/collect_v3.py'] | 0 | 518303 |
| 6 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/analyze.py'] | 1 | 520 |
| 7 | ['python3', 'EXPERIMENTS/095-crates-io-viewcount/analyze.py'] | 0 | 392 |

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
| 1 | 10:28:13 | session_start | Design and run fresh observation experiment on crates.io (Rust package registry) to test view-count principle on a new package registry domain |
| 2 | 10:28:26 | command | $ curl -s https://crates.io/api/v1/crates?page=1&per_page=5 |
| 3 | 10:41:17 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect.py |
| 4 | 10:59:59 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect_v2.py |
| 5 | 11:11:51 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/collect_v3.py |
| 6 | 11:13:54 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/analyze.py |
| 7 | 11:15:25 | command | $ python3 EXPERIMENTS/095-crates-io-viewcount/analyze.py |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-017-design-and-run-fresh-observation-experim/events.jsonl
```

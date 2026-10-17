# Session 2026-10-17-004-test-the-mission-s-one-standing-constrai

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-17
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-17T06:45:42+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test the mission's one standing constraint head-on: is a free general assistant actually worse when the deciding evidence is absent from the question, on a population where the key is automatic?

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/177-evidence-gated-need/PROTOCOL.md | 8604eaf35d3c | 11479 |

## Commands

4 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['./tools/origin', 'doc', 'lint'] | 0 | 276346 |
| 3 | ['git', 'commit', '-q', '-am', 'E177 PROTOCOL + fetch + census: measure the standing constraint D107 rests on'] | 0 | 399 |
| 5 | ['python3', 'EXPERIMENTS/177-evidence-gated-need/fetch.py'] | 1 | 17515 |
| 6 | ['git', 'commit', '-q', '-am', 'E177 AMENDMENT 1: accept both tag shapes; the withbody filter returns strings'] | 1 | 295 |

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
| 1 | 06:45:42 | session_start | Test the mission's one standing constraint head-on: is a free general assistant actually worse when the deciding evidence is absent from the question, |
| 2 | 06:50:28 | command | $ ./tools/origin doc lint |
| 3 | 06:50:55 | command | $ git commit -q -am E177 PROTOCOL + fetch + census: measure the standing constraint D107 rests on |
| 4 | 06:50:58 | artifact | wrote EXPERIMENTS/177-evidence-gated-need/PROTOCOL.md |
| 5 | 06:51:20 | command | $ python3 EXPERIMENTS/177-evidence-gated-need/fetch.py |
| 6 | 06:51:34 | command | $ git commit -q -am E177 AMENDMENT 1: accept both tag shapes; the withbody filter returns strings |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-17-004-test-the-mission-s-one-standing-constrai/events.jsonl
```

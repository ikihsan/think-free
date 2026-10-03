# Session 2026-10-03-038-implement-origin-release-check-so-releas

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `opencode`
- **Started:** 2026-10-03T23:10:09+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

implement 'origin release check' so RELEASE-MANIFEST.md is machine-enforced, and repair the front-door documents it exposes as false

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tools/originlib/release.py | 8814910f33ce | 11977 |
| tests/test_release.py | 83be2a89e8ec | 10330 |
| tools/originlib/cli.py | 3506be00ff7d | 11034 |
| tools/originlib/cli_repo.py | 6d91902d716d | 4255 |
| RELEASE-MANIFEST.md | c4b03772fab2 | 4347 |
| README.md | 331bda8703ff | 4529 |
| ROADMAP.md | 2a17f95e9d42 | 8428 |
| STATE.md | 5865edd1fdf6 | 21101 |
| STATE-history.md | 090a3c941437 | 14485 |
| AGENTS.md | f80258c06f28 | 8102 |
| docs/reference/cli-reference.md | 74ed37d37c44 | 6656 |
| tests/README.md | 5e448cc35e9f | 3368 |
| .github/workflows/ci.yml | 6fc478fb9a43 | 2396 |
| tasks/T-0022-implement-origin-release-check-so-release-manife.md | ff05ef6d1241 | 5566 |
| sessions/2026-10-03-038-implement-origin-release-check-so-releas/README.md | 25f36b18e97e | 2340 |
| sessions/2026-10-03-038-implement-origin-release-check-so-releas/commands.log | dec99c22ff1f | 8905 |
| sessions/2026-10-03-038-implement-origin-release-check-so-releas/events.jsonl | 96df8123b49c | 12525 |

## Commands

4 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', 'cd /home/ubuntu/think-free\nPYTHONPATH=tools python3 - <<"PY"\nimport pathlib, shutil, tempfile\nfrom originlib import release\n\nbase | 0 | 215 |
| 3 | ['bash', '-c', 'cd /home/ubuntu/think-free\ncp RELEASE-MANIFEST.md /tmp/opencode/relfix/new-manifest.md\ncp /tmp/opencode/relfix/RELEASE-MANIFEST.md R | 0 | 7094 |
| 4 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^Ran\|^OK\|^FAILED"; echo "--- gates ---"; tool | 0 | 117515 |
| 5 | ['tools/origin', 'task', 'verify', 'T-0022'] | 0 | 111376 |

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
| 1 | 23:10:09 | session_start | implement 'origin release check' so RELEASE-MANIFEST.md is machine-enforced, and repair the front-door documents it exposes as false |
| 2 | 23:17:40 | command | $ bash -c cd /home/ubuntu/think-free PYTHONPATH=tools python3 - <<"PY" import pathlib, shutil, tempfile from originlib import release  base = |
| 3 | 23:17:55 | command | $ bash -c cd /home/ubuntu/think-free cp RELEASE-MANIFEST.md /tmp/opencode/relfix/new-manifest.md cp /tmp/opencode/relfix/RELEASE-MANIFEST.md R |
| 4 | 23:22:19 | command | $ bash -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^Ran\|^OK\|^FAILED"; echo "--- gates ---"; tools |
| 5 | 23:24:39 | command | $ tools/origin task verify T-0022 |
| 6 | 23:24:47 | artifact | wrote tools/originlib/release.py |
| 7 | 23:24:47 | note | tests/test_release.py declares origin-allow-secret-patterns: github-token; suppressed for this file only |
| 8 | 23:24:47 | artifact | wrote tests/test_release.py |
| 9 | 23:24:47 | artifact | wrote tools/originlib/cli.py |
| 10 | 23:24:47 | artifact | wrote tools/originlib/cli_repo.py |
| 11 | 23:24:47 | artifact | wrote RELEASE-MANIFEST.md |
| 12 | 23:24:47 | artifact | wrote README.md |
| 13 | 23:24:47 | artifact | wrote ROADMAP.md |
| 14 | 23:24:47 | artifact | wrote STATE.md |
| 15 | 23:24:47 | artifact | wrote STATE-history.md |
| 16 | 23:24:47 | artifact | wrote AGENTS.md |
| 17 | 23:24:47 | artifact | wrote docs/reference/cli-reference.md |
| 18 | 23:24:47 | artifact | wrote tests/README.md |
| 19 | 23:24:47 | artifact | wrote .github/workflows/ci.yml |
| 20 | 23:24:47 | artifact | wrote tasks/T-0022-implement-origin-release-check-so-release-manife.md |
| 21 | 23:24:47 | artifact | wrote sessions/2026-10-03-038-implement-origin-release-check-so-releas/README.md |
| 22 | 23:24:47 | artifact | wrote sessions/2026-10-03-038-implement-origin-release-check-so-releas/commands.log |
| 23 | 23:24:48 | artifact | wrote sessions/2026-10-03-038-implement-origin-release-check-so-releas/events.jsonl |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-038-implement-origin-release-check-so-releas/events.jsonl
```

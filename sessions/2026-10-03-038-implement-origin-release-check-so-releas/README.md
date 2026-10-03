# Session 2026-10-03-038-implement-origin-release-check-so-releas

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T23:10:09+00:00
- **Duration:** 957.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

implement 'origin release check' so RELEASE-MANIFEST.md is machine-enforced, and repair the front-door documents it exposes as false

## Summary

Implemented origin release check (T-0022): RELEASE-MANIFEST.md said three times that nothing enforced it, and the first run reported 14 real violations - nine tracked top-level entries classified by neither table and so published or withheld by accident, three paths declared public that do not exist and had no way to say so, the missing release-state directive, and a credential-shaped fixture in the check's own new test file. Six properties enforced, 29 tests seeding one defect per clause plus a fixture that passes. A declared file classifies only itself, so docs/policy/one.md does not make docs/ public; .agents/ and .claude/ are declared as directories for that reason. CI gains a sixth step inserted after Documentation lint so the VM holding T-0020 can rebase cleanly. The check enforces agreement between manifest and README, not truth, and all three places that claim say so. Also corrected two false statements in the front door while there: the README described four sealed investigations and two experiments when there are six and nine.

## Next

Unclaimed infrastructure work left: headless task-runner script for VMs (a VM exists now, so the roadmap's 'once a VM exists' condition is met) and 'origin release check' is now done. Scheduling and supervision need user authorization and must not be started. Three documents remain false and unclaimed: docs/operations/github-app.md still says no GitHub App exists, docs/operations/vm-execution.md requires Python 3.11+ while this VM runs 3.8.10 with the suite green, and both are repairable in one task. E2 side B stays time-gated. T-0020 remains claimed on instance-20260717-0947.

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
| 24 | 23:26:06 | doc_update | updated ROADMAP.md |
| 25 | 23:26:06 | doc_update | updated STATE.md |
| 26 | 23:26:06 | session_end | Implemented origin release check (T-0022): RELEASE-MANIFEST.md said three times that nothing enforced it, and the first run reported 14 real violation |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-038-implement-origin-release-check-so-releas/events.jsonl
```

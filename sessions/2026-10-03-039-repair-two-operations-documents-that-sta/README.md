# Session 2026-10-03-039-repair-two-operations-documents-that-sta

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T23:26:36+00:00
- **Duration:** 616.5s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

repair two operations documents that state requirements the repository has already falsified

## Summary

Repaired four operations documents that told a fresh VM something untrue, all public. vm-execution.md and bootstrap.md required Python 3.11+ from the development machine's 3.14.6, while this VM runs 3.8.10 with 232 tests green; both now state what is exercised and name the missing Python equivalent of tests/git-versions.json. github-app.md claimed no GitHub App exists while 123 of 133 commits carry a [bot] App identity; it now separates observed from unverified, marks its least-privilege table as a design to check against rather than a reading of reality, and records the result of the key-handling check it was waiting on. That check turned up a private key at mode 0644 inside a 0700 directory on this VM, repaired to 0600. ci.md was stale in the same family: five gates listed, sixth missed, preflight described as covering four when it covers three. Left open and recorded rather than silently fixed: the App's real permissions are unobservable from here, and doctor checks credential environment variables while the App uses a key file, so a VM with a broken helper reports healthy.

## Next

Unclaimed and genuinely useful: (a) a machine-readable record of the Python versions the suite is verified on, mirroring tests/git-versions.json; (b) a credential-presence check in doctor for a key-file App, so a broken helper stops looking healthy; (c) a headless task-runner script for VMs - the roadmap's 'once a VM exists' condition is now met, but scheduling and supervision still need the user's authorization and must not be started. T-0020 remains claimed on instance-20260717-0947 and is the only in-flight work. E2 side B stays time-gated until days after side A.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| docs/operations/bootstrap.md | 18bb52c91159 | 3844 |
| docs/operations/ci.md | c8b2cf1d227d | 5115 |
| docs/operations/github-app.md | 0da6fb258b75 | 8245 |
| docs/operations/vm-execution.md | 9def01d4f00d | 5136 |
| ROADMAP.md | 5eaafddf0df0 | 8844 |
| STATE.md | f184dec2c444 | 21211 |
| STATE-history.md | ca3d7fd131b9 | 16534 |
| tasks/T-0023-repair-the-two-operations-documents-whose-stated.md | 4ffd2d103a60 | 4138 |
| sessions/2026-10-03-039-repair-two-operations-documents-that-sta/README.md | 77e7e6d54f66 | 2602 |
| sessions/2026-10-03-039-repair-two-operations-documents-that-sta/commands.log | 2e6a82c18dff | 5625 |
| sessions/2026-10-03-039-repair-two-operations-documents-that-sta/events.jsonl | b3dbca1c304c | 10936 |

## Commands

5 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', 'cd /home/ubuntu/think-free\necho "python3: $(python3 --version 2>&1)"\necho "--- author census over all commits ---"\ngit log --format | 0 | 103 |
| 3 | ['bash', '-c', 'cd /home/ubuntu/think-free\necho "--- does the App key material appear anywhere in the repository? ---"\nPYTHONPATH=tools python3 - << | 0 | 1134 |
| 4 | ['bash', '-c', 'cd /home/ubuntu/think-free\nPYTHONPATH=tools python3 - <<"PY"\nimport pathlib\nfrom originlib import secrets\np = pathlib.Path(".origi | 0 | 127 |
| 5 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^Ran\|^OK\|^FAILED"; echo "--- gates ---"; tool | 0 | 114733 |
| 6 | ['tools/origin', 'task', 'verify', 'T-0023'] | 0 | 111683 |

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
| 1 | 23:26:36 | session_start | repair two operations documents that state requirements the repository has already falsified |
| 2 | 23:27:05 | command | $ bash -c cd /home/ubuntu/think-free echo "python3: $(python3 --version 2>&1)" echo "--- author census over all commits ---" git log --format= |
| 3 | 23:27:39 | command | $ bash -c cd /home/ubuntu/think-free echo "--- does the App key material appear anywhere in the repository? ---" PYTHONPATH=tools python3 - << |
| 4 | 23:27:49 | command | $ bash -c cd /home/ubuntu/think-free PYTHONPATH=tools python3 - <<"PY" import pathlib from originlib import secrets p = pathlib.Path(".origin/ |
| 5 | 23:34:18 | command | $ bash -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 \| grep -E "^Ran\|^OK\|^FAILED"; echo "--- gates ---"; tools |
| 6 | 23:36:23 | command | $ tools/origin task verify T-0023 |
| 7 | 23:36:32 | artifact | wrote docs/operations/bootstrap.md |
| 8 | 23:36:32 | artifact | wrote docs/operations/ci.md |
| 9 | 23:36:32 | artifact | wrote docs/operations/github-app.md |
| 10 | 23:36:32 | artifact | wrote docs/operations/vm-execution.md |
| 11 | 23:36:32 | artifact | wrote ROADMAP.md |
| 12 | 23:36:32 | artifact | wrote STATE.md |
| 13 | 23:36:33 | artifact | wrote STATE-history.md |
| 14 | 23:36:33 | artifact | wrote tasks/T-0023-repair-the-two-operations-documents-whose-stated.md |
| 15 | 23:36:33 | artifact | wrote sessions/2026-10-03-039-repair-two-operations-documents-that-sta/README.md |
| 16 | 23:36:33 | artifact | wrote sessions/2026-10-03-039-repair-two-operations-documents-that-sta/commands.log |
| 17 | 23:36:33 | artifact | wrote sessions/2026-10-03-039-repair-two-operations-documents-that-sta/events.jsonl |
| 18 | 23:36:52 | doc_update | updated ROADMAP.md |
| 19 | 23:36:52 | doc_update | updated STATE.md |
| 20 | 23:36:52 | session_end | Repaired four operations documents that told a fresh VM something untrue, all public. vm-execution.md and bootstrap.md required Python 3.11+ from the  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-039-repair-two-operations-documents-that-sta/events.jsonl
```

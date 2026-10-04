# Session 2026-10-04-013-t-0035-stop-the-credential-sandbox-from

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-04T04:37:16+00:00
- **Duration:** 1194.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `task/T-0035-instance-20260717-0944`

## Goal

T-0035: stop the credential sandbox from inheriting a CI runner's GITHUB_TOKEN

## Summary

T-0035: the credential sandbox inherited a CI runner's GITHUB_TOKEN, which pushprobe counts as a credential mechanism, so a test asserting 'unavailable' read 'broken'. Three CI runs were red while both VMs were green. Found by reproducing with the variable set rather than by reading the run, and confirmed against 4401bd2c, so it arrived with the fixture in T-0025. Falsified three ways, the third found by falsifying: a fixture that clears but never restores leaves every test green. Recorded as defect 7 - a defect that only reproduces where the author does not work. 380 tests green with and without tokens exported.

## Next

Land the branch. T-0034 (VM 0947) is in flight on the Python-version matrix and is the right next piece of work; do not start it here. After it lands, the remaining unchecked ROADMAP items are seeding tasks from STATE-next-actions and headless supervision, which needs authorization.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| tests/pushcred_fixture.py | 12f674d59e0d | 4505 |
| tests/test_pushcred.py | 106d13a254bd | 13009 |
| docs/operations/doctor.md | bf850348e850 | 8871 |
| tests/README.md | 9358dfcffb1c | 10096 |
| STATE.md | 213c5b5de62e | 24025 |
| STATE-defects.md | 576d63e564da | 9675 |
| STATE-next-actions.md | e4726e5d49bc | 6276 |
| ROADMAP.md | 3f635602d71c | 13035 |
| tasks/T-0035-stop-the-credential-sandbox-from-inheriting-a-ci.md | d92134f31ae0 | 5527 |

## Commands

7 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['sh', '-c', '\necho "=== FALSIFICATION: pre-fix fixture (inherits the environment) ==="\npython3 - <<PY\nfrom pathlib import Path\np=Path("tests/push | 0 | 12814 |
| 3 | ['python3', '/tmp/opencode/falsify35.py'] | 0 | 11773 |
| 4 | ['python3', '/tmp/opencode/falsify35.py'] | 0 | 11999 |
| 5 | ['python3', '/tmp/opencode/falsify35.py'] | 0 | 12311 |
| 6 | ['python3', '/tmp/opencode/falsify35.py'] | 0 | 12510 |
| 7 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; echo "--- with runner tokens ---"; GITHUB_TOKEN=x G | 0 | 398593 |
| 19 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -3; tools/origin doc lint --quiet; echo "lint=$?"; tool | 0 | 202816 |

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
| 1 | 04:37:16 | session_start | T-0035: stop the credential sandbox from inheriting a CI runner's GITHUB_TOKEN |
| 2 | 04:38:24 | command | $ sh -c  echo "=== FALSIFICATION: pre-fix fixture (inherits the environment) ===" python3 - <<PY from pathlib import Path p=Path("tests/pushcr |
| 3 | 04:38:46 | command | $ python3 /tmp/opencode/falsify35.py |
| 4 | 04:39:08 | command | $ python3 /tmp/opencode/falsify35.py |
| 5 | 04:39:38 | command | $ python3 /tmp/opencode/falsify35.py |
| 6 | 04:40:13 | command | $ python3 /tmp/opencode/falsify35.py |
| 7 | 04:47:42 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -4; echo "--- with runner tokens ---"; GITHUB_TOKEN=x |
| 8 | 04:47:49 | note | tests/pushcred_fixture.py declares origin-allow-secret-patterns: github-app-private-key, github-token; suppressed for this file only |
| 9 | 04:47:49 | artifact | wrote tests/pushcred_fixture.py |
| 10 | 04:47:49 | note | tests/test_pushcred.py declares origin-allow-secret-patterns: github-token; suppressed for this file only |
| 11 | 04:47:49 | artifact | wrote tests/test_pushcred.py |
| 12 | 04:47:49 | artifact | wrote docs/operations/doctor.md |
| 13 | 04:47:49 | artifact | wrote tests/README.md |
| 14 | 04:53:32 | artifact | wrote STATE.md |
| 15 | 04:53:32 | artifact | wrote STATE-defects.md |
| 16 | 04:53:32 | artifact | wrote STATE-next-actions.md |
| 17 | 04:53:32 | artifact | wrote ROADMAP.md |
| 18 | 04:53:32 | artifact | wrote tasks/T-0035-stop-the-credential-sandbox-from-inheriting-a-ci.md |
| 19 | 04:56:55 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1\|tail -3; tools/origin doc lint --quiet; echo "lint=$?"; too |
| 20 | 04:57:10 | doc_update | updated ROADMAP.md |
| 21 | 04:57:10 | doc_update | updated STATE.md |
| 22 | 04:57:10 | session_end | T-0035: the credential sandbox inherited a CI runner's GITHUB_TOKEN, which pushprobe counts as a credential mechanism, so a test asserting 'unavailabl |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-013-t-0035-stop-the-credential-sandbox-from/events.jsonl
```

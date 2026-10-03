# Session 2026-10-03-004-stop-declaring-gitignored-build-output-a

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T17:18:33+05:30
- **Duration:** 37.5s
- **Host:** `fedora`
- **Branch:** `research/origin`

## Goal

stop declaring gitignored build output as artifacts

## Summary

Found and fixed a defect in the sweep introduced minutes earlier: --dir tools declared 13 gitignored .pyc files as artifacts. Gitignored paths are now refused by name and skipped by sweep, with three tests. Recorded as FAILURES F004 and DECISIONS D014. 133 tests green, all gates pass.

## Next

Write falsification kill gates for the three held candidates in HYPOTHESES.md (task T-0001). No candidate may be tested before its gate exists.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| FAILURES.md | 72c69ce5bb1e | 7552 |
| docs/policy/logging-standard.md | 82f257dd74b7 | 6031 |
| .agents/skills/session-lifecycle/SKILL.md | 4b65f483ef1b | 5303 |
| tools/originlib/gitutil.py | 14ef5ccf3fac | 3675 |
| tools/originlib/sessionlog.py | c5d4ee1e69c2 | 3922 |
| tools/originlib/cli_session.py | e310044ab06f | 9864 |
| tests/test_session.py | d1b072584697 | 13540 |
| DECISIONS.md | 64266c7fa168 | 9931 |
| STATE.md | 44477777ed81 | 6266 |
| README.md | b71d55f9ede0 | 4409 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 12 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 3153 |
| 13 | ['./tools/origin', 'preflight'] | 0 | 130 |

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
| 1 | 17:18:33 | session_start | stop declaring gitignored build output as artifacts |
| 2 | 17:18:33 | note | Found while reading session 003's generated report: the new --dir sweep declared 13 __pycache__/*.pyc files, because the sweep took every file under t |
| 3 | 17:18:39 | artifact | wrote FAILURES.md |
| 4 | 17:18:39 | artifact | wrote docs/policy/logging-standard.md |
| 5 | 17:18:39 | artifact | wrote .agents/skills/session-lifecycle/SKILL.md |
| 6 | 17:18:39 | artifact | wrote tools/originlib/gitutil.py |
| 7 | 17:18:39 | artifact | wrote tools/originlib/sessionlog.py |
| 8 | 17:18:39 | artifact | wrote tools/originlib/cli_session.py |
| 9 | 17:18:39 | note | tests/test_session.py declares origin-allow-secret-patterns: github-token; suppressed for this file only |
| 10 | 17:18:39 | artifact | wrote tests/test_session.py |
| 11 | 17:18:39 | decision | a directory sweep skips gitignored files and naming one directly is refused, because build output is reproducible from the declared source |
| 12 | 17:18:42 | command | $ python3 -m unittest discover -s tests -t tests |
| 13 | 17:18:43 | command | $ ./tools/origin preflight |
| 14 | 17:19:05 | artifact | wrote DECISIONS.md |
| 15 | 17:19:05 | artifact | wrote STATE.md |
| 16 | 17:19:05 | artifact | wrote README.md |
| 17 | 17:19:10 | milestone | D014 recorded; state and readme counts updated |
| 18 | 17:19:11 | doc_update | updated DECISIONS.md |
| 19 | 17:19:11 | doc_update | updated FAILURES.md |
| 20 | 17:19:11 | doc_update | updated STATE.md |
| 21 | 17:19:11 | session_end | Found and fixed a defect in the sweep introduced minutes earlier: --dir tools declared 13 gitignored .pyc files as artifacts. Gitignored paths are now |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-004-stop-declaring-gitignored-build-output-a/events.jsonl
```

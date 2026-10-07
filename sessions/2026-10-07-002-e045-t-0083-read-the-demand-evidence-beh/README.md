# Session 2026-10-07-002-e045-t-0083-read-the-demand-evidence-beh

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-07T06:21:32+00:00
- **Duration:** 3283.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E045 (T-0083): read the demand evidence behind the only candidate, ask who the requester is, and decide which population the candidate may be evaluated against

## Summary

E045 read all 189 unique issues in E038's cached demand corpus row by row, recording per row the requester and the interface it says it lacks. The population STATE-next-actions.md item 0a was built to measure does not exist in the evidence: 29 of 189 rows are about choosing which lines reach the index, 28 carry explicit diff access and the 29th GUI-implied, and none carries none (F081). All ten automated callers in the need rows name their own diff access. Three of the four issues F064 cites are not evidence of what they were cited for. The same reading killed the differentiator: the 29 rows name 26 distinct repositories, two of them shipped installable command-line tools taking stg's coordinate, one of which has already run the two-arm agent experiment item 0a was built around (F082). stg is withdrawn as a candidate and stays in the repository as a correct tool: 37/37 tests, index byte-identical to a hand-built patch, honest exits, unreleased. A server restart interrupted the session after it left 12 doc-lint violations; those were repaired here by invariant, not by shortening prose -- the two verbatim prior-art captures moved under raw/sources/ as .txt (the class E038 already declared exempt), read.py split into read.py/rules.py/report.py, three ../ links that left the repository fixed, doc index regenerated. The split was verified behaviour-preserving: read.py reproduces raw/issues.jsonl byte-identical and the same stdout. doc lint exits 0, captured in this session's command log.

## Next

The named next action was the hook observation E045 left unpromoted. Reading both rows verbatim, as D077 requires, inverts it: nextjs-app-template#95 is a report that lefthook 2.x does NOT sweep unstaged hunks -- it hides the unstaged half exactly as lint-staged does, and the repository's own warning is the stale part -- while agent-orchestra#154's own review record shows a reviewer raising exactly the sweep hazard and the defense being SUSTAINED as out of scope. So the two rows disagree about the premise, and the shipped tool named as the offender is the one shown to fix it. Establish the fact against the real tools with a byte-level oracle on the index rather than against two issue bodies; declare the failure condition first.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/045-demand-evidence/README.md | 217fded4422e | 11158 |
| EXPERIMENTS/045-demand-evidence/raw/hand-labels.tsv | f9cfe652eae0 | 6771 |
| EXPERIMENTS/045-demand-evidence/raw/issues.jsonl | 4d88ed25db9a | 250571 |
| EXPERIMENTS/045-demand-evidence/raw/sources/gah-README.txt | 97cc0aff4967 | 6040 |
| EXPERIMENTS/045-demand-evidence/raw/sources/git-hunk-README.txt | e6082d9e429d | 17729 |
| EXPERIMENTS/045-demand-evidence/read.py | 7bebe0402680 | 7374 |
| EXPERIMENTS/045-demand-evidence/rules.py | d79fe9c65dd1 | 7419 |
| EXPERIMENTS/045-demand-evidence/report.py | 956c19799a08 | 5889 |
| STATE-in-flight-7.md | 1916eeb45a1e | 7527 |
| HYPOTHESES-candidates-2.md | 4f3afb0e5c05 | 10173 |

## Commands

6 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/045-demand-evidence/read.py'] | 0 | 7113 |
| 3 | ['python3', '-c', "\nimport json\nrows=[json.loads(l) for l in open('EXPERIMENTS/045-demand-evidence/raw/issues.jsonl')]\nrows.sort(key=lambda r:(r['r | 1 | 591 |
| 4 | ['python3', '-c', "\nimport json\nrows=[json.loads(l) for l in open('EXPERIMENTS/045-demand-evidence/raw/issues.jsonl')]\nneed=[r for r in rows if r[' | 0 | 158 |
| 5 | ['tools/origin', 'doc', 'lint'] | 2 | 728970 |
| 6 | ['tools/origin', 'doc', 'lint'] | 2 | 867699 |
| 18 | ['tools/origin', 'doc', 'lint'] | 0 | 102503 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 7 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-12.md |
|   undeclared | DECISIONS.md |
|   undeclared | FAILURES-findings-30.md |
|   undeclared | FAILURES.md |
|   undeclared | HYPOTHESES-candidates.md |
|   undeclared | STATE-next-actions.md |
|   undeclared | STATE.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 06:21:32 | session_start | E045 (T-0083): read the demand evidence behind the only candidate, ask who the requester is, and decide which population the candidate may be evaluate |
| 2 | 06:25:06 | command | $ python3 EXPERIMENTS/045-demand-evidence/read.py |
| 3 | 06:25:13 | command | $ python3 -c  import json rows=[json.loads(l) for l in open('EXPERIMENTS/045-demand-evidence/raw/issues.jsonl')] rows.sort(key=lambda r:(r['re |
| 4 | 06:25:31 | command | $ python3 -c  import json rows=[json.loads(l) for l in open('EXPERIMENTS/045-demand-evidence/raw/issues.jsonl')] need=[r for r in rows if r['h |
| 5 | 06:41:45 | command | $ tools/origin doc lint |
| 6 | 06:45:23 | command | $ tools/origin doc lint |
| 7 | 07:09:17 | artifact | wrote EXPERIMENTS/045-demand-evidence/README.md |
| 8 | 07:09:20 | artifact | wrote EXPERIMENTS/045-demand-evidence/raw/hand-labels.tsv |
| 9 | 07:09:21 | artifact | wrote EXPERIMENTS/045-demand-evidence/raw/issues.jsonl |
| 10 | 07:09:23 | artifact | wrote EXPERIMENTS/045-demand-evidence/raw/sources/gah-README.txt |
| 11 | 07:09:24 | artifact | wrote EXPERIMENTS/045-demand-evidence/raw/sources/git-hunk-README.txt |
| 12 | 07:09:25 | artifact | wrote EXPERIMENTS/045-demand-evidence/read.py |
| 13 | 07:09:26 | artifact | wrote EXPERIMENTS/045-demand-evidence/rules.py |
| 14 | 07:09:26 | artifact | wrote EXPERIMENTS/045-demand-evidence/report.py |
| 15 | 07:09:27 | artifact | wrote STATE-in-flight-7.md |
| 16 | 07:09:28 | artifact | wrote HYPOTHESES-candidates-2.md |
| 17 | 07:10:28 | milestone | Repaired the 12 lint violations this session left behind: the two verbatim prior-art captures moved to raw/sources/ as .txt (the class E038 already de |
| 18 | 07:12:18 | command | $ tools/origin doc lint |
| 19 | 07:16:15 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-12.md |
| 20 | 07:16:15 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 21 | 07:16:15 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-30.md |
| 22 | 07:16:15 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 23 | 07:16:15 | unlogged_change | changed but never declared as an artifact: HYPOTHESES-candidates.md |
| 24 | 07:16:15 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 25 | 07:16:15 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 26 | 07:16:15 | doc_update | updated DECISIONS-SCREENING-12.md |
| 27 | 07:16:15 | doc_update | updated DECISIONS.md |
| 28 | 07:16:15 | doc_update | updated FAILURES.md |
| 29 | 07:16:15 | doc_update | updated STATE.md |
| 30 | 07:16:15 | session_end | E045 read all 189 unique issues in E038's cached demand corpus row by row, recording per row the requester and the interface it says it lacks. The pop |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-07-002-e045-t-0083-read-the-demand-evidence-beh/events.jsonl
```

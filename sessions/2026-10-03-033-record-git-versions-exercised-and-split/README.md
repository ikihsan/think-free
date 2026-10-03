# Session 2026-10-03-033-record-git-versions-exercised-and-split

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T22:17:34+00:00
- **Duration:** 444.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Record git versions exercised and split DECISIONS-PRACTICE.md before the cap

## Summary

T-0018: machine-readable exercised-git-versions record plus invariant split of DECISIONS-PRACTICE.md; 176 tests green, lint and skills gates pass

## Next

T-0017 attribution on 0944; E2 lockfile snapshot still unscheduled

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| DECISIONS-GATING.md | 0bbd5b102185 | 10184 |
| tests/git-versions.json | 4841c7f6841c | 884 |
| tests/test_gitversions.py | c6a31ca977d3 | 1637 |
| DECISIONS.md | aad43fda8842 | 1914 |
| DECISIONS-PRACTICE.md | 09cd93dac7e3 | 8246 |
| STATE.md | c1e7f5128a64 | 19655 |
| ROADMAP.md | 5e2b50aa5ae9 | 7177 |
| tests/README.md | 5ec6b3c00139 | 2559 |
| docs/operations/ci.md | feb589c4881e | 4459 |
| docs/process/session-protocol.md | c5bcbc26ee20 | 6258 |
| docs/reference/cli-reference.md | 255abcb6e0db | 5878 |
| docs/reference/repo-map.md | 5b28b4aad603 | 4538 |
| docs/process/experiment-protocol.md | 4e7fd3b44c3d | 5216 |
| tools/originlib/paths.py | e7cbf55b9042 | 3364 |
| tools/originlib/reconcile.py | 3f9816235e9f | 5131 |
| AGENTS.md | 6b69591613ec | 7952 |
| RELEASE-MANIFEST.md | 68973b268467 | 2751 |
| .agents/skills/session-lifecycle/SKILL.md | 14e041a9e18d | 5819 |
| .agents/skills/evidence-record/SKILL.md | fe0124430714 | 5079 |
| tasks/T-0018-record-exercised-git-versions-machine-readably-a.md | 1955a925c9d5 | 1523 |

## Commands

5 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['tools/origin', 'doc', 'lint'] | 0 | 1295 |
| 4 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 93670 |
| 5 | ['tools/origin', 'skills', 'check'] | 0 | 421 |
| 6 | ['tools/origin', 'skills', 'verify'] | 0 | 374 |
| 7 | ['tools/origin', 'task', 'verify', 'T-0018'] | 0 | 96028 |

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
| 1 | 22:17:34 | session_start | Record git versions exercised and split DECISIONS-PRACTICE.md before the cap |
| 2 | 22:18:28 | milestone | T-0018 created, claimed, and pushed; starting implementation |
| 3 | 22:20:55 | command | $ tools/origin doc lint |
| 4 | 22:22:33 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 5 | 22:22:40 | command | $ tools/origin skills check |
| 6 | 22:22:41 | command | $ tools/origin skills verify |
| 7 | 22:24:32 | command | $ tools/origin task verify T-0018 |
| 8 | 22:24:44 | artifact | wrote DECISIONS-GATING.md |
| 9 | 22:24:44 | artifact | wrote tests/git-versions.json |
| 10 | 22:24:44 | artifact | wrote tests/test_gitversions.py |
| 11 | 22:24:44 | artifact | wrote DECISIONS.md |
| 12 | 22:24:44 | artifact | wrote DECISIONS-PRACTICE.md |
| 13 | 22:24:46 | artifact | wrote STATE.md |
| 14 | 22:24:46 | artifact | wrote ROADMAP.md |
| 15 | 22:24:46 | artifact | wrote tests/README.md |
| 16 | 22:24:46 | artifact | wrote docs/operations/ci.md |
| 17 | 22:24:46 | artifact | wrote docs/process/session-protocol.md |
| 18 | 22:24:46 | artifact | wrote docs/reference/cli-reference.md |
| 19 | 22:24:47 | artifact | wrote docs/reference/repo-map.md |
| 20 | 22:24:47 | artifact | wrote docs/process/experiment-protocol.md |
| 21 | 22:24:47 | artifact | wrote tools/originlib/paths.py |
| 22 | 22:24:47 | artifact | wrote tools/originlib/reconcile.py |
| 23 | 22:24:48 | artifact | wrote AGENTS.md |
| 24 | 22:24:48 | artifact | wrote RELEASE-MANIFEST.md |
| 25 | 22:24:48 | artifact | wrote .agents/skills/session-lifecycle/SKILL.md |
| 26 | 22:24:48 | artifact | wrote .agents/skills/evidence-record/SKILL.md |
| 27 | 22:24:48 | artifact | wrote tasks/T-0018-record-exercised-git-versions-machine-readably-a.md |
| 28 | 22:24:50 | milestone | T-0018 implementation complete: 176 tests green, doc lint OK, skills checks OK, task verify exit 0 |
| 29 | 22:24:58 | doc_update | updated DECISIONS-GATING.md |
| 30 | 22:24:58 | doc_update | updated DECISIONS-PRACTICE.md |
| 31 | 22:24:58 | doc_update | updated DECISIONS.md |
| 32 | 22:24:58 | doc_update | updated ROADMAP.md |
| 33 | 22:24:58 | doc_update | updated STATE.md |
| 34 | 22:24:58 | session_end | T-0018: machine-readable exercised-git-versions record plus invariant split of DECISIONS-PRACTICE.md; 176 tests green, lint and skills gates pass |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-033-record-git-versions-exercised-and-split/events.jsonl
```

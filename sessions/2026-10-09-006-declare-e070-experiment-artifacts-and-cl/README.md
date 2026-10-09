# Session 2026-10-09-006-declare-e070-experiment-artifacts-and-cl

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T10:30:22+00:00
- **Duration:** 25.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Declare E070 experiment artifacts and close session

## Summary

E070 measured pip's 'did you mean' name guard gap across PyPI and Crates.io ecosystems. 0/50 PyPI names and 0/50 Crates.io names received 'did you mean' warnings from pip install --dry-run. Kill gate G3 FAILed (gap fraction lower CI95 = 0.929 ≥ 0.15 threshold), verdict: KILL — pip's name guard gap is too large across ecosystems, closing the claim that pip's warning adequately protects users. The E069 lesson (gate with vacuous passing region cannot fail) was validated by designing G3 with non-vacuous passing/failing regions. Negative result recorded as F103 in FAILURES-findings-35.md. Experiment infrastructure in EXPERIMENTS/070-name-guard-gap/. Next action: fresh observation in new domain per D080.

## Next

fresh-observation-E071

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| FAILURES-findings-35.md | f7b3f0a3b6bb | 9771 |
| EXPERIMENTS/070-name-guard-gap/PROTOCOL.md | ea457cdaf32a | 6101 |
| EXPERIMENTS/070-name-guard-gap/control.py | 80d4bcf0e095 | 8516 |
| EXPERIMENTS/070-name-guard-gap/results.json | 54bd1fd98be6 | 770 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-09-005-e070-experiment-completion-and-session-c/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:30:22 | session_start | Declare E070 experiment artifacts and close session |
| 2 | 10:30:32 | artifact | E070 experiment files |
| 3 | 10:30:33 | artifact | E070 experiment files |
| 4 | 10:30:33 | artifact | E070 experiment files |
| 5 | 10:30:34 | artifact | E070 experiment files |
| 6 | 10:30:47 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-09-005-e070-experiment-completion-and-session-c/events.jsonl |
| 7 | 10:30:47 | session_end | E070 measured pip's 'did you mean' name guard gap across PyPI and Crates.io ecosystems. 0/50 PyPI names and 0/50 Crates.io names received 'did you mea |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-006-declare-e070-experiment-artifacts-and-cl/events.jsonl
```

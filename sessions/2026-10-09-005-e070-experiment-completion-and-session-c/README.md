# Session 2026-10-09-005-e070-experiment-completion-and-session-c

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-09
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T10:28:02+00:00
- **Duration:** 20.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

E070 experiment completion and session close

## Summary

E070 measured pip's 'did you mean' name guard gap across PyPI and Crates.io ecosystems. 0/50 PyPI names and 0/50 Crates.io names received 'did you mean' warnings from pip install --dry-run. Kill gate G3 FAILed (gap fraction lower CI95 = 0.929 ≥ 0.15 threshold), verdict: KILL — pip's name guard gap is too large across ecosystems, closing the claim that pip's warning adequately protects users. The E069 lesson (gate with vacuous passing region cannot fail) was validated by designing G3 with non-vacuous passing/failing regions. Negative result recorded as F103 in FAILURES-findings-35.md. Experiment infrastructure in EXPERIMENTS/070-name-guard-gap/. Next action: fresh observation in new domain per D080.

## Next

fresh-observation-E071

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/070-name-guard-gap/PROTOCOL.md |
|   undeclared | EXPERIMENTS/070-name-guard-gap/control.py |
|   undeclared | EXPERIMENTS/070-name-guard-gap/results.json |
|   undeclared | FAILURES-findings-35.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 10:28:02 | session_start | E070 experiment completion and session close |
| 2 | 10:28:23 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-name-guard-gap/PROTOCOL.md |
| 3 | 10:28:23 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-name-guard-gap/control.py |
| 4 | 10:28:23 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/070-name-guard-gap/results.json |
| 5 | 10:28:23 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-35.md |
| 6 | 10:28:23 | session_end | E070 measured pip's 'did you mean' name guard gap across PyPI and Crates.io ecosystems. 0/50 PyPI names and 0/50 Crates.io names received 'did you mea |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-005-e070-experiment-completion-and-session-c/events.jsonl
```

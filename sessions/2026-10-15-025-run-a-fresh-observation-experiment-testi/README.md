# Session 2026-10-15-025-run-a-fresh-observation-experiment-testi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T20:15:40+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run a fresh observation experiment testing the view-count principle on VS Code Marketplace, chosen by stated rule: largest untouched extension marketplace with exposable per-item install-count metadata

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/151-vscode-marketplace-viewcount/PROTOCOL.md | 38f51dfb9193 | 7106 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/run.py | cf4a4b78c1ca | 10378 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/classifier.py | ab6c2e6b91db | 7065 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/RESULT.md | 72549b15ff73 | 2047 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIER.md | 28af4b55ce5c | 3110 |
| docs/reference/VIEW-COUNT-SUMMARY.md | f1b272d3df73 | 5415 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/RAW_DATA.jsonl | fd8c705583af | 813551 |
| EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIED.jsonl | 513d4e5f18ea | 807255 |

## Commands

0 captured, 0 non-zero exit.

_none_

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
| 1 | 20:15:40 | session_start | Run a fresh observation experiment testing the view-count principle on VS Code Marketplace, chosen by stated rule: largest untouched extension marketp |
| 2 | 21:10:46 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/PROTOCOL.md |
| 3 | 21:10:54 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/run.py |
| 4 | 21:11:09 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/classifier.py |
| 5 | 21:11:20 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/RESULT.md |
| 6 | 21:11:33 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIER.md |
| 7 | 21:11:44 | artifact | wrote docs/reference/VIEW-COUNT-SUMMARY.md |
| 8 | 21:11:51 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/RAW_DATA.jsonl |
| 9 | 21:12:00 | artifact | wrote EXPERIMENTS/151-vscode-marketplace-viewcount/CLASSIFIED.jsonl |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-025-run-a-fresh-observation-experiment-testi/events.jsonl
```

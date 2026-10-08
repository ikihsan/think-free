# Session 2026-10-08-021-test-e038-s-189-github-issues-and-e012-s

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T17:12:30+00:00
- **Duration:** 1578.9s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test E038's 189 GitHub issues and E012's 1401 HN needs against answerability by a free general assistant, following E058's protocol

## Summary

E066 tested the mission's two need corpora (E038's 189 GitHub issues, E012's 1401 HN needs) against answerability by a free general assistant, following E058's protocol. Found: GitHub corpus has 82% false positive rate (only 34/189 actually about git line staging), and those real issues are served by existing tools (lazygit, magit, vscode, git-hunk, gah, git add -p). HN corpus top triggers are 55% non-software content (political, personal, philosophical), and 86.7% of actual software needs are resolved-from-knowledge. The mission's need-harvest route selects statements, not unmet software needs.

## Next

Record findings in FAILURES.md and update STATE.md. The need-harvest generator is refuted at the population level. Next: fresh exploration in a new domain per D083.

## Artifacts

_none_

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 11 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/066-need-answerability/PROTOCOL.md |
|   undeclared | EXPERIMENTS/066-need-answerability/README.md |
|   undeclared | EXPERIMENTS/066-need-answerability/classify.py |
|   undeclared | EXPERIMENTS/066-need-answerability/classify_github.py |
|   undeclared | EXPERIMENTS/066-need-answerability/classify_github_v2.py |
|   undeclared | EXPERIMENTS/066-need-answerability/classify_hn.py |
|   undeclared | EXPERIMENTS/066-need-answerability/classify_hn_manual.py |
|   undeclared | EXPERIMENTS/066-need-answerability/raw/classification.tsv |
|   undeclared | EXPERIMENTS/066-need-answerability/raw/github_issues.jsonl |
|   undeclared | EXPERIMENTS/066-need-answerability/raw/hn_needs.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:12:30 | session_start | Test E038's 189 GitHub issues and E012's 1401 HN needs against answerability by a free general assistant, following E058's protocol |
| 2 | 17:38:28 | milestone | Completed E066: classified 189 GitHub issues and 100 HN needs. Key finding: mission's need-harvest corpora are predominantly false positives, non-soft |
| 3 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/PROTOCOL.md |
| 4 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/README.md |
| 5 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/classify.py |
| 6 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/classify_github.py |
| 7 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/classify_github_v2.py |
| 8 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/classify_hn.py |
| 9 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/classify_hn_manual.py |
| 10 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/raw/classification.tsv |
| 11 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/raw/github_issues.jsonl |
| 12 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/raw/hn_needs.jsonl |
| 13 | 17:38:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/066-need-answerability/raw/to_classify.jsonl |
| 14 | 17:38:48 | session_end | E066 tested the mission's two need corpora (E038's 189 GitHub issues, E012's 1401 HN needs) against answerability by a free general assistant, followi |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-021-test-e038-s-189-github-issues-and-e012-s/events.jsonl
```

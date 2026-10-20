# Session 2026-10-15-029-fresh-observation-in-a-new-domain-test-t

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T23:28:09+00:00
- **Duration:** 1043.8s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation in a new domain: test the view-count principle on VS Code Marketplace (extension marketplace), chosen by stated rule: next largest software extension registry by user base with public per-item metadata, not a Q&A forum or model hub

## Summary

E165 completed: VS Code Marketplace view-count principle test fails. 1,884 extensions fetched from 28 categories; classifier too broad (90.5% need-related, 5.6% general, 3.9% other). Cliff's delta (install count, need-related vs general) = -0.0266, below 0.147 kill gate. General category (themes, keymaps, snippets) has marginally higher median installs (1,033 vs 955). Compare E162 (Mozilla Add-ons) which used targeted keywords (productivity, privacy) and measured average_daily_users where G1-G4 all passed. Kill gate fired; view-count principle boundary extended. F129 recorded in FAILURES.md. Next action: fresh observation in a new untouched domain.

## Next

Fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md | e1777e1e0b9e | 3387 |
| EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py | 08895046e960 | 13065 |
| EXPERIMENTS/165-vscode-marketplace-viewcount/raw_data.json | a52331c73b6b | 3991909 |

## Commands

12 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery', '-X', 'POST', '-H', 'Content-Type: application/json', '-d', | 0 | 441 |
| 3 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0', '-X', 'POST', '-H', 'Content-Type: applicat | 0 | 896 |
| 4 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0', '-X', 'POST', '-H', 'Content-Type: applicat | 0 | 1044 |
| 5 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0', '-X', 'POST', '-H', 'Content-Type: applicat | 0 | 1324 |
| 6 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 367 |
| 7 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 1645 |
| 8 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 453 |
| 9 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 2035 |
| 10 | ['python3', 'EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py'] | 1 | 727 |
| 11 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 1365 |
| 12 | ['curl', '-s', 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1', '-X', 'POST', '-H', 'Content-Type | 0 | 716 |
| 13 | ['python3', 'EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py'] | 0 | 297813 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 14 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
|   undeclared | EXPERIMENTS/165-golang-viewcount/RESULT.md |
|   undeclared | EXPERIMENTS/165-golang-viewcount/classified.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/classify.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/gate_results.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/harvest.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/measure.py |
|   undeclared | EXPERIMENTS/165-golang-viewcount/raw_harvest.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/run.py |
|   undeclared | FAILURES.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:28:09 | session_start | Fresh observation in a new domain: test the view-count principle on VS Code Marketplace (extension marketplace), chosen by stated rule: next largest s |
| 2 | 23:28:25 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery -X POST -H Content-Type: application/json -d {"filters":[{" |
| 3 | 23:28:35 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0 -X POST -H Content-Type: application/json - |
| 4 | 23:28:45 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0 -X POST -H Content-Type: application/json - |
| 5 | 23:28:59 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=1.0 -X POST -H Content-Type: application/json; |
| 6 | 23:29:09 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 7 | 23:29:20 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 8 | 23:29:33 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 9 | 23:29:46 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 10 | 23:32:57 | command | $ python3 EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py |
| 11 | 23:33:09 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 12 | 23:33:23 | command | $ curl -s https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery?api-version=7.1-preview.1 -X POST -H Content-Type: applicat |
| 13 | 23:40:04 | command | $ python3 EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py |
| 14 | 23:44:56 | artifact | wrote EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md |
| 15 | 23:45:13 | artifact | wrote EXPERIMENTS/165-vscode-marketplace-viewcount/fetch_extensions.py |
| 16 | 23:45:24 | artifact | wrote EXPERIMENTS/165-vscode-marketplace-viewcount/raw_data.json |
| 17 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
| 18 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/RESULT.md |
| 19 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/classified.json |
| 20 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/classify.py |
| 21 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/gate_results.json |
| 22 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/harvest.py |
| 23 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/measure.py |
| 24 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/raw_harvest.json |
| 25 | 23:45:33 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/run.py |
| 26 | 23:45:33 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 27 | 23:45:33 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 28 | 23:45:33 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 29 | 23:45:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-028-fresh-observation-test-view-count-princi/commands.log |
| 30 | 23:45:33 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-028-fresh-observation-test-view-count-princi/events.jsonl |
| 31 | 23:45:33 | doc_update | updated FAILURES.md |
| 32 | 23:45:33 | doc_update | updated STATE.md |
| 33 | 23:45:33 | session_end | E165 completed: VS Code Marketplace view-count principle test fails. 1,884 extensions fetched from 28 categories; classifier too broad (90.5% need-rel |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-029-fresh-observation-in-a-new-domain-test-t/events.jsonl
```

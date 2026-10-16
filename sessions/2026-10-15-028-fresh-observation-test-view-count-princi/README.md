# Session 2026-10-15-028-fresh-observation-test-view-count-princi

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T23:05:48+00:00
- **Duration:** 742.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation: test view-count principle on Go module ecosystem (pkg.go.dev) - a major package registry not yet tested

## Summary

E165 completed: Fresh observation test of view-count principle on Go module ecosystem (pkg.go.dev). Harvested 225 packages with universal 'Imported by' metadata (G4 PASS). Classifier vocabulary mismatch caused G1 FAIL (only 19 general vs 150 need-related packages, threshold 30). Cliff's delta = 0.0744 < 0.147 threshold (G2 FAIL). Both classes show 100% arrival rate, no differential activity (G3 FAIL). Result mirrors classifier vocabulary mismatches seen in E146 (crates.io), E157/E162/E163 (GitLab). Kill gate fired per protocol. Principle test inconclusive due to classifier mismatch, not absence of mechanism.

## Next

Return to fresh observation in a new untouched domain per STATE.md next action. Do not iterate on Go classifier adaptation; choose a domain not yet tested by this mission.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/165-golang-viewcount/RESULT.md | 2ac42d7563ac | 6062 |
| EXPERIMENTS/165-golang-viewcount/PROTOCOL.md | 7ce98e7aca65 | 4964 |
| EXPERIMENTS/165-golang-viewcount/harvest.py | c0f87e6612c5 | 4890 |
| EXPERIMENTS/165-golang-viewcount/classify.py | 3780f081e4ce | 3661 |
| EXPERIMENTS/165-golang-viewcount/measure.py | 549ebe990767 | 6118 |
| EXPERIMENTS/165-golang-viewcount/run.py | 2ddbb0faf30e | 1160 |

## Commands

20 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', 'https://proxy.golang.org/github.com/gin-gonic/gin/@v/list'] | 0 | 782 |
| 3 | ['curl', '-s', 'https://pkg.go.dev/github.com/gin-gonic/gin?tab=versions'] | 0 | 1301 |
| 4 | ['curl', '-s', 'https://api.pkg.go.dev/v3/packages/github.com/gin-gonic/gin'] | 6 | 108 |
| 5 | ['curl', '-s', 'https://pkg.go.dev/api/search?q=gin&limit=5'] | 0 | 463 |
| 6 | ['curl', '-s', 'https://proxy.golang.org/github.com/gin-gonic/gin/@v/v1.9.0.info'] | 0 | 141 |
| 7 | ['curl', '-s', 'https://pkg.go.dev/_/api/search?q=gin&limit=10'] | 0 | 723 |
| 8 | ['curl', '-s', 'https://proxy.golang.org/github.com/gin-gonic/gin/@latest'] | 0 | 594 |
| 9 | ['curl', '-s', 'https://pkg.go.dev/github.com/gin-gonic/gin'] | 0 | 1278 |
| 10 | ['curl', '-s', 'https://pkg.go.dev/search?q=web+framework&limit=20'] | 0 | 3307 |
| 11 | ['curl', '-s', 'https://pkg.go.dev/search?q=web+framework&limit=20'] | 0 | 912 |
| 12 | ['curl', '-s', 'https://pkg.go.dev/search?q=web+framework&limit=5'] | 0 | 740 |
| 13 | ['curl', '-s', 'https://pkg.go.dev/search?q=web+framework&limit=5'] | 0 | 593 |
| 14 | ['curl', '-s', 'https://pkg.go.dev/search?q=web+framework&limit=5'] | 0 | 511 |
| 15 | ['curl', '-s', 'https://pkg.go.dev/search?q=framework&limit=20'] | 0 | 1129 |
| 17 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/RESULT.md'] | 0 | 1431 |
| 19 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/PROTOCOL.md'] | 0 | 1335 |
| 21 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/harvest.py'] | 0 | 1375 |
| 23 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/classify.py'] | 0 | 1397 |
| 25 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/measure.py'] | 0 | 1522 |
| 27 | ['tools/origin', 'session', 'artifact', 'EXPERIMENTS/165-golang-viewcount/run.py'] | 0 | 1919 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 3 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/165-golang-viewcount/classified.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/gate_results.json |
|   undeclared | EXPERIMENTS/165-golang-viewcount/raw_harvest.json |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:05:48 | session_start | Fresh observation: test view-count principle on Go module ecosystem (pkg.go.dev) - a major package registry not yet tested |
| 2 | 23:06:00 | command | $ curl -s https://proxy.golang.org/github.com/gin-gonic/gin/@v/list |
| 3 | 23:06:07 | command | $ curl -s https://pkg.go.dev/github.com/gin-gonic/gin?tab=versions |
| 4 | 23:06:13 | command | $ curl -s https://api.pkg.go.dev/v3/packages/github.com/gin-gonic/gin |
| 5 | 23:06:19 | command | $ curl -s https://pkg.go.dev/api/search?q=gin&limit=5 |
| 6 | 23:06:27 | command | $ curl -s https://proxy.golang.org/github.com/gin-gonic/gin/@v/v1.9.0.info |
| 7 | 23:06:35 | command | $ curl -s https://pkg.go.dev/_/api/search?q=gin&limit=10 |
| 8 | 23:06:41 | command | $ curl -s https://proxy.golang.org/github.com/gin-gonic/gin/@latest |
| 9 | 23:06:51 | command | $ curl -s https://pkg.go.dev/github.com/gin-gonic/gin |
| 10 | 23:07:03 | command | $ curl -s https://pkg.go.dev/search?q=web+framework&limit=20 |
| 11 | 23:07:18 | command | $ curl -s https://pkg.go.dev/search?q=web+framework&limit=20 |
| 12 | 23:07:46 | command | $ curl -s https://pkg.go.dev/search?q=web+framework&limit=5 |
| 13 | 23:07:56 | command | $ curl -s https://pkg.go.dev/search?q=web+framework&limit=5 |
| 14 | 23:08:02 | command | $ curl -s https://pkg.go.dev/search?q=web+framework&limit=5 |
| 15 | 23:13:56 | command | $ curl -s https://pkg.go.dev/search?q=framework&limit=20 |
| 16 | 23:17:30 | artifact | wrote EXPERIMENTS/165-golang-viewcount/RESULT.md |
| 17 | 23:17:31 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/RESULT.md |
| 18 | 23:17:39 | artifact | wrote EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
| 19 | 23:17:40 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/PROTOCOL.md |
| 20 | 23:17:42 | artifact | wrote EXPERIMENTS/165-golang-viewcount/harvest.py |
| 21 | 23:17:43 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/harvest.py |
| 22 | 23:17:44 | artifact | wrote EXPERIMENTS/165-golang-viewcount/classify.py |
| 23 | 23:17:46 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/classify.py |
| 24 | 23:17:47 | artifact | wrote EXPERIMENTS/165-golang-viewcount/measure.py |
| 25 | 23:17:48 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/measure.py |
| 26 | 23:17:51 | artifact | wrote EXPERIMENTS/165-golang-viewcount/run.py |
| 27 | 23:17:52 | command | $ tools/origin session artifact EXPERIMENTS/165-golang-viewcount/run.py |
| 28 | 23:18:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/classified.json |
| 29 | 23:18:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/gate_results.json |
| 30 | 23:18:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/165-golang-viewcount/raw_harvest.json |
| 31 | 23:18:10 | session_end | E165 completed: Fresh observation test of view-count principle on Go module ecosystem (pkg.go.dev). Harvested 225 packages with universal 'Imported by |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-028-fresh-observation-test-view-count-princi/events.jsonl
```

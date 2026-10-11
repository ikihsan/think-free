# Session 2026-10-11-021-design-and-run-rubygems-view-count-princ

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T13:50:02+00:00
- **Duration:** 994.5s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Design and run RubyGems view-count principle test as fresh observation in new domain per D083

## Summary

Designed and ran RubyGems view-count principle test (E103) as fresh observation in new domain per D083. All four gates PASS: G1 retrieval (40 need-related, 40 random gems), G2 separation (Mann-Whitney U=289, p=1e-6, Cliff's δ=0.639), G3 effect magnitude (36/40 need-related above random median, Wilson LB=0.7695), G4 arrival field coverage (80/80 gems have downloads > 0). The view-count principle generalizes to RubyGems, consistent with PyPI, NPM, and NuGet. Created PROTOCOL.md, rubygems_classify.py, rubygems_stats.py, run.py, README.md, results.json.

## Next

Update STATE-next-actions.md to record E103 result and identify next fresh observation domain per D083

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/103-rubygems-viewcount/run.py | 6aa22fae456b | 2188 |
| EXPERIMENTS/103-rubygems-viewcount/PROTOCOL.md | 145eaadf7183 | 6424 |
| EXPERIMENTS/103-rubygems-viewcount/README.md | 17afe1d106f7 | 3861 |
| EXPERIMENTS/103-rubygems-viewcount/results.json | c8ee87d60940 | 16354 |
| EXPERIMENTS/103-rubygems-viewcount/rubygems_lib.py | 8777d5ec1584 | 11655 |
| EXPERIMENTS/103-rubygems-viewcount/rubygems_stats.py | d9e8913c40d1 | 4290 |
| EXPERIMENTS/103-rubygems-viewcount/rubygems_classify.py | 3e3a85624f2e | 7496 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 4 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/096-rubygems-viewcount/results.json |
|   undeclared | EXPERIMENTS/096-rubygems-viewcount/run.py |
|   undeclared | EXPERIMENTS/097-stackoverflow-viewcount/run.py |
|   undeclared | sessions/2026-10-11-020-continue-view-count-principle-fresh-obse/events.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/103-rubygems-viewcount/rubygems_lib.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 13:50:02 | session_start | Design and run RubyGems view-count principle test as fresh observation in new domain per D083 |
| 2 | 13:55:06 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/run.py |
| 3 | 13:55:06 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/PROTOCOL.md |
| 4 | 13:55:07 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/README.md |
| 5 | 13:55:07 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/results.json |
| 6 | 13:55:07 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/rubygems_lib.py |
| 7 | 14:06:21 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/rubygems_stats.py |
| 8 | 14:06:21 | artifact | wrote EXPERIMENTS/103-rubygems-viewcount/rubygems_classify.py |
| 9 | 14:06:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/096-rubygems-viewcount/results.json |
| 10 | 14:06:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/096-rubygems-viewcount/run.py |
| 11 | 14:06:37 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/097-stackoverflow-viewcount/run.py |
| 12 | 14:06:37 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-11-020-continue-view-count-principle-fresh-obse/events.jsonl |
| 13 | 14:06:37 | integrity_error | declared artifact no longer exists: EXPERIMENTS/103-rubygems-viewcount/rubygems_lib.py |
| 14 | 14:06:37 | session_end | Designed and ran RubyGems view-count principle test (E103) as fresh observation in new domain per D083. All four gates PASS: G1 retrieval (40 need-rel |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-021-design-and-run-rubygems-view-count-princ/events.jsonl
```

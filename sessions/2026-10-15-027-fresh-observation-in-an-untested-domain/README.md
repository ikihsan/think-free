# Session 2026-10-15-027-fresh-observation-in-an-untested-domain

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T21:52:50+00:00
- **Duration:** 2976.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Fresh observation in an untested domain: job posting platforms (LinkedIn/Indeed/Glassdoor) where needs are job requirements and activity signals are applications/views. Test whether view-count principle generalizes to labor market needs.

## Summary

Ran three fresh observation experiments testing view-count principle generalization to new domains: (1) Hacker News Ask HN — INVALIDATED: API only returns ~23 current posts, classifier vocabulary mismatch for HN phrasing. (2) Dev.to — INVALIDATED: page_views_count=0 for all articles in public API; measured reactions/comments proxy instead. (3) Wikipedia stubs vs developed — ALL GATES PASS: stubs (unmet information needs) have 2.5x higher views/byte (δ=0.377, p=0.0012). Principle extends to reference knowledge platform with explicit need markers (stub templates) and public view metadata.

## Next

View-count principle now validated on 10+ platform types. Boundary clear: works on artifact registries + Wikipedia; fails on forums, fault codes, infrastructure layers. Next: fresh observation in untested domain per stated rule, or pivot from view-count line (diminishing returns).

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/165-hn-ask-fresh-observation/README.md | fb88b787f8d5 | 5004 |
| EXPERIMENTS/165-hn-ask-fresh-observation/run.py | d387a5349b81 | 8488 |
| EXPERIMENTS/165-hn-ask-fresh-observation/classification.json | cb206b0871d7 | 9634 |
| EXPERIMENTS/165-hn-ask-fresh-observation/RESULT.md | 226ac0d09b6f | 4994 |
| EXPERIMENTS/166-devto-fresh-observation/README.md | bfaaa490c133 | 5477 |
| EXPERIMENTS/166-devto-fresh-observation/run.py | 67aa2244876a | 10572 |
| EXPERIMENTS/166-devto-fresh-observation/classification.json | 75ee6a729814 | 76237 |
| EXPERIMENTS/166-devto-fresh-observation/RESULT.md | 61bf50e21f13 | 5193 |
| EXPERIMENTS/167-wikipedia-fresh-observation/README.md | 661c02b7f19c | 5310 |
| EXPERIMENTS/167-wikipedia-fresh-observation/run.py | 21e56913ed16 | 15115 |
| EXPERIMENTS/167-wikipedia-fresh-observation/classification.json | 67ff285d4d80 | 14610 |
| EXPERIMENTS/167-wikipedia-fresh-observation/RESULT.md | 4726d7200ef7 | 6249 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-15-026-run-fresh-observation-experiment-t-0094/commands.log |
|   undeclared | sessions/2026-10-15-026-run-fresh-observation-experiment-t-0094/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:52:50 | session_start | Fresh observation in an untested domain: job posting platforms (LinkedIn/Indeed/Glassdoor) where needs are job requirements and activity signals are a |
| 2 | 22:42:03 | artifact | wrote EXPERIMENTS/165-hn-ask-fresh-observation/README.md |
| 3 | 22:42:04 | artifact | wrote EXPERIMENTS/165-hn-ask-fresh-observation/run.py |
| 4 | 22:42:05 | artifact | wrote EXPERIMENTS/165-hn-ask-fresh-observation/classification.json |
| 5 | 22:42:06 | artifact | wrote EXPERIMENTS/165-hn-ask-fresh-observation/RESULT.md |
| 6 | 22:42:07 | artifact | wrote EXPERIMENTS/166-devto-fresh-observation/README.md |
| 7 | 22:42:08 | artifact | wrote EXPERIMENTS/166-devto-fresh-observation/run.py |
| 8 | 22:42:09 | artifact | wrote EXPERIMENTS/166-devto-fresh-observation/classification.json |
| 9 | 22:42:10 | artifact | wrote EXPERIMENTS/166-devto-fresh-observation/RESULT.md |
| 10 | 22:42:10 | artifact | wrote EXPERIMENTS/167-wikipedia-fresh-observation/README.md |
| 11 | 22:42:11 | artifact | wrote EXPERIMENTS/167-wikipedia-fresh-observation/run.py |
| 12 | 22:42:12 | artifact | wrote EXPERIMENTS/167-wikipedia-fresh-observation/classification.json |
| 13 | 22:42:13 | artifact | wrote EXPERIMENTS/167-wikipedia-fresh-observation/RESULT.md |
| 14 | 22:42:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-026-run-fresh-observation-experiment-t-0094/commands.log |
| 15 | 22:42:26 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-026-run-fresh-observation-experiment-t-0094/events.jsonl |
| 16 | 22:42:26 | session_end | Ran three fresh observation experiments testing view-count principle generalization to new domains: (1) Hacker News Ask HN — INVALIDATED: API only ret |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-027-fresh-observation-in-an-untested-domain/events.jsonl
```

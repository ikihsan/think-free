# Session 2026-10-04-046-test-whether-zero-adoption-is-general-or

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T20:07:00+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether zero-adoption is general or specific to the agent-auditing niche, sampling adjacent tooling niches on the GitHub API

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/011-niche-adoption-census/results.json | 66f9aef446e9 | 9954 |
| EXPERIMENTS/011-niche-adoption-census/README.md | 7278a12ef199 | 1552 |
| FAILURES-findings-6.md | ae4b865ae664 | 9968 |
| FAILURES.md | a53fad7f8579 | 6487 |
| STATE.md | 10f7cc38dca4 | 26829 |
| STATE-next-actions.md | d14aafc98421 | 19987 |
| docs/INDEX.md | 46564b626671 | 21719 |

## Commands

3 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse\nterms = ['reproducible builds', 'build provenance', 'supply chain audit', 'lockfile dr | 0 | 3601 |
| 6 | ['python3', '-c', "\nimport json, urllib.request, urllib.parse, time\nterms = ['reproducible builds', 'build provenance', 'supply chain audit', 'lockf | 0 | 18073 |
| 8 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 368387 |

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
| 1 | 20:07:00 | session_start | Test whether zero-adoption is general or specific to the agent-auditing niche, sampling adjacent tooling niches on the GitHub API |
| 2 | 20:07:14 | command | $ python3 -c  import json, urllib.request, urllib.parse terms = ['reproducible builds', 'build provenance', 'supply chain audit', 'lockfile dr |
| 3 | 20:07:34 | task_rewrite | appended a create record for T-0058 |
| 4 | 20:07:46 | task_rewrite | rewrote tasks/T-0058-test-whether-flat-adoption-is-general-or-niche-s.md (status: claimed) |
| 5 | 20:07:47 | task_rewrite | appended a claim record for T-0058 |
| 6 | 20:08:23 | command | $ python3 -c  import json, urllib.request, urllib.parse, time terms = ['reproducible builds', 'build provenance', 'supply chain audit', 'lockf |
| 7 | 20:08:28 | artifact | wrote EXPERIMENTS/011-niche-adoption-census/results.json |
| 8 | 20:19:53 | command | $ python3 -m unittest discover -s tests |
| 9 | 20:20:00 | milestone | census taken: young vocabularies flat (lockfile drift 6, quarantine 8), established vocabularies heavy-tailed; F028 recorded |
| 10 | 20:20:00 | artifact | wrote EXPERIMENTS/011-niche-adoption-census/README.md |
| 11 | 20:20:01 | artifact | wrote FAILURES-findings-6.md |
| 12 | 20:20:01 | artifact | wrote FAILURES.md |
| 13 | 20:20:02 | artifact | wrote STATE.md |
| 14 | 20:20:04 | artifact | wrote STATE-next-actions.md |
| 15 | 20:20:05 | artifact | wrote docs/INDEX.md |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-046-test-whether-zero-adoption-is-general-or/events.jsonl
```

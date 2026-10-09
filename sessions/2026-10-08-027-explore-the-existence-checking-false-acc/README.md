# Session 2026-10-08-027-explore-the-existence-checking-false-acc

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T22:05:30+00:00
- **Duration:** 2545.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Explore the existence-checking false-accept problem from E064: measure whether the 24 healthy-metadata false accepts cause real user confusion, and whether a semantic 'did you mean' warning has a population that wants it

## Summary

E069 completed: searched for real confusion evidence on the 24 healthy-metadata false accepts from E064. Stack Overflow (all 10 top pairs) and GitHub Issues (top 2 pairs) show zero credible confusion reports across ~17.7M mutation downloads/yr. Kill gate G1 met (< 10 reports). No 'did you mean' warning population exists. Experiment artifacts: PROTOCOL.md, search_v2.py, outcome.py, README.md.

## Next

The existence-checking line is now closed at three levels: E064 measured the 16% false-accept rate and falsified the cheap fix; E069 shows the residual 24 healthy false accepts cause no measurable confusion. The semantic separator remains a model call. Next: explore fresh observations in a new domain per D080, or test the view_count instrument from E062 on a software population.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/069-false-accept-confusion/PROTOCOL.md | 43fea9958797 | 4779 |
| EXPERIMENTS/069-false-accept-confusion/search_v2.py | c174fc904b4d | 10639 |
| EXPERIMENTS/069-false-accept-confusion/outcome.py | c353eb51731f | 2538 |
| EXPERIMENTS/069-false-accept-confusion/README.md | ffcebe11fc4f | 4758 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 8 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/067-viewcount-framework/README.md |
|   undeclared | EXPERIMENTS/067-viewcount-framework/classify.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/outcome.py |
|   undeclared | EXPERIMENTS/067-viewcount-framework/viewcount.py |
|   undeclared | EXPERIMENTS/069-false-accept-confusion/search.py |
|   undeclared | sessions/2026-10-08-024-synthesize-view-count-instrument-finding/events.jsonl |
|   undeclared | sessions/2026-10-08-025-build-e067-view-count-measurement-framew/events.jsonl |
|   undeclared | sessions/2026-10-08-026-artifact-e067-framework-files/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 22:05:30 | session_start | Explore the existence-checking false-accept problem from E064: measure whether the 24 healthy-metadata false accepts cause real user confusion, and wh |
| 2 | 22:10:25 | milestone | Identified 24 residual false accepts from E064; now designing falsification experiment to search for real confusion evidence |
| 3 | 22:29:58 | milestone | Search hit GitHub rate limits; Stack Overflow shows ~0 confusion questions; need more targeted approach with global search queries |
| 4 | 22:40:29 | artifact | wrote EXPERIMENTS/069-false-accept-confusion/PROTOCOL.md |
| 5 | 22:40:30 | artifact | wrote EXPERIMENTS/069-false-accept-confusion/search_v2.py |
| 6 | 22:40:31 | artifact | wrote EXPERIMENTS/069-false-accept-confusion/outcome.py |
| 7 | 22:40:32 | artifact | wrote EXPERIMENTS/069-false-accept-confusion/README.md |
| 8 | 22:47:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/README.md |
| 9 | 22:47:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/classify.py |
| 10 | 22:47:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/outcome.py |
| 11 | 22:47:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/067-viewcount-framework/viewcount.py |
| 12 | 22:47:55 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/069-false-accept-confusion/search.py |
| 13 | 22:47:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-024-synthesize-view-count-instrument-finding/events.jsonl |
| 14 | 22:47:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-025-build-e067-view-count-measurement-framew/events.jsonl |
| 15 | 22:47:55 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-08-026-artifact-e067-framework-files/events.jsonl |
| 16 | 22:47:55 | session_end | E069 completed: searched for real confusion evidence on the 24 healthy-metadata false accepts from E064. Stack Overflow (all 10 top pairs) and GitHub  |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-027-explore-the-existence-checking-false-acc/events.jsonl
```

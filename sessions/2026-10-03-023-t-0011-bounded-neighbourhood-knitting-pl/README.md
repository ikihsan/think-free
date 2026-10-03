# Session 2026-10-03-023-t-0011-bounded-neighbourhood-knitting-pl

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T17:41:26+00:00
- **Duration:** 9968.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

T-0011: bounded-neighbourhood knitting planner vs the same exhaustive oracle

## Summary

T-0011 complete. Rejected the interrupted session's draft bounded.py after measuring that its per-neighbourhood candidates were cross-multiplied, so its search space equalled the oracle's and its 'all optimal' was a tautology; replaced it with a planner that takes each neighbourhood's minimum and charges the union of releases once, plus a chunk-cap and beam sweep. Result: valid and cost-identical to the 004 oracle on 115/115 checked fixtures (116/116 with --slow), on the development and holdout seeds, at every swept PATCH_COST, refusing both unsupported states; 004's per-error rule is optimal on 85/115. Chunk cap is the failure boundary (cap 1 fails 20/115, cap 3 fails 2 holdout cases) and two settings that look optimal enumerate exactly 2**|errors|, so they are labelled exhaustive-search-in-disguise. Work accounting shows the bounded planner is 1.28x worse than the oracle on T-0010's own fixtures, so 'bounded neighbourhood' is not an efficiency claim at this scale. Kill gate not met; verdict narrow, not abandon. Also corrected two pre-existing false claims in the record and split DECISIONS.md by subject because it had reached the line cap.

## Next

Run the prior-art check on the knitting candidate's remaining kill-gate condition (whether existing graph tooling supplies equivalent intervention sequences) before any Stage-B physical work; record it as a new failure or a narrowed claim.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/005-knitting-bounded-search/README.md | 647390976d80 | 9540 |
| EXPERIMENTS/005-knitting-bounded-search/planner.py | db0a4134872c | 7867 |
| EXPERIMENTS/005-knitting-bounded-search/fixtures.py | 7a25064a7681 | 4858 |
| EXPERIMENTS/005-knitting-bounded-search/run.py | d4505da78a7f | 12682 |
| EXPERIMENTS/005-knitting-bounded-search/results.json | 98a3dea4117a | 571468 |
| DECISIONS.md | 8126061f9086 | 1099 |
| DECISIONS-infrastructure.md | eabe0d384a3a | 11313 |
| DECISIONS-research.md | d5a5ebed12a1 | 6695 |
| STATE.md | c3a5af017d19 | 12815 |
| HYPOTHESES.md | 6c501c6022a4 | 14326 |
| AGENTS.md | 6ebbddecc273 | 7878 |
| RELEASE-MANIFEST.md | ab2e529d32f1 | 2733 |
| EXPERIMENTS/PLAN.md | 69bdb7551b14 | 2906 |
| EXPERIMENTS/004-knitting-stage-a/README.md | af728ec85f6a | 5390 |
| docs/process/experiment-protocol.md | bfe3619a6f95 | 5023 |
| docs/INDEX.md | 4c726cbf3c89 | 10183 |
| ROADMAP.md | 62c2198fae71 | 5001 |
| tasks/T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md | 6fcecb073999 | 2055 |
| tasks/CLAIMS.jsonl | b33c99884ffe | 9013 |
| EXPERIMENTS/005-knitting-bounded-search/README.md | 75215baf06aa | 9578 |

## Commands

15 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/bounded.py'] | 0 | 200 |
| 5 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 319811 |
| 6 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 314776 |
| 7 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 317744 |
| 10 | ['./tools/origin', 'doc', 'lint'] | 2 | 905 |
| 11 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 339788 |
| 12 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 1 | 812 |
| 13 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 1 | 993 |
| 14 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 2506 |
| 15 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py', '--slow'] | 0 | 335003 |
| 16 | ['python3', 'EXPERIMENTS/005-knitting-bounded-search/run.py'] | 0 | 3983 |
| 17 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 91176 |
| 18 | ['./tools/origin', 'doc', 'lint'] | 0 | 900 |
| 38 | ['./tools/origin', 'doc', 'lint'] | 0 | 880 |
| 40 | ['./tools/origin', 'doc', 'lint'] | 0 | 889 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 17:41:26 | session_start | T-0011: bounded-neighbourhood knitting planner vs the same exhaustive oracle |
| 2 | 19:08:14 | milestone | resumed interrupted T-0011 session on VM 0947: session 023 had only session_start and an untracked bounded.py draft |
| 3 | 19:08:29 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/bounded.py |
| 4 | 19:09:59 | decision | rejected the interrupted draft bounded.py: its per-neighbourhood candidates are cross-multiplied, so the enumerated combination count equals the oracl |
| 5 | 19:25:34 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 6 | 19:32:55 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 7 | 19:38:39 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 8 | 19:46:17 | milestone | T-0011 experiment run: bounded planner valid and optimal 113/113 vs the 004 oracle; cap sweep finds the failure boundary; results.json byte-identical  |
| 9 | 19:46:17 | note | two pre-existing false claims in the record found while updating docs: 004's README says results.json holds 'input_hashes' (no such key) and RELEASE-M |
| 10 | 19:48:49 | command | $ ./tools/origin doc lint |
| 11 | 19:54:46 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 12 | 20:14:06 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 13 | 20:14:18 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 14 | 20:14:31 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 15 | 20:20:15 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py --slow |
| 16 | 20:21:30 | command | $ python3 EXPERIMENTS/005-knitting-bounded-search/run.py |
| 17 | 20:23:32 | command | $ python3 -m unittest discover -s tests |
| 18 | 20:23:39 | command | $ ./tools/origin doc lint |
| 19 | 20:25:11 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/README.md |
| 20 | 20:25:12 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/planner.py |
| 21 | 20:25:13 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/fixtures.py |
| 22 | 20:25:13 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/run.py |
| 23 | 20:25:14 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/results.json |
| 24 | 20:25:14 | artifact | wrote DECISIONS.md |
| 25 | 20:25:15 | artifact | wrote DECISIONS-infrastructure.md |
| 26 | 20:25:15 | artifact | wrote DECISIONS-research.md |
| 27 | 20:25:15 | artifact | wrote STATE.md |
| 28 | 20:25:16 | artifact | wrote HYPOTHESES.md |
| 29 | 20:25:16 | artifact | wrote AGENTS.md |
| 30 | 20:25:17 | artifact | wrote RELEASE-MANIFEST.md |
| 31 | 20:25:17 | artifact | wrote EXPERIMENTS/PLAN.md |
| 32 | 20:25:18 | artifact | wrote EXPERIMENTS/004-knitting-stage-a/README.md |
| 33 | 20:25:18 | artifact | wrote docs/process/experiment-protocol.md |
| 34 | 20:25:19 | artifact | wrote docs/INDEX.md |
| 35 | 20:26:04 | artifact | wrote ROADMAP.md |
| 36 | 20:26:04 | artifact | wrote tasks/T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md |
| 37 | 20:26:04 | artifact | wrote tasks/CLAIMS.jsonl |
| 38 | 20:26:06 | command | $ ./tools/origin doc lint |
| 39 | 20:27:20 | artifact | wrote EXPERIMENTS/005-knitting-bounded-search/README.md |
| 40 | 20:27:21 | command | $ ./tools/origin doc lint |
| 41 | 20:27:35 | doc_update | updated DECISIONS.md |
| 42 | 20:27:35 | doc_update | updated HYPOTHESES.md |
| 43 | 20:27:35 | doc_update | updated ROADMAP.md |
| 44 | 20:27:35 | doc_update | updated STATE.md |
| 45 | 20:27:35 | session_end | T-0011 complete. Rejected the interrupted session's draft bounded.py after measuring that its per-neighbourhood candidates were cross-multiplied, so i |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-023-t-0011-bounded-neighbourhood-knitting-pl/events.jsonl
```

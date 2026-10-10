# Session 2026-10-09-020-begin-fresh-observation-in-a-new-domain

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-09T18:19:06+00:00
- **Duration:** 1573.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `HEAD`

## Goal

Begin fresh observation in a new domain to find a testable invention opportunity

## Summary

Ran fresh observation experiment E074 in the DIY (home improvement) Stack Exchange domain. Fetched 676 questions, classified them into 10 problem types, measured structured-input rates, and evaluated predeclared kill gates. G1 (population) passed for PROC at 27.8%, but G2 (structure) failed at 1.1% structured rate << 50% threshold. No candidate emerges from this domain. The experiment correctly falsifies the hypothesis that DIY Stack Exchange contains a concentrated, structured problem population amenable to a computational tool. Key insight: physical-world Q&A problems are predominantly unstructured procedural questions; structured types (diagnosis, code compliance) lack population dominance.

## Next

Design next fresh observation experiment in a domain with inherent structured data (e.g., automotive OBD2 codes, industrial equipment logs, medical device alarms, laboratory instrument errors) where problem statements naturally include codes, IDs, measurements.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/074-diy-problem-taxonomy/PROTOCOL.md | f47b318b0fad | 4143 |
| EXPERIMENTS/074-diy-problem-taxonomy/PROTOCOL.md | f47b318b0fad | 4143 |
| EXPERIMENTS/074-diy-problem-taxonomy/VERDICT.md | 23f51bd77002 | 4326 |
| EXPERIMENTS/074-diy-problem-taxonomy/analyze.py | b35cf3f740e3 | 11449 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/distribution.json | f27217503f94 | 1521 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/questions.json | d1ee470378f8 | 597138 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/questions_raw.json | d1ee470378f8 | 597138 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/structured_by_type.json | e275bc7a4c03 | 716 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.csv | 22c0abfd73af | 79800 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/tool_check.md | 0a2f1a4f43a0 | 2572 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/verdict.json | 0c7e34f68397 | 489 |
| EXPERIMENTS/074-diy-problem-taxonomy/fetch.py | 2e0e532e6e16 | 4201 |
| EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.jsonl | e44c320f5cd4 | 194540 |
| EXPERIMENTS/074-diy-problem-taxonomy/README.md | bccc407cd3c9 | 1859 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   error | declared artifact no longer exists: EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.csv |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 18:19:06 | session_start | Begin fresh observation in a new domain to find a testable invention opportunity |
| 2 | 18:29:35 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/PROTOCOL.md |
| 3 | 18:29:41 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/PROTOCOL.md |
| 4 | 18:29:42 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/VERDICT.md |
| 5 | 18:29:43 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/analyze.py |
| 6 | 18:29:43 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/distribution.json |
| 7 | 18:29:44 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/questions.json |
| 8 | 18:29:45 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/questions_raw.json |
| 9 | 18:29:46 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/structured_by_type.json |
| 10 | 18:29:47 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.csv |
| 11 | 18:29:48 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/tool_check.md |
| 12 | 18:29:48 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/verdict.json |
| 13 | 18:29:49 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/fetch.py |
| 14 | 18:33:01 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.jsonl |
| 15 | 18:44:29 | artifact | wrote EXPERIMENTS/074-diy-problem-taxonomy/README.md |
| 16 | 18:45:19 | integrity_error | declared artifact no longer exists: EXPERIMENTS/074-diy-problem-taxonomy/data/taxonomy.csv |
| 17 | 18:45:19 | session_end | Ran fresh observation experiment E074 in the DIY (home improvement) Stack Exchange domain. Fetched 676 questions, classified them into 10 problem type |
| 18 | 19:40:07 | milestone | E077 verified - view-count on non-software Discourse/SE, all gates pass |
| 19 | 19:41:15 | milestone | E077 integrated - view-count principle validated across 5 platforms |
| 20 | 19:57:00 | milestone | E078 prototype complete - framework validated, G4 needs larger sample |
| 21 | 20:07:19 | milestone | E077+E078 completed - view-count + need-classification validated |
| 22 | 20:08:27 | milestone | Mission state updated - E077/E078 completed, view-count principle validated across 5 platforms |
| 23 | 20:10:38 | milestone | Work complete - view-count principle + need-classification framework validated |
| 24 | 20:11:11 | milestone | Mission state: view-count + need-classification validated, candidates retired, seed empty. Next: fresh observation in unexplored domain. |
| 25 | 20:12:18 | milestone | Summary: E077/E078 complete, principle validated 5 platforms, framework prototyped, candidates retired, seed empty. Next action: choose fresh observat |
| 26 | 08:56:00 | session_end | Retroactive close: session had session_end at seq 17 but continued with milestones; this final session_end properly terminates the record |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-09-020-begin-fresh-observation-in-a-new-domain/events.jsonl
```

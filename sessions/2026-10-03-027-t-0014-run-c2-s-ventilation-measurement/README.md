# Session 2026-10-03-027-t-0014-run-c2-s-ventilation-measurement

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-03T20:46:42+00:00
- **Duration:** 1003.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

T-0014: run C2's ventilation measurement-design kill gate (adaptive vs fixed vs passive at equal budget)

## Summary

T-0014 complete and negative. Ran RESEARCH/C.md's predeclared kill gate for the ventilation candidate: at equal budget (12 sample slots, one decision) with the adaptive rule handed the surviving pair for free, a prescribed door-open protocol discriminated 0.833 against adaptive's 0.792 on correctly specified paired hypotheses (passive 0.333, chance). Gate 1 required adaptive > fixed and was not met, so the formulation is stopped (FAILURES F008); gate 2 was met but near-vacuously. Adaptive was genuinely better under poor mixing (0.708 vs 0.542), which is recorded as the narrower surviving observation rather than as a pass. One design correction was made before any result was recorded: the first build's paired room-A traces differed by 32 ppm RMS against 6 ppm noise, making the comparison vacuous, so it was rejected and rebuilt with the passive trace identical by construction. Also split FAILURES.md into FAILURES-findings.md plus a stub and STATE.md into STATE.md plus STATE-history.md, both at the standards' line triggers. task verify T-0014 exit 0; doc lint exit 0; 173 tests pass.

## Next

Run the prior-art check on the knitting candidate's remaining kill-gate condition (whether existing graph tooling supplies equivalent intervention sequences) and record it as a finding or a narrowed claim; do not extend the synthetic planner line and do not re-run the stopped ventilation experiment.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/006-ventilation-measurement-design/README.md | db3122ab6099 | 10110 |
| EXPERIMENTS/006-ventilation-measurement-design/estimator.py | 5c0a80b9ba43 | 7695 |
| EXPERIMENTS/006-ventilation-measurement-design/results.json | 9a8771a474b1 | 239412 |
| EXPERIMENTS/006-ventilation-measurement-design/run.py | 6b962e031a35 | 12734 |
| EXPERIMENTS/006-ventilation-measurement-design/simulate.py | f8f26cb12bf5 | 6336 |
| FAILURES.md | e949b0346cc4 | 2694 |
| FAILURES-findings.md | 9387911a0e36 | 16497 |
| STATE.md | b32f8f301c43 | 11899 |
| STATE-history.md | 62e11393f767 | 7950 |
| HYPOTHESES.md | 86b0915ffdb5 | 16509 |
| ROADMAP.md | 5a17fcd56aeb | 5597 |
| docs/process/experiment-protocol.md | 3a0e7adbb101 | 5220 |
| ROADMAP.md | 5a17fcd56aeb | 5597 |
| STATE.md | b32f8f301c43 | 11899 |
| tasks/T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md | b021931cba52 | 2778 |
| tasks/CLAIMS.jsonl | 315e178da847 | 11797 |
| tasks/INDEX.md | c1ea8103d651 | 3681 |

## Commands

2 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 15 | ['./tools/origin', 'doc', 'lint'] | 0 | 917 |
| 16 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 93988 |

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
| 1 | 20:46:42 | session_start | T-0014: run C2's ventilation measurement-design kill gate (adaptive vs fixed vs passive at equal budget) |
| 2 | 20:53:47 | milestone | 006 design rebuilt: room-A-only sensor, occupied neighbour, menu mixing door_open with co_locate_b; first build made paired traces trivially separable |
| 3 | 21:00:35 | artifact | wrote EXPERIMENTS/006-ventilation-measurement-design/README.md |
| 4 | 21:00:35 | artifact | wrote EXPERIMENTS/006-ventilation-measurement-design/estimator.py |
| 5 | 21:00:35 | artifact | wrote EXPERIMENTS/006-ventilation-measurement-design/results.json |
| 6 | 21:00:35 | artifact | wrote EXPERIMENTS/006-ventilation-measurement-design/run.py |
| 7 | 21:00:35 | artifact | wrote EXPERIMENTS/006-ventilation-measurement-design/simulate.py |
| 8 | 21:00:36 | artifact | wrote FAILURES.md |
| 9 | 21:00:36 | artifact | wrote FAILURES-findings.md |
| 10 | 21:00:37 | artifact | wrote STATE.md |
| 11 | 21:00:37 | artifact | wrote STATE-history.md |
| 12 | 21:00:37 | artifact | wrote HYPOTHESES.md |
| 13 | 21:00:38 | artifact | wrote ROADMAP.md |
| 14 | 21:00:38 | artifact | wrote docs/process/experiment-protocol.md |
| 15 | 21:00:47 | command | $ ./tools/origin doc lint |
| 16 | 21:02:27 | command | $ python3 -m unittest discover -s tests |
| 17 | 21:02:44 | artifact | wrote ROADMAP.md |
| 18 | 21:02:44 | artifact | wrote STATE.md |
| 19 | 21:02:44 | artifact | wrote tasks/T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md |
| 20 | 21:02:44 | artifact | wrote tasks/CLAIMS.jsonl |
| 21 | 21:02:44 | artifact | wrote tasks/INDEX.md |
| 22 | 21:03:25 | doc_update | updated FAILURES.md |
| 23 | 21:03:25 | doc_update | updated HYPOTHESES.md |
| 24 | 21:03:25 | doc_update | updated ROADMAP.md |
| 25 | 21:03:25 | doc_update | updated STATE.md |
| 26 | 21:03:25 | session_end | T-0014 complete and negative. Ran RESEARCH/C.md's predeclared kill gate for the ventilation candidate: at equal budget (12 sample slots, one decision) |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-027-t-0014-run-c2-s-ventilation-measurement/events.jsonl
```

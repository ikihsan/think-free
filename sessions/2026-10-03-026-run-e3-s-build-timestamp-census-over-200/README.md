# Session 2026-10-03-026-run-e3-s-build-timestamp-census-over-200

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-03T19:33:16+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Run E3's build-timestamp census over 200 recent PyPI wheels and apply its kill gate

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/005-build-timestamps/census.py | c09b5f15cf2a | 8381 |
| EXPERIMENTS/005-build-timestamps/census.py | bd66121df896 | 8879 |
| EXPERIMENTS/005-build-timestamps/sampling.py | 92acc37e7d44 | 4008 |
| EXPERIMENTS/007-build-timestamps/census.py | 5bf1b5f9c2fe | 10965 |
| EXPERIMENTS/007-build-timestamps/README.md | 7eaefae3bbb6 | 9062 |
| EXPERIMENTS/007-build-timestamps/sampling.py | 1237db22f985 | 5183 |
| EXPERIMENTS/007-build-timestamps/results.json | 8ee8ffe4af22 | 135245 |
| FAILURES.md | c51e9167f044 | 3614 |
| FAILURES-claims.md | 129a48ef7c0b | 14673 |
| FAILURES-process.md | a5b0119406f4 | 6665 |
| DECISIONS-PRACTICE.md | 049573f8ef8d | 15794 |
| HYPOTHESES.md | 6bc8d1ed640d | 18836 |
| tasks/T-0013-run-e3-s-build-timestamp-census-over-200-recent.md | c8f573eeb97f | 3477 |
| tasks/T-0016-build-one-source-twice-under-different-source-da.md | dce7b647f508 | 3467 |
| STATE.md | 31dd47040796 | 14598 |
| ROADMAP.md | ce4d3ca991e6 | 6159 |
| RESEARCH.md | 00e6deac7c6d | 5838 |
| docs/INDEX.md | d6c4767e65ca | 11736 |
| tasks/INDEX.md | 2470dd3092d2 | 4083 |
| EXPERIMENTS/007-build-timestamps/census.py | d718786e343a | 10966 |

## Commands

7 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'EXPERIMENTS/005-build-timestamps/census.py'] | 0 | 109828 |
| 7 | ['python3', 'census.py'] | 0 | 122683 |
| 10 | ['python3', 'EXPERIMENTS/007-build-timestamps/census.py'] | 0 | 80318 |
| 11 | ['python3', 'EXPERIMENTS/007-build-timestamps/census.py'] | 0 | 36095 |
| 12 | ['python3', 'EXPERIMENTS/007-build-timestamps/census.py'] | 0 | 36271 |
| 16 | ['python3', 'EXPERIMENTS/007-build-timestamps/census.py'] | 0 | 37082 |
| 28 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 88813 |

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
| 1 | 19:33:16 | session_start | Run E3's build-timestamp census over 200 recent PyPI wheels and apply its kill gate |
| 2 | 19:34:44 | artifact | wrote EXPERIMENTS/005-build-timestamps/census.py |
| 3 | 19:36:34 | command | $ python3 EXPERIMENTS/005-build-timestamps/census.py |
| 4 | 19:42:29 | artifact | wrote EXPERIMENTS/005-build-timestamps/census.py |
| 5 | 19:42:29 | artifact | wrote EXPERIMENTS/005-build-timestamps/sampling.py |
| 6 | 19:42:29 | milestone | census written and split (sampling.py + census.py); first pass showed 58% of wheels carry multiple distinct zip entry timestamps |
| 7 | 19:44:20 | command | $ python3 census.py |
| 8 | 21:05:16 | milestone | resumed the interrupted session after fast-forwarding onto origin; remote had landed 005-knitting-bounded-search and reserved 006 for T-0014 |
| 9 | 21:05:16 | decision | Renumber the census to EXPERIMENTS/007-build-timestamps: 005 was claimed and landed by EXPERIMENTS/005-knitting-bounded-search on instance-20260717-09 |
| 10 | 21:08:38 | command | $ python3 EXPERIMENTS/007-build-timestamps/census.py |
| 11 | 21:10:42 | command | $ python3 EXPERIMENTS/007-build-timestamps/census.py |
| 12 | 21:12:25 | command | $ python3 EXPERIMENTS/007-build-timestamps/census.py |
| 13 | 21:18:32 | milestone | resumed session 026 after stashing, fast-forwarding onto origin (now includes T-0014 ventilation stop and T-0015 claim), and verifying the census is d |
| 14 | 21:20:53 | artifact | wrote EXPERIMENTS/007-build-timestamps/census.py |
| 15 | 21:20:53 | decision | Report an absent package (index resolved, no wheels) in its own sample.packages_absent field instead of appending it to the failure list: the earlier  |
| 16 | 21:21:34 | command | $ python3 EXPERIMENTS/007-build-timestamps/census.py |
| 17 | 21:26:40 | experiment_result | Build-timestamp census over 200 PyPI wheels drawn from 10 declared packages (T-0013, EXPERIMENTS/007-build-timestamps/). Gate metric non_1980_fraction |
| 18 | 21:26:44 | artifact | wrote EXPERIMENTS/007-build-timestamps/README.md |
| 19 | 21:26:44 | artifact | wrote EXPERIMENTS/007-build-timestamps/sampling.py |
| 20 | 21:26:44 | artifact | wrote EXPERIMENTS/007-build-timestamps/results.json |
| 21 | 21:26:44 | artifact | wrote FAILURES.md |
| 22 | 21:26:44 | artifact | wrote FAILURES-claims.md |
| 23 | 21:26:44 | artifact | wrote FAILURES-process.md |
| 24 | 21:26:44 | artifact | wrote DECISIONS-PRACTICE.md |
| 25 | 21:26:44 | artifact | wrote HYPOTHESES.md |
| 26 | 21:26:44 | artifact | wrote tasks/T-0013-run-e3-s-build-timestamp-census-over-200-recent.md |
| 27 | 21:26:44 | artifact | wrote tasks/T-0016-build-one-source-twice-under-different-source-da.md |
| 28 | 21:30:29 | command | $ python3 -m unittest discover -s tests |
| 29 | 21:30:36 | artifact | wrote STATE.md |
| 30 | 21:30:36 | artifact | wrote ROADMAP.md |
| 31 | 21:30:36 | artifact | wrote RESEARCH.md |
| 32 | 21:30:36 | artifact | wrote docs/INDEX.md |
| 33 | 21:30:36 | artifact | wrote tasks/INDEX.md |
| 34 | 21:30:36 | milestone | T-0013 complete: census landed as EXPERIMENTS/007-build-timestamps, gate met at 0.965 but recorded as near-vacuous (F009), attribution deferred to T-0 |
| 35 | 21:31:33 | artifact | wrote EXPERIMENTS/007-build-timestamps/census.py |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-03-026-run-e3-s-build-timestamp-census-over-200/events.jsonl
```

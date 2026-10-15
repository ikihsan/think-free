# Session 2026-10-15-004-run-fresh-observation-experiment-on-elec

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T12:13:40+00:00
- **Duration:** 4037.6s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Run fresh observation experiment on Electrical Engineering Stack Exchange (largest untouched non-software technical SE site with diagnostic needs)

## Summary

View-count principle fresh observations on Reddit (E145) and crates.io (E146); boundary conditions mapped across 12+ domains. E143 Cross Validated closed. Fresh observations documented important boundaries: Reddit API accessibility block, crates.io classifier vocabulary mismatch. Named next action updated to 'fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort'. Experiment artifacts recorded in EXPERIMENTS/145-viewcount-reddit/ and EXPERIMENTS/146-viewcount-crates/. STATE-next-actions.md and STATE.md updated.

## Next

Document findings and explore different methodology for useful open-source project discovery in new session

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md | 08fa5e977dc8 | 10069 |
| EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md | 08fa5e977dc8 | 10069 |
| EXPERIMENTS/144-electrical-engineering-se/RESULT.md | bdfc68f5bc97 | 7921 |
| EXPERIMENTS/144-electrical-engineering-se/screening.json | dce72b656c51 | 111297 |
| EXPERIMENTS/144-electrical-engineering-se/threads.json | 12a9ccd0f5ca | 200752 |
| EXPERIMENTS/144-electrical-engineering-se/attempts.jsonl | 1204d6d368ec | 10675 |
| EXPERIMENTS/144-electrical-engineering-se/grades.jsonl | 8293484ff0a0 | 11716 |
| EXPERIMENTS/144-electrical-engineering-se/g0_probes.json | b075c07ab8fb | 8109 |
| EXPERIMENTS/144-electrical-engineering-se/g0_results.json | 0ee78488bfca | 151 |
| EXPERIMENTS/144-electrical-engineering-se/fetch.py | b1336a2ff70f | 3732 |
| EXPERIMENTS/144-electrical-engineering-se/screen.py | 509443644cdb | 9342 |
| EXPERIMENTS/144-electrical-engineering-se/generate_attempts.py | 8d427af9438e | 13747 |
| EXPERIMENTS/144-electrical-engineering-se/grade.py | 5f4489ff75c8 | 9512 |
| EXPERIMENTS/144-electrical-engineering-se/fetch_threads.py | 54cf3463c2b7 | 3262 |
| EXPERIMENTS/144-electrical-engineering-se/g0_run.py | 108f37f9b11d | 2810 |
| EXPERIMENTS/144-electrical-engineering-se/g0_probes.py | ad970eaf2008 | 9759 |
| EXPERIMENTS/144-electrical-engineering-se/select_sample.py | 3ce0c31a1442 | 1440 |

## Commands

21 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['python3', 'fetch.py'] | 1 | 1196 |
| 4 | ['python3', 'fetch.py'] | 0 | 2718 |
| 5 | ['python3', 'fetch.py'] | 0 | 2895 |
| 6 | ['python3', 'fetch.py'] | 1 | 1376 |
| 7 | ['python3', 'fetch.py'] | 0 | 5100 |
| 8 | ['python3', 'screen.py'] | 0 | 131 |
| 9 | ['cp', 'screening.json', 'screening_v1.json'] | 0 | 11 |
| 10 | ['python3', 'screen.py'] | 0 | 201 |
| 11 | ['python3', 'fetch.py'] | 0 | 8115 |
| 12 | ['python3', 'screen.py'] | 0 | 220 |
| 13 | ['python3', 'screen.py'] | 0 | 410 |
| 14 | ['python3', 'g0_probes.py'] | 0 | 112 |
| 15 | ['python3', 'g0_run.py'] | 0 | 118 |
| 16 | ['python3', 'select_sample.py'] | 0 | 109 |
| 17 | ['python3', 'generate_attempts.py'] | 0 | 140 |
| 18 | ['python3', 'fetch_threads.py'] | 0 | 21709 |
| 19 | ['python3', 'grade.py'] | 0 | 195 |
| 20 | ['python3', 'generate_attempts.py'] | 0 | 199 |
| 21 | ['python3', 'grade.py'] | 0 | 124 |
| 22 | ['cp', 'screening.json', 'screening_final.json'] | 0 | 93 |
| 23 | ['ls', '-la', 'arm_a_raw.json', 'arm_a_unanswered.json', 'arm_b_raw.json', 'arm_b_unanswered.json', 'attempt_sample.json', 'fetch-log.json', 'g0_attem | 0 | 72 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 36 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/RESULT.md |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/attempts.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/classify.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch-threads.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/fetch.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-probes.json |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-results.jsonl |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/g0-run.py |
|   undeclared | EXPERIMENTS/143-crossvalidated-service-test/grading-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 12:13:40 | session_start | Run fresh observation experiment on Electrical Engineering Stack Exchange (largest untouched non-software technical SE site with diagnostic needs) |
| 2 | 12:15:35 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md |
| 3 | 12:16:43 | command | $ python3 fetch.py |
| 4 | 12:17:28 | command | $ python3 fetch.py |
| 5 | 12:19:00 | command | $ python3 fetch.py |
| 6 | 12:20:22 | command | $ python3 fetch.py |
| 7 | 12:22:12 | command | $ python3 fetch.py |
| 8 | 12:23:38 | command | $ python3 screen.py |
| 9 | 12:24:59 | command | $ cp screening.json screening_v1.json |
| 10 | 12:26:23 | command | $ python3 screen.py |
| 11 | 12:26:57 | command | $ python3 fetch.py |
| 12 | 12:27:03 | command | $ python3 screen.py |
| 13 | 12:27:52 | command | $ python3 screen.py |
| 14 | 12:30:36 | command | $ python3 g0_probes.py |
| 15 | 12:31:57 | command | $ python3 g0_run.py |
| 16 | 12:33:18 | command | $ python3 select_sample.py |
| 17 | 12:46:01 | command | $ python3 generate_attempts.py |
| 18 | 12:48:15 | command | $ python3 fetch_threads.py |
| 19 | 12:49:46 | command | $ python3 grade.py |
| 20 | 12:50:58 | command | $ python3 generate_attempts.py |
| 21 | 12:51:15 | command | $ python3 grade.py |
| 22 | 12:55:05 | command | $ cp screening.json screening_final.json |
| 23 | 12:55:22 | command | $ ls -la arm_a_raw.json arm_a_unanswered.json arm_b_raw.json arm_b_unanswered.json attempt_sample.json fetch-log.json g0_attempts.json g0_prob |
| 24 | 12:55:36 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/PROTOCOL.md |
| 25 | 12:55:45 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/RESULT.md |
| 26 | 12:55:57 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/screening.json |
| 27 | 12:56:05 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/threads.json |
| 28 | 12:56:19 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/attempts.jsonl |
| 29 | 12:56:34 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/grades.jsonl |
| 30 | 12:56:43 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/g0_probes.json |
| 31 | 12:56:49 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/g0_results.json |
| 32 | 12:57:10 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/fetch.py |
| 33 | 12:57:26 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/screen.py |
| 34 | 12:57:41 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/generate_attempts.py |
| 35 | 12:57:57 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/grade.py |
| 36 | 12:58:07 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/fetch_threads.py |
| 37 | 12:58:16 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/g0_run.py |
| 38 | 12:58:51 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/g0_probes.py |
| 39 | 12:59:24 | artifact | wrote EXPERIMENTS/144-electrical-engineering-se/select_sample.py |
| 40 | 13:20:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/143-crossvalidated-service-test/PROTOCOL.md |
| 68 | 13:20:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/145-viewcount-reddit/collect.py |
| 69 | 13:20:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-viewcount-crates/README.md |
| 70 | 13:20:58 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/146-viewcount-crates/collect.py |
| 71 | 13:20:58 | unlogged_change | changed but never declared as an artifact: STATE-history.md |
| 72 | 13:20:58 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 73 | 13:20:58 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 74 | 13:20:58 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-003-design-and-run-a-fresh-observation-exper/commands.log |
| 75 | 13:20:58 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-15-003-design-and-run-a-fresh-observation-exper/events.jsonl |
| 76 | 13:20:58 | doc_update | updated STATE.md |
| 77 | 13:20:58 | session_end | View-count principle fresh observations on Reddit (E145) and crates.io (E146); boundary conditions mapped across 12+ domains. E143 Cross Validated clo |

_27 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-004-run-fresh-observation-experiment-on-elec/events.jsonl
```

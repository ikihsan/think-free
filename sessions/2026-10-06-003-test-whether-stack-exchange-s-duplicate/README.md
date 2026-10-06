# Session 2026-10-06-003-test-whether-stack-exchange-s-duplicate

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-06T04:58:20+00:00
- **Duration:** 4292.8s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Test whether Stack Exchange's duplicate-closure canonical is recoverable by a channel E033 did not try, and if it is, prototype the smallest tool that turns that edge into a map of questions people keep re-asking

## Summary

E034 (T-0078) ran, reported and completed. Pooled duplicate-closure rate 0.1352 CI95 [0.1122,0.1620] in the score tail against 0.0303 [0.0201,0.0455] in the Active tab and 0.0371 at the score head, 4.5x and 0.1454 vs 0.0282 on equal denominators, replicating F055 whole-site gradient on an independent tag-stratified population with a platform-owned label. The rate is a per-tag property this record had never measured: ten tags span 0.0000 to 0.4300, twelve pairs have disjoint intervals, and AMENDMENT-1 R1 replicates both extremes on the next four pages. Two declared claims failed and are recorded as failures: D6, tag and site are not apportioned at 3-5 tags per site (4/10 within-site disjoint pairs against 14/26 cross-site), and B1, the answer-existed mechanism is not separable from a moderator closing it (CI95 [-0.0774,+0.3075]); the a-priori stratum hypothesis is backwards. E033 open question is closed on its other half: the canonical edge is unreachable through nine named channels. F057, D063, D064 recorded; 799 tests green; doc lint and release check clean.

## Next

E034 next action, which is D6 own: three to four more tags on each of the three sites (stackoverflow, travel, math), tail arm only, 4 pages each, about 30 requests against a fresh 300 daily quota. Until tag is separable from site the per-tag reading stays not_established and nothing is built on it. If D6 clears, the next question is whether the repeats content clusters into a usable clause set, which is what four earlier demand-side generators could not answer; if it does not clear, the per-tag diagnostic dies and what remains is a sampling recommendation.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/034-reask-tail/PROTOCOL.md | 1fca1d1972ce | 9840 |
| EXPERIMENTS/034-reask-tail/PROTOCOL.md | 3a10dba9a466 | 12262 |
| EXPERIMENTS/034-reask-tail/README.md | a531f2350892 | 11793 |
| EXPERIMENTS/034-reask-tail/reask.py | c1efaf84b401 | 6991 |
| EXPERIMENTS/034-reask-tail/harvest.py | d875a1b1f9c0 | 7175 |
| EXPERIMENTS/034-reask-tail/measures.py | 7fefe635c627 | 9767 |
| EXPERIMENTS/034-reask-tail/tally.py | 9f74cec0db91 | 11727 |
| EXPERIMENTS/034-reask-tail/check.py | dcb11fde5c44 | 10599 |
| FAILURES-findings-23.md | 5613fac020e4 | 7057 |
| DECISIONS-SCREENING-6.md | 4821e6cfd1d9 | 5711 |
| FAILURES.md | 212cfd4f3eda | 26975 |
| DECISIONS.md | 1e85628fa584 | 9264 |
| STATE.md | 419bb67f8985 | 35391 |
| STATE-in-flight-2.md | 2d88d0cc1269 | 17700 |
| STATE-next-actions.md | c6417a5771f3 | 18904 |
| tasks/T-0078-e034-test-whether-stack-exchange-questions-close.md | 1bf266454dcc | 2457 |
| EXPERIMENTS/034-reask-tail/PROTOCOL.md | e528471f0259 | 13766 |
| EXPERIMENTS/034-reask-tail/README.md | e28c71478f90 | 12398 |
| FAILURES-findings-23.md | ec74f5894b1d | 7054 |
| DECISIONS-SCREENING-6.md | 3977174c957c | 5708 |
| STATE.md | f5b66aab16c8 | 35388 |
| STATE-in-flight-2.md | 4cd9e816e8f2 | 17697 |
| STATE-next-actions.md | f915b146564f | 18901 |
| tools/originlib/paths.py | f197cad91ee4 | 4094 |
| tools/originlib/reconcile.py | 9fef253426e3 | 8182 |
| tests/test_decision_files.py | 6139a1e34a12 | 4156 |
| EXPERIMENTS/034-reask-tail/reask.py | 1eb95dda3dbb | 8588 |
| EXPERIMENTS/034-reask-tail/harvest.py | 459516542c64 | 7163 |
| EXPERIMENTS/034-reask-tail/measures.py | 90e2f0b507e3 | 9913 |
| EXPERIMENTS/034-reask-tail/tally.py | 9f74cec0db91 | 11727 |
| EXPERIMENTS/034-reask-tail/check.py | 974961117d69 | 12249 |
| EXPERIMENTS/034-reask-tail/falsify.py | 408da457bf2d | 7245 |
| EXPERIMENTS/034-reask-tail/README.md | 96417b7dd8af | 13166 |
| ROADMAP.md | 8c70acdd463b | 14826 |
| tasks/T-0078-e034-test-whether-stack-exchange-questions-close.md | 6e15bd33da25 | 2454 |

## Commands

59 captured, 25 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['bash', '-c', '\nUA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"\nmkdir -p /tmp/opencode/probe | 0 | 12546 |
| 3 | ['bash', '-c', '\nfor q in 189869 189816 189334; do\n  echo "== q=$q answers"\n  curl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3 | 0 | 1370 |
| 4 | ['bash', '-c', '\necho "== default filter answers q=189869"\ncurl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3/questions/189869/an | 0 | 1021 |
| 5 | ['bash', '-c', '\nfor q in 189910 189869 189816; do\n  echo "== q=$q comments (withbody)"\n  curl -s --max-time 25 --compressed "https://api.stackexch | 0 | 1205 |
| 6 | ['bash', '-c', '\nfor q in 189910 189816 189814; do\n  echo "== q=$q all comments"\n  curl -s --max-time 25 --compressed "https://api.stackexchange.co | 0 | 1646 |
| 7 | ['bash', '-c', '\necho "== TAIL: sort=votes order=asc pagesize=25"\ncurl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3/questions?si | 0 | 1112 |
| 13 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 895 |
| 14 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 593 |
| 15 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 555 |
| 16 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 547 |
| 17 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 250 |
| 18 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 707 |
| 19 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 287 |
| 20 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 689 |
| 21 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 296 |
| 22 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 298 |
| 23 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 238 |
| 24 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 0 | 236 |
| 25 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'harvest', '--pages', '4'] | 0 | 64990 |
| 26 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'report'] | 0 | 303 |
| 27 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'replicate'] | 1 | 6698 |
| 28 | ['python3', '-'] | 0 | 211 |
| 29 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 3 | 422 |
| 30 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'replicate', '--sample', 'R2'] | 0 | 8134 |
| 31 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 1 | 345 |
| 32 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 0 | 343 |
| 33 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 4 | 396 |
| 34 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 1 | 896 |
| 35 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 0 | 343 |
| 36 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 1 | 839 |
| 37 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 0 | 194 |
| 38 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'report'] | 0 | 194 |
| 39 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 0 | 245 |
| 60 | ['python3', 'EXPERIMENTS/034-reask-tail/tally.py', '--check'] | 0 | 903 |
| 61 | ['python3', 'EXPERIMENTS/034-reask-tail/check.py'] | 0 | 683 |
| 68 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests'] | 1 | 566835 |
| 69 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest tests.test_decision_files tests.test_decision_row_pattern tests.test_decision_header 2>&1 \ | 0 | 3169 |
| 70 | ['bash', '-c', 'PYTHONPATH=tools:tests python3 -m unittest tests.test_decision_files tests.test_decision_row_pattern tests.test_decision_header 2>&1 \ | 0 | 2999 |
| 71 | ['bash', '-c', 'cd /home/ubuntu/think-free && PYTHONPATH=tools:tests python3 -m unittest tests.test_decision_files tests.test_decision_row_pattern tes | 0 | 3292 |
| 76 | ['python3', 'EXPERIMENTS/034-reask-tail/reask.py', 'report'] | 0 | 407 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 5 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/034-reask-tail/raw/harvest.jsonl |
|   undeclared | EXPERIMENTS/034-reask-tail/raw/pages.jsonl |
|   undeclared | EXPERIMENTS/034-reask-tail/raw/r1.jsonl |
|   undeclared | EXPERIMENTS/034-reask-tail/raw/r2.jsonl |
|   undeclared | EXPERIMENTS/034-reask-tail/raw/tally.json |
|   error | HYPOTHESES.md was not updated although the session recorded experiment_result |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 04:58:20 | session_start | Test whether Stack Exchange's duplicate-closure canonical is recoverable by a channel E033 did not try, and if it is, prototype the smallest tool that |
| 2 | 04:58:59 | command | $ bash -c  UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" mkdir -p /tmp/opencode/probe |
| 3 | 04:59:45 | command | $ bash -c  for q in 189869 189816 189334; do   echo "== q=$q answers"   curl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3/ |
| 4 | 04:59:58 | command | $ bash -c  echo "== default filter answers q=189869" curl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3/questions/189869/an |
| 5 | 05:00:15 | command | $ bash -c  for q in 189910 189869 189816; do   echo "== q=$q comments (withbody)"   curl -s --max-time 25 --compressed "https://api.stackexcha |
| 6 | 05:00:23 | command | $ bash -c  for q in 189910 189816 189814; do   echo "== q=$q all comments"   curl -s --max-time 25 --compressed "https://api.stackexchange.com |
| 7 | 05:01:08 | command | $ bash -c  echo "== TAIL: sort=votes order=asc pagesize=25" curl -s --max-time 25 --compressed "https://api.stackexchange.com/2.3/questions?si |
| 8 | 05:02:06 | task_rewrite | appended a create record for T-0078 |
| 9 | 05:03:28 | milestone | E034 PROTOCOL.md declared (population, 8 pre-named tags, 3 matched arms, gates A1-A4/B1, kill gate A4) before any fetch of the declared population |
| 10 | 05:03:28 | artifact | wrote EXPERIMENTS/034-reask-tail/PROTOCOL.md |
| 11 | 05:03:41 | task_rewrite | rewrote tasks/T-0078-e034-test-whether-stack-exchange-questions-close.md (status: claimed) |
| 12 | 05:03:41 | task_rewrite | appended a claim record for T-0078 |
| 13 | 05:05:05 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 14 | 05:05:21 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 15 | 05:05:35 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 16 | 05:05:54 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 17 | 05:06:12 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 18 | 05:06:44 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 19 | 05:07:01 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 20 | 05:07:20 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 21 | 05:07:32 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 22 | 05:08:03 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 23 | 05:08:14 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 24 | 05:08:32 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 25 | 05:09:47 | command | $ python3 EXPERIMENTS/034-reask-tail/reask.py harvest --pages 4 |
| 26 | 05:09:53 | command | $ python3 EXPERIMENTS/034-reask-tail/reask.py report |
| 27 | 05:11:05 | command | $ python3 EXPERIMENTS/034-reask-tail/reask.py replicate |
| 28 | 05:11:05 | command | $ python3 - |
| 29 | 05:12:15 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 30 | 05:14:23 | command | $ python3 EXPERIMENTS/034-reask-tail/reask.py replicate --sample R2 |
| 31 | 05:15:59 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 32 | 05:16:12 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 33 | 05:16:13 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 34 | 05:17:38 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 35 | 05:18:04 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 36 | 05:20:40 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 37 | 05:20:40 | command | $ python3 EXPERIMENTS/034-reask-tail/check.py |
| 38 | 05:20:41 | command | $ python3 EXPERIMENTS/034-reask-tail/reask.py report |
| 39 | 05:20:53 | command | $ python3 EXPERIMENTS/034-reask-tail/tally.py --check |
| 40 | 05:43:23 | artifact | wrote EXPERIMENTS/034-reask-tail/PROTOCOL.md |
| 110 | 06:09:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/034-reask-tail/raw/r1.jsonl |
| 111 | 06:09:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/034-reask-tail/raw/r2.jsonl |
| 112 | 06:09:52 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/034-reask-tail/raw/tally.json |
| 113 | 06:09:52 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 114 | 06:09:52 | doc_update | updated DECISIONS-SCREENING-6.md |
| 115 | 06:09:52 | doc_update | updated DECISIONS.md |
| 116 | 06:09:52 | doc_update | updated FAILURES.md |
| 117 | 06:09:52 | doc_update | updated ROADMAP.md |
| 118 | 06:09:52 | doc_update | updated STATE.md |
| 119 | 06:09:52 | session_end | E034 (T-0078) ran, reported and completed. Pooled duplicate-closure rate 0.1352 CI95 [0.1122,0.1620] in the score tail against 0.0303 [0.0201,0.0455]  |

_69 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-003-test-whether-stack-exchange-s-duplicate/events.jsonl
```

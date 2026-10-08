# Session 2026-10-08-013-e063-run-the-e062-answerability-instrume

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-08T08:05:49+00:00
- **Duration:** 6774.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

E063: run the E062 answerability instrument on the mission's own need corpora (189 GitHub issues, 1401 HN need rows) and decide whether the need-statement route selects unmet need or already-served statements

## Summary

E063 ran the E062 answerability instrument on the mission's own corpora: unserved-open is 0 of 103 rows (arm A served 0.676, arm B 0.969), so the trigger-phrase need-statement route selects served statements and is retired as a candidate source (F098, D085). Repaired defect 24 with a flocked stream allocator and .finish.lock; 452 tests green.

## Next

A fresh observation of a need this harvest cannot show: a population that generates no statement because the harm is invisible to the requester.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/063-own-corpus-answerability/PROTOCOL.md | 43044dfa9a09 | 7475 |
| EXPERIMENTS/063-own-corpus-answerability/README.md | b44e0bb03c5c | 6898 |
| EXPERIMENTS/063-own-corpus-answerability/AMENDMENT-1.md | 1706233bf46b | 3688 |
| EXPERIMENTS/063-own-corpus-answerability/raw/verdicts.json | bb72ca849a3e | 2329 |
| EXPERIMENTS/063-own-corpus-answerability/raw/remedy-verification.json | f77143d11e6f | 7069 |
| EXPERIMENTS/063-own-corpus-answerability/raw/labels-pass1.tsv | 2bd498252d82 | 16381 |
| EXPERIMENTS/063-own-corpus-answerability/PROTOCOL.md | 43044dfa9a09 | 7475 |
| EXPERIMENTS/063-own-corpus-answerability/README.md | b44e0bb03c5c | 6898 |
| EXPERIMENTS/063-own-corpus-answerability/AMENDMENT-1.md | 1706233bf46b | 3688 |
| EXPERIMENTS/063-own-corpus-answerability/sample.py | 945fca3fff27 | 7644 |
| EXPERIMENTS/063-own-corpus-answerability/outcome.py | c4b1b34d3fb9 | 5525 |
| EXPERIMENTS/063-own-corpus-answerability/verify.py | dc12cbfd721d | 5754 |
| EXPERIMENTS/063-own-corpus-answerability/raw/verdicts.json | bb72ca849a3e | 2329 |
| EXPERIMENTS/063-own-corpus-answerability/raw/remedy-verification.json | f77143d11e6f | 7069 |
| EXPERIMENTS/063-own-corpus-answerability/raw/labels-pass1.tsv | 2bd498252d82 | 16381 |
| EXPERIMENTS/063-own-corpus-answerability/raw/control-key.json | 4e0b70a224bc | 382 |
| EXPERIMENTS/063-own-corpus-answerability/raw/controls.tsv | 79d2e0fc67d8 | 2590 |
| EXPERIMENTS/063-own-corpus-answerability/raw/queue.tsv | 2789bc3404fe | 55436 |
| EXPERIMENTS/063-own-corpus-answerability/raw/queue-unique.tsv | 6fa0add20305 | 52820 |
| EXPERIMENTS/063-own-corpus-answerability/raw/sample-armA.tsv | 8371b57fb663 | 32739 |
| EXPERIMENTS/063-own-corpus-answerability/raw/sample-armB.tsv | c29225f66bf9 | 16858 |
| sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/DEDUPE-008.md | 07f789300324 | 3431 |
| sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/repair-008.py | 1a3b8b1e4893 | 3050 |
| tools/originlib/sessionlock.py | 26ef9e9820af | 2740 |
| tests/test_event_stream_concurrency.py | 046d12906732 | 5944 |
| tests/test_finish_exclusion.py | 9b27b752f9bb | 12049 |
| tests/test_stream_allocation_rules.py | eac9dc0d4663 | 2381 |
| .gitignore | 6b16caed76d4 | 2514 |
| tools/originlib/events.py | 91078c95da33 | 6920 |
| tools/originlib/recorder.py | 8b1cef78deca | 4415 |
| tools/originlib/session.py | e425551ddf68 | 9448 |
| sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/events.jsonl | 84dd5a5a7093 | 70740 |
| sessions/INDEX.md | cd4a5703aabc | 6774 |
| EXPERIMENTS/README.md | 20fe0568aac0 | 9097 |
| docs/INDEX.md | e8d4593d9859 | 34162 |
| STATE.md | 63019d972398 | 47268 |
| FAILURES.md | 835e69316632 | 60339 |
| FAILURES-findings-33.md | 922a3830cb38 | 8710 |
| DECISIONS.md | 23a807840f6b | 14321 |
| DECISIONS-SCREENING-13.md | 4d9071663a44 | 20538 |
| STATE-defects.md | 08abfdc00d40 | 20768 |
| STATE-history-3.md | 0f8b41dd4a5d | 5848 |

## Commands

4 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 9 | ['python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 9879 |
| 10 | ['python3', 'EXPERIMENTS/063-own-corpus-answerability/outcome.py'] | 0 | 291 |
| 11 | ['python3', 'EXPERIMENTS/063-own-corpus-answerability/outcome.py'] | 0 | 210 |
| 48 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 1027488 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | tests/test_finish_exclusion_concurrent.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 08:05:49 | session_start | E063: run the E062 answerability instrument on the mission's own need corpora (189 GitHub issues, 1401 HN need rows) and decide whether the need-state |
| 2 | 08:06:47 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/PROTOCOL.md |
| 3 | 08:15:44 | milestone | labelled 123 rows (71 HN, 32 GitHub issues, 20 controls); G1 met 10/10 and 9/10; G2 met 22/23 after a channel correction; served share A 0.676, B 0.96 |
| 4 | 08:17:07 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/README.md |
| 5 | 08:17:08 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/AMENDMENT-1.md |
| 6 | 08:17:09 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/raw/verdicts.json |
| 7 | 08:17:09 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/raw/remedy-verification.json |
| 8 | 08:17:10 | artifact | wrote EXPERIMENTS/063-own-corpus-answerability/raw/labels-pass1.tsv |
| 9 | 08:57:12 | command | $ python3 -m unittest discover -s stage-lines |
| 10 | 09:08:27 | command | $ python3 EXPERIMENTS/063-own-corpus-answerability/outcome.py |
| 11 | 09:08:45 | command | $ python3 EXPERIMENTS/063-own-corpus-answerability/outcome.py |
| 12 | 09:18:13 | artifact | session 013: E063 evidence, defect-24 repair |
| 13 | 09:18:15 | artifact | session 013: E063 evidence, defect-24 repair |
| 14 | 09:18:16 | artifact | session 013: E063 evidence, defect-24 repair |
| 15 | 09:18:18 | artifact | session 013: E063 evidence, defect-24 repair |
| 16 | 09:18:19 | artifact | session 013: E063 evidence, defect-24 repair |
| 17 | 09:18:20 | artifact | session 013: E063 evidence, defect-24 repair |
| 18 | 09:18:21 | artifact | session 013: E063 evidence, defect-24 repair |
| 19 | 09:18:23 | artifact | session 013: E063 evidence, defect-24 repair |
| 20 | 09:18:25 | artifact | session 013: E063 evidence, defect-24 repair |
| 21 | 09:18:26 | artifact | session 013: E063 evidence, defect-24 repair |
| 22 | 09:18:27 | artifact | session 013: E063 evidence, defect-24 repair |
| 23 | 09:18:28 | artifact | session 013: E063 evidence, defect-24 repair |
| 24 | 09:18:29 | artifact | session 013: E063 evidence, defect-24 repair |
| 25 | 09:18:31 | artifact | session 013: E063 evidence, defect-24 repair |
| 26 | 09:18:32 | artifact | session 013: E063 evidence, defect-24 repair |
| 27 | 09:18:33 | artifact | session 013: E063 evidence, defect-24 repair |
| 28 | 09:18:35 | artifact | session 013: E063 evidence, defect-24 repair |
| 29 | 09:18:36 | artifact | session 013: E063 evidence, defect-24 repair |
| 30 | 09:18:37 | artifact | session 013: E063 evidence, defect-24 repair |
| 31 | 09:18:39 | artifact | session 013: E063 evidence, defect-24 repair |
| 32 | 09:18:40 | artifact | session 013: E063 evidence, defect-24 repair |
| 33 | 09:18:41 | artifact | session 013: E063 evidence, defect-24 repair |
| 34 | 09:18:43 | artifact | session 013: E063 evidence, defect-24 repair |
| 35 | 09:18:44 | artifact | session 013: E063 evidence, defect-24 repair |
| 36 | 09:18:46 | artifact | session 013: E063 evidence, defect-24 repair |
| 37 | 09:18:47 | artifact | session 013: E063 evidence, defect-24 repair |
| 38 | 09:18:48 | artifact | session 013: E063 evidence, defect-24 repair |
| 39 | 09:18:49 | artifact | session 013: E063 evidence, defect-24 repair |
| 40 | 09:18:50 | artifact | session 013: E063 evidence, defect-24 repair |
| 45 | 09:19:12 | artifact | docs: F098, D085, defect 24, STATE/FAILURES/DECISIONS updates |
| 46 | 09:19:13 | artifact | docs: F098, D085, defect 24, STATE/FAILURES/DECISIONS updates |
| 47 | 09:19:15 | artifact | docs: F098, D085, defect 24, STATE/FAILURES/DECISIONS updates |
| 48 | 09:24:34 | command | $ python3 -m unittest discover -s tests -t tests |
| 49 | 09:58:42 | unlogged_change | changed but never declared as an artifact: tests/test_finish_exclusion_concurrent.py |
| 50 | 09:58:43 | doc_update | updated DECISIONS-SCREENING-13.md |
| 51 | 09:58:43 | doc_update | updated DECISIONS.md |
| 52 | 09:58:43 | doc_update | updated FAILURES.md |
| 53 | 09:58:43 | doc_update | updated STATE.md |
| 54 | 09:58:43 | session_end | E063 ran the E062 answerability instrument on the mission's own corpora: unserved-open is 0 of 103 rows (arm A served 0.676, arm B 0.969), so the trig |

_4 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/events.jsonl
```

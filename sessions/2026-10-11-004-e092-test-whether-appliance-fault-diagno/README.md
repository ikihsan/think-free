# Session 2026-10-11-004-e092-test-whether-appliance-fault-diagno

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T02:12:48+00:00
- **Duration:** 6060.4s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E092: test whether appliance-fault diagnosis is a general need outside one vendor's forum (multi-vendor venue, vendor/repair-bound rows screened out per D103)

## Summary

Worker completed E092 (G0 10/10 answered + 10/10 declined; G1 66/150 diagnosis-shaped 44.0%; K1 30/37 = 0.8108 CI95 [0.6580, 0.9052]; Arm A 0/40 program-shaped), landed F115 + D104 + STATE paragraph + E091 Steam correction, then the process died before committing (no session_end, tree dirty). Recovery instance: declared the landed artifacts, fixed the openai-key false positive that refused pool.jsonl, committed the records (f6627eae) and the fix (b9d7d96d), closed the session.

## Next

Fresh observation in a new domain per D103: software-owning venue, or report ownership mix beside the rate, or screen vendor- and repair-bound needs out before computing a share.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| DECISIONS-SCREENING-18.md | 2d45cd9211a4 | 12879 |
| DECISIONS.md | 23505c0a0a89 | 20660 |
| FAILURES-findings-37.md | 19c35221f432 | 17720 |
| FAILURES-findings-38.md | e8374cd61242 | 4142 |
| FAILURES.md | e1ccfc3a0eca | 70767 |
| STATE-next-actions.md | d29410706ac7 | 12262 |
| STATE.md | 07adee432780 | 23988 |
| docs/INDEX.md | 5a4114053457 | 44816 |
| sessions/INDEX.md | 17ccdaaa3a30 | 6803 |
| EXPERIMENTS/091-anova-answerability/RESULT.md | bb5a8a14b9a7 | 9602 |
| EXPERIMENTS/092-appliance-diagnosis/PROTOCOL.md | f5914c74a0d8 | 5530 |
| EXPERIMENTS/092-appliance-diagnosis/RESULT.md | 97248ecfec30 | 6953 |
| EXPERIMENTS/092-appliance-diagnosis/attempts.jsonl | 64809c4e962b | 24637 |
| EXPERIMENTS/092-appliance-diagnosis/attempts.py | 38ddef1922b6 | 1956 |
| EXPERIMENTS/092-appliance-diagnosis/attempts_sample_1_20.py | 3c4f62d4bcb0 | 11583 |
| EXPERIMENTS/092-appliance-diagnosis/attempts_sample_21_40.py | ab933dc0b9ce | 11617 |
| EXPERIMENTS/092-appliance-diagnosis/fetch-log.jsonl | 29844150a4af | 2783 |
| EXPERIMENTS/092-appliance-diagnosis/fetch.py | bd964aea5727 | 3254 |
| EXPERIMENTS/092-appliance-diagnosis/fetch_threads.py | 502c25991926 | 2558 |
| EXPERIMENTS/092-appliance-diagnosis/g0_probes.json | 012490ee30d0 | 8744 |
| EXPERIMENTS/092-appliance-diagnosis/g0_probes.py | 187160d82e19 | 9352 |
| EXPERIMENTS/092-appliance-diagnosis/grade-0-10.txt | 919805485f34 | 28991 |
| EXPERIMENTS/092-appliance-diagnosis/grade-10-20.txt | 5bd72caf71a9 | 21238 |
| EXPERIMENTS/092-appliance-diagnosis/grade-20-30.txt | d99801156e4c | 20289 |
| EXPERIMENTS/092-appliance-diagnosis/grade-30-40.txt | 607f0ac26ee7 | 24756 |
| EXPERIMENTS/092-appliance-diagnosis/grade_dump.py | d7b4afa12438 | 1366 |
| EXPERIMENTS/092-appliance-diagnosis/grades.jsonl | 104a30520755 | 43148 |
| EXPERIMENTS/092-appliance-diagnosis/grades.py | d80d17d10b11 | 1965 |
| EXPERIMENTS/092-appliance-diagnosis/grades_sample_1_20.py | f8b901b1c6d9 | 9187 |
| EXPERIMENTS/092-appliance-diagnosis/grades_sample_21_40.py | af979597f06e | 9946 |
| EXPERIMENTS/092-appliance-diagnosis/pool.jsonl | 201e151e1842 | 1258412 |

## Commands

13 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '-c', "\nimport urllib.request, json\nu='https://api.stackexchange.com/2.3/search/advanced?site=diy&tagged=appliance&answered=false&sort=v | 0 | 570 |
| 3 | ['python3', '-c', "\nimport urllib.request, json\nu='https://api.stackexchange.com/2.3/search/advanced?site=diy&tagged=appliance&answered=false&sort=v | 0 | 817 |
| 4 | ['python3', '-c', "\nimport urllib.request, json\ndef get(u):\n    return json.load(urllib.request.urlopen(u, timeout=30))\n# does the tag exist on di | 0 | 1905 |
| 5 | ['python3', '-c', "\nimport urllib.request, json\ndef get(u):\n    return json.load(urllib.request.urlopen(u, timeout=30))\nd=get('https://api.stackex | 0 | 1498 |
| 6 | ['python3', 'EXPERIMENTS/092-appliance-diagnosis/fetch.py'] | 1 | 8616 |
| 7 | ['python3', 'EXPERIMENTS/092-appliance-diagnosis/fetch.py'] | 0 | 6208 |
| 8 | ['python3', 'EXPERIMENTS/092-appliance-diagnosis/g0_probes.py'] | 0 | 98 |
| 9 | ['python3', 'EXPERIMENTS/092-appliance-diagnosis/attempts.py'] | 1 | 577 |
| 10 | ['python3', 'attempts.py'] | 0 | 93 |
| 11 | ['python3', 'fetch_threads.py'] | 0 | 1779 |
| 12 | ['python3', 'fetch_threads.py'] | 0 | 3609 |
| 13 | ['python3', 'grades.py'] | 0 | 191 |
| 14 | ['python3', 'score.py'] | 0 | 901 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 12 |
| declared artifacts now missing | 0 |
| integrity errors | 1 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/results.json |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/sample.tsv |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/score.py |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/screen-0-50.txt |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/screen-100-150.txt |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/screen-50-100.txt |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/screen.py |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/screening.tsv |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/thread-fetch-log.jsonl |
|   undeclared | EXPERIMENTS/092-appliance-diagnosis/threads.jsonl |
|   error | refused artifact EXPERIMENTS/092-appliance-diagnosis/pool.jsonl: secret pattern(s) openai-key |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:12:48 | session_start | E092: test whether appliance-fault diagnosis is a general need outside one vendor's forum (multi-vendor venue, vendor/repair-bound rows screened out p |
| 2 | 02:17:05 | command | $ python3 -c  import urllib.request, json u='https://api.stackexchange.com/2.3/search/advanced?site=diy&tagged=appliance&answered=false&sort=v |
| 3 | 02:17:38 | command | $ python3 -c  import urllib.request, json u='https://api.stackexchange.com/2.3/search/advanced?site=diy&tagged=appliance&answered=false&sort=v |
| 4 | 02:17:51 | command | $ python3 -c  import urllib.request, json def get(u):     return json.load(urllib.request.urlopen(u, timeout=30)) # does the tag exist on diy? |
| 5 | 02:18:31 | command | $ python3 -c  import urllib.request, json def get(u):     return json.load(urllib.request.urlopen(u, timeout=30)) d=get('https://api.stackexch |
| 6 | 02:21:30 | command | $ python3 EXPERIMENTS/092-appliance-diagnosis/fetch.py |
| 7 | 02:21:52 | command | $ python3 EXPERIMENTS/092-appliance-diagnosis/fetch.py |
| 8 | 02:34:29 | command | $ python3 EXPERIMENTS/092-appliance-diagnosis/g0_probes.py |
| 9 | 02:38:47 | command | $ python3 EXPERIMENTS/092-appliance-diagnosis/attempts.py |
| 10 | 02:40:21 | command | $ python3 attempts.py |
| 11 | 02:40:53 | command | $ python3 fetch_threads.py |
| 12 | 02:42:07 | command | $ python3 fetch_threads.py |
| 13 | 02:49:46 | command | $ python3 grades.py |
| 14 | 03:01:20 | command | $ python3 score.py |
| 15 | 03:24:01 | milestone | E092 landed in records: F115 in FAILURES-findings-38.md with FAILURES.md row, D104 in DECISIONS-SCREENING-18.md with DECISIONS.md row, STATE.md E092 p |
| 16 | 03:39:03 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 17 | 03:39:04 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 18 | 03:39:04 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 19 | 03:39:05 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 20 | 03:39:06 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 21 | 03:39:06 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 22 | 03:39:07 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 23 | 03:39:08 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 24 | 03:39:08 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 25 | 03:39:09 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 26 | 03:39:10 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 27 | 03:39:10 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 28 | 03:39:11 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 29 | 03:39:12 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 30 | 03:39:13 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 31 | 03:39:15 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 32 | 03:39:15 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 33 | 03:39:16 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 34 | 03:39:17 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 35 | 03:39:17 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 36 | 03:39:18 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 37 | 03:39:19 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 38 | 03:39:19 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 39 | 03:39:20 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 40 | 03:39:21 | artifact | E092 landed records, committed by recovery instance after worker process death |
| 55 | 03:53:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/screening.tsv |
| 56 | 03:53:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/thread-fetch-log.jsonl |
| 57 | 03:53:48 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/092-appliance-diagnosis/threads.jsonl |
| 58 | 03:53:48 | unlogged_change | changed but never declared as an artifact: tests/test_secrets.py |
| 59 | 03:53:48 | unlogged_change | changed but never declared as an artifact: tools/originlib/secrets.py |
| 60 | 03:53:49 | doc_update | updated DECISIONS-SCREENING-18.md |
| 61 | 03:53:49 | doc_update | updated DECISIONS.md |
| 62 | 03:53:49 | doc_update | updated FAILURES.md |
| 63 | 03:53:49 | doc_update | updated STATE.md |
| 64 | 03:53:49 | session_end | Worker completed E092 (G0 10/10 answered + 10/10 declined; G1 66/150 diagnosis-shaped 44.0%; K1 30/37 = 0.8108 CI95 [0.6580, 0.9052]; Arm A 0/40 progr |

_14 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-004-e092-test-whether-appliance-fault-diagno/events.jsonl
```

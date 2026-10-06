# Session 2026-10-05-006-measure-what-happened-to-e012-s-1401-pub

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `opencode`
- **Started:** 2026-10-05T03:45:05+00:00
- **Duration:** 124018.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Measure what happened to E012's 1401 public need statements: did the thread's own readers name a tool, and are the unanswered ones a usable candidate signal

## Summary

E039 measured what happened to E012's 1401 public need statements, the one channel that was still unmeasured: their own reply subtrees. All 1276 parent threads captured (278,686 comments), giving 1391 needs against 277,295 matched controls. The declared kill gate fired on three estimators (1.235x against a bar of 1.5 fixed before the first fetch), so attention to a need is not distinguishable from position in a thread. The finding that changes a decision: 0 of 1391 needs drew a reply naming a tool new to its thread and 1 of 794 requesters replied again, so the corpus records that a need was recognised and never that it was served - which explains why F029's 0-of-50 and F035's corpus silence are hard to contradict, closes item 0's last proposed axis, and is the fifth measurement agreeing the supply-side screens measure the wrong channel. Three defects in my own instruments are recorded against me: a declared gate that cannot fail (0 of everything), an endpoint that undercounts replies one-directionally, and a hand-written manifest whose sha256 fields were padded with hex never measured. No candidate was found and none is claimed.

## Next

The owner decision on what the mission selects candidates on is now fully informed and is the only thing blocking stage B: five measurements say supply-side counts do not carry it, and the one demand-side channel that could be read from public data records recognition rather than service. STATE-selection.md holds the reasoning and the ceilings. Alternatives if that decision is deferred: (a) run E2 side B, the lockfile two-snapshot drift comparison, which is banked and waiting on time to pass; (b) build a prototype for one named need from the 1250, which needs authorization to contact anyone and is the only route to a measured outcome signal this repository has now shown it lacks; (c) pick a fresh research direction unrelated to the prior-art screen entirely.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/021-need-statement-response/README.md | 8539a387ba0e | 7713 |
| EXPERIMENTS/021-need-statement-response/PROTOCOL.md | bb1dcc90856c | 8108 |
| EXPERIMENTS/021-need-statement-response/results.json | d19cf573242c | 5426 |
| EXPERIMENTS/021-need-statement-response/trigger_shape.json | 2dba1d70c399 | 5581 |
| EXPERIMENTS/021-need-statement-response/calibration.json | 825d259c7ae0 | 2454 |
| EXPERIMENTS/021-need-statement-response/read_order.json | 6b3dc26e8742 | 275 |
| EXPERIMENTS/021-need-statement-response/capture.py | 9440955b7d9a | 6221 |
| EXPERIMENTS/021-need-statement-response/merge.py | 5bfdb877138f | 1444 |
| EXPERIMENTS/021-need-statement-response/arms.py | a98fa8cef0e5 | 5950 |
| EXPERIMENTS/021-need-statement-response/stats.py | 49c0914dcb5a | 10513 |
| EXPERIMENTS/021-need-statement-response/trigger_shape.py | e7635239383d | 5074 |
| EXPERIMENTS/021-need-statement-response/read_silent.py | fc490509ffc1 | 1801 |
| EXPERIMENTS/021-need-statement-response/calibration.py | 0484c75b3c4c | 3631 |
| STATE.md | 85986eca1f9c | 29402 |
| STATE-selection.md | b7cdd2ecc6c1 | 6743 |
| STATE-history-3.md | f18d16afe0a0 | 4414 |
| STATE-next-actions.md | 3e350085a5e9 | 11908 |
| STATE-constraints.md | 4319d8f03358 | 11232 |
| DECISIONS-SCREENING-3.md | 0d6d936ae75c | 4880 |
| DECISIONS.md | 8260bf4d3853 | 7857 |
| DECISIONS-SCREENING-2.md | 0c44deba5456 | 18642 |
| FAILURES.md | 0bbab05047dd | 9327 |
| FAILURES-findings-16.md | bc4a9aa583cb | 7723 |
| RELEASE-MANIFEST.md | af08f72a6a89 | 4989 |
| .gitignore | 13213ae4cf28 | 1450 |
| EXPERIMENTS/README.md | 5c757941d9f5 | 3649 |
| EXPERIMENTS/020-copied-config-drift/README.md | 8829eea19bc9 | 13845 |
| docs/INDEX.md | e5e253201d70 | 25598 |
| tasks/INDEX.md | 6b60020b2aa3 | 8941 |
| tasks/T-0066-measure-what-happened-to-e012-s-1401-pub.md | 8a0f720f55f9 | 3236 |
| tools/originlib/paths.py | 1c9ded8f888c | 3998 |
| tools/originlib/reconcile.py | b9ad3ff7fd00 | 8062 |
| tests/test_decision_files.py | 85ba3de37363 | 3763 |
| EXPERIMENTS/021-need-statement-response/raw/arms.jsonl | af77ebbd4ca6 | 398503 |
| EXPERIMENTS/021-need-statement-response/raw/fetch_log.jsonl | a5f9a9ebd276 | 2418 |
| EXPERIMENTS/021-need-statement-response/raw/MANIFEST.json | 17014ab6355b | 4361 |
| EXPERIMENTS/021-need-statement-response/verify_manifest.py | 5452f7ec4f4f | 2585 |
| EXPERIMENTS/021-need-statement-response/trigger_shape.json | 2dba1d70c399 | 5581 |
| STATE-next-actions.md | 86d14b53237d | 19403 |
| STATE.md | 3b676fc756d5 | 42367 |
| STATE-selection.md | a6c0262d8b79 | 6743 |
| STATE-in-flight-4.md | 6e6491801215 | 6899 |
| STATE-history-3.md | 48b6e31c5403 | 4414 |
| STATE-next-actions.md | 91567630ca83 | 15106 |
| STATE-next-actions-closed.md | 9a4103e160d1 | 15939 |
| STATE-next-actions-closed-2.md | b3b5fda2755d | 10274 |
| STATE-constraints.md | 719340ac0dcc | 17408 |
| DECISIONS.md | 3a58b44713cf | 10109 |
| DECISIONS-SCREENING-2.md | 3076eaf7c1d8 | 18638 |
| DECISIONS-SCREENING-8.md | 6f20a9442917 | 5202 |
| FAILURES.md | 626eb5d51ea6 | 32410 |
| FAILURES-findings-25.md | 5aa31f6c2303 | 8147 |
| RELEASE-MANIFEST.md | ec79ecf87851 | 6556 |
| EXPERIMENTS/README.md | 0b56f262366e | 6884 |
| docs/INDEX.md | 98ad901d22df | 39812 |
| tools/originlib/paths.py | 34be56bc653d | 4158 |
| tools/originlib/reconcile.py | 2a41410ab250 | 8262 |
| tests/test_decision_files.py | 8ab726e0d271 | 4735 |
| tasks/INDEX.md | 7c089390604a | 8941 |
| tasks/T-0081-measure-what-happened-to-e012-s-1401-pub.md | 1454c34355b8 | 3233 |
| STATE-selection.md | 5f6eb7674d1c | 6966 |
| STATE-selection.md | 8753ce6828e5 | 8501 |
| STATE.md | 3b676fc756d5 | 42367 |
| STATE-selection.md | 8753ce6828e5 | 8501 |
| STATE-in-flight-4.md | 6e6491801215 | 6899 |
| STATE-next-actions.md | 91567630ca83 | 15106 |
| STATE-next-actions-closed.md | 9a4103e160d1 | 15939 |
| STATE-next-actions-closed-2.md | b3b5fda2755d | 10274 |
| STATE-history-3.md | 48b6e31c5403 | 4414 |
| ROADMAP.md | 6a47b3426b0c | 16115 |
| STATE.md | 16b5277315b2 | 42367 |

## Commands

13 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/021-need-statement-response/calibration.py'] | 0 | 40136 |
| 3 | ['python3', 'EXPERIMENTS/021-need-statement-response/arms.py'] | 1 | 821 |
| 4 | ['python3', 'EXPERIMENTS/021-need-statement-response/arms.py'] | 0 | 265 |
| 5 | ['python3', 'EXPERIMENTS/021-need-statement-response/merge.py'] | 0 | 893 |
| 6 | ['python3', 'EXPERIMENTS/021-need-statement-response/arms.py'] | 0 | 1730 |
| 7 | ['python3', 'EXPERIMENTS/021-need-statement-response/stats.py'] | 0 | 757 |
| 8 | ['python3', 'EXPERIMENTS/021-need-statement-response/merge.py'] | 0 | 113497 |
| 9 | ['python3', 'EXPERIMENTS/021-need-statement-response/stats.py'] | 0 | 17598248 |
| 24 | ['python3', 'EXPERIMENTS/021-need-statement-response/verify_manifest.py'] | 0 | 6581 |
| 25 | ['python3', 'EXPERIMENTS/021-need-statement-response/verify_manifest.py'] | 0 | 3868 |
| 54 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 705320 |
| 55 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 862917 |
| 82 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 1210417 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 17 |
| declared artifacts now missing | 0 |
| integrity errors | 19 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/039-need-statement-response/PROTOCOL.md |
|   undeclared | EXPERIMENTS/039-need-statement-response/README.md |
|   undeclared | EXPERIMENTS/039-need-statement-response/arms.py |
|   undeclared | EXPERIMENTS/039-need-statement-response/calibration.json |
|   undeclared | EXPERIMENTS/039-need-statement-response/calibration.py |
|   undeclared | EXPERIMENTS/039-need-statement-response/capture.py |
|   undeclared | EXPERIMENTS/039-need-statement-response/merge.py |
|   undeclared | EXPERIMENTS/039-need-statement-response/raw/MANIFEST.json |
|   undeclared | EXPERIMENTS/039-need-statement-response/raw/arms.jsonl |
|   undeclared | EXPERIMENTS/039-need-statement-response/raw/fetch_log.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/PROTOCOL.md |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/README.md |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/arms.py |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/calibration.json |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/calibration.py |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/capture.py |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/merge.py |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/raw/MANIFEST.json |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/raw/arms.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/raw/fetch_log.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 03:45:05 | session_start | Measure what happened to E012's 1401 public need statements: did the thread's own readers name a tool, and are the unanswered ones a usable candidate  |
| 2 | 03:48:10 | command | $ python3 EXPERIMENTS/021-need-statement-response/calibration.py |
| 3 | 03:56:05 | command | $ python3 EXPERIMENTS/021-need-statement-response/arms.py |
| 4 | 03:56:30 | command | $ python3 EXPERIMENTS/021-need-statement-response/arms.py |
| 5 | 03:58:27 | command | $ python3 EXPERIMENTS/021-need-statement-response/merge.py |
| 6 | 03:58:29 | command | $ python3 EXPERIMENTS/021-need-statement-response/arms.py |
| 7 | 03:58:30 | command | $ python3 EXPERIMENTS/021-need-statement-response/stats.py |
| 8 | 04:11:41 | command | $ python3 EXPERIMENTS/021-need-statement-response/merge.py |
| 9 | 09:16:03 | command | $ python3 EXPERIMENTS/021-need-statement-response/stats.py |
| 10 | 12:01:46 | milestone | E021 measured: kill gate fired on three estimators, 0/1391 needs drew a novel-host link, 1/794 requesters returned |
| 11 | 12:01:47 | artifact | wrote EXPERIMENTS/021-need-statement-response/README.md |
| 12 | 12:01:47 | artifact | wrote EXPERIMENTS/021-need-statement-response/PROTOCOL.md |
| 13 | 12:01:48 | artifact | wrote EXPERIMENTS/021-need-statement-response/results.json |
| 14 | 12:01:48 | artifact | wrote EXPERIMENTS/021-need-statement-response/trigger_shape.json |
| 15 | 12:01:49 | artifact | wrote EXPERIMENTS/021-need-statement-response/calibration.json |
| 16 | 12:01:49 | artifact | wrote EXPERIMENTS/021-need-statement-response/read_order.json |
| 17 | 12:01:55 | artifact | wrote EXPERIMENTS/021-need-statement-response/capture.py |
| 18 | 12:01:56 | artifact | wrote EXPERIMENTS/021-need-statement-response/merge.py |
| 19 | 12:01:56 | artifact | wrote EXPERIMENTS/021-need-statement-response/arms.py |
| 20 | 12:01:57 | artifact | wrote EXPERIMENTS/021-need-statement-response/stats.py |
| 21 | 12:01:58 | artifact | wrote EXPERIMENTS/021-need-statement-response/trigger_shape.py |
| 22 | 12:01:58 | artifact | wrote EXPERIMENTS/021-need-statement-response/read_silent.py |
| 23 | 12:01:59 | artifact | wrote EXPERIMENTS/021-need-statement-response/calibration.py |
| 24 | 12:03:24 | command | $ python3 EXPERIMENTS/021-need-statement-response/verify_manifest.py |
| 25 | 12:05:40 | command | $ python3 EXPERIMENTS/021-need-statement-response/verify_manifest.py |
| 26 | 12:48:38 | artifact | wrote STATE.md |
| 27 | 12:48:42 | artifact | wrote STATE-selection.md |
| 28 | 12:48:44 | artifact | wrote STATE-history-3.md |
| 29 | 12:48:47 | artifact | wrote STATE-next-actions.md |
| 30 | 12:48:51 | artifact | wrote STATE-constraints.md |
| 31 | 12:48:54 | artifact | wrote DECISIONS-SCREENING-3.md |
| 32 | 12:48:57 | artifact | wrote DECISIONS.md |
| 33 | 12:49:00 | artifact | wrote DECISIONS-SCREENING-2.md |
| 34 | 12:49:03 | artifact | wrote FAILURES.md |
| 35 | 12:49:06 | artifact | wrote FAILURES-findings-16.md |
| 36 | 12:49:08 | artifact | wrote RELEASE-MANIFEST.md |
| 37 | 12:49:11 | artifact | wrote .gitignore |
| 38 | 12:49:14 | artifact | wrote EXPERIMENTS/README.md |
| 39 | 12:49:17 | artifact | wrote EXPERIMENTS/020-copied-config-drift/README.md |
| 40 | 12:49:20 | artifact | wrote docs/INDEX.md |
| 128 | 14:11:45 | integrity_error | declared artifact no longer exists: EXPERIMENTS/021-need-statement-response/verify_manifest.py |
| 129 | 14:11:45 | integrity_error | declared artifact no longer exists: tasks/T-0066-measure-what-happened-to-e012-s-1401-pub.md |
| 130 | 14:12:03 | integrity_error | HYPOTHESES.md was not updated although the session recorded experiment_result |
| 131 | 14:12:03 | doc_update | updated DECISIONS-SCREENING-2.md |
| 132 | 14:12:04 | doc_update | updated DECISIONS-SCREENING-8.md |
| 133 | 14:12:04 | doc_update | updated DECISIONS.md |
| 134 | 14:12:04 | doc_update | updated FAILURES.md |
| 135 | 14:12:04 | doc_update | updated ROADMAP.md |
| 136 | 14:12:04 | doc_update | updated STATE.md |
| 137 | 14:12:04 | session_end | E039 measured what happened to E012's 1401 public need statements, the one channel that was still unmeasured: their own reply subtrees. All 1276 paren |

_87 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-006-measure-what-happened-to-e012-s-1401-pub/events.jsonl
```

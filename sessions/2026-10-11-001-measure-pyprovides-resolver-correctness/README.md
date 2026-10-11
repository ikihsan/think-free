# Session 2026-10-11-001-measure-pyprovides-resolver-correctness

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-11T00:03:04+00:00
- **Duration:** 6780.3s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Measure pyprovides resolver correctness on real independent import-error reports, with the hardcoded alias table ablated, against the strongest accessible alternatives

## Summary

E100 (F114, D103): query-time resolver vs strongest alternatives on real import-error modules, alias table ablated. On the pre-declared home-turf population B (10 alias modules with live SE reports): general assistant 10/10, resolver as shipped 9/10, resolver ablated 8/10, alias table alone 9/10, pip install M 1/10. KILL-R fires (arm5 >= arm4); CARRY fails; KILL-M not-met (arm3 != arm4 by one row, cv2). pyprovides withdrawn as a candidate; package-name line closed on measured grounds. Two scorer defects repaired before any number was read, both in the direction of punishing arm 5.

## Next

Land E100 evidence; repair the .gitignore defect that dropped 26 session reports; resume E102 (DIY arrival read) when the SE daily quota resets at 00:00 UTC.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md | ac86b50db79b | 3998 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py | bd94c5a76108 | 7513 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json | eb0f9a8e500d | 2333 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py | d2b1de47d8c6 | 7755 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py | 739aae3f86fd | 7779 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json | b67faa3fe551 | 10028 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/third-party-verify.json | d4092d46c896 | 1318 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/sdist-check.md | 7a4c368c88ed | 915 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json | 76829c5ec9f1 | 1926 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md | ac86b50db79b | 3998 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/VERDICT.md | 8c6001dd1537 | 7400 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json | 76829c5ec9f1 | 1926 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-1-4.json | 40f7d9153e9a | 7421 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-3-ablated.json | bc6a727cef8a | 7369 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/categories.json | 8b6f96a4deca | 2774 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth-v2.json | 0261041ede3b | 21100 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json | b67faa3fe551 | 10028 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json | eb0f9a8e500d | 2333 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/rescore.py | 4c1ca1f52696 | 10554 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py | 739aae3f86fd | 7779 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/score.py | 7e04649fe8a1 | 7145 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored-v2.json | a3152fc3d38c | 9603 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored.json | f1a954251a2b | 10234 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/sdist-check.md | 7a4c368c88ed | 915 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_threads.py | 88bd54ba1730 | 6260 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md | ac86b50db79b | 3998 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/VERDICT.md | 8c6001dd1537 | 7400 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json | 76829c5ec9f1 | 1926 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-1-4.json | 40f7d9153e9a | 7421 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-3-ablated.json | bc6a727cef8a | 7369 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/categories.json | 8b6f96a4deca | 2774 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth-v2.json | 0261041ede3b | 21100 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json | b67faa3fe551 | 10028 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json | eb0f9a8e500d | 2333 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/rescore.py | 4c1ca1f52696 | 10554 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py | 739aae3f86fd | 7779 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/score.py | 7e04649fe8a1 | 7145 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored-v2.json | a3152fc3d38c | 9603 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored.json | f1a954251a2b | 10234 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/sdist-check.md | 7a4c368c88ed | 915 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_threads.py | 88bd54ba1730 | 6260 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_truth.py | 5a9442d159fa | 9712 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/threads-extract.json | 528942e52cc1 | 40458 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/threads-raw.json | 6b51577e093f | 154413 |
| EXPERIMENTS/100-query-time-resolver-vs-alternatives/verified-suggestions.json | fa2cd81765b0 | 10979 |
| .gitignore | c6b4ce122ca6 | 4767 |

## Commands

1 captured, 0 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 56 | ['python3', 'EXPERIMENTS/100-query-time-resolver-vs-alternatives/rescore.py'] | 0 | 211 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 36 |
| declared artifacts now missing | 0 |
| integrity errors | 2 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-18.md |
|   undeclared | FAILURES-findings-37.md |
|   undeclared | README.md |
|   undeclared | RELEASE-MANIFEST.md |
|   undeclared | pyprovides/MANIFEST.in |
|   undeclared | pyprovides/pyproject.toml |
|   undeclared | sessions/2026-10-09-012-explore-fresh-observations-on-non-softwa/commands.log |
|   undeclared | sessions/2026-10-09-012-explore-fresh-observations-on-non-softwa/events.jsonl |
|   undeclared | sessions/2026-10-09-013-continue-view-count-measurement-investig/events.jsonl |
|   undeclared | sessions/2026-10-09-014-fresh-observation-in-a-new-non-software/commands.log |
|   error | refused artifact EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_truth.py: secret pattern(s) assigned-credenti |
|   error | refused artifact EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_truth.py: secret pattern(s) assigned-credenti |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:03:04 | session_start | Measure pyprovides resolver correctness on real independent import-error reports, with the hardcoded alias table ablated, against the strongest access |
| 2 | 00:05:51 | milestone | Adopted session; target is D099's promoted experiment: resolver correctness with alias ablation vs strongest alternatives |
| 3 | 00:06:30 | milestone | E091 positives enumerated: 23 unique modules, zero alias cases; session-019 publication claim false (PyPI 404); repairing release-state markers, then  |
| 4 | 00:10:30 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md |
| 5 | 00:10:38 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py |
| 6 | 00:10:42 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json |
| 7 | 00:11:52 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py |
| 8 | 00:11:56 | milestone | PROTOCOL frozen; population B 10/10 real reports; ground-truth downloads in background; release-state falsehood repaired |
| 9 | 00:14:40 | note | Adopted session post-restart; pre-restart state verified: PROTOCOL frozen, population-b 10/10, ground-truth download stage running (PID 1638382); rele |
| 10 | 00:20:30 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py |
| 11 | 00:20:32 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json |
| 12 | 00:20:35 | milestone | Ground truth frozen for 33 modules; two pre-arm repairs recorded (POP_A git->voluptuous_openapi; depthflow case-match corrected) |
| 13 | 00:30:16 | milestone | Adopted after restart. Ground-truth v1 audited by hand: demonstrably incomplete for >=6 of 33 modules (dbus, telegram, pyspark, google, module1, depth |
| 14 | 00:46:47 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/third-party-verify.json |
| 15 | 00:46:49 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/sdist-check.md |
| 16 | 00:46:50 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json |
| 17 | 00:46:52 | milestone | Third-party suggestions verified by wheel inspection (adafruit-blinka, python-telegram-bot, voluptuous-openapi ship M; google-api-python-client does n |
| 18 | 00:51:24 | task_rewrite | appended a create record for T-0091 |
| 19 | 01:21:11 | milestone | Adopted in-flight E100: protocol frozen, ground truth arm-blind and verified; found 4 instrument defects (3 ground-truth holes that punish arm5, score |
| 20 | 01:33:34 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md |
| 21 | 01:33:36 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/VERDICT.md |
| 22 | 01:33:36 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json |
| 23 | 01:33:37 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-1-4.json |
| 24 | 01:33:38 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/arms-3-ablated.json |
| 25 | 01:33:38 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/categories.json |
| 26 | 01:33:39 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth-v2.json |
| 27 | 01:33:40 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/ground-truth.json |
| 28 | 01:33:41 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/population-b.json |
| 29 | 01:33:41 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/rescore.py |
| 30 | 01:33:42 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/run.py |
| 31 | 01:33:43 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/score.py |
| 32 | 01:33:43 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored-v2.json |
| 33 | 01:33:44 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/scored.json |
| 34 | 01:33:45 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/sdist-check.md |
| 35 | 01:33:45 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_threads.py |
| 36 | 01:33:46 | integrity_error | refused artifact EXPERIMENTS/100-query-time-resolver-vs-alternatives/stage_truth.py: secret pattern(s) assigned-credential |
| 37 | 01:33:46 | milestone | E100 scored: KILL-R fires on B (arm5 10/10 vs arm4 9/10); CARRY fails; pyprovides leaves the candidate line |
| 38 | 01:34:14 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/PROTOCOL.md |
| 39 | 01:34:15 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/VERDICT.md |
| 40 | 01:34:15 | artifact | wrote EXPERIMENTS/100-query-time-resolver-vs-alternatives/arm5-verbatim.json |
| 90 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-014-fresh-observation-in-aviation-maintenanc/events.jsonl |
| 91 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-016-package-pyprovides-for-distribution-and/events.jsonl |
| 92 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-017-package-pyprovides-for-distribution-and/events.jsonl |
| 93 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-018-finalize-pyprovides-packaging-for-distri/events.jsonl |
| 94 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-019-publish-pyprovides-to-pypi-and-measure-a/events.jsonl |
| 95 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-020-measure-pyprovides-adoption-and-evaluate/events.jsonl |
| 96 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-021-package-pyprovides-resolver-for-pypi-dis/events.jsonl |
| 97 | 01:56:05 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-10-022-prepare-pyprovides-for-pypi-publication/events.jsonl |
| 98 | 01:56:05 | doc_update | updated DECISIONS-SCREENING-18.md |
| 99 | 01:56:05 | session_end | E100 (F114, D103): query-time resolver vs strongest alternatives on real import-error modules, alias table ablated. On the pre-declared home-turf popu |

_49 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-11-001-measure-pyprovides-resolver-correctness/events.jsonl
```

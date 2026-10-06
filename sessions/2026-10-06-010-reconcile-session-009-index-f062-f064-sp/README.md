# Session 2026-10-06-010-reconcile-session-009-index-f062-f064-sp

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T11:07:00+00:00
- **Duration:** 116.4s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Reconcile session 009: index F062-F064, split oversized files, declare all artifacts, commit E038

## Summary

Session 009 reconciled: F062-F064 indexed, oversized files split, both decision-file list copies updated, doc lint OK, stage-lines 30 tests and E038 compare rerun green

## Next

Choose and run the demand-side evaluation for the stg candidate (KILL-Q), or a fresh observation per the owner brief

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| DECISIONS-SCREENING-9.md | 32bf18193bb6 | 4700 |
| DECISIONS.md | 621ec4706941 | 11080 |
| EXPERIMENTS/038-staging-prior-art/harvest_core.py | 8837393f3589 | 7799 |
| EXPERIMENTS/038-staging-prior-art/harvest_pools.py | 76a4660893f8 | 6751 |
| EXPERIMENTS/038-staging-prior-art/raw/compare.jsonl | bda1dd708641 | 36579 |
| EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl | a4464250caf0 | 3572297 |
| FAILURES-findings-25.md | f045d22b9c58 | 5024 |
| FAILURES-findings-26.md | 705cf5f6f207 | 7183 |
| FAILURES.md | 352e4b025779 | 35270 |
| HYPOTHESES-candidates.md | 142dd006089a | 8612 |
| RELEASE-MANIFEST.md | caea1b1848c9 | 5805 |
| STATE.md | 2a4bdf660753 | 36232 |
| stage-lines/stagelib_change.py | 4f22e06914e8 | 3007 |
| stage-lines/stagelib_split.py | fa0ec9ef6a86 | 3600 |
| tests/test_decision_files.py | fa28211c0c30 | 4468 |
| tools/originlib/paths.py | 693ef0cf36e4 | 4190 |
| tools/originlib/reconcile.py | 4cdc709ec4b6 | 8294 |
| vendor/MANIFEST.md | 446ae38c6b78 | 6990 |
| EXPERIMENTS/037-line-staging/driver.py | 49ef684ca4e8 | 5482 |
| stage-lines/stagelib.py | ab63f8535b32 | 5734 |
| stage-lines/test_parser.py | e1aa960135f5 | 2595 |
| stage-lines/test_stage.py | 77575349ecc1 | 12312 |
| stage-lines/tests_support.py | 27dbbda30b6b | 3555 |
| docs/INDEX.md | ccae7e678aa2 | 39887 |
| sessions/INDEX.md | 0f393e77b924 | 6799 |
| EXPERIMENTS/038-staging-prior-art/PROTOCOL.md | e99fb7bd346a | 6705 |
| EXPERIMENTS/038-staging-prior-art/README.md | 7c74e9e240f6 | 16663 |
| EXPERIMENTS/038-staging-prior-art/compare.py | 2c0440bbbb61 | 9250 |
| EXPERIMENTS/038-staging-prior-art/harvest.py | 141139ddc40d | 1628 |
| EXPERIMENTS/038-staging-prior-art/precision.py | f4ea9b1dd7d6 | 4540 |
| EXPERIMENTS/038-staging-prior-art/readout.py | faa73bbf9a1a | 5866 |
| EXPERIMENTS/038-staging-prior-art/score.py | 5cde1b8dc5ef | 7392 |
| sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/commands.log | 36a83f4667a4 | 93781 |
| sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/events.jsonl | b4f42154da04 | 34073 |

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 28 | ['PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision_files'] | 127 | 4 |
| 29 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests', '-k', 'decision_files'] | 0 | 525 |
| 30 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'stage-lines'] | 0 | 9711 |
| 31 | ['env', 'FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff', 'python3', 'EXPERIMENTS/038-staging-prior-art/compare.py'] | 0 | 43516 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 9 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/038-staging-prior-art/PROTOCOL.md |
|   undeclared | EXPERIMENTS/038-staging-prior-art/README.md |
|   undeclared | EXPERIMENTS/038-staging-prior-art/compare.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/harvest.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/precision.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/readout.py |
|   undeclared | EXPERIMENTS/038-staging-prior-art/score.py |
|   undeclared | sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/commands.log |
|   undeclared | sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:07:00 | session_start | Reconcile session 009: index F062-F064, split oversized files, declare all artifacts, commit E038 |
| 2 | 11:07:09 | artifact | wrote DECISIONS-SCREENING-9.md |
| 3 | 11:07:09 | artifact | wrote DECISIONS.md |
| 4 | 11:07:10 | artifact | wrote EXPERIMENTS/038-staging-prior-art/harvest_core.py |
| 5 | 11:07:11 | artifact | wrote EXPERIMENTS/038-staging-prior-art/harvest_pools.py |
| 6 | 11:07:12 | artifact | wrote EXPERIMENTS/038-staging-prior-art/raw/compare.jsonl |
| 7 | 11:07:15 | artifact | wrote EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl |
| 8 | 11:07:16 | artifact | wrote FAILURES-findings-25.md |
| 9 | 11:07:16 | artifact | wrote FAILURES-findings-26.md |
| 10 | 11:07:17 | artifact | wrote FAILURES.md |
| 11 | 11:07:17 | artifact | wrote HYPOTHESES-candidates.md |
| 12 | 11:07:18 | artifact | wrote RELEASE-MANIFEST.md |
| 13 | 11:07:19 | artifact | wrote STATE.md |
| 14 | 11:07:19 | artifact | wrote stage-lines/stagelib_change.py |
| 15 | 11:07:20 | artifact | wrote stage-lines/stagelib_split.py |
| 16 | 11:07:20 | artifact | wrote tests/test_decision_files.py |
| 17 | 11:07:21 | artifact | wrote tools/originlib/paths.py |
| 18 | 11:07:22 | artifact | wrote tools/originlib/reconcile.py |
| 19 | 11:07:22 | artifact | wrote vendor/MANIFEST.md |
| 20 | 11:07:23 | artifact | wrote EXPERIMENTS/037-line-staging/driver.py |
| 21 | 11:07:23 | artifact | wrote stage-lines/stagelib.py |
| 22 | 11:07:24 | artifact | wrote stage-lines/test_parser.py |
| 23 | 11:07:25 | artifact | wrote stage-lines/test_stage.py |
| 24 | 11:07:25 | artifact | wrote stage-lines/tests_support.py |
| 25 | 11:07:26 | artifact | wrote docs/INDEX.md |
| 26 | 11:07:26 | artifact | wrote sessions/INDEX.md |
| 27 | 11:07:32 | milestone | Reconciled: FAILURES.md indexes F062-F064 via findings-26, prose list gained findings-25/26, stagelib split into stagelib_change+stagelib_split (30 te |
| 28 | 11:07:42 | command | $ PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision_files |
| 29 | 11:07:47 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests -k decision_files |
| 30 | 11:08:02 | command | $ env PYTHONPATH=tools:tests python3 -m unittest discover -s stage-lines |
| 31 | 11:08:50 | command | $ env FILTERDIFF=/tmp/opencode/pu/x/usr/bin/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py |
| 32 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/PROTOCOL.md |
| 33 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/README.md |
| 34 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/compare.py |
| 35 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/harvest.py |
| 36 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/precision.py |
| 37 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/readout.py |
| 38 | 11:08:56 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/038-staging-prior-art/score.py |
| 39 | 11:08:56 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/commands.log |
| 40 | 11:08:56 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-06-009-test-e037-s-two-open-gates-does-the-ecos/events.jsonl |
| 46 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 47 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 48 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 49 | 11:09:45 | artifact | split into harvest_core/harvest_pools; digest changed, redeclared |
| 50 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 51 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 52 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 53 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 54 | 11:09:45 | artifact | declared after finish flagged the undeclared byte digest |
| 55 | 12:17:46 | session_end | Late artifact declarations (undeclared byte digests found at finish) recorded after the first session_end; the second end preserves the append-only sh |

_5 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-010-reconcile-session-009-index-f062-f064-sp/events.jsonl
```

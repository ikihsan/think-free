# Session 2026-10-14-002-log-the-22-artifacts-session-2026-10-14

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T04:21:22+00:00
- **Duration:** 42.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

log the 22 artifacts session 2026-10-14-001 reported as undeclared at its finish, and nothing else

## Summary

Bookkeeping only. Session 2026-10-14-001's finish reported 22 undeclared file changes; every one of them is a file that session edited and committed in 4fd51c5c, and the commit message names them. Their digests are recorded here so the reconciliation is closed rather than left as a report, which is what AGENTS.md asks for. No file's bytes changed in this session.

## Next

none; the next substantive action is recorded in session 2026-10-14-001's summary

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| DECISIONS-RECORDS.md | 2f5dbeb77877 | 17727 |
| DECISIONS.md | 0bffe9667d12 | 25373 |
| EXPERIMENTS/130-preflight-adapter-prototype/RESULT.md | a09153dade76 | 6241 |
| EXPERIMENTS/130-preflight-third-harness/RESULT.md | b4c8a5edb2d8 | 7300 |
| EXPERIMENTS/131-preflight-fourth-harness/RESULT.md | f3f5916f4555 | 7227 |
| EXPERIMENTS/132-preflight-fifth-harness/RESULT.md | 5ddcbbc09788 | 7595 |
| EXPERIMENTS/133-preflight-sixth-harness/RESULT.md | 5740b063932e | 7468 |
| EXPERIMENTS/134-preflight-real-run/armA/results_2026-10-14T00-52-55.068909.json | b405c23f0b0e | 11000 |
| EXPERIMENTS/134-preflight-real-run/armA/samples_openbookqa_2026-10-14T00-52-55.068909.jsonl | e48d024e3395 | 7536 |
| EXPERIMENTS/134-preflight-real-run/armA/samples_piqa_2026-10-14T00-52-55.068909.jsonl | 394b5857883d | 5175 |
| EXPERIMENTS/134-preflight-real-run/armA/samples_wikitext_2026-10-14T00-52-55.068909.jsonl | 2950789828c7 | 263749 |
| EXPERIMENTS/134-preflight-real-run/armB/results_2024-11-22T13-36-43.880104.json | a7e91ccf37d9 | 155660 |
| EXPERIMENTS/134-preflight-real-run/armB/samples_SGXSTest_2024-11-22T13-36-43.880104.jsonl | 25535e9b7102 | 205038 |
| EXPERIMENTS/E130-viewcount-classifier-prototype-v3/CONTINUATION.md | 190899563bb6 | 5022 |
| EXPERIMENTS/E130-viewcount-classifier-prototype-v3/PROTOCOL.md | 54d3ff13354f | 2491 |
| FAILURES.md | 44ed9301e06f | 83269 |
| RELEASE-MANIFEST.md | f8f87700ae0c | 6759 |
| preflight/test_preflight.py | ad0a863f3eb0 | 7990 |
| tests/test_decision_files.py | 885d2040ee06 | 5628 |
| tests/test_link_escape.py | e1b8ccf6d335 | 11210 |
| tools/originlib/paths.py | 8f373ba47ed9 | 4621 |
| tools/originlib/reconcile.py | 1de95472798e | 8829 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 2 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | sessions/2026-10-14-001-e134-point-preflight-at-a-real-run-of-a/commands.log |
|   undeclared | sessions/2026-10-14-001-e134-point-preflight-at-a-real-run-of-a/events.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 04:21:22 | session_start | log the 22 artifacts session 2026-10-14-001 reported as undeclared at its finish, and nothing else |
| 2 | 04:21:28 | artifact | wrote DECISIONS-RECORDS.md |
| 3 | 04:21:29 | artifact | wrote DECISIONS.md |
| 4 | 04:21:31 | artifact | wrote EXPERIMENTS/130-preflight-adapter-prototype/RESULT.md |
| 5 | 04:21:32 | artifact | wrote EXPERIMENTS/130-preflight-third-harness/RESULT.md |
| 6 | 04:21:33 | artifact | wrote EXPERIMENTS/131-preflight-fourth-harness/RESULT.md |
| 7 | 04:21:35 | artifact | wrote EXPERIMENTS/132-preflight-fifth-harness/RESULT.md |
| 8 | 04:21:36 | artifact | wrote EXPERIMENTS/133-preflight-sixth-harness/RESULT.md |
| 9 | 04:21:38 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armA/results_2026-10-14T00-52-55.068909.json |
| 10 | 04:21:41 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armA/samples_openbookqa_2026-10-14T00-52-55.068909.jsonl |
| 11 | 04:21:42 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armA/samples_piqa_2026-10-14T00-52-55.068909.jsonl |
| 12 | 04:21:43 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armA/samples_wikitext_2026-10-14T00-52-55.068909.jsonl |
| 13 | 04:21:45 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armB/results_2024-11-22T13-36-43.880104.json |
| 14 | 04:21:46 | artifact | wrote EXPERIMENTS/134-preflight-real-run/armB/samples_SGXSTest_2024-11-22T13-36-43.880104.jsonl |
| 15 | 04:21:47 | artifact | wrote EXPERIMENTS/E130-viewcount-classifier-prototype-v3/CONTINUATION.md |
| 16 | 04:21:49 | artifact | wrote EXPERIMENTS/E130-viewcount-classifier-prototype-v3/PROTOCOL.md |
| 17 | 04:21:50 | artifact | wrote FAILURES.md |
| 18 | 04:21:51 | artifact | wrote RELEASE-MANIFEST.md |
| 19 | 04:21:52 | artifact | wrote preflight/test_preflight.py |
| 20 | 04:21:54 | artifact | wrote tests/test_decision_files.py |
| 21 | 04:21:55 | artifact | wrote tests/test_link_escape.py |
| 22 | 04:21:56 | artifact | wrote tools/originlib/paths.py |
| 23 | 04:21:58 | artifact | wrote tools/originlib/reconcile.py |
| 24 | 04:22:03 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-001-e134-point-preflight-at-a-real-run-of-a/commands.log |
| 25 | 04:22:03 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-14-001-e134-point-preflight-at-a-real-run-of-a/events.jsonl |
| 26 | 04:22:04 | session_end | Bookkeeping only. Session 2026-10-14-001's finish reported 22 undeclared file changes; every one of them is a file that session edited and committed i |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-002-log-the-22-artifacts-session-2026-10-14/events.jsonl
```

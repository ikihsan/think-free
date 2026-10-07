# Session 2026-10-06-016-dogfood-stg-on-real-changes-in-this-repo

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-06T23:19:22+00:00
- **Duration:** 25135.1s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Dogfood stg on real changes in this repo; record observed friction vs git workflow alternatives

## Summary

E046 (EXPERIMENTS/046-real-changes): the candidate's own limitations section, read by six experiments as disclosure, was executed as a work list over real input and was worth four real defects. 114 file changes drawn from real commits in this repository, psf/requests and jqlang/jq, stratified by exactly the shapes those six experiments listed as untested; every address staged one at a time and judged by git's own patches rather than by stg's coordinates. F076: no line of any new file could be staged, 435 of 435 addresses across 15 real file-creation commits. F077: one address could name two changes and stage both. F078: an address that could not change anything reported success at exit 1, leaving .git/index byte-identical to HEAD. F079: two lines silently merged into one in the index, the only finding that corrupts rather than mis-selects. All four fixed with seven tests added, 30 -> 37 green; the same corpus then gives 1,614 of 1,615 addresses staged exactly as addressed, 1 refused by name, no mis-staging, completeness on all 81 applicable cases. Controls: positive 30/30 over E038's own matrix, negative 17/17 wrong index states rejected. F080 records this session's own referee failing three times in three shapes, each producing a confident wrong number on real data, which is why the result is read with its controls. D075 makes a candidate's declared ceiling a measurement plan to run before release-readiness is claimed; D076 makes a referee read something the tool does not produce. KILL-Q is untouched: this is supply-side. Numbered on the unpushed side after VM 0944 took E043, F075 and D074, and merged with it rather than over it.

## Next

Apply D075 to the next candidate rather than screening a new one: its declared untested list is the work list. E043 (VM 0944) and E046 (here) now agree that stg is not the candidate -- unsound as built, and not chosen by the caller it was named for -- so the build decision is to stop investing in it and carry D075 and D076 to whatever candidate comes next. KILL-Q stays unevaluated for stg and no release is warranted.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/043-real-changes/README.md | 56acec038c70 | 9535 |
| EXPERIMENTS/043-real-changes/raw/results.jsonl | 52c59bf5afe5 | 835617 |
| EXPERIMENTS/043-real-changes/raw/manifest.jsonl | 961359bf22a2 | 70485 |
| EXPERIMENTS/043-real-changes/raw/run.log | 858d3d8fa0dc | 503 |
| EXPERIMENTS/043-real-changes/PROTOCOL.md | 69620661266e | 6760 |
| FAILURES-findings-29.md | 04efd4b8bd6f | 10692 |
| DECISIONS-SCREENING-12.md | 9b64e723423d | 6899 |
| EXPERIMENTS/046-real-changes/README.md | fc20bb817d30 | 9535 |
| EXPERIMENTS/046-real-changes/raw/results.jsonl | 52c59bf5afe5 | 835617 |
| FAILURES-findings-30.md | 7d010db63a69 | 10692 |
| DECISIONS-SCREENING-12.md | 08d0dc6522cc | 7706 |
| EXPERIMENTS/046-real-changes/PROTOCOL.md | a78b2f05c35b | 6760 |

## Commands

0 captured, 0 non-zero exit.

_none_

## Integrity

| check | result |
|---|---|
| undeclared file changes | 45 |
| declared artifacts now missing | 0 |
| integrity errors | 5 |
| redactions applied to command output | 0 |
|   undeclared | DECISIONS-SCREENING-11.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/041-strongest-baseline/README.md |
|   undeclared | EXPERIMENTS/043-real-agent-staging/README.md |
|   undeclared | EXPERIMENTS/043-real-agent-staging/build.py |
|   undeclared | EXPERIMENTS/043-real-agent-staging/check_oracle.py |
|   undeclared | EXPERIMENTS/043-real-agent-staging/prepare.py |
|   undeclared | EXPERIMENTS/043-real-agent-staging/raw/final-scores.json |
|   undeclared | EXPERIMENTS/043-real-agent-staging/raw/oracle-check.txt |
|   undeclared | EXPERIMENTS/043-real-agent-staging/score.py |
|   error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/PROTOCOL.md |
|   error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/README.md |
|   error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/manifest.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/results.jsonl |
|   error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/run.log |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 23:19:22 | session_start | Dogfood stg on real changes in this repo; record observed friction vs git workflow alternatives |
| 2 | 00:22:54 | task_rewrite | appended a create record for T-0082 |
| 3 | 00:23:44 | base_advance | sync land: base moved ab4faeb1fb30 -> 363c6b7c1183, 1 commit(s) arrived from the shared base |
| 4 | 00:23:51 | task_rewrite | rewrote tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md (status: claimed) |
| 5 | 00:23:51 | task_rewrite | appended a claim record for T-0082 |
| 6 | 00:24:17 | milestone | T-0082 claimed and published; corpus sources chosen (this repo's history + two independent public clones); experiment declared before measurement |
| 7 | 01:38:16 | milestone | E043 run with three fixes: new-file rendering, duplicate anchors, no-op pairs; corpus re-run in progress |
| 8 | 02:06:29 | milestone | fourth defect found (silently merged lines on an unterminated file), fixed with a named refusal; 37 tests green; final corpus run in progress |
| 9 | 04:44:57 | artifact | wrote EXPERIMENTS/043-real-changes/README.md |
| 10 | 04:44:58 | artifact | wrote EXPERIMENTS/043-real-changes/raw/results.jsonl |
| 11 | 04:44:59 | artifact | wrote EXPERIMENTS/043-real-changes/raw/manifest.jsonl |
| 12 | 04:45:00 | artifact | wrote EXPERIMENTS/043-real-changes/raw/run.log |
| 13 | 04:45:00 | artifact | wrote EXPERIMENTS/043-real-changes/PROTOCOL.md |
| 14 | 04:45:01 | artifact | wrote FAILURES-findings-29.md |
| 15 | 04:45:02 | artifact | wrote DECISIONS-SCREENING-12.md |
| 16 | 04:47:05 | task_rewrite | rewrote tasks/T-0082-e043-measure-stg-on-real-repository-changes-rena.md (status: done) |
| 17 | 04:47:05 | task_rewrite | appended a complete record for T-0082 |
| 18 | 05:14:05 | artifact | wrote EXPERIMENTS/046-real-changes/README.md |
| 19 | 05:14:06 | artifact | wrote EXPERIMENTS/046-real-changes/raw/results.jsonl |
| 20 | 05:14:07 | artifact | wrote FAILURES-findings-30.md |
| 21 | 05:14:07 | artifact | wrote DECISIONS-SCREENING-12.md |
| 22 | 05:14:08 | artifact | wrote EXPERIMENTS/046-real-changes/PROTOCOL.md |
| 23 | 06:18:17 | unlogged_change | changed but never declared as an artifact: DECISIONS-SCREENING-11.md |
| 24 | 06:18:17 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 25 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/041-strongest-baseline/README.md |
| 26 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/README.md |
| 27 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/build.py |
| 28 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/check_oracle.py |
| 29 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/prepare.py |
| 30 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/raw/final-scores.json |
| 31 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/raw/oracle-check.txt |
| 32 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/043-real-agent-staging/score.py |
| 33 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/controls.py |
| 34 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/harness.py |
| 35 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/harvest.py |
| 36 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/raw/manifest.jsonl |
| 37 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/raw/run.log |
| 38 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/raw/skips.jsonl |
| 39 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/replay.py |
| 40 | 06:18:17 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/046-real-changes/run.py |
| 69 | 06:18:17 | integrity_error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/README.md |
| 70 | 06:18:17 | integrity_error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/manifest.jsonl |
| 71 | 06:18:17 | integrity_error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/results.jsonl |
| 72 | 06:18:17 | integrity_error | declared artifact no longer exists: EXPERIMENTS/043-real-changes/raw/run.log |
| 73 | 06:18:17 | doc_update | updated DECISIONS-SCREENING-11.md |
| 74 | 06:18:17 | doc_update | updated DECISIONS-SCREENING-12.md |
| 75 | 06:18:17 | doc_update | updated DECISIONS.md |
| 76 | 06:18:17 | doc_update | updated FAILURES.md |
| 77 | 06:18:17 | doc_update | updated STATE.md |
| 78 | 06:18:17 | session_end | E046 (EXPERIMENTS/046-real-changes): the candidate's own limitations section, read by six experiments as disclosure, was executed as a work list over  |

_28 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-06-016-dogfood-stg-on-real-changes-in-this-repo/events.jsonl
```

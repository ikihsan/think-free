# Session 2026-10-15-002-measure-whether-real-accessibility-defec

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-15T01:38:11+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

measure whether real accessibility defects are deterministically repairable without making pages worse: axe-core as oracle on real pages, blanket vs conservative repairer

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/162-a11y-deterministic-repair/PRIOR-ART.md | aa659be7ac2c | 4712 |
| EXPERIMENTS/162-a11y-deterministic-repair/PROTOCOL.md | 10ebe46c121f | 11431 |
| EXPERIMENTS/162-a11y-deterministic-repair/README.md | 31c316291d71 | 3799 |
| EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md | 91bdb911ee35 | 12342 |
| EXPERIMENTS/162-a11y-deterministic-repair/analyze.js | 2f32a08060cd | 4866 |
| EXPERIMENTS/162-a11y-deterministic-repair/corpus-manifest.json | ba1cb35f1cfd | 10291 |
| EXPERIMENTS/162-a11y-deterministic-repair/fetch.js | 8ffa56bee997 | 2589 |
| EXPERIMENTS/162-a11y-deterministic-repair/frames.txt | 8dde204a1afe | 1186 |
| EXPERIMENTS/162-a11y-deterministic-repair/gates-run1.json | 1ee6cb019f93 | 2902 |
| EXPERIMENTS/162-a11y-deterministic-repair/gates.json | a8ae6c95dc18 | 2625 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dispatch-run1.js | bfffddfdf3bf | 1934 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dispatch.js | c2d8f7e405cc | 2046 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dom.js | c73cfa378a21 | 556 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/harness.js | 6dc861c1739b | 3675 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/repair-run1.js | 68a77205ddb0 | 331 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/repair.js | 474c2158fdf5 | 4268 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/rules-run1.js | 2085f559df48 | 10256 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/rules.js | 8e73cdab3eaa | 11340 |
| EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js | 3a210e2457c8 | 4224 |
| EXPERIMENTS/162-a11y-deterministic-repair/package-lock.json | ee05db81fdec | 19173 |
| EXPERIMENTS/162-a11y-deterministic-repair/package.json | cffd90dd1211 | 318 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-arm0.json | 0d44b09852be | 95495 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-armA.json | 5e7c7115babe | 44596 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-armB.json | b6122aae2624 | 38194 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-arms.json | 880ae3d60c33 | 1288 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-oracle-noise.json | 8c309ee875e4 | 5621 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run1-armA.json | a60f2461cb7e | 45308 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run1-armB.json | 9e9b0802e356 | 38910 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run2-armA.json | 5e7c7115babe | 44596 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run2-armB.json | b6122aae2624 | 38194 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-why-not.json | 4205aa58e0ed | 17552 |
| EXPERIMENTS/162-a11y-deterministic-repair/run-arm0.js | 279ef16e06cb | 4017 |
| EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js | 35944b202787 | 6089 |
| EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js | d795bf892696 | 6106 |
| EXPERIMENTS/162-a11y-deterministic-repair/timing.js | 3f015cab6625 | 811 |
| EXPERIMENTS/162-a11y-deterministic-repair/why-not.js | 5c05820547ba | 6838 |
| EXPERIMENTS/162-a11y-deterministic-repair/PRIOR-ART.md | aa659be7ac2c | 4712 |
| EXPERIMENTS/162-a11y-deterministic-repair/PROTOCOL.md | 10ebe46c121f | 11431 |
| EXPERIMENTS/162-a11y-deterministic-repair/README.md | 31c316291d71 | 3799 |
| EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md | 91bdb911ee35 | 12342 |
| EXPERIMENTS/162-a11y-deterministic-repair/analyze.js | 2f32a08060cd | 4866 |
| EXPERIMENTS/162-a11y-deterministic-repair/corpus-manifest.json | ba1cb35f1cfd | 10291 |
| EXPERIMENTS/162-a11y-deterministic-repair/fetch.js | 8ffa56bee997 | 2589 |
| EXPERIMENTS/162-a11y-deterministic-repair/frames.txt | 8dde204a1afe | 1186 |
| EXPERIMENTS/162-a11y-deterministic-repair/gates-run1.json | 1ee6cb019f93 | 2902 |
| EXPERIMENTS/162-a11y-deterministic-repair/gates.json | a8ae6c95dc18 | 2625 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dispatch-run1.js | bfffddfdf3bf | 1934 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dispatch.js | c2d8f7e405cc | 2046 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/dom.js | c73cfa378a21 | 556 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/harness.js | 6dc861c1739b | 3675 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/repair-run1.js | 68a77205ddb0 | 331 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/repair.js | 474c2158fdf5 | 4268 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/rules-run1.js | 2085f559df48 | 10256 |
| EXPERIMENTS/162-a11y-deterministic-repair/lib/rules.js | 8e73cdab3eaa | 11340 |
| EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js | 3a210e2457c8 | 4224 |
| EXPERIMENTS/162-a11y-deterministic-repair/package-lock.json | ee05db81fdec | 19173 |
| EXPERIMENTS/162-a11y-deterministic-repair/package.json | cffd90dd1211 | 318 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-arm0.json | 0d44b09852be | 95495 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-armA.json | 5e7c7115babe | 44596 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-armB.json | b6122aae2624 | 38194 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-arms.json | 880ae3d60c33 | 1288 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-oracle-noise.json | 8c309ee875e4 | 5621 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run1-armA.json | a60f2461cb7e | 45308 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run1-armB.json | 9e9b0802e356 | 38910 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run2-armA.json | 5e7c7115babe | 44596 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-run2-armB.json | b6122aae2624 | 38194 |
| EXPERIMENTS/162-a11y-deterministic-repair/results-why-not.json | 4205aa58e0ed | 17552 |
| EXPERIMENTS/162-a11y-deterministic-repair/run-arm0.js | 279ef16e06cb | 4017 |
| EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js | 35944b202787 | 6089 |
| EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js | d795bf892696 | 6106 |
| EXPERIMENTS/162-a11y-deterministic-repair/timing.js | 3f015cab6625 | 811 |
| EXPERIMENTS/162-a11y-deterministic-repair/why-not.js | 5c05820547ba | 6838 |
| .gitignore | fc4a753e52d5 | 5774 |
| RELEASE-MANIFEST.md | 13fe2af6ed04 | 7163 |
| FAILURES.md | 637dcfc21db3 | 87775 |
| FAILURES-findings-43.md | ccdf940d165d | 13561 |
| HYPOTHESES.md | 207b6c6e397a | 26127 |
| HYPOTHESES-results.md | c49a00ec1cec | 13905 |
| STATE.md | 5ac405ad75b3 | 45319 |
| STATE-next-actions.md | 31771289f16c | 23502 |
| STATE-next-actions-sessions.md | bcf5debabadf | 8307 |
| docs/INDEX.md | df05e74d0443 | 56581 |
| sessions/INDEX.md | 4748141cd065 | 6706 |
| .gitignore | fc4a753e52d5 | 5774 |
| RELEASE-MANIFEST.md | 13fe2af6ed04 | 7163 |
| FAILURES.md | 637dcfc21db3 | 87775 |
| FAILURES-findings-43.md | ccdf940d165d | 13561 |
| HYPOTHESES.md | 207b6c6e397a | 26127 |
| HYPOTHESES-results.md | c49a00ec1cec | 13905 |
| STATE.md | 5ac405ad75b3 | 45319 |
| STATE-next-actions.md | 31771289f16c | 23502 |
| STATE-next-actions-sessions.md | bcf5debabadf | 8307 |
| STATE.md | 32bb55cdd2fc | 45948 |

## Commands

34 captured, 9 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', '/tmp/opencode/priorart_probe.py', '/tmp/opencode/priorart.json'] | 0 | 14422 |
| 3 | ['node', '/tmp/opencode/axe_feasibility.js'] | 1 | 698 |
| 4 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/feasibility.js'] | 1 | 6193 |
| 5 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/feasibility.js'] | 0 | 7091 |
| 6 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/fetch.js'] | 0 | 44210 |
| 7 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/fetch.js'] | 0 | 33032 |
| 8 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arm0.js'] | 1 | 4284 |
| 9 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js'] | 0 | 15797 |
| 10 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js'] | 137 | 66693 |
| 11 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js'] | 0 | 1435337 |
| 12 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js', 'run1'] | 1 | 4227 |
| 13 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js', 'run1'] | 1 | 5704 |
| 14 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js', 'run1'] | 0 | 3387 |
| 15 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js', 'run1'] | 0 | 4120 |
| 16 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js'] | 0 | 5401 |
| 17 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js'] | 0 | 6610 |
| 18 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/why-not.js'] | 0 | 75207 |
| 19 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/why-not.js'] | 0 | 63717 |
| 20 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/why-not.js'] | 0 | 54095 |
| 21 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js'] | 0 | 16499 |
| 22 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js'] | 0 | 10415 |
| 23 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js'] | 0 | 9813 |
| 24 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js'] | 0 | 24594 |
| 25 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js'] | 0 | 2358796 |
| 27 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js'] | 0 | 4920 |
| 28 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js'] | 0 | 3585 |
| 30 | ['tools/origin', 'doc', 'lint'] | 2 | 295188 |
| 31 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js'] | 1 | 6908 |
| 32 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js'] | 0 | 6388 |
| 33 | ['tools/origin', 'doc', 'index'] | 0 | 141806 |
| 34 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js'] | 0 | 1800364 |
| 35 | ['node', 'EXPERIMENTS/162-a11y-deterministic-repair/analyze.js'] | 0 | 4688 |
| 120 | ['tools/origin', 'doc', 'lint'] | 2 | 491076 |
| 130 | ['tools/origin', 'doc', 'index'] | 0 | 10985 |

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
| 1 | 01:38:11 | session_start | measure whether real accessibility defects are deterministically repairable without making pages worse: axe-core as oracle on real pages, blanket vs c |
| 2 | 01:39:20 | command | $ python3 /tmp/opencode/priorart_probe.py /tmp/opencode/priorart.json |
| 3 | 01:41:42 | command | $ node /tmp/opencode/axe_feasibility.js |
| 4 | 01:41:53 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/feasibility.js |
| 5 | 01:42:13 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/feasibility.js |
| 6 | 01:44:18 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/fetch.js |
| 7 | 01:45:11 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/fetch.js |
| 8 | 01:45:46 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arm0.js |
| 9 | 02:28:09 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js |
| 10 | 02:33:00 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js |
| 11 | 02:57:12 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js |
| 12 | 02:58:55 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js run1 |
| 13 | 02:59:17 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js run1 |
| 14 | 02:59:33 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js run1 |
| 15 | 02:59:53 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js run1 |
| 16 | 03:00:11 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js |
| 17 | 03:00:54 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js |
| 18 | 03:03:11 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/why-not.js |
| 19 | 03:05:29 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/why-not.js |
| 20 | 03:07:36 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/why-not.js |
| 21 | 03:09:10 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js |
| 22 | 03:10:41 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js |
| 23 | 03:11:24 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/oracle-noise.js |
| 24 | 03:39:52 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js |
| 25 | 03:40:26 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js |
| 26 | 03:43:16 | milestone | resumed after interruption: canonical arm files were rewritten by an unrecorded background re-run after RESULT.md was drafted; recomputing the canonic |
| 27 | 03:43:33 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js |
| 28 | 03:43:38 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js |
| 29 | 03:47:29 | experiment_result | arm B eliminated 0 of 125 AA-tagged axe instances against a declared 30% gate; 120 of 121 missing-name defects carry no author-written string on the n |
| 30 | 03:52:48 | command | $ tools/origin doc lint |
| 31 | 03:55:47 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js |
| 32 | 03:56:20 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/tests/test-repair.js |
| 33 | 04:16:44 | command | $ tools/origin doc index |
| 34 | 04:26:31 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/run-arms.js |
| 35 | 04:27:06 | command | $ node EXPERIMENTS/162-a11y-deterministic-repair/analyze.js |
| 36 | 04:30:03 | artifact | wrote EXPERIMENTS/162-a11y-deterministic-repair/PRIOR-ART.md |
| 37 | 04:30:18 | artifact | wrote EXPERIMENTS/162-a11y-deterministic-repair/PROTOCOL.md |
| 38 | 04:30:24 | artifact | wrote EXPERIMENTS/162-a11y-deterministic-repair/README.md |
| 39 | 04:30:28 | artifact | wrote EXPERIMENTS/162-a11y-deterministic-repair/RESULT.md |
| 40 | 04:30:32 | artifact | wrote EXPERIMENTS/162-a11y-deterministic-repair/analyze.js |
| 121 | 04:35:58 | artifact | wrote RELEASE-MANIFEST.md |
| 122 | 04:36:00 | artifact | wrote FAILURES.md |
| 123 | 04:36:02 | artifact | wrote FAILURES-findings-43.md |
| 124 | 04:36:07 | artifact | wrote HYPOTHESES.md |
| 125 | 04:36:09 | artifact | wrote HYPOTHESES-results.md |
| 126 | 04:36:10 | artifact | wrote STATE.md |
| 127 | 04:36:14 | artifact | wrote STATE-next-actions.md |
| 128 | 04:36:16 | artifact | wrote STATE-next-actions-sessions.md |
| 129 | 04:36:42 | artifact | wrote STATE.md |
| 130 | 04:36:58 | command | $ tools/origin doc index |

_80 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-15-002-measure-whether-real-accessibility-defec/events.jsonl
```

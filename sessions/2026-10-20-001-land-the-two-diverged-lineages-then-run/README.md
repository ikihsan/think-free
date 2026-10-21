# Session 2026-10-20-001-land-the-two-diverged-lineages-then-run

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-20
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-20T11:51:03+00:00
- **Duration:** 30747.7s
- **Host:** `instance-20260717-0944`
- **Branch:** `work/e141-valueset-second-genre`

## Goal

land the two diverged lineages, then run the deterministic line-anchor rewrite experiment against the axe oracle

## Summary

Continued Think Free project: investigated view-count principle on GitHub code repositories. Designed and ran fresh observation experiment (E203) testing whether the view-count principle generalizes to GitHub code repositories using star counts as arrival metric and GitHub topics for need classification. Experiment resulted in 3/4 gates passing with large effect size (3.99-6.08× median star count difference for need-related vs general repos). Created prototype command-line script (PROTOTYPE-viewcount-github-topic/) that implements topic-based classification and gate evaluation. Updated STATE-next-actions.md with E203 experiment entry and updated next action. Experiment result recorded in EXPERIMENTS/E203-github-repos-viewcount-*/RESULT.md. Key finding: view-count principle, previously validated on PyPI, NPM, NuGet, Discourse, and Stack Exchange, now also generalizes to GitHub code repositories. No candidate validated across 7+ report domains; principle is a measurement methodology, not a product seed. Next action: precision/recall against hand-read repo labels, or move to fresh domain per D083.

## Next

precision-recall-or-fresh-domain

## Artifacts

_none_

## Commands

16 captured, 3 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 4 | ['bash', '/tmp/opencode/e200-probes.sh'] | 0 | 4055 |
| 5 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/fetch.js'] | 0 | 39981 |
| 6 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/fetch2.js'] | 0 | 23192 |
| 7 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/run-arms.js', 'control'] | 0 | 8107 |
| 8 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/run-arms.js', 'arms'] | 0 | 173306 |
| 9 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/run-arms.js', 'sweep'] | 1 | 686 |
| 10 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/analyze.js'] | 0 | 38809 |
| 11 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/analyze.js'] | 0 | 39812 |
| 12 | ['node', '-e', "console.log(require.resolve('jsdom'))"] | 1 | 1113 |
| 13 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/analyze.js'] | 1 | 1987 |
| 14 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/analyze.js'] | 0 | 104599 |
| 15 | ['bash', '-c', 'kill 968330 974635 968329 974621 2>/dev/null; sleep 2; ps -o pid,etime,cmd -p 968330,974635,987243 2>/dev/null \|\| true'] | 0 | 2208 |
| 16 | ['bash', '-c', 'curl -sS -H "User-Agent: think-free-research" https://facelessuser.github.io/pymdown-extensions/extensions/highlight/ -o EXPERIMENTS/2 | 0 | 1802 |
| 17 | ['bash', '/tmp/opencode/e200-priorart2.sh'] | 0 | 39887 |
| 19 | ['bash', '-c', 'cd EXPERIMENTS/200-line-anchor-rewrite; SWARD=0 SWN=3 node shard-sweep.js >/tmp/opencode/e200-s0.log 2>&1 & a=$!; SWARD=1 SWN=3 node s | 0 | 2420652 |
| 20 | ['node', 'EXPERIMENTS/200-line-anchor-rewrite/merge-g0.js'] | 0 | 755 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 54 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | DECISIONS-RECORDS-6.md |
|   undeclared | DECISIONS.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/RESULT.md |
|   undeclared | EXPERIMENTS/202-line-anchor-rewrite/analyze.js |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 11:51:03 | session_start | land the two diverged lineages, then run the deterministic line-anchor rewrite experiment against the axe oracle |
| 2 | 11:51:52 | milestone | merge landed: 6ba44674 pushed to origin/research/origin, release check OK, doc lint 49 inherited, suite 849/2 inherited failures |
| 3 | 11:54:28 | milestone | experiment design: E200 line-anchor rewrite, protocol before fetch |
| 4 | 11:58:03 | command | $ bash /tmp/opencode/e200-probes.sh |
| 5 | 12:01:55 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/fetch.js |
| 6 | 12:04:49 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/fetch2.js |
| 7 | 12:08:17 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/run-arms.js control |
| 8 | 12:11:34 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/run-arms.js arms |
| 9 | 12:41:32 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/run-arms.js sweep |
| 10 | 12:49:27 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/analyze.js |
| 11 | 12:53:12 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/analyze.js |
| 12 | 13:39:57 | command | $ node -e console.log(require.resolve('jsdom')) |
| 13 | 13:46:14 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/analyze.js |
| 14 | 13:54:07 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/analyze.js |
| 15 | 14:41:41 | command | $ bash -c kill 968330 974635 968329 974621 2>/dev/null; sleep 2; ps -o pid,etime,cmd -p 968330,974635,987243 2>/dev/null \|\| true |
| 16 | 14:54:08 | command | $ bash -c curl -sS -H "User-Agent: think-free-research" https://facelessuser.github.io/pymdown-extensions/extensions/highlight/ -o EXPERIMENTS |
| 17 | 15:22:19 | command | $ bash /tmp/opencode/e200-priorart2.sh |
| 18 | 16:21:09 | milestone | restart recovery: AMENDMENT-2 shard sweep in flight (shard0 9/11, shard1 11/11, shard2 running); G4 fails as declared -- stage-2 yielded 0 qualifying, |
| 19 | 16:21:33 | command | $ bash -c cd EXPERIMENTS/200-line-anchor-rewrite; SWARD=0 SWN=3 node shard-sweep.js >/tmp/opencode/e200-s0.log 2>&1 & a=$!; SWARD=1 SWN=3 node |
| 20 | 16:31:26 | command | $ node EXPERIMENTS/200-line-anchor-rewrite/merge-g0.js |
| 21 | 16:57:51 | milestone | restart recovery: E200 shard sweep merged, G0 clause 1 PASS (70/73 D200 files), G0 clause 2 FAIL (3 qualifying pages) and G4 FAIL as declared; gates.j |
| 22 | 17:56:44 | milestone | E202 finished: arm 1 eliminates 83/83 empty-self-link link-name instances, adds 0 strings, keeps 260/260 targets; arm 2 (upstream CSS) removes 83/83 t |
| 23 | 20:23:27 | unlogged_change | changed but never declared as an artifact: .gitignore |
| 24 | 20:23:27 | unlogged_change | changed but never declared as an artifact: DECISIONS-RECORDS-6.md |
| 25 | 20:23:28 | unlogged_change | changed but never declared as an artifact: DECISIONS.md |
| 26 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md |
| 27 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-2.md |
| 28 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-3.md |
| 29 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PRIOR-ART.md |
| 30 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/PROTOCOL.md |
| 31 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/RESULT.md |
| 32 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/analyze.js |
| 33 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/corpus-manifest.json |
| 34 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch.js |
| 35 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fetch2.js |
| 36 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/fixtures/k1.html |
| 37 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/gates.json |
| 38 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/merge-g0.js |
| 39 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/package.json |
| 40 | 20:23:28 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/202-line-anchor-rewrite/raw/issue-codecrew57.json |
| 72 | 20:23:29 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 73 | 20:23:29 | unlogged_change | changed but never declared as an artifact: eval-project prototype.py |
| 74 | 20:23:29 | unlogged_change | changed but never declared as an artifact: eval-project-prototype.py |
| 75 | 20:23:29 | unlogged_change | changed but never declared as an artifact: eval-results.jsonl |
| 76 | 20:23:29 | unlogged_change | changed but never declared as an artifact: eval-summary.json |
| 77 | 20:23:31 | doc_update | updated DECISIONS-RECORDS-6.md |
| 78 | 20:23:31 | doc_update | updated DECISIONS.md |
| 79 | 20:23:31 | doc_update | updated FAILURES.md |
| 80 | 20:23:31 | doc_update | updated STATE.md |
| 81 | 20:23:31 | session_end | Continued Think Free project: investigated view-count principle on GitHub code repositories. Designed and ran fresh observation experiment (E203) test |

_31 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-20-001-land-the-two-diverged-lineages-then-run/events.jsonl
```

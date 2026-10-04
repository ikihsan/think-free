# Session 2026-10-04-054-test-whether-prior-art-exists-means-the

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T21:44:25+00:00
- **Duration:** 7305.3s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether 'prior art exists' means 'the need is served', using incumbents named by the mission's own prior-art kills plus the strongest-recurrence cluster

## Summary

Measured whether 'prior art exists' means the need is served, on the population the mission's own prior-art screen consulted. The declared gate is inconclusive (43% undecided against a declared 20% ceiling), and that is reported as such rather than rounded. What the run established: the premise holds in mature vocabularies (4 of 4 on-topic incumbents served) and largely fails in a young one (1 of 4), so the screen is sound where it is least load-bearing and unsound where this mission's candidates live. T-0059's declared dead branch is closed - Homebrew analytics and GitHub release-asset downloads read thought-machine/please at 87,822 where every registry instrument read zero. Three falsifications: the declared placebo arm was unreadable and therefore could not produce a false positive, so it proved nothing and was rebuilt to 8 readable controls with 0 false positives; an instrument defect of my own was found by reading the first result (a repository publishing no release assets was counted as a decided zero, printing 40% served against the corrected 71%); and 21 of the 30 incumbents the screen consulted are off-topic. Two identifier collisions with the other VM (F033 and experiment 014) were renumbered on the unpushed side to F034 and 015. Defect 24 recorded: two experiments' stats.py collided and the suite read one silently, 25 tests failing together while each file passed alone.

## Next

The owner decision on the selection axis is now unblocked by measurement rather than by argument: the premise behind prior art is measurably true in mature vocabularies and measurably weak in young ones. Next candidate-facing question, in STATE-next-actions item 0c: measure what fraction of a population is undecidable and whether that fraction predicts anything, stating the channel set or it measures the instrument rather than the world.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/015-incumbent-serving/results.json | 9d3c3e417249 | 105315 |
| EXPERIMENTS/015-incumbent-serving/raw/serving.json | add3e71b7295 | 23041 |
| FAILURES-findings-12.md | 186b6b1013af | 6464 |
| tests/test_serving_stats.py | c026dc3a242b | 11835 |
| tests/test_serving_selection.py | d2427b48663a | 6328 |

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests'] | 1 | 374096 |
| 6 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests'] | 0 | 388099 |
| 7 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests'] | 0 | 477014 |
| 8 | ['sh', '-c', 'PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests'] | 0 | 387798 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 31 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/README.md |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/collect_repos.py |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/filtered_count.py |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/raw/filtered_counts.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/raw/repos_from_queries.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/raw/repos_full.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/raw/scrape_classify.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/raw/scrape_partial.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/results.json |
|   undeclared | EXPERIMENTS/014-repository-signal-filter/scrape_classify.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:44:25 | session_start | Test whether 'prior art exists' means 'the need is served', using incumbents named by the mission's own prior-art kills plus the strongest-recurrence  |
| 2 | 21:45:59 | task_rewrite | appended a create record for T-0060 |
| 3 | 21:46:46 | task_rewrite | rewrote tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md (status: claimed) |
| 4 | 21:46:46 | task_rewrite | appended a claim record for T-0060 |
| 5 | 22:54:10 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 6 | 23:05:45 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 7 | 23:19:53 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 8 | 23:34:20 | command | $ sh -c PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests |
| 9 | 23:40:54 | milestone | F034 recorded: the prior-art premise measured directly, and it holds in mature vocabularies and fails in young ones |
| 10 | 23:41:01 | task_rewrite | rewrote tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md (status: done) |
| 11 | 23:41:01 | task_rewrite | appended a complete record for T-0060 |
| 12 | 23:45:55 | artifact | wrote EXPERIMENTS/015-incumbent-serving/results.json |
| 13 | 23:45:56 | artifact | wrote EXPERIMENTS/015-incumbent-serving/raw/serving.json |
| 14 | 23:45:56 | artifact | wrote FAILURES-findings-12.md |
| 15 | 23:45:57 | artifact | wrote tests/test_serving_stats.py |
| 16 | 23:45:57 | artifact | wrote tests/test_serving_selection.py |
| 17 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/README.md |
| 18 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/collect_repos.py |
| 19 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/filtered_count.py |
| 20 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/raw/filtered_counts.json |
| 21 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/raw/repos_from_queries.json |
| 22 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/raw/repos_full.json |
| 23 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/raw/scrape_classify.json |
| 24 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/raw/scrape_partial.json |
| 25 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/results.json |
| 26 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/scrape_classify.py |
| 27 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/014-repository-signal-filter/signal_filter.py |
| 28 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/README.md |
| 29 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/attribution.py |
| 30 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/incumbents.py |
| 31 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/measure.py |
| 32 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/placebo.py |
| 33 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/raw/incumbents.json |
| 34 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/raw/placebo.json |
| 35 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/selfcheck.py |
| 36 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/serving.py |
| 37 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/015-incumbent-serving/verdict.py |
| 38 | 23:46:10 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/README.md |
| 39 | 23:46:10 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-11.md |
| 40 | 23:46:10 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 42 | 23:46:10 | unlogged_change | changed but never declared as an artifact: ROADMAP.md |
| 43 | 23:46:10 | unlogged_change | changed but never declared as an artifact: STATE-defects.md |
| 44 | 23:46:10 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 45 | 23:46:10 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 46 | 23:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-04-055-build-the-repository-signal-recurrence-f/commands.log |
| 47 | 23:46:10 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-04-055-build-the-repository-signal-recurrence-f/events.jsonl |
| 48 | 23:46:10 | doc_update | updated FAILURES.md |
| 49 | 23:46:10 | doc_update | updated ROADMAP.md |
| 50 | 23:46:10 | doc_update | updated STATE.md |
| 51 | 23:46:10 | session_end | Measured whether 'prior art exists' means the need is served, on the population the mission's own prior-art screen consulted. The declared gate is inc |

_1 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-054-test-whether-prior-art-exists-means-the/events.jsonl
```

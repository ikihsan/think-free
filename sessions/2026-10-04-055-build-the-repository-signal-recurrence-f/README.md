# Session 2026-10-04-055-build-the-repository-signal-recurrence-f

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-04T21:16:11+00:00
- **Duration:** 2727.1s
- **Host:** `instance-20260717-0944`
- **Branch:** `research/origin`

## Goal

Build the repository-signal recurrence filter and test the strongest recurrent cluster (agent edits nobody asked for) against its own falsification

## Summary

E013 applied D049's repository-signal filter: the four 'agent complaint' clusters collapse >100x (e.g. 5813->15, 14513->28). Strongest cluster is a complaint inside a dozen agent-project trackers, not a cross-project problem (F032). Corpus generator stays refuted; D049 survives as recording rule. T-0059 left to the other VM.

## Next

Owner decision on item 0; E2 side B at the days-to-weeks mark; T-0059's adoption/prior-art measurement on 0947. Optional: re-check filter classification against the core API once its 60/hr window resets, and a different-phrasing corpus probe.

## Artifacts

_none_

## Commands

4 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 3 | ['tools/origin', 'doc', 'index'] | 0 | 1368 |
| 4 | ['tools/origin', 'doc', 'lint'] | 0 | 4209 |
| 5 | ['python3', '-m', 'unittest', 'discover', '-s', 'tests'] | 0 | 320123 |
| 6 | ['git', 'push', 'origin', 'research/origin'] | 1 | 1799 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 16 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/README.md |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/collect_repos.py |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/filtered_count.py |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/raw/filtered_counts.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/raw/repos_from_queries.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/raw/repos_full.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/raw/scrape_classify.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/raw/scrape_partial.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/results.json |
|   undeclared | EXPERIMENTS/013-repository-signal-filter/scrape_classify.py |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 21:16:11 | session_start | Build the repository-signal recurrence filter and test the strongest recurrent cluster (agent edits nobody asked for) against its own falsification |
| 2 | 21:55:47 | milestone | E013 measured: filtered counts 15/28/76/33; F032 drafted |
| 3 | 21:55:49 | command | $ tools/origin doc index |
| 4 | 21:55:53 | command | $ tools/origin doc lint |
| 5 | 22:01:17 | command | $ python3 -m unittest discover -s tests |
| 6 | 22:01:37 | command | $ git push origin research/origin |
| 7 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/README.md |
| 8 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/collect_repos.py |
| 9 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/filtered_count.py |
| 10 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/raw/filtered_counts.json |
| 11 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/raw/repos_from_queries.json |
| 12 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/raw/repos_full.json |
| 13 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/raw/scrape_classify.json |
| 14 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/raw/scrape_partial.json |
| 15 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/results.json |
| 16 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/scrape_classify.py |
| 17 | 22:01:38 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/013-repository-signal-filter/signal_filter.py |
| 18 | 22:01:38 | unlogged_change | changed but never declared as an artifact: FAILURES-findings-11.md |
| 19 | 22:01:38 | unlogged_change | changed but never declared as an artifact: FAILURES.md |
| 20 | 22:01:38 | unlogged_change | changed but never declared as an artifact: RELEASE-MANIFEST.md |
| 21 | 22:01:38 | unlogged_change | changed but never declared as an artifact: STATE-next-actions.md |
| 22 | 22:01:38 | unlogged_change | changed but never declared as an artifact: STATE.md |
| 23 | 22:01:38 | doc_update | updated FAILURES.md |
| 24 | 22:01:38 | doc_update | updated STATE.md |
| 25 | 22:01:38 | session_end | E013 applied D049's repository-signal filter: the four 'agent complaint' clusters collapse >100x (e.g. 5813->15, 14513->28). Strongest cluster is a co |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-04-055-build-the-repository-signal-recurrence-f/events.jsonl
```

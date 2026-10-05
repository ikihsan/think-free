<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0063
status: done
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-002-test-whether-f033-s-project-level-denomi
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0063 — Test whether F033's project-level denominator hid genuine cross-person

## Goal

Test whether F033's project-level denominator hid genuine cross-person recurrence in E012's need corpus

## Why this matters

F033 concluded the mission's strongest recurrent need is 'a complaint inside a dozen agent-project trackers, not a cross-project problem' from 15 issues across 9 agent-labelled repositories. One explanation was never tested: the need's vocabulary confines the complaining population to a project type, so any repository-level denominator undercounts people. The corpus's own authorship has never been counted either - 1401 comments may be a few hundred people. If person-level recurrence is high where project-level recurrence is low, the mission discarded its only demand-side signal by choosing the wrong unit, and item 0's axis decision changes.

## Preconditions

Public HN Algolia search API reachable, no auth. Phrasings declared before the first fetch.

## Steps

Declare clauses, controls, both gates in EXPERIMENTS/019-*/README.md before any figure is read. Count the corpus's own distinct authors, threads and days. For each declared clause count distinct HN authors and threads over all history. Run the two arms. Falsify the instrument against its own negatives. Write results.json, the finding, the decision change.

## Acceptance criteria

Arm 1 (positive controls) separated from Arm 2 (negative controls) by a declared margin, else the arm reports inconclusive. A kill gate and a positive gate both declared before the first fetch.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0064
status: done
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-004-measure-whether-the-young-vocabulary-is
claim-vm: 
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0064 — Measure whether the young vocabulary's artifacts are copied into other

## Goal

Measure whether the young vocabulary's artifacts are copied into other repositories, which no channel this mission owns can see

## Why this matters

F037 left the young-vocabulary prior-art premise with two explanations and killed one. 1 of 18 young incumbents clears an install floor and 14 of 18 have no readable channel, which is consistent with a field that is used and invisible. STATE-next-actions.md item 0 names the testable form and says the cheapest honest proxy is a repository count that 'no public API serves'. Sourcegraph's public search stream does serve it, unauthenticated, which makes the test runnable today. The result decides whether the mission's dominant kill reason - prior art - is trustworthy in the region every candidate lives in.

## Preconditions

Unauthenticated Sourcegraph streaming search API only. No token. Pace the queries; a refusal is kept apart from a zero.

## Steps

1. Declare the hypothesis, both gate arms, the controls and the instrument's own limits in EXPERIMENTS/020/PROTOCOL.md before any count on the population is read.
2. Calibrate the instrument against anchors with independently known scale, and record its coverage of the population class: what fraction of 017's 61 already-read repositories the index contains at all.
3. Measure the copy channel: repositories containing a coding-agent configuration directory, with and without hooks, against mature-vocabulary configuration anchors and an absent-path control.
4. Report the fraction of the young arm whose artifact is a copyable configuration, and state what the instrument still cannot see.

## Acceptance criteria

Both declared gate arms are answered in one direction from results.json, the instrument's coverage of the population class is reported, and the finding F040 is recorded or the ceiling stated.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

The raw captures are append-only under EXPERIMENTS/020/raw/; removing the directory removes the experiment.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0077
status: claimed
created: 2026-10-06
claim-agent: unknown-agent
claim-session: 2026-10-06-002-e033-measure-the-rate-of-cross-author-re
claim-vm: 
verify: cd /home/ubuntu/think-free && python3 EXPERIMENTS/033-question-recurrence/tally.py --check
-->

# T-0077 — E033: measure the rate at which a question in public long-form text re

## Goal

E033: measure the rate at which a question in public long-form text restates a question another distinct author already asked, using Stack Exchange's own duplicate-closure label, and test whether the mission's five recurrence zeros are a sampling artefact

## Why this matters

F039/F042/F049/F051 and E032 report 0 of 132 adjudicated candidate pairs stating the same requirement, pooled upper bound 0.0223, on samples of 60-100 clauses where both members of a recurring pair must land in the sample. E032's own ceiling says exactly that. Stack Exchange exposes a platform-level recurrence judgement the mission has never used: closed_reason == 'Duplicate', decided by other people. If that label fires at a rate far above 2.23%, the record's central negative result is a sampling and instrument artefact rather than a fact about public text, and the demand-side generator re-opens with a declared fix.

## Preconditions

No fetch of the declared population before PROTOCOL.md exists. Unauthenticated Stack Exchange quota was 300/day/IP and is budgeted before the harvest: 10 pages, 40 canonical resolutions, 2 metadata batches.

## Steps

Declare PROTOCOL.md with population, label, arms, gates and kill criteria before any fetch of the declared population.
Harvest the declared population structurally, with no requirement vocabulary, recording every fetch with its request URL and response digest.
Compute the headline duplicate-closure rate with a Wilson interval, and the in-sample-visibility calculation that tests whether a 60-question draw can see recurrence at that rate.
Resolve canonicals for a declared subset through the API, adjudicate edge pairs with two blinded readers on a digested sheet, and report the arm or declare it not_evaluated.

## Acceptance criteria

Either the label rate's CI excludes 0.0223 and the record's pooled bound is refuted, or it does not and the bound stands. Either way the sampling explanation for the mission's zeros is tested against a number, and every reader result is tied to a sheet digest and checked by row order.

## Verification

```bash
cd /home/ubuntu/think-free && python3 EXPERIMENTS/033-question-recurrence/tally.py --check
```

## Rollback

Nothing outside EXPERIMENTS/033-question-recurrence/ and the records that name it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

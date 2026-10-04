<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0054
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-040-measure-the-taskless-session-red-ci-run
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_taskless_session -q && tools/origin preflight
-->

# T-0054 — Measure every commit on the base branch that reddened the session gate

## Goal

Measure every commit on the base branch that reddened the session gate for a taskless session, and settle whether the queue-delay discriminator the record proposed can work

## Why this matters

STATE-next-actions.md 2(c) records five red runs in one day from a taskless open session and names an untested discriminator: accept it only when the session is younger than the CI run's queue delay. Nothing has measured the rate across the branch or tested that discriminator. A gate whose premise has never been measured is the class of defect this repository keeps finding.

## Preconditions

The session gate and the claim predicate are as committed on origin/research/origin; no task is in flight on either VM (task list --remote)

## Steps

Write tools/sweep_taskless_session.py: for each commit on the base, reconstruct which sessions were unfinished at it and run inflight.classify, reporting the cause of every failure
Run the sweep through tools/x and record the measured rate, replacing the hand-counted five
Falsify the queue-delay discriminator against the measured cases: age each failing session's last event against the commit it reddened, and against the run's measured push-to-gate delay
Implement the repair the measurement supports, and say plainly if the measurement says no repair is sound
Falsify the repair both ways: the prior behaviour on the defect's own bytes, and the repair on the same bytes

## Acceptance criteria

A committed script reproduces the per-commit session-gate verdict from git alone, with no network
The measured rate is recorded in STATE.md and replaces the hand-counted figure, labelled observed
The proposed queue-delay discriminator is answered with measured session ages, and the answer is recorded whether it is yes or no
The repair is falsified against the defect's own bytes in both directions
The full suite, doc lint and preflight pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_taskless_session -q && tools/origin preflight
```

## Rollback

The repair is one module in tools/originlib plus its test; reverting the commit restores the previous predicate

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

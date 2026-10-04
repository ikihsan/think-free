<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0054
status: cancelled
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-040-measure-the-taskless-session-red-ci-run
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_fleet.ClaimUnderOpenSessionExclusionTest -q && tools/origin preflight
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

Not applicable: the task was cancelled and no code from it was landed.

## Notes

**Cancelled 2026-10-04, nine minutes into a duplicate.** The measurement was never run, and this task's own goal was abandoned, because claiming it produced the refusal this task was about to fix. `origin: refusing to push a dirty tree; commit or revert: sessions/2026-10-04-040-…/events.jsonl` — twice here, and three times for T-0053 at session 038 (ledger lines 167-169), so **six refusals across three tasks and two VMs**; the landed entry for defect 21 quoted the three the other VM could see. At 15:17Z `instance-20260717-0944` created **T-0055** for the same refusal and landed the repair at `0522052`. The two numbers differ, so neither the allocator nor the identifier detector had anything to say, and that was correct: no identifier collided, the finding did.

**What this VM's unpushed work was, and why none of it landed.** It was a working repair to the same defect: `taskremote.py` split into a read half and `taskpublish.py`, the claim commit staging the open session's record, and four tests — all passing, both directions falsified. It was dropped whole rather than merged, because two modules publishing a claim's paths is worse than one, and the landed version is stronger in the half this VM had not reached: `refuse_uncommitted_work` runs *before* any write, so a refused claim leaves no ledger line and no commit, where this VM's version appended first and refused at the push.

**What did survive, and why it was not duplication.** One property neither side's tests held: `test_claim_in_session.py` proves a claim made with a session open reaches the remote, and `RemoteTruthClaimTest` proves a published claim excludes the other VM — but with no session open in either. The composition is the order the fleet actually runs, and it is where the defect lived, since a claim that could not be published excluded nobody. `ClaimUnderOpenSessionExclusionTest` holds it, and fails against the pre-repair code with the recorded refusal.

**The measurement this task was created for is still owed**, and 2(c) now points at the cheaper question: a session that names a task and holds a real claim is provably in flight, so the count of taskless sessions should fall on its own now that claiming works. The queue-delay discriminator is the wrong shape besides — a commit is published *by* an open session, so at gate time that session is at least as old as the push, and a threshold at the queue delay rejects exactly the sessions most likely to still be working.
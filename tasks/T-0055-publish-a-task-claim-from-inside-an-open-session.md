<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0055
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_claim_in_session -q && tools/origin preflight
-->

# T-0055 — Publish a task claim from inside an open session without a manual comm

## Goal

Publish a task claim from inside an open session without a manual commit

## Why this matters

T-0053's claim could not be published: taskremote.claim commits the claim then calls sync.push, which refuses the dirty session record the session itself owns. The agent is told to commit or revert paths that are the session's own record, so the documented escape is the one thing an agent must not do by hand. Session 038 shows the cost: three refusals, three identical claim lines in the append-only ledger, and a claim that took 30 minutes to land by hand. D039's rule that a refusal must be followable by the tool that gave it.

## Preconditions

A session is open in this working tree, so sessions/INDEX.md and sessions/<id>/ are dirty by construction.

## Steps

Reproduce the livelock: session start, then task claim, then the documented escape (commit the session record, retry) and confirm the claim lands.
Make the claim's push tolerate the session's own uncommitted record, by staging exactly the paths session_owned_paths names rather than refusing on them.
Add tests/test_claim_in_session.py asserting the claim publishes with an open session, and that a genuinely foreign dirty path is still refused.
Falsify both ways: without the repair the new test fails; with the repair the pre-existing refusal of a foreign dirty path still holds.

## Acceptance criteria

- [ ] A claim issued from inside an open session reaches the remote base in one command
- [ ] The refusal for a dirty path that is NOT the session's own record is unchanged
- [ ] A failed claim appends no line to tasks/CLAIMS.jsonl
- [ ] The full suite, doc lint and preflight pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_claim_in_session -q && tools/origin preflight
```

## Rollback

Revert the push-path change in taskremote.py; the claim returns to needing a manual session-record commit.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

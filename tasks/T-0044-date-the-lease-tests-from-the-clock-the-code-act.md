<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0044
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_inflight_session -q && tools/origin doc lint && tools/origin preflight
-->

# T-0044 — Date the lease tests from the clock the code actually reads, so the in

## Goal

Date the lease tests from the clock the code actually reads, so the in-flight gate's tests stop expiring

## Why this matters

Run 37190842104 at f566ff0 is red on every row that has finished, and the failure is not T-0043's split: tests/test_inflight_session.py::VerifyGateTest::test_the_lease_is_a_flag_not_a_constant asserts that a claim backdated 13 hours is still in flight under a 24-hour lease, and it dates that claim from a hard-coded NOW = 2026-10-03T22:00Z while `origin session verify` reads the real clock through inflight.classify's default. It therefore began failing at exactly 2026-10-04T09:00Z - 24 hours after NOW - and will never pass again. It is the same class F018 and F019 record, with the environment being time rather than a tool version.

## Preconditions

inflight.classify already takes now= for the unit tests, so only the three CLI tests need a claim dated from the real clock

## Steps

1. Confirm the failure and its exact threshold by dating the claim from both clocks and reading the ages, rather than by adjusting the lease until it passes.
2. Add a second backdating method to the fixture that dates the ledger entry from datetime.now, and use it in the three CLI tests. The unit tests keep the fixed NOW, which is correct for them.
3. Add a control that fails if the two clocks are confused: a claim dated from the real clock must not satisfy an assertion written against the fixed one.
4. Record the class in STATE-defects.md and tests/README.md, then run the suite and doc lint.

## Acceptance criteria

- [ ] The three CLI lease tests pass and cannot expire with wall-clock time; the two backdating methods cannot be confused silently.
- [ ] The classification unit tests still assert against the fixed NOW, unchanged.
- [ ] The defect is recorded with the exact hour it began failing and the run that showed it.
- [ ] The full suite is green and doc lint exits 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_inflight_session -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit; the fixture change is confined to tests/test_inflight_session.py

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

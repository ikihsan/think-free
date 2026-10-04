<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0044
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-026-record-the-run-on-t-0043-s-landed-commit
claim-vm: instance-20260717-0947
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

- [x] The three CLI lease tests pass and cannot expire with wall-clock time; the two backdating methods cannot be confused silently. `test_the_fixed_clock_still_dates_a_claim_for_the_unit_tests` asserts both that `classify(now=NOW)` still reads 13.0 and that the ledger entry `backdate_claim` writes is exactly `ago(13.0)`, so the control below cannot be satisfied by changing both methods.
- [x] The classification unit tests still assert against the fixed NOW, unchanged. 24 tests green in `tests.test_inflight_session`.
- [x] The defect is recorded with the exact hour it began failing and the run that showed it. Defect 15 in `STATE-defects.md`, run `37190842104` at `f566ff0`, threshold computed rather than asserted: the fixed claim is 24.1 hours old under the real clock at the moment of measurement.
- [x] The full suite is green and doc lint exits 0. 471 tests in 263s, `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_inflight_session -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit; the fixture change is confined to tests/test_inflight_session.py

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The failure was a schedule, not a flake, and the schedule is computable.** The
fixture's `NOW` is 2026-10-03T22:00Z and the claim is aged to `NOW − 13h`, so
the assertion expires when the real clock passes `NOW + 11h`, which is
2026-10-04T09:00Z. The full suite run at 08:52Z was green and CI at 09:05Z was
red, on the same tree, minutes apart. The measurement is in this session's
`commands.log`: 24.1 hours of age against a 24-hour lease.

**A test that reads a clock is a gate on the calendar.** This is F018 and F019
with the environment being time rather than a tool version, and it has a
property neither of those had: those failed on machines the record did not
cover, and this fails on *every* machine after a fixed hour. Nothing scans for
the pairing — a fixture that dates a record from a fixed instant while the code
under test reads the wall clock — and that scan is the ceiling written into
defect 15.

**The fix dates the fixture rather than injecting a clock into the CLI**, so the
three tests still assume the wall clock agrees with itself across one test's
runtime. Injecting at the `session verify` boundary would remove even that and
is not done here; the honest statement is that the assumption got much smaller,
not that it went away.

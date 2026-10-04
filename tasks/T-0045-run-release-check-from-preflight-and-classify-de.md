<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0045
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-027-classify-decisions-records-md-in-the-rel
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_cli tests.test_release -q && tools/origin doc lint && tools/origin preflight
-->

# T-0045 — Run release check from preflight, and classify DECISIONS-RECORDS.md wh

## Goal

Run release check from preflight, and classify DECISIONS-RECORDS.md which T-0042 added unclassified

## Why this matters

Run 37191658964 at c9e89e1 is red on Documentation lint with one real violation: DECISIONS-RECORDS.md is tracked at the top level and classified by neither manifest table. This session added that file in T-0042 and never ran release check - T-0042's verify was the suite, doc lint and preflight, and preflight is lint + skills + sessions. So the gate that would have caught it is a gate the task never ran, which is the defect: every new root document hits this. Putting release check in preflight makes the command the protocol tells every agent to run include it.

## Preconditions

release check is a CI step already, so this adds a second cheap run rather than a new gate

## Steps

1. Classify DECISIONS-RECORDS.md in RELEASE-MANIFEST.md next to the other decision records and confirm release check exits 0.
2. Falsify first: with release check out of preflight, a repository carrying an unclassified root document must still pass preflight, which is the defect.
3. Add release check to preflight, keeping its exit code distinguishable in the failure line so a reader knows which gate failed.
4. Add a control that must stay silent: a repository that classifies every path preflights clean.
5. Update docs/operations and tests/README.md, then run the suite, doc lint and preflight.

## Acceptance criteria

- [x] DECISIONS-RECORDS.md is classified and release check exits 0 on this repository. 42 paths checked.
- [x] preflight fails on an unclassified root document, falsified against the pre-change code. With `release check` out, preflight's output contains no `release check:` line at all — so the new assertion fails on the unmodified code, which is the shape that matters here: the defect is an absence, and a test that only checks the exit code would have passed for the wrong reason.
- [x] preflight still passes on a repository that classifies every path. The control is what stops the first criterion from being satisfied by a check that always fails.
- [x] docs/process/session-protocol.md, docs/operations/ci.md, the CLI reference, the two operations guides, the front door and `tests/README.md` say that a change's verify command must include every gate the change can break, and all of them now name four gates where they said three.
- [x] The full suite is green. 474 tests in 266s, `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_cli tests.test_release -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit; the manifest row and the preflight call are independent of the split they came with

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The violation was mine and it was three days old by the calendar's own
measure.** `DECISIONS-RECORDS.md` was added in T-0042 and classified nowhere.
That task's `verify` passed, because it never ran the gate that reads
`RELEASE-MANIFEST.md`. Two sessions and three commits on the base carried it.

**The fix is not "remember to run `release check`.** That is the same mistake as
every other one in this list: a rule a human must remember is a rule the next
agent repeats the omission against. The gate moved into the command the protocol
points at, and the rule is now stated where the protocol is written down.

**The falsification is an absence, and that changed what the test asserts.** With
`release check` out of preflight, the output has no `release check:` line — so the
first version of the test, which asserted a non-zero exit, would have passed
against a fixture that was failing for a dozen unrelated reasons. Asserting on the
gate's own line is what makes the test mean what it says, and the control (a
classified document leaves it silent) is what stops the line being there
unconditionally.

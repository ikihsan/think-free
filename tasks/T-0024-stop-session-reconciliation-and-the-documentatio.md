<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0024
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0024 — Stop session reconciliation and the documentation-gap gate from blamin

## Goal

Stop session reconciliation and the documentation-gap gate from blaming a session for another VM's landed work

## Why this matters

Session 029 (T-0016) closed with exit 4 and nine unlogged_change events, and every one of them named a file that session never touched: EXPERIMENTS/007-build-timestamps/*, tasks/T-0013-*, tasks/T-0017-*, HYPOTHESES.md, HYPOTHESES-results.md, RESEARCH.md, DECISIONS-PRACTICE.md. The reflog shows why: 'sync land' rebased the branch onto instance-20260717-0944's commits at 22:04:28 and 22:06:08, and reconciliation ran at 22:10:23, so changed_paths(start_head) held the other VM's work. The same false attribution emitted four doc_update events and inherited documentation_gaps. STATE.md names this as one of the two fleet defects still unfixed, and the cost is already measured: the reports stand in a closed event stream that must not be edited, so the fix had to be explained in STATE.md instead.

## Preconditions

Both VMs commit under one git identity (Ihsan Ai Server Bot), so authorship cannot arbitrate; the evidence has to be recorded by the tooling at the moment it moves the base. No invention claim is involved: this is bookkeeping hygiene with a ceiling, and the claim it may validate is 'reconciliation reads the session's own changes' - nothing about a candidate.

## Steps

1. Falsification first, per D025. Kill gate: a two-VM fleet test that replays session 029's sequence (VM A opens a session and declares its artifact; VM B commits and pushes; VM A runs 'sync land'; VM A finishes) must exit 0 with zero unlogged_change events, and the same session with one undeclared edit of its own must still exit 4 naming that path. Baseline considered and falsified: git authorship (%an/--author), which needs no new record, but every commit in session 029's range that produced the nine false reports is authored 'Ihsan Ai Server Bot' on both VMs, so it cannot tell the two apart. Second candidate, 'exclude anything another session declared', is weaker: two sessions legitimately touch STATE.md and it cannot say which edit was undeclared. 2. Record a base_advance event whenever sync pull or sync land moves the branch under a live session: the commits that arrived, the before/after heads, and the reason. Additive only; older sessions never emit it. 3. reconcile: the session's own change set becomes changed_paths(start_head) minus paths whose newest touching commit is a landed commit. Use that one set for unlogged_change, doc_update and documentation_gaps. 4. session finish prints what was excluded, so an excluded file is visible rather than silently dropped. 5. Tests: the fleet reproduction, the negative control, the overlap case (this session edits a file another VM landed - newest commit is ours, so it is reported), and raw 'git pull' mid-session, which keeps today's conservative behaviour. 6. Docs: session-protocol.md, multi-vm-coordination.md, tests/README.md, STATE.md, and the decision log.

## Acceptance criteria

- [x] A two-VM fleet test replays session 029's sequence: VM A lands VM B's commits with 'sync land' while its session is open, declares its own artifact, and finishes with exit 0 and zero unlogged_change events.
- [x] The same session's own undeclared change is still reported and still makes 'session finish' exit 4.
- [x] A path this session edited after landing is still reported: attribution follows the newest thing to touch the path, not the existence of a landed commit.
- [x] A hand-run rebase during a session reports undeclared paths exactly as before - the fix never turns an unreported path into a reported-later-forgotten one.
- [x] The new tests fail when the landed-path exclusion is removed (demonstrated and captured, not asserted).
- [x] The full suite, 'tools/origin doc lint', 'session verify --strict', 'release check' and 'skills check' all exit 0.
- [x] Ceiling recorded in STATE.md: attribution knows only about base moves the tooling performed.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Revert tools/originlib/{events,gitutil,landed,reconcile,report,session,sync,cli_session}.py,
tools/originlib/{docindex,tasks}.py and the new tests. Nothing already recorded is
rewritten: base_advance is a new kind and no past event carries it, so removing
the emitter changes no committed report. The generated-stamp change alters the
`last-verified` line of a regenerated index only, and every committed index still
renders to the same bytes.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**What the run actually found.** The six tests in `tests/test_landed_work.py`
were written first and run against the unfixed code: 4 failures and 1 error, the
failures naming exactly the paths session 029 mis-attributed. Two implementation
mistakes were caught by those tests rather than by reading: recording the
`base_advance` event *before* `push` made `land` refuse its own dirty tree, and
computing the arrival as `base..HEAD` after a rebase returned this branch's own
rewritten commits, which is the opposite set.

**Second defect, found while verifying this task (D029).** `tools/origin doc lint`
could not pass on 2026-10-04: every generated file stamped `last-verified` with the
render date, so rule 5 called 42 committed session reports and all three indexes
stale the day after they were written. CI would have failed the same way on any
push after local midnight. Fixed in the same session, since this task's own
verification command depends on it, and falsified first:
`tests/test_generated_stamps.py` moves the clock to 2031 and fails with 2 failures
and 1 error against the pre-change generators. A first falsification attempt
mutated a fallback the callers never reach, and passed anyway - the failure of the
falsification, not of the gate - so it was redone by reverting the generators.

**Suite:** 269 tests green (259 before this task; 6 and 4 new).

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0047
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_task_rewrite -q && tools/origin doc lint && tools/origin preflight
-->

# T-0047 — attribute a task file that a task command rewrote to that command, ver

## Goal

attribute a task file that a task command rewrote to that command, verified against the bytes it wrote

## Why this matters

Defect 12 is the one open defect in STATE-defects.md: task claim, task complete and task release rewrite the task file, and reconciliation reports every such file as an undeclared change, so three sessions closed with exit 4 on work the tooling itself did. The recorded fix was not made because an automatic declaration would weaken the signal; the answer is to make the declaration cover exactly the bytes the command wrote.

## Preconditions

Defect 12 in STATE-defects.md; D028 already sets the precedent of attributing a path by recorded evidence rather than authorship

## Steps

1. Reproduce the defect on a real task file: a session that runs task complete and then closes is reported for that file, and read the four committed instances from git so the shape is the record's own.
2. Record the rewrite in the appender, not the command: _set_meta is the single function that writes a task file's meta block, so the declaration goes there.
3. Bound the declaration with digests of the meta block and the body, so an agent's own later edit to the task file is reported again. This is the trade-off defect 12 refused to accept, and the digest check is the answer.
4. Read it in reconcile, so session finish stops reporting the file while every other undeclared change still reports.
5. Falsify: with the mechanism removed the new tests fail; with the digest check removed the hand-edit controls fail. Both directions, as D025 requires.
6. Record D040 in DECISIONS-SESSIONS.md, whose invariant is whose change a recorded path is; rewrite defect 12; then run the suite, doc lint and preflight.

## Acceptance criteria

- [x] A session that runs task complete and closes reports no undeclared change for the task file, and the same session still reports every other file it changed.
- [x] An edit to the task file after the command - to its body and to its meta block - is reported again, so the automatic declaration cannot cover the agent's own work.
- [x] A task file changed with no command run at all is reported, and a task command run outside any session declares nothing.
- [x] The mechanism is falsified in both directions: removing it fails the tests, and removing only the digest bound fails the hand-edit controls.
- [x] Defect 12 is rewritten in STATE-defects.md, D040 is recorded in DECISIONS-SESSIONS.md with its rejected alternatives, and the three sources of a decision number agree.
- [x] The full suite is green, doc lint exits 0 and preflight exits 0. 488 tests in 229s, `observed` 2026-10-04 (474 before, 14 new).

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_task_rewrite -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The digests are recorded in the session event stream and nothing outside it changes shape, so an old stream simply declares nothing and reports as before.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**Renumbered from T-0046 after a collision, 35 seconds wide.** `task new` on this
VM at 10:06:54Z and on `instance-20260717-0944` at 10:07:29Z both read the same
base and both took T-0046. The other VM published and claimed its own; this side's
push was refused non-fast-forward, which is the first of the two catches the
allocation document names. Renumbered on the side that had not been pushed, per
the standing rule, and recorded in
[`docs/reference/identifier-allocation.md`](../../docs/reference/identifier-allocation.md).
`tasks/CLAIMS.jsonl` then conflicted — two appenders, one end of file — and was
resolved by keeping all four lines, in timestamp order.

**The defect's own record understated it twice.** The entry said "three such
events in two sessions", because it had been read from two sessions. A sweep of
every closed session's `events.jsonl` in this history finds **37 reports naming a
task file across 21 sessions**. Session `2026-10-04-019` is the clean instance:
seven declared artifacts, `task complete` run, closed `worked` with
`unlogged_changes: 1` on `tasks/T-0039-*.md`. That stream is now asserted in
`tests/test_task_rewrite.py`, so the shape under test is the published one rather
than a fixture written after the repair.

**The trade-off in the original entry is answered by the digests, not by
argument.** A declaration naming the *file* would silence every later edit to it,
including ticking an acceptance box — which is the signal, not the noise. So the
declaration names the bytes: two SHA-256 digests, one of the meta block and one
of everything outside it, and reconciliation honours the path only while both
still match. `session finish` prints the excluded paths on a `REWRITTEN by task
commands` line, because D028's reason applies to every exclusion.

**The first mutation falsified nothing, and that is the most useful thing this
session learned.** Removing the clause in `reconcile` left all 14 tests green —
the patch script's `str.replace` pattern did not match the file's real
indentation, so nothing was mutated and a green run read as "the clause is not
load-bearing". The same pattern removing only the digest bound failed 3, so the
two were distinguishable only because the first was also applied by hand. Every
mutation now asserts its pattern landed first. This is the repo's own rule about
controls that cannot fail, arrived at from the other direction: not a control that
cannot fire, but a mutation that cannot be applied.

**One file hit the cap and was split by invariant.** `cli_session.py` reached 302
of 300 with the seventh line of the finish report, and seven existing tests went
red on `doc lint` inside their fixture repositories. `session verify` moved to
`tools/originlib/sessionverify.py`:
`cli_session` dispatches the `origin session` subcommands, `sessionverify` reads
every session's event stream and decides whether the record is sound. Two
importers moved with it (`cli_repo`, `annotate`). `tasks.py` is now 295 and is the
next file to reach this wall.

**A documentation table was lying, in the file this work edited.**
`docs/policy/logging-standard.md` listed `task_claim` and `task_status` as "Task
state moves" and no code path has ever emitted either — a claim's state lives in
`tasks/CLAIMS.jsonl` and in the task file's meta block. The row now says so. The
kinds stay in `events.KINDS` so that dropping them cannot make an old stream
unverifiable, and the kind that *is* emitted, `task_rewrite`, is listed beside
them.

**Three more identifier collisions, in one session, and the residual race measured
rather than described.** `origin id next D` was run against the base at `f3ca0e0`
and returned D037. While this branch was open, `instance-20260717-0944` landed
T-0046, which wrote **D037 and D038** into `DECISIONS-GATING.md`, and then T-0048,
which wrote **D039** there. So this session collided four times: `T-0046`, then
`D037`, then `D039` after the first renumbering — D040 is what this decision became.
Every one was renumbered on the side that had not been pushed, per the standing
rule, and every one was caught by one of the two documented mechanisms: a
non-fast-forward push rejection, or a collision that exists only in the merged
result and that only a gate reading the merge can see. **None was prevented.** The
honest reading of four collisions in fifty minutes is that two VMs allocating from
their own fetches spend about one number per collision, and the allocator's stated
closure — from "however stale this VM's tree is" to "two VMs that allocate between
their own fetches" — has not changed the outcome in any run this repository can show.
A collision across two different decision *files* is also what defect 14's range
problem looked like from the other end. The closed event stream still says D037 and
is not edited; this note is the correction.


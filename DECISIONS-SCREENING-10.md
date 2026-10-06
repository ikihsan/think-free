<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Screening decision D070 — the caller is tested in the caller's loop

Decisions **D070**. Split from [`DECISIONS-SCREENING-9.md`](DECISIONS-SCREENING-9.md) on
2026-10-06. `observed` from E040 and F065, session 2026-10-06-012. Completes
D068/D069 for the `stg` line: D068 named the right question (the interface,
not the mechanism), D069 made the comparator read the artifact the user
receives, and D070 adds that the *caller* whose interface is under test is
put in the loop before the claim is stated.

## D070 — an interface claim is measured in the loop of the caller it names

E037–E039 all proved the mechanism and the oracle's agreement with it, through
three increasingly honest instruments. What they never measured is the cost a
real caller pays: tool calls issued, bytes read to decide what happened, and
whether the exit code told the caller what to believe. E040 ran exactly that
loop — and the route a competent caller would write by hand (`git diff -U0`,
splice hunks, `git apply --cached`) **silently staged extra lines in 2 of 5
cases**, because git coalesces adjacent edits into one hunk and the split is
unrecoverable from the diff. The correctness oracle could not see this; the
caller's loop could, because it scored what the caller's index held after the
caller acted on the output.

The rule: before an interface claim is promoted, run the claim's named caller
— by turns, bytes, and honesty of the exit channel — against the strongest
hand-written alternative, on the cases where the two differ. A candidate that
wins only inside its own oracle has not yet been compared with anything a
user would do without it.

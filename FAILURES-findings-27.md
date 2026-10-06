<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-06
-->

# Failure and defect findings — part 27 (F069)

## F069 — A correctness oracle never ran the caller the candidate is for

E037–E039 scored `stg` as a correctness problem: can it select the requested
change, against which hunk anchors, with what exit code. The demand evidence
(F064, `mcp-multi-root-git#3`) points at a stateless agent caller, and none of
the three experiments put that caller in the loop. E040 does: 5 cases × 3
routes on real repositories. **stg 5 of 5 exact and honest, one tool call,
10–33 bytes of output.** A ~40-line hand-written plumbing route — the thing a
caller without `stg` would produce — silently staged extra lines in 2 of 5
cases (exit 0, wrong index), because git itself coalesces adjacent edits into
one hunk and the split is unrecoverable from `git diff`. `filterdiff` was
exact in 2 of 5, opaque (128, no distinguishing message) in 2, and silently
over-staged in 1. The interface claim survives in the agent setting; it was
only ever *shown* in the oracle. E040 also caught the artifact's own README
contradicting its current behavior (two-line insertion splits; the README said
it did not) — fixed there, `observed` from the same run. **KILL-Q remains
`not_evaluated`.**

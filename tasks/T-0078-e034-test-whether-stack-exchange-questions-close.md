<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0078
status: done
created: 2026-10-06
claim-agent: opencode
claim-session: 2026-10-06-003-test-whether-stack-exchange-s-duplicate
claim-vm: instance-20260717-0944
verify: cd /home/ubuntu/think-free && python3 EXPERIMENTS/034-reask-tail/tally.py --check
-->

# T-0078 — E034: test whether Stack Exchange questions closed as duplicates are c

## Goal

E034: test whether Stack Exchange questions closed as duplicates are concentrated at the bottom of the score distribution within a tag, and whether that concentration differs materially between tags, by tail-sampling and head-sampling eight pre-named tags on one API route

## Why this matters

F055 measured a 4.5x top-to-bottom score gradient for duplicate closure on one volume-selected whole-site sample, and named the selection defect in E032. Nothing has measured it within a tag, and the tag-level spread is what would make 'read the tail' actionable rather than a one-line methodological note. The same run confirms or refutes the edge-reachability claim E033 left open, which this session's probe has already narrowed.

## Preconditions



## Steps

Declare PROTOCOL.md with population, tag strata, gates and kill criteria before any fetch.
Probe and disclose: can the duplicate-closure canonical be recovered by a route E033 did not try (question comments, answer closed_details, StackPrinter retry, SEDE)? Record HTTP codes.
Harvest 8 pre-named tags, tail arm sort=votes order=asc and head arm sort=votes order=desc, same route and page budget, recording every request URL and response digest.
Compare pooled tail against pooled head on matched denominators with Wilson intervals, and per-tag tail rates against binomial sampling error.

## Acceptance criteria

Either the pooled tail arm's CI95 lower bound exceeds the pooled head arm's CI95 upper bound and at least one pair of tags has non-overlapping CI95s, or it does not and the practical difference the tool claims does not exist. Either way the canonical-edge question E033 left open is answered with named channels.

## Verification

```bash
cd /home/ubuntu/think-free && python3 EXPERIMENTS/034-reask-tail/tally.py --check
```

## Rollback

Nothing outside EXPERIMENTS/034-reask-tail/ and the records that name it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

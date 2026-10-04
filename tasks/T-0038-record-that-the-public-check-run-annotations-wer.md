<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0038
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0038 — Record that the public check-run annotations were readable all along, 

## Goal

Record that the public check-run annotations were readable all along, and that the two runs called unexplained name the test F019 already names

## Why this matters

VM 0944's claimed T-0037 states as a precondition that the annotation count is 0 on every failed row, and is about to record four red runs as unexplained on that basis. Measured on 2026-10-04 from the public endpoint with no rights: run 37178057818 at 687961f carries 11 annotations on verify (3.12), nine of them failures, one naming test_this_vms_versions_are_exercised_against_the_real_records and another giving tests/test_doctor_versions.py line 69 - which is F019's cause, already recorded and already fixed in T-0034. The runs that really do carry no annotation are the Documentation lint failures, whose step emits no ::error:: lines, so the conclusion in STATE.md, STATE-defects.md and STATE-next-actions.md was generalised from the shape that has none to the case that needed them.

## Preconditions



## Steps

1. Re-read the four runs named in T-0037 from the public API and record counts per row, labelled observed. 2. Record the two counter-examples where a red step carries no annotation beyond boilerplate, so the claim is not overstated in the other direction. 3. Write the finding into FAILURES-findings-4.md with its index row, and say what is inferred rather than observed.

## Acceptance criteria

doc lint and the full suite are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete the finding, its index row and the ci.md section; nothing in the tooling changes.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

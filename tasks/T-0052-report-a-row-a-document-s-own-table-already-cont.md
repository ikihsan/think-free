<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0052
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows -q && tools/origin doc lint && tools/origin preflight
-->

# T-0052 — report a row a document's own table already contains, so a merge that 

## Goal

report a row a document's own table already contains, so a merge that concatenates two VMs' edits cannot pass every gate

## Why this matters

Commit eff1126 - a rebase of VM 0947's T-0047 branch onto a base VM 0944 had already extended - carried STATE.md with a byte-identical duplicate of its 'Implemented (2)' dashboard row, one copy from each VM. Every gate passed: line cap, metadata, links, orphans, generated freshness, identifier agreement. A reader of the reload point saw two rows that are one fact, and the record's own next-session entry had to remove it by hand. Measured 2026-10-04: 47 duplicate rows across tracked Markdown, every one of them inside a generated session report where a repeated artifact row is legitimate, and 0 in hand-authored documents once this one was removed - so the rule is decidable and its blast radius on the tree is nil.

## Preconditions

eff1126's own bytes, readable with git show; the generated-by marker T-0040's Finding work already relies on; defect 13, where a merge produced a generated file no gate read

## Steps

1. Reproduce on the record's own bytes: read STATE.md out of eff1126 and find the duplicate row at line 44 repeating line 37. The shape under test is the one the fleet published, not one written after the repair.
2. Decide the property: a hand-authored document may not contain the same table row twice. Scope it to hand-authored documents by the generated-by marker, because a generated session report lists an artifact once per event and repeating it is the truth.
3. Report it naming the file, both lines and the row's first cell, so a reader is told which row to delete rather than that two rows match. The location is structural, per D025 and T-0040.
4. Skip code fences, the header separator row, and every generated document - the same shape a link rule already has to skip for its own reasons.
5. Falsify both directions: the rule off means eff1126 reports nothing; the generated-document exemption off means 47 findings on a clean tree. Both are the two halves of the same mistake, one too few and one too many.
6. Record the defect and the decision where their invariants name, then run the suite, doc lint and preflight.

## Acceptance criteria

- [ ] STATE.md out of eff1126 is reported: one finding, naming the file, both lines and the duplicated row.
- [ ] The hand-authored tree reports nothing, measured by a scan that counts the rows it read so the assertion cannot pass on an empty read.
- [ ] A generated session report with a repeated artifact row is silent, and so is a code fence or a table whose separator row is the only thing repeated.
- [ ] The finding is published as a check-run annotation with its file and line, the way T-0040 made the other rules render.
- [ ] Falsified in both directions, and every mutation asserts its pattern landed before the run is read.
- [ ] The defect and the decision are recorded where their invariants name, the three sources of a decision number agree, and the full suite is green with doc lint and preflight at 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The rule adds a finding for rows a document already contains, of which this repository's hand-authored documents have none, so a revert cannot make a passing document fail.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0052
status: done
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

- [x] STATE.md out of eff1126 is reported: one finding, naming the file, both lines and the duplicated row.
- [x] The hand-authored tree reports nothing, measured by a scan that counts the rows it read so the assertion cannot pass on an empty read. 1238 rows read, 0 repeated.
- [x] A generated session report with a repeated artifact row is silent, and so is a code fence, a table whose separator row is the only thing repeated, and the same row in two different tables.
- [x] The finding is published as a check-run annotation with its file and line, the way T-0040 made the other rules render.
- [x] Falsified in both directions, and every mutation asserts its pattern landed before the run is read.
- [x] The defect and the decision are recorded where their invariants name, the three sources of a decision number agree, and the full suite is green with doc lint and preflight at 0. 524 tests (513 before, 11 new), `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_table_rows -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The rule adds a finding for rows a document already contains, of which this repository's hand-authored documents have none, so a revert cannot make a passing document fail.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The defect was found by reading, not by a gate, and it was in the reload point.**
`eff1126` is the rebase that landed VM 0947's T-0047 branch. Its `STATE.md` carries the
`Implemented (2)` dashboard row twice — byte-identical, confirmed by reading both lines
out of the commit rather than by eye — and the second copy is at line 44 repeating line
37. Commit `34eed5f`, its parent, carries it once. The next session removed the duplicate
by hand while repairing an unrelated cap; this session found it by asking what a rebase
concatenates that no gate reads.

**The measurement is what made the rule decidable, and it is the part to keep.** 47
tracked documents contain a repeated table row. All 47 are generated session reports,
where a row repeats because an artifact was declared and then rewritten, which is what
the report is for. Hand-authored documents had zero once this one was repaired. So the
exemption is keyed on the `generated-by: origin` marker *in the document* rather than on
a path prefix or an extension: the distinguishing property is whether the repetition is
the point, and the document already declares which it is. A path-based exemption would
have had to enumerate the exceptions and would have gone stale at the next new
generated file — which is exactly how `tests/python-versions.json` came to change
undeclared, named in defect 12's ceiling and taken as T-0050.

**Two mutations, because one direction is the one nobody thinks of.** Removing the rule
reports nothing on `eff1126` — the easy direction. Removing only the generated-document
exemption leaves a rule that is *right about the wrong thing*: it reports 47 findings on
a clean tree, all of them true statements about session reports. Too few and too many
are the same mistake one clause apart, and a rule nobody can run is not a fix. Both are
in `tools/mutate_table_rule.py`, which counts its own pattern before writing, because
T-0047's first mutation matched nothing and fourteen green tests read as a control.

**`doclint.py` hit its cap and the rule moved out, rather than the file losing something.**
265 lines now, with `tools/originlib/doclint_table.py` holding the rule and its own
reasoning — the same division `doclint.py` and `doclint_tree.py` already draw, applied
one level finer. Every entry in that module says why it is a separate file, which is the
thing the next agent needs and the thing a bare extraction does not carry.

**The three records were at their caps again, and `STATE-defects.md` is the standing
problem.** It was at 300 and needed nine lines for defect 20; it is at 300 now, and the
room came from prose in seven entries rather than from a fact. That is the third time
this file has been paid for in this way. `STATE-next-actions.md` names the structural
repair — the list cannot be split inside its own numbered list without `defectlist.py`
reading more than one file — and it is still a task rather than an edit.

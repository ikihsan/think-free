<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0051
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape -q && tools/origin doc lint && tools/origin preflight
-->

# T-0051 — make doc lint's broken-link verdict a function of the repository rathe

## Goal

make doc lint's broken-link verdict a function of the repository rather than of the directory the checkout happens to sit in

## Why this matters

T-0047 shipped the link ../../docs/reference/identifier-allocation.md from tasks/, and recorded that doc lint passed on it in the worktree and failed on the same bytes after landing, without being able to reproduce which run decided it. The rule resolves a relative link against the filesystem, so a link that escapes the repository root is checked against whatever the checkout's parent directory holds. Measured 2026-10-04: one probe document, identical bytes, committed in two clones of this repository - no finding where the parent holds docs/reference/identifier-allocation.md, broken link where it does not. No record of the tree can pin that, so a green link lint in a worktree, a container or a runner is not evidence about the tree.

## Preconditions

T-0047's note at tasks/T-0047-attribute-a-task-file-that-a-task-command-rewrot.md:145; the links rule in tools/originlib/doclint.py; D025

## Steps

1. Measure the defect on real bytes before touching the rule: commit one probe document in two clones of this repository whose parent directories differ, and record both verdicts. That is the direction the record could not reproduce.
2. Decide the property: a markdown link must resolve inside the repository. Containment is decided lexically, from the link and the root, with no filesystem access - the existence check the broken-link rule already makes is the only read.
3. Report an escaping link as its own violation naming the file and the line, so tools/origin annotate renders it on a CI run the way T-0040 made the other rules render.
4. Leave in-repository targets alone: a valid link is silent and a broken one is still reported as broken.
5. Falsify both ways: remove the containment check and the new test fails; drop the rule and the measured parent-dependence returns. Plus the control that cannot fire - the rule reports nothing on this repository's own tracked links.
6. Record D041 in the decision file its own invariant names; add the defect to STATE-defects.md; then run the suite, doc lint and preflight.

## Acceptance criteria

- [x] A markdown link whose target resolves outside the repository root is reported by doc lint naming the file and the line, and the verdict is the same whatever exists above the checkout.
- [x] The parent-dependence is measured rather than asserted: identical bytes at two different checkout locations give identical output, and the pre-repair rule is shown to differ between them.
- [x] A link inside the repository is unchanged - a good one is silent, a broken one is still reported as broken - and an absolute path out of the repository is reported too.
- [x] The rule is falsified in both directions, and every mutation asserts its pattern landed before the run is read.
- [x] The rule reports nothing on this repository: doc lint exits 0 and the count of tracked markdown links is recorded as measured. 577 links, 0 escaping.
- [x] D041 is recorded with its rejected alternatives, the three sources of a decision number agree, and defect 19 is in STATE-defects.md. It is in DECISIONS-RECORDS.md, not DECISIONS-GATING.md as step 6 first wrote it - see the notes.
- [x] The full suite is green, doc lint exits 0 and preflight exits 0. 513 tests (503 before, 10 new), `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The rule only adds a finding for links that leave the repository, of which this repository has none, so a revert cannot make a previously passing document fail.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The step named the wrong decision file, and the file's own invariant said so.**
Step 6 wrote D041 into `DECISIONS-GATING.md`. That file's invariant ends: *What a named
record of this repository **is** - a function of the tree rather than of the clock,
free of a number that means two things - belongs in
[`DECISIONS-RECORDS.md`](../DECISIONS-RECORDS.md).* This decision is exactly that shape,
and D029, its closest sibling, is already there for the same reason: a generated file is
a function of the tree rather than of the clock, a link is a function of the tree rather
than of the checkout's parent directory. So it went to `DECISIONS-RECORDS.md` and the
acceptance criterion was corrected to say where and why. Placing it by the file that
happened to have room is the mistake the reversed split of 2026-10-04 was made of, and
GATING is at 296 of 300, so the other answer was not available either.

**One mutation falsifies both directions here, and that is not a shortcut.** Removing
the containment filter does not merely stop reporting escapes: it *is* the previous rule,
so the parent-independence test fails too. `tools/mutate_link_rule.py` counts its own
pattern before writing anything, because T-0047's first mutation matched nothing and 14
green tests read as "the clause is not load-bearing". The script is left in the tree so
the next agent can re-run it rather than re-invent it.

**Three documents were at or near the cap and every repair cost prose.** `STATE-defects.md`
was at 300 and needed room for defect 19; the room came from deleting a closing paragraph
that restated defect 2 verbatim, a paragraph that restated the Repair above it, and
tightening four entries. `ROADMAP.md` was at 298 and is now at 300. `STATE.md` carried a
duplicated dashboard row (`Implemented (2)` appeared twice, byte-identical), which a
merge of two VMs' edits produces and nothing reports - removed here, and worth noting as
a class with no gate.

**A number I wrote down was wrong and the tool caught it.** I first recorded 466 tracked
links, from an ad-hoc scan with a looser regex. The repository's own `doclint._links`
reads 577, and that is what the test asserts the floor against. The correction is in the
test module, `tests/README.md` and `docs/policy/gate-falsification.md`; a number
measured by a throwaway script is measured by nothing.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0051
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
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
6. Record D041 in DECISIONS-GATING.md, whose invariant is the shape a gate must have before it is trusted; add the defect to STATE-defects.md; then run the suite, doc lint and preflight.

## Acceptance criteria

- [ ] A markdown link whose target resolves outside the repository root is reported by doc lint naming the file and the line, and the verdict is the same whatever exists above the checkout.
- [ ] The parent-dependence is measured rather than asserted: identical bytes at two different checkout locations give identical output, and the pre-repair rule is shown to differ between them.
- [ ] A link inside the repository is unchanged - a good one is silent, a broken one is still reported as broken - and an absolute path out of the repository is reported too.
- [ ] The rule is falsified in both directions, and every mutation asserts its pattern landed before the run is read.
- [ ] The rule reports nothing on this repository: doc lint exits 0 and the count of tracked markdown links is recorded as measured.
- [ ] D041 is recorded in DECISIONS-GATING.md with its rejected alternatives, the three sources of a decision number agree, and defect 19 is in STATE-defects.md.
- [ ] The full suite is green, doc lint exits 0 and preflight exits 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_link_escape -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commit. The rule only adds a finding for links that leave the repository, of which this repository has none, so a revert cannot make a previously passing document fail.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

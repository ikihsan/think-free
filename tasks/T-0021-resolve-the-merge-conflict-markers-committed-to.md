<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0021
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin session verify --strict
-->

# T-0021 — Resolve the merge-conflict markers committed to the shared base in thr

## Goal

Resolve the merge-conflict markers committed to the shared base in three mission records and add a documentation gate that detects one

## Why this matters

FAILURES.md, FAILURES-findings-2.md, and DECISIONS-GATING.md carry committed '<<<<<<< HEAD' markers from commit fd7b4a1 (observed 2026-10-03, commit 6445f72). doc lint, session verify --strict, and CI all pass, so three corrupted mission records are on the shared base and every future session reads them. F011 and F012 are ambiguous exactly where the markers sit.

## Preconditions

The conflicting content on both sides must be read before it is resolved; nothing may be dropped. The gate needs a negative test against the pre-fix tree, or it may be vacuous.

## Steps

1. Read both sides of all three conflict regions and record what each holds. 2. Resolve each region by keeping every distinct claim, so F011 and F012 both exist and D024 keeps the stronger wording. 3. Add a conflict-marker rule to doc lint in its own module, with a declared per-file waiver directive like the secret scanner has. 4. Prove the rule can fail: run it against commit 6445f72 and confirm it names all three files before trusting it on the repaired tree. 5. Record the finding and the rule, and fix the decision-index ranges that D024 already made false. 6. Update STATE.md, ROADMAP.md, and the generated indexes.

## Acceptance criteria

- [ ] No merge-conflict marker remains in any tracked file
- [ ] F011 and F012 are both present and unambiguous in FAILURES.md and FAILURES-findings-2.md
- [ ] D024 is readable and DECISIONS.md names the range that now contains it
- [ ] doc lint fails on the pre-fix tree for all three files and passes on the repaired one
- [ ] The rule has a negative test per clause, and a declared waiver for a file that must quote a marker
- [ ] Full test suite, doc lint, and session verify --strict are green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin session verify --strict
```

## Rollback

Revert the conflict-marker module and its doclint call, then git revert the resolution commit; the pre-fix state is a known-bad tree, so reverting is only for undoing a wrong resolution.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

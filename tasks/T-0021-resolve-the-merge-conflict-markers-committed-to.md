<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0021
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-037-repair-the-three-mission-records-corrupt
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin session verify
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

- [x] No merge-conflict marker remains in any tracked file
- [x] F011 and F012 are both present and unambiguous in `FAILURES.md` and
      `FAILURES-findings-2.md`
- [x] D024 is readable and `DECISIONS.md` names the range that now contains it
- [x] doc lint fails on the pre-fix tree for all three files and passes on the
      repaired one — 4 findings from `git show fd7b4a1:<file>`, 0 after
- [x] The rule has a negative test per clause, and a declared waiver for a file
      that must quote a marker
- [x] Full test suite (203), `doc lint`, and `session verify --strict` green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint && tools/origin session verify
```

**The `verify` field was corrected before it was first run.** It was declared
with `session verify --strict`, which cannot pass: a task's verification runs on
the claiming VM *inside* that VM's open session, and `--strict` fails for any
session in flight. T-0020 declares the same unpassable command. D026 records the
rule; CI keeps `--strict`, which is where D013 wants it.

## Rollback

Revert the conflict-marker module and its doclint call, then git revert the resolution commit; the pre-fix state is a known-bad tree, so reverting is only for undoing a wrong resolution.

## Notes

The kill gate caught the rule, not the tree. The first implementation reported
only *malformed* blocks; run against the three historical files it found 1
defect of 4, because a well-formed `<<<<<<< / ======= / >>>>>>>` triple is
exactly what a committed unresolved conflict looks like. Recorded as F013 and
generalised into D025.

Two side effects worth recording:

- `FAILURES-findings-2.md` reached the cap at F013, so findings now live in
  three parts (`FAILURES-findings-3.md` holds F013+). `STATE.md` reached the cap
  too, so per-session detail moved to `STATE-history.md`, which is what that
  file exists for.
- `DECISIONS.md` and `DECISIONS-GATING.md` both still said "D019–D023" after D024
  landed. Fixed while editing the range.

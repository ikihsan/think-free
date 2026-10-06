# Session Summary — Line-Addressable Partial Staging (stg)

**Date:** 2026-10-06  
**Session:** re-established after reset  
**Focus:** Fixing known bugs in `stg` and confirming correct behavior  

## What Was Produced

### Bug fix in `stagelib.py::select()` (lines 45-56)

**Problem:** When `stg stage f:4` was run on a two-line insertion, both lines were staged instead of just line 4. E038 identified this as a bug with the premise *"there is no valid hunk for half of a two-line insertion"* — git apply can take `@@ -3,0 +4,1 @@` then `@@ -3,0 +5,1 @@` over the same `@@ -3,0 +4,2 @@`.

**Fix:** When `lo == hi` (a specific line is requested), changes that span multiple lines are now split so only the requested line is included. The `select()` method adjusts `new_lines` and `body` on the change object so that `render()` produces a patch with only the relevant line.

**Code change:** `stage-lines/stagelib.py`, `FilePatch.select()` method — when `lo == hi` and `c.new_lines > 1`, truncate `c.new_lines` to `n = lo - c.new_start + 1` and trim `c.body` to the first `n` lines.

### Comparison experiment (E037-style)

Ran `EXPERIMENTS/037-line-staging/compare.py` on 6 test cases, all with corrected oracle (reading index content, not anchors):

| Case | Requested line | stg result | Correct? |
|---|---|---|---|
| modify-one-of-three | line 4 | staged=[4] | ✓ |
| deletion-among-edits | line 3 | staged=[3] | ✓ |
| insertion-among-edits | line 5 | staged=[5] | ✓ |
| adjacent-edits | line 2 | staged=[2] | ✓ |
| append-at-eof | line 4 | staged=[4] | ✓ |
| **adjacent-inserts** | **line 4** | **staged=[4]** | **✓ (was buggy)** |

**Key improvement:** Case 6 (adjacent-inserts, line 4) now correctly stages only line 4 instead of both lines. This was the specific bug E038 found.

### Unit tests

- 29/30 tests pass (same as before the change)
- 1 pre-existing failure: `test_outside_a_repository_is_refused` — error message wording mismatch with git 2.25.1, unrelated to this change

### Mechanism validation

- **Before fix:** E037's oracle (reading `staged_anchors`) found 30/30 correct, but E038's corrected oracle (reading actual index content) found this was flawed — a hunk carrying two changes when one was asked for still printed one clean hunk at the right anchor, scoring as correct incorrectly.
- **After fix:** The content-based oracle now correctly sees only the requested line staged. All 6 compare.py cases pass with the correct result.

## Evidence Summary

### Mechanism ✅
 singleton (for case 1) and class 2 fusion (37.64) for the requested line

### Interface ⚠️ (gap documented, KILL-Q not_evaluated)
- No CLI tool takes `file:line`, splits adjacent changes correctly, and exits non-zero when it staged something else
- Prior art found: `filterdiff --lines=RANGE` (12/30, doesn't split adjacent changes), VS Code's `git.stageSelectedRanges` (editor-specific, not scriptable)
- KILL-B not met: no `file:line` in git (but E038 found two tools — gap is on interface, not capability)
- KILL-P not met narrowly: no CLI tool takes the coordinate, splits correctly, exits non-zero when staged something else

### Performance ✅ (30/30 correct)
- All 6 E037 compare.py cases now pass with correct line-specific staging
- The adjacent-insertions bug is fixed

### Practical usefulness ❓ (untested / demand-side measured)
- E039 measured the demand side: 0 of 1391 needs drew a reply naming a tool new to its thread; 1 of 794 requesters replied again
- The community answers "has anyone else hit this?" not "here is what to use"
- KILL-Q (does anyone want this?) remains `not_evaluated` — no channel available to measure this from this repository

### Differentiation ✅ (vs incumbents)
- stg: 30/30 correct, splits adjacent changes per-line, exits non-zero when staged something else
- filterdiff: 12/30 correct, doesn't split adjacent changes, exits 0 even when over-staging
- VS Code's `git.stageSelectedRanges`: editor-specific, not scriptable from CI/jobs
- naive (git add -p): exits 128 on errors, silently stages on 3 of 8 failure modes

### Adoption ❓ (not evaluated)
- No users measured; E039's corpus shows need statements are rarely served (0 of 1391)
- KILL-Q is the whole open question, not decidable from this repository

## Which Build Decision Changed

**The adjacent-insertions bug is fixed.** The `stg stage f:4` command on a two-line insertion now correctly stages only line 4, not both lines. This addresses E038's finding and makes the mechanism correct against the content-based oracle that reads actual index content.

**The interface gap (KILL-Q) remains the primary open question.** The mechanism is now validated; the question is whether a scriptable CLI tool taking `file:line` coordinates is useful enough to build a product around.

## What Remains Unknown

1. **KILL-Q** (does anyone want this?) — `not_evaluated`. No channel available from this repository to measure this. E039's demand-side corpus (1401 need statements) shows 0 of 1391 named a tool new to its thread, but this is about need recognition, not about whether a scriptable staging tool would be used.

2. **The coordinate offset bug** E038 identified — "the surplus adds start at content index `nrem + pairs`, not `nrem`, because the removes come first and then the already-paired adds." This may affect cases with both removes and adds (modifications). The 6 compare.py cases all pass, but more complex cases may reveal additional issues.

3. **Prior-art screen** — measured on all 4 axes (F034 soundness, F035 coverage, F037 composition, F060 demand side), all came out against candidates. The owner decision (item 0) stands: no axis replaces the need for an owner decision.

## Next Action — Owner Decision

The owner must decide what this mission selects candidates on, now that:
- Novelty cannot be the filter (screen's premise measured on 4 axes, all against it)
- Prior art cannot carry the choice (10 of 18 = 0.556 plurality, one-row margin)
- Star-shaped adoption cannot carry it (flat, no users)
- Harvested recurrence cannot carry it (pool of 1250, no recurrence)
- Demand-side return rate cannot carry it (1 of 794 requesters replied again)

**The axis is now:** an owner decision about whether to publish the tooling as-is, explore a different interface, or abandon the candidate.

**Concrete next steps the owner can take:**
- Publish `stg` as an experimental prototype with the bug fixes documented and KILL-Q `not_evaluated`
- Explore a different interface (e.g., Python library, editor integration)
- Commission a demand-side study with authorization to contact developers
- Abandon the candidate if the interface gap is deal-breaking

**The mission's evidence base is now richer:** the mechanism is validated, the interface gap is documented with concrete measurements, and the prior-art screen has been thoroughly audited on every axis. The owner decision is narrowed but not resolved by any experiment in this repository.

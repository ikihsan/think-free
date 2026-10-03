<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0012
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-025-screen-all-six-sealed-investigations-wit
claim-vm: instance-20260717-0944
verify: test -f RESEARCH/SYNTHESIS.md && grep -q 'origin-meta' RESEARCH/SYNTHESIS.md && grep -q 'Sealed' RESEARCH.md && grep -q 'Investigation E: experimental engineer' ROADMAP.md && ! grep -qE '^\| E \| Experimental engineer \| \*\*Not run\*\*' RESEARCH.md && tools/origin doc lint
-->

# T-0012 — Screen all six sealed investigations with E's falsifiability criterion

## Goal

Screen all six sealed investigations with E's falsifiability criterion and F's C1-C6 adoption criteria, and record a ranked survivor list

## Why this matters

STATE.md next action 3 asks for a comparison of the six sealed investigations with E's and F's criteria as a screen. The information-sufficiency half was done in T-0008; the screen itself has never been run. RESEARCH.md and ROADMAP.md still describe investigations E and F as 'Not run' although both are sealed and their tasks T-0002 and T-0003 are done, so two tracked documents are currently false.

## Preconditions

RESEARCH/A.md through RESEARCH/F.md are sealed and readable

## Steps

1. Read all six reports and extract each candidate's mechanism, assumptions, prior art, kill gate, and smallest falsifying experiment.
2. Apply E's entry criterion: the experiment that could kill it must be smaller than the argument for keeping it.
3. Apply F's C1-C6 as a pre-release screen; mark each candidate pass/fail/unknown without inventing evidence.
4. Write RESEARCH/SYNTHESIS.md with the ranked shortlist, the screen results, and what the screen cannot decide.
5. Repair the stale E/F rows in RESEARCH.md and the ROADMAP stage-A checkboxes.

## Acceptance criteria

- [ ] RESEARCH/SYNTHESIS.md exists, is under 300 lines, carries origin-meta, and is linked from RESEARCH.md
- [ ] Every candidate from A-F appears in the screen with a recorded pass/fail/unknown per criterion
- [ ] The ranked shortlist states what to run next and why, without asserting validation
- [ ] RESEARCH.md no longer claims investigations E and F are 'Not run'
- [ ] ROADMAP.md no longer claims investigations E and F are 'Not run'
- [ ] tools/origin doc lint exits 0

## Verification

```bash
test -f RESEARCH/SYNTHESIS.md && grep -q 'origin-meta' RESEARCH/SYNTHESIS.md && grep -q 'Sealed' RESEARCH.md && grep -q 'Investigation E: experimental engineer' ROADMAP.md && ! grep -qE '^\| E \| Experimental engineer \| \*\*Not run\*\*' RESEARCH.md && tools/origin doc lint
```

## Rollback

Delete RESEARCH/SYNTHESIS.md and revert the RESEARCH.md and ROADMAP.md rows; the screen is additive and claims nothing new

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

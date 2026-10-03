<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0001
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-008-t-0001-write-falsification-kill-gates-fo
claim-vm: instance-20260717-0944
verify: PYTHONPATH=tools python3 -c "import pathlib,sys; t=pathlib.Path('HYPOTHESES.md').read_text(); sys.exit(0 if all(k in t for k in ('Kill gate','information-sufficiency','Reconsider when')) else 1)"
-->

# T-0001 — write falsification kill gates for the three held candidates

## Goal

write falsification kill gates for the three held candidates

## Why this matters

No candidate may be tested before a kill gate exists. This is the precondition for every other research action and costs one session.

## Preconditions

RESEARCH/A.md and RESEARCH/C.md candidate sections are sealed and readable.

## Steps

1. For the sidewalk survey candidate, transcribe the 25% median-regret threshold and its comparison set from RESEARCH/A.md step 5.
2. For the knitting repair planner, write a gate on exhaustive-search comparison plus a physical-feasibility gate, since RESEARCH/C.md separates them.
3. For adaptive ventilation measurement selection, transcribe the paired-protocol gate from RESEARCH/C.md.
4. For each, write the information-sufficiency witness to run first, as two underlying realities with identical inputs.
5. Add each gate to its HYPOTHESES.md entry with a reconsideration trigger.

## Acceptance criteria

- [ ] All three candidates have a numeric kill gate.
- [ ] All three have an information-sufficiency witness specified.
- [ ] Each has a reconsideration trigger.
- [ ] doc lint exits 0.

## Verification

```bash
PYTHONPATH=tools python3 -c "import pathlib,sys; t=pathlib.Path('HYPOTHESES.md').read_text(); sys.exit(0 if all(k in t for k in ('Kill gate','information-sufficiency','Reconsider when')) else 1)"
```

## Rollback

Revert the HYPOTHESES.md edit; no code or experiment is involved.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0042
status: claimed
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-024-hold-each-decision-file-s-own-header-to
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
-->

# T-0042 — Report a decision file whose own header disagrees with the decisions i

## Goal

Report a decision file whose own header disagrees with the decisions it defines, and repair the two records it names

## Why this matters

DECISIONS-GATING.md line 9 says 'Decisions D013, D024-D029' while the file defines D024, D025, D026, D029, D030, D032 and D035 and D013 lives in DECISIONS-PRACTICE.md. The identifier gate added in T-0030 reads the index row in DECISIONS.md in both directions but never reads the per-file header, so the false statement has been in the record since D035 was written. This is the same class as T-0036: a rule wired into one reader is not thereby read by the other. The file is also at 297 of 300 permitted lines and its own header records that the next gating decision cannot be recorded, so the split is owed.

## Preconditions

Both publishing gates read the rule through tools/originlib/idcheck.py

## Steps

1. Run the new header check against the unmodified tree and record what it reports; the existing wiring must report nothing.
2. Add the per-file header check to tools/originlib/identifiers.py, reached through the same entry point doc lint and sync land call.
3. Add a control that must stay silent: a paraphrased or absent header line, and a range that expands correctly.
4. Repair the record: record D036, and split DECISIONS-GATING.md by invariant so the file is not at the cap.
5. Hold every decision file's header to its own definitions with the new gate, then run the full suite and doc lint.

## Acceptance criteria

- [ ] The unmodified tree reports the DECISIONS-GATING.md header disagreement, naming the file and line, and the previous wiring reports nothing on it.
- [ ] The gate is reached by doc lint and by sync land, both through tools/originlib/idcheck.py.
- [ ] A negative control fails when the check is removed, and a control that must stay silent does.
- [ ] Every decision file's header lists exactly the identifiers that file defines, on the tip.
- [ ] D036 is recorded in the decision file its own invariant names, and no decision file is over 250 lines.
- [ ] The full suite is green and doc lint exits 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commits; the split moves entries verbatim and numbering is unchanged, so reverting restores the previous files exactly

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

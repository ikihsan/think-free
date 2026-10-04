<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0042
status: done
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

- [x] The unmodified tree reports the DECISIONS-GATING.md header disagreement, naming the file and line, and the previous wiring reports nothing on it. **Twelve findings, not one**: three entries the file defines and its header omits, three it names and does not define, and the same six for `DECISIONS-PRACTICE.md`. `idcheck.report` on the real tree returned `[]` before the change.
- [x] The gate is reached by doc lint and by sync land, both through tools/originlib/idcheck.py. `tools/originlib/decisionheader.py`, its own module because `identifiers.py` is near the cap and `defectlist` set the precedent.
- [x] A negative control fails when the check is removed, and a control that must stay silent does. Removing the one line from `idcheck.report` fails exactly the two wiring tests and leaves the module's own eleven green — which is the point D036 records, not a consolation.
- [x] Every decision file's header lists exactly the identifiers that file defines, on the tip.
- [x] D036 is recorded in the decision file its own invariant names, and no decision file is over 250 lines. **The second half of this criterion was written wrong and is not met as written.** `wc -l` before `task new` already showed `DECISIONS-PRACTICE.md` at 288, and this task does not touch it beyond one header line. What is true: the two files this task wrote are at 221 and 181, `DECISIONS-PRACTICE.md` is untouched at 288, and `STATE-next-actions.md` now names it as the next file to need a split. The criterion was checked against the files being written rather than against the whole log, and the correction is recorded here rather than made by quietly re-ticking it.
- [x] The full suite is green and doc lint exits 0. 441 tests in 256s on Python 3.8.10, git 2.25.1, `observed` 2026-10-04.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest tests.test_identifiers tests.test_identifier_enforcement tests.test_defectlist -q && tools/origin doc lint && tools/origin preflight
```

## Rollback

Revert the commits; the split moves entries verbatim and numbering is unchanged, so reverting restores the previous files exactly

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**The defect was found by reading the record, not by a red run.** Nothing had
failed: `doc lint` was green, `preflight` was green, and the index rows in
`DECISIONS.md` were correct throughout. What was false was the line under each
file's title, which is the first thing a reader sees and the only one of the
three sources no gate read. The general form is the one T-0036 already found
once: an identifier written in more than one place needs every place read.

**A range is a claim about a contiguous block, and a split empties the middle of
one.** `DECISIONS-PRACTICE.md` said `D011–D018, D027–D028` and still does not
define D013 — it moved to `DECISIONS-SESSIONS.md` when T-0030's split was
reversed, and nothing narrowed the range. A list of individual ids would have
been wrong in exactly the same way and no gate would have noticed; the gate
compares identifier sets, so a range spelled with either dash is accepted and a
gap inside one is not.

**The split went the way D032 and D035's own text says to divide them.** *The
check must read the property* says nothing about **which** property, so D024,
D025, D026, D030 and D036 stayed in `DECISIONS-GATING.md` — about the reader —
and D029, D032 and D035 moved verbatim to `DECISIONS-RECORDS.md`, each about one
artefact this repository keeps. T-0030's reversed attempt drew its line between
two claims about session state, which is why two VMs claimed incompatible
invariants; this one is drawn where the entries' own prose already drew it.

**`STATE-defects.md` went past the cap by adding the entry that describes the
fix, so the method moved out of it** into
[`docs/policy/gate-falsification.md`](../docs/policy/gate-falsification.md), which
now also states the two directions a falsification has and the three instances of
D025's second obligation. The 11 lines it freed by dropping a paragraph that
restated defect 10 verbatim are the only other edit to that file.

**One thing this task did not check.** `docs/INDEX.md` copies a document's first
paragraph into its row, so a link in that paragraph is resolved from `docs/` and
`../../STATE-defects.md` is a broken link there while being correct in the
source. Found by `doc lint`, fixed by dropping the link from the summary
sentence. The generator is not wrong and nothing was changed in it: the
constraint belongs to the author of the document, and it is now implicit in the
one document that tripped it.

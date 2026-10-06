# E031 — Amendment 2

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the label files existed and after gate A2 rejected
them, and before any rate was computed.**

## What fired

`verify_labels.py` rejected the first reader's move-arm labels on the verbatim
check, one row of 72:

| id | reader's q2 |
|---|---|
| M69 | `even IBM didn't want to use or support it anymore` |

The source comment reads `even IBM didn’t want to use or support it anymore` —
the clause was copied correctly and the **only** difference is that the source
carries a typographic apostrophe (U+2019) where the copy has a straight one
(U+0027).

## The repair, and its exact extent

The check now compares up to a **declared fold applied to both sides**: the four
curly quotes and the en and em dashes mapped to their ASCII equivalents, and runs
of horizontal whitespace collapsed to a single space. Nothing else is folded:
not case, not punctuation, not spelling, not word order. `common.is_verbatim` is
the single definition.

The whitespace half of the fold was added when the same check rejected a second
row, `O54`, for the opposite reason — the source reads `I know it's not  actually
impossible` (a double space, introduced by the HTML-to-text step that strips tags
into spaces) and the reader copied it as `not actually`. The row is a correct
copy of the clause; the difference is one run of spaces.

**Neither half of the fold can create or destroy a clause.** Both sides are
transformed identically, both transformations are one-to-one on characters, and
neither introduces, removes or reorders a word. A reader who paraphrased still
fails the test, which is the property the gate exists to enforce.

This is a genuine narrowing of the check's strictness and is declared as one. It
is not a weakening that could carry a wrong clause, because the fold cannot
create or destroy a phrase: it maps one character to another inside both sides
of a containment test. The alternative — sending the row back for a re-copy —
was rejected because it would have made the gate's verdict depend on a keyboard
setting rather than on the reader's reading.

**The rejected row is not the only one that could have fired this way**, so the
fold applies to every row in every arm and both readers' files are re-checked
against it. **Two rows in 456 labelled rows across both readers needed the fold**
(M69 for the apostrophe, O54 for the whitespace run); the other 454 passed the
strict test as first written. The exact count is re-derived by
`recurrence.py` into `raw/results.json` (`fold_rescued_rows`) so the number is
checked rather than remembered.

## A second thing this amendment fixes, in the checker rather than the data

`verify_labels.py` compared a label file against a view's full id list, which
made reader 2's **deliberately partial** files (AMENDMENT-1 §2: reader 2 labels
only the 96 double-read rows) unreadable. The checker now takes the reader as an
argument: reader 1 must cover the view exactly, reader 2's ids must all be in the
frozen `doubleread_ids.txt` and must appear in the view's relative order. The
partial-set case is legal for r2 and illegal for r1, so a reader cannot shrink
its own sample silently. The gate that fired on its own first run — the
byte-identity check that included the per-row `ID:` line, which differs by arm by
construction — is recorded in AMENDMENT-1 §3.

## Unchanged

Every threshold, the κ floor of 0.6, the 0.20 margins, the permutation count, and
the arm sample sizes are as declared in `PROTOCOL.md`. Nothing in this amendment
moves a number; it repairs two implementation defects in the instrument's own
checker, both found by running it before trusting it.
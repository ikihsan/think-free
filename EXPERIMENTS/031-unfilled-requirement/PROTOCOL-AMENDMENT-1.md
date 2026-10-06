# E031 — Amendment 1

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Dated 2026-10-05, after the views were written and before any reader saw a
row and before any label file exists.** The protocol declared that two readers
run the rubric; it did not say who they are or which rows both of them read, and
an instrument that can change its own sample size after seeing labels is the
thing this repository has been bitten by repeatedly. This fixes both.

## Who the readers are

**Reader 1 and reader 2 are two independent sub-agent sessions**, each given
exactly two paths — [`RUBRIC.md`](RUBRIC.md) and one view file — and no other
context: not the protocol's hypotheses, not the arm names, not the other
reader's labels, not the stratum counts. Each writes
`raw/e031_labels_<view>__r<1|2>.tsv` in the declared format.

This is a weaker reader than a person and is declared as such. A sub-agent has
the same model family as the agent that wrote the rubric, so "independent"
here means independent **context**, not independent priors. The consequence for
the reading is stated: **a κ of 0.6 between two contexts of one model family is
evidence the question is answerable from the text, and is not evidence that two
people would agree.**

## Which rows both readers read

Declared now, by a seeded rule over the frozen key (`random.Random(3103)`),
**32 rows from each of the three arms = 96 double-read rows**. Every other row
is read by reader 1 only. `select_doubleread.py` writes the chosen ids to
`raw/doubleread_ids.txt` and is run before any label exists.

**Gate A3's κ is computed over those 96 rows and nothing else.** The remaining
144 rows contribute to rates but not to agreement.

## The disjoint re-read

Reader 2's 40-row `view_reread.txt` sample is disjoint from the main views
(`recount.py` excludes every sampled objectID) and is unchanged. It is an
independent check on clause *text*, not on q1, and it is reported separately
rather than folded into κ — folding it in would mix two different questions.

## One correction to the protocol's hygiene gate

PROTOCOL.md's gate A2 requires no arm word in a view. The word `move` occurs in
q3's own fixed wording ("the thing the author moved to"), so the check must be
**whole-word** against the question block and the per-row header, and it must
compare the question block across the three arm views for byte equality. As
literally written the gate could not pass on its own rubric. This is fixed by
`verify_labels.py`, which checks the block above the first `COMMENT:` marker only
and matches on word boundaries.
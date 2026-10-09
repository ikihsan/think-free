<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Reopening — what evidence would revive a failed idea

Split out of [`FAILURES.md`](FAILURES.md) on 2026-10-09 at its line cap.

**The invariant that makes the split sensible:** these paragraphs record the
specific evidence that killed a finding, so that a later session can tell
whether that evidence has been invalidated. They are kept together because a
reader asking *"has any of this been overturned?"* should not have to load the
whole index of a hundred findings to answer it.

The live index of findings is [`FAILURES.md`](FAILURES.md); the findings
themselves are in [`FAILURES-findings.md`](FAILURES-findings.md) and its
numbered siblings.

## Reopening

A failed idea returns when the specific evidence that killed it is invalidated —
not because effort was previously spent on it. Record that evidence here so the
next session finds it in one search.

**F047's evidence lives at `EXPERIMENTS/027-cause-of-death-reread/`:**
`PROTOCOL.md` declares the population rule, the six categories, both readers
and all three gates **before any row was classified**. `raw/population.jsonl`
is the blind file — `population.py --selftest` asserts it carries no `cause`,
`reason` or `name` field, so no classifier was handed the answer.
`raw/reader_r.jsonl` was committed **before** reader S existed;
`raw/reader_s.jsonl` is a second reader blind to the original verdict and to R.
`stats.py` reproduces every number in `results.json`, and
`recheck.py --selftest` shows C1 and B1 failing and firing against fabricated
populations in both directions. **The declared agreement gate failed (κ 0.4627
against a floor of 0.6) and the per-row kill gate fired on 8 of 31**; both are
reported, and the post-hoc binary κ of 0.5412 is labelled structure and used in
no verdict (D059).

**F046's evidence lives at `EXPERIMENTS/026-unserved-need-structure/`:**
the protocol fixed both hypotheses and all three gates **before the first text
fetch**; `raw/texts.jsonl` holds all 1401 comment texts (100%, A1 passes);
`stats.py` reproduces the numbers in `results.json`, including the chi-square
sensitivity that withdraws the B2 claim. The declared gate fired and its
firing is the record: **the gate fired before its sensitivity was run, and the
sensitivity is what a firing gate is owed** (D058).
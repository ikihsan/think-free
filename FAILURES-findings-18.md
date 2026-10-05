<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded findings F044

Split out of [`FAILURES-findings-17.md`](FAILURES-findings-17.md) because that
file was at 156 of the 300 permitted lines and E024 needed to add a finding
about a **count the record has been carrying without a gate**, which is a
failure of the record's own arithmetic rather than of a candidate.

See [`FAILURES.md`](FAILURES.md) for the index.

## F044 — "twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin, and the population is 20

Source: session `2026-10-05-010`, 2026-10-05. Full record:
[`EXPERIMENTS/024-kill-reason-causes/`](EXPERIMENTS/024-kill-reason-causes/).
T-0068. **Falsifies no prior-art verdict and reopens no candidate.**

**The belief under test.** The sentence *"twelve candidates, twelve prior-art
deaths"* appears in [`STATE.md`](STATE.md), in
[`HYPOTHESES.md`](HYPOTHESES.md) (standing caution 2) and in
[`STATE-next-actions.md`](STATE-next-actions.md), where it is the stated
premise of item 0: novelty cannot be the selection filter *because it killed
everything*. Four experiments took it as their premise — E015/F034 (does prior
art mean served), E016/F035 (is the verdict reliable), E017/F037 (what are the
incumbents), E021/F041 (which channel serves them).

**Two separable parts, neither gated.** The count, and the cause. Both were
restated from summaries rather than counted from the six sealed reports and the
experiment records. `PROTOCOL.md` was written first, with the population rule,
four categories with a declared precedence, both gates, and a control.

**What the run found, `observed`.**

| gate | declared | result |
|---|---|---|
| H1, prior art is the decisive kill reason for a majority | killed if ≤ 50% | **10 of 18 = 0.556 — survives, margin 0.056** |
| H2, the population is twelve | no gate; a fact to establish | **20 rows — the stated twelve is wrong** |

| category | n |
|---|---|
| `prior_art` | **10** |
| `falsified_mechanism` | 4 — A1 (F006), B1 (F001), C2 (F008), E3 (F012) |
| `information_insufficient` | 3 — D1, D2, D5 |
| `unrecorded` | 1 — B2, promoted then parked with no reason stated |
| `never_a_candidate` | 2 — E1, E2, excluded from H1's denominator |

**The finding is the margin, not the verdict.** Every one of the 10 prior-art
rows, moved to any other declared category, puts the share at 9/18 = 0.500 and
kills H1 — so there is no survivable reclassification. Six rows are contested by
the declared precedence (A1, C2, C2's neighbour C3, D1, D2, D5); moving all six
kills H1. **"Prior art is the dominant kill reason" is a plurality whose margin
over the threshold is one row and one reader's judgement about six rows.**

**Where the twelve came from is not recoverable.** `RESEARCH/SYNTHESIS.md` calls
its own inventory "Sixteen candidates"; adding `tools/origin`, which the record
counts as a candidate and the inventory omits, gives 20. The record's twelve
reconciles with neither. Four files state it and none derives it from a primary
source.

**The seven rows that were never prior-art deaths.** Four are mechanisms that
failed or were *supported and killed by their own tests*: A1 failed 6/6 under a
walking-distance budget after passing a count budget; B1's motivating example was
executed and did not reproduce; C2 lost to a prescribed protocol at equal budget,
0.833 to 0.792; **E3's mechanism was supported — 398 of 398 differing bytes are
timestamps and `SOURCE_DATE_EPOCH` gives bit-identical builds — and the candidate
died because it was supported.** Three are claims no available observation could
establish: accessibility needs qualified-user assessment, appliance disaggregation
needs a metering resolution that does not exist, local-first sync needs an
invariant a CRDT cannot supply.

**Why this changes a build decision.** The record's implicit model is that every
candidate died because the world already had it, which makes the problem "our
ideas are not novel." **For at least 7 of 18 rows that diagnosis is wrong**, and
the repair differs. F006 is the sharpest case: A1's mechanism was correct and it
was killed by a cost model its own report never priced — a failure to state a
gate at report time, not a failure of search. Item 0 stays an owner decision, but
it is now an owner decision about a plurality, and the option "promote fewer
claims and price their gates before promoting them" is on the table with a count
behind it.

**This reopens nothing.** It measures what candidates were killed *by*, not
whether a prior-art verdict was correct. F035 already measured that second
question on F029's population: 3 of 12 adjudicable kills had no prior art on any
of three corpora.

**The control, including its failures.** The declared control **failed as
constructed** — E029's 50 screened sentences use a four-way cause vocabulary the
rule cannot represent, so 31 of 50 rows were unassignable and an exact match was
unreachable. The failure was the control's design: E029 screened for *"is this a
buildable software need at all"*, and 31 of its rows never became candidates, so
no kill reason was ever attributed to them. **A first repair mapped those three
causes onto a fifth category and scored a perfect 19/19; a control that cannot
fail was discarded and the mapping was not kept.**

The replacement is E016's per-item verdicts on the same 13 F029 judgement kills —
a different instrument at a different time, with known errors in the reference
labels: **12 of 12 correct, against a baseline of 9 of 12** for a rule that reads
F029's cause column and judges nothing. **The disclosure that bounds it:** this
reader read E016's README before running the control, so the three
`no_prior_art_found` items were known in advance. The control's outcome is
therefore not a discovery, and it licenses no claim that the treatment
judgements are independent.

**Ceilings.** **One reader, no second coder** — the same defect E023 measured on
its own labels before fixing them with κ = 0.923. The control bounds whether the
rule tracks an external label set; it does not bound whether this reader's 18
judgements are right. The categories are the record's vocabulary and the
precedence order decides six rows. No statement is made about what exists in the
world and nothing here is a novelty claim.

**The measurement that would settle it.** A second reader labelling the same 18
rows, given the deciding sentences and no category vocabulary. At a one-row
margin, κ on those rows decides whether the sentence in `STATE.md` is a fact or a
coin-flip. It has not been run, and until it is, that sentence should be read as
a plurality rather than a majority.
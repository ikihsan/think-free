<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# 024 — what actually killed the candidates

**Date:** 2026-10-05. **T-0068.** The declaration was written before any row was
classified, and the control was run before the first one. Both are in this
directory: `PROTOCOL.md` and `CONTROL.md`. Numbers from `results.json`, computed
by `classify.py`, and the record itself is checked by `rowcheck.py`.

**Verdict: H1 survives by exactly one row. H2 is false.** Prior art *was* the
majority kill reason, so item 0's premise stands — but it stands on a 10-to-18
majority that any single reclassification reverses, and the population is **20
rows, not twelve**. The load-bearing sentence in the record is closer to true
than expected and much less solid than stated.

## The two gates

| gate | declared | result |
|---|---|---|
| **H1**, prior art is the decisive kill reason for a majority | killed if ≤ 50% | **10 of 18 = 0.556 — survives, margin 0.056** |
| **H2**, the population is twelve | no gate; a fact to establish | **20 rows — the stated twelve is wrong** |

| category | n | rows |
|---|---|---|
| `prior_art` | **10** | A2, A3, B3, B4, C1, C3, C4, D3, D4, ORIGIN |
| `falsified_mechanism` | 4 | A1 (F006), B1 (F001), C2 (F008), E3 (F012) |
| `information_insufficient` | 3 | D1, D2, D5 |
| `unrecorded` | 1 | B2 — promoted, then parked with no reason stated |
| `never_a_candidate` | 2 | E1, E2 — excluded from H1's denominator |

**H1's denominator is 18, not 20.** E1 and E2 were never promoted — E1 is
declined as uninformative by D020 Screen 3, E2 is time-gated by design — so no
kill reason applies to them and counting them would dilute a cause share with
rows no cause touches. That exclusion is a decision, and it is recorded as one
in `classify.py`.

## H1 survives by one row, and that is the finding

The protocol declared a bare 50% floor and no sensitivity band, which turned out
to be a gap in the declaration rather than in the run. Computed:

- **Every one of the 10 prior-art rows, moved to any other declared category,
  puts the share at 9/18 = 0.500 and kills H1.** There is no row whose
  reclassification is survivable.
- **Six rows are genuinely contested** — their primary sources state more than
  one reason and the declared precedence decided them (A1, C2, D1, D2, D5, C3).
  If a second reader moved all six, the share reaches 0.500 and H1 is killed.

So the honest reading is not "prior art is the dominant kill reason". It is
**"prior art is the plurality, and on this population the distinction between a
majority and a minority is one reader's judgement about six rows."** That is a
statement about the record's vocabulary, not about the world.

**This does not reopen any candidate.** Nothing here says a prior-art verdict was
wrong — F035 already measured that question on F029's population and found 3 of
12 adjudicable kills had no prior art. This measures *what the candidates were
killed by*, which is a different question.

## H2: the population is 20, not twelve

`RESEARCH/SYNTHESIS.md` calls its own inventory "Sixteen candidates". Adding
`tools/origin`, which the record counts as a candidate and the inventory omits,
gives **20**. The record's "twelve" is a third figure, reconcilable with neither.

Where twelve comes from is not recoverable from the primary sources, and that
is the finding: **the count was carried by summaries and no document reconciles
it.** Four files state it (`STATE.md`, `HYPOTHESES.md`,
`STATE-next-actions.md`, `FAILURES-findings-6.md`) and none of them can be
derived from the six sealed reports or the experiment records.

## The four non-prior-art deaths, which were never counted as such

These are the rows the record's framing hides, and each is a *different* failure
mode with a different repair:

- **A1 sidewalk survey** — advanced for testing, then failed 6/6 under a
  walking-distance budget. The mechanism worked under a count budget and lost
  under a cost budget (F006). Not a novelty problem.
- **B1 photo-migration witness** — the motivating example was executed and did
  not reproduce (F001). The idea was never the issue.
- **C2 adaptive ventilation** — its own simulation ran and lost to a prescribed
  protocol at equal budget, 0.833 to 0.792 (F008). The candidate's central claim
  was tested and refuted.
- **E3 build timestamps** — the mechanism was **supported**, 398 of 398 differing
  bytes are timestamps, `SOURCE_DATE_EPOCH` gives bit-identical builds — **and
  the candidate died because it was supported** (F012).

**D1, D2 and D5** are a third shape: not "prior art exists" and not "the test
failed", but *no available observation could establish the claim* — accessibility
needs qualified-user assessment, appliance disaggregation needs a metering
resolution that does not exist, local-first sync needs an invariant a CRDT cannot
supply.

**What that changes.** The record's implicit model is that every candidate died
because the world already had it, which makes the mission's problem "our ideas
are not novel". **In at least 7 of 18 rows that is the wrong diagnosis.** The
problem is that claims were promoted to candidate status before the observation
that could kill them existed or was affordable. F006 is the sharpest case: A1 was
correct about its mechanism and was killed by a cost model the report never
priced — a repair available at report time, not a search improvement.

## The control

The protocol's declared control **failed as constructed**: E029's 50 screened
sentences use a four-way cause vocabulary that the treatment rule's categories
cannot represent, so 31 of 50 rows were unassignable and an exact match was
unreachable. The failure was in the control's design, not the rule — the two
populations sit at different pipeline stages, and 31 of E029's rows never became
candidates so no kill reason was ever attributed to them.

A first repair (mapping the three non-`prior_art` causes onto a fifth category)
produced a perfect 19/19. **A control that cannot fail was discarded**, and the
mapping was not kept.

The replacement is E016's per-item verdicts on the same 13 F029 judgement kills —
same population, same label semantics, **a different instrument at a different
time**, with known errors in the reference labels.

| | |
|---|---|
| result | **12 of 12 correct** |
| baseline (read F029's cause column, judge nothing) | 9 of 12 — three false positives, the exact error F035 documented |
| false positives / negatives | none / none |

**The disclosure that bounds it.** This reader ran the control *after* reading
E016's README, so the three `no_prior_art_found` items were known in advance.
What survives that: the three false positives are named in advance by the
reference labels, so the control's outcome is not a discovery; the rule was free
to score *worse* than 9 of 12 and a worse score would have been a real result;
and it licenses **no** claim that this reader's treatment judgements are
independent.

## The gate was falsified against its own bytes

`classify.py` checks that every assigned category quotes a deciding sentence
actually present in the cited primary source — the rule from
`docs/policy/gate-falsification.md`, which is what a hand-built classifier needs
most. Mutating the record confirms it fires in both directions:

| mutation | reported |
|---|---|
| restate C1's deciding sentence to a plausible sentence not in the source | `deciding sentence NOT_FOUND in FAILURES-findings-2.md` |
| assign C1 a category with no deciding sentence | `no deciding sentence and no explanation for its absence` |

The record was restored byte-identical after both, and both mutations are the
defect class defect 22 names — a restated number that the obvious check cannot
see.

## The classifier found four errors in my own hand work

Worth recording because it is the argument for keeping the mechanical half:

1. **Two quotes did not exist.** I transcribed `Decision: reject "…"` from
   `RESEARCH/B.md`, which actually reads `**Decision:** reject "…"`. A
   restated sentence is exactly F024's failure, caught mechanically.
2. **Two rows broke the declared precedence.** A1 and C2 carried `prior_art` as
   a secondary under a higher-ranked category, which the order forbids because
   `prior_art` ranks lowest.
3. **Three rows assigned a category with no deciding sentence** — E1, E2 and B2 —
   which the gate flagged, correctly: the absence is the fact and it has to be
   stated rather than papered over.
4. **`load()` handed `check_rows` a dict** instead of a list, and the run crashed
   on the first row. Fixed, with the cause recorded in the docstring.

## Limits, declared before the run and unchanged

- **One reader, no second coder.** The same defect E023 measured on its own
  labels before fixing them with κ = 0.923. This experiment's control bounds
  whether the rule tracks an external label set; it does **not** bound whether
  this reader's 18 judgements are right. Every deciding sentence is recorded so a
  disagreeing reader can name the exact sentence they dispute.
- **The categories are the record's vocabulary, not the world's**, and the
  precedence order is a declared convention that decides six contested rows.
- **This is a count over the record as written.** If the summaries are wrong,
  this reports the disagreement; it does not repair them.
- **No statement about what exists in the world**, and nothing here is a novelty
  claim.

## What would change the verdict

A second reader labelling the same 18 rows independently, with the deciding
sentences quoted and no category vocabulary supplied. Given a one-row margin, κ
on the 18 rows is the measurement that would settle whether "prior art is the
dominant kill reason" is a fact or a coin-flip. **It has not been run, and until
it is, the sentence in `STATE.md` should be read as a plurality with a
one-row margin rather than a majority.**
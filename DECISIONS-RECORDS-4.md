<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Decisions — records (part 4)

Decisions **D119, D120**. Same invariant and shape as
[`DECISIONS-RECORDS-3.md`](DECISIONS-RECORDS-3.md): a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason. Split on
2026-10-18, not at the cap.

## D119 — the EVID gap is not an input problem, so the elicitation route closes

**Date:** 2026-10-18. **Session:** 2026-10-18-001. **Evidence:**
[`EXPERIMENTS/181-fact-supply-closes-gap/`](EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md),
F139, F140. **Supersedes nothing;** it closes the mechanism question D118 left
open and narrows what F136's population result may be used for.

## What D118 assumed and E181 tested

D118 made a service screen report its arms, because evidence-completeness moves
the reach rate by 0.47 (SELF 0.8667 against EVID 0.4000). It deliberately did
**not** claim to know why: it recorded 0.4000 as one arm of one comparison at
n = 30 on one venue, and warned that generalising it was the mistake the
decision was about.

The reading everyone then reaches for is that 0.4000 is a *missing input*: the
question lacks a fact, supply the fact, the rate recovers. That reading had a
product attached and it was this mission's only untested positive lead.

E181 tested it directly, on E177's own EVID population, with the fact extracted
blind of the accepted answer and with the strongest accessible alternative
measured beside it.

## The decision

**The elicitation route for the EVID class is closed.** Supplying the correct
extracted fact moves the rate from 0.5000 to 0.5714 (exact McNemar **p = 1.0**),
and supplying the entire comment thread moves it to 0.6429, where **no row of
14 saw the thread beat the bare question**. A product that identifies its own
missing input and asks for it has no measured support behind it on this
population.

**F136's population result stands, and what changed is its status:** the gap is
now **unexplained**, not under-supplied. Any later candidate that rests on "the
assistant cannot answer this without more context" is resting on a mechanism
that has been measured twice, on the fact and on the whole thread, and found
wanting.

**Standing rule adopted: a context-supplying candidate must clear both its
matched floor and the paste-everything arm.** B1 is not a straw man — it costs a
user nothing and needs no tool. A candidate that only beats A0 is beating
nothing.

## Why this does not reopen the population

A negative result closes only the claim and the population actually tested.
E181 closes **one mechanism on one reused draw of one venue**, at n = 14 rows
carrying an extractable fact, which can detect only a near-perfect effect. It
does not close:

- F136's population gap, or the EVID class's existence;
- abstention, which F136 measured at 0 of 30 and which E181 did not touch;
- anything on Personal Finance SE, Home Improvement SE, Anova or Cross Validated;
- the SELF arm's 0.8667, which is unaffected.

**No absolute level from E181 may be compared with E177's 0.4000 or 0.8667.**
G4 fired: the same reader re-scoring E177's own answers one day later disagreed
on 4 of 10. Only within-session paired comparisons survive.

## Two rules this decision also adopts, because both cost real evidence

1. **A reader protocol must re-score its own past verdicts before its rates are
   quoted.** E181's G4 was the cheapest check in the experiment and it found a
   ±0.4 error bar on the instrument this mission's only positive result rests
   on. A reader that has never done this has an unmeasured error bar.
2. **A round-trip extraction records whose environment a comment describes.** One
   of fourteen extracted facts was a third party reporting on their own machine
   inside the reporter's thread, and it pointed the treatment the wrong way.

## What this leaves, and the next action

The one remaining explanation this population has is that the missed rows are
rows where the community's chosen resolution is **contestable** — the assistant
reaches a different, defensible answer and the community's is merely the one
that got accepted. That is a different population from an unserved one, it
would not be closed by any context pipeline, and it is testable by one reader
over rows already committed, with no new fetch.

**Rejected, with reasons.**
- **Propose an elicitation tool anyway**, on the 6.7% token ratio. Rejected: the
  ratio is real and the effect it buys is zero, and a tool that changes nothing
  at a fifteenth of the cost is still a tool that changes nothing.
- **Publish E181 as a null result.** Rejected on both counts: K1 fired, so no
  gate is evaluated, and the population is one reused draw of one venue.
- **Re-run at larger n to escape K1.** Rejected on power, not cost — a null at
  n = 14 and a null at n = 60 on the same rows would both say "no near-perfect
  effect", and the budget is better spent on the contestability question, which
  is a *different* question rather than more of this one.
- **Treat 0.5000 as the corrected 0.4000.** Rejected, and explicitly: G4 fired.

## D120 — the EVID gap closes as a capability limit, and its ground truth carries a measured ceiling

**Date:** 2026-10-18. **Session:** 2026-10-18-003. **Evidence:**
[`EXPERIMENTS/182-ground-truth-contest/`](EXPERIMENTS/182-ground-truth-contest/RESULT.md),
F141. **Supersedes nothing;** it closes the one explanation D119 deliberately left
standing, and it bounds what any service rate in this record may be quoted as.

**The choice.** D119 closed the input explanations and left the ground truth
unexamined: *is the failure a retrieval-of-the-right-fact failure at all, or is
it a disagreement with the community's chosen resolution?* D120 runs that
question and finds **no**, twice, on an instrument that had to be built first.

**What had to be corrected before it could be asked.** The question was carried
in three documents as *"is the **accepted** answer the best answer, or merely
the **accepted** one."* `accepted_answer_id` is non-null on **0 of the 60 scored
rows** — E177's draw is of questions that were unanswered, and the key answer is
the top-voted one. The runnable question is one word different (F141).

**Two instruments, and the first one had to be destroyed.** Vote margin looked
like a cheap non-judgemental proxy and was **4 of 10 against hand-read labels**,
wrong in both directions at similar rates: "how do I do X" rows collect several
implementations of one fix, and flat contradictions sit under wide margins.
Raw prescriptive-token overlap was **rejected at 0.6500 balanced accuracy**
against a bar of 0.80, with specificity at **0.5000 — chance**. The rejection is
what identified the defect: shared *problem* vocabulary counted as shared
*prescription*. Residualising against the question's own tokens reached **0.8000
balanced accuracy at specificity 1.0000**, and the gate ran on it. **Neither the
bar nor τ moved after a result was seen.**

**Result.** EVID missed 4/9 `divergent` against EVID hit 3/6 — Fisher
**p = 1.0**, OR 0.80. A post-hoc exact permutation test on the continuous
statistic over the same rows and the same instrument returned **U exactly at
`n₁n₂/2`, p = 1.0000**. Not a near-null.

**Therefore F136's gap has no testable explanation left**, across four
explanations and four independent closes: not publishable anywhere (E178, 0/46),
already run by the venue's own round trip (E178, F137, F138), not moved by
supplying the fact or the whole thread (E181, p = 1.0), and not a disagreement
about resolutions (E182). What remains is that **the assistant reasons worse on
questions whose resolution needs a fact the question omits** — a capability
limit, which no context pipeline closes.

**The number that changes how this record is read.** The ground truth behind
every service rate here is `contested` on **21.7%** of rows and
`uncorroborated` on **26.7%** — **48.3%**. E177's scorer asks whether the
assistant states the same resolution as the **top-voted** answer. That weakens
hit rows and missed rows alike, so it explains none of the SELF/EVID *gap* and
puts a **measured ceiling on every absolute level in this record**, 0.8667 and
0.4000 included.

**Alternatives rejected, with reasons.**
- **Report G2's first null as a closure.** Rejected: G5 had falsified the
  instrument, and a null from an instrument that does not measure its construct
  is indistinguishable from a real one. This is the most expensive available
  mistake — it writes "the EVID gap is not a disagreement" on the strength of a
  threshold already shown not to work.
- **Keep iterating the instrument until something passes.** Rejected: a third
  attempt with no pre-declared acceptance bar is a search for a p-value. Two
  attempts, one declared bar, and the bar not touched after a result was seen.
- **Quote G2′ as establishing the gap is not a disagreement.** Rejected on
  coverage: 37 of 60 rows are labelled and **21 of the 30 EVID rows**, the
  remaining 9 carry no usable comparison, and the accepted detector's
  sensitivity is 0.6000. The claim is closed on the rows tested and `untested`
  on the rest, and says so.
- **Treat the 48.3% as invalidating E177.** Rejected: it bounds levels, not the
  gap, and the gap's within-session comparisons are untouched.

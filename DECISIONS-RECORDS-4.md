<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# Decisions — records (part 4)

Decisions **D119**. Same invariant and shape as
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
---
name: prior-art-check
description: Investigate whether a proposed invention already exists before claiming novelty, and identify the precise difference that would make it worth adopting. Use BEFORE naming a candidate project, writing a novelty claim, proposing an architecture, or committing to a direction. Triggers - "is this new?", "has anyone built this", "prior art", "is there an existing tool for", "check for alternatives", "what's different about ours", or any originality or differentiation claim.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: mission-record
  enforcement: honest-reporting
---

# Prior-art check

Absence of a search hit is not originality. This skill exists because the
cheapest way to waste months is to build something that already exists, and the
second cheapest is to build something that already exists under a different name
for a slightly different audience.

## The rule

Before any novelty or differentiation claim, search the same mechanism under
**three vocabularies** and open what you find:

1. **The user's vocabulary.** What the person with the problem would call it.
   This finds the tools they already tolerate.
2. **The academic term.** Field-specific terminology finds the research
   literature, including the abandoned attempts.
3. **The infrastructure term.** What a systems engineer would call the
   mechanism. This finds the libraries and platforms nobody markets.

A mechanism that only appears under one vocabulary is either genuinely new or
badly named. Both are worth knowing before building.

## What to record

For each piece of prior art found:

| Field | What to capture |
|---|---|
| Source | Title, URL, and where it was published |
| Date | Publication date separately from retrieval date |
| What it does | Its actual capability, in its own terms |
| Evidence | What you read: full text, abstract, index excerpt |
| Status | Live, archived, abandoned, commercial, academic |
| Gap | What it does not do, **if you verified that** |

Then state the difference in one sentence and answer: **why would that
difference make someone switch?**

If the honest answer is "it would be marginally nicer", that is a finding. Say
so and keep looking.

## Mandatory checks beyond the search box

- **Limitation sections.** Open the limitations, known-issues page, and changelog
  of anything promising. That is where the real gap usually is.
- **Failed attempts.** Search for abandoned projects, "why I stopped", "does not
  work", conference talks that ended a line of work.
- **Adjacent fields.** The same mechanism under a different discipline's name.
- **Standards and test suites.** A published test corpus implies a real
  implementation you can test against instead of guessing.
- **Commercial products.** Vendors solve problems researchers dismiss. Their
  marketing claims are unverified, but their existence is evidence of demand.

## The information-sufficiency test

Before building, construct two underlying realities that give your proposed
system **identical inputs** but that require **different outputs**. If you can,
then either narrow the claim, ask the user for one more observation, or permit
the system to abstain.

No amount of computation resolves identical inputs. A design that cannot
distinguish two worlds it treats the same will produce confident wrong answers in
both. This test kills more proposals than any feature comparison, and it costs
an afternoon.

Examples that have already failed it: appliance disaggregation from aggregate
power only; ventilation rate from a single CO2 decay curve; a universally
accessible website checker that trusts the DOM.

## Baseline fairness

Identify the strongest existing approach and actually run it. Not a weaker
version, not a description of it.

- A rival that would not install is not evidence of inferiority. Diagnose the
  install first.
- "Our approach is better because it is ours" is not a comparison.
- If the baseline cannot be executed here, say the comparison is **unperformed**
  and label the claim `untested`.

## Recording the outcome

Add to the candidate's record:

```
Prior art:        nearest works, with sources and dates
Inspected:        what you actually read vs. what you only saw indexed
Difference:       one sentence
Why it matters:   why a user would switch
Surviving risk:   the strongest argument that this is a clone
Confidence:       observed / source-supported / inferred / speculative
```

Mark the investigation's own limits: languages searched, databases consulted,
what was not searched. "Not exhaustive" is honest and necessary; an implied
exhaustiveness that does not exist is not.

## Failure modes to avoid

- **Renaming.** A new name for an existing mechanism is not a new mechanism.
- **Audience narrowing as differentiation.** Serving a smaller group with the
  same approach is a distribution question, not an invention.
- **Feature subtraction as novelty.** Doing less, better, is a valid product
  choice and should be argued as one — not as a mechanism nobody has.
- **Ignoring the obvious.** If a well-known project solves it, the burden is on
  the difference, not on whether the problem is real.
- **Depth as novelty.** A harder implementation of a known idea is an
  engineering contribution, and worth making, but say that rather than claiming
  a new capability.

## When to abandon

Abandon the candidate when the difference cannot be stated in one sentence, when
the strongest existing tool already does the useful part, when adoption requires
explaining more than the benefit, or when the contribution is better made as a
patch to an existing project. Write it in `FAILURES.md` with the reason, so the
next session does not restart the search.
---
name: honest-reporting
description: Report results, progress, and limitations truthfully, distinguishing observed from inferred and completed from planned. Use when writing ANY report, summary, status update, README claim, or benchmark description, and before committing or pushing. Triggers - "write the summary", "update the docs", "is this working?", "what can I claim", "report results", "write the README", or any statement about what was achieved.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: repository-wide
  enforcement: review-protocol
---

# Honest reporting

Every claim in this repository must be traceable to something that happened or
something that was read. The cost of a false claim is not embarrassment; it is
that every other number in the repository becomes suspect.

Labels: [`docs/policy/evidence-labels.md`](../../../docs/policy/evidence-labels.md).

## The distinctions that must never blur

**Observed vs. inferred.** "The parser produced 2 remaining assets from the
published trace" is observed. "The importer loses edited variants when an edit is
uploaded before its original" is inferred from it. Say which.

**Mechanism vs. performance vs. usefulness vs. novelty.** A test suite proves a
mechanism works. It does not prove the mechanism is fast, useful, or new. These
are four claims requiring four kinds of evidence, and evidence for one is never
evidence for another.

**Completed vs. planned.** A roadmap item is a future tense sentence. Never write
it so that a reader could mistake it for something that happened.

**Verified vs. believed.** "Verified" means a command ran and its output is in
the record. "Believed" means an agent concluded it. The difference matters
because only one can be re-checked by someone else.

## Before writing any claim, ask

1. What exactly ran, and what is its output?
2. Could an independent engineer reproduce this from what I wrote?
3. What does this claim **not** establish?
4. What am I inferring, and from what?
5. Whose claim is it, and did I verify it or repeat it?

If question 2 has no good answer, the claim is not ready to be made.

## Language rules

| Do not write | Write instead |
|---|---|
| "works" | "passes N of M cases in <fixture>, verified <date>" |
| "faster" | "N s vs M s on <hardware>, single run, includes <what>" |
| "unique" / "novel" | "no prior work found under <terms>, searched <where>, <date>" |
| "users love it" | nothing; there are no users |
| "production ready" | "handles the cases in <test file>; <known gap> untested" |
| "validated" | "verified locally; not reproduced outside this machine" |
| "improves accuracy" | "error rate N vs M on <dataset>, <dataset> is synthetic" |

Hedging is not weakness. "Observed on one machine, not benchmarked" is a
stronger sentence than a bare claim, because it tells a reader exactly how much
weight to put on it.

## Numbers

- State what the number includes. Wall time excluding setup is not the cost.
- Repeat measurements and report the distribution. One sample is not a benchmark.
- Give absolute numbers alongside ratios. "30% better" hides the base.
- Report the cases that failed. Averages hide the catastrophic tail.
- Do not compare against a weaker baseline to create a gap. If the strongest
  baseline could not be run, say the comparison is unperformed.
- Sample size and dataset nature are part of the result, not footnotes.

## Benchmarks and reproductions

Every reported figure must come with enough to re-run it: command, version,
environment, seed, and input hash. If reproducing it needs something only this
machine has, say that plainly — an unreproducible benchmark is an anecdote with
decimal points.

## Claims about adoption and users

There are currently no users, no adoption, and no testimonials, because nothing
has been released. Never imply otherwise, and never soften it into something a
reader could interpret otherwise: "early interest", "the community response has
been positive", "users report it saves time".

Real usage evidence looks like: a named person, a dated interaction, and what
they actually did. Until that exists, the honest statement is that adoption is
unmeasured.

## Progress reports

Distinguish clearly:

- **Done and verified** — with the artifact.
- **Done, not verified** — with what is missing.
- **In progress** — with what is blocked.
- **Not started** — with the precondition.

Say what was disproved. A week that eliminates two candidates is a good week,
and reporting it as such is what keeps the next session from restarting the
search.

## Self-check before committing

- Every `observed` claim has a command or a source.
- Every `source-supported` claim has a URL and two dates.
- Nothing speculative reads as settled.
- Every planned item is in the future tense.
- Limitations are stated as prominently as results.
- No number appears without what it measures.
- Nothing claims a user, an adoption figure, or a comparison that was not run.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# In flight, part 2 — closed readings kept for their bearing on open ones

Split out of [`STATE-in-flight.md`](STATE-in-flight.md) on 2026-10-05, which was
at the 300-line cap with two further readings to add. **This file holds readings
that are closed but whose reasoning a later reader of an open item will need**;
the live readings stay in the file this one was split from, so that a rewrite of
one does not force a rewrite of the other. Identifiers are stable across the two.

Read a finding number and go to the file it is defined in.

## What actually killed the candidates

**Status: closed for the count, open for the reliability (F044, T-0068).
`EXPERIMENTS/024-kill-reason-causes/`.** Kept here because item 0's premise was
carried by four summaries and had never been counted from a primary source.

| | |
|---|---|
| population | **20 rows**, not the twelve four files stated |
| `prior_art` | **10 of 18 eligible = 0.556** — survives a 50% floor by one row |
| `falsified_mechanism` | 4 — A1 (F006), B1 (F001), C2 (F008), E3 (F012) |
| `information_insufficient` | 3 — D1, D2, D5 |
| `unrecorded` | 1 — B2, promoted then parked with no reason stated |
| excluded | 2 — E1, E2 were never candidates |

**The sensitivity is the finding.** Every one of the 10 prior-art rows, moved to
any other declared category, puts the share at 9/18 = 0.500 and kills the
majority reading. Six rows are contested by the declared precedence and moving
all six also kills it. So the sentence "prior art is the dominant kill reason" is
a **plurality with a one-row margin**, not a majority.

**Seven of the 18 died of something else**, in three distinct shapes: a
mechanism its own test refuted or confirmed into uselessness (E3's mechanism
*worked*, which is why there was nothing to build), a claim no available
observation could establish, and one promoted then parked with no reason at all.
F006 is the sharpest: A1's mechanism passed a count budget and failed 6/6 under a
walking-distance budget its own report never priced — a gate missing at report
time, not a search failure.

**Why it matters for item 0.** The record's implicit model was that every
candidate died because the world already had it, which makes the problem "our
ideas are not novel." For at least 7 of 18 that diagnosis is wrong, and the
repair differs: **promote fewer claims and price each one's gate before
promoting it.** That is now an option for the owner decision with a count behind
it, alongside the axes item 0 already named.

**What is still open, and it is the same shape as E023's.** One reader, no
second coder — at a one-row margin, **κ on the same 18 rows by an independent
reader is what would settle whether the record's sentence is a fact or a
coin-flip.** Not run.

**Ceiling.** A count over the record as written. It falsifies no prior-art
verdict and reopens no candidate — F035 already measured that separate question
on F029's population and found 3 of 12 adjudicable kills had no prior art.

## Is a screen whose premise is unmeasurable four times in five a screen?

**Status: closed as an open reading, with one question left (F034, F037, F041).**
Was item 0c of `STATE-next-actions.md`, moved here when F041 made the ranked
list's entry redundant.

F034 could read serving evidence for **57% of the incumbents its own population
contained and 22% of the young arm** — which is a statement about the world's
distribution rather than about this repository's tooling. F037 measured the
fraction and it is **high exactly where the candidates live: 14 of 18 young rows
undecided, 13 of them tools, and 43% of the mature arm.** It also showed
undecidability does **not** track artifact class — 10 of the 14 unreadable young
rows are executable — so "this is just a document" never explains an unreadable
row. F041 then found the missing channel is a *smaller* one, and that its own
blind spot is the placebo arm.

**What remains open is whether the unmeasurable fraction predicts anything about
the need**, and its falsifier is a population where that fraction is near zero.

**Ceiling, and it is the reason this is a reading rather than a verdict:**
015's `placebo.py` shows the instrument *can* read unpopular projects when it looks
for readable ones, so "unmeasurable" is partly an artefact of which channels were
consulted. **A follow-up must state its channel set or it measures the
instrument.** That is now also the fifth condition of
[`docs/process/experiment-protocol.md`](docs/process/experiment-protocol.md)'s
prior-art rule.

## The recurrence bound is refuted; the zeros were a stratum effect (F055)

**Status: closed, and it withdraws the reading below rather than confirming it.** Item
0d's last standing question, re-asked with a different instrument. Raw evidence in
[`EXPERIMENTS/033-question-recurrence/`](EXPERIMENTS/033-question-recurrence/README.md).

**What was measured.** Cross-author recurrence read off **Stack Exchange's own
duplicate-closure judgement** — `closed_reason == "Duplicate"`, decided by other people —
rather than off a linkage rule this repository invented. **1000 questions from two
volume-selected sites: 54 duplicate closures = 0.0540, CI95 [0.0416, 0.0698]**, against
the pooled **0.0223** bound E031 and E032 established. `travel` 0.0660, `math` 0.0420.
**B1 fired; the bound is refuted**, and conservatively so, because the label counts only
closures — a repeat that was answered is not counted.

**The mechanism is measured for E032, and it is not a defect in the reader.** Sorting this
population by score and taking the top 60 — what `sort=votes` drew — yields **0** duplicate
closures, against a mean of **3.37** over all 941 sliding 60-question windows. The rate runs
**0.0180 in the top score tertile and 0.0808 in the bottom, a 4.5× gradient.** E032 declared
that bias as a caveat in its own limitations section; it was load-bearing. `sort=votes` was
chosen because "elaborated need statements live there", and it selects for answered
questions — which are the ones that were *not* repeats.

**That explains E032 and only E032.** The Hacker News zeros have their own already-recorded
explanation, F039: the corpus is **1250 individuals each asking once**, so no requirement
could recur inside it at any sample size. Calling both "the wrong stratum" would be tidier
than the evidence allows, and transferring the tertile effect to Hacker News is an
inference, not a measurement.

**So both readings were true and the record kept the weaker one.** Recurrence is common in
public questions, *and* the mission's samples were drawn from where it is rarest. The
five zeros were a statement about a stratum before they were a statement about the world.

**A second claim was withdrawn by the run itself.** The same data reads as convergent-and-
unanswered demand — a duplicate closure is **2.6× more likely to carry `answer_count == 0`**
(0.5556 against 0.2114, CI95 [+0.2096, +0.4710]) — but **zero of the 54 has an accepted
answer**, and closing a question as a duplicate does not answer it, so most of that gap is
what closure *does* rather than what askers needed
([`PROTOCOL.md`](EXPERIMENTS/033-question-recurrence/PROTOCOL.md) AMENDMENT-3 §2). The
sharper defect is the order: **the mechanical explanation arrived only after both readers had
reported**, because nothing in the protocol asked whether the label could produce the
difference by itself. **The run therefore has one result, not two.**

**What is not revived.** No candidate: 54 closures were counted, **no clause or cluster was
recovered**, and no prior-art screen was run. This is not Hacker News either — the method
defect transfers, not a rate.

**The constraint that follows, and it is about the archive.** A duplicate closure is a
reliable **label** and an unreachable **edge**: the public API exposes neither
`closed_details` (which names the canonical) nor `question_type`, and the four vectorised
`{ids}` routes tried all return `no_method`, so one canonical costs one request.
`/questions/{id}/related` returns topical rows that the reader arm confirmed as the
canonical only **6 times of 24**, failing its declared gate. `tally.py` therefore refuses
to print the declared visibility product rather than compute it from canonicals this run
had just rejected. Four routes tried, in
[`API.md`](EXPERIMENTS/033-question-recurrence/API.md).

## The first demand-side instrument that returned positives — and could not read them (F057, D063, D064)

**Status: the pooled gradient is closed and replicated; the per-tag reading is
`not_established`; the mechanism is not measurable on this instrument.** Item 0d's
empty invention seat. `EXPERIMENTS/034-reask-tail/`, T-0078, D063/D064.

**What was measured.** Duplicate closure read off Stack Exchange's own `closed_reason`
on three matched arms of the same tags — `tail` (`sort=votes&order=asc`), `head`
(`sort=votes&order=desc`), and **`default` (`sort=activity&order=desc`, the `Active`
tab, which is what a person browsing the tag actually sees)** — 2124 rows over eight
pre-named tags in four a-priori strata, 101 requests, every response body committed
beside its sha256.

| arm | n | duplicates | rate | CI95 | score range |
|---|---|---|---|---|---|
| `tail` | 725 | 98 | **0.1352** | [0.1122, 0.1620] | −85 … 0 |
| `head` | 674 | 25 | 0.0371 | [0.0252, 0.0542] | 30 … 27242 |
| `default` | 725 | 22 | **0.0303** | [0.0201, 0.0455] | −11 … 5855 |

**4.5× against the feed a person reads**, on equal denominators too (0.1454 against
0.0282), and **F055's whole-site gradient is now measured twice in two designs**.

**What is new: the rate is a per-tag property, and it was never measured before.** Ten
tags span **0.0000 to 0.4300** with **12 disjoint interval pairs** among the seven
clearing n ≥ 50, and **both extremes reproduce on the next four pages** out of sample
(`customs` 0.430 → 0.495, `excel-formula` 0.000 → 0.000) from **43 distinct askers over
28 distinct months**. The `Active` tab reads 0.02 where the tail reads 0.43 for
`customs`, and 0.03 where the tail reads 0.00 for `excel-formula`: a reader watching the
feed would call those two tags identical and would be wrong in opposite directions.

**Why it is still not a candidate, in two sentences each.**

- **D6 fails.** Duplicate closure is a **moderator act**, and the declared population had
  one `travel` tag against five `stackoverflow` ones, so the highest cell was the only
  cell from its site. AMENDMENT-1 added `travel`/`baggage` (0.1979) and
  `math`/`calculus` (0.1020); **within-site disjoint tag pairs run 4/10 against 14/26
  cross-site**, so site and tag both carry real variance and 3–5 tags per site cannot
  apportion them. The declared R2 gate was **ill-formed before the fetch** — "disjoint
  from *both* math tags" and "overlaps *a* math tag" were both true — which is D064.
- **B1 fails.** Among duplicates, the share with no accepted answer is 0.8163 in the tail
  against 0.7273 in the `Active` tab, difference **CI95 [−0.0774, +0.3075]**. *"The
  answer existed and was not found"* cannot be separated here from *"a moderator closed
  it"* or from *"closure hides the answer"* — E033's AMENDMENT-3 §2 error, walked into a
  second time because nothing in the protocol asked whether the label could produce the
  difference by itself. **What is established is where the repeats sit, not what
  happened to them.**

A third declared claim is dead: **the a-priori stratum hypothesis is backwards.**
`excel-formula`, the situational exemplar, has the *lowest* rate of all ten tags at 0/100
while the "one canonical answer exists" tags sit at 0.12–0.19. It was declared before
the fetch, and nothing replaces it.

**Two facts that outlive this run.** **The canonical edge is unreachable** from this host
through **nine** named channels — adding the question's own comments, the answer's
`closed_details`, a browser User-Agent on two hosts, both StackPrinter hosts and SEDE to
E033's five — so **E033's open question "what to measure recurrence on" is answered on
its other half: the label is available, the edge is not.** And **the label is ten
literals, not one** (D063): `closed_reason` is absent on all 1790 open rows and present
on every one of the 724 closed rows, so absence means "not closed" and nothing is
imputed, but `exact duplicate` (9 rows) is the legacy spelling of `Duplicate` (222).
**E033's 0.0540 is a floor, and every rate derived from it is too.**

**The single next action is D6's own:** three to four more tags on each of the three
sites, `tail` arm only, 4 pages each — about 30 requests against a fresh 300. Nothing is
built on this population until tag is separable from site.

## The demand-side absence of recurrence survives a change of venue — **superseded by F055**

**Status: withdrawn as a general statement. What it measured is sound; what it concluded
is refuted.** F039, F049 and F051 as below; F053 and F054 above. **The pooled 0.0223
bound did not survive being measured on a whole population with the platform's own
judgement instead of this repository's linkage rule** — see F055 above. Read this section
for what the five zeros established, and the one above for what they were about.

**What the two populations now say.** F039 found the need corpus is **1250
individuals each asking once**, with no need-level recurrence inside it. E031
reached the same reading from a **structurally different** population — 919
departure accounts from people who had depended on the thing, 326 of them framed
as seeking an alternative — and found **0 recurring requirements in 63 clauses**,
against a reader-adjudicated random-pair control at 0.

**Why this is a change and not a repetition.** Until now the recurrence null had a
single alternative explanation available: F043 showed the trigger vocabulary is
blind to outcomes, so the need corpus's zero could have been the instrument's. A
second corpus, harvested by **different phrases about a different event**, with
its own reader question and its own controls, gives the same zero. The absence is
therefore **not an artefact of any vocabulary this mission chose** — and it is a
fact about **what people write on Hacker News about tools they have left**, which
is what F053 leaves it as.

**The premise that failed is the useful part.** E031's hypothesis was that
accounts seeking an alternative state a requirement the artifact failed. They
state a missing capability at **twice** the base rate of ordinary comments — and
**exactly as often as accounts that named a successor** (0.347 against 0.347).
**What a departure account lacks is not a missing capability; it is a named
successor.** The population is people reporting friction, not people holding an
unfilled slot. That is why recurrence is zero, and it is why this closes a
generator rather than merely failing to open one.

**What this makes cheap to believe, and what it does not license.** It is cheap to
believe that **a cross-author recurring requirement will not be found by mining
Hacker News comments** — two corpora, five readings, five zeros, and the
vocabulary varied each time. That part is earned and it is the stronger claim.
It licenses **no** claim about other venues, and **not** one that unmet
requirements do not exist, that none recur, or that they cannot recur: F042's
0-of-24 and F049's CI95 [−0.0156, +0.1125] are disclosures and bounded
intervals, not zeros, and E031's own sample is **63 clauses** with its ceiling
declared before the adjudication (AMENDMENT-4).

> **Superseded 2026-10-06 (F055).** The 0.0223 bound this paragraph defends is
> **refuted**: 54 duplicate closures in 1000 questions, 0.0540 CI95 [0.0416, 0.0698], read
> from Stack Exchange's own closure judgement rather than from this repository's linkage
> rule. The mechanism is a stratum effect — `sort=votes` draws the tertile where recurrence
> is 4.5× rarest, and the top 60 by score contains 0 duplicate closures. The paragraphs
> below are kept because they record what each run established; none of them carries the
> generalisation any further.
>
> **Corrected 2026-10-06 (F053).** This paragraph used to read "mining public
> conversations — three populations, three instruments, three zeros". **The venue
> was never varied.** All 3,856 comment ids behind F039, F042, F043, F049 and
> F051 come from `hn.algolia.com` / `hacker-news.firebaseio.com`, and E019, E022,
> E026 and E029 all re-read E012's single 1401-comment file at **100% identifier
> overlap** — so there are two corpora, one of them read four times, not three
> populations. F051's own ceilings already said as much ("One corpus and one
> channel set"); the summary sentence was where the bound was dropped.
> [`EXPERIMENTS/032-venue-recurrence/`](EXPERIMENTS/032-venue-recurrence/PROTOCOL.md)
> tests the venue as the single changed variable.

**The transferable instrument lesson is D062.** A linkage rule is part of the
instrument: state the candidate count it produces against the count chance alone
produces, before reading any adjudication. E031's declared rule produced **4
pairs against a chance expectation of 4.9** — unreachable, the mirror of F010's
gate that could not fail — and **fixing F050's coincidence problem caused it**,
because a ≥ 2-rare-token rule tuned for 90-word comments does not transfer to
11-word clauses. The control is **reader-adjudicated random pairs from the same
arms through the same filters**, not a permutation of the candidate set, which is
F043's missing control in a second instrument.

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Failures — recorded finding F053

Split out of [`FAILURES-findings-21.md`](FAILURES-findings-21.md), which held
F051 and F052. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F053 — "three populations, three instruments, three zeros" is two populations and one venue, and the venue was never varied

**Date:** 2026-10-06. Task T-0076. Established from primary sources — the
harvest code and the raw captures — before any part of E032 was run. The
experiment that tests it is [`EXPERIMENTS/032-venue-recurrence/`](EXPERIMENTS/032-venue-recurrence/PROTOCOL.md);
this entry does not depend on that experiment's outcome.

### The sentence under test

[`STATE-in-flight-2.md`](STATE-in-flight-2.md) line 120, written after E031:

> It is now cheap to believe that **a cross-author recurring requirement will not
> be found by mining public conversations** — three populations, three
> instruments, three zeros.

Item 0d of [`STATE-next-actions.md`](STATE-next-actions.md) then reads "All three
generators under this seat are closed, for measured reasons", and F039, F049 and
F051 are the evidence those readings lean on.

### What was checked, and how

Every host and every identifier in the chain that produced those zeros, counted
from the code and the captures rather than from any summary:

| population | file | distinct ids | shared with E012 |
|---|---|---|---|
| E012 trigger harvest | `012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl` | 1401 | — |
| E019 / F039 authors | reads that file directly | 1401 | **1401** |
| E022 / F042, F043 outcomes | `022-need-outcomes/raw/outcomes.jsonl` | 1401 | **1401** |
| E026 structure | `026-unserved-need-structure/raw/texts.jsonl` | 1401 | **1401** |
| E029 / F049 need-to-build | derives from E025 ← E022 ← E012 | 1401 | **1401** |
| E030 / E050, F051 departures | `030-departure-recurrence/raw/harvest.jsonl` | 2457 | **2** |

**3,856 distinct Hacker News comment ids** stand behind F039, F042, F043, F049
and F051. Every host any of those experiments contacted for *account text* is a
Hacker News host: `hn.algolia.com`, `hacker-news.firebaseio.com`,
`news.ycombinator.com`. The only other host is `api.github.com`, used in E012
and E030 solely by `prior_art_probe*.py` and `recurrence_probe.py` to look up
whether an author has published a repository — no account text was read there.

### What is correct, and what is not

**Correct, and the stronger of the two claims: the zero does not follow from the
harvest vocabulary.** The vocabulary genuinely varied — 25 unmet-need phrases in
E012, departure-framing phrases in E030 — and the result held. That is real, and
it is the more useful half.

**Not carried by the evidence: the venue.** One venue was sampled, five times,
with one variable changed. "Public conversations" is a claim about every public
conversation; the evidence is about Hacker News comments: short, story-anchored
replies, written largely by self-selected technical readers, on one platform in
one language in one era.

**Also over-counted: the populations.** There are **two** corpora, not three, and
one of them was read four times. E019, E022, E026 and E029 are four readings of
E012's single 1401-comment file at 100% identifier overlap. Calling them three
populations makes one corpus look like corroboration.

**The findings themselves are honest; the summary sentence is what over-reaches.**
F051's own ceilings already say *"One corpus and one channel set. GitHub issues,
Reddit, support forums and the open web were declared unread by E030 and remain
unread."* The finding is bounded correctly. `STATE-in-flight-2.md` line 120 is
the place the bound is dropped.

### Why it changes a decision

The recurrence result is what retires item 0d's seat. If the zero is
**venue-specific**, then the three generators were closed by a property of one
platform rather than by a property of unmet needs, and the seat is empty for a
reason that a different venue can overturn. If the zero **generalises**, the
mission's most expensive belief is right and rests on more than it claimed to.

Both readings change what to do next, which is why the confound is worth a run
rather than a footnote. `EXPERIMENTS/032-venue-recurrence/` changes exactly one
variable — the venue — on a population selected by a structural rule carrying no
requirement vocabulary, and keeps E031's instrument, its linkage rule, its
control and all four of its instrument gates.

### Ceilings

- **This is a count of hosts and identifiers in code and captures.** It shows the
  venue never varied. It does **not** show a recurring requirement exists
  elsewhere, and nothing here is a result about any venue but Hacker News.
- The comparison is between what was written and what was measured. A different
  reader might have phrased the summary more narrowly on the same evidence; the
  point is that the sentence is not supported by what sits behind it.
- `api.github.com` was checked for account reads and found carrying none; a
  different reading of those scripts could change that, though the file names and
  the query parameters say otherwise.
## F054 — the recurrence zero is not a property of Hacker News: it holds on a second venue class, and the generator closes for a better reason

**Date:** 2026-10-06. `EXPERIMENTS/032-venue-recurrence/`, task T-0076.
Protocol declared before any fetch, amended once before any pair existed.
F053 named this as the run that would settle the venue; this is its result.

### What was asked

F053 established that the mission's three-zero recurrence result rests on **one
venue**. E032 changes that and nothing else: same reader question, same linkage
rule imported from E031's own module, same reader-adjudicated control, same four
instrument gates, same 0.20 margins. The population is **60 long-form questions
from three non-programming Stack Exchange sites**, 53 authors, selected by date,
site and length with **no requirement vocabulary anywhere in the selection** —
F043's constraint, so the population is not the harvest's fault.

### What was observed

| | |
|---|---|
| clauses both readers agreed state a want | **28** (of 60 questions) |
| candidate pairs under E031's rule | **32**, against a chance expectation of **1.19** — reachable by 27× |
| candidate pairs judged `same` | **0 of 32** |
| control pairs judged `same` | **0 of 60** |
| difference | **0.0000**, CI95 **[−0.0602, +0.1072]** |
| instruments | A1 6/6 fetches, **A2 reachable**, **A3 κ = 0.8344**, **A4 0/24 and 0/10**, **A5 20/20** |

**B2 fires. Nothing recurs on a second venue class either**, and the instrument
returned a positive on 20 of 20 synthetic positives and none on 10 unrelated
pairs.

### What this rules out, and what it does not

**Ruled out:** the reading that the zero is a property of Hacker News — its
comment length, its story-anchored unit, its technical population, or its
selection by trigger vocabulary. Any of those could have produced it, and none
of them does.

**Established, as a bound rather than a zero.** 0 of 32 puts the one-sided 95%
upper bound at **0.0894**: a recurring-requirement rate near **1 in 11** is not
excluded by this run. Pooled with E031's 100 adjudicated candidates, 0 of 132
gives **0.0223** across two venue classes — and pooling is what makes the number
mean something, since E032 alone is the weaker of the two.

**Not established:** any claim about unmet requirements themselves. Consistent
with F042 (0 of 24 unserved requesters built it), F043 (the served figure was the
base rate of a Hacker News conversation) and F049 (**167 of 241** need-staters
shipped *before* they complained), a zero here is one more reading of the same
picture: a need stated in public is absorbed in conversation, and the requesters
are largely people who had already built something.

### Ceilings

- **28 clauses.** Two people needing the same capability twice must both land in
  the sample. This is the binding constraint on the bound and it is not lifted by
  the venue change.
- **One platform, one language, 2025–2026, three sites.** A negative is bounded
  the way a positive would be.
- **`sort=votes` prefers answered questions**, so the population over-samples
  engaged users. Chosen deliberately — elaborated need statements live there —
  and recorded because it is a bias.
- **Two readers of one model family.** κ = 0.8344 is evidence the question is
  answerable from the text, not evidence two people would agree; they disagreed
  on 5 of 60 rows about whether a want is stated at all.

### What this costs item 0d, honestly

Item 0d closes three demand-side generators and says the seat is empty by
measurement. **That reading survives**, and it survives for a stronger reason than
the one it was written on: not one platform's properties but two structurally
different venue classes, with instruments that pass their own controls. What
F053 withdrew was the generalisation to public conversation; what F054 replaces
it with is a venue-agnostic claim at a **2.2% upper bound**, which is a real
constraint on candidate generation and is worth more than the sentence it
corrects.

## F055 — the pooled recurrence bound is refuted, and E032's population was drawn where recurrence is rarest

**Status: this refutes a reading the record drew, not a measurement in it.** Evidence in
`EXPERIMENTS/033-question-recurrence/`, protocol declared before the fetch and amended
three times: twice for defects in the *protocol* itself, and once after the run to withdraw
this experiment's own second claim and correct one of the earlier amendments.

Five experiments in this record reported zero cross-author recurring requirements, and
`EXPERIMENTS/032-venue-recurrence/README.md` pooled two of them into an upper bound of
**0.0223** — the number that closes item 0d's third demand-side generator. E033 read
recurrence off **Stack Exchange's own duplicate-closure judgement** rather than off a
linkage rule this repository invented, over 1000 questions from two sites chosen by volume:

- **54 of 1000 questions closed as duplicates = 0.0540, CI95 [0.0416, 0.0698]**, against
  the record's 0.0223. `travel` 0.0660, `math` 0.0420. **The bound is refuted** and the
  refutation is conservative: the label counts only closures, so the true rate is higher.
- **E032's population was drawn where the thing is rarest.** Sorting this population by
  score and taking the top 60 — what `sort=votes` drew — yields
  **0** duplicate closures, against a mean of 3.37 over all 941 sliding windows. Duplicate
  closures are **0.0180 in the top score tertile and 0.0808 in the bottom**, a 4.5×
  gradient. E032 recorded this bias as a caveat; it was load-bearing — but it explains
  E032, and only E032.
- **The run's second claim was withdrawn by the run itself.** 0.5556 of duplicate closures
  carry `answer_count == 0` against 0.2114 of every other closure state, and that gap reads
  as convergent-and-unanswered demand — but **zero of the 54 has an accepted answer**, and
  closing a question as a duplicate does not answer it, so most of the gap is what closure
  does rather than what askers needed. `PROTOCOL.md` AMENDMENT-3 §2 withdraws it. The
  sharper defect is the order: **the mechanical explanation only arrived after both readers
  had reported**, because nothing in the protocol asked whether the label could produce the
  difference by itself.

### What it does not license

Nothing revives a candidate: 54 closures were counted, **no clause or cluster was
recovered**, and no prior-art screen was run. This is not Hacker News either — what
transfers is the method defect, not a rate.

**The two zeros have two explanations and only one is measured here.** E032's is the score
tertile above. The Hacker News need corpus has a different one already on record: F039
measured **1250 individuals each asking once**, so no requirement could recur inside it at
any sample size. Reading both as "the wrong stratum" would be tidier than the evidence
allows; the tertile effect is a fact about this population and its transfer to Hacker News
is an inference.

### The instrument finding that constrains everything downstream

**A duplicate closure on this platform is a reliable label and an unreachable edge.** The
public API exposes neither `closed_details` (which names the canonical) nor `question_type`
(which marks a related row as the duplicate), and the **four vectorised `{ids}` routes tried all return
`no_method`**, so one canonical costs one request. `/questions/{id}/related` does return
6–10 topical rows with full metadata, so a canonical is guessable — and this run's reader
arm confirmed **6 of 24** of those guesses, failing its declared gate of 30 of 40. Two
third-party renderers that would show the closure banner were tried: one 403s, one returns
a "server too busy" page as HTTP 200. `tally.py` **declines to print** the declared
visibility product `n·p·q` because its second input rests on canonicals this run had just
rejected; a number that would have read as a decisive mechanism check is not reported.

### The generalisable rule

**An instrument's zero is a statement about the population it sampled before it is a
statement about the world, and a selection criterion chosen for other reasons can invert a
result.** `sort=votes` was declared because "elaborated need statements live there". It
selected for answered questions, and answered questions are the ones that were *not*
repeats — so the population was chosen against the signal while the sample was too small
to see it anyway. F039's recurrence instrument and E032's were not wrong instruments;
they were pointed at a stratum where the thing was 4.5× rarer.

Full derivation, gates, amendments and the four routes tried: `EXPERIMENTS/033-question-recurrence/`.

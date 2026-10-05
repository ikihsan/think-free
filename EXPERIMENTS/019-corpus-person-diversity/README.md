# E019 — How many people are in the need corpus, and can a shared need appear in it?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Date:** 2026-10-05. **Declarations in this file were written before any figure
below was fetched or read.** Task T-0063.

## The question

The mission's only demand-side instrument is E012's corpus: 1401 "is there a
tool that"-shaped comments harvested from Hacker News comments since
2024-01-01. Fifty of them were screened by a stated rule and **0 survived**
(F029). E014 then offered a rescue — the same cluster counted per repository is
unambiguous — and E014's own filter collapsed it by ~200x to 15 issues across 9
agent-labelled repositories, read as "a complaint inside a dozen agent-project
trackers, not a cross-project problem" (F033).

**Two quantities that would bound all of that have never been computed.**

1. **How many people are in the corpus.** 1401 comments is a count of *rows*.
   Nobody has counted authors. Every conclusion the mission draws from this
   corpus — F029's 0 of 50, D050's narrowing, F033's collapse — is a statement
   about a population whose size is unknown.
2. **Whether the corpus can express recurrence at all.** F033 measured
   recurrence per *repository*, in an audience organised by project. One
   explanation was never tested: a need whose vocabulary confines the people who
   complain to one kind of project will look non-recurrent in any
   repository-level count, because only those projects contain the complaint. A
   distinct-*person* denominator in the same corpus is the direct alternative.

So: **is F033's conclusion a fact about the needs, or a fact about the
denominator?**

## Hypotheses

- **H1.** The corpus is a wide audience — its comments come from many distinct
  people, not from a few prolific ones. If so, recurrence was *available* in
  the corpus, and F029's 0 of 50 is a statement about the needs.
- **H2.** The corpus is a narrow audience — the 1401 rows come from far fewer
  people than rows. If so, no clause could have reached recurrence inside it,
  and F029's negative is largely a fact about the instrument's reach. **This
  would not reverse F029** (the 50 still died on their own merits) but it would
  change what a negative from this corpus is allowed to mean.
- **H3.** Person-level recurrence separates clauses the repository-level count
  called non-recurrent. If it does, F033's conclusion is a denominator artefact
  for those clauses.

## Gates, declared before the first fetch

**Gate A1 (arm A integrity).** Author must be recovered for at least 95% of the
1401 comment ids. Below that the missing rows are reported as missing, never
imputed, and every arm-A figure is labelled `inconclusive` for the missing
fraction.

**Gate B1 (arm B instrument validity).** At least **5 of 6 positive controls**
must return at least **3x** the median distinct-author count of the **6 negative
controls**. Otherwise arm B reports `inconclusive` and **no recurrence verdict
is drawn from it at all**. This gate exists because F030 established that a
verdict from one query is wrong in both directions; the controls are how that
failure would be visible here.

**Kill gate (arm B, load-bearing).** If **every** declared clause returns fewer
distinct authors than the **weakest** positive control, person-level recurrence
does not rescue the need corpus: the demand-side generator is closed, and F029's
0 of 50 becomes a statement about the world's needs rather than about the
corpus.

**Positive gate (arm B).** If **any** declared clause returns more distinct
authors than the **median** positive control, then F033's project-level verdict
is a denominator artefact for that clause, and D050's narrowing is reversed for
it.

**Floor, declared so it cannot be reinterpreted.** A clause was harvested from
one comment, so its own author always appears in its own result. **Exactly one
distinct author means no external recurrence whatsoever** — it is the trivial
floor, not a weak positive.

## Method

| step | script | what it fixes |
|---|---|---|
| arm A | `corpus_authors.py` | one primary-source item fetch per comment id; author, time, parent story |
| arm B | `recurrence_probe.py` | declared clause and control phrasings against the public HN index |
| both | `stats.py` | every figure in `results.json`, from the raw captures only |

**Clause selection is mechanical and takes no taste.** The ten arm-B clauses are
rows 5, 10, 15, ... 50 of `EXPERIMENTS/012-candidate-harvest/raw/sample.jsonl`
in that file's recorded order — the same order the 0-of-50 screen used.

**Query construction is mechanical.** For each clause two queries are issued:
the clause **verbatim in quotes**, and the **first four content words** in
order, content = lowercase token of length >= 4 not in `STOPWORDS`, also quoted.
The verbatim figure is primary; the four-word figure is a sensitivity check and
is only ever allowed to **raise** the reported count.

**Positive controls (named before fetching, F029/E012 neighbours with known
adoption):** spaced repetition flashcards; self-hosted email server; atproto
personal data server; AI coding agent unrequested changes; lossy webp
conversion; OCI image to rootfs.

**Negative controls (declared activities, nobody does):** gauge drift in a
knitting chart; a quorum rule for a five-person book club; provenance for a
terrarium; a hedger for municipal bond refinancing; sorting a tram timetable by
elevation; a linter for 19th-century parish registers.

**Distinct authors** are counted from fetched hits, capped and the cap recorded;
`nbHits` is an estimate and is never used as an author count.

**Arm A2, added before any B figure was fetched.** Arm A established that the
corpus is 1250 distinct people. What that *means* for F029 turns on a fact
F029 asserted in passing and never measured properly: "term recurrence over
1273 clauses returns only function words, the top content term appearing in
six." If no two clauses in 1250 share even one distinctive word, the corpus is
a sample of **individual requests**, and a generator that needs a *need* to
appear more than once cannot be built from it at all — which would explain
0-of-50 as a property of the corpus's composition rather than of the screens.
A2 measures it with no network and no phrasing, so nothing can go wrong between
the clause and the number.

Rule, fixed now: a clause's content words are its lowercase alphabetic tokens of
length >= 4 that are not in `STOPWORDS`. A clause's **bottleneck** is the
smallest number of *other* clauses sharing any one of its content words. A
bottleneck of 1 means no other clause in the corpus mentions anything it
mentions.

Gates, declared now: **if >= 90% of eligible clauses have a bottleneck of 1,
the corpus is a sample of individual requests and the aggregation-based
generator is closed.** If < 50% do, sharing exists in the corpus and F029's
recurrence reading was wrong. Between 50% and 90% the experiment reports the
distribution and refuses a verdict. F033's cluster -- changes a
coding agent makes that nobody asked for -- was measured across 9
agent-labelled *repositories* after E014's filter collapsed it. The
person-level version of the same question needs no network and no phrasing, so
it is run inside the corpus that is already in hand: **how many distinct
authors among the 1250 wrote a clause containing both an agent-family term and
a change-family term?** Both term families are listed in
`recurrence_probe.py::FAMILIES` and were fixed before the count ran. This is the
only arm-B row that can be *refuted* by a count rather than by a query, so it is
the load-bearing half of arm B and the kill gate is evaluated on it.

## Environment

Public Hacker News Firebase item API and `hn.algolia.com` search index, both
unauthenticated. Python 3.8.10, `instance-20260717-0944`, 2 CPUs. No rate limit
was hit and every refused answer is kept apart from an absence.

## Results

All figures computed from the captures in `raw/` by `stats.py`.

### Arm A — who is in the corpus (decisive)

| figure | value |
|---|---|
| comments | 1401 |
| **distinct authors** | **1250** |
| comments per author | median 1, mean 1.12, p90 1, p99 3, max 8 |
| distinct parent stories | 1276 |
| distinct days | 466 |
| rows with a recovered author | 1401 (100.0%) — **gate A1 met** |
| deleted or dead rows | 0 |
| top 10 authors' share of comments | 0.55% |

**H1 supported; H2 disproved.** The corpus is a wide audience of individual
requesters. "The harvest was too small or too concentrated for a shared need to
appear" is not available as an explanation for anything downstream.

### Arm A2 — does the corpus contain any need twice? (no verdict, by its own band)

Rule fixed before the count: a clause's *bottleneck* is the fewest **other**
clauses sharing any one of its content words; `1` means no other clause in the
corpus mentions anything it mentions.

| figure | value |
|---|---|
| eligible clauses | 1152 |
| clauses with bottleneck 1 | 913 (**79.25%**) |
| the 49 sample rows the 0-of-50 screen used | 43 at bottleneck 1 (87.8%) |
| bottleneck histogram | 1:913, 2:156, 3:52, 4:9, 5:6, 6:6, 7:2, 8:3, 12:2, 13:1, 21:1, 24:1 |
| top document-frequency terms | `x2f` 119, `better` 41, `people` 41, `know` 31, `easy` 30 |

79.25% is inside the declared 50–90% band, so **the experiment reports the
distribution and refuses a verdict**. The top term is a URL-escaping artefact of
the harvester; the top genuine terms are all generic, which is F029's
"recurrence returns only function words" confirmed in substance and measured
under a declared rule instead of asserted.

### Arm B — the recurrence instrument, and the person-level cluster count

| query group | distinct authors |
|---|---|
| the 10 declared clauses | **0–1 each; eight at the floor of 1** |
| positive controls | 34 (`spaced repetition flashcards`), 47 (`self-hosted email server`), 1, **0, 0, 0** |
| negative controls | 0, 0, 0, 0, 0, 0 |

**Gate B1 is met numerically and is degenerate.** Its threshold was `3 × the
median negative control`; the negative median is 0, so the threshold is 0 and
six of six positives clear it — including the four that returned nothing.
**Arm B1 therefore reports `inconclusive` and no recurrence verdict is drawn
from it.** The declared kill gate is recorded as **not evaluable**, not met.

The finding that survives arm B is about the instrument, not the corpus:
**exact-phrase author counts returned 0 for four of six activities with
demonstrated adoption.** A low recurrence number carries no information about
whether others share a need, which is F030's failure mode reached by a different
route, and it bounds every recurrence figure this mission has ever produced
against a *written* population.

**Arm B2** — 25 of 1250 authors (2.0%) named both a declared agent-family term
and a declared change-family term. Reading the rows shows most are not F033's
cluster (Windows 11 without Copilot, hiring staff to use AI, a sensor that
detects people at a distance), so 2% is consistent with background
co-occurrence of a common term family. **Inconclusive.**

## Verdict

| arm | verdict |
|---|---|
| A | **decisive** — 1250 distinct people |
| A2 | declared band 50–90%, no verdict, distribution reported |
| B1 | instrument failed its own controls |
| B2 | inconclusive |

**What is established (`observed`):** the corpus is a wide audience of
individual requesters, and 79.25% of its clauses share no content word with any
other clause. It is not a sample of shared needs.

**What is not established:** that these requests lack shared demand — only that
this corpus cannot show it, and that no lexical recurrence instrument tried here
can show it either. F039 must not be cited as a claim about the world's needs.

## Two instrument defects, recorded because both would have flattered a verdict

1. **A schema mismatch between two APIs for one site read as perfect recovery.**
   `raw/corpus_authors.attempt1.jsonl` holds 1313 rows, every one `ok`, every
   one with a null author: the Firebase item API names the field `by` and the
   Algolia API names it `author`, and the script asked Algolia's name of
   Firebase. A status column said the fetch worked.
2. **A gate can be met degenerately by a zero.** `3 × median(negatives)` is 0
   when the negatives are all 0, so the gate could not have failed. A ratio to a
   control that can be zero needs a floor, and this one had none.

## Limits

- Distinct-author recurrence is **attention in one audience**, not demand, not
  willingness to pay, and not need. This experiment bounds an instrument; it
  measures nothing about whether a need exists.
- Phrasings are lexical. A clause's recurrence is only as real as its query, and
  the negative controls are the only check on that.
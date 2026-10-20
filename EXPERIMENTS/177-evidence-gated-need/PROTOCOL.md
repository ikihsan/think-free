<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E177 PROTOCOL — is the assistant worse when the deciding evidence is absent from the question?

**Date opened:** 2026-10-17. **Status:** pre-declared before the fetch, before the
classifier, and before any answer body was read. Nothing below may be edited
after the first answer body is on disk, except by an amendment file that names
what it changed and why.

## Why this population, and why not E176

E175 drew 200 answered high-arrival Stack Overflow questions and found that
**21 of 145 (0.1448) name a repository and 10 (0.0690) name a tracker
document — 79% record no repository link at all** (F135). E176, the named next
action, classifies what those 124 answers contain instead. E176 is a
classification of the *same 200 rows* by the same instrument as E175 and E168.

This is the third consecutive session whose population is those rows, and the
brief asks for the opportunity cost of that to be stated rather than assumed.
So this experiment states it: **E176 would tell us which bucket is biggest; it
cannot tell us whether any of the buckets is worth building for**, because
every candidate this mission has ever had to reject was rejected for the same
reason — a free general assistant already serves it (D107's table: six
populations, 0.85 to 1.0). The reason those six all came out served has never
been isolated, and it is not a fact about the venues.

## The reason six closures in a row came out served

Each closure measured a population whose answer is **computable from the text
already in hand**:

| population | decidable from | served |
|---|---|---|
| non-software SE needs (E062) | question + facts | 17/20 |
| Anova appliance threads (E091) | question + facts | 5/20 |
| Home Improvement SE (E092) | question + facts | 30/37 |
| SO program-shaped residue (E126) | question + facts | 0.6750 |
| Cross Validated (E143) | question + facts | 20/20 |
| CFR applicability (E115) | rule text + facts | 14/14 |

D107 turned this into the mission's **only standing constraint**: a candidate
must target a task whose answer *cannot* be computed from the text plus the
facts, because the missing input is **evidence**, not arithmetic. That
constraint has governed candidate selection for five days and has **never been
measured**. It rests on an inference, not an observation.

E115's protocol named the inference exactly: populations whose correct answer
turns on facts no rule states "cannot be keyed by hand, so they cannot be
scored against a committed key." That is a statement about E115's instrument.
It is not evidence that the population is small, served, or absent.

## The practical difficulty, stated concretely

Somebody hits a wall and asks. Sometimes the answer is a two-line reasoning
step over what they already wrote. Sometimes the answer needs one fact they did
not write down — the version they are on, the platform they are on, the exact
config, the upstream changelog, the library they are actually calling. In the
second case the answer exists and is correct, but it is **not derivable from the
question**, so it took a human being to go and get it. That is the population
D107 points at without ever having measured it.

## The question, as one comparison

**Given a real answered question, is a free general assistant measurably worse
at reaching the accepted answer's resolution when that resolution depends on
at least one fact or artefact the question does not contain?**

Both arms get the identical treatment and the identical key. Only the question's
own evidence completeness differs.

| arm | definition | 
|---|---|
| **SELF** | the accepted answer's resolution is reachable from the question's own text |
| **EVID** | the accepted answer's resolution depends on at least one fact or artefact absent from the question |

Both classes are drawn from one population, so this is a within-population
comparison and not a comparison of two venues.

## The population and the draw

**E175's committed draw, reused verbatim.** `queries.json` in
`EXPERIMENTS/175-repo-from-report/` records a seeded shuffle
(`SEED = 17520261017`, 200 of 287 free rows, exclusions declared) and E175's
`sample.json` records the ids, the view counts and the question bodies.

Reused rather than redrawn, for two stated reasons: the draw rule and its
corrections are already on the record (F055), so a fresh draw would re-open a
settled bias question for no gain; and every number here is then directly
comparable to E175's 0.1448 and to E168's 0.2843.

**The cost, declared:** these 200 rows are no longer fresh, and E175's session
ran an extractor over their answer bodies to find tracker links. So this
experiment's claims are **conditional** (a difference between two classes of
these rows) and **not** a prevalence estimate on any pool. A fresh draw would
be required for a prevalence claim, and is the named next action if G3 fires.

E177 re-fetches the same ids for the question and answer bodies E175 discarded
(5 requests). Every response is written to `raw/se.jsonl` with its headers, so
the quota cost is auditable.

## Three roles, kept apart on purpose

The record's own failures here are F049 (a judgement re-keyed against the wrong
reference) and D061 (a label tied to no bytes). So no single reader both answers
and grades, and no reader sees the arm label it is being measured on.

| role | sees | never sees | writes |
|---|---|---|---|
| **CLF** | question + accepted answer | any assistant answer | `labels.json` — one row per drawn id: arm, the missing evidence named in free text, its kind |
| **ANS** | the question text only | any accepted answer, any label | `answers.json` — its own answer to each question, no retrieval, no tools |
| **SCORE** | assistant answer + accepted answer | both arm labels | `verdicts.json` — `reached` / `not_reached`, one line of justification |

Order is forced and committed: **`labels.json` is committed before `answers.json`
exists**, and `answers.json` is committed before `verdicts.json` exists. A
later reader can check the ordering from git, not from this file.

## Measurement 1 — the census (automatic, no reader, all 200 rows)

**Evidence gain**: the share of the accepted answer's content tokens that do
not already appear in the question. Tokens are lowercased, `[a-z0-9_+.-]{3,}`,
minus a fixed stopword list of 120 terms written into `census.py` before the
fetch. Reported as a distribution and as `evidence_gain >= 0.5`.

This is a **descriptive** number about lexical overlap, not the arm definition,
and the two must not be confused: a high-gain answer can still be reasoning the
question fully supports. It is reported because it characterises the region even
if G3 does not fire, and because it costs no reader time.

## Measurement 2 — the comparison (the declared claim)

Same treatment, same key, two arms:

```
p_reached = reached / scored        reported per arm with Wilson 95%
gap       = p_reached(SELF) - p_reached(EVID)
test      = Fisher exact, two-sided
```

**Declared bar (G3):** `gap >= 0.25` **and** `Fisher p < 0.05`. Both, declared
together, because E170's record shows what a point estimate clearing a bar
while its interval does not looks like on the page (F134).

**n.** 30 rows per arm. At 30 per arm the gap above is detectable (Fisher
p ≈ 0.0008 at 0.85 against 0.35), but each arm's own rate carries roughly
±0.15 — so **n is chosen for the gap and not for either point estimate**, and
no claim may be made about either arm's absolute level from this run. Rows are
the 30 highest-view-count rows of each arm, taken in the order CLF emitted them,
which is the draw order, so the selection is by arrival and not by anything CLF
saw.

## Controls, declared before measurement

- **G0a — the treatment can discriminate.** Ten questions from this pool that
  are answerable and ten that this record has committed as unanswerable
  (E115's null pair set: the six counting-rule cases and their naive readings,
  which are computable, plus four whose fact pattern is not derivable) —
  actually simpler and cheaper: **G0a is 10 answerable and 10 answerable-only-
  with-the-missing-fact questions drawn from this same pool**, where CLF has
  named the missing fact. `ANS` must answer both. It is a capability check on
  the treatment, and it fails the run if `ANS` reaches more than 7 of the 10
  answerable ones.
- **G0b — SCORE can recover independent real positives.** Five pairs are
  planted that are equivalent by construction and are drawn from **outside** the
  60: each is one row's accepted answer paired with the *same row's* accepted
  answer as returned by a second, independent fetch of the same answer
  (identity after whitespace normalisation), so the positive is a real
  document pair and not a paraphrase this experiment wrote. **SCORE must mark
  5 of 5.**
- **G0c — SCORE can reject independent real negatives.** Five pairs drawn from
  outside the 60: row *i*'s accepted answer against row *j*'s accepted answer,
  *i* ≠ *j*, same arm if possible. **SCORE must mark 0 of 5 as reached.**
- **G0d — the arms are not the same rows twice.** The two arms' question ids
  must be disjoint, and no id may appear in both.

## Kill and ending conditions, declared before measurement

- **K1.** Fewer than 30 rows in either arm after CLF labels all 200 → the
  comparison does not run; report the census and the arm sizes, and name which
  arm is short.
- **K2.** G0a fails → the treatment is not a free general assistant in any useful
  sense; nothing downstream is reported as a measurement.
- **K3.** G0b or G0c fails → SCORE is not a measuring instrument on this
  population; the verdicts are reported as `not_established`, not as a rate.
- **G4 (the constraint's kill).** **G3 does not fire → D107's standing
  constraint is unsupported as stated**, and the candidate-selection rule it
  imposes is withdrawn: a population whose answer is *not* computable from the
  text is no longer the required target, and the next selection rule has to be
  written from what is measured here instead.
- **G5 (the constraint's support).** **G3 fires → the constraint is supported
  on this population at n = 30/arm**, the EVID class is named with its size and
  its composition, and the next experiment is the one that asks *what the
  missing evidence is*, on a fresh draw. **No product is proposed by this
  experiment**; it produces a population and a mechanism question, not a
  candidate.

## Ceilings, declared up front

- **`ANS` is a language model of the same family as this agent, not a human
  reader**, and MISSION.md already says agents are not independent human
  validation. Three blinded roles reduce shared bias; they do not remove it.
- **n = 30 per arm.** Enough for the gap, not for either arm's level.
- **CLF is one reader with no second coder.** Its labels are the arms, so a
  systematic mislabel would be invisible to every control except G0d. The
  census is the check on it, and the census is reported whether or not G3 fires.
- **One venue, one platform, one question shape.** A result is a statement about
  high-arrival answered Stack Overflow questions and about nothing else.
- **Conditional, not prevalence**, because the draw is reused (stated above).
- `ANS` has no retrieval, by design. That is the incumbent D107's six closures
  measured, and it is the only fair comparison to them.
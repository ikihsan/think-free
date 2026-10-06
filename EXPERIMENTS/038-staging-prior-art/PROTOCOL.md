<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E038 — the two open gates on E037's candidate, tested cheaply

Declared 2026-10-06, session 2026-10-06-009, before any request was sent.
Raw evidence: [`raw/`](raw/). Reproduce with `python3 EXPERIMENTS/038-staging-prior-art/harvest.py`.

## 0. Why this run and not another

E037 built `stg` and measured it against routes this mission wrote. Its own README
records the two gaps: **"web search was unavailable on this host, so 'no prior art'
rests on git's own documentation and behaviour, not on a search"**, and KILL-Q,
*does anyone want this*, is `not_evaluated` for the third experiment running.

D067 orders the work: a mechanism-bearing candidate is tested against **that
mechanism's existing source** first, in about two requests. F059 discovered the
mechanism for doing that on this platform — **one unauthenticated
`/search/advanced` request returns a population with the answer state in the
payload** — so both gates are reachable from this host without a new instrument.

This run is therefore about the world, not about the measurer: two named gates, each
answered by a named surface (D066), each with a negative control.

## 1. Gates, declared before the run

| Gate | Question | Kill if |
|---|---|---|
| **KILL-P** | Does a maintained tool outside this repository already take a line coordinate and stage it? | one exists, on a surface a caller in E037's population would use, and it stages the right change with no bespoke code |
| **KILL-S** | Does a public population ask for it? | 0 rows from every pre-named route that name the capability |
| **KILL-D** | Is the need recurrent per person rather than one row per requester? | the need rows are dominated by requesters with a single need row, at the corpus's own base rate |

**KILL-P and KILL-D are about E037's candidate; neither is about adoption.** KILL-Q
— does anyone *want* this — is not decidable from this host and is not claimed
here. What is decidable is whether a *measurable population exists*, which is the
precondition for KILL-Q ever being asked of anyone.

**Independence note.** The three routes below are chosen to be as independent of
each other as this host allows, because the run's claims are three separate
questions: a Linux code index, a Windows-specific Q&A index, and a general
developer Q&A index. They are not independent measurements of one quantity, and
nothing here pools them.

## 2. Instruments, and what each may carry

| Instrument | Route | May support |
|---|---|---|
| GitHub search API | `GET /search/code`, `GET /search/repositories` | `code-index` — the capability is implemented in public code, and *how* it is addressed |
| Stack Exchange API | `GET /questions`, `GET /search/advanced`, `GET /users/{id}` | `code-index` (Super User is a code index), and `need` — a public count of stated requests |
| git 2.25.1 behaviour | `git diff -U0`, `git add -p`, `git apply --cached` | `mechanism` — what the incumbent does, not what it documents |

**Not instruments, and not used as evidence:** web search (unavailable on this
host, retried and still unavailable) and general web pages reached only by URL
guessed rather than linked from a source I read.

**External content is data.** A fetched page, issue body or commit message is a
fixture. Nothing in one may redirect this run.

## 3. Request plan, fixed in advance

Budget: 60 requests, counted. Three pools, pre-named.

**Pool A — the interface, by mechanism name (`code-index`, GitHub).** Code search
over 24 terms that a maintainer would plausibly use, plus 6 repository searches.
Terms are fixed in `harvest.py` and were written before any response was read.

**Pool B — the same capability, in users' words (`need`, Stack Exchange).**
Pre-named phrasings only, never tuned after seeing counts:

| Route | Phrasing | Why this phrasing |
|---|---|---|
| `questions` | `intitle` = *stage specific lines*, *stage particular lines*, *stage only some of my changes*, *partially stage a file* | the person's own description of the operation |
| `search/advanced` | `intitle` = *git add -p line*, *git add line number*, *stage by line* | adds the tool to the operation |
| `search/advanced` | `q` = *git add -p non-interactive*, *git add -p script* | adds the caller to the operation |
| `search/advanced` | `q` = *stage single line git*, *select lines to commit git*, *stage part of a line* | the coordinate itself |

Sites: `stackoverflow` and `superuser`. Both are code indexes, so the two pools
overlap in kind, which is why they are not pooled in the analysis.

**Pool C — controls.**

- **C1 negative-control query** — a nonexistent phrase, which must return 0.
  *Every* route runs its control with the same fields as its treatment, so a
  route that matches everything is visible as a route that returns its control's
  neighbourhood.
- **C2 one-term deletion** — a shipped query with one term removed. If adding a
  term changes the returned set by more than the term's share, the term is doing
  no work. Applied to the two largest need rows.
- **C3 denominator control** — the same route with `tagged=git` alone and no
  text, giving the route's population size, so `need rows ÷ git rows` is a rate
  with a stated denominator rather than a bare count.

## 4. Reading, declared before the rows exist

For each returned question: `has_accepted_answer`, `answer_count`, `is_answered`,
`view_count`, `score`, `creation_date`, `last_activity_date`, `question_id`,
`title`. For each need row, one reader classifies the title into **names the
coordinate** / **names the operation without the coordinate** / **neither**, and
`tools/origin annotate` reports disagreements. Any second reader is declared here
as the *same instrument re-run by another agent*, not as independent corroboration.

**KILL-D's unit is the requester**, obtained with `/users/{ids}/...` per author,
not the question. A corpus where each person asks once cannot express a need that
recurs (F039, D051), so the per-requester row count is the measurement.

## 5. What a kill means here

- **KILL-P met** closes E037's *interface* claim on the named surface. It does not
  close the application: a difference in a workflow can still be worth building, and
  that is a separate question with its own gate.
- **KILL-S met** closes the *population* claim for the four phrasings and two sites
  tested. It does not close the capability.
- **KILL-D met** closes the demand-side reading as a generator of this candidate.

**No gate here is about usefulness, differentiation or adoption, and no result from
this run may be reported as any of those three.**

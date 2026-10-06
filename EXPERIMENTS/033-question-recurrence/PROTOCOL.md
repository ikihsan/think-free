# E033 — protocol: how often does a public question restate another author's question?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Declared 2026-10-06, after a feasibility probe and before any fetch of the declared
population.** Task T-0077. The probe is disclosed in §2 and its sample is excluded from
everything below.

## 1. The question

This mission's most load-bearing negative is a zero. F039 (E019), F042/F049 (E022/E029)
and F051 (E030/E031) each returned **0** cross-author recurring requirements, and E032
returned **0 of 32** candidate pairs on a second venue class. `EXPERIMENTS/032-venue-recurrence/README.md`
pools them: **0 of 132 adjudicated candidate pairs, upper bound 0.0223**. Item 0d closes
three demand-side generators on the strength of that number.

Every one of those measurements worked the same way: draw a small sample of text, ask a
reader whether two clauses state the same requirement, and count. E032's own declared
ceiling names the mechanism — *"two people needing the same capability twice must both
land in the sample"*, on 28 clauses from 60 questions — and E032's population was drawn
`sort=votes`, which prefers questions that were **answered** rather than closed as
repeats.

**This experiment changes the measurement, not the belief's direction.** It asks what
fraction of public long-form questions restates a question *another distinct author
already asked*, and it reads that off **Stack Exchange's own duplicate-closure
judgement** rather than off this mission's linkage rule and reader. `closed_reason ==
"Duplicate"` is a judgement made by other people, on the platform, at scale — the one
recurrence signal available here that no instrument of this repository produced.

| | what the record has | E033 |
|---|---|---|
| population | 60–1401 *items* per run | **1000 questions**, a declared consecutive run of the creation order |
| recurrence label | shared-token linkage → reader | **the platform's duplicate closure** |
| power | both members must land in a small sample | **no pair has to co-occur** |
| selection | trigger vocabulary, or `sort=votes` | **date window and creation order only** |

The venue class is deliberately *the same one E032 used* — non-programming Stack Exchange
— so the comparison is about population and label, not about topic.

## 2. The probe, disclosed

Two feasibility probes ran against the API before this file existed, both on
`site=cooking`, `sort=creation`, `filter=withbody`, 100 questions, window
2025-05-28…2025-06-15, plus single-question `related` lookups on four of the duplicate
closures found there. **That sample is excluded from the population below**, its window
does not overlap the declared one, and **no number from it is used as evidence**. What it
established, and what it cost:

- the API serves `closed_reason`, and `Duplicate` is one of its literal values;
- `closed_details` (which names the canonical question) and `question_type` (which marks
  a related row as the duplicate) are **not exposed** by API v2.3 — `filters/create`
  returns 392 available fields and neither is among them. Recorded in [`API.md`](API.md).
- `questions/{ids}/related` **404s on a vectorised id list**, so one canonical costs one
  request;
- unauthenticated `quota_max` is **300 per IP per day**;
- the probe's 12 duplicate closures of 100 are the reason `closed_reason` was chosen as
  the label. That is a pilot-informed choice and is recorded as one.

## 3. Population, declared before the fetch

1. **Sites:** the first **two** of `cooking`, `outdoors`, `home-improvement`, `travel`,
   `math` that yield at least 500 questions inside the window. The order is fixed here so
   the site cannot be chosen on its answer rate.
2. **Window:** `fromdate` 2024-06-01T00:00:00Z, `todate` 2024-07-01T00:00:00Z,
   `sort=creation`, `order=desc`, `pagesize=100`, pages 1–5 per site, `filter=withbody`.
   The last 500 questions created before 2024-07-01. Six months of closure history have
   accrued by the date of this file; **that lag biases the rate downwards**, which is the
   safe direction for B1.
3. **Every question in the sample is in the population.** No length filter, no
   readability filter, no author filter. E032 filtered to 40–600 words because it needed
   extractable clauses; this run measures a closure, and a filter would only reduce power.
4. **No requirement vocabulary appears in the selection** — F043's constraint, in force.

### AMENDMENT-1, made after the first harvest attempt and before any duplicate count was computed

The declared site rule was executed as written and **yielded one qualifying site**, so the
declared population was not reachable. What happened, in full:

| site | outcome |
|---|---|
| `cooking` | 50 questions in the whole declared month |
| `outdoors` | 9 questions in the whole declared month |
| `home-improvement` | **HTTP 400** — the identifier in §3 is not a valid API site parameter |
| `travel` | 185 questions in the declared month |
| `math` | 500 questions (5 pages) — the only site meeting the declared floor |

`raw/fetch_log.jsonl` and the aborted `raw/harvest.jsonl` from that attempt are committed,
and **no rate, distribution or closure count was computed from it**. The figures above are
row counts per site, which the harvest printed to choose the next site — the one quantity
the declared rule was permitted to look at.

Amendment, declared before the amendment's fetch:

1. **Sites:** the sites in the order `travel`, `math`, `cooking`, `outdoors` that yield
   **≥ 400** questions inside the window, **500 questions per site, at most 3 sites**. The
   floor of 400 is a power requirement; the cap of 3 is the quota budget. `home-improvement`
   is removed, having been shown not to be an API site identifier.
2. **Window widened** to 2024-01-01T00:00:00Z … 2024-07-01T00:00:00Z. With `pagesize=100`
   and 5 pages the cost is unchanged at 5 requests per site; the window only decides *which*
   500, and the 500 most recent inside a six-month window are the least closure-starved
   questions available in that window.
3. **Everything else stands**, including the labels, the gates, the kill direction and the
   mechanism arm. The population is **not** E032's: E032's three sites yield 50, 9 and an
   unreported third inside any window this run can afford, so the comparison to E032 is a
   comparison of **rates**, not of the same questions. Recorded as a ceiling in §10.

### AMENDMENT-2, made after the edge resolution and before any adjudication

The declared mechanism arm (§6) needs *q*, the share of a duplicate's canonical that falls
inside the sample, and §7's only route to a canonical is `/questions/{id}/related`, which
returned 200 for all 40 edges — but the vectorised id list this protocol's cross-check
depends on returns `400 {"error_id":404,"error_name":"no_method"}` on this API revision,
so **the cross-check cannot be run as declared**. Recorded in [`API.md`](API.md).

If that makes the canonical unreadable, the mechanism arm loses its input, so one addition
is declared now, computed **only from bytes already committed**:

**D7 — the counterfactual draw.** From this population, take the **60 highest-scored
questions**, which is what E032's `sort=votes` selection drew, and count how many are
duplicate-closed. Repeating over every 60-question window of the score-sorted population
gives the distribution the record's zero actually sat inside. It needs no canonical and no
reader, so it cannot be voided by A3.

**D8 — canonical co-occurrence.** The share of resolved canonicals that are themselves in
the population. Reported **only if A3 passes**; otherwise `not_evaluated` with the count
stated but not interpreted, because a count of wrong canonicals is not a count of anything.

### AMENDMENT-3, made after the run, recording two statements this protocol got wrong

Written after `tally.py` and after both readers had reported, so it cannot have influenced
either. It corrects the record rather than the result, and the second correction
**withdraws a conclusion the run had been carrying**.

**1. AMENDMENT-1's rationale was false.** It claimed the widened window made the sample
"the least closure-starved questions available in that window". It did the opposite. With
`sort=creation` paired with `order=desc`, "the 500 questions inside the window" means the
500 **newest**, so the population is not spread across the six months at all: `math` is
**four days** of questions (2024-06-27…06-30) and `travel` is ~90 days with a median
creation date of 2024-05-21. The *bias direction* is unaffected and if anything stronger,
because the observation date is 2026-10-06 and the measured closure lag is **median 0.3
days, max 64.3 days** — every row had 26 months to be closed. The headline rate is
therefore still a lower bound on recurrence, but for a different reason than AMENDMENT-1
gave, and the population is far narrower in time than the protocol describes.

**2. D9 is confounded and its conclusion is withdrawn.** The run reported that a repeat is
2.6× more likely to go unanswered (0.5556 against 0.2114). **Zero of the 54 duplicate
closures has an accepted answer**, and closing a question as a duplicate does not answer
it, so most of that gap is mechanical. It cannot be read as evidence that convergent
questions go unmet. The weaker form that survives: duplicates were **older** than the rest
(median 7.9 days old at the window edge against 3.3) and still carried no answer of their
own — but closure mechanics explain that too, so D9 decides nothing on its own and is
reported as a description, not a finding.

## 4. The label, declared before the fetch

- **Positive:** `closed_reason` is exactly `"Duplicate"`.
- **Negative:** any other `closed_reason` string, or the field absent (the question is
  not closed). The **full distribution of `closed_reason` values is printed**, so the
  positive cannot be read as a residual.
- A question whose closure reason is `Duplicate` is, by the platform's judgement, a
  question another author had already asked. **This is a lower bound on cross-author
  recurrence**: a repeat that was answered, or that nobody noticed, is not labelled.
- **The label is the mission's evidence, not the reader's.** The reader arm below does
  not decide which questions are duplicates; it checks whether the API's guess at the
  canonical is recognisably the same question, and separately whether this mission's own
  reader can see recurrence that the platform sees.

## 5. Gates, declared before the fetch

| gate | rule | fails ⇒ |
|---|---|---|
| **A1** | ≥ 95% of fetches HTTP 200; every row carries a `closed_reason` value from the API's own vocabulary or the field's documented absence; the distribution is printed | `not_evaluated` |
| **A2** | the in-sample visibility calculation (§6) is computable and its inputs are measured, not assumed | `not_evaluated` |
| **A3** | canonical resolution: ≥ 30 of 40 resolved edges read as the same question, and canonical author ≠ duplicate author on ≥ 30 of 40 | edges `not_evaluated`; D3/D4 are not reported |
| **A4** | reader κ ≥ 0.6 over the double-read rows. **κ undefined ⇒ `not_evaluated`** (E032's first defect) | `not_evaluated` |
| **A5** | the unrelated-pair arm reads `same` for ≤ 0.20 of its rows | `not_evaluated` |
| **B1 fires** | the duplicate rate's Wilson **CI95 lower bound > 0.0223** | the record's pooled bound is refuted |
| **B2 fires** | the duplicate rate's Wilson **CI95 upper bound ≤ 0.0223** | the record's pooled bound stands |

B1 and B2 are exhaustive over a CI that is not degenerate, and the direction of the bias
is fixed above: if anything is undercounted, B1 fires more easily, so B1 firing is the
conservative reading.

## 6. The mechanism arm, and why it can fail

**Sampling cannot explain the record's zeros.** From the measured rate *p* and the
measured share *q* of resolved canonicals that fall inside the sample, the expected number
of **visible in-sample** recurrence edges in a draw of *n* questions is

    E[n] = n · p · q

with *n* = 60 (E032's population) and *n* = 100 (E031's). If **E[60] < 1**, a 60-question
draw usually contains no pair at all, and E032's 0 of 32 is what this rate looks like from
inside a small sample — the zero would be a fact about the sample, not about public text.
If **E[60] ≥ 1**, sampling is not the explanation and the record's zero needs another one;
that is a real possibility and is not wished away here.

**E032's selection is a second, independent power loss, and it is measured, not argued.**
The rate is reported by score tertile (D6): `sort=votes` draws from the top tertile, so if
the bottom tertile's rate is materially higher, the record's population was selected
*against* the signal as well as being too small.

## 7. Arms and readers

**Canonical resolution (A3).** For the **first 20 duplicate closures per site in file
order**, call `/questions/{id}/related` and take its **top-ranked** row as the API's guess
at the canonical. Record the row's id, author, score, `answer_count`, `is_answered` and
`accepted_answer_id`. The canonical's own metadata is then fetched in one batched
`/questions/{ids}` call (≤ 100 ids), which is cheap.

**Reader sheet.** One blinded sheet, 48 rows, built after resolution and hashed; every
reader is handed the sheet's **sha256** before it reads anything, and the key file is
written **in the sheet's order** (E032's second defect).

- **24 edge rows**: a resolved duplicate and its guessed canonical, read as *"do these
  two questions ask for the same thing?"* → `same` / `not same` / `unclear`.
- **24 unrelated rows**: pairs drawn from **different sites**, never within a resolved
  cluster, matched on title length. This is the blind control (A5) and it is drawn from
  the same population through the same code path.

Two readers, blind to arm, author, site, score and each other. Row identity is checked **by
order** against the key file, never by key set (D061, from F049).

**κ is computed on the double-read rows and is `not_evaluated` when undefined.** No
`unclear` is silently folded into `not same`.

## 8. Descriptive outputs, declared, no gates

| | |
|---|---|
| **D1** | duplicate rate per site and pooled, Wilson CI95 |
| **D2** | the complete `closed_reason` distribution |
| **D3** | over resolved edges: canonical-in-population share, distinct-author clusters, canonical `answer_count` and `accepted_answer_id` |
| **D4** | E[n] for n = 60 and n = 100 (§6) with its two measured inputs |
| **D5** | word-length distribution, so the contrast with E032's 40–600 word filter is explicit |
| **D6** | duplicate rate by score tertile |
| **D9** | the share with `answer_count == 0` in the duplicate arm against every other closure arm, with the interval of the difference — **added after the harvest, before any reader saw a sheet, and labelled as post-hoc**: it uses the label, not the reader, so it cannot be moved by adjudication, but it was not in the declared table. **Withdrawn as a finding by AMENDMENT-3 §2: zero of the 54 has an accepted answer, so the gap is substantially mechanical** |

## 9. What each outcome decides, written before the run

- **B1 fires.** The pooled 0.0223 bound is a statement about two small samples, not about
  public text. Item 0d's third closure is withdrawn as an artefact of sample size, and the
  demand-side generator re-opens **with a declared requirement**: measure recurrence on a
  whole population, and read the recurrence relation from the platform rather than from a
  linkage rule this repository invented. Nothing is revived — a recurring question is not a
  candidate, and this run screens nothing.
- **B2 fires.** The record's negative is among the best-supported facts here, and the
  sampling defence is withdrawn. Item 0d's closure stands on a measured rate rather than on
  a count of small samples.
- **A3 fails.** The platform's duplicate closure is usable as a **rate** and unusable as an
  **edge set**, which is itself a result about the API and is recorded as such. D1, D2, D4,
  D5, D6 stand; D3 does not.
- **Any other A-gate fails.** `not_evaluated`. No claim in either direction, nothing else in
  this repository moves.

## 10. Ceilings, declared now

- **Two or three sites of 2024, English, chosen by question volume** (AMENDMENT-1), not by
  anything about their duplicate rate. A rate is a rate for that population; nothing
  licenses a claim about any other community, or about Hacker News, which is where all five
  of the record's zeros came from.
- **The population is not E032's.** E032's sites cannot supply 500 questions inside a
  window this run can afford, so the contrast between the two runs is between rates
  measured by different instruments on different questions.
- **The rate is a lower bound** on recurrence (§4), by an unknown amount.
- **A3's canonical is a guess.** `related` returns related questions; the top row is not
  guaranteed to be the closure's target, and the API does not name the target (§2). A3
  exists because of exactly this.
- **40 resolved edges** is a small population for D3 and D4's *q*; both are reported with
  their own counts and are not verdicts.
- **Anonymity.** No `closed_details`, no registered filter, 300 requests/day/IP. The run is
  budgeted for 51.

## 11. Reproduction

    python3 harvest.py       # 10 fetches; raw/harvest.jsonl + raw/fetch_log.jsonl
    python3 resolve.py       # 40 + 1 fetches; raw/edges.jsonl + raw/canonicals.jsonl
    python3 sheet.py         # blinded 48-row sheet + key file + MANIFEST.json
    python3 tally.py --check # re-derives every number in README.md from committed bytes
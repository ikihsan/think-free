# E034 — protocol: are re-asked questions in the score tail, and is that different per tag?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Declared 2026-10-06, after a feasibility probe (§2) and before any fetch of the
declared population.** Task T-0078. The probe is disclosed in §2, its sample is
excluded from §3, and the tag it touched is replaced rather than kept.

## 1. The question

F055 measured, on one volume-selected whole-site sample of 1000 questions, that
duplicate closure is **4.5× rarer in the top score tertile than the bottom**
(0.0180 against 0.0808) and that the **top 60 by score contains 0** duplicate
closures. That is a fact about one population, drawn `sort=creation`, pooled
across all tags. Two things it does not say, and both are what a tool would need:

1. **It does not say the gradient holds inside a tag.** Pooling across tags can
   produce a gradient from tag composition alone.
2. **It does not say the rate differs between tags.** Without that, "sample the
   tail" is a one-line methodological note, not a thing a person can act on.
   A docs owner, a support lead or a tag wiki editor needs to know *which* tag.

**The practical difficulty this names.** Every surface a person uses to find
questions — a search result, a tag page, the `Active` tab — presents a
score-ordered or activity-ordered feed. Questions that were closed as duplicates
are exactly the ones that sank: nobody voted them up, and closing them ended their
activity. So the questions that record *this question was asked before and the
answer was not found* are, by construction, the ones the ranked feed is worst at
showing. The evidence that they exist and where they sit is F055's; nobody has
measured whether they cluster by topic, which is what would make them usable.

## 2. The probe, disclosed

Before this file existed, in session 2026-10-06-003:

| probe | result |
|---|---|
| `GET /questions?site=travel&tagged=visas&sort=votes&order=asc` | 200, 25 rows, scores −7…−4, `closed_reason` absent on all 25 |
| the same with `order=desc` | 200, 25 rows, scores 167…57, `closed_reason` absent on all 25 |
| `travel.stackexchange.com/questions/189910`, browser UA | **403**, 5676 bytes, Cloudflare `Just a moment…` challenge |
| `stackoverflow.com/questions/189910`, browser UA | **403**, 5647 bytes, same |
| `stackprinter.appspot.com` × 3 and `www.stackprinter.com` × 1 | **200**, 1213 bytes each, `The StackExchange server is too busy at the moment` |
| `data.stackexchange.com/StackOverflow/query/new` and a saved query | **403** × 2, Cloudflare |
| `GET /questions/{id}/comments?filter=withbody` on three duplicate closures | 200; **0**, 3 and 0 rows; one human comment linked another SE question, **no system comment naming a canonical** |
| `GET /questions/{id}/answers` with the default filter on two of them | 200; **no `closed_details` field on any answer** |

**What the probe establishes.** The route this experiment needs works, and one
request buys 25 rows. **It also answers the question E033 left open** — *what to
measure recurrence on* — by closing its other half: a duplicate closure is a
reliable label and an **unreachable edge**. E033 tried four vectorised `{ids}`
routes, the question page, and StackPrinter. This adds the question's **comments**
(the system "already has an answer here" banner is not in them), the **answer's
`closed_details`**, a browser User-Agent, both StackPrinter hosts, and the **SEDE
archive**; all six fail. The canonical is not reachable from this host, and E034
therefore never needs it: the label alone carries every gate below.

**What the probe must not be allowed to do.** It revealed that `travel`/`visas`
has **0 duplicate closures in 25 tail rows and 0 in 25 head rows**. `visas` is
therefore **dropped from the declared population and replaced by `customs`**,
which had not been touched. §3's tag list is fixed with that replacement already
made, so no tag's population was chosen with its outcome in hand.

## 3. The population, declared

Eight tags on two sites, **two per a-priori stratum**, every tag named before any
fetch. The strata are a hypothesis about *why* answers are findable or not: a tag
with one obvious canonical answer should be findable, a tag whose questions are
specific to a situation should not.

| stratum | reading | tag A | tag B |
|---|---|---|---|
| S1 | one canonical answer exists | `stackoverflow`/`git` | `stackoverflow`/`regex` |
| S2 | generalist programming | `stackoverflow`/`python` | `stackoverflow`/`docker` |
| S3 | specific to a situation | `stackoverflow`/`excel-formula` | `travel`/`customs` |
| S4 | textbook | `math`/`linear-algebra` | `math`/`probability` |

**Three arms, same route, same filter, same page budget** — `GET /2.3/questions`,
`pagesize=25`, `order=desc` unless stated, 4 pages per arm:

| arm | route parameters | what it is |
|---|---|---|
| `tail` | `sort=votes&order=**asc**` | the bottom of the score distribution |
| `head` | `sort=votes&order=desc` | the top — what E032's `sort=votes` drew |
| `default` | `sort=activity&order=desc` | **the `Active` tab, the strongest accessible alternative**: what a person browsing the tag actually sees |

Every request is logged with its URL, HTTP status, `quota_remaining`, `has_more`
and the sha256 of the response bytes. A page that stops early is recorded, and
`n` is always the **fetched row count**, never the page budget.

## 4. What is measured

The label is Stack Exchange's own, on one field, with no missing-value imputation:
`closed_reason == "Duplicate"`.

- **D1** duplicate-closure rate per arm per tag, Wilson CI95.
- **D2** the same pooled over all eight tags, and pooled again **matched-n** (each
  arm truncated to the smallest per-tag arm) so unequal `n` cannot drive D3.
- **D3** the score range each arm realized, so "tail" and "head" are checkable
  against the bytes rather than against the route's promise.
- **D4** among duplicate closures, the share with `is_accepted == false`, per arm,
  with CI95. This is the mechanism the tool claims to expose: a repeat that is
  closed and then never answered records that the answer existed and was not found.
- **D5** the **edge-reachability verdict**: which channels were consulted for the
  canonical and what each returned, so a reader knows what an absence means.

## 5. Gates, declared before the run

| gate | rule | fires when |
|---|---|---|
| **A1** | ≥95% of declared requests return 200 with an `items` array, and **100%** of rows carry the `closed_reason` key (present-or-absent recorded, never imputed) | otherwise the population is not the declared one |
| **A2** | ≥3 of 8 tags have ≥1 duplicate closure in the `tail` arm | otherwise the design is **`not_evaluated`**: no positive examples exist, and no rate in §4 can be compared to anything |
| **A3a** | pooled `tail` CI95 **lower** > pooled `default` CI95 **upper** | **fails** if they overlap — the practical claim is that the ranked feed misses these |
| **A3b** | pooled `tail` CI95 **lower** > pooled `head` CI95 **upper**, and the same on matched-n | **fails** if either overlaps — this is F055's gradient, replicated on an independent tag-stratified population |
| **A4** | two tags with `tail` n ≥ 50 whose `tail` duplicate-rate CI95s are **disjoint** | **fails** otherwise — **this is the kill gate for the application** |
| **B1** | `tail` and `default` share of duplicate closures with `is_accepted == false` are compared by Newcombe CI95 | reported; labelled **`inferred`** unless the interval excludes 0 |

**A4 is the gate that can kill the candidate.** If every tag's rate is
statistically indistinguishable, "sample the tail" is true and useless, and the
tool's differentiating output — *which* tag needs attention — has no measured
basis. The candidate dies and the reason is recorded; A3 passing would not save it.

**A3b failing does not kill the candidate and A3a passing does not rescue it.**
A3b is a replication of a number this mission already published; A4 is the only
gate that tests the thing being proposed.

## 6. Kill, narrow, or continue

- **A4 fires** → build the reader. Next: does the *content* of the repeats cluster
  into a usable clause set, which is the question four earlier demand-side
  generators could not answer. Narrowed to one site and the tag set that fires.
- **A4 fails, A3 fires** → the tool is not a per-tag diagnostic. It collapses to a
  sampling recommendation, which belongs in a methodology note, not a repository.
  Record and stop.
- **A3a and A3b both fail** → the gradient was an artefact of E033's population.
  Record; this closes the reading F055 opened on an independent sample.
- **A2 fails** → `not_evaluated`, not a negative result. The label is not dense
  enough at this page budget in these tags; that is a resource statement.

## 7. AMENDMENT-1 — out-of-sample replication of the two tags that decide A4

**Declared after the run of §3 and before the §7-arm fetch.** A4 fired on a
per-tag spread, and the highest tag — `travel`/`customs`, 43 of 100 — is also the
**only tag drawn from the `travel` site**. Site and tag are therefore confounded,
and the obvious alternative to "this tag has questions people re-ask" is "this
community closes aggressively". That alternative is not a subtlety: Stack Exchange
duplicate closure is a moderator act, so a community's moderation policy is a
first-class explanation of the rate and E034 cannot see it.

Two arms, fetched after the declared population and kept in it:

| arm | what | rule |
|---|---|---|
| **R1** | the **next four pages** of the `tail` arm for the two tags that decide A4 (`customs`, `excel-formula`) | a rate that holds on pages 5–8 is a rate in a second sample. The paginated ordering is not perfectly stable across the page boundary, so overlapping ids are removed and the count reported |
| **R2** | the `tail` arm for **one further tag on each of the two sites whose single existing tag decided A4** | this is the confound test, and it is a declared gate |

R2's tags, fixed here before the fetch and not chosen by looking at any rate:
`travel`/**`baggage`** — the mundane, high-volume tag on the site that produced the
highest rate, chosen as the S3 exemplar's neighbour rather than as another
situational tag — and `math`/**`calculus`** — a second textbook tag on the site
that produced the lowest-but-one rate. The rule is *a second tag on each of those
two sites, matched to the a-priori stratum of the extreme it is testing*, so the
choice does not depend on an outcome.

| gate | rule | reading |
|---|---|---|
| **R2-tag** | `travel`/`baggage`'s tail CI95 is **disjoint** from both `math` tags' | the spread is a property of the **tag**; the site hypothesis is not supported |
| **R2-site** | `travel`/`baggage`'s tail CI95 **overlaps** a `math` tag's | the spread tracks the **site**; A4 survives as a fact about the numbers and the per-tag reading is withdrawn |

**R2-site firing would not be a null result for the population** — the pooled
gradient (A3) is unaffected by which of the two explanations holds. It would kill
only the *per-tag diagnostic*, which is the thing the application is for, and
§6's first branch would then collapse to the second.

## 7a. AMENDMENT-2 — the R2 gate above is ill-formed, and this note is written after the run

`baggage`'s tail CI95 came back **[0.1305, 0.2886]**: disjoint from `probability`
[0.0055, 0.0700] and `linear-algebra` [0.0215, 0.1118], **overlapping `calculus`
[0.0564, 0.1777]**. §7's two branches were therefore **both true** — R2-tag's *both* and
R2-site's *a* — so the gate as declared could not return one answer, and neither branch is
reported as having fired.

**§7 is left exactly as declared above, because it was declared before the fetch and that
is the whole point of declaring it.** This note records that the defect is in the gate's
form, not in the data, and names the amendment made in the same session as §7 declared the
alternative: the unambiguous statistic is **how often two tags on the same site separate at
all** — `tally.py`'s **D6** — which is a count over the whole relation rather than a
predicate about one candidate against a chosen subset of comparators.

The governing decision is **D064**, and its scope is this: **a gate about how one
candidate relates to several others is an exclusive partition or a statistic over the
relation, never a conjunction over a subset of comparators.** D062 already requires a
*linkage rule* to be shown capable of firing; D064 requires the *decision rule applied to
a relation between candidates* to be capable of returning one answer. The two failures are
mirror images — D062's rule could not fire, this one could fire twice.

## 8. Ceilings, declared before the run

- One platform, and its duplicate closure is a **moderator-adjudicated** judgement,
  not a mechanical match, so the rate is a property of a community's practice.
- Two sites of one network, eight tags chosen by a declared a-priori rule and not
  sampled; the spread across *other* vocabularies is unmeasured.
- 4 pages per arm caps each arm at 100 rows and the deepest-scoring slice of a
  popular tag; `tail` is therefore mostly negative scores, a stratum E033's low
  tertile (median 1) did not reach. **D3 is what a reader checks this against.**
- Unauthenticated quota is 300 requests/IP/day and this run needs 96; §2's probes
  spent 12.
- `is_accepted == false` is what closure does to a duplicate as often as what the
  asker needed. D4 is **not** evidence that anyone was left without an answer, and
  E033 already recorded the shape of that error (AMENDMENT-3 §2).

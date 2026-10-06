<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# In flight, part 3 — E034's own run

Split out of [`STATE-in-flight-2.md`](STATE-in-flight-2.md) at its 300-line cap on
2026-10-06, by content rather than by size: E034 is one experiment's full reading and its
successor's section reads as its correction. **Identifiers are stable across the parts.**
Read a finding number and go to the file it is defined in.

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

## The score-tail backlog is confirmed, unreachable, and not a rescue (F058, D065)

**Status: E035's frame and its declared branch both re-scoped; the candidate is neither
established nor killed.** Item 0f. `EXPERIMENTS/035-unanswered-surface/`,
`observed` 2026-10-06. Four reads over E034's committed bytes, zero quota cost.

**Four findings, in the order they changed the decision.**

1. **The population is not one that was overlooked.** Within E034's tail arm the
   duplicate-closed rows have a **higher** median view count than their non-duplicate
   neighbours — **251 against 193**, means 1612 against 906 — and the arm's median age is
   **8.49 yr** against `Active`'s 5.53. E034 §1 motivated the candidate on *"the answer
   existed and was not found"*; that is **falsified as a findability failure**. What exists
   is an eight-year-old backlog with a measured duplicate rate, which is a different product
   aimed at a different user.
2. **The two arms are not two densities of one population.** For two of eight tags they do
   not intersect: `stackoverflow`/`python` tail −34…−11 against `Active` −9…304;
   `math`/`probability` −9…−4 against −2…159. The 4.5× reads much more usefully as a
   statement about **membership**.
3. **No rendered Stack Overflow tag page offers the ordering (corrected by F059: the API route does).** With the site itself behind a Cloudflare
   challenge from this host on every path, a 2026-09-26 archive snapshot of a real tag page
   was read: **409,639 bytes** of first-party rendered HTML whose tab bar offers `Newest ·
   Active · Votes · Frequent · Trending · Bounties · Unanswered` and which contains **0**
   occurrences of `oldest`, `order=asc`, `sort=votes&order=asc` or `ascending`.
   `not_measured`: the direction of `tab=Votes`.
4. **D6's remedy was aimed at the wrong constraint.** Between-tag excess variance on the
   arcsine scale is **+0.0417** pooled and **+0.0420 within `stackoverflow` alone**, whose
   four tags read 0.000 / 0.130 / 0.150 / 0.210. Tag variance is already reproducible
   without a site, so "three to four more tags per site, ~30 requests" — which item 0e
   ranked the mission's top action — was not the binding constraint. The objection that a
   rank-selected tail is a non-comparable stratum is **unsupported** (r = +0.2485, t = 0.725,
   df = 8, `not_established`).

**What E035's own gates did.** `/questions/unanswered`, behind `tab=Unanswered` and the
strongest accessible alternative, **excludes the population by definition**: **0** of
E034's 224 known duplicate-closed ids appear in its 2050 rows, while **98 of 186** tail
duplicates meet the route's advertised `is_answered == false` criterion and are still
absent. The overlap gate **fired at 0.0283** and its firing was definitional — which is
**D065**, and the branch §6 attached to it is therefore **not taken**. **U2 is
`not_evaluated`, not zero**: `closed_reason` is unreadable *on that route* (six filter
forms, custom filters refused unauthenticated, `/questions/{ids}` omits it too), so the
density comparison needs an API key **— and F059 shows `/search/advanced`'s default
filter carries it without one, so this is a per-route fact and not a platform one.**
Quota ended at 19 of a shared 300.

**The transferable rule, and the one this section earns.** **Before spending a declared
remedy on a population, check the committed bytes for whether its premise is still the
binding one.** Reachability, commensurability, aim and the obvious objection — four
questions, zero requests — reordered this mission's top item. The opposite is the standing
risk: three consecutive sessions on one platform, and this one spent most of its budget
discovering the label was unreadable on the route that mattered.

**Ceiling.** One platform; duplicate closure is a moderator act; `customs` at 0.4650 and
`excel-formula` at 0.0000 are single cells; **whether anyone wants the backlog surfaced is
entirely unmeasured**, and that is the whole adoption question.

## The mechanism was a public query the whole time (F059, D066, D067)

**Status: the candidate is closed, the measurement stands, and the order of work
changed.** `EXPERIMENTS/036-search-backlog/`, T-0080, 8 requests. Verdict
`platform_enumerates_the_tail`, **KILL-R met**, `candidate_status:
mechanism_killed_no_build`.

**The finding, in one request's worth of bytes.**

```
/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100
```

100 questions, ordered **−20 … −5, non-decreasing**; **81 are ids already in E034's
committed harvest**, the first at **rank 1**; **48 rows carry `closed_reason`** and **13
of those are `Duplicate` or `exact duplicate`**. Unauthenticated, default filter, no
computation. E035 named the differentiator as *"the platform's own closure label over a
population no surface orders that way"*, and **both halves are the platform's**.
`readout.py` prints the URL and the 13 rows — it is a URL, not an algorithm, and deeper
pages need `page=2`, a documented parameter (`inferred`, not fetched).

**Why the three experiments before it read it the other way.** They enumerated one
**rendered** interface. The platform also ships a documented filter vocabulary —
`sort`, `order`, `tagged`, `closed`, `votes`, `answers`, `accepted`, `body`, `title`,
`user`, `url`, `created`, `updated` — and **two of those are an ordering**. F058 was a
correct reading of 409,639 bytes of a tag page and was used as a statement about the
platform; that gap is **D066**. E035's *"the label needs an API key"* came from two
routes and generalised to the platform, and `/search/advanced`'s default filter carries
it — **F020's shape, in the mission's own instrument.**

**The instrument's own controls, and one that mattered.** `order` is validated
(`order=descending` → 400 `order`), `filter` is validated (400 `Invalid filter
specified`), and **`closed` is not**: `closed=maybe` returns 200 with `closed=yes`'s
first three items. So a closed-only control was never establishable from this route's
behaviour, and gate **R0** existed only to settle it — it showed the closed tail returns
with **no `closed` parameter at all**.

**Retrieval, thin.** Tail titles 3 of 4 (ranks 1, 7, 1; one absent past 100), `Active`
control 2 of 2 (both rank 1). **The positive control fired on real positive examples**,
which is the check this record has needed seven times. **KILL-Q is `not_evaluated`** — the
rule is not decidable at n=4 against n=2 — and the negative control was **refused by the
quota window**, so a nonzero rate rests on the positive control alone.

**The run failed twice in its own plumbing, and both are in the raw bytes.** A stage
argument fell through to a nine-request plan against a four-request budget, so three
requests were refused; and `quota_wall()` discarded successful 200s reporting negative
quota, which zeroed R3's apparent rate until it was fixed. **The kill rests on neither**,
being an id-intersection against committed evidence. The retrieval arms do need controls,
and they are thin.

**What this changes beyond the line.** F055, F058 and F059 are one shape three times over:
a fact about the instrument's own selection, read *after* the measurement. **D067** now
orders the work — a mechanism-bearing candidate faces **its mechanism's existing source**
first, in about two requests, before any population is measured for it. Three experiments
and 1125 rows described a population whose mechanism was a documented query. **The
adoption question is now the whole question, and three experiments never measured it.**

**Ceiling.** The rendered site is Cloudflare-blocked from this host, so whether the **web
UI** exposes this against the API is `not_measured` — a browser or user question, not
another request. **R1 is unexplained**: `tagged=customs&closed=yes&sort=votes&order=asc`
on `travel` returned 200 with **0 items** while the same construction worked on
`stackoverflow`. One page fetched, so depth is `inferred`.

## Moved out of STATE.md on 2026-10-06 — closed readings, kept whole

`STATE.md` hit the 300-line cap again on adding E036, and this is the same repair the cap
has required thirteen times: **material moved to the file whose invariant owns it, and
nothing shortened.** Both blocks below were already labelled "pointers only" in
`STATE.md`; they are now the pointers' own text, here, next to E034–E036.

**Five closed readings, kept here as pointers only — each one's full text is in the file
named, and none of them changes what is next.** (i) **F037's reconciliation for the supply
question is withdrawn:** the copies are adapted, not duplicated, so near-zero install
readings are not an invisible channel (F040, `EXPERIMENTS/020`); drift is `inconclusive`.
(ii) **F049 followed the 1250 need-starters forward**: of the 241 with a public `Show HN`
item, **167 shipped before they stated the need** and only 74 after, and the reader arm is
`not_evaluated` (κ = 0.5004), so the need-to-build link bounds at **[−0.0156, +0.1125]**
— F042's 0-of-24 is confirmed on a 10× larger instrument. (iii) **The candidate generator
was refuted**: 1401 harvested need statements, 50 drawn by rule, **0 survived**, and its
strongest cluster collapsed ~200× (F029, F033). (iv) **The prior-art screen measured on
coverage**: 6 of 6 positive controls recovered, 3 of 12 adjudicable kills have no prior art,
and **corpus carriage is the result** — GitHub's index carried every verdict the code corpora
carried (F035, F036, D050). (v) **Its population came out against it**: 14 of 18 young
rows are executable code, documents carry a median 6,072 stars against 566, and the most
-starred tool there is installed 363 times a month (F037). Readings in
[`STATE-in-flight-2.md`](STATE-in-flight-2.md) and
[`STATE-in-flight.md`](STATE-in-flight.md).

**Four closed tooling findings, kept as pointers because they are the standing reasons a
session's own gate can be green and its records still false.** A restated experiment number
was false and the obvious gate is blind to it (defect 22, T-0056, D047, F024);
identifier collisions between two VMs are closed (T-0030, T-0031) but **the work-collision
case still has no detector**, so read the remote task list first
([`docs/reference/identifier-allocation.md`](docs/reference/identifier-allocation.md)); a
gate belongs in the one command the protocol tells every agent to run (T-0045); and a test
can read a clock the code does not (defect 15, T-0044). Accounts:
[`STATE-defects.md`](STATE-defects.md),
[`docs/operations/ci-diagnosis.md`](docs/operations/ci-diagnosis.md). **One rule survives:**
rebase a moving base with `origin sync land`, because a hand-run rebase records nothing and
its paths are then attributed to whoever holds the tree (T-0053; sessions 040 and 012 hit
that ceiling seven and twice).

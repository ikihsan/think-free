<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E036 — does Stack Overflow's own search return the score-tail backlog?

Task T-0080. Protocol written before the second measurement request; one reachability
probe (recorded in §1) preceded it and is reported as such, not folded into the result.
Labels per [`docs/policy/evidence-labels.md`](../../docs/policy/evidence-labels.md).

## 0. The question

E034 measured a population: questions in the **lowest score band** of a tag, at
**4.5×** the duplicate-closure rate of the `Active` tab. E035 established that
**no Stack Overflow page offers an ascending-score ordering** — it read the
rendered tab bar of a tag page, whose tabs are `Newest / Active / Votes / Frequent /
Trending / Bounties / Unanswered` — and that `tab=Unanswered` excludes the
population by construction.

E035 named one untested alternative: **a person's own search box**. That is the
strongest accessible alternative to any reader built here, and it is reachable
from this host while `stackoverflow.com` itself is not.

**Claim under test, in one sentence, with its scope.** *Within one platform's API,
no route a person can reach enumerates the lowest-scored closed questions of a
tag, so a tool built over that ordering is differentiated.* Scope: `api.stackexchange.com`
routes, three sites, the tags E034 declared. It is not a claim about the rendered
site, about users, or about demand.

**What would end the line.** Either of these, not "it did not look useful":

| | condition |
|---|---|
| **KILL-R** | A single first-party route returns the population, ordered ascending by score, over closed questions only, in one request. The ordering and the label are both the platform's, so the prototype has no mechanism left. |
| **KILL-Q** | The `Active` control arm and the `tail` arm are indistinguishable in title self-recovery. The ordering was never the binding constraint, so an ordering tool cannot help even a user who wants it. |

Neither kill needs a user, and both are reachable here. That is why this is the
right next action and not another audit.

## 1. What one probe already found, before this protocol was written

`observed`, 6 requests, 2026-10-06, VM `instance-20260717-0944`, unauthenticated,
User-Agent `think-free-research/1.0`. Reproduce with `python3 harvest.py --probe`.

| route | parameters | status | items |
|---|---|---|---|
| `/info` | `site=stackoverflow` | 200 | — |
| `/search/advanced` | `q=python` | **200** | 3 |
| `/search/excerpts` | `q=python` | **200** | 3 |
| `/search/advanced` | `tagged=git&closed=yes&pagesize=5` | **200** | 5 |
| `/search/advanced` | `tagged=git&closed=yes&sort=votes&order=asc&pagesize=5` | **200** | 5 |
| `/search/advanced` | `tagged=git&sort=votes&order=asc&pagesize=5&filter=!6VvPDzQ)QncrQ` | **400** `Invalid filter specified` | — |
| `/search/advanced` | `tagged=git&sort=votes&order=descending` | **400** `order` | — |
| `/search/advanced` | `tagged=git&closed=maybe` | **200** | 5 |

**The first row of the `closed=yes&sort=votes&order=asc` result is question
`37625790`, score −20, title "Few questions about Visual Studio 2015 Git" — the
first row of E034's own committed harvest, whose `closed_reason` is
`Needs more focus`.** The route returned the population E035 said no surface
orders, and it returned a row already in this repository's bytes.

**Three properties of the instrument, each with its own control, because the
route does not validate every filter value:**

| property | control | reading |
|---|---|---|
| `order` is validated | `order=descending` → 400 `order` | an invalid ordering is refused, so a 200 on `asc` is not a silent default |
| `filter` is validated | the `/questions` default-with-body id → 400 `Invalid filter specified` | matches E035 §"Unanswered surface" |
| **`closed` is NOT validated** | `closed=maybe` → 200, and the same first three items as `closed=yes` | **`closed` may be silently ignored, so `closed=yes` proves nothing on its own.** §3 R0 exists only to settle this, and every closed-question reading in this run depends on it. |

## 2. Inputs, all from committed bytes, zero new collection

E034's `raw/harvest.jsonl`, `raw/r1.jsonl`, `raw/r2.jsonl`, digests in
[`../035-unanswered-surface/README.md`](../035-unanswered-surface/README.md).
Arms as E034 declared them: `tail` = `sort=votes&order=asc` (1125 rows),
`default` = `sort=activity&order=desc` = the `Active` tab (725 rows).

- **Tail arm.** 186 rows with `closed_reason` in `{duplicate, exact duplicate}`.
- **Control arm.** Rows from `default`, which is what a browsing reader sees.
- **Query construction.** A question's own title, HTML-unescaped and stripped of
  the `&quot;`/`&#39;` entities the API returns. This is the **strongest** query a
  person can type: the exact words of the question. A weaker query is strictly more
  favourable to the platform, so if the strongest query already retrieves, the
  weaker one does too, and the kill is safe.

## 3. Measures, gates and the failure condition, declared now

Let `recovered(q)` be: the question's own `question_id` appears in the first 100
items of `/search/advanced?q=<title>&site=<site>`. Let `rank(q)` be its 1-based
position, or `absent` past 100.

| gate | declared rule | consequence |
|---|---|---|
| **R0** | `/search/advanced?tagged=git&sort=votes&order=asc&pagesize=100` **with no `closed` parameter** returns at least one question whose id is in E034's known closed set | **if it does, `closed` is decorative, the platform enumerates the closed tail by default, and KILL-R is met at one request.** If it returns zero, `closed=yes` is doing real work and R1 is the decisive test. |
| **R1** | `tagged=travel/customs&closed=yes&sort=votes&order=asc&pagesize=100` returns ≥ 30 of E034's 200 `travel/customs` tail ids, **and** returns them in non-decreasing score order | **KILL-R met.** The population is enumerated by a first-party route in one request. |
| **R2** | tail title self-recovery ≥ 0.60 **and** ≥ control-arm self-recovery − 0.20 | **KILL-Q met.** The ordering was never the constraint. |
| **R3** | control-arm self-recovery ≥ 0.80 | the instrument can recover independently real positive examples. **Fails → every rate in this run is `not_evaluated`, not zero.** This is the gate the mission has needed seven times. |
| **R4** | a nonsense query returns 0 items | negative control. A route that returns rows for `zzqxwv nonexistent phrase 4198` is measuring noise and R2/R3 are void. |
| **R5** | `/search/advanced` reads `q` such that a title of 3+ tokens returns ≥ 1 item; and the response carries `quota_remaining` and an `items` array | request shape. Any `quota_remaining` ≤ 0 → `not_evaluated`, quota, not a rate. |

**Positive controls that must fire, or the run is void:** R3 (open questions are
recoverable through this route) and R4 (nonsense is not). **Negative control that
must fail:** R4. There is no synthetic fixture anywhere in this run — every id is
a real row of a real platform's dataset, and the four-token title construction is
shared by all three arms so no arm gets a query the others do not.

**Sample sizes are declared, not convenient.** R0: 1 request. R1: 1 request.
R2: 4 requests, ≤ 8 tail duplicates, at most 3 per `(site, tag)` cell. R3: 4
requests, ≤ 8 `default`-arm rows. R4: 1 request. **Total 11 of the remaining
~13 unauthenticated requests**, which E035 left at 19. If the quota runs out
mid-run, the unevaluated gate is reported as `not_evaluated`; nothing is imputed.

**Why these arms and not more.** Brief: match denominators. The two arms are
drawn from the same platform, the same eight tags, the same query construction and
the same route, and differ in exactly the variable under test — the score band
the route drew them from. The arms are **not** equal in size; the rates are
reported with Wilson intervals and no comparison is asserted unless the intervals
exclude 0.

## 4. What this design cannot settle, written before the run

- **The rendered site.** `stackoverflow.com` is Cloudflare-blocked from this host on
  every path (E035). "A person's search box" is the **API's** search route. Whether
  the web UI exposes an ascending-score or closed-only control is `not_measured`
  here and is not inferable from an API route.
- **Adoption.** No gate touches demand. If both kills miss, the next question is
  whether a tag maintainer wants the worklist, and this host cannot answer it.
- **The canonical question.** Still unreadable (E034 §2, nine channels). No
  measure here needs it, and none of them is a proxy for "the answer existed and
  was not found" — which E034's B1 already left unresolved (CI95 [−0.0774, +0.3075]).
- **Whether `closed=yes` survives an authenticated key's wider filter set.** The
  probe shows the unauthenticated route does not validate `closed`; whether a key
  changes that is `untested` and would need a key this host does not have.

## 5. Verdict table, an exclusive partition, declared now

| branch | condition |
|---|---|
| `platform_enumerates_the_tail` | R1 met, or R0 met |
| `search_recovers_the_tail` | R0 and R1 both fail and R2 met |
| `search_does_not_recover_the_tail` | R0 and R1 both fail and R2 not met and R3 met |
| `not_evaluated` | R3 or R4 or R5 not met, or the quota ran out |

The four are exclusive and exhaustive on the declared rules. D064 governs that
shape. **No branch is `candidate_validated`.** The strongest possible outcome of
this run is that the mechanism survives to face a demand measurement nobody has
made; the run cannot supply that measurement and will not claim it.

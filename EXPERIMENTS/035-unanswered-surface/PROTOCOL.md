<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E035 — protocol: is the score-tail backlog reachable through Stack Overflow's own surfaces?

**Declared 2026-10-06 in session 2026-10-06-004, after the §2 feasibility probes and
before any fetch of the §4 population.** Task T-0079. Probes are disclosed in §2 and
their samples are excluded from §4.

## 1. The question, and why it is not more measurement of the same rate

E034 (T-0078) established a rate: duplicate closure runs 0.1352 in a tag's score tail
against 0.0303 in its `Active` tab. It could not read the population (D6: site and tag
confounded; B1: closure is a moderator act). Its declared next action was **more of the
same rate on more tags**, and `STATE-next-actions.md` ranked it first.

Three things were checked before spending that budget, all of them on bytes already
committed, and **two of them change what the candidate would be**:

1. **Is the population reachable at all?** (§2 P1)
2. **Is the `Active` tab a lower-density copy of it, or a different set of questions?**
   (§2 P2 — this decides what a 4.5× ratio *means*)
3. **Is D6's remedy the binding constraint?** (§2 P3 — this decides whether 30 more
   requests on more tags buys anything)

If a population has no UI surface, is disjoint from the feed, and is eight years old,
then the honest product is not *"rescue questions people are failing to find today"*. It
is a **backlog with a measured duplicate rate**, addressed to whoever maintains a tag.
That is a different tool with a different user, and the difference is decided by these
three checks rather than by another rate.

## 2. Probes, disclosed

Run in session 2026-10-06-004 before this file existed. None of these rows enters §4.

| # | probe | result |
|---|---|---|
| **P1a** | `GET https://stackoverflow.com/questions/tagged/python?tab=Newest` and `GET https://stackoverflow.com/`, browser User-Agent | **403**, 5738 and 5578 bytes, Cloudflare `Just a moment…` challenge on **every** path |
| **P1b** | `GET http://web.archive.org/web/20260926121939id_/https://stackoverflow.com/questions/tagged/python`, decompressed | **200**, 409,639 bytes of first-party rendered HTML |
| **P1c** | `GET http://web.archive.org/web/20260707152619id_/…?tab=Votes` | **620 bytes**: the Wayback Machine refused as suspected bot traffic. **Not retried.** |
| **P1d** | `GET https://api.stackexchange.com/2.3/questions/unanswered?site=stackoverflow&tagged=python&sort=votes&order=asc` | **200**, `items` array present, `sort` and `order` accepted on this route |
| **P2** | quota probe `GET /2.3/info` | **`quota_remaining` 76**, not the fresh 300 E034 declared. The unauthenticated budget is per-IP per-day and this host shares it. **§4 needs 24.** |

**P1b is the decisive probe and it is first-party bytes, not a summary.** The rendered
tab bar of a real tag page offers exactly:

`Newest` · `Active` · `Votes` · `Frequent` · `Trending` · `Bounties` · `Unanswered`,
scoped by `Week` / `Month`.

Over those 409,639 bytes: **0 occurrences** of `oldest`, `order=asc`,
`sort=votes&order=asc`, `lowest.vote`, or `ascending`.

**Therefore the ordering E034 measured is not offered by the tag page.** `tab=Votes` is
the score-ordered surface and the page carries no control that reverses it.
**What this does not establish:** the *direction* of `tab=Votes` is `not_measured` in
this session — P1c was refused, and the direction is not inferable from a page that has
no ascending control. Every claim below that depends on the direction is marked.

## 3. What §2's free reads established, and what they change

All four are computed by `analyse.py` over the **committed** E034 bytes, whose sha256
are recorded in `README.md` per D061. No fetch, no new rows.

| id | finding | effect on the candidate |
|---|---|---|
| **R1** | **The `Active` arm and the `tail` arm are strictly disjoint for two of eight tags.** `stackoverflow`/`python`: tail scores **−34…−11**, Active **−9…304**. `math`/`probability`: tail **−9…−4**, Active **−2…159**. Not "4.5× poorer" — **no intersection** | the practical claim is about **membership**, not density. A tool that reorders the feed cannot help; a tool that fetches a different population can |
| **R2** | **Within the tail arm, duplicate rows are viewed slightly *more*.** median `view_count` **251 against 193** for their non-duplicate neighbours; mean 1612 against 906. Tail median age **8.49 yr** against Active's 5.53 | **kills** the motivating frame "the answer existed and was not found". These questions have been seen ~200 times. Whatever this is, it is not a findability failure |
| **R3** | **D6's declared remedy is mis-targeted.** Arcsine-transform between-tag excess variance (observed minus binomial): pooled over 9 eligible tags **+0.0417**; within `stackoverflow` alone (4 tags: 0.000, 0.130, 0.150, 0.210) **+0.0420**; within `travel` (2 tags) **+0.0339**; within `math` (3 tags: 0.030, 0.070, 0.110) **+0.0030** | **tag variance is reproducible inside one site and equals the pooled figure**, so adding 3–4 tags per site is not the binding constraint. `math` reads homogeneous. The residual question is only whether `travel`'s two tags are high *because of travel* |
| **R4** | **Tag mean tail score does not predict the tag's duplicate rate.** Pearson r = **+0.2485**, t = 0.725, df = 8, n = 10 — **not established**. The obvious objection to R3's use of a rank-selected tail is itself unsupported | the tail arm is not a non-comparable stratum across tags |

**R2 and R1 together are the finding that matters.** The population E034 found is an
eight-year-old, two-hundred-view backlog that is not in the feed, and R2 shows the
questions were not ignored while it sat there. So the candidate is **not** rescue. The
only surface that could still be a competitor is the one Stack Overflow itself built for
this — and it is the one E034 never measured.

## 4. The population, declared

**The `Unanswered` surface.** `/questions/unanswered` is a first-class route (P1d) and
`tab=Unanswered` is in the rendered tab bar (P1b). It is the surface the platform points
a person who wants to help at, and it is the strongest accessible alternative to any tool
that claims to find the backlog.

Eight tags, **the same eight E034 declared**, so every rate is comparable to E034's
without any new sampling decision:

`stackoverflow`/`git`, `stackoverflow`/`regex`, `stackoverflow`/`python`,
`stackoverflow`/`docker`, `stackoverflow`/`excel-formula`, `travel`/`customs`,
`math`/`linear-algebra`, `math`/`probability`.

| arm | route | what it is |
|---|---|---|
| **U** | `GET /2.3/questions/unanswered?site=…&tagged=…&sort=votes&order=**asc**&pagesize=100` | the `Unanswered` surface **if it could reverse its own sort**, i.e. the arm that should reach the tail if the surface's *filter* is `unanswered` and only its *ordering* is the obstacle |

3 pages per tag, 24 requests, ≤ 2400 rows. `n` is always the **fetched row count**.
`order=asc` is declared here on purpose: it makes §5's U1 an **identity test between two
id sets** rather than a comparison of two rates, which is what the question is.

**Asymmetry, declared:** U is fetched in *ascending* order and E034's `tail` arm in
ascending order, so both are drawn from the bottom of their own distribution. If U's
filter (`unanswered`) is the binding constraint rather than its ordering, U will read
*lower* than the tail, and U1 will fire with a small overlap. Both readings are
reported; the gate is written so that only the strong form passes.

## 4a. AMENDMENT-1 — A1 fired, and the cause is that the two routes have different default filters

**Declared after the first U fetch and before the second.** The first fetch returned 21
status-200 requests and **2050 rows, and `closed_reason` was absent from every one.** A1
requires the key on 100% of rows, so it fired false and `tally.py` returned
**`not_evaluated`**. That is the gate doing its job, and the cause is named rather than
guessed, from the committed response bodies:

| route | default filter's key set |
|---|---|
| `/questions` (what E034 used) | **19 keys** — includes `closed_reason`, `closed_date`, `accepted_answer_id`, `locked_date`, `community_owned_date`, `migrated_to` |
| `/questions/unanswered` (this arm) | **15 keys** — `closed_reason`, `closed_date` and `accepted_answer_id` are **absent from the key set**, not returned null |

So the field is missing because the **route's default filter does not carry it**, not
because the questions are open. **This is itself a first-class fact about the platform's
own answerer surface** and it is recorded whether or not the re-fetch succeeds: the
surface Stack Overflow provides for *"questions that need an answer"* does not return
whether a question has already been answered elsewhere, unless the caller asks for the
field explicitly. A caller who does not know this reads absence as "not closed" — the
exact imputation D063 forbids.

**The re-fetch, declared now.** Same route, same tags, same pages, `pagesize=100`,
`sort=votes&order=asc`, plus an explicit filter naming
`closed_reason;closed_date;accepted_answer_id`. 21 requests; the run had 53 quota left.
The first fetch's bodies stay committed and are reported as attempt set 1.

**This is not a second bite at the gates.** The re-fetch changes *whether the label is
readable*, not what is measured, and it discriminates two worlds that look identical from
outside:

| what the re-fetch shows | what it means |
|---|---|
| key **present**, values populated | U is a genuinely different surface. U1's low overlap is a fact and U2's density comparison is real |
| key **present**, every value **null** | the `/questions/unanswered` route **structurally excludes closed questions**, so it cannot contain the backlog by construction and U1's overlap is mechanically explained rather than empirical |

Either outcome is decisive and neither is a null. Only a third outcome — key still absent
— would leave the arm `not_evaluated`, and it costs 21 requests to find out.

## 4b. AMENDMENT-2 — the re-fetch cannot be done on this route, so U2 is re-read through E034's

**Declared after AMENDMENT-1's re-fetch returned 400 on all 8 requests and before any
further request.** 42 quota remained.

AMENDMENT-1's premise was *"the route's default filter does not carry the field"* and its
repair was to name the field explicitly. **The premise is right and the repair is
impossible.** Six filter forms were tried, one request each, and the result is a fact
about the route rather than about this caller:

| filter | status | `closed_reason` in the returned keys |
|---|---|---|
| *(omitted)* | 200 | **absent** |
| `default` | 200 | **absent** |
| `withbody` | 200 | **absent** |
| `score;view_count` (a control that names only fields the row certainly has) | **400** `Invalid filter specified` | — |
| `closed_reason` | **400** | — |
| `!6VvPDzQ)QncrQ` — the `/questions` default-with-body filter id | **400** | — |

**The control is the finding.** `score;view_count` is refused, so the route rejects
*custom filters entirely*, not merely filters naming an unknown field. `/questions`
accepts the same syntax and returns 19 keys including `closed_reason`. So the two routes
differ in kind: one is filterable and one is not, and the unfilterable one is the
platform's own answerer surface.

**What this costs, and the repair.** U2 cannot be computed on U's own bytes, and a rate of
0.0000 read off an absent field is a statement about the filter, not about the
population — the exact confusion this repository has already paid for twice (F056's
budget limits, D063's absent key). Declaring U2 `not_evaluated` would be honest but it
would stop one request short of an answer that is available.

**The repair: re-read U's ids through E034's route.** `GET /2.3/questions/{ids}` accepts
up to 100 ids per request and carries the default filter that includes `closed_reason`.
U holds **2050 distinct ids**, so this is **21 requests** against 42 remaining, and it
leaves the ids, the scores, the sites and the tags exactly as fetched — only the closure
label is added, and it is added from the route that has it. The two fetches' union is the
population; nothing is sampled away.

**This is declared before the request and it does not move the threshold.** U2 keeps the
rule it was declared with. If the re-read shows U is as dense in duplicates as the tail,
U2 does not fire and §6's third branch closes the candidate. If it shows U is denser, U2
fires and the first branch holds.

## 5. Gates, declared before the fetch

| gate | rule | fires when | what it decides |
|---|---|---|---|
| **A1** | ≥95% of the 24 requests return 200 with an `items` array, and 100% of rows carry the `closed_reason` key (present-or-absent recorded, never imputed) | otherwise `not_evaluated` | is this the declared population |
| **U1** | **per-tag Jaccard overlap** of U's id set with E034's `tail` id set, median over the eight tags, is **< 0.10** | fires when the `Unanswered` surface does not contain the backlog | **Stack Overflow's own answerer surface does not reach the population.** This is the finding that gives the candidate a home |
| **U2** | pooled U CI95 **lower** > pooled `tail` CI95 **upper** | fires when the backlog is denser in repeats than the surface | the density half; U1 and U2 can both fire, and both are needed |
| **U3** | U's per-tag score range **overlaps** E034's `tail` per-tag score range for ≥6 of 8 tags | fails when the surfaces are disjoint in *score* as well as in id | R1's mechanism, tested on a second surface |

**D064 governs these.** Each is a statistic or a predicate over a whole relation — a
median over eight overlaps, an interval comparison, a count of eight — never a
conjunction over a chosen subset of comparators. E034's §7 gate failed by being the
latter and both of its branches were true.

## 6. Kill, narrow, or continue

- **U1 and U2 fire** → build the reader (§7). The population is real, denser, and absent
  from the platform's own surface for it.
- **U1 fails** (overlap ≥ 0.10) → **the candidate dies here, and this is the strongest
  kill available**: Stack Overflow ships the surface itself. Prior art does not get to
  outbid the platform's own product. Record the overlap and stop.
- **U1 fires, U2 fails** → the backlog is real and reachable by no surface, but is **not
  denser in repeats**. Collapses to "an old unanswered backlog exists", which is not a
  product. Record and stop.
- **A1 fails** → `not_evaluated`. A resource statement, not a negative result.

## 7. If it survives: what is built, and against what

A per-tag reader over `sort=votes&order=asc`, printing each row's score, view count,
age, answer count and **platform-owned `closed_reason`**, with the tag's measured
duplicate rate beside it. It needs **no canonical and no similarity computation** — the
canonical edge is unreachable through nine channels (E034 §2), so a tool that clustered
questions would be guessing. The label is free.

**The strongest accessible alternative is `tab=Unanswered`, and §5 is the comparison
against it.** The prototype's differentiating output is therefore: *the questions the
platform's own answerer surface does not show you, and how many of them are already
answered somewhere else.*

## 8. Ceilings, declared before the fetch

- One platform. Duplicate closure is a **moderator act**, so every rate is a property of
  a community's practice (E034 §8, unchanged).
- **Eight tags chosen by E034's declared a-priori rule, not sampled.** U2's pooled rate
  inherits E034's tag set and is not a network-wide figure.
- The direction of `tab=Votes` is `not_measured` (P1c refused). **U is a route, not a
  screenshot of the tab.** No claim here is about what the tab renders; every claim is
  about what the route returns.
- `pagesize=100` means U's rows are *not* rank-adjacent to E034's `pagesize=25` rows at
  equal depth — a 100-row page reaches deeper into the tail than a 25-row page. U is
  therefore expected to read **higher** than `tail`, and U1's overlap is the honest
  measure, not the rate.
- Quota is 76 and shared per-IP; this run needs 24.
- R3's variance components rest on 4/2/3 tags per site and one exactly-zero cell
  (`excel-formula`, 0 of 200). They are **sufficient to show D6's remedy is not the
  binding constraint** and **not sufficient to apportion tag against site**.

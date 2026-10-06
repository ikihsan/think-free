<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Failures — recorded finding F059

Split out of [`FAILURES-findings-23.md`](FAILURES-findings-23.md), which held F057 and
F058. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are stable across all
findings files.**

## F059 — the score-tail worklist is one unauthenticated URL, and F058's reachability claim was a fact about one rendered view

**Status: a candidate killed by the platform's own documentation, at a cost of 8 requests,
after three experiments had spent 1125 rows establishing that the population was real.**
`EXPERIMENTS/036-search-backlog/`, T-0080, 2026-10-06. What fired: **R0**, the
reachability gate. What is `not_evaluated`: R1, R2, R4. What was corrected: three claims in
F058 and E035's README, two of them load-bearing for a build decision.

### The mechanism, and why it ends the candidate

E035 named the proposed differentiator as *"the platform's own closure label over a
population no surface orders that way"*. Both halves are the platform's. One
unauthenticated request:

```
https://api.stackexchange.com/2.3/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100
```

returns **100 questions ordered ascending by score (−20 … −5, non-decreasing)**, **81 of
them ids already in E034's committed harvest** (the first at rank 1), and **13 of them
labelled `Duplicate` or `exact duplicate` in the payload's own `closed_reason` field**,
which the route's default filter carries on 48 of 100 rows and omits on the open ones.
**No API key, no custom filter, no second route, no computation.** Deeper pages need
`page=2`, a documented parameter of the same route (`inferred`, not fetched).

The whole instrument is therefore a presentation layer over a public query. `readout.py`
prints the URL and the 13 rows. That is not a prototype with a thin mechanism; it is a
proof that there is no mechanism to have.

### Correction 1 — "no surface offers the ordering" was measured on one rendered view

F058's evidence is 409,639 bytes of first-party HTML from a tag page: seven tabs, zero
occurrences of `oldest`, `order=asc` or `ascending`. That is a correct and careful reading
of **a tag page**, and F058 labelled its own limit — *every claim about surfaces is a
claim about routes*. What it did not do is enumerate the platform's **interface surface**.
Stack Exchange ships a documented filter vocabulary that includes `sort`, `order`, `tagged`,
`closed`, `votes`, `answers`, `accepted`, `body`, `title`, `user`, `url`, `created`,
`updated`. Two of those are an ordering. **D066.**

### Correction 2 — `closed` is not validated, so that control could not have been read off the route either

| filter value | status | reading |
|---|---|---|
| `order=descending` | **400** `order` | `order` is validated; a 200 on `asc` is not a silent default |
| `filter=!6VvPDzQ)QncrQ` | **400** `Invalid filter specified` | `filter` is validated |
| `closed=maybe` | **200**, same first three items as `closed=yes` | **`closed` is not validated** |

So "the platform offers no closed-only control" was not establishable from that route's
behaviour, and R0 showed the closed tail comes back with **no `closed` parameter at all**.
The gate existed only to settle this, and it is the one that fired.

### Correction 3 — the label does not need an API key on this route

E035's README recorded that the closure label "needs an API key this host does not have",
established from **two routes**: `/questions/unanswered`, whose key is absent from the
response, and `/questions/{ids}`, whose default omits it. `/search/advanced`'s **default**
filter carries it. A per-route fact had been generalised to a platform fact — **F020's
shape, and F048's lesson applied to the mission's own instrument** — and it removed the
API-key premise a tool over this population would have rested on.

### The retrieval arms: the ordering was not the binding constraint either, and it is thin

| arm | recovered | ranks | CI95 |
|---|---|---|---|
| tail, own title, 4 requests | **3 / 4** = 0.75 | 1, 7, 1 (one absent past 100) | [0.3006, 0.9544] |
| `Active` control, own title, 2 evaluated | **2 / 2** = 1.00 | 1, 1 | [0.3424, 1.0] |

The **positive control fired on independently real positive examples** — the seven checks
this record has needed since F013. Tail recovery sits at the 0.75 KILL-Q's threshold would
need and one rank behind the control arm, so retrieval does not separate the arms either;
**at n=4 against n=2 that is `inferred`, and KILL-Q is declared `not_evaluated` because the
rule is not decidable at this n.** R4, the negative control, was refused by the quota
window and is `not_evaluated`, so a nonzero rate rests on the positive control alone.

### The run failed in its own process, twice, and both are in the bytes

1. `harvest.py`'s stage argument did not accept `retrieval`, so it fell through to the
   full **nine**-request plan against a budget of **four**. Three requests were refused
   with *"too many requests from this IP, more requests available in 53004 seconds"*, and
   R3 and R4 are unevaluated **because of a bug in the runner**, not because the controls
   are hard.
2. `quota_wall()` treated a successful **200** whose `quota_remaining` had gone negative
   as a failed request, which silently discarded both evaluated control rows and reported
   R3's rate as `null`. Caught and fixed; the corrected tally is the committed one.

**The kill does not rest on either bug**, because KILL-R is an id-intersection against
committed evidence and needs no control. The retrieval arms do, and they are thin. This is
the run's own version of the pattern F055 and F058 keep hitting: an instrument's own
selection and plumbing shaping what it reports.

### What survives, and what it costs

**The population is untouched.** E034's 4.5× gradient, its per-tag spread, F058's 8.49-year
median age and the 251-against-193 view reading all stand. Only the **reachability and
mechanism** claims died, and they died for the best available reason: the strongest
accessible alternative turned out to be a public URL, found before anything was built.
That is a kill worth having.

**The adoption question is now the whole question, and it has never been measured.** Three
experiments found a real, large, reproducible population and never found a person who
wants it surfaced. E035 said so; this run says it louder, because it removed the last
technical reason to think a tool was needed.

### Not established, and not to be assumed

- **The rendered site.** `stackoverflow.com` is Cloudflare-blocked from this host on every
  path. Whether the **web UI** offers an ascending-score or closed-only control is
  `not_measured`. A person with a browser and no key may lack what the API gives away,
  and this run cannot say. **The narrow application that would survive is exactly this
  gap — and it needs a browser or a user, not another request.**
- **R1's 0 items is unexplained.** `tagged=customs&closed=yes&sort=votes&order=asc` on
  `travel` returned **200 with 0 items** while the same construction on `stackoverflow`
  worked. One request was not spent separating a site-parameter mistake from a population
  fact, because KILL-R was already met.
- **Depth.** One page fetched; `page=2` is documented, not exercised.

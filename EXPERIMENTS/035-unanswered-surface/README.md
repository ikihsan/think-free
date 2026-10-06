<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E035 — the score-tail backlog, and why every surface Stack Overflow offers misses it

`observed` 2026-10-06, session 2026-10-06-004, VM `instance-20260717-0944`. Protocol:
[`PROTOCOL.md`](PROTOCOL.md). Gates: [`raw/tally.json`](raw/tally.json). Free reads:
`python3 analyse.py`. Prototype: `python3 readout.py --tag travel/customs`.

**Verdict: `backlog_confirmed_unanswered_surface_excluded_density_unknown`.** The
population E034 found is confirmed and its reachability is now mapped, but the run's own
declared verdict table has **no branch for what happened**, and the gate that fired does
not carry the weight the protocol put on it. Both are stated below rather than smoothed.

## What the free reads found, before any request

Four results over E034's committed bytes, at zero quota cost. Input digests:

| file | sha256 |
|---|---|
| `034-reask-tail/raw/harvest.jsonl` | `d752ae2909f38830ba11c0beeabc3b22404f5ec1cec9ab0477e21601add00e71` |
| `034-reask-tail/raw/r1.jsonl` | `5b6c7283242ce198d2578618f40f87b798b05316423430cc714952f4d59103b4` |
| `034-reask-tail/raw/r2.jsonl` | `399468ab791f9b0a45a1e68dd99dc95a5b998599f986d33139a21771cb6a8001` |

**R1 — the `Active` and `tail` arms are not two densities of one population. For two of
eight tags they do not intersect at all.**

| tag | tail scores | `Active` scores | overlap |
|---|---|---|---|
| `stackoverflow`/`python` | −34 … −11 | −9 … 304 | **none** |
| `math`/`probability` | −9 … −4 | −2 … 159 | **none** |
| `travel`/`customs` | −7 … 0 | −3 … 24 | −3 … 0 |

**R2 — and the population is not one that was overlooked.** Within the tail arm the
duplicate-closed rows have a **higher** median view count than their non-duplicate
neighbours, not a lower one.

| | n | views median | views mean | age median |
|---|---|---|---|---|
| tail, duplicate | 186 | **251** | 1612 | 8.86 yr |
| tail, not duplicate | 939 | **193** | 906 | 8.42 yr |
| `Active` arm | 725 | 718 | — | 5.53 yr |

**R2 removes E034 §1's motivating frame.** Its protocol says the questions worth surfacing
are "the ones the ranked feed is worst at showing", implying people are failing to find
answers. These questions have been read a median of 200 times and the duplicates slightly
more than their neighbours. Whatever this is, it is not a findability failure. The product
is a **backlog with a measured duplicate rate**, not a rescue.

**R3 — D6's declared remedy was aimed at the wrong constraint.** Between-tag excess
variance on the arcsine scale (observed minus binomial), tags with n ≥ 50:

| grouping | tags | excess |
|---|---|---|
| pooled | 9 | **+0.0417** |
| within `stackoverflow` alone | 4 | **+0.0420** |
| within `travel` | 2 | +0.0339 |
| within `math` | 3 | +0.0030 |

Within `stackoverflow` the four tags read 0.000 / 0.130 / 0.150 / 0.210 — a clean ladder,
and its excess variance **equals the pooled figure**. Tag variance is therefore
reproducible inside a single site. `STATE-next-actions.md` ranked "three to four more tags
on each of the three sites, about 30 requests" as the top item on the mission; this
computation reads the same question off bytes already committed and largely answers it.
The residual is only whether `travel`'s two tags are high *because of travel*.

**R4 — the obvious objection to using a rank-selected tail is unsupported.** Pearson
r(tag mean tail score, tag duplicate rate) = **+0.2485**, t = 0.725, df = 8, n = 10 —
`not_established`. `sort=votes&order=asc` returns the lowest 100 per tag, and those sit at
very different score depths (`travel` −7…0 against `stackoverflow`/`regex` −85…−8), but
that depth does not predict the rate.

## Reachability: the ordering is not offered anywhere

`stackoverflow.com` is behind a Cloudflare challenge from this host on **every** path,
browser User-Agent included (403, `Just a moment…`). A Wayback snapshot of
`stackoverflow.com/questions/tagged/python` from 2026-09-26 was reachable: **200,
409,639 bytes of first-party rendered HTML**.

The tab bar it renders offers exactly:

`Newest` · `Active` · `Votes` · `Frequent` · `Trending` · `Bounties` · `Unanswered`,
scoped by `Week` / `Month`.

Across those 409,639 bytes: **0 occurrences** of `oldest`, `order=asc`,
`sort=votes&order=asc`, `lowest.vote`, `ascending`. **The ordering E034 measured is not
offered by the tag page.** `not_measured`: the *direction* of `tab=Votes` — the Wayback
Machine refused the `tab=Votes` snapshot as suspected bot traffic and no claim here depends
on it.

## The Unanswered surface: excluded by construction, and unreadable

`/questions/unanswered`, the route behind `tab=Unanswered` — the surface the platform
points a person who wants to help at. **8 tags, 21 requests, 2050 distinct ids.**

| gate | declared rule | result |
|---|---|---|
| **A1** | ≥95% requests 200, 100% of rows carry `closed_reason` | requests **21/21**, label **0/2050** |
| **U1** | median per-tag Jaccard overlap with E034's `tail` ids < 0.10 | **0.0283** — fires |
| **U2** | pooled U CI95 lower > pooled `tail` CI95 upper (0.1653 [0.1448, 0.1882]) | **`not_evaluated`** |
| **U3** | score ranges overlap for ≥6 of 8 tags | **7 of 8** — fires |

**U1 fires, and the reason is not the one section 6 assumed.** A low overlap has two
causes that look identical from the overlap alone. It is the second:

| | |
|---|---|
| E034's known duplicate-closed ids | **224** |
| — of those, present in U | **0** |
| E034's tail duplicates | **186** |
| — of those, returned by U | **0** |
| — of those, satisfying `is_answered == false` (U's only stated criterion) yet still absent | **98** |
| E034's tail non-duplicates present in U | 108 |

**`/questions/unanswered` returns open questions.** 98 of the 186 tail duplicates meet its
advertised criterion and are still not returned, so the exclusion is on closure, not on
answeredness. U's low overlap is therefore **definitional, not empirical** — which means
U1 firing is much weaker support for the candidate than §6 treated it as.

**U2 is `not_evaluated`, and the reason is worth the space.** The label is absent from all
2050 rows because `/questions/unanswered`'s default filter omits `closed_reason`,
`closed_date` and `accepted_answer_id` — absent from the key set, not returned null.
`/questions` returns 19 keys including all three. Six filter forms were tried:

| filter | status | `closed_reason` present |
|---|---|---|
| *(omitted)* / `default` / `withbody` | 200 | **no** |
| `score;view_count` — a control naming only fields the row certainly has | **400** `Invalid filter specified` | — |
| `closed_reason` | **400** | — |
| `!6VvPDzQ)QncrQ` — the `/questions` default-with-body filter id | **400** | — |

The control is the finding: the route refuses *custom filters entirely*, unauthenticated.
Re-reading all 2050 ids through `/questions/{ids}` — 21 requests, **every id returned** —
produced **0** with the field, because that route's default omits it too. **The label on
this population needs an API key this host does not have.** A rate of 0.0000 read off an
absent field would be a statement about the filter, so `tally.py` returns a third answer
instead. Quota at the end: 19 of 300.

## The prototype

`readout.py` runs on committed bytes and makes no network request, so its output is
reproducible offline and diffable against the digests above.

```
travel/customs
  backlog          200 lowest-scored questions
  closed duplicate 93  0.4650  CI95 [0.3972, 0.5341]
  listed by tab=Unanswered   24 of 200 (12.0%)

  score   views       age   ans   closure  title
     0    5059     11.9y     1 Duplicate  Carrying two iPads (and other electronics) to India
     0    4157      7.9y     1 Duplicate  Health supplements/Vitamins bringing into Malaysia
     0    3209     11.4y     1 Duplicate  Time from Terminal B to Terminal A at Newark (EWR)
```

`readout.py --survey` prints the per-tag table: of the 1125 lowest-scored questions across
these ten tags, **186 (16.5%) are closed as duplicates**, and the rate spans
**0.0000 (`excel-formula`) to 0.4650 (`customs`)**.

It computes no similarity and cannot name the canonical question — no client can
(E034 §2, nine channels). That is the point: **the differentiating output is the
platform's own closure label over a population no surface orders that way**, so the tool
needs no new algorithm to have a mechanism.

## What this does not establish

- **Nothing measured whether anyone wants this.** No adoption claim, no user, no
  interview. The application is a worklist for a tag maintainer and the mission has never
  measured that person.
- **U2 is unknown**, so "the backlog is denser in duplicates than the alternatives" is
  unverified. E034's pooled `tail` figure of 0.1653 is a rate on one route's population,
  not a margin over anything.
- **One platform, and its duplicate closure is a moderator act.** Every rate here is a
  property of three communities' practice.
- **Eight tags, chosen by E034's declared a-priori rule and never sampled.** The survey is
  not a network-wide figure.
- **The direction of `tab=Votes` is `not_measured`.** Every claim about surfaces is a claim
  about routes, except the tab-bar enumeration, which is rendered bytes.
- **`travel`/`customs` at 0.4650 is one site's one tag**, and R3 leaves open whether that is
  the tag or the community.

## Digests of this run's raw evidence

| file | sha256 |
|---|---|
| `raw/u1.jsonl` (2050 rows) | `ab23dc2767a9cadf7f87b50d6c4b3b512de0a983f6d113b53db044c5b37712ea` |
| `raw/pages1.jsonl` (21 attempts, bodies) | `897a6d4333ba95a31e60419b6250013ff3068f2471db84a175a9a70c15021a0d` |
| `raw/relabel.jsonl` (22 attempts, bodies) | `fee2124d1a1853291289b8bda578765546dfbb339ed3dfc08d25c40961edf281` |
| `raw/tally.json` | `771a5f27da885d30b9f3aa021145a5b1988618a0600d14500461840eb1ad38db` |
| `raw/u2.jsonl` (**empty** — attempt set 2's 8 requests all returned 400) | `e3b0c442…b855` |

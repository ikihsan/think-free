<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E036 — the score-tail worklist is one unauthenticated URL

`observed` 2026-10-06, session 2026-10-06-005, VM `instance-20260717-0944`, **8 requests
of 300** (6 reachability probe + 2 reach gates; the retrieval arms spent the rest and the
quota window then refused three). Protocol: [`PROTOCOL.md`](PROTOCOL.md), written before
the second measurement request. Gates: [`raw/tally.json`](raw/tally.json). Free reads:
`python3 tally.py`, `python3 readout.py`. Verdict:
**`platform_enumerates_the_tail` — KILL-R met, mechanism killed, nothing built.**

## The finding

One request:

```
https://api.stackexchange.com/2.3/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100
```

returns **100 questions ordered ascending by score (−20 … −5, non-decreasing)**, of which
**81 are ids already in E034's committed harvest** — the first at rank 1 — and **13 carry
`closed_reason` in the `Duplicate`/`exact duplicate` set**. No API key, no custom filter,
no second route, no computation.

That is the entire proposed product. E035's README named the differentiator as *"the
platform's own closure label over a population no surface orders that way"*. The label is
in the payload, and the platform orders the population the way it was measured.

| what the prototype would do | the platform's own route |
|---|---|
| order a tag's questions ascending by score | `sort=votes&order=asc` |
| restrict to a tag | `tagged=git` |
| label each row with Stack Overflow's own closure reason | `closed_reason`, present on 48 of 100 rows; absent means open |
| filter to duplicate closures | `closed_reason ∈ {Duplicate, exact duplicate}` |
| compute nothing | nothing |

`python3 readout.py` prints the URL and the 13 rows it returned. **It is a URL, not an
algorithm.** Deeper pages need `page=2`, a documented parameter of the same route —
`inferred` from the parameter set, not fetched.

## Three corrections to the record this run makes

**1. E035's "no surface offers the ordering" was a statement about one rendered view.**
F058's evidence is 409,639 bytes of first-party HTML from a tag page: tabs `Newest /
Active / Votes / Frequent / Trending / Bounties / Unanswered`, zero occurrences of
`oldest`, `order=asc` or `ascending`. That is a correct reading of a **tag page**. The
platform also ships a documented filter API whose vocabulary includes `sort`, `order`,
`tagged`, `closed`, `votes`, `answers`, `accepted`, `body`, `title`, `user`, `url`,
`created`, `updated`. Two of those are an ordering. D066 governs this.

**2. `closed` is not validated on this route, so E035's "the platform does not offer a
closed-only control" could not have been read from the route either.** `closed=maybe`
returns 200 with the same first three items as `closed=yes`. `order=descending` returns
400 `order`, and the `/questions` default-with-body filter id returns 400 `Invalid filter
specified` — so `order` and `filter` *are* validated and `closed` is not. Any claim about
the `closed` filter's behaviour needs a control that varies only that parameter; R0 exists
only to settle whether `closed` does any work, and it showed the closed tail comes back
with **no `closed` parameter at all**.

**3. The label does not need an API key on this route.** E035 recorded that
`closed_reason` "needs an API key this host does not have", from two routes:
`/questions/unanswered` (key absent from the response) and `/questions/{ids}` (omitted).
`/search/advanced`'s **default** filter carries it. That is F020's shape again — a
per-route fact generalised to the platform — and it invalidates the API-key premise a
tool over this population would have rested on.

## Gates

| gate | declared rule | result |
|---|---|---|
| **R0** | no `closed` parameter, `sort=votes&order=asc`, ≥1 id in E034's known closed set | **fires** — 81 of 100 `git` tail ids, first at rank 1; 9 of E034's 12 `git` duplicates among them |
| **R1** | ≥30 of E034's 200 `travel/customs` tail ids, ascending | **`not_evaluated`** — status 200 with **0 items**, cause untested. R0 met KILL-R without it, so no request was spent separating a site-parameter mistake from a population fact |
| **R2** | tail title self-recovery ≥ 0.60 and ≥ control − 0.20 (**KILL-Q**) | **`not_evaluated`** — 3 of 4 recovered, CI95 [0.3006, 0.9544]. KILL-Q is not decidable at n=4 |
| **R3** | control-arm self-recovery ≥ 0.80 (positive control) | **fires** — 2 of 2, both at rank 1, CI95 [0.3424, 1.0]; the other 2 refused by quota |
| **R4** | a nonsense query returns 0 items (negative control) | **`not_evaluated`** — refused with *"too many requests from this IP, more requests available in 53004 seconds"* |
| **R5** | requests carry `items` and `quota_remaining` | **met for the 5 evaluated requests**; the counter reached 0 mid-run |

The positive control **did** fire on independently real positive examples — the `Active`
arm's questions, real rows, found at rank 1 — which is the check this record has needed
seven times. R2's 3 of 4 sits *at* the 0.75 the KILL-Q threshold would need and one rank
below the control arm's 1.00, so **the ordering was not the binding constraint either**,
but at n=4 versus n=2 that is `inferred`, not established.

## The run also failed, in its own process, and the reason is recorded

`harvest.py` takes a stage argument. `retrieval` was not in the accepted set, so it fell
through to the full nine-request plan against a budget of four. Three requests were
refused by the API and R3 and R4 are `not_evaluated` because of a bug in the runner, not
because the controls are hard. `quota_wall()` also had a second bug — it discarded
successful 200 responses whose `quota_remaining` had gone negative, which zeroed R3's
apparent rate until it was fixed. Both are in the raw bytes. The scientific conclusion
does not rest on either, because KILL-R is an id-intersection against committed evidence
and needs no control; **the two retrieval arms do, and they are thin.**

## What this does not establish

- **Nothing about adoption.** No gate touches demand. If the ordering half had survived,
  the next question would be whether a tag maintainer wants the worklist — still
  unmeasured after three experiments.
- **The rendered site.** `stackoverflow.com` is Cloudflare-blocked from this host on every
  path. Whether the *web UI* exposes an ascending-score or closed-only control is
  `not_measured`. A person with a browser and no API key may not have what
  `api.stackexchange.com` gives away unauthenticated, and this run cannot say.
- **The population is untouched.** E034's 4.5× gradient, F058's 8.49-year median age and
  the per-tag spread all stand. What died is the claim that they are **unreachable**.
- **Whether the whole tail is enumerable.** One page was fetched. `page=2` is documented;
  the depth is `inferred`.
- **R1's 0 items is unexplained**, and it is the one request whose silence could have
  hidden a counter-example.

## Digests of this run's raw evidence

| file | sha256 |
|---|---|
| `raw/probe.jsonl` (6 attempts, bodies) | `1140daf532cc5e7093ac4bb73c5375d03f07eb18e0fec58173278010c5ac6ca2` |
| `raw/measures.jsonl` (9 attempts, 5 evaluated) | `f1e2e884edbb62b3c3290d2d8fac943f4ac3626daa129e3aa772cc758946f4ed` |
| `raw/tally.json` | `fc0f9a857c4d56ae2c114078dc420661bf8a3ec78443dfbef27a5435305b5399` |

Recompute: `python3 harvest.py --probe` then `python3 harvest.py reach` then
`python3 harvest.py retrieval`, then `python3 tally.py`. The retrieval stage will be
refused for ~14.7 h after a full window; `--budget` reports the counter for one request.

**The tally's own gate, falsified against the defect's bytes** (D025).
`tests/test_e036_gate_handling.py` holds two things. `quota_wall()` must classify the
API's *refusal* (a 400 carrying `too many requests`) and never an exhausted counter: a
200 reporting `quota_remaining` −1 is a successful response, and treating it as a failure
discarded both evaluated control rows and wrote R3's rate as `null`. **The test was
falsified by restoring that defect verbatim: 2 of 17 failed, on the −1 and 0 cases**, and
`raw/tally.json` is byte-identical to the digest above after the fix was put back. The
other half holds the committed gates to the numbers the record states — R0 fired with 81
ids at rank 1, the positive control fired, KILL-Q and R1 and R4 carry no rate verdict, and
**no branch claims a candidate**.

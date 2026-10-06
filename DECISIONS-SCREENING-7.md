<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Screening decisions D066–D067

Split out of [`DECISIONS-SCREENING-6.md`](DECISIONS-SCREENING-6.md) at its line cap.
Decisions **D066, D067**. Index rows and identifier spans in
[`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md); [`DECISIONS.md`](DECISIONS.md) carries
the count.

## D066 — a "no surface offers X" claim must enumerate the interface surface, not one rendered view

**Date:** 2026-10-06. **From:** F058, corrected by F059.

**Decision.** A reachability claim about a platform is admissible only if it names the
**interface surface** it enumerated — routes, documented filter vocabularies, URL
parameters, and at least one rendered view — and states which of those it did not reach.
A claim established on one rendered view is a claim about that view.

**Why.** F058 established, from 409,639 bytes of first-party tag-page HTML listing seven
tabs and zero occurrences of `oldest`, `order=asc` or `ascending`, that **no Stack Overflow
surface offers an ascending-score ordering**. That reading was correct and careful, and it
was also the whole basis for building a tool. E036 then made the same request that E034
used to harvest the population — a documented sort/order pair on a documented filter route
— and it returned **81 of E034's 100 `git` tail ids**, ascending, in one unauthenticated
request, with the closure label already in the payload. The candidate was prior art as a
URL.

**How the claim is now written.** F058 becomes: *no rendered Stack Overflow tag page
offers an ascending-score ordering; the API's `/search/advanced` route does.* The narrow
reading is the one the evidence carries, and the wide one is what the record had been
using to justify a build.

**Ceiling.** The correct remedy was not to enumerate more of this platform. It was to
notice that a candidate which dies to one documented query should have died before
1125 rows were harvested to describe its population. D067 carries that.

## D067 — test the strongest alternative before measuring a population in detail

**Date:** 2026-10-06. **From:** F059.

**Decision.** A candidate whose value is a *mechanism* — an ordering, a label, a
retrieval path, a compute step — is tested against **that mechanism's existing source**
before any population measurement on its behalf. Reading the population first is admitted
only when the existing source cannot be enumerated, and the reason must be written down.

**Why.** E034, E035 and E036 spent three experiments and 1125 harvested rows describing a
population's duplicate-closure rate, its per-tag spread, its age and its view counts. The
population was real and every number was reproducible. **The mechanism a tool would sell
was checked last**, and it was a public URL: `sort=votes&order=asc` is a documented filter
pair, and the closure label the tool would compute arrives in the same response. **8
requests and an id-intersection settled what 1125 rows could not.**

The ordering of the work was backwards, and the record shows it three times over: F055
found the sampled stratum was 4.5× poorer in the thing being measured; F058 found the
frame was "not overlooked" rather than "not found"; F059 found the population is reachable
by the platform's own default route. Each was a fact about the **instrument's selection**,
read after the measurement rather than before.

**Consequences that are already in force.**

1. The score-tail worklist line is **closed**. Its population stands; its mechanism is
   prior art. Nothing is built.
2. Any surviving application on this platform must justify itself on the gap F059 names
   as unmeasured: **the rendered web UI against the API**. That is a browser or a user
   question, not another request.
3. A next candidate whose differentiator is a mechanism is dead on arrival if the
   mechanism's source is a documented query. The check is one request.

**Ceiling.** This decision costs a request on every mechanism candidate, and a request is
cheap only where quota is. `order` and `filter` validated their values on this route and
`closed` did not, so the cheapest check is often **two** requests, not one. D065's rule —
a gate that fires needs a control that varies only the parameter under test — is what made
R0 the gate that could fire; without it the run would have read `closed=maybe` as evidence
that a closed-only control existed.

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E062 — what a non-software population says about unmet need

Session `2026-10-08-006`, VM `instance-20260717-0944`, declared 2026-10-08.

**This experiment produced no candidate and no prototype.** It produced one
reusable instrument, one disarmed gate, and a reason the mission's standing
reading of its own record is wrong.

## Verdict

| gate | outcome |
|---|---|
| **G1 retrieval** | **met.** 1200 rows, 6 non-software sites, 12 requests all HTTP 200, API `items_returned` sums to 1200, every row has a body, 519 carry `closed_reason`. `total_count` is not returned by this route, so the declared reconciliation against it is a **missing observation, not a zero** (D082). |
| **G2 control validity** | **superseded.** The control pools recovered 7 and 6 rows against a declared 20 each; rather than loosen the rules to hit a target, the reader was replaced — see below. |
| **G3 the measurement** | **not run, and permanently disarmed.** `AMENDMENT-2.md`. |
| **G4 outcome gradient** | **met.** Still-open share by age cohort: 3.0% / 0.8% / 15.2% / 3.5%. Gap 14.4 points against a declared 10. **Not monotone, right-censored at the young end**; reported as observed, no mechanism claimed. |
| **Sub-test: answerability of unremedied need** | **17 of 20 resolved by a free general assistant today.** |

## The instrument this added

`view_count` records **independent arrivals at a need**. Every population this
mission has measured counted *statements* of need. F039 measured whether
requesters came back — 1 of 794 — and read that as absence of demand.

A view count asks the same question of the platform instead of the person, on
every row, and it is the channel the substitute venue was chosen for. The
unremedied population is 110 rows carrying 118,990 views, and the top row
(`I need help to identify my bmx bike by using serial numbers`) has sat
unanswered for **9.0 years at 15,635 views**.

Arrival is not heavy-tailed here: the top 10% of unremedied rows carry 3.2% of
all views. So screening rows and keeping the most-viewed few is *not* a
privileged sample of unmet need, and the mission's habit of reading a screened
subset as representative is wrong on this venue too.

## The result that changes how the record reads

The top 20 unremedied rows by arrival were each attempted against the strongest
accessible alternative — a general-purpose assistant answering from its own
knowledge, free and instant. Full working in `raw/answerability-top20.tsv`.

| label | n of 20 |
|---|---|
| `resolved-from-knowledge` | **17** |
| `resolved-needs-per-model-spec` | 1 — method answerable, value needs a manufacturer spec sheet |
| `unresolved-no-public-data` | 1 — no free source I could reach decodes this serial number |

**Unanswered on a platform is not unserved.** The 17 are not gaps; they are
rows a forum left open because nobody who knew the answer was on the forum in
2009–2016. They are now answered, for free, in seconds.

That is a stronger reading of F039 than F039's own: "1 of 794 requesters replied
again" was never evidence that the need went unserved. It was evidence that
requesters do not post follow-ups — and someone whose washing machine is fixed
by an assistant in 2024 never posts on a forum either way. **The mission has
been measuring statements of need and reading them as service levels.**

### The residual, and why it is a data problem

The 5% that is not answerable is not a software problem. The bike serial number
`SNACEOSF18391` is the clearest case: **the answer is a record nobody kept.**
Bike Index is the nearest thing to an incumbent — a 501(c)(3) with over 1,844,000
cataloged bikes and tens of thousands of daily searches (`bikeindex.org/about`,
fetched 2026-10-08) — and it is a *registration* service: a bike appears only
because its owner chose to add it. A 2001 BMX nobody registered is absent, and
no program can reconstruct it. **My lookup of that serial returned a
client-side, rate-limited page rather than a result, so the honest label is
"no free source I could reach decoded it", not "no source exists."** The fridge
capacitor is the same shape: the method is free knowledge, the value sits in one
of thousands of per-model spec sheets nobody has made queryable.

The population that resists a program resists it for a reason no amount of
engineering addresses: the data was never recorded.

## Named asymmetries

- **The reader attempting each row is the model that would build the tool**, and
  is simultaneously the free instant incumbent. The finding is therefore framed
  against *incumbence*, not proficiency: the question is whether a gap exists
  between what a free general assistant supplies and what the requester needed —
  not whether I am good at cooking and wiring.
- **Age.** The rows are 5–11 years old and predate general assistants. This
  measures whether *today's* unremedied population is served by *today's*
  incumbent. It cannot tell you what was true in 2015.
- **Venue confound, declared in AMENDMENT-1 and unchanged.** Stack Exchange is
  one platform, non-software *within a software-shaped platform*; its members are
  technical enough to be there. This biases the arm toward tool-shaped need, so
  a null here is weak evidence against the domain hypothesis — and that is the
  main reason the domain question stays open rather than closing.

## Gates closed and gates left standing

**Closed:** G1, G4, the answerability sub-test, and G3's null branch
(permanently disarmed, not merely unfavourable).

**Left standing, and it is the one worth having:** the mission's candidate
source does **not** move out of software, because nothing here returned a
candidate — but neither does this experiment close the find-a-new-venue route.
Its own declared null branch was the thing that would have closed it, and that
branch was an artifact of the rubric. A null that cannot be computed cannot
close anything, so the route is **deferred with the reason recorded**, which is
a different standing from closed.

The one durable instrument gain is `view_count` as an arrival measure, and the
one durable correction is that **unanswered is not unserved**.

## Reproduce

```bash
python3 EXPERIMENTS/062-nonsw-need-shape/harvest.py     # arm 1, 1200 rows
python3 EXPERIMENTS/062-nonsw-need-shape/harvest2.py    # software control (partial; 429s)
python3 EXPERIMENTS/062-nonsw-need-shape/outcome.py     # every gate above
```

Raw: `raw/requests.jsonl` (per-request status), `raw/arm1.jsonl`,
`raw/outcome.json`, `raw/noremedy-classified.tsv` (all 110 rows classified),
`raw/answerability-top20.tsv`. Every number here is `observed` from those files.

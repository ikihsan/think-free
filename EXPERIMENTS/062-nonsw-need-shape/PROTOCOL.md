<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E062 — PROTOCOL

Declared 2026-10-08, session `2026-10-08-006`, VM `instance-20260717-0944`, before
any row of the new population was fetched or read.

## The question

Every population this mission has measured for candidate need comes from one route,
and that route is a software venue: GitHub issue trackers, PyPI, Hacker News, and
Stack Overflow. **Seven measurements say the seat for a candidate is empty**
(F029, F051, F039, F059, F081, F084, F085). Two readings of that emptiness have
never been separated:

- **(a) tool-solvable unmet need is scarce**, in which case no new venue helps and
  the mission's problem is structural; or
- **(b) the source is the constraint**, in which case the seat is empty *here* and
  a different population would return candidates.

This experiment measures one discriminator between them, and it is the cheapest one
available: **take a large population of publicly stated unmet needs from a domain
outside software, measure what fraction of them a self-contained program could
serve, and compare that fraction with the software corpus already on disk.**

### The candidate decision this changes

Stated in advance, because an audit of a discovery method is only worth running if
it moves a decision (owner brief §4).

- **If the non-software fraction is materially higher than the software control**,
  the mission's candidate source moves out of software, and the next session
  harvests candidates from that domain. This is an executable action, not a
  reading.
- **If it is comparable or lower**, then the seven emptiness measurements were
  never about software. "The seat is empty" is a fact about the *shape of human
  unmet need* — most unmet need is content, service, price, access, or other
  human work, and a program is not a remedy for it. That closes the
  find-a-new-venue route permanently, which is worth more than the null costs,
  because it is currently the route everything else is waiting on.

Either result is a decision, and neither result is a candidate. **This experiment
is not expected to produce a product, and the README must not imply that it did.**

## Population and arms

| arm | source | domain | what it carries |
|---|---|---|---|
| **1 (treatment)** | Steam per-game feature requests, ≥ 5 games | games | title, votes, **platform-recorded state** |
| **2 (control)** | the 1401-row Hacker News need corpus already on disk (`EXPERIMENTS/022-need-outcomes/raw/`, `EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl`) | software / tech | need text, no outcome |

**Why this venue, and why it is the only one named here.** It is large, public,
unauthenticated, non-software as a venue, and — the reason it is not interchangeable
with anything else reachable — **it records an outcome per request.** That is the
channel E039 measured as absent everywhere this mission has looked: the outcome of a
need is not recorded in the thread it was asked in (1 of 794 requesters replied
again, 0 of 77 whose need drew a link). A platform that writes the outcome down is
the only way to get at F042's `0 of 24 built it themselves` cell in a second
population.

**The confound I can name in advance, and the sub-test that handles it.** Game
modding is a software activity. A request whose remedy is a mod, plugin, config
file or script is *tool-shaped* but its requester is software-literate, so it does
not test the domain hypothesis. **Declared sub-test: every request is also labelled
`remedy-file` when its remedy is an artifact dropped into the game, and that label is
reported separately from the tool-shaped fraction.** The headline comparison is over
tool-shaped requests that are **not** `remedy-file`.

## Gates, all declared before any row was fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 300 rows across ≥ 5 distinct games, each carrying title, vote count and state; the harvest reconciled against each page's own row count | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 40 seeded control statements — 20 known tool-shaped, 20 known not — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the tool-shaped fraction of arm 1, with CI95, over ≥ 300 rows; and the same fraction over arm 2's rows | this is the result; no gate |
| **G4 outcome gradient** | the platform's state field separates at least two classes by ≥ 10 points in the still-open share, age-matched | the outcome channel carries no gradient here, so the reason this venue was chosen is not available. Record it; the G3 comparison still stands. |

**Positive control, stated as a requirement on the instrument, not on the world:**
the reader must recover seeded positives (G2). A rubric with no positive control is
the shape F029 took — 50 candidates screened, 0 survived, and the screens never
demonstrated they could find one.

**Denominators.** Every fraction is over rows read, and rows not read are reported
as rows not read. Per D082, an arm that produced no observation is a missing
observation, never a zero and never a denominator.

## The rubric, written before the rows

A stated need is **tool-shaped** when all three hold:

1. **Self-contained** — a program can serve it without the requester's own data,
   without their account, and without the platform or game operator changing
   anything.
2. **Repeatedly wanted** — the same program would serve other people who stated a
   comparable need. (Judged on the request's own text, not on a count this
   experiment cannot make.)
3. **Not a request for content, service, price, access, or human work.**

`remedy-file` is the narrower label from the confound above.

**Two readers** on an overlapping subsample, with κ reported, because E023's
withdrawal (F043, D055) was a one-reader defect at exactly this step and E029's
reader arm failed its control separation at κ = 0.5004 (F049).

## Ceiling, stated now

One platform; one retrieval route; HTML; one rubric with two readers over a
subsample; and a venue whose players are a self-selected population. This measures
the *shape* of one non-software population's unmet need. It does not measure demand,
does not measure adoption, and does not close any candidate.

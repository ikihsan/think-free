<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E028 — protocol: does the incumbent a prior-art screen named do what the clause asked?

Written 2026-10-05, task T-0072, **before any label was produced and before any
artifact documentation was fetched**. The question, the population rule, the
gates and the decision each verdict changes are declared here in that order.

## The question

Prior art is the largest single kill reason in this mission's record — **10 of
18** candidate deaths (`EXPERIMENTS/024-kill-reason-causes/`, F044) — and it is
the reason all twelve candidates from the six sealed reports were dropped. No
candidate has ever survived a prior-art screen here.

That verdict has been checked for **existence** and never for **fit**:

- E016 re-adjudicated 19 of the 19 harvest-side kills on three corpora with six
  positive controls and recovered 6 of 6 (F035). Its question was whether an
  artifact that plausibly serves the clause exists.
- E020's own H2 — *are the incumbents a screen names actually serving?* — is
  recorded `not evaluable` "because the instrument could not answer it".
- [`STATE.md`](../../STATE.md) carries it as a standing limitation: *"What has
  not been shown is that any need is served by the incumbents a screen names."*

**What nobody has measured is whether the named artifact does the thing the
clause asked for.** Two places in the record already gesture at the gap without
measuring it:

1. E016's note on its `atomic-distro` row: *"Recovery is of the category, not of
   the clause's distinguishing attribute: no returned artifact's text claims
   broad hardware and vendor support."*
2. `EXPERIMENTS/024-kill-reason-causes/rows.json` shows three sealed-report
   prior-art deaths — **A2** ("old decision-theoretic troubleshooting"), **C1**
   ("minimum-cost repair planning is prior art from 2007-2026"), **C3**
   ("REPAIR and earlier pottery-reassembly research establish substantial prior
   art") — that **name no artifact at all**.

**H1.** Among the candidates this mission killed for prior art, a material share
were killed by a **category match** rather than a **fit**: the named incumbent
is an instance of the wanted thing's category but does not meet the property
that distinguished the wanted thing from that category.

H1 has two live readings, and they change the mission differently:

- **H1a, the world is saturated.** The incumbents do what was needed. The
  twelve deaths and the corpus closure stand for a *measured* reason rather than
  on the absence of a hit, and a screening rule that records the attribute test
  replaces one that records a count.
- **H1b, the screen is misattributing.** The incumbents do not do what was
  needed. The prior-art verdict is not a valid kill for those rows, they reopen,
  and item 0's selection axis cannot be novelty on prior-art grounds.

## The distinction being measured

A **category** is what kind of thing the clause asks for — an HN client, a
nesting tool, a map-annotation platform, a session reconciler. A
**distinguishing attribute** is the property the clause states that an ordinary
instance of that category would not have. A verdict is a **fit** only when the
artifact satisfies the attribute; a **category-only** match is the artifact
being an instance of the category.

E016's own `served` boolean does not separate the two. That is the measurement.

## Population rule

Declared before the first label. The population is:

1. **Every row whose single declared kill category is `prior_art`** in
   `EXPERIMENTS/024-kill-reason-causes/rows.json` — **10 rows** (A2, A3, B3, B4,
   C1, C3, C4, D3, D4, ORIGIN). These are the deaths of the twelve sealed-report
   candidates, and eight of the ten are outside software.
2. **Every row with `cause == "prior_art"`** in
   `EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl` — **19 rows**. F029
   drew these 50 from 1401 harvested need statements.

**29 prior-art deaths, read-only from two existing captures. No new harvesting,
no new population, no new population claim.** Any row that cannot be labelled
carries a stated reason and stays in the denominator.

### The requirement text a reader is given

F047 is the reason this is stated as a rule: 31 of E012's verdicts were
assigned from a regex-extracted clause rather than the comment, and six of
fifteen `vague` kills were false of the comment.

- Harvest rows: the **full comment text** from `screened.jsonl`, never the
  `clause` field.
- Sealed rows: the report's own **"Possibility examined"** statement from the
  inventory table in the primary report named by `rows.json`'s `source` field,
  plus the paragraph stating the candidate's mechanism. Never `deciding_sentence`,
  `reason_text`, or any prior-art sentence.

A reader is given the requirement text and **no verdict, no kill reason, no
incumbent name, and no other reader's labels**.

### The incumbents a reader is given

The artifacts a screen **named**, which is a fact about the record and not a
judgement: the `artifacts` arrays in E016's `raw/attributions.jsonl` for harvest
rows, and the artifacts named inside `rows.json`'s `reason_text` for sealed rows.
Each is paired with **its own published documentation**, fetched into `raw/`, and
the reader sees that text.

## Procedure, in this order

1. **C1, mismatched-pairing control, before any real pairing.** Every
   requirement is also paired with an incumbent named for a *different* row.
   A reader that calls mismatched pairings a fit is not measuring fit. Declared
   threshold: **both readers must label at least 90% of mismatched pairings
   `does_not_serve`.** Below that the run reports `not_evaluated` and no fit
   table is published.
2. **C2, positive control, before any real pairing.** Rows E016 already
   declared served beyond argument — `webp-encode`, where `sharp` carries
   436,835,441 downloads per month — must be recovered as a fit by both
   readers.
3. **C3, lexical calibration, before any fit label.** A lexical
   attribute-match index over the artifact's own documentation is computed and
   its **base rate is measured on the C1 mismatched pairings**. An index that
   cannot separate matched from mismatched pairings is reported and not used as
   evidence; it is never quoted without its C1 rate beside it. This is the
   control F043 needed and did not have.
4. **Step A, the distinguishing attribute, from the requirement text alone.**
   A reader who has not seen any incumbent writes the property the wanted thing
   must have that an ordinary instance of its category would not, or
   `no_distinguishing_attribute`. Deriving the attribute **before** seeing the
   documentation is deliberate: it stops the incumbent's documentation from
   shaping what is then asked of it.
5. **Step B, the fit label**, given the requirement text, the Step A attribute,
   and the artifact's own documentation: `serves`, `partial`, `does_not_serve`,
   `unreadable`.
6. **Two readers, blind to each other, on both steps.** Readers are separate
   contexts that see neither the screen's verdict nor the other's labels.
7. **Agreement is computed on the grouping the decision consumes** (D059): a
   four-category κ over the fit population, and a separate agreement figure for
   Step A.

## Gates

| gate | declared | meaning |
|---|---|---|
| **A1, instrument validity** | C1 ≥ 90% and C2 recovered by both readers | the pairing procedure measures fit and not agreement |
| **A2, reader agreement** | Cohen's κ ≥ 0.6 over the four-category fit scheme | below it the fit table is reported `inconclusive`, not a result |
| **A3, kill gate** | share of `does_not_serve` over the fit population has Wilson 95% **lower bound ≥ 0.20** | the prior-art verdict is **not valid at the recorded population**; the affected rows reopen and item 0's selection axis cannot be novelty |
| **B1, the opposite gate** | share of `serves` has Wilson 95% **lower bound ≥ 0.60** | the verdict is sound on what it was asked about; the deaths stand for a measured reason |
| **A4, `not_evaluated`** | fires if the fit population is under 10 rows, or if C1 or C2 fails, or if both readers label the population identically on every row | a fourth answer, declared **now**, because adding it after the measurement is indistinguishable from adding it to make a result look better |

Between A3 and B1, with A4 not firing, the verdict is **`inconclusive` with the
measured distribution reported**, never rounded to either side.

**κ = 1.0 is not a pass.** It is a warning that the four-category scheme carried
no information on this population, and the run says so in words rather than
reporting it as agreement.

## What each verdict changes, declared in advance

- **A3 fires** → the prior-art deaths in the `does_not_serve` set reopen as
  candidates; item 0d's corpus closure is withdrawn **for those rows only**;
  F044's plurality reading is restated as *prior art, frequently misattributed*.
- **B1 fires** → the twelve deaths and the corpus closure stand on a measured
  reason; a screening rule that records the attribute test and its artifact text
  replaces a rule that records a count.
- **A4 fires** → no verdict; the instrument is refused and the population is
  reported as unmeasured.
- **Otherwise** → the measured distribution and its resolution limit, with no
  claim about validity either way.

**Nothing here reopens F029's 0-of-50 by itself.** That is a composition
finding about the corpus and F047 confirmed its closure by a re-read; this
experiment can only decide whether *the prior-art column of that screen* was a
valid test.

## Prior art on this method

Stated so the record does not carry an unexamined novelty claim: attributing
competing products to a requirement's distinguishing attributes is ordinary
competitive and feature-gap analysis, and requirements-engineering methods have
published on it for decades. **No novelty is claimed for the method.** The claim
under test is empirical and local: *that this mission's own prior-art verdicts
were fit tests*, which is a question about a specific set of 29 recorded
verdicts and can be settled by reading primary sources.

## Ceilings, declared before the run

- One population of 29 rows from two screens, both made by one agent's
  judgement; the population is what this mission happened to kill, not a sample
  of anything.
- Two readers are **the same model family**. MISSION.md records that agents
  share model biases and are **not independent human validation**. κ measures
  their consistency, not their correctness.
- Artifact documentation is read at one instant, 2026-10-05. An artifact that
  served the clause once and no longer does, or whose documentation never said
  so, is invisible here in both directions.
- An artifact whose own documentation is silent is `unreadable`, not
  `does_not_serve`. The fit is being tested against what the vendor claims, and
  against the documentation a practitioner would have read before building.
- 19 of the 29 rows are one community's need statements; the ten sealed rows
  are the strongest available contrast because eight are outside software.
<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E143 — Cross Validated: the highest program-density untouched venue, served?

Predeclared **before any population row is fetched**.
Follows E126 (`../126-stackoverflow-service-test/`), the mission's
soundest service design, which fixed E091's defects.

## Question

On **Cross Validated** (`stats.stackexchange.com`) — the largest
untouched non-software Q&A venue, whose community's native idiom is
the statistical computation (answers are very often R/Python code,
configs, or self-contained scripts) — what share of the highest-arrival
recent unanswered questions is:

1. **question-shaped** (the remedy is an explanation or a snippet the
   asker applies with judgment), and of those, what share is
   **answerable** (general knowledge suffices) versus **specific**
   (needs the asker's logs, versions, or environment, absent from the
   post)?
2. **execution-shaped** (the remedy is an action on the asker's own
   code, data, or system that produces an artifact — refactor,
   migrate, convert, build), split `program` (a self-contained
   script/tool the asker runs) versus `manual` (needs the asker's
   judgment or system access)?
3. of the **answerable question-shaped** class, what share does a free
   general assistant serve in full?

**Why this venue.** The venue sweep (E126/E127) closed the Q&A venue
classes: non-software SE (E062), Anova appliance (E091), Home
Improvement appliance (E092), Stack Overflow (E126). All served; the
program-shaped residue (6/299 in SO) was served by prior art. Cross
Validated is the largest untouched venue and the one where
program-shaped resolutions are MOST native — statistics answers are
computations. The candidate-seat question is whether the
"program-shaped → served by a free assistant" law is structural: if
it holds even here, where programs are the native idiom, the law is
a property of the assistant, not of the venue. If unserved
program-shaped rows exist, that is a concrete candidate signal.

**The new measurement.** The program-shaped residue rate in a
high-program-density venue (SO was 2%), and whether any residue is
unserved. E126 could not test this: SO's residue was 2% and was not
attempted. Cross Valuated's higher program-density is the venue
where the residue is most likely to be large enough to measure.

## Domain selection rule (stated, not by comfort)

Among Stack Exchange sites — the platform class with the most
validated instrument (public questions, `view_count` arrival
metadata, answers as serving signal) — choose the site in a domain
the mission has **not** measured as a need-venue, where:

- (a) the domain is **non-software** (the practitioner is a domain
  expert — statistician, analyst, researcher — not a programmer);
- (b) the resolution is **plausibly a self-contained artifact**
  (script, calculation, config) — the only class a tool could serve,
  and the one the candidate-seat question needs;
- (c) the site is **large enough to justify a candidate**
  (> 10k questions).

Among qualifying sites, choose the **largest by question count**.
Cross Validated (~200k questions) is the top hit under this rule.
Data Science SE and GIS SE are the next candidates; both are more
software-adjacent. Bioinformatics SE is excluded: E100 measured it
as a fault-code source.

## Population and sample

- **Venue:** `site=stats`, Stack Exchange API v2.3 (unauthenticated),
  the same surface E062/E079/E092/E126 used.
- **Pool:** questions with `accepted=false` (no accepted answer)
  **and** `creation_date >= 2025-01-01` (unix 1735689600; recency
  declared so 2026 methods are the population, not a decade of
  accumulated legacy).
- **Two arms, because the API cannot rank by `view_count`:**
  - **Arm A (votes):** `sort=votes&order=desc`, 2 pages of 100.
    The vote-stratum limitation is declared, not hidden (E033/E034,
    E126's stratum finding).
  - **Arm B (creation):** `sort=creation&order=desc`, 1 page of
    100 — the newest unanswered, a second stratum. Composition
    agreement between arms bounds the stratum concern; disagreement
    *is* the finding.
- **`view_count` is a covariate, never a selection rule** (E034/E113's
  lesson). The attempt sample is the top 20 by `view_count` **within**
  Arm A's question-shaped rows, after screening.

## Screening (title + body only, before any answer or comment is read)

Each row is classified by shape:

- **question** — the remedy is an explanation or snippet the asker
  applies with judgment. Sub-class:
  - `answerable` — general knowledge suffices;
  - `specific` — the answer requires the asker's logs, versions, or
    environment, which the post does not contain.
- **execution** — the remedy is an action on the asker's own code,
  data, or system producing an artifact. Sub-class:
  - `program` — a self-contained script/tool the asker runs
    (E091's K2 shape);
  - `manual` — needs the asker's judgment or direct system access.
- **other** — meta, opinion, off-topic, typo, purchase, or
  debugging-please-type-this-for-me with no general content.

## Gates (declared before measurement)

| gate | rule |
|---|---|
| **G0 discrimination** | 20 construction-labelled probes (10 answerable, 10 specific), labels known by construction and independent of any thread. Pass: ≥ 9/10 answered, ≥ 9/10 declined. Fail: the instrument fails and no rate is read. |
| **G1 population** | the two arms together contain ≥ 60 question-shaped rows of ≥ 300 fetched. Fail: the class is too thin at high arrival; the line narrows and closes. |
| **G2 composition** | reported per arm and pooled, with Wilson CI95. No threshold — the mix is the finding. |
| **K1 served share** (answerable class, n = 20) | Wilson CI95. Lower bound ≥ 0.50: served — the venue closes like the others. Upper bound < 0.50: an unserved answerable population exists — the line reopens with the concrete reason. Straddling: extend the sample once, to 40 (E092's rule). |
| **K2 execution share** | the execution-shaped share, pooled, with its `program`/`manual` split. Reported, not gated: it is the measurement the venue exists to produce. |
| **K3 program-shaped residue** | count of rows whose remedy is a self-contained program, across all screened rows. Zero: no program-shaped population exists regardless of shares (E091's K2 shape). |

## Attempt discipline (E091's defects carried forward)

1. Attempts are written from title + body, from general knowledge
   only — no web, no thread content — and committed to
   `attempts.jsonl` **before** any answer or comment is read. Every
   row carries an explicit `attempt_first` flag.
2. Grading reads the thread (answers, accepted answer, comments) and
   grades served/unserved with a reason; every row's flag is checked
   against its own reason (E091 defect 2).
3. Every denominator is filled before any rate is computed (E091
   defect 3).
4. The attempt arm is the same model family as the grader (the
   E062/E091/E092/E126 shape) — declared as a limitation, not hidden.

## Served definition (E092's, unchanged)

**Served:** the attempt names the likely fault and the action that
resolves it, at the specificity the thread's own resolution reaches,
and is consistent with the thread's converged answer. **Unserved:**
wrong fault, vacuous ("could be many things"), or a correct
resolution that requires information not in general knowledge.

## What this does not establish

- Two strata, not the whole pool; vote-sorted and creation-sorted
  arms over-represent their strata (E033/E034's lesson, declared).
- One reader (the session's model); no human baseline.
- `answered=false` means no *accepted* answer; threads may still
  carry converged answers, which grading uses.
- The execution share is a property of this venue's curation and
  population as much as of the need.
- A high program-density venue is not the only venue where a
  program-shaped residue could be large; it is the largest such
  untouched venue.

## Decision this changes

Either E143 supplies the composition that every future
high-program-density-venue screen needs — and, if the answerable
class is unserved or the program-shaped residue is large and
unserved, a concrete population a tool could serve — or it extends
the composition finding to the largest untouched venue and closes
the candidate-seat question more firmly. Both outcomes are recorded
as such.

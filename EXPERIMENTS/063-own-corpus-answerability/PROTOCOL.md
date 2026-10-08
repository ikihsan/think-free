<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E063 — PROTOCOL

Declared 2026-10-08, session `2026-10-08-013`, VM `instance-20260717-0944`, before any
row of either population was sampled or read for this measurement.

## The claim under test, in one sentence

**Every candidate population this mission has ever screened came from a route that
collects *statements* of need, and a free general assistant answers in full today a
majority of those statements — so the route selects statements, not unmet need.**

Scope: two corpora already on disk, in software/tech. It says nothing about any
other route, about adoption, or about whether a tool could be built for the minority
that resists. It is a claim about the *sampling instrument*, not about the world.

## Why this is the next experiment rather than another audit

E062 (F096) measured the gap between a statement of need and service in a
non-software population: **17 of the top 20 arrival-ranked unremedied needs are
answered in full today by a free general assistant.** Nobody has run that
instrument on the corpora the mission's own candidate screens consumed. Seven
emptiness measurements (F029, F039, F051, F059, F081, F084, F085) all read a
need-statement corpus and concluded "no candidate". If the instrument selects
served statements, all seven are *correct about the domain they sampled and
irrelevant as evidence about unmet need*, and the route — not the domains — is
what is empty.

## The candidate decision this changes

Stated in advance (owner brief §4: an audit is worth running only if it moves a
decision).

- **If the served share of arm A is ≥ 0.60**, the need-statement route is
  **retired as a candidate source**. No further session harvests another software
  need corpus and no further screen is applied to one. The replacement class is
  named in advance so the next session does not re-derive it: a population where
  the need is **not stated in words**, i.e. where the work is done in public and
  leaves traces, so arrivals can be counted per task rather than per complaint.
- **If it is < 0.60**, the route stands, the emptiness measurements were about
  their domains, and the next action is unchanged: sharpen the screen on this
  route.

Both results are decisions. Neither is a candidate, and the README must not imply
otherwise.

## Populations, sampling, denominators

| arm | population | on disk | sample |
|---|---|---|---|
| **A (primary)** | Hacker News need statements | 1401 rows, `EXPERIMENTS/012-candidate-harvest/raw/hn_needs_2026-10-04.jsonl` | deterministic stride, every 20th row, **70 rows** |
| **B (secondary)** | GitHub issues behind the `stg` demand claim | 189 rows, `EXPERIMENTS/045-demand-evidence/raw/issues.jsonl` | deterministic stride, every 6th row, **31 rows** |
| **C (controls)** | seeded needs | written by this experiment | **20**: 10 known-served, 10 known-unserved |

Arm A is the mission's largest and only outcome-free need corpus, and the one
E012's 50-candidate screen consumed. Arm B is the corpus behind the one artifact
this mission built. **Arm B carries a declared asymmetry**: its rows hold the title
and a lead excerpt, not the full issue body, so its served share is measured on
less of the requester's own text and is reported as a bound, not as the headline.

Stride sampling, not screening: no row is dropped after reading. Rows read =
denominator; rows not read are reported as rows not read (D082: a missing
observation is never a zero and never a denominator).

## The baseline: the strongest accessible alternative

**A free general-purpose assistant, answering from its own general knowledge and,
where the answer turns on whether an artifact exists *today*, one public-index or
open-web check.** Any requester has this for free and instantly. It is the same
baseline F096 used, so the two arms are comparable, and it is stronger than
knowledge alone because it stops me calling a need served on the strength of a tool
name that does not exist.

## Gates, declared before any row was sampled

| gate | condition | if not met |
|---|---|---|
| **G1 instrument control** | the labeller recovers **≥ 9 of 10** seeded known-served and **≥ 9 of 10** seeded known-unserved needs, blind, interleaved with the sample in the same format | the share is not measurable. Stop; record the instrument defect. A rubric that cannot find a served row and a rubric that cannot find an unserved row both measure nothing. |
| **G2 remedy verification** | of the artifacts named as remedies in a bounded subsample, **≥ 90% resolve** on a public index or the open web, or are labelled `named-artifact-unverified` and excluded from the served numerator | the baseline is being inflated by names that do not exist (F036's shape). Stop. |
| **G3 reader stability** | a second blind pass over **40** sampled rows gives Cohen's κ ≥ 0.60 against the first | the labels are not stable under re-reading; the share is reported with that caveat. |
| **G4 the measurement** | served share per arm with Wilson CI95, over the full declared sample | this is the result; no gate |

**Positive controls are a requirement on the instrument, not on the world** — the
shape F029 took: 50 candidates screened, 0 survived, and no screen had ever
demonstrated it could find one.

## Labels

A row is **served** when a free general assistant hands the requester a remedy they
could execute today, using only what the requester already holds. Otherwise:

- `served-method-value-missing` — the method is free knowledge, a required value or
  spec is not public (F097's shape).
- `unserved-data-absent` — no program can answer because the record was never
  created.
- `unserved-remedy-is-human` — the need is service, access, price or human work.
- `unserved-open` — genuinely not served. **This label must be argued in one line**;
  it is the only label that can open a candidate, so it is the one most likely to
  be self-granted, and G1's unserved controls exist to catch exactly that.

## Named asymmetries, declared now

- **The labeller is the model that would build the tool** and is simultaneously the
  free instant incumbent. The question asked is therefore about *incumbence* — is
  there a gap between what a free assistant supplies and what the requester needed —
  not about whether I am good at the task. This is F096's asymmetry, unchanged.
- **The second reader is the same model** in a separate blind pass. κ measures label
  stability under re-reading, not independent judgement. Stated so it is not read as
  E029's reader arm (F049), which used two readers that differed.
- **Today, not then.** Arm A is 2–8 months old and arm B ranges from 2010 to 2026.
  This measures whether *today's* statements of need are served by *today's*
  incumbent. It cannot tell you what was true when they were written.
- **Labelling cost is not attempt cost.** A real requester would not read 1401 rows;
  this experiment measures what an assistant can supply for a need, not whether a
  requester would think to ask.

## Ceiling, stated now

Two corpora, one route, one labeller, one rubric, hand-written attempts with no
retrieval except the G2 verification step. This measures **the served share of
stated need in two software corpora**. It does not measure demand, adoption, or
difficulty, it does not reopen any closed candidate, and a low served share would
not by itself open one.

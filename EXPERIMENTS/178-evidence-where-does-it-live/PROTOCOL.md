<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-17
-->

# E178 PROTOCOL — where the missing evidence lives, and whether the round trip already carries it

**Date opened:** 2026-10-17. **Status:** pre-declared before the comment fetch,
before the comment lexicon is applied to any row of the 46, and before the
re-key reader sees any row. Nothing below may be edited after the first fetch,
except by an amendment file that names what changed and why.

## The build decision this experiment decides

E177 measured the mission's first service ceiling on a class it had never
separated: on 46 of the 100 highest-arrival answered Stack Overflow questions,
**the key answer's resolution depends on at least one fact or artefact the
question does not contain**, and on that class a free general assistant reaches
**12/30 = 0.4000** against **26/30 = 0.8667** on the self-contained half
(gap +0.4667, Fisher p = 0.000368; F136, D118). The population is named. **No
mechanism is named, and a mechanism is what a candidate needs.**

There are exactly two mechanisms this class could support, and they need
opposite evidence:

| mechanism | what it does | needs | kill |
|---|---|---|---|
| **FETCH** | reads a published artefact — changelog, release note, spec, commit, upstream thread — and grounds the answer in it | the missing evidence to be in something the project **publishes** | `publishable` too small |
| **ASK** | names the one fact that discriminates between the causes the posted symptoms allow, and asks for that | the missing evidence to be something the **person holds** | FETCH's share is large, or the venue already asks |

Nothing else follows from E177's number. So this experiment measures the one
thing that separates them, on the 46 rows themselves, with three instruments.

## The question, in one sentence

**For each of the 46, what single fact or artefact does the key answer depend
on and the question does not contain, where does that thing live, does its
value change the resolution, and did the thread itself ever ask for it?**

Four fields, one per row: `missing_evidence`, `where`, `discriminating`, and the
thread's own behaviour.

### The buckets, declared before any row is read

| bucket | meaning | fetchable by a tool? |
|---|---|---|
| `publishable` | the organisation that owns the answer publishes the fact — changelog, release note, spec, commit, upstream issue, documentation of its own behaviour, or its own source | yes, in principle |
| `asker_only` | a value or artefact only the reporter holds — their version output, their config, their data, their platform, their steps | no; it must be **asked for**, one round trip |
| `third_party` | it lives in another organisation's system, store or account | no; the ceiling is that third party's own reporting |
| `none` | the reader judges the resolution reachable from the question's own text | — |

`none` is a legal answer and it is the experiment's second coder: every `none`
is a row E177's CLF called EVID and this reader does not. **No row may be left
unclassified.** An unclassifiable row is a `none` with `basis` saying so, and
the count is reported separately, because a reader that abstains silently and a
reader that says "I cannot tell" are different instruments.

### `discriminating`, declared

**`true`** if the key answer's resolution would plausibly be a *different
resolution* if that fact took a different value — the posted symptoms leave
several causes open and this fact picks between them. **`false`** if the
resolution is the same either way and the fact only confirms it. This is the
field E177's addendum turned on, speculatively, on one reader's 30 rows
(**18 of 18 misses load-bearing, 8 of 12 reaches not**); here it is asked
directly, blind to verdicts.

## The population

**E177's 46 EVID rows, verbatim, from `EXPERIMENTS/177-evidence-gated-need/labels.json`.**
Reused, and therefore **conditional**: nothing here is a prevalence estimate on
any pool, and no rate here may be compared to a rate from a fresh draw. What a
fresh draw would add to these 46 rows is a composition, and composition is what
this experiment measures.

E177's own label file is **not shown to the re-key reader** (control G0d), and
the reader is given the question and the key answer in a wrapper that carries
no arm, no kind, no verdict and no view count of any other row.

## The three measurements

### M1 — the thread's own round trip (automatic, all 46, no reader)

Fetch, for each of the 46: the **question's comments** and the **key answer's
comments**. Four numbers, then two more:

| # | number | meaning |
|---|---|---|
| 1 | `has_comment` | share of the 46 whose question carries at least one comment |
| 2 | `has_ask` | share whose question comments contain an **ask** (lexicon below) |
| 3 | `ask_then_asker` | share where a comment by the **question's owner** appears after an ask — the person actually went and got the fact |
| 4 | `answer_asks` | share whose key answer carries an ask, i.e. the answerer asked the asker for the fact |
| 5 | `evidence_in_comments` | share where the M2 reader's `missing_evidence` tokens reach **0.5 containment** somewhere in the comments (the ask was answered in the thread) |
| 6 | `discriminating_and_asked` | the joint that matters for ASK: an ask that supplied a discriminating fact |

**The ask lexicon, fixed here before the fetch.** A comment is an **ask** if
either rule fires:

- **A (request form):** it contains a question mark, **or** it matches one of
  the leading forms — `what|which|when|where|why|who|how|can you|could you|do
  you|did you|are you|is there|have you|would you|can we|could we|any idea|which
  version|please` — as a word in the first 12 tokens; **or**
- **B (artefact request):** it contains an artefact word (`version|build|log|
  code|config|configuration|error|message|output|trace|stack|screenshot|example|
  repro|reproduce|minimal|snippet|source|branch|commit|dependency|package|
  library|environment|env`) **and** a supply word (`post|share|paste|show|
  add|include|provide|exact|full|your|you|output|result|contents|file`).

Both rules are case-insensitive. **They are a proxy**: a request can be phrased
outside the lexicon ("Can we see the schema?" fires on the artefact word
`schema`… no — it does not, and that miss is counted, not corrected). The
proxy's error rate is measured by control **G0a** before any population row is
read.

### M2 — the re-key (one reader, all 46, blind)

[`READER-INSTRUCTION.md`](READER-INSTRUCTION.md), committed before the run, is
given verbatim to one reader per batch of rows. Outputs `rekey.jsonl`, one JSON
object per row, validated by `score.py` against the schema.

**One reader, same family as every reader in this record.** MISSION.md already
says agents are not independent human validation. This reader's independence is
from E177's CLF (it never sees `labels.json`), not from the model's biases.

### M3 — the inherited label's grounding (automatic, all 46, no reader)

E177's CLF wrote a free-text `missing_evidence` for each of the 46. Two token
containments, E169's instrument, the same tokenizer and stopword list as
`census.py`:

- **`already_present`**: share of the named evidence's tokens appearing in the
  **question**. **>= 0.5 is a defect**: the fact the label says is missing is
  in the question. There is no paraphrase escape here — the fact is either in
  the text or not — which is why this is the sharper of the two.
- **`used`**: share appearing in the **key answer**. `< 0.5` means the answer
  never mentions it, which is *suggestive* of a label naming something the
  answer does not use, but it is **not** a defect: a resolution can depend on a
  fact without restating it. Reported as a distribution and never used to drop a
  row.

**M3 is one-sided and is declared one-sided here.** It examines the EVID rows
only. E178 does **not** re-read the 52 SELF rows, so it cannot measure how many
SELF rows are really EVID, and every precision statement below is a bound on
EVID precision only. Re-opening the SELF arm is the move E177's addendum
declined on the same grounds, and it is declined again here rather than done
quietly.

## Controls, declared before measurement

- **G0a — the ask lexicon recovers independent real positives.** Five control
  questions drawn **from outside the 46**, fixed by rule before the fetch: the
  five SELF-arm rows of E177's population with the highest `comment_count` on
  the default filter. Their question comments are hand-labelled `ask` / `not
  ask` by one reader, **before** the lexicon is applied to any of them, and
  lexicon precision and recall are reported against that hand labelling.
  **Declared bar: recall >= 4 of the hand-labelled asks and 0 of the hand-
  labelled non-asks classified as asks.** A lexicon that misses a third of real
  requests makes every M1 rate a **lower bound**, and that is what will be
  reported.
- **G0b — the fetch is complete.** Every one of the 46 question ids and every
  key answer id must return a response with `has_more == false` and no error,
  and the per-question comment count must equal the `comment_count` the default
  filter reports for that question. Any shortfall is **named per id**; nothing
  is imputed.
- **G0c — the reader is an instrument.** All 46 rows present exactly once, every
  field present, every value in the declared vocabulary, and `basis` non-empty
  and quoting the key answer. **Any violation makes M2 `not_established`** and
  the bucket counts are reported as the reader's raw output, not as a rate.
- **G0d — the reader was blind.** `grep` over the reader's input directory must
  find none of the inherited strings: no `arm`, no `kind`, no `missing_evidence`
  from `labels.json`, no `reached` verdict from `score/verdicts.jsonl`, and no
  qid other than the batch's own.

## Gates, declared before measurement

- **G1 (the standing kill, inherited from `STATE-next-actions.md`).**
  **`publishable` < 0.50 of the 46** → the missing evidence is mostly something
  the asker holds; the FETCH route closes; **E177's population closes with no
  candidate**; the only surviving route is ASK, and its next step is decided by
  G4 rather than by this gate.
- **G4 (the incumbent check, new here).** **`has_ask` >= 0.50 of the 46 and
  `ask_then_asker` >= 0.25** → the venue's own workflow already runs the round
  trip, on the very rows this experiment measures, and the person supplies the
  fact. Then the honest statement about the class is **not** "unserved": it is
  *served by an interaction that already exists, and unreachable by one-shot
  answering*, and any ASK-based candidate must beat that interaction rather than
  replace an absence.
- **G5 (the reader's precision).** **`none` > 9 of the 46** → this reader
  disagrees with CLF on more than a fifth of the class, so EVID precision on
  this population is **below 0.80** and every number in E177 that carries the
  class's size is conditional on a single reader of unestablished precision.
  **The E177 headline is still not recomputed** — choosing rows to drop after
  seeing which arm scored is the fitting this record has been burned by twice.

## A comparison declared in advance, because it is the reframing's real test

E177's addendum claims the class is not "questions missing a fact" but
**"questions whose posted symptoms underdetermine the cause"**, on one reader's
post-hoc reading. M2 measures that claim properly: join `discriminating` to
E177's per-row `reached` verdict.

```
p(discriminating | missed)   vs   p(discriminating | reached)
declared bar: gap >= 0.20 and Fisher exact two-sided p < 0.10
```

**Declared ceilings, in advance:** the reader never saw the verdicts, but the
verdicts are E177's, produced by an instrument whose arms are CLF's labels, and
CLF's labels are what this experiment is re-keying. So a `none` row sits
entirely on one side of this comparison by construction. **The comparison is
reported as exploratory and is not a gate.** Its only claim is whether the
*shape* the addendum described reproduces on a blind reader over all 46.

## Ceilings, declared up front

- **Conditional, not prevalence.** E177's draw is reused from E175, which
  reused E168's method. No number here is a rate on any pool.
- **Comments are not the thread.** Asker **edits to the question body** are
  invisible to M1 except through the API's revision record, which this
  experiment does not fetch. On Stack Overflow, editing the question *is* the
  canonical way to supply a missing fact, so **M1 under-counts the round trip
  by an unknown amount and every M1 number is a lower bound.** This is the
  largest single ceiling in the experiment and it is declared here, not
  discovered afterwards.
- **The lexicon under-counts asks** (G0a measures how much).
- **M2 is one reader, same family, blind to labels but not to the key answer** —
  it judges the resolution by reading the resolution, which is what CLF did.
  Agreement between two same-family readers is not two independent codings.
- **n = 46 and the gate is a decision rule.** At n = 46, a share of 0.50 has a
  Wilson 95% interval of roughly [0.36, 0.64]. **G1 cannot distinguish 0.36 from
  0.50**, so it decides which route the next session spends its budget on, not
  whether the class is fetchable. Every G-share is reported with its interval so
  the next session can see how thin it was.
- **`third_party` is a ceiling, not a source.** If the fact lives in another
  organisation's system, that organisation's own reporting is the ceiling on any
  answer, whatever the tool.
- **No product is proposed by this experiment.** It produces a bucket
  distribution, a precision bound, and a served-or-not reading of the venue's own
  workflow.

## Not to be run here

E177's own exclusion list stands: E176 as written (a third classification of the
same rows by the same instrument), E170's global arm, another view-count domain
(D105, F133), and a fresh draw of E177's comparison before the composition of
the 46 is examined.
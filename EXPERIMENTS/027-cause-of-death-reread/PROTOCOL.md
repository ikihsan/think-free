# E027 protocol — is F029's cause of death an artefact of the clause extractor?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

**Written 2026-10-05, before any row was classified.** Task T-0071. Every
declaration below is fixed before the classifications in `results.json` exist.

## The belief under test

F029 screened 50 mechanically-drawn need statements from Hacker News and
**0 survived**: `prior_art` 19, `vague` 15, `not_a_software_need` 12,
`needs_hardware` 4. That result closed the live-need generator (D049),
emptied item 0d's invention seat, and is carried in four files as a fact about
the world's stated needs.

**31 of the 50 verdicts were assigned from a clause, not from the comment.**
The clause is produced by `sample_needs.py::clause()` as *the text between the
matched trigger phrase and the first sentence break*, capped at 300
characters. Two recorded consequences, both visible in the committed file
before this protocol existed:

1. **Thirteen of the 31 carry at least 20 words of comment text after the
   clause** — the rest of the comment the screen never read. Median residual
   across all 50 is 0, so this is a minority shape, not the whole population.
2. **Three of the 50 clauses are not substrings of their own comment text**,
   all from the 300-character cap or the first-sentence split.

One recorded reason is a claim about the whole comment that was never checked:
index 10's verdict asserts *"no mechanism stated anywhere in the comment"*.
F030 established that a prior-art verdict from one query is wrong in both
directions; this is the same shape one stage earlier — a verdict about a
document, taken from an extract of it.

## The question

**Are the 31 clause-based causes of death properties of the needs, or of the
extraction rule?**

## Population, stated by rule not by taste

The 31 rows of `EXPERIMENTS/012-candidate-harvest/raw/screened.jsonl` whose
`cause` is one of `vague`, `not_a_software_need`, `needs_hardware` — the three
categories a mechanism screen decides by reading prose. **The `prior_art` 19
are excluded and are not re-read**: that category was already re-adjudicated on
three corpora by E016, which is a different and stronger procedure, and
re-reading it here would add a weaker second opinion to a settled question.

Each row is presented as **id, date, story, trigger, and the full comment
text**. The original `cause` and `reason` are withheld from the classifier.

## Two independent readers, because F044's ceiling was exactly this

`EXPERIMENTS/024-kill-reason-causes/` counted 20 kill reasons with **one reader
and no second coder at a one-row margin**, and named that as its own ceiling.
E023 measured κ = 0.923 for a second reader on an identical population, and that
number changed what the experiment was allowed to say. This protocol therefore
declares two readers mandatory, not optional.

- **Reader R** classifies all 31 rows from the full comment, blind to the
  original verdict.
- **Reader S** classifies all 31 rows from the full comment, blind to both the
  original verdict and Reader R's answers.
- **Cohen's κ is computed** and reported whatever it is. A κ below 0.6 makes the
  restated table `inconclusive` and no cause share from this experiment is
  reported as a fact.

Both readers are the same model family as the original screen, which E016
already declared as its known limit: they are not blind to how the original
phrased its reasons, only to the labels themselves. Recorded, not repaired.

## Categories, fixed before the classification

A row takes exactly one. The three clause-based categories are kept because
they are the ones under test; `prior_art` and `mechanism` are added because a
reader who finds a stated mechanism has to be able to say what to do with it.

| category | rule |
|---|---|
| `mechanism_stated` | the full comment names a thing that could be built and a way it would work, whether or not anyone built it |
| `prior_art` | the full comment names an existing artifact serving the need |
| `self_built` | the commenter says they built it themselves |
| `not_a_software_need` | asks for a price, a regulation, a community, a document, or a person's behaviour |
| `needs_hardware` | the mechanism requires a device, a room, or a person present |
| `still_vague` | none of the above is present in the full comment |

`mechanism_stated` is deliberately generous: it asks whether a mechanism is
*stated*, not whether it is good. **This experiment measures the screens'
recall, not a candidate's quality, and no surviving row is a candidate.**

## Gates, declared before the first classification

- **A1 (population integrity).** All 31 clause-killed rows are present, and
  every one carries a non-empty `text`. Below 31, the run reports `not
  evaluable`.
- **B1 (reader agreement).** Cohen's κ ≥ **0.6** between R and S over the six
  categories. Below it the restated table is `inconclusive`.
- **C1 (the kill gate, load-bearing).** If **≥ 5 of the 31** rows receive
  `mechanism_stated`, `self_built`, or `prior_art` from the full text where the
  clause-based screen killed them for a different reason, then **the clause
  extraction rule is a load-bearing cause of F029's 0-of-50**, the cause table
  is restated, and `vague` as a cause of death is withdrawn at its recorded
  size. At **≤ 2**, the extraction rule is not the cause and F029's table
  stands as measured. Between 3 and 4 the distribution is reported and the
  verdict is refused, because one reader's judgement is then decisive for the
  whole reading — the same margin F044 named and E023 closed with a second
  reader.

**What would make this a false positive**, declared before the run: a reader
who marks `mechanism_stated` for prose that names no buildable thing. The gate
is therefore read with R and S reported separately and with every flipped row's
deciding text quoted, so a later reader can check the flips rather than the
number.

## Ceilings, declared before the run

- **This is a re-read of one population by instruments that share a model
  family with the original.** It bounds a screen; it does not re-screen the
  world.
- **A clause-based verdict that survives re-reading is still right for the
  clause.** Nothing here says the extractor should have been different for
  every row; C1 says whether it moved verdicts at a rate that changes the
  table.
- **The `prior_art` 19 are out of scope by design**, so the restated table
  covers 31 of F029's 50 and cannot be read as a full re-screen of F029.
- **No row that flips becomes a candidate.** F029's Screen 1 and Screen 3 still
  apply, as E016 recorded for its own three survivors. The most this can do is
  move a number in a table.
- One corpus, one platform, one sample of 50 drawn by E012's stated rule.
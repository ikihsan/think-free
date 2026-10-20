<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-16
-->

# E171 AMENDMENT 1 — two defects in this protocol's reading rule, found before any label

Both were found while **preparing** the population, before a single class label
existed, so neither was found by a result and neither moves a bar. Recorded
here because the protocol is the instrument and both defects would have biased
`version_fact` **downward**, i.e. in the direction that fires the kill gate.

## Defect 1 — the "accepted answer" rule has no referent in this population

The protocol says: *read the **accepted** answer if the thread has one;
otherwise the highest-scoring answer.*

**0 of the 24 threads has an accepted answer.** E126 drew its pool with
`accepted=false`, and `is_accepted` is false for every answer of every one of
these 24 threads, while 16 of the 24 are `is_answered: true` with converged
answers present. So the rule silently collapses to "highest-scoring answer" on
every row, and **highest-scoring is not the resolution on 5 of 24 rows**: the
highest-scoring answer's version-mention disagrees with some other answer's on
idx 0, 63, 65, 66, 67.

Both disagreements are the same shape and they matter for this experiment:

- **idx 67** — highest-scoring answer (23) *explains where the folders come
  from*; the answer that *fixes it* (10) is "Upgrading
  `Microsoft.EntityFrameworkCore.Design` to version **10.0.2** or greater
  solves the issue."
- **idx 65** — highest-scoring answer (17) is "I added `openssl` to the
  Gemfile"; the answer carrying the version fact (8) is "fixed with Ruby
  **3.4.7** by building it against OpenSSL **3.5.4** instead of OpenSSL
  **3.6.0**."

E168's own grader reasons read *both* of those answers, which is why its
reasons name the version fact. Reading only the top-scoring answer would have
labelled both rows non-`version_fact` and understated the ceiling G3 could
reach.

**Repair.** Read **every** answer. Assign the class by the **operative content
of the thread's resolution** — the step a reader who follows the thread would
actually take — and record which answer supplied that operative step
(`n_answers_read`, `operative_answer_score`, `operative_has_version`). The
rule is still deterministic and still pre-declared; it is simply the rule that
matches what `is_accepted: false` means on a venue with no acceptance.

## Defect 2 — the thread, not the answer, is the unit that G3 would have to serve

The protocol classified "the resolution" from a single answer. E168's G3 arm
grounds an attempt in the component's **version history**, which serves a row
only if the version fact is the operative one. Where a thread carries **both**
a version fact and a surface fact, the operative rule already sends the row to
`version_fact` "so it counts in the arm's favour" — correct, but it needs to be
recorded as a **compound** rather than silently merged, because the honest
ceiling is then "grounding reaches the version half of a compound resolution",
which is a partial serve under E126's rubric.

**Repair.** Add a `compound` boolean: the operative resolution contains a
version fact **and** a fact of another class. `version_fact` rows with
`compound: true` are reported separately in the ceiling sentence, and G1 is
computed over all `version_fact` rows (the arm's best case) *and* over
non-compound `version_fact` rows only (the arm's clean case). **The kill gate
fires only if the arm's best case is below the bar**, so the amendment can
only make the kill harder to fire.

## Declared sensitivity arm, kept because it costs nothing

The original single-answer reading is still computed and reported as
`top_scoring_only`, so a reader can see the size of the defect rather than take
the repair on trust.

## Gates, restated after the amendment

| gate | rule | change |
|---|---|---|
| **G0 discrimination** | ≥ 8 of 10 probe rows labelled as constructed | unchanged |
| **G1** | `version_fact` over the **13 unserved rows** ≥ **0.40** | unchanged; **also** reported over non-compound rows only |
| **G2** | same share over the **11 served rows**, as the comparison | unchanged |

Nothing in `PROTOCOL.md` is amended except the reading rule in *The question*
and the addition of `compound`. No bar moves.
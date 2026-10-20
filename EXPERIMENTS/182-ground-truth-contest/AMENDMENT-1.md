<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-18
-->

# E182 AMENDMENT 1 — G5 fired as a failure, so G2 is withdrawn rather than reported

**Declared 2026-10-18, after the first run and before any second measurement.**
Commit this file before the repair fetch; `git log` is the evidence.

## 1. What ran

`fetch.py` then `analyse.py` on E177's 60 scored rows. Every gate was
evaluated as written and the numbers are in `states.json`:

| gate | result |
|---|---|
| G4 population stable | **PASS** — 59 of 60 reproduced (`qid 79408101`: key score 9 → 10, one vote, real drift over the intervening day) |
| G1 population measured | **PASS** — 60 of 60 complete score vectors |
| G3 contested ≥ 0.25 | **FAIL** — 13/60 = 0.2167, Wilson [0.1312, 0.3362] |
| K1 uncorroborated ≥ 0.50 | not fired — 16/60 = 0.2667 |
| **G2 differential** | **did not fire** — EVID missed 4/18 = 0.222 vs EVID hit 3/12 = 0.250, diff **−0.0278**, Fisher p = **1.0**, OR 0.857 |
| **G5 real-positive recovery** | **FAILED — 4 of 10 correct against a declared bar of 8 of 10** |

The state distribution, overall and by cell:

| state | overall | EVID missed | EVID hit | SELF hit | SELF missed |
|---|---|---|---|---|---|
| `contested` | 13/60 = 0.217 | 4/18 = 0.222 | 3/12 = 0.250 | 6/26 = 0.231 | 0/4 |
| `decisive` | 29/60 = 0.483 | 10/18 = 0.556 | 5/12 = 0.417 | 13/26 = 0.500 | 1/4 |
| `unopposed` | 2/60 = 0.033 | 0 | 0 | 2/26 | 0 |
| `uncorroborated` | 16/60 = 0.267 | 4/18 = 0.222 | 4/12 = 0.333 | 5/26 = 0.192 | 3/4 |

## 2. G5's hand-read, and what it means for G2

G5 fetched answer bodies for the 5 highest-ratio `contested` rows and the 5
highest-ratio `decisive` rows (`g5_fetch.py`, `g5-bodies.json`) and I read
them. **The question G5 asks is not "do two answers both exist" but "do the
two answers state the same resolution"** — which is the quantity E177's own
scorer used (`same_resolution`), and the quantity the disagreement
explanation depends on.

| qid | ratio | label | do the top two state the same resolution? | why |
|---|---|---|---|---|
| 79824381 | 0.833 | contested | **differ** | A0 exposes the queue as a byte-buffer struct in the C header; A1 re-declares `typedef struct` and specializes the template — different mechanisms |
| 79408101 | 0.800 | contested | **differ** | A0 is PEP 639 (`license = "MIT"` SPDX + `license-files`); A1 is a twine/pkginfo version bug — unrelated diagnoses |
| 79537353 | 0.800 | contested | **same** | both argue the LHS is evaluated to determine which object is assigned; A1 is a longer defence of A0's position |
| 79796450 | 0.676 | contested | **same** | both are the C++23 `std::views::zip` family; A0 `zip_transform`, A1 `zip` + `emplace_back` |
| 79663905 | 0.667 | contested | **same** | both `withTintColor(...)` + `.withRenderingMode(.alwaysOriginal)` |
| 79589468 | 0.481 | decisive | **same** | both hold you cannot legally bind a `uint64_t&` to two `uint32_t`s; A0 sidesteps with accessors, A1 says it is illegal and warns |
| 79791886 | 0.480 | decisive | **differ** | A0 blames modulo bias from `rand()`'s small `RAND_MAX`; A1 rewrites the loop to iterate −R..R; A2 blames the PRNG and `time(NULL)` seeding |
| 79556333 | 0.444 | decisive | **differ** | A0 says "you can't, closed Shadow Root"; A1 says "you can add CSS to `gmp-place-autocomplete`, see the docs" — a flat contradiction |
| 79843062 | 0.435 | decisive | **differ** | A0 hide the folders in `.csproj`; A1 upgrade `EntityFrameworkCore.Design` to 10.0.2+; A2 strip `contentfiles` from `IncludeAssets` — three different fixes |
| 79600161 | 0.429 | decisive | **same** | A0 and A1 both "download the `.aar` into `app/libs`", from different mirrors |

**4 of 10 correct, against a bar of 8 of 10. G5 fails.** The errors run in
both directions at similar rates — 3 of 5 `contested` rows state the same
resolution, and 3 of 5 `decisive` rows state different ones — so the 0.5
ratio threshold is not merely noisy, it is **not a monotone proxy for
resolution divergence** on this corpus. Two failure shapes, both legible:

- **Implementation competition reads as disagreement.** "How do I do X"
  questions collect several working implementations of the same fix
  (`zip_transform` vs a `zip` loop; two mirrors of the same `.aar`). Two
  answers, one resolution.
- **Genuine contradiction hides under a wide margin.** `qid 79556333`'s
  runner-up is at 44% of the top and flatly contradicts it; `qid 79843062`
  has three different fixes across 23/10/7.

## 3. What this withdraws

**G2's null is withdrawn, not reported.** As it stands, `contested` is a
label for *answer competition*, and G2 tested whether answer competition is
differential between the rows the assistant reached and the rows it missed.
That is not the question. The disagreement explanation E181 named is a claim
about **resolutions**, and it is **`untested`** after this run, not closed.

This is stated plainly because the alternative is the most expensive kind of
mistake available here: a null on an instrument that does not measure the
construct reads exactly like a closure, and the record's next reader would
have written "the EVID gap is not a disagreement about answers" on the
strength of a threshold G5 had already falsified.

G3's failure and K1's non-firing **stand** — they are shares over a defined
row set and do not depend on the label's meaning. So the record keeps two
things from this run: 21.7% of the ground truth is answer-contested and
26.7% has no alternative at all (**48.3% combined**), and neither share is
differential between hit and missed rows.

## 4. The repair, declared before it runs

The construct is available lexically. E171 already measured the vocabulary
contrast on an adjacent corpus — *a failure report names the symptom and the
environment; a fix states the cause and the change* — and E169 measured that
a fix shares **0 of 13** three-word runs with the report. Two answers to the
same question, therefore, overlap on **prescriptive tokens** when they state
the same fix, and diverge when they do not.

**`divergent`(A0, A1) ≡ overlap ≤ τ**, where `P(A)` is the set of prescriptive
tokens in A — identifiers inside backticked spans or code blocks, plus
CamelCase / snake_case / dotted-path tokens of length ≥ 4 — and

> **overlap = |P(A0) ∩ P(A1)| / |P(A1)|** — the share of the **runner-up's**
> prescriptions the top answer also makes.

The denominator is the runner-up because a runner-up that proposes something
new must supply prescriptions the top answer lacks; a top answer is free to
add extras without becoming divergent.

Pre-declared acceptance, so this cannot be fitted after the fact:

1. **τ is chosen to maximise balanced accuracy on the 10 hand-read rows
   above**, which are committed here and are the only calibration data.
2. The instrument is **accepted only if balanced accuracy ≥ 0.80** on those
   10 rows. Below that, **G2 is reported `not_evaluated`** and the
   disagreement explanation stays `untested`.
3. **The 10 calibration rows are excluded from G2.** A threshold fitted on
   them cannot then be scored on them; n falls from 60 to 50.
4. **Only rows with ≥ 2 answers and a runner-up score > 0 are eligible**, so
   `uncorroborated` and `unopposed` rows cannot become `divergent` for lack
   of a comparison.
5. G2' keeps the original bar: Fisher exact two-sided, `p < 0.05` **and**
   difference ≥ 0.20, EVID missed against EVID hit.
6. The hand-read labels above are the **only** judgement in this experiment.
   One reader, and E181's G4 already measured that one reader's verdicts are
   not stable to ±0.4 on assistant answers — these are judgements about two
   answers agreeing with each other, a narrower task, but the ceiling stands
   and is not re-measured here.

Nothing about this repair proposes a product. It decides whether one named
explanation of F136's gap is open or closed.
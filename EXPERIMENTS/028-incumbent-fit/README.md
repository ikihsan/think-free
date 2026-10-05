<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E028 — does the incumbent a prior-art screen named do what the clause asked?

**Date:** 2026-10-05. Task T-0072. Protocol declared before any label and
before any documentation was fetched: [`PROTOCOL.md`](PROTOCOL.md), amended twice
([`1`](PROTOCOL-AMENDMENT-1.md), [`2`](PROTOCOL-AMENDMENT-2.md)) and given both
readers the same [`RUBRIC.md`](RUBRIC.md). Numbers from `results.json` via
`stats.py`.

## Verdict: `not_evaluated`, and the reason is the instrument, not the world

| gate | declared | result |
|---|---|---|
| **A1**, C1 mismatched control | ≥ 90% of foreign bundles called not-serving | **32 of 32 at 0.0** — both readers, every row |
| **A1**, C2 positive control `H03` | both readers label it `serves` | **both `partial`** — **fails** |
| **A2**, reader agreement | κ ≥ 0.6 | **κ = 0.5625**, 10 of 14 agree — **fails** |
| **A3**, kill | `does_not_serve` lower bound ≥ 0.20 | 5 of 14, lower bound **0.163** — does not fire |
| **B1**, opposite | `serves` lower bound ≥ 0.60 | 2 of 14, **[0.040, 0.399]** — does not fire |
| **A4**, `not_evaluated` | fires if a control fails | **fires** |

**The declared positive control failed, so no verdict on fit is published, and
neither A3 nor B1 is read as an answer.** Moving a threshold after seeing which
side of it the data fell on is the one thing this repository's own standing
constraints forbid.

## What the control's failure actually says, and it is not what it looks like

`H03` is `webp-encode`. The clause asks for **fast on-the-fly WebP encoding**,
because it was *"unusably slow multiple seconds for large images."* E016 called
it *"served beyond argument, on install counts as well as on existence"* —
`sharp` at 436,835,441 downloads per month.

Both readers read `sharp`'s and the other stored documentation and returned
`partial`, for the same stated reason:

> no document states any latency figure or makes a claim about encoding one
> large image inline, so the performance half of the attribute is documented
> for a narrower case than the attribute asks

The strongest thing either reader found was `webp4j`'s *"~42% faster animated
encode on a 10-core M5"* — a **relative** figure for **animated** WebP, which is
a different case from the clause's.

**So the control failed because it was selected on the wrong criterion.** It was
chosen as a row where prior art is *demonstrably used*, and a download count
measures use, not fit. That is the same conflation E016's own `served` boolean
makes, and this experiment's question is whether that boolean means what a kill
needs it to mean. **The failure is evidence for the question and against the
control, not evidence about `sharp`.**

Which is a real result, and it is the transferable part: **a prior-art verdict
justified by install counts is not evidence of fit.** In this population the one
row whose incumbent has the strongest possible evidence of use — 437 million
downloads a month — is a row whose documentation does not establish the clause's
attribute.

## What the table shows, read as description and not as a verdict

Both readers, 14 rows in the fit population (16 rows named an artifact; `H05`
and `H30` were excluded because R1 refused them as having no distinguishing
attribute and R2 did not, and the declared exclusion rule removes any row either
reader refused):

| label | rows |
|---|---|
| `serves` — **both** readers | **2** — H08 (bulk flashcards), H49 (drive disk usage) |
| `serves` — **either** reader | 4 — adds H26, H36 |
| `partial` — both readers | 3 — H01, H03, H45 |
| `does_not_serve` — **both** readers | **5** — H00, H14, H34, H35, H42 |

Five rows where both readers read the named incumbents' own documentation and
found **none of it** establishing the clause's attribute: `H00` (an HN client
that permits bots), `H14` (an AT Protocol handle resolver that finds a server's
new address from a signed identity), `H34` (a project recommender driven by the
user's own star list), `H35` (a C++ subset linter), `H42` (git line staging).
`H01`'s note is the one that reads most like the general case: the incumbents
offer the atomic-update mechanism but the clause asks for *Debian-like broad
hardware and vendor support*, which E016's own note already flagged and which no
stored documentation claims.

**This is a description of 14 rows read once.** κ = 0.5625 is below the declared
floor, so the four-category scheme has not earned the right to carry a decision,
and the readers are the same model family — MISSION.md records that agents are
not independent human validation.

## The lexical index, reported with the control that makes it readable

Coverage of the Step A attribute's content words in the best-matching artifact's
own documentation: **0.2092 on matched pairs against 0.1438 on mismatched
pairs, difference 0.0654, `informative: false`.** F043's lesson is the reason
this is printed with its base rate beside it: a bare 0.2092 would have read as
evidence that incumbents match clauses. Against a control, it is 6 points of
noise over 32 pairs, and it feeds no gate — asserted by a test that greps the
gate table for `coverage`.

## Three defects this run found in its own instrument

1. **HTTP 200 with a body that strips to nothing was written as a capture.**
   Eight `openweb` fetches returned a page whose text extraction yielded
   **zero bytes**, and the first version of `store()` wrote a zero-length file —
   which a later reader reads as *"this product's documentation says nothing"*
   rather than *"we did not get it"*. Repaired: an empty body is never stored,
   an empty file is removed rather than left, and the log records the refusal
   beside the artifact. The eight rows are marked `has_text: false` and appear
   in no reader's view. **No reader label cited any of them**, which is checked.
2. **The contamination test was reading the wrong thing.** It banned the token
   `github` from a reader's Step A, and it fired on `H34` — where the
   *requirement itself* says *"i lost a lot of github projects"*. The reader was
   quoting the requirement, exactly as the rubric asks. Replaced with a check
   against the owner segment and the separator-stripped artifact name, which no
   prose contains, and the assertion count is checked so the check cannot
   quietly stop reading.
3. **A view could show an artifact with no documentation as though a product had
   been examined.** Entries with empty documentation are dropped from the bundle
   and the bundle's size is published, so a row cannot reach `does_not_serve`
   because a product's documentation was missing rather than silent.

## What this does not do

- **It does not reopen F029's 0-of-50.** That is a composition finding about the
  corpus, confirmed by F047's re-read. This experiment can only decide whether
  *the prior-art column of that screen* was a valid test, and it returned
  `not_evaluated`.
- **It does not reopen the twelve deaths or the corpus closure.** `H08` and
  `H49` are rows where the incumbents do fit, and the corpus is a population of
  needs the world absorbed conversationally whatever this table says.
- **It does not validate the instrument that produced it.** 29 rows were
  declared; **19 were measured**. The ten sealed-report rows — the ones that
  closed the mission's own candidates — were **not run**, because the declaration
  requires their requirement text to be copied out of report prose, and that
  extraction is itself a labelling act. Doing it after the harvest arm reported
  a result would have been a second measurement chosen by the first one's result.
  `results.json` says `arm2_executed: false` and a test asserts it stays false
  without the reason changing.
- **It says nothing about whether the incumbents work.** The fit is tested
  against what an artifact's own documentation claims.

## Reproduce

```bash
tools/x -- python3 EXPERIMENTS/028-incumbent-fit/build_population.py
tools/x -- python3 EXPERIMENTS/028-incumbent-fit/fetch_docs.py
tools/x -- python3 EXPERIMENTS/028-incumbent-fit/make_step_b_view.py --reader r1
tools/x -- python3 EXPERIMENTS/028-incumbent-fit/make_step_b_view.py --reader r2
tools/x -- python3 EXPERIMENTS/028-incumbent-fit/stats.py
python3 -m unittest discover -s EXPERIMENTS/028-incumbent-fit -p 'test_*.py' \
  -t EXPERIMENTS/028-incumbent-fit
```

29 tests. Each is asserted against the committed capture rather than a fixture
built from the same object as the assertion: the Wilson interval for 0/24 must
equal the `[0.0, 0.138]` the record quotes for F042, κ of 1.0 must be reported as
a warning rather than agreement, a reader quote must appear in the file it names,
no control bundle may share an artifact with its own row, Step A may name no
incumbent the screen named for that row, and the verdict must be `not_evaluated`
with the positive control recorded as the failure.
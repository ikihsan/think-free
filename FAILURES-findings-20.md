<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Failures — recorded finding F048

Split out of [`FAILURES-findings-19.md`](FAILURES-findings-19.md), which held
F045–F047. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F048 — a prior-art verdict justified by install counts is not evidence of fit, and the instrument that tests fit is refused by its own positive control

**Date:** 2026-10-05. `EXPERIMENTS/028-incumbent-fit/`, task T-0072. Protocol
declared before the first label and before the first documentation fetch.

### What was asked

Prior art is **the plurality kill reason in this mission's record** — 10 of 18
(F044) — and it is the reason all twelve candidates from the six sealed reports
were dropped. The verdict had been checked for **existence** (E016, F035) and
never for **fit**. [`STATE.md`](STATE.md) carried that as a standing limitation:
*"What has not been shown is that any need is served by the incumbents a screen
names."*

**Result: `not_evaluated`.** The declared positive control failed, so no verdict
on fit is published.

### The finding, which is the control's failure and not the instrument's verdict

`H03` is the row where prior art is *demonstrably used*: `sharp` at **436,835,441
downloads per month**, which E016 called *"served beyond argument, on install
counts as well as on existence."* The clause asks for **fast on-the-fly WebP
encoding** because it was *"unusably slow multiple seconds for large images."*

Both blind readers read `sharp`'s and the other stored documentation and
returned `partial`, for the same stated reason: **no document states a latency
figure or claims the multi-second case is solved.** The strongest figure either
reader found is `webp4j`'s *"~42% faster animated encode on a 10-core M5"* — a
relative number, for animated WebP, which is a different case.

**A download count measures use. A prior-art kill needs evidence of fit.** The
control failed because it was selected on the wrong criterion, and its failure is
evidence for this experiment's question rather than against `sharp`. This is the
same conflation E016's `served` boolean makes, and the experiment's whole point
was whether that boolean means what a kill needs it to mean.

**The transferable statement:** *the strongest evidence of use available in this
record is not evidence that a product does what a clause asked for, and a screen
that cites it as a kill has not tested what it claims to test.*

### What the table shows, as description only

19 of 29 declared rows measured; 16 named an artifact; 14 in the fit population.
**Reader agreement κ = 0.5625 against a declared floor of 0.6** — the four-category
scheme has not earned the right to carry a decision. Both readers, from the same
model family, which MISSION.md records is not independent human validation.

| label | rows |
|---|---|
| `serves` — both readers | **2** — H08 (bulk flashcards), H49 (drive disk usage) |
| `serves` — either reader | 4 — adds H26, H36 |
| `partial` — both readers | 3 — H01, H03, H45 |
| `does_not_serve` — both readers | **5** — H00, H14, H34, H35, H42 |

`H01` reads most like the general case: the incumbents offer the atomic-update
mechanism, and the clause asks for *Debian-like broad hardware and vendor
support* — which **E016's own note already flagged** and no stored documentation
claims. So the category/attribute gap was visible in the record before this
experiment and was not acted on.

### The lexical index, with the control that makes it readable

Attribute-term coverage in the best-matching artifact's documentation: **0.2092
matched against 0.1438 mismatched, difference 0.0654, `informative: false`.**
F043's lesson: the bare 0.2092 would have read as evidence that incumbents match
clauses. Against a control it is noise over 32 pairs, and it feeds no gate.

### Three defects found in this experiment's own instrument

1. **HTTP 200 with a body that strips to nothing was written as a capture.**
   Eight `openweb` fetches produced **zero-byte files**, which a later reader
   reads as *"this product's documentation says nothing"* rather than *"we did
   not get it."* Repaired, and **no reader label cited any of them**, which is
   asserted by a test rather than claimed.
2. **The contamination test banned `github` from a reader's Step A and fired on
   the requirement's own words** (*"i lost a lot of github projects"*). The test
   was reading the wrong thing; replaced with a check against owner segments and
   separator-stripped artifact names, with the assertion count checked so the
   check cannot quietly stop reading.
3. **A bundle could show an artifact with no documentation as though a product
   had been examined**, letting a row reach `does_not_serve` for a missing
   document rather than a silent one.

### What this rules out, and what it does not

- **It does not reopen F029's 0-of-50**, confirmed by F047's re-read. This can
  only decide whether the prior-art *column* of that screen was a valid test.
- **It does not reopen the twelve deaths or the corpus closure.** Two rows do
  fit, and the corpus is a population of needs the world absorbed conversationally
  regardless.
- **The ten sealed-report rows were not run.** Their requirement text must be
  copied from report prose, which is itself a labelling act; doing it after the
  harvest arm reported would have been a second measurement chosen by the first
  one's result. `arm2_executed: false` and a test holds it.
- **Nothing about whether the incumbents work.** The fit is tested against what
  an artifact's documentation claims.

### Ceilings

14 rows in the fit population, read once, by two passes of one model family, with
documentation stored at 12,000 characters and shown at 1,800, and with at most the
**four artifacts the screen listed first** — an artifact it listed fifth could
serve and the row would still read `does_not_serve`. 90 artifacts were named, 87
have stored documentation. One community, one instant, 2026-10-05.

**The unresolved part is now specific:** whether a prior-art screen should test
fit rather than existence is answerable, and the instrument that answers it is
buildable, and this run shows the two requirements it must satisfy — a positive
control chosen on **fit demonstrated in documentation** rather than on use, and a
reader scheme whose agreement clears its own floor.
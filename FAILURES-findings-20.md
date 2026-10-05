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
## F049 — 167 of 241 need-staters shipped *before* they stated the need, and the
## reader arm could not resolve the rest

`observed`, 2026-10-05, task T-0073,
[`EXPERIMENTS/029-need-build-match/`](EXPERIMENTS/029-need-build-match/README.md).
E029 is the join nobody had made: F042 followed the corpus's *needs* forward and
F045 followed its *people* forward, and the two captures were never joined.

**What failed.** Two things, and the second is the finding.

**The instrument, first.** Verdict `not_evaluated`, and it is refused twice over:
reader agreement **κ = 0.5004** against a declared floor of 0.6, and the declared
negative control **C1 separation 0.0405** against a required 0.20. Three reader
passes were spent and none produced a usable comparison. The run was invalidated by
its own instrument, three times:

- **45 of 74 control rows rendered an empty SHIPPED section**, so the control could
  only be labelled `unrelated`. Caught by a test whose *population* was what hid the
  defect — the first version iterated only the treatment arm and passed.
- **The control was the treatment arm, renamed**: 74 self-pairs, 0 cross-pairs. The
  alarm was an arm that feeds no gate printing byte-identical lexical means for both
  (0.044952), which two different pairings cannot produce. Repaired: 0.023632.
- **A label file with 222 correct row ids and a wrong row-to-pair mapping** — a
  reader re-labelled a regenerated view in the previous view's order. Asserting the
  id *set* is what let it through. **My repair script made it worse**, re-keying
  against the wrong reference at a reassuring 221/222, and was deleted. A second
  reader returned 4 duplicated and 4 missing ids, caught by the pre-declared test.

**The population, which is the part that survives.** Of the 241 need-staters with a
public `Show HN` item, **167 shipped it before they stated the need and only 74
shipped anything after it.** A build cannot answer a need stated after it, so **69%
of the population was never askable**, and the experiment as first written would have
manufactured its own null. Selection is by HN item-id ordering and that proxy was
falsified rather than assumed: **8 of 8 sampled authors agree with real
`created_at`, 0 disagree, 0 unreadable**, sampled four from each side of the cut.

**What it changes.** Not the closure — F042's `0 of 24 built it themselves` is not
refuted, because the reader arm bounds the matched − control separation at CI95
**[−0.0156, +0.1125]** (Fisher p = 0.245) and is consistent with zero. What changes
is what the closure *is*: E025's `22.2% of need-staters have shipped something` is
consistent with these people **having built something first and then hitting a gap
they did not close**, which nobody had read that way because nobody asked *when*.

### What this rules out, and what it does not

- **It rules out** treating this corpus as 1401 independent unmet needs. A 69%
  majority of the demonstrably-building subset had already shipped before they
  complained, so "is there a tool that…" is substantially a question asked by people
  who build, not a queue awaiting a builder.
- **It does not rule out** a real need→build link: 3 of 74 matched rows against 0 of
  74 cross-paired, named identically by two independent readers, is the predicted
  direction. It is 4%, it is imprecise, and κ is below its own floor.
- **It does not touch** any prior-art death, F029's 0 of 50, or F048/D060. Use is
  still not fit, and E028's positive control is still mis-selected.

### Ceilings

One community, one trigger vocabulary, one reader scheme whose agreement is 0.50,
74 rows per arm after the temporal restriction, `addresses` judged from a title by
one model family. The direction is consistent and the magnitude is unresolved; a
larger n is the only thing that would move the verdict, and it is the same instrument
asked to do more.

## F050 — the recurrence statistic that "found" clause sharing measured comment length and coincidence, not clauses

E030 (`EXPERIMENTS/030-departure-recurrence/`) declared a pair-level recurrence
statistic over rare shared signature tokens and a B1 gate, then measured it:
treatment 0.3493 vs control 0.2155, difference 0.1338 with CI95
[0.0997, 0.1687] — B1 fired. Printing the mutual groups' linking tokens showed
four unrelated comments (firewall, mainframes, Ruby, Go) chained through
`abandon`, `absolute`, `allocation`, `apis` — ordinary English of length ≥ 4
occurring in ≤ 5 of 919 accounts, which is what ~8 500 rare tokens spread over
long comments produce (`raw/mutual_treatment.jsonl`, AMENDMENT-8).

**What it rules out:** B1's verdict and every cluster-level figure. **What it
shows instead:** the treatment arm's comments are longer (median 90 vs 74
words), its common-token cutoff keeps more rare tokens per account (2% of 919
vs 2% of 2687), and the declared statistic tracks those, not clause sharing.
The A9 permutation control explains the arm difference (treatment observed
0.3493 against a 50-permutation null of 0.2925 ± 0.012; control 0.2155
against 0.0496 ± 0.0044), and the length-matched recomputation reverses the
sign: −0.0735, CI95 [−0.1176, −0.0290]. H1 is `not_evaluated` a third and
final time; A6's absolute-precision gate had already failed (0.3855) and is
unreachable at n=24; A8's held-out separation **did** fire (16/25 = 0.64 vs
1/28 = 0.036), so the departure-framing population is real and distinct — the
population rule works, and the ruler for recurrence was falsified. C1's pilot
was never run, because its referent (clusters of clauses) never established.

**Ceilings:** one reader pass (A8's 25 and 28 answered rows, agreement not
measured), one corpus, one framing set, and the extraction's own defect
recorded in AMENDMENT-4 §2 (it names the replacement artifact when the
departure is not name-shaped, q2 = 13/24). A recurrence claim on this corpus
must wire A9's null and printed linkage into the protocol before the first
fetch; the production token rule remains unproven.

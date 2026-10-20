<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# Findings — failures and negative results, part 46

Local lineage (pre-merge F125–F129) renumbered on the 2026-10-20 merge, which
adopted upstream's F125–F143 for the same identifiers: this file holds **F144–F146**. Split out of
`FAILURES-findings-41.md`–`43.md` as they stood on `3bae5f6a`.
See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are stable across
all findings files.**
Continued in [`FAILURES-findings-47.md`](FAILURES-findings-47.md) (F147, F148).

---

## F144 — the verifier question is two questions, and only one of them is solvable cheaply

**Observed 2026-10-14**, session `2026-10-14-001`,
[`EXPERIMENTS/140-judge-form-invariance/`](EXPERIMENTS/140-judge-form-invariance/RESULT.md).

E114 closed with: the subject was fine (0 of 374 values fabricated) and the
**verifier was dead** — a checker that passed every declared gate had a
false-positive rate of 1.00 on faithful paraphrase, and named as the missing
number *"the false-positive rate of a verifier whose comparison step tolerates
faithful paraphrase"*, adding that it was not cheap to get. E140 got it, three
times, on one corpus, with the arms declared before the instruments ran.

**Population.** E114's 15 committed (document, question, answer) triples over 5
real Federal Register final rules; 241 numeric and 398 canonical values. Judge
arm 31 items in 7 batches: 10 verbatim, 10 surface-transformed, 4 re-authored by
a blind writer, 7 corrupted.

| instrument | FP on verbatim | FP on surface-paraphrased | FP on re-authored | detects a swapped value | detects an omission | detects a misattribution |
|---|---|---|---|---|---|---|
| M1 `ground.py` (E114's) | 0.3727 | 0.4651 | 0.6019 | 9/11 | — | 6/6 |
| M2 `valueset.py` (canonicalizer) | **0.0000** | **0.0000** | **0.0000** | **11/11** | 11/11 | **0/6** |
| J1 shipped `inspect_ai` `model_graded_fact` | 0/10 | 0/10 | 0/4 | 6/7 | not run | not run |

Every rate in the three false-positive columns is a *false*-positive rate because
K4 machine-verifies that each arm carries the identical value multiset as the
verbatim answer. J1's 0/24 correct answers is Wilson CI95 [0.0000, 0.1380]; its
6/7 detection is [0.4869, 0.9743].

**What is disproved.** Not the judge: it produced zero false positives on 24
correct-but-reworded answers and found 6 of 7 swapped values, including a
transposition inside a telephone number. The **incumbent mechanical verifier is
disproved as a gate, and this time quantitatively**: its false-positive rate is
not a constant that transfers between arms (F123) but a **monotone function of
how far the input has been reworded** — 0.3727 verbatim, 0.4651 after mechanical
surface transforms, 0.6019 after a writer re-authored the same answer in
different words. E114's 0.3717 reproduces here independently, and the 1.00 of
F118 is the far end of a curve rather than an outlier.

**The finding that changes a build decision.** The paired measurement — *was the
swapped value itself the flagged one?* — gives M1 **9/11**, where differencing
aggregate flag counts gives **6/11**. M1 detects most substitutions while
flagging 37–60% of correct values, so a flag from it is worth about as much on a
correct answer as on a wrong one: it is not a paraphrase detector, it is a
paraphrase detector of the wrong thing, and its detection is inseparable from its
noise. **E114's "the verifier is dead, not the subject" stands, and is now a
measurement rather than an assertion.**

**What survives, and is the first positive build trigger this line has produced.**
`valueset.py` — canonicalise each value (separators, decimal trailing zeros,
currency placement, `per`/`each`, percent sign or word, case, whitespace, list
order) and compare multisets — passes every declared gate: **zero false
positives in 929 values** across three correct arms, 11/11 substitutions, 11/11
omissions, K4 15/15 and 4/4. G0 passed first (6/7 ≥ 0.667), so the comparison
was not void.

**And the weakness the protocol declared, now `observed` rather than inferred.**
PROTOCOL.md named M2's blind spot before the run: comparing multisets binds
nothing to what a value is said to be about. Six mechanical misattribution arms
were built (one value transposed onto the wrong subject, K4-preserving) and **M2
detected 0 of 6**; M1 flagged 6 of 6. So the cheap pass is blind to binding by
construction *and by measurement*, while the only instrument here that sees
binding is the one twice measured unusable as a gate. **The expensive check
cannot be replaced, only deferred** — M2 is a pre-pass that removes omissions and
substitutions (22 of 22 of the wrongness built) and hands on the binding
question, which is now the open problem rather than an assumption.

**One practitioner finding with no counterpart in F118/F123.** J1's single miss
was a corrupted billing code, `4915-01-P` → `1247-01-P`. The judge **found the
discrepancy in writing** — "This is a factual discrepancy in a data value, not a
style or punctuation difference" — and then graded it **correct**, because the
question asked for CFR, U.S.C., docket and FR-document numbers and a billing
code is none of those. The failure is the rubric's *scope clause outvoting
evidence in front of it*: a different defect class from context-word mismatch,
and one that a re-run at larger n does not fix.

**Ceilings, all declared before the run.** One genre, five documents, one reader,
one day; expert answers are model-produced, not gold. One rubric, one judge
model, no panel, no majority reducer, uncontrolled model variation between the
seven batches. Misattribution by transposition only — a binding wrong in prose is
`untested`. **Generalisation is the declared next action and is not done**: the
extractor was written against this corpus's value shapes, so a pass here is
evidence of mechanism and not of generality.

**Corroborates** F118, F123. **Consumes** the number E114 named as the one it
could not afford. **Produces** a candidate artifact (`valueset.py`) whose scope
is fixed by measurement: *value correspondence under rephrasing*, never
faithfulness.

## F145 — the value pre-pass's 0 false positives in 929 values was a fact about the corpus's writing conventions, and its detection rate on real human errors is 0.28

**Observed 2026-10-14**, session `2026-10-14-002`,
[`EXPERIMENTS/141-valueset-second-genre/`](EXPERIMENTS/141-valueset-second-genre/RESULT.md).

E140 ended with a build trigger: `valueset.py` passed every declared gate, 0
false positives in **929** values across three correct arms, 11/11 on
substitutions, 11/11 on omissions, and the protocol's own proposal was to ship
it as the cheap first stage in front of a faithfulness check. E141 ran it
**unchanged** on SQuAD v2.0 dev — 11,873 questions, 1,204 paragraphs, every
question and answer span written by a person, **no item corrupted by the
experiment** — and the build trigger does not survive.

| | declared | observed |
|---|---|---|
| detection on real human value errors | ≥ 0.95 | **0.2826** (223/789) |
| false positives on correct human answers | ≤ 0.02 | 0.0113 (67/5,928) — *passes* |
| coverage over all answerable items | ≥ 0.30 | 0.2146 — *fails* |
| coverage where the answer **is** a value | ≥ 0.30 | 0.9379 (800/853) |
| share of a real corpus the pre-pass resolves | — | **0.1647** |
| of what it clears, genuinely unsupported | — | **0.2763** (460/1,665) |

**Three separable results, and the middle one is the one that changes what can
be said.**

1. **The declared blind spot is confirmed on text nobody built for it.** Of 566
   misses, **460 (0.5830 of the arm)** are items where the value is real, is in
   the paragraph, and is attached to the wrong subject — the exact shape E140
   measured at 0 of 6 on arms it constructed. Two orders of magnitude larger,
   independently produced.
2. **An extraction gap nobody had named.** The other **106** are items where
   the question contains a digit and the canonicalizer returned *no value at
   all*, because `\b\d…\b` cannot match `19th`, `1980s` or `1100s`. On
   encyclopedic prose the most common way of stating a period is invisible to
   an extractor written for regulatory prose.
3. **E140's 0.0000 was a property of its corpus, and the hand-built control
   says how.** `canonical()` keys a value by `(kind, number)`, so
   `$12,500,000` and `12500000 dollars` are different keys for one number. Six
   hand-written positives — the same document, the same values, a person's
   phrasing, not copies of the arms that built the instrument — **four pass and
   two fail**, both on that. Federal Register rules write dollar amounts with a
   symbol, so 929 values from that corpus could not have found it. On SQuAD the
   class is **latent**: 0 of 67 real false positives is a kind mismatch.

**And the baseline reverses the reading.** On the same rows and the same
denominators, `ground.py` flags **0.0940** of correct items against M2's
0.0113, and detects **0.7174** against M2's 0.2826. E140 concluded M1's
detection was inseparable from its noise. On human-written prose M1 detects
**2.5× more** of the real errors at **8× the** false positives. The two are not
ranked; they are two points on one curve, and on this population M2's point is
far less favourable than the regulatory corpus made it look.

**Rule.** An instrument's false-positive rate and detection rate are properties
of *(instrument, population)* and not of the instrument. A zero measured on one
corpus licenses the instrument on that corpus. When the population changes, both
numbers are re-measured or neither is quoted — and the measurement needs a
**positive control the builder did not write**, because the population the
instrument was built for cannot expose the instrument's own blind spots.

**Corroborates** F123 (a rate belongs to an arm), F144 (F118's 1.00 is the far
end of a curve, and a 0.0000 is the other end of the same problem),
F116 (a coverage number over the whole population is not the number that
transfers), F118. **Consumes** the build trigger E140 fired. **Produces** a
measured scope for the artifact — a ranker for value-typed QA, blind to binding
at 0.2763 of what it clears, and not worth running on a corpus where 0.8353 of
items assert no value.

## F146 — a renumbering that resolved one collision created another, and an overwrite that recorded a decision deleted the decision before it

**Observed 2026-10-14**, session `2026-10-14-002`, while repairing a suite
that was already red when this session started. Both defects were inherited;
neither was caused by E141, and both were reproduced on the parent commit
before anything was changed.

### (1) D044 was overwritten, not edited

`f65940c4` ("Record D046: release preflight as public prototype with adapter
interface") is `10 insertions(+), 40 deletions(-)` on
`DECISIONS-PUBLISHING.md`. The 40 deleted lines are **D044 in full** — *"The
session's own record is not uncommitted work, and the claim says so"*, T-0055,
defect 21, F023. The file's own header and `DECISIONS.md`'s row both still
named `D044–D046`, and the section boundary that recovered D044 is
`old.index("## D045 —")` — which sits **before** D044 in that file, so a naive
"from D044 to D045" extraction returns nothing at all and the overwrite is
invisible to the obvious repair.

Three independent gates each caught a different half of it and none of them
caught the whole: `doc lint` said the header named an id the file does not
define, `test_decision_header` said the same, and
`test_identifier_enforcement` said `DECISIONS.md` lists `D044` and nothing
defines it. D044's body is recovered verbatim from `f65940c4^` and re-appended.

**An overwrite of a section header destroys the section.** The pattern that
caught it is the one already in the repository's own rules — the index, the
file header and the heading must all move together (D124's invariant) — and it
fired correctly. What the rules could not say is *where* the destroyed section
used to be.

### (2) The D046 → D048 renumbering resolved one collision by creating another

`1cc83e2a` ("Resolve D046 identifier collision: renumber DECISIONS-RECORDS D046
to D048") moved `DECISIONS-RECORDS.md`'s D046 to **D048**, which was already
defined in `DECISIONS-SCREENING-2.md` since 2026-10-05. It also left
`DECISIONS.md`'s row for `DECISIONS-RECORDS.md` naming the old id `D046`, and
left a **stale `D048` in that file's own header** — a leftover from T-0063,
when D048–D050 moved *verbatim* to `DECISIONS-SCREENING-2.md` and numbering was
deliberately preserved. So `D048` was in `DECISIONS-RECORDS.md` three times over
and the identifier check, which reads every source, reported the collision
correctly.

Repaired by the standing rule — **the later allocation yields.** `SCREENING-2`'s
D048 is from 2026-10-05 and is referenced from **ten** places across the record
(`FAILURES-findings-8.md`, `-9.md`, `STATE-next-actions-closed.md`,
`DECISIONS-SCREENING.md`, `DECISIONS-SCREENING-3.md`, `DECISIONS.md`'s row,
`EXPERIMENTS/012-candidate-harvest/README.md` and session summaries).
`DECISIONS-RECORDS.md`'s is from 2026-10-13, was a mechanical renumbering of an
existing id, and is referenced only inside its own file. It yields:
`DECISIONS-RECORDS.md`'s D048 is now **D110**, its header's stale `D048` is
gone, and `DECISIONS.md`'s row reads `D029, D032, D035, D041, D043, D047,
D110`.

**The rule this adds.** A renumbering is not finished when the two colliding
headings differ: it is finished when **every** source of the identifier agrees —
the index row, the file's own header, and every reference elsewhere. `1cc83e2a`
updated two of five and checked the free list rather than the used one.

### What was left red, and why

Adding two new `DECISIONS-SCREENING-*.md` files is itself a four-place edit, and
the suite names all four: `paths.MISSION_RECORDS` (the list a session obligation
reaches), `reconcile.IMPLICATIONS["decision"]` (the list that satisfies a
`decision` event), and the same two names in `tests/test_decision_files.py`,
which pins each against the other. **All four were updated here**, and the
repair is worth one sentence for the next session that splits a file: a new
`DECISIONS-` file is not one index row, it is two source lists in
`tools/originlib/` and the same two names again in the test that holds them to
each other.

Two failures remain, and **neither was caused by this session.** Both were
reproduced on the parent commit before anything was changed.

`test_no_tracked_link_leaves_the_repository` fails on **21 links in
`EXPERIMENTS/125-third-party-harness-preflight/readmes/`** — E125's captured
third-party READMEs, whose `/owner/repo/path` links are meaningful in *their*
tree and meaningless here. The same 21 files are the source of ~400 of the 427
remaining `doc lint` violations. Scoping a link gate away from vendored
third-party prose is defensible, but it is a change to what a gate enforces, it
was not this session's work, and **it is not done here on a red suite by a
session that did not own the debt.** It is named instead, with the exact
repair: a declared `exempt:` glob in `vendor/MANIFEST.md` for captured
`readmes/*.md`, honoured by `doclint.check_links` and by
`test_link_escape`, with a negative control that a link in an *authored*
document still fails.

`test_ci_annotations.test_the_tip_reports_nothing_and_annotates_nothing`
fails in the full discover run and passes when its module is run alone — a
test-ordering dependency, present at baseline, cause `untested`.

**Corroborates** F117 (two uncoordinated runs writing one identifier and
returning opposite results — the same failure at file scope rather than
experiment scope), F121 (a key that could not match what it was compared
against), F003/F004 (this repository's own record-keeping). **Consumes** the
`doc lint` and `test_identifier_enforcement` failures as named, dated
failures. **Ceiling:** the repair restored the gates, it did not explain why
`f65940c4` overwrote a section rather than appending one, and that cause is
`untested`.

**The 2026-10-20 lineage merge applied this rule a third time.** This lineage's
F125–F129 became F144–F148 and its D110–D112 became D124–D126; every index row,
file header and authored reference moved with them. **The sealed session streams
from that lineage still cite the old numbers and were deliberately not
rewritten** — an append-only log is the one source allowed to disagree with the
index, and here it disagrees out loud.

---


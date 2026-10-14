<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Failures — recorded finding F126

Continues [`FAILURES-findings-41.md`](FAILURES-findings-41.md), which held
F125. See [`FAILURES.md`](FAILURES.md) for the index. **Identifiers are
stable across all findings files.**

## F126 — the value pre-pass's 0 false positives in 929 values was a fact about the corpus's writing conventions, and its detection rate on real human errors is 0.28

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

**Corroborates** F123 (a rate belongs to an arm), F125 (F118's 1.00 is the far
end of a curve, and a 0.0000 is the other end of the same problem),
F116 (a coverage number over the whole population is not the number that
transfers), F118. **Consumes** the build trigger E140 fired. **Produces** a
measured scope for the artifact — a ranker for value-typed QA, blind to binding
at 0.2763 of what it clears, and not worth running on a corpus where 0.8353 of
items assert no value.

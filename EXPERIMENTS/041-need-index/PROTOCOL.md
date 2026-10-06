<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — Does the need-similarity instrument find a repeat a human already saw?

**Every gate, threshold, instrument parameter, arm definition and exclusion rule in
this file was fixed before any similarity between two rows was computed.** Session
`2026-10-06-007-e041`. The only things read beforehand were E040's `PROTOCOL.md`
and `AMENDMENTS.md`, E012's 26 trigger literals, and the two probe scripts in this
directory — which measure **what the source can serve** (D067) and never a
similarity.

## The question

E040's G2 was to validate the clustering instrument against Stack Overflow's own
duplicate judgement. **It could not fire, for two reasons, both recorded as
defects of the instrument's own design (F064):**

1. each positive row was labelled "a repeat of *some* question" and **that
   question was not in the arm**, so no arm contained a pair; and
2. the arms had **unequal candidate-set sizes** (140 against 2260), and
   `partner_rate` is a maximum over the candidate set, so it rose mechanically
   with pool size — enough to **invert a gate's sign** (F065).

The target was then unreachable from this host by six routes (F066, D070). So the
record's one instrument used for every demand-side claim in this line rests on a
gate that is `not_evaluated`, and **every result read through it carries that
ceiling.**

**A control that holds one member per row cannot validate a similarity
instrument.** That is arithmetic, not opinion: there is nothing in the arm for a
pair to be found in. So the question here is prior to any second venue, any
scaling claim and any needs index:

> **Given two short technical texts that a practitioner independently judged to be
> the same thing, does this instrument rank the judged partner above the rest of
> the corpus — and at what threshold?**

If yes, the instrument is usable and E040's positive result can be read as
*resemblance*, with a measured false-positive rate attached. If no, the whole
demand-side line rests on a lexical instrument that does not detect repeats, and
that is worth knowing before any population is harvested on its behalf.

## The population, and why this one

**GitHub issues that the platform itself closed with `state_reason: "duplicate"`,
together with the issue each one names.** The judgement is a human triage act
recorded by the platform, made by the same practitioner who filed the row, on text
they wrote themselves. **No near-copy was constructed here** — E040's protocol
already ruled synthetic near-copies insufficient as a positive control, and that
rule is inherited unchanged.

Chosen after a two-request mechanism probe, which is D067's check run before
measuring the population: `GET /search/issues` returns **full issue bodies**, and
`repo:<o>/<r> is:issue` enumerates a repository's whole issue space. So one
mechanism serves **both members of a pair**: the duplicate and its target are both
inside one complete repository capture. That is what F064's control lacked and
what F066 could not reach.

**Corpus construction, declared in order and not varied afterwards.**

1. **Repository list, fixed here.** Ten established projects of mixed language and
   size, taken in this order and not replaced by better yield:
   `pallets/click`, `tiangolo/typer`, `psf/requests`, `pytest-dev/pytest`,
   `vuejs/vue`, `d3/d3`, `rust-lang/cargo`, `scrapy/scrapy`, `tornado/tornado`,
   `jupyter/notebook`.
2. **Each repository captured completely** — every `is:issue` row, page by page at
   100 per page, split by creation year when a repository exceeds the search
   index's 1000-result ceiling. "Completely" is asserted per repository against
   the API's own `total_count`, and a repository whose captured count does not
   reconcile is **reported as unreconciled and excluded**, not padded.
3. **Automation exclusion, declared before the rates were read.** Any repository
   whose duplicate-labelled share exceeds **0.20** is excluded, with its share
   recorded. Mass-generated duplicate fixtures are not a human judgement; the
   first probe sample was three `gh-aw-test` fixtures and nothing learned from
   them is evidence about people.
4. **Target extraction.** A fixed ordered list of six reference patterns
   (`duplicate of #N`, `dupe of #N`, `same as #N`, `-> #N`, `see #N`, a GitHub
   issue URL). First match wins. A duplicate whose parsed target is **not in the
   corpus** is dropped and counted; it is not silently replaced by another target.

**Corpus bias, stated plainly.** These are repositories that attract triage, so
the rate of duplicate closure here is **not** a population rate for software
issues and no gate below reads it as one. It is a pool from which judged repeats
are drawn. The rates per repository are reported anyway, because F055's lesson is
that a property read off one stratum is not the property.

## Arms

| arm | what it is | why it is here |
|---|---|---|
| **P** | a duplicate row and the target it names, **both in the corpus** | the positive control F064 could not build |
| **N0** | for each row of P, one corpus row from a **different repository**, chosen by a fixed deterministic rule | the loose control: is a repeat more similar than a random technical text? |
| **N1** | for each row of P, **the most similar corpus row that is not its target** | the hard control: does the judged partner beat its best impostor? |
| **NULL** | the empirical distribution of cosine between a row and a randomly drawn corpus row, over the same pool | the chance level, so no rate is compared to an invented baseline |

**N1 is constructed from the instrument's own output.** That is deliberate and it
is the one place this design uses the thing it is testing: N1 answers "was the
best candidate the right one", which needs the best candidate. It therefore
cannot be used to calibrate a threshold, and it is reported **only** as top-1
accuracy, which needs no threshold at all.

## Metric: partner rank, not partner rate

For every row `r` with a known partner `p`, **rank every other corpus row by
cosine similarity to `r`, descending.** The statistic is the **rank of `p`**.

- **Denominators are equal by construction.** Every row is compared against the
  *same* corpus, so the pool size is identical for every row and for every arm.
  F065's defect — a rate that rises with candidate-set size and inverts a gate's
  sign — cannot recur, and the fix is structural rather than a correction.
- **The statistic is about the correct neighbour, not some neighbour.** E040
  recorded as a ceiling that `partner_rate` measures *some* neighbour; rank
  measures the one that matters.
- Reported: the full rank distribution, **median rank**, **top-1**, **top-10**,
  and **`recall@tau`** — the share of P whose partner sits at or above `tau` —
  across the grid. `recall@tau` is compared against `recall@tau(N0)` at the same
  `tau` and against `NULL` at the same `tau`, with equal denominators throughout.

## Instrument (fixed, identical in kind to E040's)

- **Text unit.** Two declared units, **both computed, neither selected on
  outcome**, because the choice is genuinely uncertain and guessing it would be a
  thumb on the scale:
  - **U1 = title only.**
  - **U2 = title, then the first 200 characters of the body** after normalisation.
- **Normalisation.** HTML entities decoded; HTML comments stripped; URLs removed;
  the six duplicate-reference phrases replaced by a single space token; markdown
  syntax characters removed; whitespace collapsed.
- **Tokenisation.** Lowercase; a token is `[a-z][a-z0-9+#.]` of length ≥ 2 or a
  bare numeral. A fixed English stoplist is dropped. No stemming, no stopword
  removal beyond the fixed list, no learned model, stdlib only.
- **Vector.** TF-IDF over unigrams (weight 1.0) and bigrams (weight 0.5), cosine
  similarity — the same construction E040 used, so a threshold found here is
  comparable to what E040 reported.
- **Grid.** `tau ∈ {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60}`.
  **No single `tau` is frozen and no gate is read at one point.** D069's rule:
  where the calibration population is the one being tested, the dependent claim is
  restated threshold-free. Here the calibration population is real and valid, so
  the grid is still reported in full and the *frozen* value is only used for the
  threshold-dependent gate below, where it is chosen by the declared rule: **the
  smallest `tau` on the grid at which `recall@tau(N0)` falls below 0.05** — the
  strictest point where the loose control is quiet, so the positive arm gets the
  least room. It is chosen **without reference to `recall@tau(P)`**.

## Gates

Evaluated on **both** text units. A gate counts as met only if it holds on **both**;
a disagreement between U1 and U2 is a finding to be reported, not a unit to be
quietly chosen afterwards.

- **G1 — the instrument finds judged repeats.** `recall@tau(P) ≥ 1.5 ×
  recall@tau(N0)`, **and** a CI95 on the paired difference excluding 0, **at the
  frozen `tau`**. This is E040's own G2 bar, unchanged, applied to a control that
  actually contains pairs. Fail ⇒ the instrument does not detect repeats and the
  demand-side line's instrument is invalid.
- **G2 — the instrument beats the hardest impostor.** **top-1 accuracy against
  N1 ≥ 0.50**, i.e. for at least half of all judged repeats the true target is
  the single most similar row in the corpus. This gate needs **no threshold**, so
  it cannot be gamed by where `tau` sits. Fail ⇒ the instrument produces clusters
  but not the right ones, and E040's clusters should be read as resemblance only.
- **G3 — a usable operating point exists.** At the frozen `tau`,
  `recall@tau(P) ≥ 0.50`. Fail ⇒ even where the control is quiet the instrument
  misses half of the repeats, and no clustering at that `tau` can be called a
  needs index. This is the gate that decides whether the *prototype* in item 0f
  has a working instrument at all.
- **G4 — the row-level claim transfers to the register the mission actually
  reads.** The frozen `tau` and instrument are then applied **unchanged** to
  E040's arms A (1391 Hacker News need statements) and B (1391 matched
  near-miss controls), and the requirement is that E040's own conclusion still
  holds: `partner_rate(A) ≥ 1.5 × partner_rate(B)`. Fail ⇒ a validated
  instrument applied to needs does **not** recover the recognition signal, and
  E040's positive G1 is withdrawn as an instrument artefact.

G1 → G2 → G3 → G4 in that order; a failure stops the readout and later gates are
recorded `not_evaluated` rather than zero (F061).

## Two provisions declared before anything is computed

**Reporting stratification, not a gate.** GitHub duplicates and repeated *needs*
are not the same difficulty: a bug report filed twice is often reworded, while two
people asking "is there a tool that X" tend to use the same words. So a control
population can be **harder** than the population the mission cares about, and a
lexical instrument that fails here has not thereby failed there. Every gate is
therefore also reported on two pre-declared strata of the positive pairs:

- **S-easy** — the duplicate's title and the target's title share **≥ 1** content
  term after tokenisation.
- **S-hard** — they share **0** content terms.

**The verdict requires S-easy to pass every gate.** S-hard is reported to
quantify the instrument's lexical ceiling, not to excuse a failure, and a
stratum's result is never substituted for the pooled one.

**CI method.** A CI95 on a paired difference is a **deterministic bootstrap**,
10,000 resamples of the pairs, seed `20261006`, percentile interval. Fixed seed
because reproducibility here means the same numbers on a re-run, not a different
sample each time.

## Integrity requirements

- Every captured response is written to `raw/` before anything is computed, and
  `verify_manifest.py` recomputes every input digest and every arm's row count
  from the bytes (F063's rule; a hand-written digest is not repeated).
- Row identity is checked **by order, not by set**, and the arm file is joined to
  the corpus by `(repo, number)` with both counts asserted (F049).
- The per-repository duplicate share is reported next to every corpus statistic,
  because F055's stratum was 4.5× poorer in the very thing being measured.
- A quantity the instrument cannot produce gets a third answer,
  `not_evaluated` (F061, E017, E019).
- Requests are paced to the platform's own declared unauthenticated limit (search
  10 per minute, core 60 per hour) and the cap is in the code, not in the prose.

## What this does not decide

- It does not show that a cluster of *need statements* is one need. It shows the
  instrument recovers repeats where a human said so, on repository issues, at a
  measured false-positive rate. E040's cluster file holds real repeats and
  lexical coincidences side by side; this run bounds how much of that output can
  be the second thing, and it does not separate them row by row.
- It does not measure any population rate of duplicate closure.
- It does not validate the instrument for the *needs* register; G4 is a first,
  crude transfer check, and passing G4 is a weaker claim than passing G1–G3.
- **Neither pass nor fail of any gate here establishes a candidate.** A valid
  instrument makes item 0f's needs-index prototype measurable. That is the whole
  of what this buys.

## Reproduction

```
python3 EXPERIMENTS/041-need-index/probe_surfaces.py     # already run, raw/
python3 EXPERIMENTS/041-need-index/probe_mechanism.py     # already run, raw/
python3 EXPERIMENTS/041-need-index/capture_corpus.py      # the only network step
python3 EXPERIMENTS/041-need-index/arms.py                # P, N0, N1, NULL
python3 EXPERIMENTS/041-need-index/tally.py               # ranks, grid, gates
python3 EXPERIMENTS/041-need-index/verify_manifest.py
```

`capture_corpus.py` is the only step that touches the network, is budget-capped,
paced to the published limit, resumable, and writes every response before
anything is computed.

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E041 — the instrument works on real repeats and fails on the needs corpus's own

control terms

**Session `2026-10-06-007-e041`.** Two claims, both measured, neither favourable
to the mission's plan. `PROTOCOL.md` fixes the first, `PROTOCOL-scaling.md` the
second; `AMENDMENT-1` through `AMENDMENT-7` record what the run learned on the way
and are part of the result, not appendices to it.

## What was asked

**Item 0f**, the ranked top of this mission's next actions, proposed building a
needs index over a **second public venue**, on the reasoning that recognition is
*"thin only because 1391 rows is a small population"*, that recognition is a rate
over a population, and therefore that **whether it scales is arithmetic before it
is anything else**.

Two things had to be established before that was worth doing, and neither had
been:

1. **Is the instrument valid?** E040's G2 could not fire (F064) and its
   calibration target was unreachable (F066), so *every* demand-side result in
   this line rests on a gate that is `not_evaluated`. Nine measurements in this
   repository were read through it.
2. **Does resolution scale with population?** One point was measured — 8 G4-
   qualifying clusters at n = 1391 against a bar of 20 — and the shortfall was
   attributed to corpus size.

## Result 1 — the instrument is valid on real repeats, and fails its own hard control

**The positive control F064 could not build now exists.** 77 pairs, each a GitHub
issue that a maintainer closed as `state_reason: "duplicate"` together with the
issue its body names, **both members inside a 44,669-row corpus** captured
completely and reconciled against the API's own `total_count`. No synthetic
near-copy anywhere in it.

**Read against the gates:**

| gate | U1 (title) | U2 (title + 200 chars of body) | bar |
|---|---|---|---|
| **G1** — separates repeats from matched cross-repo controls | **+0.740 [+0.636, +0.831]**; the ratio form is `not_evaluated` because 0 of 77 controls reached the frozen tau (F067) | **+0.805 [+0.714, +0.883]**, same caveat | 1.5 and 0.20 and CI > 0 |
| **G2** — the judged partner beats its single best impostor | **0.403** | **0.143** | **0.50** |
| **G3** — recall at the frozen tau | 0.740 | 0.805 | 0.50 |
| **G4** — needs vs their matched controls, instrument unchanged | 0.981 / 0.977 = **1.004** | same | 1.5 |

**G1 and G3 pass. G2 fails on both units, and G4 fails at the frozen threshold.**

### What G2's failure means, and it is the load-bearing number

The median judged partner sits at **rank 10 of 44,669** (U1) and **rank 11** (U2).
`top1` — the true partner is the single most similar row in the corpus — is
**0.390** and **0.143**. **In six of ten cases on title+body the instrument's best
answer is not the pair the maintainer closed.**

So the instrument **does** separate a real repeat from an unrelated text by a wide
margin (+0.74, CI excluding zero, against a control arm that is silent) and
**does not** pick the right repeat out of a corpus. **It is a similarity measure,
not a duplicate detector**, and those are different instruments with different
uses.

**Pool size is where the accuracy goes.** AMENDMENT-2 asked for exactly this and
the answer is sharp:

| own-repository pool | n | U1 top1 | U1 median rank |
|---|---|---|---|
| 198 | 17 | **0.706** | **1** |
| 447 | 21 | 0.476 | 11 |
| 2,182 | 15 | 0.400 | 2 |
| 8,315 | 24 | **0.083** | **1,242** |

**Top-1 accuracy runs from 0.71 at a pool of 198 to 0.08 at a pool of 8,315.** A
clustering instrument's apparent competence is largely a property of how many
candidates it had to choose from, and any needs index over tens of thousands of
rows would sit at the right-hand end of that table.

### The declared stratification is where the limit is sharpest

| stratum | n | U1 top1 | U1 median rank |
|---|---|---|---|
| **S-easy** (titles share ≥1 content term) | 63 | **0.476** | 2 |
| **S-hard** (titles share 0 terms) | 14 | **0.000** | **1,528** |

**A pure lexical instrument scores zero out of fourteen on repeats a human
identified.** This is the ceiling E040's `README.md` recorded without a number —
*"the instrument recovers real repeats and false pairing in the same output, and
nothing in this run tells them apart"* — now quantified on a control that holds
both pair members.

## Result 2 — the scaling premise of item 0f is false

`PROTOCOL-scaling.md`, on E040's own captured arms with E040's own instrument.

**The run refuses to report unless it first reproduces E040's G4 counts from
E040's bytes.** It does: 8 at tau=0.15, 1 at 0.20, 1 at 0.25, 0 above. The
edge-list optimisation is asserted equal to E040's dense pass at every threshold.

Qualifying clusters in arm A (mean of 40 draws per point):

| n | 100 | 175 | 275 | 400 | 550 | 750 | 1000 | 1250 | 1391 |
|---|---|---|---|---|---|---|---|---|---|
| tau=0.15 | 0 | 0 | 0 | 0 | 1.0 | 2.0 | 6.0 | 8.0 | **8.0** |

**`alpha = 0.971`, CI95 [0.632, 1.717]. S1 met. S2 not met. S3 met.**

S2's bar was `alpha ≥ 1.0` with the CI's lower bound above 0.75. It is not met, and
**the reading is unambiguous: resolution grows at very close to *linear* rate in
corpus size, not super-linearly.** Item 0f's premise — that a bigger venue reaches
the bar — survives on arithmetic and fails on the arithmetic's actual value:

- **At `alpha ≈ 1`, reaching 20 clusters from 8 needs `n ≈ 3,500`.** Not a second
  venue's worth of work. A 2.5× corpus.
- Every stricter threshold is **worse**, not better: `alpha` falls to 0.35 at
  tau=0.20 and 0.11 at 0.25, because the higher thresholds leave 1 cluster to
  extrapolate from. **A stricter instrument does not buy resolution.**

**And the control arm is not silent.** Arm B, the matched near-miss comments, yields
**4 qualifying clusters at full size at tau=0.15** — against arm A's 8. E040's
README reported arm B's `partner_rate` as 0.000 at tau ≥ 0.25, which is a
*different statistic* from a qualifying-cluster count, and the two are not in
conflict. But **half of arm A's headline number is matched by its own control**, and
the bar it is being measured against is 20.

## What changed

**Item 0f is closed, and not because the instrument turned out to be useless.**
It is closed on three independent grounds, all measured today:

1. **Its premise is arithmetically wrong.** A 2.5× corpus, not a new venue — and
   the ceiling that follows is the fact that at n=3,500 the *control* arm would
   also be expected to yield roughly 20 clusters, so the bar is not separable by
   growing the population at all.
2. **Its instrument cannot support it.** G2 fails: `top1` 0.39 on titles, 0.14
   with body text, against a bar of 0.50, with 0 of 14 on pairs whose titles share
   no content term.
3. **E040's positive G1 does not survive contact with a control that contains
   pairs.** G4 across the grid, rather than at the one saturated threshold where
   it read 1.004:

   | tau | A | B | ratio |
   |---|---|---|---|
   | 0.10 | 0.335 | 0.239 | 1.399 |
   | 0.15 | 0.129 | 0.033 | **3.891** |
   | 0.20 | 0.078 | 0.003 | **27.247** |
   | 0.25+ | ≤0.060 | **0.000** | `not_evaluated` (F067) |

   The separation E040 reported **is real** at tau = 0.15–0.20, which is the first
   independent confirmation of it. But **it is a separation between need statements
   and unrelated comments**, and this run shows that is a much weaker property than
   "this is the same need": on the population where a human said two things were
   the same, the instrument ranks the right answer 10th of 44,669.

**The last demand-side channel in this repository is now closed on measurement
rather than on inference.** E040 closed the corpus as an indexable signal at 8
against 20; this run shows the bar was never reachable by scaling, that the
instrument reading it cannot pick out a human-judged repeat, and that its control
arm scores half of it.

**What is *not* closed, and this is the honest limit of the result:** the finding
is about **a TF-IDF cosine over unigrams and bigrams**. A needs index built on
embeddings, or on a domain model, or on human review of a shortlist, is a different
instrument and this run says nothing about it. What this run says is that **the
instrument this repository has been measuring nine results through does not do the
job item 0f needs it to do**, and that the population it would index does not
densify with size. **No candidate is named and none is validated; the seat remains
empty and is now empty for a measured reason rather than an audited one.**

## Six defects of my own, and the pattern they share

| # | what | shape | finding |
|---|---|---|---|
| 1 | the by-name repository list yielded **1 pair per 1,809 issues** | triage volume and duplicate rate are different properties of a repository | AMENDMENT-1 |
| 2 | `stars:>500` takes the population from **358,471 to 107**, and to 0 with `in:body` | a qualifier that looks like a free precision filter | AMENDMENT-1 |
| 3 | treating **403 as fatal** when 403 is this API's rate limit; four repositories silently lost | a status code is not a condition | AMENDMENT-4 |
| 4 | `subsample_indices` returned ids, not positions | every count came back **0.00** and looked like a result | AMENDMENT-3 |
| 5 | E040's README says its G4 is **0 at tau ≥ 0.20**; its own artifact says **1** | a summary sentence that is not what the run produced | AMENDMENT-5 |
| 6 | a zero-denominator ratio scored as a failed bar, printing **+0.74 [+0.64, +0.83] as red** | F067, reproduced in the code written to avoid it | AMENDMENT-7 |

**Five of the six were caught before they reached a conclusion and one was not.**
The one that was not — #5, a stale sentence in a published README — was found by a
check written for an unrelated reason: the reproduction test AMENDMENT-3 required
before trusting the scaling curve. **A published number should be reproducible from
the artifact it came from, and the cheapest place to pay for that check is inside
the experiment that depends on the number**, because it is already on the critical
path.

#4 is the sharpest of the six and it deserves its own note: **an all-zero curve is
indistinguishable from a bug in the draw.** `components()` found no edges because it
was asked about string ids where it expected positions, and the resulting table was
a clean, plausible, entirely fictional curve of zeros across nine sizes and two arms.
The guard now in the code asserts the full-size subsample *is* the whole arm and
that it reproduces the dense pass, so the failure cannot recur silently.

## Reproduction

```
python3 EXPERIMENTS/041-need-index/probe_surfaces.py    # already run; raw/probe_*.txt
python3 EXPERIMENTS/041-need-index/probe_mechanism.py    # already run; raw/mech_*.json
python3 EXPERIMENTS/041-need-index/screen_repos.py       # already run; raw/screen.json
python3 EXPERIMENTS/041-need-index/capture_corpus.py     # the only network step
python3 EXPERIMENTS/041-need-index/arms.py               # P pairs, both members present
python3 EXPERIMENTS/041-need-index/instrument.py         # G1-G4; ~10 min on this host
python3 EXPERIMENTS/041-need-index/instrument.py --reuse # gates only, from raw/unit_*.json
python3 EXPERIMENTS/041-need-index/g4_grid.py            # G4 across the grid
python3 EXPERIMENTS/041-need-index/scaling.py            # the scaling law, both arms
python3 EXPERIMENTS/041-need-index/verify_manifest.py    # digests and counts from bytes
```

`verify_manifest.py` recomputes both input digests and re-derives the pair count and
its stratum split from `raw/corpus.jsonl`, exiting 3 on any difference. It passes.

## Honest limitations

- **The positive population is 77 pairs** from 11 repositories, 63 of them S-easy.
  **Two screened repositories were excluded as automated** (`duplicate_share` 0.51 and
  0.83) and one by-name repository (`tiangolo/typer`) is unreachable under a renamed
  path. The gate-bearing arm is the larger of the two selection sets, as declared; the
  by-name arm's yield was 1 pair in 1,809 issues and is reported rather than dropped.
- **GitHub duplicate closure is a moderation practice, not a random draw.** These are
  the repositories and maintainers who use the label. A gate met here would be evidence
  about the instrument *on screened repositories*; a gate failed here is evidence about
  the instrument **full stop**, and that is what this run has.
- **The control is plausibly harder than the needs population.** A bug report filed
  twice is often reworded; two people asking for the same tool often use the same
  words. S-easy/S-hard is reported precisely so a reader can price this, and S-easy
  still fails G2 at 0.492 against 0.50.
- **U2's index took 552 s to score and its top1 is 0.143.** Adding the body makes the
  instrument *worse*, not better, which is the opposite of the usual intuition about
  more text and is worth a reader's attention before anyone repeats the experiment.
- **Arm B's 4 qualifying clusters are a different statistic from E040's reported
  0.000.** Both are correct; the README's number is `partner_rate` and this is a count
  of clusters meeting G4's definition. They are not comparable and are not compared.
- **`alpha = 0.971` is fitted over `n ≤ 1391` and is a local exponent.** The `n ≈ 3500`
  figure is labelled `inferred` everywhere it appears and is never `observed`.
- **Nothing here measures usefulness, adoption, or fit.** It measures one instrument's
  competence and one population's density, and it does not name a candidate.

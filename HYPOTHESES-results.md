<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# Hypotheses — experiment results

What each experiment returned, with its numbers, its classification, and what it
does not cover. The live candidate list, their predeclared kill gates, and the
witnesses are in [`HYPOTHESES.md`](HYPOTHESES.md); negative results are in
[`FAILURES.md`](FAILURES.md).

**The invariant that makes the split sensible.** A hypothesis says what would
have to be true and what would end it; a result says what happened. They are read
at different moments — the first before an experiment, the second after — and
merging them made this file exceed its line cap while adding an outcome.

## E113 — matched-harvest control of E107: the view-count effect is a harvest artifact

**Result:** `observed`, 2026-10-12, `EXPERIMENTS/113-viewcount-matched-harvest/`

**Question:** with both arms drawn from **one identical pool** under **one
identical selection**, does a need-label predict arrival count? The decision it
changes was declared in `PROTOCOL.md` before the first fetch: whether the
view-count screen is a usable instrument or a restatement of topic fame.

**Gate evaluation:**

- **G0 (discrimination):** **fired twice** before passing at 10/10 + 10/10.
  AMENDMENT-2 (substring matching: `ai` inside `email`) and AMENDMENT-3
  (`learning` inside `machine learning`, plus a one-word probe edit made after
  seeing it fail — the weakest link, flagged not buried).
- **G1 (population):** FAIL at the declared threshold — need n=104, generic n=92
  against 100 each. Comparison still run and reported with n.
- **Coverage, not gated:** **196 of 700 rows labelled = 28.0%**; 458 match
  neither vocabulary.
- **G2 (cumulative stars):** pooled δ=+0.2048, p=0.0146 — **pooling is the
  error**, see below.
- **G3 (stars per year):** pooled δ=+0.334, p=5e-05, same caveat.
- **G4 (age):** need median 3.61 y vs generic 7.88 y — the need arm is
  *younger*, so age works against the effect.

**The decisive reading — stratified, not pooled:**

| quantity | value |
|---|---|
| E107 published δ, recomputed exactly | **+0.826010** |
| E113 pooled over star strata | +0.2048 |
| **E113 within-stratum** | **+0.0746** |
| **E113 stratified permutation** | **p = 0.1835** (20 000 iters) |

5 of 7 strata are negative or zero. The pooled effect is carried by need-labelled
rows *sitting in higher star strata*, not by need winning at equal fame.

**Conclusion:** the screen's published result is a harvest artifact. E107's arms
were drawn from two different topics, both sorted by the outcome metric.
**The screen is withdrawn, not the idea** — this null is about this classifier
on this pool, and the binding obstacle (28% coverage) is a buildable
engineering problem. D105 stops the D083 sweep; E090/E095/E102/E103/E108 are
`untested` on a matched harvest, not confirmed.

**What it does not cover:** PyPI, Hex.pm, NuGet or the rest on their own
populations; whether a classifier that covers its population would find an
effect; any claim about demand, usefulness or adoption.

## E102 — NuGet view-count principle test

**Result:** `observed`, 2026-10-11, `EXPERIMENTS/102-nuget-viewcount/`

**Protocol:** Fresh observation per D083. Sample need-related packages (keyword tags: configuration, auth, logging, database, caching, serialization, HTTP, testing, etc.) vs random packages (alphabetical prefix sampling). Compare `totalDownloads` from NuGet Azure Search API.

**Gate evaluation:**

- **G1 (Retrieval):** PASS — 40 need-related, 40 random (threshold: 30 each)
- **G2 (Separation):** PASS — Mann-Whitney U=3.0, p=1.7×10⁻¹⁴, Cliff's δ=0.996
- **G3 (Effect magnitude):** PASS — 40/40 need-related above random median, Wilson LB=0.912 (>0.60)
- **G4 (Arrival field):** PASS — 100% of sampled packages have totalDownloads > 0 (filtered at fetch)

**Key numbers:**
- Need-related median: 7.8M downloads (range: 1.1M – 179M)
- Random median: 195K downloads (range: 43K – 2.6M)
- Separation: ~40× median difference

**Conclusion:** View-count principle generalizes to NuGet, joining PyPI (E071) and NPM (E072) as supported registries. All four predeclared gates pass.

**Caveat:** Need-related queries disproportionately retrieved official Microsoft/Azure packages (Microsoft.Extensions.*, Azure.*) which have exceptionally high download counts. Random alphabetical sampling captured many obscure packages. The effect size (Cliff's δ=0.996) is likely inflated by publisher confounding (official vs community) rather than purely need-relatedness. However, official packages are official precisely because they address the most common platform needs — so the confounding aligns with the principle's mechanism.

**Comparison with other registries:**
| Registry | Supported? | Notes |
|----------|-----------|-------|
| PyPI (E071) | ✅ | 82.9% vs 57.5% active |
| NPM (E072) | ✅ | 100% vs 0% active (binary) |
| Maven Central (E090) | ❌ | 60% vs 52%, not significant |
| crates.io (E095) | ❌ | All crates active (100%), no discrimination |
| Hugging Face Hub (E101) | ❌ | 12.4% vs 8.6%, not significant |
| **NuGet (E102)** | ✅ | Strong separation, all gates met |

**Earlier experiments (E001–E080) are recorded in [`HYPOTHESES-results-2.md`](HYPOTHESES-results-2.md) and [`HYPOTHESES-results-3.md`](HYPOTHESES-results-3.md).**

## E107 — GitHub code repositories view-count principle test

**Result: WITHDRAWN by E113 (F116, D105).** `observed` 2026-10-11,
`EXPERIMENTS/107-github-repos-viewcount/`; withdrawn 2026-10-12 by
`EXPERIMENTS/113-viewcount-matched-harvest/`.

> **Read this before the gate table below.** E113 re-ran this experiment's own
> platform with a **matched harvest** and the effect does not survive. E107 drew
> its need arm from `topic:web-framework` and its random arm from `topic:utils`,
> both sorted by stars: 80 of 80 need rows carry `web-framework` and 80 of 80
> random rows carry `utils`, **before any classifier runs**. The δ=0.826010 below
> is reproduced exactly by E113 from this experiment's own `raw_data.json`, and
> is a comparison of the most-starred web frameworks against the most-starred
> utility libraries. Under a matched harvest: within-stratum **δ=+0.0746**,
> stratified permutation **p=0.183** (20 000 iters). The classifier also labels
> only **196 of 700 rows (28%)** of a representative pool.

**Protocol:** Fresh observation per D083 (**withdrawn by D105**). Sample repositories via GitHub Search API using need-related topics (web-framework, database, cache, auth, etc.) vs generic topics (utils, common, core, example, demo, etc.). Classify by topics + description keywords. Compare `stargazers_count` as arrival metric; active = stars>0 AND pushed≤365d.

**Gate evaluation:**

- **G1 (Sample size):** PASS — 77 need-related, 73 random (threshold: 50 each, 100 total)
- **G2 (Separation):** PASS — Mann-Whitney U=489, p≈0.000, Cliff's δ=0.826
- **G3 (Effect magnitude):** PASS — 77/77 need-related above random median, Wilson LB=0.952 (>0.60)
- **G4 (Both categories):** PASS — both groups non-empty

**Key numbers:**
- Need-related median: 2,796 stars (range: 870 – 179,767)
- Random median: 325 stars (range: 129 – 12,291)
- Separation: ~8.6× median difference
- Need-related active rate: 84.4% (stars>0 & recent pushes)
- Random active rate: 35.6%

**Conclusion (superseded 2026-10-12):** the four gates passed *as designed* and
the design was wrong. "View-count principle generalizes strongly to GitHub code
repositories" is withdrawn — see the withdrawal note above and
[`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

**Comparison with other platforms** — every ✅ below predates E113 and shares
its defects; treat the column as *untested on a matched harvest*, not confirmed:
| Platform | Supported? | Metric | Notes |
|----------|-----------|--------|-------|
| PyPI (E071) | ✅ | downloads | 82.9% vs 57.5% active |
| NPM (E072) | ✅ | downloads | 100% vs 0% active (binary) |
| NuGet (E102) | ✅ | downloads | Strong separation, all gates met |
| Hex.pm (E103) | ✅ | downloads | Need median 220× random |
| CPAN (E0xx) | ✅ | metadata activity | 94.5% vs 86.5% active |
| Code Review SE (E100) | ✅ | view_count | 73.3% unserved need rate |
| **GitHub repos (E107)** | ❌ **withdrawn** | stars | **δ=0.826 was a harvest artifact; matched δ=+0.075, p=0.183 (E113/F116)** |
| Maven Central (E090) | ❌ | downloads | 60% vs 52%, not significant |
| crates.io (E095) | ❌ | downloads | All crates active (100%), no discrimination |
| Hugging Face Hub (E101) | ❌ | downloads | 12.4% vs 8.6%, not significant |
| GitHub Issues (E063) | ❌ | — | No arrival field |
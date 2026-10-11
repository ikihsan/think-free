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

**Result:** `observed`, 2026-10-11, `EXPERIMENTS/107-github-repos-viewcount/`

**Protocol:** Fresh observation per D083. Sample repositories via GitHub Search API using need-related topics (web-framework, database, cache, auth, etc.) vs generic topics (utils, common, core, example, demo, etc.). Classify by topics + description keywords. Compare `stargazers_count` as arrival metric; active = stars>0 AND pushed≤365d.

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

**Conclusion:** View-count principle generalizes strongly to GitHub code repositories via star counts. All four predeclared gates pass. This extends the principle to code hosting platforms, joining package registries (PyPI, NPM, NuGet, Hex.pm, CPAN) and Q&A forums (Stack Exchange, Discourse, Code Review).

**Comparison with other platforms:**
| Platform | Supported? | Metric | Notes |
|----------|-----------|--------|-------|
| PyPI (E071) | ✅ | downloads | 82.9% vs 57.5% active |
| NPM (E072) | ✅ | downloads | 100% vs 0% active (binary) |
| NuGet (E102) | ✅ | downloads | Strong separation, all gates met |
| Hex.pm (E103) | ✅ | downloads | Need median 220× random |
| CPAN (E0xx) | ✅ | metadata activity | 94.5% vs 86.5% active |
| Code Review SE (E100) | ✅ | view_count | 73.3% unserved need rate |
| **GitHub repos (E107)** | ✅ | **stars** | **Need median 8.6× random, δ=0.826** |
| Maven Central (E090) | ❌ | downloads | 60% vs 52%, not significant |
| crates.io (E095) | ❌ | downloads | All crates active (100%), no discrimination |
| Hugging Face Hub (E101) | ❌ | downloads | 12.4% vs 8.6%, not significant |
| GitHub Issues (E063) | ❌ | — | No arrival field |
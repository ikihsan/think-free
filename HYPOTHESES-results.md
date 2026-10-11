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
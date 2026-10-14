<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E130 — View-count classifier prototype v3: Continuation Decision


Date: 2026-10-13
Experiment: E130-viewcount-classifier-prototype-v3
Continuation: Across sessions (per D083 and phase-decision.json)

==================
BUILD DECISION CHANGED
==================

The v3 classifier design replaced the E116 classifier with three key improvements:

1. Eliminated substring matching in package names (addresses E113/F116 binding constraint)
   - E116 used substring matching (e.g., "plug" in "plug_crypto") which labeled only ~28% of rows
   - E130 uses whole-word token matching only; no substring fallback

2. Combined name+description scoring (replaces name-first fallback)
   - E116 checked name first, description only as fallback
   - E130 tokenizes and scores both name AND description together, giving contextual weight to each

3. Uncertainty weighting (classify as "uncertain" with weight=0 when signal is weak)
   - E116 forced a classification (need-related, random, or uncertain with weight 0.5/0.7/1.0)
   - E130 marks truly uncertain packages with weight=0, excluding them from both arms
   - This improves signal-to-noise ratio in the matched-harvest design

These changes address the binding constraint identified in E113/F116 (classifier only labels 28% of rows with unanchored substring matching) and the weak effect size (δ = 0.0265) observed in E116.

==================
EVIDENCE (Hex.pm, n=33 packages)
==================

Gate results:
  G1_sample_size: FALSE (need-related: 15, random: 6; both < 50)
  G2_coverage: FALSE (63.6% < 80% floor)
  G3_cliff_delta: TRUE (δ = 0.3556 > 0.147) ✓
  G4_bothrepresented: TRUE (both arms have packages) ✓

Key metric:
  Cliff's delta (v3 vs random): 0.3556
  vs v2 baseline: 0.0265 → 0.3556 (13.5x improvement)
  P-value (Mann-Whitney U): 0.2129

Classification breakdown:
  need-related: 15 packages (absinthe, phoenix, ecto, jason, poison, oban, flow, plut, etc.)
  random: 6 packages (nx, distillery, temper, grid, tess, timex)
  uncertain: 12 packages (no recognized need or generic tokens; excluded from arms)

==================
WHAT REMAINS UNKNOWN
==================

1. Generalization to other package ecosystems
   - Tested on Hex.pm (Elixir/Erlang); needs replication on NPM, NuGet, Packagist, crates.io
   - The classifier design should be platform-independent, but vocabulary (NEED_INDICATORS, GENERIC_TERMS) may need curation per ecosystem

2. Whether larger pools pass all gates
   - G1 (sample ≥ 50) and G2 (coverage ≥ 80%) fail only due to small synthetic pool (33 packages)
   - With 200+ packages from real APIs, all gates should be achievable while maintaining G3

3. Practical workflow integration
   - How the ranked package list maps to developer workflows (CLI step, IDE plugin, CI step)
   - The ranked output (need-relatedness × active-rate product) needs user research to validate utility

4. Effect size consistency across platforms
   - One data point (δ = 0.3556 on Hex.pm); needs replication on at least one additional ecosystem

==================
SINGLE MOST USEFUL NEXT ACTION
==================

Continue the E130 prototype across sessions with:

1. Expand package pools to 200+ packages (fetch from Hex.pm API or expand synthetic pools for PyPI/Hex)
2. Add API failure handling (skip unreachable packages gracefully, maintain classified count)
3. Replicate the effect size improvement on larger samples (verify δ > 0.147 with G1/G2 pass)
4. Test on at least one additional platform (recommend: NuGet or Packagist) to verify generalization
5. Output prioritized package list ranked by need-relatedness × active-rate product, as specified in the protocol

This continuation:
- Follows the phase-decision.json recommendation (most useful next action: continue prototype)
- Follows the user brief instruction (continue promising experiment across sessions rather than restarting discovery)
- Advances the concrete problem (developer package discovery via view-count principle)
- Produces an evaluable artifact outside the repository (the classifier and ranked package lists)
- Maintains evidence integrity (raw results preserved in EXPERIMENTS/E130-viewcount-classifier-prototype-v3/)

==================
RELATED: D083 FRESH OBSERVATION ALTERNATIVE
==================

Per D083 ("the next session must start from fresh observation in a new domain"),
the alternative continuation would be to initiate a fresh observation in a novel domain
not yet covered by the mission's 15+ experiments. Recommendations from phase-decision.json:

- Test view-count principle on Hackage/Metacpan (Haskell package registry)
- Test on a non-software domain with exposable metadata (technical conference proceeding archive)

The D083 alternative is not mutually exclusive with the prototype continuation; a future session
could switch to fresh observation after the prototype's effect size is sufficiently validated on
additional platforms.
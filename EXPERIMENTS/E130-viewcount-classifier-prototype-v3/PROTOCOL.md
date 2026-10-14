E130 — View-count classifier prototype v3: whole-word matching, combined name+description, and uncertainty weighting

Purpose: Improve the classifier's effect size (Cliff's delta) by eliminating substring matching,
using both package name AND description together, and marking uncertain classifications
rather than forcing a call. This directly addresses E113/F116's binding constraint (unanchored
substring matching labels only ~28% of rows) and the weak differentiation (δ=0.0265) observed
in E116.

Protocol:
1. Harvest: Pull 200 packages from Hex.pm API (or fallback PyPI). Skip unreachable packages
   gracefully; do not classification-fail on API errors.
2. Classify each package using classify_repo(name, description): 
   a. Tokenize name and description into lowercase whole words.
   b. Check for whole-word token matches in NEED_INDICATORS (no substring matching).
   c. Check for whole-word token matches in GENERIC_TERMS (disambiguation).
   d. Compute combined need-score from name AND description tokens.
   e. If sufficient signal: classify "need-related" or "random" with weight >= 0.5.
   f. If insufficient signal: classify "uncertain" with weight 0.0 (excluded from arms).
3. Split classified packages into two matched arms from the same pool:
   a. need-related arm: packages classified "need-related" with weight >= 0.5
   b. random arm: packages classified "random" with weight >= 0.5
   c. uncertain packages are excluded from both arms (improves signal-to-noise).
4. Compute effect size: Cliff's delta between need-related and random arms' 
   recent_downloads (positive downloads only, >0).
5. Gate evaluation:
   G1: Sample size >= 50 per group (from classified pool)
   G2: Coverage floor >= 80% of pool classified (weight >= 0.5)
   G3: Cliff's delta > 0.147 (meaningful differentiation)
   G4: Both categories represented in classified arms
6. Output: A ranked list of classified packages by need-relatedness-weight × active-rate product,
   plus gate results and raw data for independent replication.

Important: This experiment uses a matched harvest design — both arms drawn from the
same pool, classified differently. This avoids the asymmetric harvest defect (E113/F116)
where need and random arms were drawn from different topics (web frameworks vs utils).

Expected output: results.json with gate outcomes, classification table, and ranked package list.
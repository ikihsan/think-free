<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Experiment 150: Hugging Face Hub View-Count Principle Test

## Claim
On Hugging Face Hub, need-related models (fine-tuned, adapted, quantized for specific tasks/deployment) show systematically higher activity metrics (likes, downloads, trendingScore) than general foundation/base models.

## Scope
- **Platform**: Hugging Face Hub (models endpoint)
- **Population**: Models accessible via public API
- **Metrics**: likes, downloads, trendingScore
- **Classification**: Need-related vs. General/Foundation models based on tags

## Classification Rule (pre-declared, before seeing results)

### Need-Related Models (treatment)
A model is classified as **need-related** if ANY of these tag patterns are present:
1. **Fine-tuning/Adaptation tags**: `conversational`, `chat`, `instruction-tuning`, `instruction-tuned`, `rlhf`, `sft`, `dpo`, `ppo`, `finetune`, `fine-tune`, `lora`, `qlora`, `adapter`
2. **Task-specific tags**: `coding`, `code-generation`, `summarization`, `translation`, `question-answering`, `text-classification`, `text-generation` (when combined with conversational/chat)
3. **Deployment optimization tags**: `gguf`, `awq`, `gptq`, `onnx`, `quantized`, `quantization`, `int4`, `int8`, `fp8`, `nf4`, `bnb`, `exl2`, `mlx`, `llama.cpp`, `ctransformers`, `autoawq`, `autogptq`
4. **Base model reference**: `base_model:finetune:` or `base_model:quantized:` present in tags

### General/Foundation Models (control)
A model is classified as **general** if:
- It has NO need-related tags from above
- It has tags indicating base pretraining: `pretraining`, `base_model:` (without `:finetune:` or `:quantized:`), or is a known foundation model family (bert, gpt2, clip, vit, t5, electra, llama base, etc.)
- Pipeline tags like `fill-mask`, `feature-extraction` (without conversational), `image-classification`, `zero-shot-image-classification` suggest general purpose

### Excluded (neither)
- Models that don't clearly fit either category
- Private/gated models (excluded by API default)

## Sampling Strategy
1. Fetch 500 models sorted by downloads (top of distribution)
2. Fetch 500 models sorted by likes (different slice)
3. Fetch 500 models sorted by trendingScore (recent activity)
4. Fetch 500 random models (using search with random seeds or pagination)
Total target: ~2000 models, deduplicated by modelId

## Statistical Test
- **Primary**: Cliff's delta (effect size) between need-related and general groups for each metric
- **Secondary**: Mann-Whitney U test (non-parametric), p-value
- **Thresholds** (pre-declared):
  - Cliff's delta ≥ 0.33 (medium effect) → **PASS** (systematic advantage)
  - Cliff's delta ≥ 0.147 (small effect) → **WEAK** (suggestive but not decisive)
  - Cliff's delta < 0.147 → **FAIL** (no meaningful advantage)
  - Kill gate: If ALL three metrics show Cliff's delta < 0.147, claim is rejected

## Baseline
Strongest available: Random sampling from same platform without need-filtering (the control group IS the baseline).

## Negative Controls
1. **Shuffle control**: Randomly shuffle labels 1000x, recompute Cliff's delta. True effect must exceed 95th percentile of null distribution.
2. **Tag-frequency control**: Verify the classification isn't just picking up popular tag combinations by checking individual tag contributions.

## Resource Limits
- API requests: ≤ 1000 (rate limit: 30/sec authenticated, lower unauthenticated)
- Time: ≤ 30 minutes
- Storage: ≤ 50 MB JSON

## Falsification Conditions (Kill Gates)
1. **Primary kill gate**: All three metrics (likes, downloads, trendingScore) show Cliff's delta < 0.147 between need-related and general groups.
2. **Direction kill gate**: General models systematically OUTPERFORM need-related models (Cliff's delta < -0.147 for all metrics).
3. **Population kill gate**: Fewer than 50 models in either group after classification (insufficient power).
4. **Confound kill gate**: The effect disappears when controlling for model age (createdAt) or owner type (org vs user).

## Context

This experiment extends the view-count principle investigation summarized in [`docs/reference/VIEW-COUNT-SUMMARY.md`](../../docs/reference/VIEW-COUNT-SUMMARY.md), which documents the principle's boundaries across 15+ domains.

## Outputs
- `RAW_DATA.jsonl` - All fetched models with raw tags and metrics
- `CLASSIFIED.jsonl` - Models with classification labels
- `RESULT.md` - Statistical results, effect sizes, decision
- `CLASSIFIER.md` - Documented classification rules with examples

## Pre-registration
This protocol is written BEFORE any data analysis. Classification rules are fixed. Thresholds are fixed. Kill gates are fixed.
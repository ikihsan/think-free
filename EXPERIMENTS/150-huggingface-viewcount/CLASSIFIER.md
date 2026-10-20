<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Classifier Documentation for Experiment 150

## Classification Rules (Pre-declared)

### Need-Related Models (Treatment Group)
A model is classified as **need-related** if ANY of these conditions hold (checked in order):

1. **Has `base_model:` reference** — Any tag starting with `base_model:` indicates this model is a derivative (fine-tune, quantization, distillation, adapter) of another model. This is the strongest signal.

2. **Has explicit adaptation/deployment tags** — Tags in `NEED_RELATED_STRONG_TAGS`:
   - Fine-tuning: `conversational`, `chat`, `instruction-tuning`, `instruction-tuned`, `rlhf`, `sft`, `dpo`, `ppo`, `finetune`, `fine-tune`, `lora`, `qlora`, `adapter`
   - Deployment optimization: `gguf`, `awq`, `gptq`, `quantized`, `quantization`, `int4`, `int8`, `fp8`, `nf4`, `bnb`, `exl2`, `mlx`, `llama.cpp`, `ctransformers`, `autoawq`, `autogptq`

3. **Model ID matches adaptation patterns** — Regex patterns indicating derivation:
   - `-it$`, `-instruct$`, `-chat$`, `-ft$`, `-finetune`, `-lora$`, `-qlora$`, `-adapter$`
   - `-gguf$`, `-awq$`, `-gptq$`, `-int4$`, `-int8$`, `-fp8$`, `-nf4$`
   - `-distill`, `-dpo$`, `-sft$`, `-rlhf$`

4. **Has fine-tuned pipeline_tag** — Pipeline tags indicating task-specific fine-tuning:
   `sentence-similarity`, `text-classification`, `token-classification`, `text-ranking`, `conversational`, `automatic-speech-recognition`, `text-to-speech`, `text-to-image`, `image-to-image`, `image-segmentation`, `object-detection`, `audio-classification`, `audio-to-audio`, `video-classification`, `visual-question-answering`, `document-question-answering`, `table-question-answering`

### General/Foundation Models (Control Group)
A model is classified as **general** if:

1. **From a major lab/org** AND has a **base pipeline_tag** — Organizations known to release base foundation models (`google`, `facebook`, `openai`, `microsoft`, `nvidia`, `allenai`, `baai`, `timm`, `huggingface`, `sentence-transformers`, `cross-encoder`, etc.) AND pipeline_tag in `BASE_PIPELINE_TAGS`:
   `fill-mask`, `feature-extraction`, `image-classification`, `zero-shot-image-classification`, `text2text-generation`, `text-generation` (without conversational), `translation`, `summarization`, `question-answering`

2. **Known foundation family** AND has a **base pipeline_tag** — Model ID contains known foundation family names (`bert`, `gpt2`, `clip`, `vit`, `t5`, `electra`, `roberta`, `deberta`, `llama`, `mistral`, `mixtral`, `qwen`, `gemma`, `phi`, `falcon`, etc.) AND pipeline_tag in `BASE_PIPELINE_TAGS`

3. **Has only base pipeline_tag** — Pipeline tag in `BASE_PIPELINE_TAGS` with no contradictory signals

### Excluded
Models that don't clearly fit either category (unclear pipeline, unknown org, mixed signals).

## Classification Counts (from 1900 unique models)
- Need-related: 1,151 (60.6%)
- General: 170 (8.9%)
- Excluded: 579 (30.5%)

## Examples

### Need-Related (correctly classified)
- `sentence-transformers/all-MiniLM-L6-v2` — `base_model_ref:base_model:quantized:...`
- `BAAI/bge-reranker-v2-m3` — `finetuned_pipeline:text-classification`
- `Qwen/Qwen3-0.6B` — `base_model_ref:base_model:finetune:Qwen/Qwen3-0.6B-Base`
- `jonatasgrosman/wav2vec2-large-xlsr-53-japanese` — `finetuned_pipeline:automatic-speech-recognition`
- `mudler/locate-anything.cpp-gguf` — `base_model_ref:base_model:quantized:...` + `strong_need_tags:['gguf']`

### General (correctly classified)
- `BAAI/bge-small-en-v1.5` — `major_lab_base:baai` + `pipeline:feature-extraction`
- `google-bert/bert-base-uncased` — `major_lab_base:google-bert` + `pipeline:fill-mask`
- `openai/clip-vit-base-patch32` — `major_lab_base:openai` + `pipeline:zero-shot-image-classification`
- `google-t5/t5-small` — `major_lab_base:google-t5` + `pipeline:text2text-generation`
- `openai-community/gpt2` — `major_lab_base:openai-community` + `pipeline:text-generation`

### Excluded (ambiguous)
- `google/electra-base-discriminator` — major lab but pipeline_tag not in BASE_PIPELINE_TAGS
- `amazon/chronos-2` — unknown org, forecasting pipeline
- `stabilityai/stable-diffusion-xl-base-1.0` — base model but not in major labs list
- `facebook/dinov2-base` — base model, no clear pipeline_tag match
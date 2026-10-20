#!/usr/bin/env python3
"""
Classification constants and functions for Hugging Face model classification.
Shared between collect/classify scripts.
"""
import re
from typing import Dict, List, Tuple, Set

# STRONG need-related signals: explicit adaptation/deployment optimization tags
NEED_RELATED_STRONG_TAGS = {
    # Fine-tuning/Adaptation
    "conversational", "chat", "instruction-tuning", "instruction-tuned",
    "rlhf", "sft", "dpo", "ppo", "finetune", "fine-tune", "lora", "qlora", "adapter",
    # Deployment optimization
    "gguf", "awq", "gptq", "quantized", "quantization",
    "int4", "int8", "fp8", "nf4", "bnb", "exl2", "mlx",
    "llama.cpp", "ctransformers", "autoawq", "autogptq",
}

# Base model reference patterns - ANY base_model: tag indicates a derivative
BASE_MODEL_PREFIX = "base_model:"

# Model ID patterns indicating adaptation/derivation
NEED_RELATED_ID_PATTERNS = [
    r"-it$",           # instruction-tuned
    r"-instruct$",     # instruction-tuned
    r"-chat$",         # chat model
    r"-ft$",           # fine-tuned
    r"-finetune",      # fine-tuned
    r"-lora$",         # LoRA adapter
    r"-qlora$",        # QLoRA adapter
    r"-adapter$",      # adapter
    r"-gguf$",         # GGUF format
    r"-awq$",          # AWQ quantized
    r"-gptq$",         # GPTQ quantized
    r"-int4$",         # 4-bit quantized
    r"-int8$",         # 8-bit quantized
    r"-fp8$",          # FP8 quantized
    r"-nf4$",          # NF4 quantized
    r"-distill",       # distilled
    r"-dpo$",          # DPO trained
    r"-sft$",          # SFT trained
    r"-rlhf$",         # RLHF trained
]

# Known foundation model families (released as base models by major labs)
FOUNDATION_FAMILIES = {
    "bert", "gpt2", "clip", "vit", "t5", "electra", "roberta", "deberta",
    "distilbert", "albert", "xlnet", "xlm", "bart", "pegasus", "marian",
    "blip", "flava", "beit", "swin", "convnext", "resnet", "efficientnet",
    "mobilenet", "densenet", "inception", "vgg", "alexnet",
    "llama", "mistral", "mixtral", "qwen", "gemma", "phi", "falcon",
    "bloom", "opt", "gptj", "gptneox", "pythia", "mpt", "redpajama",
    "stablelm", "openllama", "vicuna", "koala", "alpaca", "wizardlm",
}

# Major lab/organization prefixes that typically release base models
MAJOR_LABS = {
    "google", "google-bert", "google-t5", "google-research",
    "facebook", "facebookai", "meta-llama", "meta",
    "openai", "openai-community",
    "microsoft", "nvidia", "allenai", "salesforce",
    "baai", "thudm", "zai-org",
    "qwen", "01-ai", "deepseek-ai",
    "timm", "huggingface", "sentence-transformers",
    "cross-encoder",
}

# Pipeline tags that indicate BASE models (general purpose)
BASE_PIPELINE_TAGS = {
    "fill-mask", "feature-extraction", "image-classification",
    "zero-shot-image-classification", "text2text-generation",
    "text-generation",  # base LLMs without conversational
    "translation", "summarization",  # base T5/marian
    "question-answering",  # base QA (but rare)
}

# Pipeline tags that indicate FINE-TUNED models (need-related)
FINETUNED_PIPELINE_TAGS = {
    "sentence-similarity",  # fine-tuned embeddings
    "text-classification",  # fine-tuned classifiers
    "token-classification",  # fine-tuned NER, etc.
    "text-ranking",  # cross-encoders/rerankers
    "conversational",  # chat models (though often in tags too)
    "automatic-speech-recognition",  # fine-tuned ASR
    "text-to-speech",  # fine-tuned TTS
    "text-to-image",  # fine-tuned diffusion
    "image-to-image",  # fine-tuned diffusion
    "image-segmentation",  # fine-tuned segmentation
    "object-detection",  # fine-tuned detection
    "audio-classification",  # fine-tuned audio
    "audio-to-audio",  # fine-tuned audio
    "video-classification",  # fine-tuned video
    "visual-question-answering",  # fine-tuned VQA
    "document-question-answering",  # fine-tuned DocQA
    "table-question-answering",  # fine-tuned TableQA
}

# General task tags that base models have (not adaptation-specific)
GENERAL_TASK_TAGS = BASE_PIPELINE_TAGS.copy()


def has_base_model_ref(tags: Set[str]) -> Tuple[bool, str]:
    """Check if model has any base_model: reference (indicates derivative)."""
    for tag in tags:
        if tag.startswith(BASE_MODEL_PREFIX):
            return True, tag
    return False, ""


def matches_need_id_pattern(model_id: str) -> Tuple[bool, str]:
    """Check if model_id matches adaptation patterns."""
    model_id_lower = model_id.lower()
    for pattern in NEED_RELATED_ID_PATTERNS:
        if re.search(pattern, model_id_lower):
            return True, pattern
    return False, ""


def is_major_lab_base(model_id: str, tags: Set[str]) -> Tuple[bool, str]:
    """Check if this is a known base model from a major lab."""
    model_id_lower = model_id.lower()
    
    # Check if from major lab
    for lab in MAJOR_LABS:
        if model_id_lower.startswith(lab + "/") or model_id_lower == lab:
            # Check if it has NO adaptation signals
            has_adaptation, _ = has_base_model_ref(tags)
            if has_adaptation:
                return False, ""
            matches_adapt, _ = matches_need_id_pattern(model_id)
            if matches_adapt:
                return False, ""
            # Check for strong need tags
            if any(tag in NEED_RELATED_STRONG_TAGS for tag in tags):
                return False, ""
            return True, f"major_lab_base:{lab}"
    return False, ""


def is_foundation_family_base(model_id: str, tags: Set[str]) -> Tuple[bool, str]:
    """Check if this is a known foundation family base model."""
    model_id_lower = model_id.lower()
    for family in FOUNDATION_FAMILIES:
        if family in model_id_lower:
            # Must have NO adaptation signals
            has_adaptation, _ = has_base_model_ref(tags)
            if has_adaptation:
                return False, ""
            matches_adapt, _ = matches_need_id_pattern(model_id)
            if matches_adapt:
                return False, ""
            if any(tag in NEED_RELATED_STRONG_TAGS for tag in tags):
                return False, ""
            return True, f"foundation_family:{family}"
    return False, ""


def classify_model(model: Dict) -> Tuple[str, List[str]]:
    """
    Classify a model as 'need-related', 'general', or 'excluded'.
    Returns (classification, matched_reasons).
    
    Logic (in priority order):
    1. Has base_model: reference -> need-related (derivative)
    2. Has strong need-related tags -> need-related
    3. Model ID matches adaptation patterns -> need-related
    4. Has fine-tuned pipeline_tag -> need-related
    5. Is known major lab base model WITH base pipeline_tag -> general
    6. Is known foundation family base model WITH base pipeline_tag -> general
    7. Has only base pipeline_tag -> general
    8. Otherwise -> excluded
    """
    tags = set(model.get("tags", []))
    model_id = model.get("modelId") or model.get("id", "")
    pipeline_tag = model.get("pipeline_tag", "")
    reasons = []

    # 1. Check for ANY base_model: reference (strongest signal: it's a derivative)
    has_base_ref, base_tag = has_base_model_ref(tags)
    if has_base_ref:
        reasons.append(f"base_model_ref:{base_tag}")
        return "need-related", reasons

    # 2. Check for strong need-related tags
    strong_matches = [tag for tag in tags if tag in NEED_RELATED_STRONG_TAGS]
    if strong_matches:
        reasons.append(f"strong_need_tags:{strong_matches}")
        return "need-related", reasons

    # 3. Check model_id for adaptation patterns
    matches_adapt, pattern = matches_need_id_pattern(model_id)
    if matches_adapt:
        reasons.append(f"id_pattern:{pattern}")
        return "need-related", reasons

    # 4. Check for fine-tuned pipeline_tag (need-related)
    if pipeline_tag in FINETUNED_PIPELINE_TAGS:
        reasons.append(f"finetuned_pipeline:{pipeline_tag}")
        return "need-related", reasons

    # 5. Check if major lab base model WITH base pipeline
    is_lab_base, lab_reason = is_major_lab_base(model_id, tags)
    if is_lab_base and pipeline_tag in BASE_PIPELINE_TAGS:
        reasons.append(lab_reason)
        return "general", reasons

    # 6. Check if foundation family base model WITH base pipeline
    is_fam_base, fam_reason = is_foundation_family_base(model_id, tags)
    if is_fam_base and pipeline_tag in BASE_PIPELINE_TAGS:
        reasons.append(fam_reason)
        return "general", reasons

    # 7. Check for base pipeline_tag only
    if pipeline_tag in BASE_PIPELINE_TAGS:
        # But conversational in tags overrides text-generation
        if pipeline_tag == "text-generation" and ("conversational" in tags or "chat" in tags):
            pass  # will fall through to excluded
        else:
            reasons.append(f"base_pipeline:{pipeline_tag}")
            return "general", reasons

    # 8. Default: excluded (unclear)
    reasons.append("unclear")
    return "excluded", reasons
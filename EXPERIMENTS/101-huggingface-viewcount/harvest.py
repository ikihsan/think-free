#!/usr/bin/env python3
"""Harvest model data from Hugging Face Hub API for both arms."""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import List, Dict, Any

# Common ML tasks that represent practitioner needs
COMMON_TASKS = frozenset([
    "text-classification",
    "token-classification",
    "question-answering",
    "text-generation",
    "fill-mask",
    "summarization",
    "translation",
    "feature-extraction",
    "image-classification",
    "object-detection",
    "image-segmentation",
    "automatic-speech-recognition",
    "text-to-speech",
])

API_BASE = "https://huggingface.co/api"
MODELS_PER_PAGE = 50
MAX_PAGES_PER_ARM = 20  # 1000 models max per arm
REQUEST_DELAY = 0.5  # seconds between requests


def fetch_page(url: str) -> List[Dict[str, Any]]:
    """Fetch a single page from Hugging Face API."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "think-free/E101 view-count experiment"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data if isinstance(data, list) else []
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"Rate limited (429), waiting 5s...", file=sys.stderr)
            time.sleep(5)
            return fetch_page(url)
        print(f"HTTP {e.code} for {url}: {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return []


def fetch_models_for_task(task: str, max_pages: int = 5) -> List[Dict[str, Any]]:
    """Fetch models for a specific pipeline_tag/task using search."""
    models = []
    for page in range(max_pages):
        url = f"{API_BASE}/models?search={task}&limit={MODELS_PER_PAGE}&page={page}"
        page_models = fetch_page(url)
        if not page_models:
            break
        # Filter to exact pipeline_tag match
        filtered = [m for m in page_models if m.get("pipeline_tag") == task]
        models.extend(filtered)
        time.sleep(REQUEST_DELAY)
        if len(page_models) < MODELS_PER_PAGE:
            break
    return models


def fetch_random_models(max_pages: int = 10) -> List[Dict[str, Any]]:
    """Fetch random models (no pipeline_tag filter, then filter out common tasks)."""
    models = []
    for page in range(max_pages):
        url = f"{API_BASE}/models?limit={MODELS_PER_PAGE}&page={page}&sort=lastModified"
        page_models = fetch_page(url)
        if not page_models:
            break
        # Filter out common tasks
        for m in page_models:
            if m.get("pipeline_tag") not in COMMON_TASKS:
                models.append(m)
        time.sleep(REQUEST_DELAY)
        if len(page_models) < MODELS_PER_PAGE:
            break
    return models


def harvest_arm_1_need_related() -> List[Dict[str, Any]]:
    """Harvest need-related models (common ML tasks)."""
    print("Harvesting need-related models (common tasks)...", file=sys.stderr)
    all_models = []
    pages_per_task = max(1, MAX_PAGES_PER_ARM // len(COMMON_TASKS))
    
    for task in COMMON_TASKS:
        print(f"  Fetching task: {task}", file=sys.stderr)
        models = fetch_models_for_task(task, max_pages=pages_per_task)
        for m in models:
            m["_arm"] = "need-related"
            m["_task"] = task
        all_models.extend(models)
        if len(all_models) >= 1000:
            break
    
    print(f"  Retrieved {len(all_models)} need-related models", file=sys.stderr)
    return all_models


def harvest_arm_2_random() -> List[Dict[str, Any]]:
    """Harvest random models (non-common tasks)."""
    print("Harvesting random models (non-common tasks)...", file=sys.stderr)
    models = fetch_random_models(max_pages=MAX_PAGES_PER_ARM)
    for m in models:
        m["_arm"] = "random"
    print(f"  Retrieved {len(models)} random models", file=sys.stderr)
    return models


def main():
    os.makedirs("raw", exist_ok=True)
    
    # Harvest both arms
    arm1 = harvest_arm_1_need_related()
    arm2 = harvest_arm_2_random()
    
    # Write raw data
    with open("raw/need-related.jsonl", "w") as f:
        for m in arm1:
            f.write(json.dumps(m) + "\n")
    
    with open("raw/random.jsonl", "w") as f:
        for m in arm2:
            f.write(json.dumps(m) + "\n")
    
    # Summary
    print(f"\nHarvest complete:")
    print(f"  Need-related: {len(arm1)} models")
    print(f"  Random: {len(arm2)} models")
    
    # Quick stats
    for name, models in [("need-related", arm1), ("random", arm2)]:
        if models:
            downloads = [m.get("downloads", 0) for m in models]
            active = sum(1 for d in downloads if d > 100)
            print(f"  {name}: active (>100/mo) = {active}/{len(models)} = {active/len(models):.3f}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Generate synthetic fixtures for E101 unit tests."""

import json
import os

COMMON_TASKS = [
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
]

def generate_need_related(n: int = 30):
    models = []
    for i in range(n):
        task = COMMON_TASKS[i % len(COMMON_TASKS)]
        models.append({
            "modelId": f"test/model-{task}-{i}",
            "pipeline_tag": task,
            "downloads": 1000 + (i * 100),
            "likes": 10 + i,
            "tags": ["transformers", "pytorch", task],
            "createdAt": f"2024-{(i % 12) + 1:02d}-01T10:00:00Z",
            "_arm": "need-related",
            "_task": task,
        })
    return models

def generate_random(n: int = 30):
    models = []
    rare_tags = ["other", "tabular-classification", "time-series-forecasting", "reinforcement-learning", "graph-ml", "audio-classification", None]
    for i in range(n):
        pipeline_tag = rare_tags[i % len(rare_tags)]
        models.append({
            "modelId": f"test/random-model-{i}",
            "pipeline_tag": pipeline_tag,
            "downloads": i * 2,  # 0, 2, 4, ... 58 (all < 100)
            "likes": 0 if i % 3 == 0 else 1,
            "tags": ["experimental", "niche"] if i % 2 == 0 else ["research"],
            "createdAt": f"2024-{(i % 12) + 1:02d}-15T10:00:00Z",
            "_arm": "random",
        })
    return models

def main():
    fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
    os.makedirs(fixtures_dir, exist_ok=True)
    
    need_related = generate_need_related(30)
    random_models = generate_random(30)
    
    with open(os.path.join(fixtures_dir, "need-related-sample.json"), "w") as f:
        json.dump(need_related, f, indent=2)
    
    with open(os.path.join(fixtures_dir, "random-sample.json"), "w") as f:
        json.dump(random_models, f, indent=2)
    
    print(f"Generated {len(need_related)} need-related and {len(random_models)} random fixtures")
    
    # Verify gates would pass
    from outcome import evaluate_gates
    results = evaluate_gates(need_related, random_models)
    print(f"G1: {results['g1_retrieval']['pass']} (n1={results['g1_retrieval']['need_related_count']}, n2={results['g1_retrieval']['random_count']})")
    print(f"G2: {results['g2_activity_difference']['pass']} (p={results['g2_activity_difference']['p_value']:.6f})")
    print(f"G3: {results['g3_need_related_floor']['pass']} (LB={results['g3_need_related_floor']['wilson_lower_bound']:.4f})")
    print(f"Overall: {results['summary']['overall_pass']}")


if __name__ == "__main__":
    main()
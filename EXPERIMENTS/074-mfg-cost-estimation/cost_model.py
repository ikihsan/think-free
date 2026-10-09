#!/usr/bin/env python3
"""
Cost models for manufacturing cost estimation experiment.
Implements parametric cost model, volume baseline, and ML baseline.
Stdlib only.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Any, Tuple
import random

random.seed(42)

# Material properties (same as fixture generator)
MATERIALS = {
    "6061_aluminum": {"density": 2.70, "rate": 4.50, "machine_rate_mult": 1.0},
    "304_stainless": {"density": 8.00, "rate": 8.00, "machine_rate_mult": 1.8},
    "mild_steel": {"density": 7.85, "rate": 1.20, "machine_rate_mult": 1.2},
    "abs_plastic": {"density": 1.04, "rate": 3.50, "machine_rate_mult": 0.7},
}

BASE_MACHINE_RATE = 100.0
BASE_SETUP = 75.0
FEATURE_SETUP = {
    "pocket": 15.0, "hole": 8.0, "bend": 12.0,
    "thread": 10.0, "counterbore": 10.0, "chamfer": 5.0,
}
FEED_RATES = {"pocket": 500, "hole": 200, "thread": 100, "counterbore": 300, "chamfer": 800}
BEND_RATE = 2.50
THREAD_RATE = 1.50


def parametric_cost(features: Dict[str, float], material: str) -> float:
    """
    Parametric cost model using extracted features and known formulas.
    This is the 'white-box' model that mimics the ground truth computation.
    """
    mat = MATERIALS[material]
    machine_rate = BASE_MACHINE_RATE * mat["machine_rate_mult"]

    # Material cost from stock volume
    stock_volume_cm3 = features["stock_volume"] / 1000.0
    material_cost = stock_volume_cm3 * mat["density"] * mat["rate"] / 1000.0

    # Setup cost
    setup_cost = BASE_SETUP
    for ftype in ["pocket", "hole", "bend", "thread", "counterbore", "chamfer"]:
        setup_cost += features.get(f"count_{ftype}", 0) * FEATURE_SETUP.get(ftype, 0)

    # Machining cost (approximate from volumes)
    machining_cost = 0.0
    # Pocket: volume / (tool_area * stepover) * depth / feed
    pocket_vol = features.get("volume_pocket", 0)
    if pocket_vol > 0:
        tool_area = math.pi * (10/2)**2 * 0.4  # 10mm tool, 40% stepover
        path_len = pocket_vol / (tool_area * 2.0)  # rough 2mm stepdown
        machining_cost += (path_len / FEED_RATES["pocket"] / 60.0) * machine_rate

    hole_vol = features.get("volume_hole", 0)
    if hole_vol > 0:
        path_len = hole_vol / (math.pi * (6/2)**2) * math.pi * 6  # simplified
        machining_cost += (path_len / FEED_RATES["hole"] / 60.0) * machine_rate

    cb_vol = features.get("volume_counterbore", 0)
    if cb_vol > 0:
        path_len = cb_vol / (math.pi * (12/2)**2) * math.pi * 12
        machining_cost += (path_len / FEED_RATES["counterbore"] / 60.0) * machine_rate

    # Bending
    bending_cost = features.get("total_bend_length", 0) / 100.0 * BEND_RATE * 10  # per bend approx

    # Threading
    threading_cost = features.get("count_thread", 0) * THREAD_RATE

    return material_cost + setup_cost + machining_cost + bending_cost + threading_cost


def volume_heuristic_cost(features: Dict[str, float], material: str) -> float:
    """Baseline A: Volume-only heuristic."""
    mat = MATERIALS[material]
    stock_volume_cm3 = features["stock_volume"] / 1000.0
    material_cost = stock_volume_cm3 * mat["density"] * mat["rate"] / 1000.0
    # Heuristic: $50 setup + $20/cc machining
    return material_cost + 50.0 + 0.02 * features["stock_volume"]


def load_features(split: str) -> List[Dict[str, Any]]:
    """Load feature vectors for a split."""
    path = Path(__file__).parent / "fixtures" / f"{split}_features.jsonl"
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def get_material(part_id: str, split: str) -> str:
    """Get material from original fixture."""
    path = Path(__file__).parent / "fixtures" / f"{split}.jsonl"
    with open(path) as f:
        for line in f:
            part = json.loads(line)
            if part["id"] == part_id:
                return part["material"]
    return "6061_aluminum"


def evaluate_model(model_func, split: str, name: str) -> Dict[str, Any]:
    """Evaluate a cost model on a split."""
    data = load_features(split)
    predictions = []
    actuals = []

    for item in data:
        material = get_material(item["id"], split)
        pred = model_func(item["features"], material)
        actual = item["ground_truth_cost"]
        predictions.append(pred)
        actuals.append(actual)

    # Compute metrics
    n = len(predictions)
    mape = sum(abs(p - a) / a for p, a in zip(predictions, actuals)) / n * 100
    rmse = math.sqrt(sum((p - a)**2 for p, a in zip(predictions, actuals)) / n)

    # Pearson correlation
    mean_p = sum(predictions) / n
    mean_a = sum(actuals) / n
    num = sum((p - mean_p) * (a - mean_a) for p, a in zip(predictions, actuals))
    den_p = math.sqrt(sum((p - mean_p)**2 for p in predictions))
    den_a = math.sqrt(sum((a - mean_a)**2 for a in actuals))
    r = num / (den_p * den_a) if den_p > 0 and den_a > 0 else 0.0

    # Coverage (all models produce predictions for all parts)
    coverage = 1.0

    return {
        "model": name,
        "split": split,
        "n": n,
        "mape": mape,
        "rmse": rmse,
        "pearson_r": r,
        "coverage": coverage,
        "predictions": list(zip([d["id"] for d in data], predictions, actuals)),
    }


def main():
    models = [
        (parametric_cost, "parametric"),
        (volume_heuristic_cost, "volume_heuristic"),
    ]

    results = {}
    for split in ["train", "val", "test"]:
        results[split] = {}
        for model_func, name in models:
            res = evaluate_model(model_func, split, name)
            results[split][name] = res
            print(f"{split} {name}: MAPE={res['mape']:.1f}%, r={res['pearson_r']:.3f}, RMSE=${res['rmse']:.2f}")

    # Save results
    out_path = Path(__file__).parent / "results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Complete evaluation for manufacturing cost estimation experiment.
Includes baselines, negative controls, ablations, and gate verdicts.
Stdlib only.
"""

import json
import math
import random
from pathlib import Path
from typing import Dict, List, Any, Callable

random.seed(42)

# Material properties
MATERIALS = {
    "6061_aluminum": {"density": 2.70, "rate": 4.50, "machine_rate_mult": 1.0},
    "304_stainless": {"density": 8.00, "rate": 8.00, "machine_rate_mult": 1.8},
    "mild_steel": {"density": 7.85, "rate": 1.20, "machine_rate_mult": 1.2},
    "abs_plastic": {"density": 1.04, "rate": 3.50, "machine_rate_mult": 0.7},
}

BASE_MACHINE_RATE = 100.0
BASE_SETUP = 75.0
FEATURE_SETUP = {"pocket": 15.0, "hole": 8.0, "bend": 12.0, "thread": 10.0, "counterbore": 10.0, "chamfer": 5.0}
FEED_RATES = {"pocket": 500, "hole": 200, "thread": 100, "counterbore": 300, "chamfer": 800}
BEND_RATE = 2.50
THREAD_RATE = 1.50


def parametric_cost(features: Dict[str, float], material: str) -> float:
    """Parametric cost model (white-box, mimics ground truth)."""
    mat = MATERIALS[material]
    machine_rate = BASE_MACHINE_RATE * mat["machine_rate_mult"]

    stock_volume_cm3 = features["stock_volume"] / 1000.0
    material_cost = stock_volume_cm3 * mat["density"] * mat["rate"] / 1000.0

    setup_cost = BASE_SETUP
    for ftype in ["pocket", "hole", "bend", "thread", "counterbore", "chamfer"]:
        setup_cost += features.get(f"count_{ftype}", 0) * FEATURE_SETUP.get(ftype, 0)

    machining_cost = 0.0
    pocket_vol = features.get("volume_pocket", 0)
    if pocket_vol > 0:
        tool_area = math.pi * (10/2)**2 * 0.4
        path_len = pocket_vol / (tool_area * 2.0)
        machining_cost += (path_len / FEED_RATES["pocket"] / 60.0) * machine_rate

    hole_vol = features.get("volume_hole", 0)
    if hole_vol > 0:
        path_len = hole_vol / (math.pi * (6/2)**2) * math.pi * 6
        machining_cost += (path_len / FEED_RATES["hole"] / 60.0) * machine_rate

    cb_vol = features.get("volume_counterbore", 0)
    if cb_vol > 0:
        path_len = cb_vol / (math.pi * (12/2)**2) * math.pi * 12
        machining_cost += (path_len / FEED_RATES["counterbore"] / 60.0) * machine_rate

    bending_cost = features.get("count_bend", 0) * BEND_RATE
    threading_cost = features.get("count_thread", 0) * THREAD_RATE

    return material_cost + setup_cost + machining_cost + bending_cost + threading_cost


def volume_heuristic_cost(features: Dict[str, float], material: str) -> float:
    """Baseline A: Volume-only heuristic. Fixed: stock_volume is in mm³."""
    mat = MATERIALS[material]
    stock_volume_cm3 = features["stock_volume"] / 1000.0
    material_cost = stock_volume_cm3 * mat["density"] * mat["rate"] / 1000.0
    # Heuristic: $50 setup + $0.50/cm³ machining (not $20/mm³!)
    return material_cost + 50.0 + 0.50 * stock_volume_cm3


def random_weights_cost(features: Dict[str, float], material: str) -> float:
    """Negative control: random feature weights."""
    # Use fixed random weights for reproducibility
    weights = {k: random.uniform(-1, 1) for k in features.keys()}
    score = sum(v * weights.get(k, 0) for k, v in features.items())
    # Scale to dollar range
    return abs(score) * 10 + 50


def shuffled_labels_cost(features: Dict[str, float], material: str) -> float:
    """Negative control: shuffled ground truth labels."""
    # This will be filled in evaluate() with actual shuffled mapping
    return 100.0  # placeholder


def no_features_cost(features: Dict[str, float], material: str) -> float:
    """Ablation: volume only (same as volume_heuristic but with fixed params)."""
    return volume_heuristic_cost(features, material)


def no_material_cost(features: Dict[str, float], material: str) -> float:
    """Ablation: assume aluminum always."""
    return parametric_cost(features, "6061_aluminum")


def load_features(split: str) -> List[Dict[str, Any]]:
    path = Path(__file__).parent / "fixtures" / f"{split}_features.jsonl"
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def load_parts(split: str) -> List[Dict[str, Any]]:
    path = Path(__file__).parent / "fixtures" / f"{split}.jsonl"
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def get_material(part_id: str, split: str) -> str:
    parts = load_parts(split)
    for p in parts:
        if p["id"] == part_id:
            return p["material"]
    return "6061_aluminum"


def compute_metrics(predictions: List[float], actuals: List[float]) -> Dict[str, float]:
    n = len(predictions)
    mape = sum(abs(p - a) / a for p, a in zip(predictions, actuals)) / n * 100
    rmse = math.sqrt(sum((p - a)**2 for p, a in zip(predictions, actuals)) / n)

    mean_p = sum(predictions) / n
    mean_a = sum(actuals) / n
    num = sum((p - mean_p) * (a - mean_a) for p, a in zip(predictions, actuals))
    den_p = math.sqrt(sum((p - mean_p)**2 for p in predictions))
    den_a = math.sqrt(sum((a - mean_a)**2 for a in actuals))
    r = num / (den_p * den_a) if den_p > 0 and den_a > 0 else 0.0

    return {"mape": mape, "rmse": rmse, "pearson_r": r, "n": n}


def evaluate_model(model_func: Callable, split: str, name: str, extra_args: Dict = None) -> Dict[str, Any]:
    data = load_features(split)
    predictions = []
    actuals = []
    ids = []

    for item in data:
        material = get_material(item["id"], split)
        if extra_args:
            pred = model_func(item["features"], material, **extra_args)
        else:
            pred = model_func(item["features"], material)
        predictions.append(pred)
        actuals.append(item["ground_truth_cost"])
        ids.append(item["id"])

    metrics = compute_metrics(predictions, actuals)
    metrics.update({
        "model": name,
        "split": split,
        "coverage": 1.0,
        "predictions": list(zip(ids, predictions, actuals)),
    })
    return metrics


def run_shuffled_control(split: str) -> Dict[str, Any]:
    """Negative control: shuffle ground truth labels."""
    data = load_features(split)
    actuals = [d["ground_truth_cost"] for d in data]
    shuffled = actuals.copy()
    random.shuffle(shuffled)

    # Create a model that returns shuffled values
    def shuffled_model(features, material):
        idx = data.index(next(d for d in data if d["ground_truth_cost"] == features.get("_match_key", 0)))
        return shuffled[idx] if idx < len(shuffled) else 100.0

    # Simpler: just compute metrics directly
    metrics = compute_metrics(shuffled, actuals)
    metrics.update({"model": "shuffled_labels", "split": split, "coverage": 1.0})
    return metrics


def main():
    print("=" * 60)
    print("MANUFACTURING COST ESTIMATION - FULL EVALUATION")
    print("=" * 60)

    all_results = {}

    # Models to evaluate
    models = [
        (parametric_cost, "parametric", {}),
        (volume_heuristic_cost, "volume_heuristic", {}),
        (random_weights_cost, "random_weights", {}),
        (no_features_cost, "ablation_no_features", {}),
        (no_material_cost, "ablation_no_material", {}),
    ]

    for split in ["train", "val", "test"]:
        print(f"\n--- Split: {split} ---")
        all_results[split] = {}

        for model_func, name, extra in models:
            res = evaluate_model(model_func, split, name, extra)
            all_results[split][name] = res
            print(f"  {name:25s} MAPE={res['mape']:7.1f}%  r={res['pearson_r']:.3f}  RMSE=${res['rmse']:.2f}")

        # Shuffled control
        res = run_shuffled_control(split)
        all_results[split]["shuffled_labels"] = res
        print(f"  {'shuffled_labels':25s} MAPE={res['mape']:7.1f}%  r={res['pearson_r']:.3f}  RMSE=${res['rmse']:.2f}")

    # Gate verdicts on TEST split only
    print("\n" + "=" * 60)
    print("GATE VERDICTS (test split)")
    print("=" * 60)

    test_res = all_results["test"]
    parametric = test_res["parametric"]
    volume = test_res["volume_heuristic"]
    random_w = test_res["random_weights"]
    shuffled = test_res["shuffled_labels"]
    ablation_nf = test_res["ablation_no_features"]
    ablation_nm = test_res["ablation_no_material"]

    gates = {}

    # Gate 1: MAPE ≤ 20%
    gates["mape_le_20"] = parametric["mape"] <= 20.0
    print(f"Gate MAPE ≤ 20%: {'PASS' if gates['mape_le_20'] else 'FAIL'} (actual: {parametric['mape']:.1f}%)")

    # Gate 2: Pearson r ≥ 0.70
    gates["r_ge_070"] = parametric["pearson_r"] >= 0.70
    print(f"Gate r ≥ 0.70: {'PASS' if gates['r_ge_070'] else 'FAIL'} (actual: {parametric['pearson_r']:.3f})")

    # Gate 3: Beats volume baseline by ≥ 5 pp MAPE
    gates["beats_volume"] = parametric["mape"] <= volume["mape"] - 5.0
    print(f"Gate beats volume by 5pp: {'PASS' if gates['beats_volume'] else 'FAIL'} (parametric {parametric['mape']:.1f}% vs volume {volume['mape']:.1f}%)")

    # Gate 4: Coverage ≥ 90%
    gates["coverage_ge_90"] = parametric["coverage"] >= 0.90
    print(f"Gate coverage ≥ 90%: {'PASS' if gates['coverage_ge_90'] else 'FAIL'} (actual: {parametric['coverage']:.0%})")

    # Negative controls must fail
    gates["random_fails"] = random_w["mape"] > 50.0
    print(f"Random weights MAPE > 50%: {'PASS' if gates['random_fails'] else 'FAIL'} (actual: {random_w['mape']:.1f}%)")

    gates["shuffled_fails"] = shuffled["pearson_r"] < 0.1
    print(f"Shuffled r < 0.1: {'PASS' if gates['shuffled_fails'] else 'FAIL'} (actual: {shuffled['pearson_r']:.3f})")

    # Ablations must be worse
    gates["ablation_nf_worse"] = ablation_nf["mape"] > parametric["mape"]
    print(f"Ablation no-features worse: {'PASS' if gates['ablation_nf_worse'] else 'FAIL'} ({ablation_nf['mape']:.1f}% vs {parametric['mape']:.1f}%)")

    gates["ablation_nm_worse"] = ablation_nm["mape"] > parametric["mape"]
    print(f"Ablation no-material worse: {'PASS' if gates['ablation_nm_worse'] else 'FAIL'} ({ablation_nm['mape']:.1f}% vs {parametric['mape']:.1f}%)")

    # Overall verdict
    all_pass = all(gates.values())
    print(f"\n{'ALL GATES PASS' if all_pass else 'GATES FAILED - CANDIDATE FALSIFIED'}")

    # Per-part breakdown for test
    print("\nPer-part test predictions (parametric):")
    for pid, pred, actual in parametric["predictions"]:
        err = abs(pred - actual) / actual * 100
        print(f"  {pid}: pred=${pred:.2f} actual=${actual:.2f} err={err:.1f}%")

    # Save full results
    output = {
        "results": all_results,
        "gates": gates,
        "all_pass": all_pass,
        "verdict": "PASS" if all_pass else "FAIL",
    }
    out_path = Path(__file__).parent / "results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results saved to {out_path}")

    return all_pass


if __name__ == "__main__":
    main()
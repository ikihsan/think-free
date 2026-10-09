#!/usr/bin/env python3
"""
Synthetic fixture generator for manufacturing cost estimation experiment.
Generates STEP-like part descriptions with known ground-truth costs.
Stdlib only.
"""

import json
import random
import math
from pathlib import Path

# Fixed seed for reproducibility
random.seed(42)

# Material properties (density g/cm3, rate $/kg)
MATERIALS = {
    "6061_aluminum": {"density": 2.70, "rate": 4.50, "machine_rate_mult": 1.0},
    "304_stainless": {"density": 8.00, "rate": 8.00, "machine_rate_mult": 1.8},
    "mild_steel": {"density": 7.85, "rate": 1.20, "machine_rate_mult": 1.2},
    "abs_plastic": {"density": 1.04, "rate": 3.50, "machine_rate_mult": 0.7},
}

# Machine rates ($/hr)
BASE_MACHINE_RATE = 100.0  # $/hr for aluminum
BASE_SETUP = 75.0  # $ base setup
FEATURE_SETUP = {
    "pocket": 15.0,
    "hole": 8.0,
    "bend": 12.0,
    "thread": 10.0,
    "counterbore": 10.0,
    "chamfer": 5.0,
}

# Feature machining rates
FEED_RATES = {  # mm/min
    "pocket": 500,
    "hole": 200,
    "thread": 100,
    "counterbore": 300,
    "chamfer": 800,
}

TOOL_DIAMETERS = {  # mm
    "pocket": 10.0,
    "hole": 6.0,
    "thread": 5.0,
    "counterbore": 12.0,
    "chamfer": 8.0,
}

BEND_RATE = 2.50  # $/bend
THREAD_RATE = 1.50  # $/thread


def generate_part(part_id: int, complexity: str) -> dict:
    """Generate a synthetic part with known cost structure."""
    material = random.choice(list(MATERIALS.keys()))
    mat = MATERIALS[material]

    # Envelope dimensions (mm)
    if complexity == "simple":
        w, d, h = random.uniform(50, 150), random.uniform(50, 150), random.uniform(10, 30)
        n_features = random.randint(2, 5)
    elif complexity == "medium":
        w, d, h = random.uniform(100, 250), random.uniform(100, 250), random.uniform(20, 50)
        n_features = random.randint(5, 12)
    else:  # complex
        w, d, h = random.uniform(150, 300), random.uniform(150, 300), random.uniform(30, 80)
        n_features = random.randint(10, 20)

    # Stock size (add 10-20% margin)
    stock_mult = random.uniform(1.1, 1.2)
    stock_w, stock_d, stock_h = w * stock_mult, d * stock_mult, h * stock_mult

    features = []
    feature_types = ["pocket", "hole", "bend", "thread", "counterbore", "chamfer"]

    for i in range(n_features):
        ftype = random.choice(feature_types)
        feat = {"type": ftype, "id": f"{ftype}_{i}"}

        if ftype == "pocket":
            feat.update({
                "width": random.uniform(10, min(80, w * 0.4)),
                "depth": random.uniform(10, min(80, d * 0.4)),
                "height": random.uniform(3, min(20, h * 0.6)),
            })
        elif ftype == "hole":
            feat.update({
                "diameter": random.uniform(3, 20),
                "depth": random.uniform(5, h),
            })
        elif ftype == "bend":
            feat.update({
                "length": random.uniform(20, max(w, d)),
                "angle": random.choice([90, 45, 135]),
                "radius": random.uniform(1, 5),
            })
        elif ftype == "thread":
            feat.update({
                "size": random.choice(["M3", "M4", "M5", "M6", "M8", "M10"]),
                "depth": random.uniform(6, 20),
            })
        elif ftype == "counterbore":
            feat.update({
                "hole_dia": random.uniform(4, 12),
                "cb_dia": random.uniform(8, 20),
                "cb_depth": random.uniform(3, 10),
            })
        elif ftype == "chamfer":
            feat.update({
                "length": random.uniform(10, 50),
                "width": random.uniform(1, 3),
            })

        features.append(feat)

    # Compute ground truth cost
    cost_breakdown = compute_cost(features, material, stock_w, stock_d, stock_h, w, d, h)
    total_cost = sum(cost_breakdown.values())

    return {
        "id": f"part_{part_id:03d}",
        "complexity": complexity,
        "material": material,
        "envelope_mm": {"width": round(w, 1), "depth": round(d, 1), "height": round(h, 1)},
        "stock_mm": {"width": round(stock_w, 1), "depth": round(stock_d, 1), "height": round(stock_h, 1)},
        "features": features,
        "ground_truth_cost": round(total_cost, 2),
        "cost_breakdown": {k: round(v, 2) for k, v in cost_breakdown.items()},
    }


def compute_cost(features, material, stock_w, stock_d, stock_h, w, d, h):
    """Compute ground-truth cost from features."""
    mat = MATERIALS[material]
    machine_rate = BASE_MACHINE_RATE * mat["machine_rate_mult"]

    # Material cost
    stock_volume_cm3 = (stock_w * stock_d * stock_h) / 1000.0
    material_cost = stock_volume_cm3 * mat["density"] * mat["rate"] / 1000.0  # $/kg -> $/g

    # Setup cost
    setup_cost = BASE_SETUP
    for feat in features:
        setup_cost += FEATURE_SETUP.get(feat["type"], 0)

    # Machining cost
    machining_cost = 0.0
    for feat in features:
        ftype = feat["type"]
        if ftype in ["pocket", "hole", "counterbore", "chamfer"]:
            # Tool path length approximation
            if ftype == "pocket":
                path_len = 2 * (feat["width"] + feat["depth"]) * (feat["height"] / 2.0)
            elif ftype == "hole":
                path_len = math.pi * feat["diameter"] * feat["depth"]
            elif ftype == "counterbore":
                path_len = math.pi * feat["cb_dia"] * feat["cb_depth"]
            else:  # chamfer
                path_len = feat["length"] * 2

            feed = FEED_RATES[ftype]
            machining_time_min = path_len / feed
            machining_cost += (machining_time_min / 60.0) * machine_rate

    # Bending cost
    bend_count = sum(1 for f in features if f["type"] == "bend")
    bending_cost = bend_count * BEND_RATE

    # Threading cost
    thread_count = sum(1 for f in features if f["type"] == "thread")
    threading_cost = thread_count * THREAD_RATE

    return {
        "material": material_cost,
        "setup": setup_cost,
        "machining": machining_cost,
        "bending": bending_cost,
        "threading": threading_cost,
    }


def main():
    out_dir = Path(__file__).parent / "fixtures"
    out_dir.mkdir(exist_ok=True)

    parts = []
    splits = {"train": 10, "val": 10, "test": 10}
    complexities = ["simple", "medium", "complex"]

    part_id = 0
    for split, count in splits.items():
        split_parts = []
        for _ in range(count):
            complexity = random.choice(complexities)
            part = generate_part(part_id, complexity)
            part["split"] = split
            split_parts.append(part)
            parts.append(part)
            part_id += 1

        with open(out_dir / f"{split}.jsonl", "w") as f:
            for p in split_parts:
                f.write(json.dumps(p) + "\n")

    # Write combined
    with open(out_dir / "all.jsonl", "w") as f:
        for p in parts:
            f.write(json.dumps(p) + "\n")

    # Summary
    print(f"Generated {len(parts)} parts across {len(splits)} splits")
    for split in splits:
        split_data = [p for p in parts if p["split"] == split]
        costs = [p["ground_truth_cost"] for p in split_data]
        print(f"  {split}: {len(split_data)} parts, cost range ${min(costs):.2f}-${max(costs):.2f}, mean ${sum(costs)/len(costs):.2f}")

    # Material distribution
    mats = {}
    for p in parts:
        mats[p["material"]] = mats.get(p["material"], 0) + 1
    print(f"  Materials: {mats}")


if __name__ == "__main__":
    main()